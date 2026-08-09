# FRD — Review-Engine Reliability & Scale (Kody/Kodus code-review backend)

Status: draft v1 · 2026-07-29 · owner: Erik + Lead
Source: full review-pipeline **outage during the live E0 #355 loop on PR #362** (2026-07-29). Triggered by the product question *"can Kody handle ~100 customers, and can these issues be ironed out so it works most of the time?"* The review engine (Kody/Kodus) **is** the code-review surface Modula would offer customers, so its reliability and scale are **product requirements**, not one-off ops fixes.
Related: `coms-reliability-audit-2026-07-29.md`, `frd-review-fix-controller-draft.md` (convergence controller — sits *above* this engine), `frd-term-1-fully-functional.md` (F-23: Kody-on-Forgejo), `git-host-migration-roadmap.md`, `forgejo-cutover-flip-runbook.md`. Runbook: memory `kody-review-trigger-runbook`.

## 1. Problem

Today the code-review engine is a **single-tenant dogfood configuration** that took a **full outage mid-loop**: every review on PR #362 failed for ~90 minutes across three distinct signatures, invisible until each attempt returned "Could Not Complete" ~20 min later. Recovery required hand-diagnosis of a hung LLM gateway and a Docker DNS drop. Two separate questions follow, with two different answers:

- **(a) Reliable enough for our own dogfood use?** Yes — fixable cheaply (Phase 0 below).
- **(b) Production-grade for ~100 customers?** **No, not as architected.** The bugs we hit are symptoms; the disease is the LLM backend — a single home-grown process wrapping a developer-CLI, with a hard 10-way concurrency ceiling, a memory leak, and no redundancy.

This FRD separates the two halves of the stack, states which scales and which does not, and defines a phased path from "works for us" to "works for 100 tenants most of the time."

## 2. Grounded facts (verified 2026-07-29 during the PR #362 incident)

The stack is the `kodus-installer` compose project at `/home/hyperbots/agentops-kodus-101/docker-sandbox/kodus-installer` plus a systemd `--user` LLM gateway. **Two failure classes — do not conflate:** (A) the Kodus *application* (webhooks→queue→worker→post), (B) the *LLM backend* (`kodus-max-gateway` + Codex CLI). Facts G-1..G-7 are class B (the weak point); K-1..K-6 are class A.

