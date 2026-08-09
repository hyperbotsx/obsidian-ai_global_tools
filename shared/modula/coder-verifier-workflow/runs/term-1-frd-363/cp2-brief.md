# CP-2 BRIEF — Context-Brief end-to-end (FR-5..FR-8)

FRD Term-1, forge issue #363. Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-363`,
branch `prd/term-1-fully-functional-363`. All work under `term-control-center/` (plus
`pipeline-diagram/` — see G-5 below). You do no git.

**CP-1 is approved and closed** at `af1ed01` (4 commits, 0 open findings). Do not disturb it.

## Why this checkpoint exists

CP-1 made spawning *truthful*. CP-2 makes the gate *reachable*. Today the Context-Brief gate is the
#1 functional blocker in the FRD: no UI surface can pass it, and lane launches skip it entirely. Until
this lands, an approved FRD cannot be launched from the board at all.

## Scope: FR-5..FR-8 only

- **FR-5** — launch surfaces carry `task.contextBrief` (policy/scope/surfaces), defaulted from
  per-project action config. Two surfaces: **board launch** and **planner handoff**.
- **FR-6** — lane launches route through the same `contextBriefLaunch` gate.
- **FR-7** — brief agent completes → the existing `continue` transition starts implementation with
  trio+Lead.
- **FR-8** — degraded continuation stays operator-reasoned (an operator reason is required, not
  inferred).

Out of scope: CP-3 sweep/Recover/Archive, CP-4 stores, CP-5 forge, CP-6 multi-project, CP-7
wake/renewal. Stay out of `src/agentops_harness/kodus_*` and `scripts/agentops/kodus*`.

## Grounding — I re-verified this against `af1ed01` (post-CP-1). Line numbers moved; use these.

**G-1 — F-1 still holds, but do not be misled.** `grep contextBrief src/` now returns **7 hits** —
all of them are `contextBriefState` *readers* that CP-1 added for brief-state surfacing
(`JobSidebar.tsx:171`, `App.tsx:28,331,1084`, `jobView.ts:7`, `groupLaunchStatusView.ts:1,4`).
`contextBriefState` (CP-1 output, read-only) and `task.contextBrief` (CP-2 input) are **different
fields**. Producers of `task.contextBrief` are still **zero**. Do not mistake one for the other.

**G-2 — the gate and the lane bypass, current lines.** `contextBriefLaunch` is now at
`server/index.ts:749`, called from `launchHandler` at `:631`. The lane branch returns at `:617-620`,
**before** that call. That is F-6's bypass, unchanged in substance.

**G-3 — the payload contract already exists; do not invent one.** `shared/launcher.ts:208-225`
already validates `ContextBriefConfig`:
- `policy`: `auto` | `required` | `skip`
- `scope`: `tiny` | `small` | `medium` | `large` | `xl` | `one-file-fix` | `docs-only` | `unknown`
- `surfaces[]`: `cross-cutting` | `frontend-backend-contract` | `shared-schema` | `launch-flow` |
  `completion-state` | `agent-prompts` | `memory` | `github-integration` | `browser-qa`
- `reason` — **required when policy is `skip`** (already enforced)

FR-5 is about *producing* a valid config, not validating it. Match this contract exactly.

**G-4 — defaults source.** `server/projectActionConfig.ts` is the per-project action config the FRD
points at, but its current `ProjectActionConfig` is about merge method / sync, with no brief fields.
Adding brief defaults there is likely a small additive change — confirm before assuming, and follow
its existing `parseActionConfig` / `resolveProjectActionConfig` patterns rather than inventing a new
config mechanism.

**G-5 — the board launch is NOT in `src/`.** There are zero `/launch` POST sites in `src/`. The
board-side launch surfaces live in the static `pipeline-diagram/*.js` (start at
`coworker-launcher.js`; `planning-intake.js` is the likely planner-handoff surface). Ground both
before editing; the FRD's "board launch + planner handoff" maps onto these, not the React app.

**G-6 — the continue transition already works.** `POST /groups/:id/context-brief/continue`
(`server/index.ts:327` → `continueContextBriefHandler`) and `server/contextBriefTransition.ts` are
built and were exercised during CP-1. FR-7 is wiring and proving, not building. FR-8's operator
reason is already a parameter on that handler — verify it is genuinely required for the degraded
path rather than silently defaulted.

## What "done" means

FR-5..FR-8 implemented with tests, **same bar as CP-1**: every guard proven by a revert check that
mutates the exact production wiring. That gate is now the house standard — three rounds of CP-1
established it and I will hold CP-2 to it from round 0.

Note the exit criterion is AC-1, an **in-app dogfood on a real deploy** (launch from the board →
brief agent visibly spawns → produces the brief → `continue` starts trio+Lead → a live
Lead↔Coder↔Verifier exchange). The deploy is an operator-gated step I am handling separately — build
and test as if it is coming, and make sure the API path is exercisable headlessly so we are not
blocked on a browser.

## House rules

KISS: functions <20 lines, ≤3 nesting levels, files <300 lines, ≤4 parameters, comment density <5%,
"why" comments only, no commented-out code, no product-name hardcoding. `server/index.ts` is a
pre-existing 1580-line legacy file — add route adapters only, put logic in focused modules.

Any UI you touch must cite its prototype anchor per the prototype-reference gate
(`dev-plans/drafts/modula-stack-design-prototype.html`). Full visual parity is FRD Term-2, not this.

## When done

Write `/tmp/agentops/term1-363/cp2-coder-handoff.md` — files changed, per-FR status, tests + revert
checks, deviations, and anything you disagree with. Then `coms_send` to `lead`:
`cp-2 handoff ready`. If you cross ~80% context, write an interim handoff first.
