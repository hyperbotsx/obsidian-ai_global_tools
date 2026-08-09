# CP-1 Coder Handoff — Revision 1

## Source

- Lead brief: `/tmp/agentops/term1-363/cp1-fix-round-1.md`
- Verifier verdict: `/tmp/agentops/term1-363/cp1-verifier-verdict.md`
- Starting committed revision: `a2b0b12`
- Git operations performed by coder: none

## Finding disposition

All eight accepted findings are addressed.

### CP1-F001 — all agent panes receive fresh coms verification

**Status:** fixed.

- `server/launchComs.ts` now selects the actual group pool for implementation, context-brief/review, draft, and page-bot-control launches.
- Every resolved pane receives the selected pool env and every tmux-backed group remains `starting` until fresh role registration plus stabilized tmux verification succeeds.
- Context-brief success and no-registration failure are both covered.
- Dynamic Browser-QA snapshots its role registration before spawn, remains `starting` while verification is pending, and cannot accept the old session ID.

Tests:

- `tests/launchGroup.test.ts`: non-registering context-brief fails; freshly registering context-brief reaches running.
- `tests/browserQaPaneLaunch.test.ts`: old Browser-QA registration is rejected.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F001/revert.log` — skipping non-implementation verification changed the expected initial `starting` state to `running`; test exit 1.
- `/tmp/agentops/term1-363/revert-checks-final/F007-baseline/revert.log` — removing the Browser-QA baseline made stale registration pass; test timed out waiting for the required error; exit 1.

### CP1-F002 — registration/tmux TOCTOU closes fail-closed

**Status:** fixed.

- Coms verification now waits through a configurable stabilization interval and performs a final tmux liveness check before success.
- A post-registration exit produces the true-cause reason `<role> pane exited after coms registration`.
- Async failure still invokes full group failure handling and kills every started pane.
- `groupSummary` refreshes physical tmux liveness on observation, marks the group error, and supplies a readable missing-pane reason without adding a periodic sweep.

Tests:

- `tests/launchGroup.test.ts`: register-then-exit => error, true-cause reason, zero sessions.
- `tests/reusableGroup.test.ts`: observed dead tmux panes fail closed with group reason.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F002/revert.log` — deleting the stabilized final tmux check left the group non-failed until the test deadline; exit 1.

### CP1-F003 — every lane pane refreshes and dead lanes retire

**Status:** fixed.

- Liveness refresh maps across every pane before aggregate reduction; it no longer short-circuits.
- Lane submission retires matching non-reusable dead groups before capacity checks and fresh spawn.

Tests:

- `tests/reusableGroup.test.ts`: both independently killed panes become stale.
- `tests/laneOrchestrator.test.ts`: an all-dead lane is removed and replaced by a fresh running four-pane group without queueing.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F003/revert.log` — restoring `Array.every` left recoverability `[stale, recovered]` instead of `[stale, stale]`; exit 1.

### CP1-F004 — concurrent retry is serialized

**Status:** fixed.

- `server/groupRetry.ts` owns the failed-group retry transaction and a per-group in-flight claim.
- A concurrent retry receives bounded HTTP 409 semantics; it cannot enter teardown/spawn.
- `server/index.ts` contains only the route adapter.

Tests:

- `tests/groupRetry.test.ts`: delayed teardown overlap yields one 409, one successful respawn, one referenced pane, and no orphan.
- Existing token-guarded same-ID server retry test remains passing.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F004/revert.log` — deleting the in-flight claim made the concurrent request return 200 instead of 409; exit 1.

### CP1-F005 — complete structured records for tmux and PTY

**Status:** fixed.

- Every launch attempt includes non-empty `reason: spawn_requested`.
- Every terminal success/failure outcome includes a non-empty reason code.
- PTY attempts and final coms outcomes now use the same structured launch channel; tmux fields are explicitly `null` for PTY.
- Executable startup emits a structured supervisor record after installing the stdout sink.

Tests:

- `tests/spawnVerification.test.ts`: tmux failure fields, success reason, PTY attempt/outcome, and executable startup sink.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F005-pty/revert.log` — deleting PTY attempt publication made `spawn_requested` undefined; exit 1.
- `/tmp/agentops/term1-363/revert-checks-final/F005-reason/revert.log` — blanking the success reason produced `''` instead of `coms_registered_tmux_stable`; exit 1.
- `/tmp/agentops/term1-363/revert-checks-final/F007-sink/revert.log` — deleting executable `installLogSink()` removed the expected `supervisor/stdout_sink_installed` record; exit 1.

### CP1-F006 — brief transitions are surfaced

**Status:** fixed.

- `readContextBriefState` safely reads the current persisted transition and applicable route/failure reason.
- Group summaries include `contextBriefState` only when present, preserving existing deep-equality/API shape for unrelated groups.
- `jobView`, active launch parsing, the workspace status surface, and job-sidebar rows carry/render the state and reason.
- Pending, ready, degraded, and failed are all covered.

Tests:

- `tests/contextBrief.test.ts`: all four persisted statuses surface through group summaries with their applicable reason.
- `tests/contextBriefContinue.test.ts`: launch status, URL parsing, and sidebar render wiring.
- Existing Lead renewal deep-equality regression remains passing because absent brief state is omitted, not serialized as `undefined`.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F006/revert.log` — deleting summary exposure yielded `undefined` instead of `pending`; exit 1.