| # | Fact | Evidence |
|---|---|---|
| G-1 | The LLM provider is a **single home-grown Python process** wrapping the **Codex CLI**, on one host/port | `ExecStart=/usr/bin/python3 -m agentops_harness.kodus_max_gateway --backend codex --host 172.17.0.1 --port 18082 --timeout 1500 --max-concurrency 10 --queue-timeout 900 --codex-cwd /mnt/…/worktrees/agentops-prd-1102`; systemd `--user` unit `kodus-max-gateway.service` |
| G-2 | **Hard concurrency ceiling of 10 reviews, total, process-wide.** Excess queues behind a 15-min `--queue-timeout` then fails | `--max-concurrency 10 --queue-timeout 900` (G-1) |
| G-3 | **Single point of failure.** One process on `172.17.0.1:18082`, no redundancy, no load balancer — its hang blocks *all* reviews for *all* tenants | one PID; incident: gateway hang → every PR #362 review failed |
| G-4 | **Memory leak → hang.** Ran ~28h, peaked **13.1 GB**, stopped answering HTTP (accepts socket, never returns headers) → "Headers Timeout Error" / "Cannot connect to API" | journal on restart: `Consumed 49min CPU … 13.1G memory peak`; `curl 172.17.0.1:18082/` = `000` while hung, `404` (serving) after restart |
| G-5 | **Backend is repo-coupled to a single git worktree** — does not cleanly fan out across many tenants' repositories | `--codex-cwd /mnt/…/worktrees/agentops-prd-1102`; `WorkingDirectory=/mnt/…/repos/agentops-harness` |
| G-6 | **Worker→gateway link is DNS-fragile.** Worker reaches the gateway only via `host.docker.internal`, which exists solely because compose declares `extra_hosts: host.docker.internal:host-gateway`. A plain `docker restart` recreates `/etc/hosts` without it → instant `ENOTFOUND`, every review fast-fails in ~6s | `API_OPENAI_FORCE_BASE_URL=http://host.docker.internal:18082/v1`; post-`docker restart` `ExtraHosts:[]`; fix = `docker compose … up -d --force-recreate` |
| G-7 | **A just-recreated worker needs ~30s before its provider connection is stable** — a trigger fired against a <1-min-old worker posts a transient "reaching the provider" failure | incident: trigger #10720 at worker-age ~35s → transient fail #10721; same trigger at worker-age 23min → review ran clean |
| K-1 | The Kodus **application is genuinely multi-tenant** — org/team scoped throughout | logs carry `organizationId`, `teamId`, `organizationName:"ops.evono.me"` per review |
| K-2 | **Queue-based, horizontally scalable orchestration** (the right shape for scale) | worker registers RabbitMQ consumers on `workflow.exchange` (`workflow.jobs.*`), health probe on `:3334/health` (6 channels) |
| K-3 | **Only one worker replica** runs today | single `kodus-worker-prod` container in `docker ps` |
| K-4 | Stateful deps: **Postgres + Mongo**, single instances; whole stack crash-loops if a DB drops | `db_kodus_postgres`, `db_kodus_mongodb`; prior incident PR #284 (memory `kody-review-trigger-runbook` mode 1) |
| K-5 | **No health-gate before firing a review, and failures are invisible for ~20 min.** A sick pipeline is only discovered when the review returns "Could Not Complete" | incident: 3 failed rounds each surfaced ~20 min post-trigger |
| K-6 | A **reaper for dropped triggers exists** but did not prevent or surface the outage | `kodus-review-reaper.service` present; no proactive alert fired |
| K-7 | **Reap-window churn.** The reaper marks any review `in_progress > 25 min` stale and re-triggers it. A normal review takes ~20 min, so it races the threshold — a slightly-slow review is reaped mid-flight and re-fired, generating duplicate work and a moving target for callers | `kodus-review-reaper.py --interval 120`, SQL `updatedAt < now() - interval '25 minutes'`; incident: review #10722 (20:32) reaped at 20:57 → re-fired #10725 |
| K-8 | **Data tier is already slow enough to break recovery.** The reaper's Postgres query **timed out at 30s** during the incident — the review DB is loaded/slow, which both slows reviews and blinds the scanner (K-4) | reaper log 20:44: `subprocess.TimeoutExpired … docker exec db_kodus_postgres psql … timed out after 30 seconds` |

## 3. The two halves — what scales, what does not

- **Half A — the Kodus app (K-1..K-6): scales, with work.** Standard NestJS + RabbitMQ + Postgres/Mongo, org/team multi-tenant, queue-driven workers that scale by replica count. This is **not** the architectural blocker; it needs replica scaling, DB hardening, quotas, and observability — all conventional.
- **Half B — the LLM gateway (G-1..G-7): the real blocker.** Using an **interactive developer CLI (Codex) as a shared production inference backend** through a single hand-rolled process is the root cause of the outage and of the scale ceiling. The 13 GB leak, the concurrency-10 wall, the SPOF, and the repo-coupling are all consequences of that one decision. No amount of bug-fixing changes it; the backend has to change.

**Why the gateway exists (the central tension):** it routes reviews through a **flat-rate Codex subscription** instead of **metered per-token API** calls — a large cost saving at dogfood volume. This FRD does not dismiss that; §7 makes it a tiered, per-plan routing decision rather than an all-or-nothing one.

## 4. Design — phased

