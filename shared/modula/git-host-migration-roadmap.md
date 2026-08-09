# Roadmap PRD: Git-Host Migration to Self-Hosted Forgejo (staged, adapter-first)

Date: 2026-07-24 · Status: **draft roadmap** (promote into the repo PRD flow on a fresh branch) · Owner: agent:agentops
Supersedes the "separate git-host migration PRD" stub referenced in #262 Phase 4.

## 1. Why now

The GitHub **GraphQL 5k/hr shared pool** is the recurring bottleneck of the trio workflow — issue creation, Projects v2 board reads/writes, and board regeneration all hit it, capping parallel lanes at ~4–6 and stalling Modula's own multi-lane dogfooding. This is a workflow-velocity problem, not a feature gap. We escape it by moving the git-host dependency to self-hosted **Forgejo** (no external rate pool, full control) — but **staged**, because a big-bang cutover mid-wave is high-risk and violates #262's "no mass migration while the wave is in flight" rule.

## 2. Current state (facts)

- Forgejo pilot **already running**: `forgejo-test`, Forgejo **15.0.5**, `localhost:3300`, user **ModulaStack** (ID 3, created 2026-07-19).
- Kodus already supports Forgejo (local forge inventory).
- GitHub is canonical; the workflow is deeply `gh`/GraphQL-coupled: PR create (git-town propose), PR state/merge, issue CRUD + comments, labels, **Projects v2 boards (the GraphQL pain)**, Kody webhook targets, board regen.
- No dedicated migration PRD existed before this draft; #262 (rebrand plan) defers it as Phase 4.

## 3. Strategy — three tiers

### Tier A — immediate relief (now, no migration)
- Prioritize **#214 (GitHub API Budget Resilience + Service Token Isolation)**: dedicated service token with its own budget, backoff, and caching.
- **REST-first everywhere** (MW-5): REST has a separate pool from GraphQL — route issues/comments/labels through REST; reserve GraphQL only for Projects v2 (which is GraphQL-only) with caching + backoff.

