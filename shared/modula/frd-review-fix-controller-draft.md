# FRD (draft) — Automated Review-Fix Controller

Status: draft · 2026-07-25 · author: lead (Fable 5) · provenance: prd-288 PL1 run (MW-20, MW-28…MW-35)
Umbrella: Modula agent-workflow engine · Related: `modula-workflow-requirements.md`, `operating-model.md`

> **Naming:** deliberately *not* "runner" — **Z4 Modula Runner** (PR #299) is the local execution-plane
> daemon. This FRD is a **control-plane controller** that decides and orchestrates; it owns no execution.

## 0. Relationship to Z4 (execution plane)

Z4 splits Modula into a hosted control plane and a local open-source Runner that spawns the user's own
CLIs in local worktrees, because subscription auth is machine-bound and **no model credential may live
control-plane-side** (master PRD §14 runner doctrine). That doctrine **corrects §4.1 of this draft**: a
review-fix job spawns a CLI in a worktree, so under Z4 the job **executes runner-side, not on the control
plane**. The split is:

| Concern | Plane |
|---|---|
| Fingerprint ledger, convergence classification, precedence rulings, deferral criteria, budgets, decision tiers (§4.2–4.3) | **Control plane** |
| Fix job execution: worktree, CLI invocation, tests/gates, model credential resolution (subscription / api-key / local) | **Runner (local)** |
| Triage report, observability surface, human gates | **Control plane** |

Consequences to carry into the final FRD:
- Job dispatch and result return ride the **shared runner seam** (`docs/runner-seam.md` + versioned
  protocol schema), which is also consumed by Z3 (desktop shell). Define once; do not invent a second
  channel here.
- Per-job **model routing** becomes per-profile access-mode resolution *runner-side*; the control plane
  selects a profile and never sees a key.
- Gate results and fix diffs are **evidence returned over the seam**, so the result artifact must be
  signed/attributable per runner and tolerate an offline or reconnecting runner (relates to per-runner
  presence/heartbeat).
- Self-host remains the co-resident special case of the same protocol — no fork, no separate code path.

Sequencing: Z4 is draft and **not CEO-reviewed** (operator decisions D1–D4 open), so this FRD must not
assume its schedule. The controller's decision logic (§4.2–4.3) is independently valuable and can be
specified now; anything that touches session/pty, launcher, or model-profile code waits on the seam
contract.

## 0.1 Decided topology — central spine, distributed fixing (operator-ratified 2026-07-27)

The operator raised and settled the architecture question directly: **one global Git Manager that
serially fixes every PR was considered and rejected**, as was a purely server-side loop invisible to
the product. The decided shape:

**Central, per project (control plane): the event spine.** One webhook ingress per project catches
every review event, dedupes, orders, and routes — nothing may depend on an agent polling (#319,
MW-36). The queue guarantees **at most one fix round in flight per PR** (two agents must never push
the same branch), but multiple PRs proceed in parallel.

**Distributed, per lane (execution plane): the fixing.** The lane that owns the PR executes the fix
round through its own Git Manager role instance (MW-19 — a role per run, never a global singleton).
Rationale, each grounded in the 2026-07-27 forge-cutover session:

1. **Context ownership.** PR #314's five review rounds required both fixes AND tier-governed
   declines-with-disposition (base-path support, requester identity checks). A context-free global
   fixer would have "fixed" those, weakening validation to satisfy the reviewer — the
   over-minimization failure §4.2 exists to prevent. Decline authority requires the lane's FRD
   context and MW-35 tiers.
2. **Throughput.** Reviews ran ~10 min, fix rounds 10–40 min; a single global queue caps the whole
   platform near one PR/hour via head-of-line blocking. Lane-parallel fixing with per-PR
   serialization scales with lanes — which is what Modula sells.
3. **Isolation and blast radius.** A global agent with write access to every repo violates the hard
   project-isolation rule and concentrates credentials into one compromise target.

**Product placement (both, per Z4):** the control plane owns queue, routing tables
(request-time-recorded ownership: requester/branch/worktree → lane), policy, and the user surfaces
("review finished", "fix round 2 running", Tier-C approval prompts); the runner executes in the
user's lanes with the user's credentials. The co-resident fix-loop daemon is the prototype; the
reaper + dropped-trigger alarm (#264 CP-1, PR #320) is the spine's first delivery/health brick.

## 0.2 Intra-lane role split for fix rounds (operator direction 2026-07-27)

Within the owning lane, fix rounds are **lead-executed**: the job runs with the lane lead's context
and Tier A/B authority, never through a coder delegation round-trip (PL1 evidence: directives
re-send heavy context for tiny fix payloads; the 2026-07-27 session ran six PR loops lead-executed
end to end). The **Git Manager role executes the forge operations** of the round (commit, push,
re-trigger — MW-19 inside the job). A finding that reopens design-scale work exits the loop as a
Tier-C scope change.

The **verifier agent does not run per round**. Verification is three-tier:
1. **Per fix (machine):** revert-proven regression + suite-at-baseline gates — non-negotiable.
2. **Per round (reviewer):** the next review pass re-verifies resolved findings on the new head.
3. **Per checkpoint (agent, once):** the verifier's whole-diff adversarial pass pre-merge — the
   MW-20 final bug-check, preserved because PL1 shipped a P0 exactly when this was dropped.

## 0.3 Forge-agnosticism (operator constraint 2026-07-27)

Modula ships with **either a local Forgejo installation or cloud GitHub** as the forge; every part
of this design must serve both. Binding rules:

- All forge operations ride the **#286 adapter contract** (`create_forge(operation)`, GitHub and
  Forgejo backends, per-operation routing) — no direct `gh`/API calls in controller or job code.
  Both backends are exercised in production today (2026-07-27 dogfood: closeout reads and PR
  lifecycle ran against each).
- The **event schema is forge-neutral**; the ingress normalizes both webhook dialects (Forgejo
  signature headers and event names vs GitHub `X-Hub-Signature-256` / `issue_comment`) into the
  same events. Ingress topology differs by deployment and that is expected: local Forgejo delivers
  to a runner-local receiver; cloud GitHub delivers to the hosted control plane's public ingress
  (Z4 puts the spine there anyway). Neither variant leaks above the ingress layer.
- Reviewer-specific knowledge (banner shapes, trigger comment) lives in the classification layer,
  not the forge layer — the review platform supports both forges.

## 1. Problem

Advisory code review currently produces findings that a human relays into an interactive terminal
agent, which fixes them, pushes, and re-reviews. The prd-288 PL1 run exercised this end to end and
the **code work was never the bottleneck — the sessions were**:

- Interactive panes wedged repeatedly (empty zero-token turns), requiring ~6 operator nudges/relaunches.
- Peer→orchestrator delivery failed one-directionally for hours; a completed fix round was invisible
  and had to be relayed by hand. Only durable artifacts survived (MW-28).
- A provider content filter repeatedly killed the reviewer on our own defensive-security code (MW-29).
- Every directive re-sent large conversational context; the fix payload itself was tiny.

The review-fix loop is a **batch, idempotent job**: bounded input (diff + findings), machine-checkable
success (findings resolved, gates green), and little ambiguity. It is the wrong shape for a long-lived
conversational session and the right shape for a server-side job runner.

It also does not scale as a product: a pane is 1:1 with a PTY and a long-lived session, cannot
multi-tenant, and is not restartable. Jobs are.

## 2. Goals

- Run the review-fix loop as server-side jobs: findings in → fixes, gates, and a pushed commit out.
- **Terminate correctly.** A declarative convergence controller that detects oscillation, decides what
  is worth leaving, and escalates a triage instead of looping (§4.2 — the core of this FRD).
- Per-job-class model routing (cheap model for mechanical fixes, strong model for adversarial checks).
- First-class observability: per-finding fix diff, gate results, receipts, decisions and their rationale.
- Human gates stay explicit and auditable: push/merge/deferral-acceptance are policy-gated, never implicit.

## 3. Non-goals

- Replacing interactive agents for planning, design, scope triage, or guarantee trade-offs. Those stay
  human-and-lead work; this runner handles the mechanical loop only.
- Making advisory review a required check or an approval gate.
- Auto-merge. Merge remains a human gate.

## 4. Design

### 4.1 Job model

`review.fix` job per finding (or per tightly-coupled finding cluster). Under §0 the control plane
*composes and dispatches* the job; the **runner executes it locally**:

```
input:  { repo, pr, head_sha, finding: {fingerprint, path, line, category, severity, body}, policy }
work:   isolated worktree → fix → focused tests → regression test (mandatory) → gates
output: { fingerprint, status: fixed|deferred|failed, diff, tests_added[], gate_results, rationale }
```

Properties: isolated worktree per job (parallel fan-out, no cross-talk), idempotent and restartable,
minimal context (finding + file + tests, never a conversation), and a durable result artifact. The
worktree, the CLI invocation and all credential resolution are **runner-side**; `policy` carries the
profile selection, never a key.

An aggregator then applies successful fixes, runs the **full** gate suite once, and produces one commit
per round. A mandatory **adversarial pass** (single strong-model job, not a chatty agent) tries to refute
each fix before the round is accepted — this is what caught tonight's worst regression (§6).

### 4.2 Convergence controller — when to stop

Counting rounds is not enough. The controller keeps a **fingerprint ledger** per PR (Kody already emits a
stable `fingerprint` per finding), and after each review round R computes:

- `new` — fingerprints never seen before
- `persistent` — open in R-1 and still open in R
- `resolved` — previously open, now absent
- `reappeared` — previously **resolved**, present again ← the oscillation signal

State classification:

| State | Condition | Action |
|---|---|---|
| **CONVERGED** | `open == 0` | Done. Report clean. |
| **CONVERGING** | `open` strictly decreasing and `reappeared == 0` | Continue. |
| **OSCILLATING** | any `reappeared` | STOP that pair. Treat as a **tension**, not a bug (below). |
| **CHURNING** | `open` not decreasing for K rounds (default 2) while `new > 0` each round | STOP. Surface is review-dense; triage. |
| **STALLED** | fix round produced no change in the open set | STOP. The fix is ineffective; escalate. |

**Tension pairs — the A→B→A case.** If a fix targeting fingerprint B in round N coincides with the
reappearance of A in round N+1, record `coupled(A, B)`. A coupled pair is a *design conflict*, and no
amount of looping resolves it: fixing one re-breaks the other. Resolve it by **declared precedence**,
not by another attempt:

```
P0  security · isolation/tenancy · data integrity · audit truthfulness
P1  correctness invariants (verified guarantees, crash-safety, no-partial-apply)
P2  reliability (restart, recovery, idempotency)
P3  performance / scale
P4  hygiene / style
```

In a coupled pair the higher-priority finding wins; the loser's fix is **reverted** and the finding is
deferred with a written rationale. Real example from this run: a receipt-store *performance* fix (P3)
regressed *fail-closed and monotonic-provenance* guarantees (P0/P1). The correct resolution was to revert
the optimization and defer it — which is exactly the ruling this ladder produces mechanically.

**Accept-and-defer criteria** (the "three bugs remain but they are worth leaving" decision). Deferral is
allowed only when **all** hold:

1. severity at or below the configured ship threshold, or the category is advisory-only;
2. category is **not** in the protected set (P0/P1);
3. blast radius is bounded — no data loss/corruption, no cross-tenant or cross-project leakage, no
   authorization bypass, no false audit record;
4. it is **tracked**: fast-follow issue created carrying the fingerprint, repro, and owner;
5. a regression guard exists, or its absence is stated explicitly;
6. the human gate approves — either a pre-declared policy that auto-accepts that class, or an operator decision.

Anything failing (2) or (3) is never deferrable; the runner stops and escalates instead of shipping it.

**Budgets** — stop on whichever binds first: `max_rounds` (default 3), wall-clock, token spend, or
`no_progress_rounds` (default 2). Budgets are ceilings, not targets.

**Suppression** — deferred fingerprints are passed into the next review as *known-deferred* so they are
not re-reported as new. Without this, deferrals get re-litigated forever.

**Regression guard** — every accepted fix ships a regression test. Re-emergence must then be caught by CI
on the next commit, not by the next review round. (This run had a finding whose only defect was a claimed
regression that was never checked in.)

### 4.3 Decision authority — what the runner decides alone, and what it must ask

The real question is not "agent or human"; it is **decide now versus decide in advance**. A good runner
converts most per-PR judgement into *pre-declared policy* (the precedence ladder §4.2, the deferral
criteria, the budgets) so the agent *applies* policy instead of inventing it. The human is consulted only
when the situation falls outside declared policy. Three tiers:

**Tier A — decides alone, inside policy.** Apply and verify a fix; classify convergence state; stop on
oscillation; **revert its own lower-priority fix when the ladder says it threatens a P0/P1 guarantee**;
defer items that meet every deferral criterion. All mechanical given the ladder — no human needed.

**Tier B — decides, then notifies (post-hoc auditable).** Reverting its own optimization, deferring a P3,
exhausting a budget. It proceeds, but the decision plus rationale is recorded and reversible.

**Tier C — must ask (blocking).** Shipping with any P0/P1 finding open; deferral outside the criteria;
**risk acceptance — shipping a known imperfection**; a design change beyond the fix's scope (e.g. adding a
new primitive to an already-verified store); anything touching security, isolation, data integrity or audit
truthfulness; and the final ship/merge decision.