### Phase 0 — Harden the current config (internal reliability; do now, ~1–2 days)
Makes our own loop reliable without changing architecture. All non-disruptive except where noted.
- **P0-1 Memory-bound the gateway:** `MemoryMax=8G` + `Restart=on-failure` + `RestartSec=` on the unit → it recycles *before* it hangs (G-4). Applies live via `systemctl --user set-property` (no restart).
- **P0-2 Liveness watchdog:** a `systemd --user` timer (~90s) that probes gateway `:18082` (`POST /v1/chat/completions` smoke) and worker `:3334/health`; restarts whichever is unresponsive. Turns a hang into a ~90s self-heal (G-3, G-4).
- **P0-3 Pre-flight health-gate on the trigger (highest value):** before any `@kody start-review`, verify gateway + worker completion path healthy; auto-recover if sick, *then* trigger. Converts all three incident signatures from "silent 20-min failure" (K-5) into "review always runs clean." Folds into the git-manager trigger step and the kody-fix-loop daemon.
- **P0-4 Restart discipline:** **never `docker restart`** these containers — always `docker compose … up -d --no-deps --force-recreate <svc>` (G-6). Codify in the runbook (done: memory `kody-review-trigger-runbook` modes 4–5) and, better, wrap in a `kody-restart` script so the fragile path can't be taken by hand.
- **P0-5 Nightly gateway recycle:** scheduled restart to shed the leak until root-caused (G-4). Band-aid, cheap.
- **P0-6 Failure alerting:** alert immediately on a "Could Not Complete" comment or a watchdog restart (K-6) so we hear before a customer would.
- **P0-7 Stop reap-window churn (K-7):** make the reaper's stale threshold **duration-aware** — bound it to *actual* p95 review time with margin (e.g. 2×), or track heartbeat progress instead of a flat 25-min wall, so a legitimately-slow review is not reaped and re-fired while still running. Also index/tune the reaper's `automation_execution` scan so it can't time out (K-8) and blind itself.

### Phase 1 — Replace the LLM backend (the load-bearing change; before any external customer)
- **P1-1 Swap Codex-CLI gateway → a real inference API** (Claude API is the natural fit — config already names the model `claude-cli` / `API_LLM_PROVIDER_MODEL=claude-cli`). Stateless HTTP calls eliminate the leak (G-4), the SPOF (G-3), *and* the concurrency-10 ceiling (G-2) in one move.
- **P1-2 Production client behavior:** retry with exponential backoff, respect the provider's own rate limits as backpressure, circuit-break on sustained provider errors, structured error surfacing (not a generic "transient error").
- **P1-3 Secrets & per-tenant keys:** API-key management, per-tenant quota/rate accounting, no shared single credential.
- **P1-4 Decouple from the worktree (G-5):** review context assembled from the PR diff + rules fetched per-tenant, no `--codex-cwd` filesystem coupling.

### Phase 2 — Horizontal scale + tenant isolation (for the 100-customer target)
- **P2-1 Worker autoscaling:** N `kodus-worker` replicas consuming the RabbitMQ queue (K-2, K-3), sized to the §7 concurrency peak.
- **P2-2 Per-customer quotas & fair scheduling:** one noisy tenant cannot starve the queue for the rest (bounded in-flight per org).
- **P2-3 Data-tier hardening:** Postgres/Mongo connection pooling, backups, and HA so a DB blip doesn't crash-loop the stack (K-4).
- **P2-4 Validate Kodus multi-tenant isolation under load** — confirm org/team scoping (K-1) holds with concurrent cross-tenant reviews; no finding/data bleed.

### Phase 3 — Observability & SLO
- **P3-1** Per-review tracing (queued→started→provider-call→posted) with latency + outcome.
- **P3-2** Dashboards + alerting on success rate, p95 latency, queue depth, provider error rate.
- **P3-3** On-call runbook + capacity dashboard (§7 live).

## 5. Checkpoints

