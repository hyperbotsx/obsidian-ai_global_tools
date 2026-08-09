# FRD: PL2 — Delegation Plan Engine + Plans Tab (P-2)

> Canonical FRD source: the GitHub issue created from this draft (labels `type:prd`, `status:draft`).
> Assigned agent: `agent:agentops`. Code home: `hyperbotsx/agentops-harness`.
> Proposed branch: `prd/delegation-plan-engine-<issue#>` off `main`; worktree `agentops-prd-<issue#>`.
> Umbrella: #267 Modula Stack Design Rollout — PL2 in `dev-plans/drafts/page-briefs/00-index.md` (spine PL1→PL2→PL3).
> Briefs: 02-planner (frozen v1) — §2.4 delegation planning, §3 plan-proposal rendering + Plans sub-tab, §5 new backend, §9 decisions (esp. §9.2 slot capacity is a Setting, §9.3 Plans sub-tab ships v1, §9.4 quick jobs foldable).
> Dependencies: F3 #277 + F4 #283 (merged) · #286 forge adapter (merged — board status ops go through `forge.boards`) · **PL1 #288 (IN FLIGHT — see Coordination)**. Blocks: PL3 (replan loop).
> Research-first surfaces: plan/lanes — `lane_plan.py`, `parallel_plan.py`, `planned_worktrees.py`, `planned_worktree_status.py`, server `laneOrchestrator`, `launchPlan`, `launchGroup`; project state — `github_project.py` (Status/CEO Approved fields), labels-as-canonical-state; forge adapter boards/dogfood lane (`src/agentops_harness/forge/`); notifications — F3 producer registration; PL1's plan-proposal message schema (the contract this engine consumes — coordinate, do not fork); settings store (R6/G-4 seam) for slot capacity.

- **Status:** draft (CEO review optional gate before implementation)
- **Date:** 2026-07-24
- **Model note:** Lead runs on **Claude Opus 5** this run (operator decision — A/B vs the Fable-led #286 run; harvest triage quality, MW-20 judgment, session coherence, token spend).

## 1. Problem

Delegation plans exist only as conversation: PL1's Planner can *render* a plan proposal and take an Approve chat act, but nothing versions, validates, or executes it — waves still populate by hand, slot capacity is un-enforced, and there is no auditable record of which plan was approved, when, or what changed between plans. Brief 02 promises immutable plan snapshots with delta views and receipts; the engine behind that promise is unbuilt, and PL3's replan loop has nothing to diff against.

## 2. Goals

1. **Versioned delegation-plan object** (per project): plan id, wave list, slot assignments, per-FRD team, gates, rationale; approved plans are immutable snapshots; any change creates v+1. Quick jobs foldable into waves with their lighter gate profile (§9.4).
2. **Validation engine**: dependency cycles, slot-capacity ceiling (a Settings value the human owns — §9.2), gate consistency. Validation failures return structured errors and NEVER partially apply.
3. **Activation semantics**: an approved plan populates waves (feeds existing lane orchestration), writes receipts to Activity (F3 producer) + audit; activation is atomic — validate-then-activate, no partial waves.
4. **Plans sub-tab (v1)**: version list; each row expands to a delta view against its predecessor (moved/added/removed jobs, slot changes, team changes) + the approval receipt (§9.3).
5. **Contract wiring**: PL1's Approve/Modify chat act drives this engine (approval = chat act, receipted, no confirm phrase).

## 3. Non-goals (bounded per MW-16)

- Replan triggers, replan chip, unprompted proposals, delta-proposal generation (PL3 — but the v+1 snapshot model must leave PL3 a clean seam).
- Board reskin / kanban / matrix / timeline tabs (R2, P-1) — the Plans sub-tab mounts on the existing board serving.
- Matrix urgency/importance derivation (P-1) and team auto-assignment cluster resolution (brief 03).
- Any Planner-side natural-language work (PL1 owns the bot; PL2 consumes its structured output).

## 4. Coordination with PL1 (in flight)

PL1 (#288) is running in a parallel lane. Phasing is ordered so overlap is near-zero until the last checkpoint: CP-1/CP-2 are pure backend (plan store, validation, activation) touching lane/orchestration modules PL1 does not modify; CP-3 (Plans tab + chat-act wiring) **requires PL1 merged** — if PL1 has not landed by CP-3, the lead pauses the lane at the CP-2 boundary rather than building against an unmerged contract. The plan-proposal message schema is PL1's artifact: consume it verbatim; any needed schema change is a cross-lane lead-to-lead negotiation, not a local fork.

## 5. Phasing (checkpoints)

- **CP-1:** delegation-plan object + store (versioned, immutable snapshots) + validation engine (cycles, capacity, gate consistency) + slot-capacity setting plumbing. Pure backend, mocked tests. No UI, no chat.
- **CP-2:** activation: approved plan → wave population through existing lane orchestration; receipts to Activity (F3 producer) + audit; atomic validate-then-activate; failure paths structured. Backend + tests; a thin CLI/route for manual activation as the temporary production consumer (MW-13: no unmounted engine).
- **CP-3 (gated on PL1 merged):** Plans sub-tab (version list, delta view, receipts) on the existing board page; wire PL1's Approve/Modify chat act to validate→snapshot→activate. Nav registry byte-parity maintained.

## 6. Acceptance

- Plan lifecycle end-to-end: propose (fixture) → validate (reject cycle/capacity/gate violations with structured errors) → approve → immutable v1 snapshot → waves populated → receipts in Activity + audit; modify → v2 with correct delta.
- Slot capacity: plans exceeding the Settings ceiling rejected; Planner may recommend a ceiling change but cannot change it (§9.2).
- MW-13 check: every engine surface has a production consumer (CP-2 route/CLI until CP-3 wires the chat act).
- Plans tab renders version list + delta + receipt; byte-parity nav test green; house gates green (node + pytest, known baselines).
- No partial application anywhere: any validation/activation failure leaves prior state untouched (tested).

## 7. Risks / open decisions

- **D-PL2-1 — plan store home:** Python side (state-file seam like activity/completion stores) vs term-server TS store. Recommend Python store + REST route (matches lane orchestration ownership and the F3 store-of-record pattern); coder proposes in CP-1 plan.
- **D-PL2-2 — wave feed shape:** feed existing `launchPlan`/`launchGroup` structures directly vs an adapter layer. Recommend direct-with-adapter-seam; decide at CP-2 plan.
- PL1 schema drift risk (see §4) — consume, never fork.
- Slot capacity default when Settings value absent (recommend: conservative 4, from the board-regen rate-limit experience).

## 8. Dogfood setup (this run)

Quartet in a fresh worktree, **isolated coms pool `agentops-trio-pl2`** (MW-21/MW-22 preflight: canonical names or stop). **Lead = Claude Opus 5** (trial, A/B vs #286). Ponytail OFF (architectural, MW-18). Coder emits commit-intents (zero git); git-manager owns VCS + the full ship-and-retrigger tail of any advisory-review loop (MW-23); push/merge human-gated. Verifier joins fix loops selectively per MW-23. Harvest every friction to `modula-workflow-requirements.md`.