The distinction that matters: an agent may decide *technical* questions and may apply *declared* policy,
but it must not **accept residual risk on the owner's behalf**. That is an accountability question, not a
technical one.

Worked example from the prd-288 PL1 review loop, which produced all three tiers in one session:

| Decision | Tier | Why |
|---|---|---|
| Detect that 3 findings sit at one site on the 4th consecutive round | A | Site/fingerprint ledger; mechanical |
| Diagnose "two stores are not transactional, so no ordering is correct" | A/B | Technical diagnosis; the reviewer itself reached it |
| Revert an intent-attribution fix that re-opened an authorization hole | **A** | Ladder-mechanical: P0 authorization beats P2 provenance. Done without asking, correctly |
| Revert the mirror-repair helper and **ship with a documented gap** | **C** | Risk acceptance. Correctly escalated; the human answered in seconds and saved an hour of churn |
| "Do the atomic receipt channel now instead" | C | Scope change beyond the fix |

**Escalations must be decision-shaped, not data dumps:** 2–3 concrete options with consequences, a
recommendation, and a **default action if no response inside a window** so the loop cannot hang overnight.
Tier C must stay rare or it becomes alert fatigue — which is precisely why policy is declared up front.

At scale the "lead developer" is a *role*, not necessarily a person: a customer may delegate Tier B/C to a
lead agent with declared authority and keep only ship/merge and security-class items with a human. Every
tier decision is recorded with its rationale, so authority can be tightened or loosened per repo from
evidence rather than guesswork.