### Tier B — the enabling adapter (next FRD; the real "start now")
- Build a **git-forge adapter interface** — one contract for: issues (CRUD + comments + labels), pull/merge requests (create, state, merge), boards/status fields, and **PR-state/completion detection** (the "Gitea-style API" adapter #262 names).
- **GitHub backend now + Forgejo backend next**, selected by config per operation/lane.
- **Owner: the Git Manager agent** — this abstraction is the Git Manager's domain, layered on approved **#251** (Git Manager default pane) + **#213** (git lifecycle autonomy) + the MW-19 full-VCS-ownership decision.
- **First win:** route Modula's OWN dogfooding board/issue ops to the Forgejo pilot (kills the biggest GraphQL cost) while GitHub stays canonical for the in-flight wave. Dual-read label mapping (`agent:agentops` ↔ `agent:modula`) during transition.

### Tier C — full cutover (post-wave; its own PRD)
- Migrate repos/history, issues/PRDs, labels, and boards to org **ModulaStack**; replace all `gh`-dependent tooling with the adapter's Forgejo backend; port the completion detector. Gated behind a wave freeze per #262.

## 4. The `gh`/GraphQL surface to abstract

| Concern | Today | Adapter method | Forgejo path |
| --- | --- | --- | --- |
| Issue CRUD + comments + labels | `gh api` REST/GraphQL | `forge.issues.*` | Gitea/Forgejo REST |
| PR create / state / merge | `git town propose`, `gh pr` | `forge.pulls.*` | Forgejo PR API |
| Boards / status fields | **Projects v2 GraphQL** (the pain) | `forge.boards.*` | Forgejo project/labels or external board |
| PR-state / completion detection | GraphQL polling | `forge.completion.detect()` | Gitea-style API / webhook |
| Review trigger | Kody webhook (GitHub event) | `forge.review.request()` | Forgejo webhook → Kodus (already supported) |

## 5. Risks / open decisions

- **Boards are the hardest piece** — Projects v2 is rich; Forgejo's native project boards are simpler. Decide: map to Forgejo projects, or keep an external board store the adapter writes to.
- **Repos under ModulaStack user vs org** (org recommended for team/permissions) — inherited open decision from #262.
- **`gh`-tooling breadth** — git-town, Kody trigger, board regen, coms are all coupled; the adapter must cover each call site (grep-gate the `gh ` / GraphQL call sites as acceptance).
- **No mass migration mid-wave** (#262 safety rule) — Tier C waits for a wave freeze.
- **Kody/Kodus** already supports Forgejo — validate the webhook path against the pilot early.

## 6. Relationships
- **#214** — Tier A relief (fast-track).
- **#251 / #213 / MW-19** — Git Manager owns the adapter (Tier B).
- **#262** — rebrand plan; this roadmap is its Phase 4, expanded.
- **#264** — Kodus Review Reliability (canonical gateway) — align the review-trigger adapter path.

## 7. Operator decisions (2026-07-24, during #286 CP-1)

- **Tier C intent confirmed:** after #286 completes, target state is ALL Modula Stack work on Forgejo — GitHub Project 3 tasks migrated, no GitHub usage for future Modula work. Tier C PRD executes it (still gated on wave freeze per #262).
- **Naming on Forgejo is greenfield Modula-only:** org/repos/labels use `modula-stack` / Modula / ModulaStack naming exclusively. FORBIDDEN on Forgejo: `SoldierOne`, `Project 3`, `agentops`/`agentops-harness` names. Forgejo never inherits legacy naming — this collapses most of #262 Phase 4 rebrand surface for the new host.
- Lead recommendations attached to the decision (to ratify in the Tier C PRD): migrate OPEN Project 3 items only, freeze GitHub as read-only archive (no history rewrite); convert/create a proper **org** (`modula-stack`) rather than the ModulaStack user (roadmap §5 open decision → resolve as org); productionize the pilot (`forgejo-test` on :3300 is a TEST instance — backups, service hardening, non-test naming) before it becomes the canonical host.

## 8. Tier B execution notes (2026-07-24 — prd-286 run, verifier-approved, pending push/PR gate)

Pilot integration gotchas learned live (apply to CP-2-style work and Tier C):
- **Webhook comment events:** subscribing `issue_comment` covers ISSUE comments only; PR comments require the `pull_request_comment` subscription — yet the DELIVERED header still reads `issue_comment` (match on header + `issue.pull_request` in payload).
- **Webhook addressing from the Docker pilot:** container's 127.0.0.1 is itself; host sinks must bind 0.0.0.0 and hooks target the container→host gateway (172.22.0.1 for forgejo-test). `[webhook] ALLOWED_HOST_LIST = private,loopback` already set in app.ini.
- **Branch deletion:** use the PR's `head.ref` with `DELETE /repos/{o}/{r}/branches/{name}` — passing `refs/pull/N/head` 500s. `POST /hooks/{id}/tests` fires an instant push-event test delivery.
- **Account state:** ModulaStack had `must_change_password` set since creation; cleared 2026-07-24 (password in `~/.config/modula/forgejo-adapter.env`, mode 600, alongside the scoped adapter token write:issue,write:repository). Repo-create needed basic auth (`write:user` scope gap).
- **Pilot fragility:** forgejo-test container was found Exited(255) and needed a manual `docker start` — reinforces the productionization prerequisite (§7) before any canonical cutover.
- Validation assets now on the pilot: private repo `ModulaStack/modula-forge-validation` with labels `agent:modula`, `smoke:keep`; live smokes are self-cleaning (repo stays main-only, hooks empty).

## 9. Acceptance (Tier B FRD)
- A `forge` adapter module with GitHub + Forgejo backends and a config selector.
- Modula dogfooding board/issue ops demonstrably running against the Forgejo pilot with zero GitHub GraphQL calls for those ops.
- `git grep` of direct `gh api`/GraphQL call sites for the abstracted concerns → routed through the adapter (measurable before/after).
- Git Manager pane (#251) is the operator of forge ops.
