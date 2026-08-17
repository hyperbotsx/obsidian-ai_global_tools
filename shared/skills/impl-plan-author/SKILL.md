---
name: impl-plan-author
description: Maintain the Implementation Plan — the one living delivery document that holds order, lanes, and what has shipped, kept at the right altitude and continuously replanned without thrash. Use when re-sequencing the plan, slotting a newly approved FRD, reconciling the plan with the PRD, or applying an operator edit to the plan. Covers altitude (order/lanes/what-shipped, not dates-as-roadmap and not feature detail), human-gated re-sequencing, derived completion, the replan lifecycle, the board↔plan boundary, provenance, and structure-safe operator edits. Language- and product-agnostic.
---

# Impl-Plan Author

The Implementation Plan's one job is to answer **what is next, in what order, in which lane — and what
has shipped.** It is the third project-document doctrine, a sibling of `prd-author` (the master PRD)
and `frd-author` (per-feature specs). Its two failure modes are **drift** (the plan and the built
reality diverge) and **thrash** (a plan churned so often it stops being a plan). This doctrine keeps
the plan *true and stable*: at the right altitude, re-sequenced only through the gate, its completion
derived rather than claimed, and reconciled with the PRD.

Its bias, like a steering document and unlike a feature spec, is **convergence and minimal delta, not
completeness — the best replan is the smallest change that reflects new reality.**

It is **one doctrine, two consumers**: the *Planner* (surface `planner`) receives it as a maintenance
overlay, and the *§3 amendment/reconciliation pipeline* + the *§8 Replan action* enforce
`plan-rules.yaml` beside this file.

## Terminology

- **Plan** = the one Implementation Plan per project (`docs/implementation-plan.md`). **This skill governs it.**
- **PRD** = the one master product document (governed by `prd-author`).
- **FRD** = every per-feature spec, traced to a PRD section (governed by `frd-author`).
- **Board** = live execution state — what is running right now. The board owns it; the plan does not.
- The Plan/Board distinction is fixed and load-bearing (below). Do not let the two vocabularies blur.

## How to invoke

- Claude Code: `/impl-plan-author` · Codex: `$impl-plan-author` · Pi/OpenCode: `/skills` picker.

## The altitude rule (the one that matters most)

The plan holds **order, lanes, parallelization constraints, and what has shipped.** The commonest ways
to ruin it are to turn it into a **dated roadmap** or to let **feature detail** leak in.

- **Belongs:** phase/order, lane assignment and lane rules, dependency/blocking relationships, the
  queued remainder, and derived shipped-state.
- **Does NOT belong:** **dates-as-roadmap** (the plan sequences work; it does not promise calendar
  dates), and **feature mechanics / acceptance criteria** (those live in the FRD). If a passage could
  be an FR or AC, it belongs in an FRD — leave a plan row that points at it.

The plan earns its keep by being *current and feasible*, not long. A row exists because there is work
to sequence, never to restate a feature's design. `plan-rules.yaml` holds the altitude map.

## Agent-maintained, human-gated re-sequencing

- **The Planner proposes; the operator disposes.** Any re-order, re-prioritisation, or scope change is
  **raised as a §3 proposal**, never silently applied — the same gate a PRD amendment goes through.
- **Carry the reason.** Every applied re-order writes a version entry naming *why the order changed*
  and *who changed it*. That record is what makes the plan legible instead of mysterious.

## Completion is derived, never asserted

A row turns **shipped** only when its PR merges **and** its validation receipts land — computed from the
Ledger, never written by hand. **A "mark shipped" is refused**: the plan must not be able to claim work
the Ledger cannot prove. This is the invariant every edit and every replan operates *underneath* —
replan only ever touches the not-yet-shipped remainder.

## The replan lifecycle — the plan is continuously replanned

FRDs are authored while others integrate and priorities move, so replanning is a **routine**, not an
event. Six rules:

1. **Recurring, triggered.** Replan runs on the operator's **Replan** action and on triggers: a new FRD
   approved, a dependency changed, a lane freed early or slipped, runner capacity changed, an operator
   priority shift, or a reconciliation gap. It re-evaluates the plan against FRDs landed since the last.
