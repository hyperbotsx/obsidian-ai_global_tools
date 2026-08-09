# CP-1 Coder Handoff — Revision 3

## Source and scope

- Base: `a9388e7`
- Lead brief: `/tmp/agentops/term1-363/cp1-fix-round-3.md`
- Verifier verdict: `/tmp/agentops/term1-363/cp1-verifier-verdict-r2.md`
- Findings addressed: `CP1-F002` and `CP1-F008` only.
- No git operations.
- No timer, sweep, notification bus, CP-2 lane routing, CP-3 recovery, or later-checkpoint work.

## CP1-F002 — remaining observation consumers

**Status: fixed.**

### Lane runtime slots and capacity

`laneOccupiesRuntimeSlot` now calls `observedGroupStatus(group, sessions)` before examining session recoverability. This is the common decision behind:

- `runningLaneSlotLetters`,
- `activeLaneGroupCount`,
- `batchLaneGroupCount`.

A physically absent tmux pane is therefore marked stale before any of those decisions. The subsequent `some(...)` check intentionally remains pane-based: an all-dead lane consumes no runtime slot, while a partially degraded lane still consumes a slot for its genuinely live pane.

Regressions in `tests/laneOrchestrator.test.ts`:

1. `running lane slots observe a physically dead tmux pane directly`
   - Calls only `runningLaneSlotLetters` after killing both tmux panes.
   - Returns `[]` and marks both sessions stale.
   - Exact-call mutation removed only the `observedGroupStatus(group, sessions)` call from `laneOccupiesRuntimeSlot`.
   - Result: exit 1; stale `['ADHOC-212']` was returned.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F002-lane-slots/revert.log`.
2. `an unrelated dead lane does not consume launch capacity`
   - Uses global capacity 1 and an unrelated physically dead lane.
   - The requested lane launches rather than queuing; the dead lane is observed as error.
   - The same exact-call mutation produced `queued: 1` instead of `0`.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F002-lane-capacity/revert.log`.
3. `a partially degraded lane keeps its live runtime slot`
   - Kills one of two physical panes.
   - Returns `['ADHOC-212']` while recoverability becomes `['stale', 'recovered']`.

### Browser-QA preflight

`assertBrowserQaGroupLive` observes the implementation group and requires observed `running` state.

- `startBrowserPane` invokes it before constructing or spawning a new Browser-QA pane.
- `prepareBrowserQaLaunch` invokes it before the route’s Browser-QA feed activation callback.
- `browserQaPaneHandler` routes feed activation through `prepareBrowserQaLaunch`, so a dead group has no feed or spawn side effect.
- An already-attached Browser-QA pane remains idempotent and returns its summary without a new side effect.

Regressions in `tests/browserQaPaneLaunch.test.ts` use a killed tmux coder pane still marked recovered:

1. `a dead implementation pane blocks Browser-QA before spawn`
   - Asserts the spawn callback is never invoked and no browser pane is attached.
   - Removing only the exact `assertBrowserQaGroupLive(input.group, input.sessions)` call from `startBrowserPane` fails with `Missing expected exception`.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F002-browser-spawn/revert.log`.
2. `a dead implementation pane blocks Browser-QA preparation side effects`
   - Asserts the feed/preparation callback is never invoked.
   - Removing only the exact `assertBrowserQaGroupLive(group, sessions)` call from `prepareBrowserQaLaunch` fails with `Missing expected rejection`.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F002-browser-prepare/revert.log`.
3. The shared physical-observation call was independently mutated from `observedGroupStatus(group, sessions)` to cached `group.status`.
   - Both regressions fail.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F002-browser-observer/revert.log`.

The prior `F002-a` registration-boundary behavior and `F007` summary observation guards remain green. Proactive detection with no observer remains deferred to CP-3/FR-9 per the binding ruling.

## CP1-F008 — structural test brittleness

**Status: fixed.**

`tests/cp1Structure.test.ts` is now 38 lines and has no private function-name lookup.

- It recursively visits actual non-exported function-like AST nodes in both CP-1 modules and enforces at most four parameters.
- Existing exported public APIs are excluded generically because `startLaunchGroup` and `startBrowserQaPane` already have seven/five parameters and were not targets of the prior private-helper guard; no exported or private function name is hardcoded.
- Import-boundary assertions remain AST-based.
- Line counting splits source text and discounts only the terminal empty segment, so a trailing newline is not counted as an extra source line.

Sensitivity proofs:

1. **Real fifth parameter fails.** The actual private `launchPane` declaration was changed to one required plus four optional parameters. The generic visitor failed with `FunctionDeclaration exceeds the four-parameter limit`.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F008-five/revert.log`.
2. **Harmless rename passes.** `launchPane` and both call sites were renamed to `spawnPane`; full typecheck and both structural tests passed.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F008-rename/typecheck.log` and `pass.log`.
3. **Legal formatting/line count passes.** A trailing-newline scratch copy was padded from 277 to exactly 299 physical lines. `wc -l` reported 299 and both structural tests passed.
   - Evidence: `/tmp/agentops/term1-363/revert-checks-r3/F008-format/linecount.log` and `pass.log`.

Scratch mutations only; none touched the worktree.

## Files changed

Product:

- `term-control-center/server/browserQaPaneLaunch.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/laneOrchestrator.ts`

Tests:

- `term-control-center/tests/browserQaPaneLaunch.test.ts`
- `term-control-center/tests/cp1Structure.test.ts`
- `term-control-center/tests/laneOrchestrator.test.ts`

## Validation

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- Focused final suite: **28/28 passed** covering launch truth, summary liveness, Browser-QA preflight, lane observation/capacity/partial degradation, and structural checks.
  - `/tmp/agentops/term1-363/cp1-r3-focused-final.log`
- All exact-call scratch mutations exited non-zero for their intended assertions.
  - `/tmp/agentops/term1-363/revert-checks-r3/`

Full suite:

- `cd term-control-center && npm test`
- **1395 passed / 11 failed / 1406 total**.
- `/tmp/agentops/term1-363/cp1-r3-full-suite-final.log`
- The 11 failing names exactly match the revision-2 verifier-confirmed baseline: four wrapper/coms fixture failures, fix-loop source expectation, Browser-QA missing-target fixture, coworker fingerprint fixture, lane hard-cap ordering expectation, and three sandbox `deny_sandbox_start` failures.

Build log: `/tmp/agentops/term1-363/cp1-r3-build-final.log` (only existing Vite warnings).

## Disagreements or deviations

None. The structural guard’s generic export exemption is explicit because two pre-existing exported APIs exceed four parameters; private implementation declarations are checked without encoding any private name.

## Commit intent

Subject: `fix(term): observe lane and browser preflights`

Why: ensure lane capacity and Browser-QA actions observe physical session liveness, and make the CP-1 structural guard resilient to harmless refactors and trailing newlines.
