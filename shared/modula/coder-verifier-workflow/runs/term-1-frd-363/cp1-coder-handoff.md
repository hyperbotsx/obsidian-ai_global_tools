# CP-1 Coder Handoff — FRD Term-1 #363

## Scope completed

CP-1 “Spawn truth,” FR-1 through FR-4 only. No git operations were performed.

## Product files changed

- `term-control-center/server/logging.ts`
  - Added `info` logging and structured fields.
  - Added one idempotent diagnostics-channel sink that emits single-line JSON to stdout.
- `term-control-center/server/sessionSupervisor.ts` (new)
  - Central create/verify/liveness seam for tmux-backed agent sessions.
  - Re-exports create/has/kill tmux operations.
  - Adds shared grace-period liveness verification, coms registration polling, stale-registration baselines, and structured launch/supervisor outcomes.
- `term-control-center/server/launchGroup.ts`
  - Creates error-visible groups before pane startup.
  - Runs one post-spawn tmux grace check across panes.
  - Runs coms registration verification asynchronously so HTTP launch responses do not wait for the registration deadline.
  - Kills partial panes and records group `status: error` plus human-readable `statusReason` on verification failure.
  - Marks failed context-brief launches as `failed`.
  - Refreshes persisted pane liveness for reuse decisions.
  - Applies the same grace/outcome checks to dynamically added Browser-QA panes.
- `term-control-center/server/launchRequestPreparation.ts` (new)
  - Holds launch freshness, brief-decision persistence, and implementation coms scoping extracted to keep `launchGroup.ts` below 300 lines.
- `term-control-center/server/launchContext.ts` (new)
  - Holds task-context artifact rendering extracted from `launchGroup.ts` without behavior changes.
- `term-control-center/server/attachToken.ts` (new)
  - Holds attach-token derivation extracted from `launchGroup.ts` without behavior changes.
- `term-control-center/server/contextBrief.ts`
  - Supports and logs `pending | ready | degraded | failed` transitions.
  - Records failure detail separately as `statusReason` while preserving the route-decision reason contract.
  - Logs routing decisions and observed ready state.
- `term-control-center/server/index.ts`
  - Installs the stdout log sink in executable server startup.
  - Logs blocked context-brief gates.
  - Verifies actual tmux liveness before returning a reusable group.
  - Adds `POST /groups/:id/retry`, restricted to failed groups; it retires and freshly respawns panes under the same group ID without pane injection.
- `term-control-center/server/laneOrchestrator.ts`
  - Applies real tmux liveness refresh before lane reuse.
- `term-control-center/server/sessionRecovery.ts`
- `term-control-center/server/browserQaLifecycle.ts`
- `term-control-center/server/completionTeardown.ts`
- `term-control-center/server/orchestrator/paneInjectionRunner.ts`
  - Route create/verify/liveness imports through `sessionSupervisor.ts`.
- `term-control-center/src/App.tsx`
  - Surfaces failed group `statusReason` and a Retry control.
  - Retry calls the group respawn endpoint and replaces panes on success.
- `term-control-center/src/jobView.ts`
  - Carries group and pane status reasons in the UI model.
- `term-control-center/scripts/fake-pi-agent.sh`
  - Adds an opt-in instant-exit mode used by checked-in spawn regression tests.

## Tests changed or added

- `term-control-center/tests/launchGroup.test.ts`
  - Instant wrapper exit => group error with reason.
  - Failed context-brief spawn => `pending -> failed` state and logged transitions.
  - Missing coms registration => asynchronous group error and pane teardown.
- `term-control-center/tests/reusableGroup.test.ts`
  - Out-of-band tmux kill is detected during reuse refresh.
- `term-control-center/tests/server.test.ts`
  - Out-of-band killed group is retired and freshly respawned rather than reused.
  - Failed group retry preserves the group ID and starts fresh panes.
  - Test-only spawn grace/deadline values keep tmux integration tests bounded.
- `term-control-center/tests/spawnVerification.test.ts` (new)
  - Structured spawn attempt/failure records reach the installed logger sink.
  - Coms registration accepts live fresh role JSON, rejects missing roles, and rejects stale pre-spawn registration IDs.
- `term-control-center/tests/contextBriefContinue.test.ts`
  - UI regression guard for statusReason and group Retry endpoint.
- `term-control-center/tests/agentopsComsLabel.test.ts`
  - Uses the SessionSupervisor seam for tmux creation.

## Validation run

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/contextBrief.test.ts tests/launchGroup.test.ts tests/reusableGroup.test.ts tests/spawnVerification.test.ts` — 15/15 passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='relaunch retires|group retry respawns' tests/server.test.ts` — 2/2 passed.
- `cd term-control-center && node --import tsx --test tests/contextBriefContinue.test.ts` — 3/3 passed.

Full suite:

- `cd term-control-center && npm test` — 1373/1384 passed; 11 unrelated existing/environment failures remain outside CP-1:
  - four `agentopsComsLabel` wrapper tests missing the context-renewal fixture/package,
  - existing Kody fix-loop source-regex expectation,
  - existing Browser-QA `missing_allowed_target` fixture failure,
  - existing coworker proposal fingerprint request returning 400,
  - existing lane-slot test receiving the hard-cap error before its expected slot error,
  - three verification-sandbox tests failing `deny_sandbox_start` in this environment.

Build completed with existing Vite warnings for the non-module `term-config.js` script and large client chunk.

## Deviations

- No FR deviation.
- Group failure persistence across a backend restart was not added because CP-4 store hardening is explicitly out of scope. The failed group remains visible and retryable in the active backend/UI state.
- A `ready` transition written directly by the context-brief agent is logged when the backend readiness gate observes and validates it.

## Known gaps intentionally deferred

- No liveness sweep, Recover/Archive, auto-archive, or wake/re-drive behavior (CP-3/CP-7).
- No store schema hardening (CP-4).
- No forge/GitHub or multi-project changes (CP-5/CP-6).

## Commit intent

Files: all product and test files listed above.

Subject: `feat(term): verify spawned agent sessions`

Why: make launch success truthful through tmux/coms verification, prevent dead-group reuse, expose actionable failures and safe group respawn, and complete brief-state observability.