| CP | Scope | Exit criteria |
|----|-------|--------------|
| CP-1 | Phase 0 hardening | Gateway memory-capped + auto-restart; watchdog live; health-gate on every trigger; `kody-restart` script replaces hand `docker restart`; failure alerting fires. **Zero silent failures** over a 1-week bake. |
| CP-2 | Phase 1 backend swap | Codex-CLI gateway retired for the primary path; reviews run on the inference-API backend with backoff/circuit-break; no memory growth; concurrency limited only by provider + worker count. Regression: findings quality ≈ Codex baseline (A/B a sample of PRs). |
| CP-3 | Phase 2 scale/isolation | ≥3 worker replicas; per-tenant quota enforced; DB pooling/HA; load test at the §7 peak passes without cross-tenant starvation or data bleed. |
| CP-4 | Phase 3 observability | Tracing + dashboards + alerting live; SLOs (§6) measured and met over a 2-week window. |

## 6. Acceptance criteria (SLOs)

- **Review success rate ≥ 99%** measured on completed vs. "Could Not Complete" (excludes genuine no-op PRs). ("Works most of the time" made concrete.)
- **No single-process SPOF** in the LLM path (P1/P2 done).
- **Concurrency headroom ≥ the §7 peak with ≥30% margin** — no `--max-concurrency`-style hard wall.
- **Mean-time-to-detect a pipeline fault < 2 min** (watchdog/alert), not ~20 min (K-5).
- **Tenant isolation:** no finding, diff, or credential crosses org boundaries under concurrent load.

## 7. Capacity model (to size Phase 2)

Sizing input, to be filled with real numbers:

`peak_concurrent_reviews ≈ customers × repos_per_customer × PRs_per_repo_per_day × review_minutes / active_minutes_per_day × burst_factor`

Worked illustration — 100 customers, 3 active repos each, 5 PRs/repo/day, ~20 min/review, 8 active hours, burst ×3:
`100 × 3 × 5 = 1,500 reviews/day ≈ 3.1/min avg → ~9.4 concurrent peak at ×3 burst.` A single-digit steady peak, but bursty (a Monday-morning push wave can spike far higher), and **today's ceiling is exactly 10 (G-2)** — i.e. we are already at the wall for even this modest model, with zero margin and no redundancy. Real numbers replace the illustration before CP-3; the point stands: concurrency-10 + one process cannot carry 100 tenants.

## 8. Options & recommendation (the cost tension)

- **Option A — Full inference-API backend (Claude API) for everyone.** Best reliability and scale; highest metered cost. Right for paying customers.
- **Option B — Keep Codex/flat-rate, but make it a real pool.** Multiple gateway instances behind a load balancer, each memory-capped + autoscaled. Cheaper; still carries CLI-as-server fragility and repo-coupling (G-5) — a lot of engineering to make a dev tool behave like a service.
- **Option C — Tiered backend routing by plan (recommended).** Route **internal + free-tier** reviews through the flat-rate Codex pool (Option B, cost-optimized) and **paying customers** through the inference-API backend (Option A, reliability-optimized). Backend selection becomes a per-tenant policy. Keeps the cost win where volume is cheap and quality tolerance is high, and buys production-grade reliability exactly where it's paid for.

**Recommendation: Phase 0 now (regardless), then Option C for Phase 1+.** It resolves the tension that created the gateway in the first place instead of paying its reliability tax on every tenant.

## 9. Non-goals

- **Not** rewriting Kodus — the app (Half A) is sound; we scale and harden it.
- **Not** the review-fix convergence/oscillation controller — that sits *above* this engine (`frd-review-fix-controller-draft.md`).
- **Not** the Forgejo trigger/webhook path — validated separately (Term-1 F-23).

## 10. Open questions

- Real capacity numbers (repos/PRs per customer) — needed to size CP-3.
- Codex flat-rate terms at multi-tenant volume — is Option B even permissible/economical at 100 tenants, or does the free tier also need metering?
- Self-host vs managed Kodus at scale — do we own the data tier (K-4) HA, or move to a managed deployment?
- Does upstream Kodus expose per-tenant backend routing (Option C), or is that a fork/config extension?