### CP1-F007 — regression guards are reversion-sensitive

**Status:** fixed.

Required mutation checks against final source:

1. Grace wiring: `/tmp/agentops/term1-363/revert-checks-final/F007-grace/revert.log` — deleting `verifySpawnGrace` produced `starting` instead of `error`; exit 1.
2. Executable sink wiring: `/tmp/agentops/term1-363/revert-checks-final/F007-sink/revert.log` — deleting `installLogSink()` removed the startup record; exit 1.
3. Caller baseline wiring: `/tmp/agentops/term1-363/revert-checks-final/F007-baseline/revert.log` — replacing the Browser-QA baseline with `{}` let the stale registration satisfy launch; exit 1.

Every other finding also has its own failing revert check above. Scratch copies only were mutated; the worktree was not altered for mutation testing.

### CP1-F008 — KISS boundaries restored

**Status:** fixed.

- `verifyComsRegistrations`, `pendingRoles`, `logOutcome`, and `launchPane` now take one request/context object each.
- Retry transaction moved to `server/groupRetry.ts`.
- Browser launch verification moved to `server/browserQaPaneLaunch.ts`.
- Pool derivation moved to `server/launchComs.ts`.
- Launch error/brief status UI and retry request moved to `src/GroupLaunchStatus.tsx`.
- `server/launchGroup.ts` is 299 lines; all new focused modules are below 300 lines.

Tests:

- `tests/cp1Structure.test.ts` checks file/parameter seams and extraction imports.

Revert proof:

- `/tmp/agentops/term1-363/revert-checks-final/F008/revert.log` — adding a second `launchPane` parameter broke the KISS seam assertion; exit 1.

## Files changed in revision 1

Product:

- `term-control-center/server/browserQaPaneLaunch.ts` (new)
- `term-control-center/server/contextBrief.ts`
- `term-control-center/server/groupRetry.ts` (new)
- `term-control-center/server/index.ts`
- `term-control-center/server/laneOrchestrator.ts`
- `term-control-center/server/launchComs.ts` (new)
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/launchRequestPreparation.ts`
- `term-control-center/server/sessionSupervisor.ts`
- `term-control-center/scripts/fake-pi-agent.sh`
- `term-control-center/src/App.tsx`
- `term-control-center/src/GroupLaunchStatus.tsx` (new)
- `term-control-center/src/JobSidebar.tsx`
- `term-control-center/src/jobView.ts`

Tests:

- `term-control-center/tests/browserQaPaneLaunch.test.ts` (new)
- `term-control-center/tests/contextBrief.test.ts`
- `term-control-center/tests/contextBriefContinue.test.ts`
- `term-control-center/tests/cp1Structure.test.ts` (new)
- `term-control-center/tests/groupRetry.test.ts` (new)
- `term-control-center/tests/laneOrchestrator.test.ts`
- `term-control-center/tests/launchGroup.test.ts`
- `term-control-center/tests/reusableGroup.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/spawnVerification.test.ts`

## Validation

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- Focused CP-1 revision suite: 37/37 passed across launch, coms, retry, lane, brief, UI, structure, and logging tests.
- Focused server tmux recovery/reuse/retry suite: 3/3 passed.
- `Lead renewal reloads only its live route context`: passed after optional brief-state omission fix.
- All 11 final scratch revert commands exited non-zero for the intended assertion; logs are under `/tmp/agentops/term1-363/revert-checks-final/`.

Full suite:

- `cd term-control-center && npm test`
- Result: **1387 passed, 11 failed, 1398 total**.
- Log: `/tmp/agentops/term1-363/cp1-r1-full-suite-final.log`.
- The 11 failures are the same verifier-confirmed baseline/environment failures: four wrapper/context-renewal fixture failures, Kody source-regex expectation, Browser-QA missing target fixture, coworker fingerprint 400, lane hard-cap ordering expectation, and three sandbox `deny_sandbox_start` failures.

Build log: `/tmp/agentops/term1-363/cp1-r1-build.log`. Existing Vite non-module-script and large-chunk warnings remain.

## Scope and deviations

- No disagreement with the eight findings.
- No CP-2 lane-gate routing, CP-3 sweep/Recover/Archive, CP-4 store hardening, CP-5 forge mutation, CP-6 multi-project work, or CP-7 wake/re-drive was added.
- No #264 Kody-area files were touched.
- Attach-token extraction/behavior was not changed.

## Commit intent

Subject: `fix(term): close spawn verification gaps`

Why: verify every agent pool fail-closed, close post-registration liveness races, serialize retry, free dead lane capacity, complete observability/state surfacing, and install mutation-sensitive regression protection.