2. **Reorder the QUEUE, not the RUNNING.** Re-sequencing applies only to *queued / not-yet-started*
   work. An FRD **in-flight in the workspace keeps its lane** until it completes or hits a stop-gate —
   that is live execution state the **board owns**. To tell in-flight from queued, the Planner **reads
   the board's execution state read-only**; it writes order/lanes for the queue only. Never propose
   yanking active work.
3. **Concurrent authoring + integration is normal.** When a new FRD is approved mid-flight, propose
   where it slots (phase/lane/priority) relative to the *queued remainder* and its dependencies,
   without disturbing running lanes. The plan holds queued and in-flight work at once.
4. **Dependency- and capacity-feasible.** Respect the dependency store (no item before its blocker;
   detect cycles) and the available lanes/runner capacity. Produce a *feasible* ordering, not a wish-list.
5. **Minimal-delta / anti-thrash.** Propose the *smallest* change that reflects new reality, not a full
   reshuffle; a stable plan beats a churned one. Every re-order records **why**.
6. **Always a §3-gated proposal; completion advances underneath.** The Planner proposes the ordering;
   the operator approves. Merged+receipted rows turn shipped automatically, so replan always operates
   on the not-yet-shipped remainder.

## Operator edits — structure-safe, because the plan is machine-consumed

The operator can edit the plan directly, and both paths coexist: a quick tweak → edit the row; a bigger
re-sequence → ask the Planner in the chat.

- **Editable vs locked.** The operator may edit **order, lane, priority, phase, and notes/rationale**.
  **Derived fields are read-only** — shipped-state is computed and MUST NOT be hand-editable.
- **Validate on save.** A manual edit is structure-checked against the plan's schema before it persists
  (malformed FRD refs, lane ids, or orderings are rejected or flagged), under base-revision guards.
  Malformed text never silently reaches execution.
- **Provenance + operator primacy.** Every edit is stamped operator-vs-Planner. **Operator edits are
  authoritative**: the Planner reads them, treats them as constraints on its next replan, and **never
  silently overturns them** — if an operator edit is infeasible (dependency/capacity), the Planner
  **flags it as a §3 proposal**, never a silent fix.

## Version history is a decision audit trail, not a restore machine

Each version records **why the order changed and who changed it** (a re-order + reason). The plan is
forward-moving — you cannot un-ship — so **restore-to-past-state is not its model.** A light
"undo my last re-order" on the not-yet-shipped queue is optional; full PRD-style restore is out of scope.

## Two-way reconciliation with the PRD

Run on demand and after each FRD approval or PR merge (not on a timer):

- A **plan item with no PRD section** → work nothing in the definition describes → raise an amendment
  proposal (the PRD may need a line, or the item may not belong in the plan).
- A **PRD section with no plan item** → a promise nothing schedules → raise a design/plan work request.

Both surface as **proposals, never automatic edits.**

## Board ↔ plan boundary (never competing sources of truth)

- **Board** = live execution state (what runs now). **Plan** = order/lanes/what-shipped. **PRD** =
  definition. The plan reads the board read-only to tell in-flight from queued; it never writes
  execution state, and the board never owns ordering.

## Less-is-more

- **Bloat is a smell** — a padded row, dates-as-roadmap, feature detail that belongs in an FRD, or a
  churned plan. Prefer the smallest change that keeps the plan true and feasible.

## Protected invariants — never weakened by a routine change

A change that would do any of these is **refused**; only an explicit, recorded operator decision may:

- **Derived completion** — shipped-state is computed from PR-merge + receipts; never hand-set.
- **Queue-not-running** — never re-sequence an in-flight lane; the board owns live execution.
- **Gated re-sequencing** — order/scope changes are §3 proposals, never silent edits.
- **The product-naming rule** — no hardcoded product name; `APP_NAME` config only.

## Notes

- Feeds Modula's existing §3 amendment pipeline, the reconciliation checker, and the §8 Replan action;
  it adds no parallel approval path. Sibling of `prd-author` (living product definition) and
  `frd-author` (feature specs) — shares the anti-bloat + provenance DNA, differs in altitude (delivery
  sequencing vs product definition vs green-field feature).
- The machine-readable altitude map, replan/edit rules, invariant checks, and reconciliation directions
  live in `plan-rules.yaml` (a Modula engine extension, not part of the Agent Skills standard) — the
  enforcement half of the contract.