### 4.4 Escalation artifact

Whenever the controller stops in a non-CONVERGED state it emits a **triage report**, not a raw dump:

- each open finding classified real-signal vs narrow-edge, with the probe/evidence;
- tension pairs with the precedence ruling and what was reverted;
- the proposed deferral list with per-item rationale against §4.2 criteria;
- a root-cause note on *why* it will not converge;
- two operator choices: **accept advisory + fast-follow** (legitimate — advisory review is non-blocking)
  or **continue with an explicit new budget**.

### 4.5 Model routing, observability, gates

- Per-job-class model policy: cheap/fast for mechanical fixes and test authoring; strong for the
  adversarial pass and triage synthesis. Configurable per repo.
- Observability is a product surface, not terminal scrollback: findings list, per-finding fix diff, gate
  results, decisions with rationale, budget/state of the convergence controller, and receipts.
- Provider-refusal handling: classify a content-filter refusal as its own state and escalate to an
  unfiltered model or the operator — never blind-retry (MW-29).

## 5. Phasing

- **CP-1** — fingerprint ledger + single-round dispatch→gates→commit, no auto-loop. Executes through the Z4 seam where available, and co-resident (self-host) otherwise — same protocol.
- **CP-2** — convergence controller (§4.2) plus the decision-authority tiers (§4.3): classification, tension detection, precedence rulings, budgets, suppression, and the Tier A/B/C split with decision-shaped escalations and a no-response default.
- **CP-3** — adversarial pass + mandatory regression authoring + triage-report artifact.
- **CP-4** — observability surface and per-job model routing; human-gate policy configuration.

