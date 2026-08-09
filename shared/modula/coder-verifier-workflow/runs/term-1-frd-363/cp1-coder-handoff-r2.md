# CP-1 Coder Handoff — Revision 2

## Source and constraints

- Base: `d035524`
- Lead brief/ruling: `/tmp/agentops/term1-363/cp1-fix-round-2.md`
- Verifier evidence: `/tmp/agentops/term1-363/cp1-verifier-verdict-r1.md`
- Findings fixed this round: F002-a/bounded F002-b mitigation, F006, F007, F008.
- No git operations by coder.
- No CP-2 lane-gate work, CP-3 sweep/Recover/Archive, CP-4 store hardening, or later-checkpoint scope.

## CP1-F002 — spawn-time truth and refresh-backed consumers

### F002-a: exit while awaiting registration

**Status: fixed.**

`sessionSupervisor.pendingRoles` now checks every still-unregistered pane’s tmux session before each poll sleep and once at loop exit. A pane that survives grace but dies before registering fails immediately with the true cause:

`<role> pane exited while awaiting coms registration`

The full group failure path logs the reason, kills all started panes, updates group state, and writes failed brief state when applicable. It no longer waits for or misreports the registration deadline.

Regression:

- `tests/launchGroup.test.ts` uses a wrapper that exits at 150 ms under a 1000 ms registration deadline.
- Current result: early error, true-cause reason, zero sessions.
- Exact-wiring revert: `/tmp/agentops/term1-363/revert-checks-r2/F002-await/revert.log`.
- Mutation: `exitedPendingRole` was neutered while polling otherwise remained intact.
- Result: test exit 1; failure reason regressed to `coder pane did not register with coms before the deadline`.

### F002-b: post-success death — lead-ruling implementation

**Status: in-scope half fixed; proactive detection explicitly deferred to CP-3.**

Added `server/groupStatus.ts` as the single refresh-backed status accessor:

- `observedGroupStatus(group, sessions)` refreshes every persisted pane against physical tmux before returning status.
- `groupSummary` uses it directly.
- `refreshGroupLiveness` remains exported from the same authority for reuse/lane callers.

All backend raw-status consumers were enumerated. The following decisions now route through `observedGroupStatus` or through `groupSummary/groupSummaries`:

1. `server/launchGroup.ts` — group summaries and async launch completion guard.
2. `server/browserQaPaneLaunch.ts` — Browser-QA async completion guard.
3. `server/heartbeatSweep.ts` — implementation-group tracking.
4. `server/laneOrchestrator.ts` — selected-lane capacity/reuse decision.
5. `server/orchestrator/paneInjection.ts` — injection live-group preflight.
6. `server/orchestrator/paneInventory.ts` — live pane candidate inventory.
7. `server/sessionStore.ts` — persisted group status.
8. `server/index.ts` — existing status-sensitive routes/reuse already consume `groupSummary`.
9. `server/diffState.ts` and `server/groupRetry.ts` — existing decisions already consume `groupSummary`.
10. `server/jobDependencyRoutes.ts` and `server/jobFolderRoutes.ts` — their remaining `group.status` expressions operate on values already produced by `groupSummaries`/`draftJobSummaries`, not raw map entries.

The only remaining direct raw `group.status` accesses are:

- the authoritative calculations/mutations inside `groupStatus.ts`,
- lifecycle transition assignments in `launchGroup.ts` and `browserQaPaneLaunch.ts`,
- queued-lane status assignment in `laneOrchestrator.ts`.

`server/sessionToken.ts` contains the unchanged token digest/match code and is re-exported by `sessionStore.ts`; this avoids a runtime dependency cycle while persistence uses the status accessor. Attach-token continuity/store tests remain green.

No periodic timer, sweep, or notification bus was added.

**Residual window per lead ruling:** after a successfully registered/live pane later dies, any backend/UI observation now fails closed. With active UI polling the verifier measured approximately **3.5–7 seconds** to observation. With no observer, raw in-memory state can remain stale for an **unbounded** interval, although no routed consumer returns it without refreshing. CP-3/FR-9’s liveness sweep closes proactive no-observer detection.

## CP1-F006 — hostile brief-state boundary

**Status: fixed.**

`readContextBriefState` now exposes state only when:

- status is allowlisted,
- `reason` is a non-empty string of at most 500 characters,
- optional `statusReason` is also a non-empty string of at most 500 characters.

Malformed, missing, object-valued, and oversized reasons cause the state to be omitted at the server boundary. The API summary remains serializable and the UI receives no unsafe React child. `src/groupLaunchStatusView.ts` centralizes the render label as a string-only view model; the React component renders that value.

Regression:

- `tests/briefStateSafety.test.ts` covers object reason, missing reason, object statusReason, and a 501-character reason; summary omits state, JSON serialization succeeds, and the render-label path is safe.
- Valid pending/ready/degraded/failed surfacing tests remain green.
- Exact-wiring revert: `/tmp/agentops/term1-363/revert-checks-r2/F006-boundary/revert.log`.
- Mutation: `boundedReason` was changed to accept all runtime values.
- Result: test exit 1 because hostile state crossed the API boundary (`Object.hasOwn` became true).

## CP1-F007 — direct observation and registration-wait guards

**Status: fixed.**

Two direct guards now protect the exact critical wiring:

1. `tests/reusableGroup.test.ts` starts with a physically dead tmux pane still marked `recovered` and calls **only `groupSummary`**. It asserts `error` plus stale recoverability.
   - Revert: `/tmp/agentops/term1-363/revert-checks-r2/F007-summary/revert.log`.
   - Mutation: replaced the exact `observedGroupStatus(group, sessions)` call in `groupSummary` with raw `group.status`.
   - Result: exit 1, `running !== error`.
2. The F002-a registration-wait regression above protects the exact polling-liveness branch.
   - Revert: `/tmp/agentops/term1-363/revert-checks-r2/F002-await/revert.log`.
   - Result: exit 1 with the old false timeout cause.

Scratch copies only were mutated; no revert mutation touched the worktree.

## CP1-F008 — honest structural guard

**Status: fixed with preferred option.**

`tests/cp1Structure.test.ts` is **39 lines** and uses the installed TypeScript compiler API:

- real `FunctionDeclaration` nodes provide actual parameter counts,
- threshold is `<= 4`, not exact formatting,
- real `ImportDeclaration`/`NamedImports` nodes enforce extraction imports,
- source-file line positions provide robust line counts,
- comments cannot satisfy any assertion.

Exact bypass proof:

- `/tmp/agentops/term1-363/revert-checks-r2/F008-ast/revert.log`.
- Mutation: real `launchPane` declaration changed to five parameters (one required plus four optional) while the one-parameter signature was left as a decoy comment.
- Result: exit 1 with `launchPane exceeds the four-parameter limit`.

## Files changed in revision 2

Product:

- `term-control-center/server/browserQaPaneLaunch.ts`
- `term-control-center/server/contextBrief.ts`
- `term-control-center/server/groupStatus.ts` (new)
- `term-control-center/server/heartbeatSweep.ts`
- `term-control-center/server/laneOrchestrator.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/orchestrator/paneInjection.ts`
- `term-control-center/server/orchestrator/paneInventory.ts`
- `term-control-center/server/sessionStore.ts`
- `term-control-center/server/sessionSupervisor.ts`
- `term-control-center/server/sessionToken.ts` (new)
- `term-control-center/src/GroupLaunchStatus.tsx`
- `term-control-center/src/groupLaunchStatusView.ts` (new)

Tests:

- `term-control-center/tests/briefStateSafety.test.ts` (new)
- `term-control-center/tests/contextBriefContinue.test.ts`
- `term-control-center/tests/cp1Structure.test.ts`
- `term-control-center/tests/launchGroup.test.ts`
- `term-control-center/tests/reusableGroup.test.ts`

## Validation

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- Focused round-2 suite: **89/89 passed** across launch, summary observation, malformed brief data, UI, AST structure, heartbeat, injection/inventory/delegation, session store/token continuity, and lane flows.
  - Log: `/tmp/agentops/term1-363/cp1-r2-focused.log`
- Four exact-wiring scratch revert checks all exited non-zero for the intended assertion.
  - Root: `/tmp/agentops/term1-363/revert-checks-r2/`

Full suite:

- `cd term-control-center && npm test`
- Result: **1390 passed, 11 failed, 1401 total**.
- Log: `/tmp/agentops/term1-363/cp1-r2-full-suite-final.log`.
- The 11 failures are the unchanged verifier-confirmed baseline/environment set: four wrapper/context-renewal fixture failures, Kody source-regex expectation, Browser-QA missing-target fixture, coworker fingerprint 400, lane hard-cap ordering expectation, and three sandbox `deny_sandbox_start` failures.

Build log: `/tmp/agentops/term1-363/cp1-r2-build-final.log`. Existing Vite warnings remain unchanged.

## Deviations/disagreements

None. F002 was implemented exactly to the lead’s split ruling. Proactive no-observer detection remains explicitly assigned to CP-3/FR-9.

## Commit intent

Subject: `fix(term): harden spawn observation boundaries`

Why: report pre-registration pane death truthfully, prevent backend consumers from returning raw stale status, reject hostile brief-state data, and replace bypassable structural checks with AST-backed guards.