## 6. Acceptance

- A seeded oscillating pair (fix A breaks B, fix B breaks A) is detected as OSCILLATING within 2 rounds,
  ruled by precedence, and escalated with a triage report — without a third fix attempt.
- A churning surface stops at `no_progress_rounds` and produces a triage report.
- A P0/P1 finding can never be auto-deferred; attempting it fails the run visibly.
- Tier A/B/C routing is enforced: a ladder-mechanical revert proceeds unattended, while shipping a known gap blocks on the owner and records who accepted what.
- An unanswered Tier C escalation applies its declared default rather than hanging the run.
- Deferred fingerprints are suppressed as known in the next review and appear as tracked issues.
- Every accepted fix carries a regression test; removing the fix fails that test.
- Zero auto-merge; push and deferral-acceptance are gated per policy.
- The loop runs to CONVERGED on a real PR with no interactive pane involved.

## 7. Risks / open decisions

- **D-1 — precedence ladder ownership:** ships as a default, per-repo overridable. Recommend the default
  above and that P0/P1 are non-overridable.
- **D-2 — fix granularity:** per-finding jobs maximize parallelism but can conflict on the same file;
  recommend clustering by file/module and fanning out across clusters.
- **D-3 — reviewer independence:** the same provider reviewing and fixing risks blind spots; recommend a
  different model for the adversarial pass than for the fix.
- **D-4 — auto-deferral policy:** whether any class auto-accepts without a human, or the first release
  always asks. Recommend always-ask in v1.
- Server-side auto-fix without §4.2 discipline is precisely how tonight's regressions would have shipped;
  the controller is not optional polish, it is the feature.
