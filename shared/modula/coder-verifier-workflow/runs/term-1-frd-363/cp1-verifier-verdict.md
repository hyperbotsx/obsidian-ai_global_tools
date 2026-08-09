# CP-1 Verifier Verdict — FRD Term-1 #363

## Review identity

- **Decision:** `revision_requested`
- **Checkpoint:** CP-1, Spawn truth (FR-1 through FR-4)
- **Revision reviewed:** 0
- **Branch:** `prd/term-1-fully-functional-363`
- **Base:** `ce25224db26812207aac1a8d59bb50fd669f924c`
- **Committed revision:** `a2b0b121f82e02a190011d5240ab4bd7c8d596aa`
- **Commit parent:** `ce25224db26812207aac1a8d59bb50fd669f924c`
- **Scope:** `term-control-center/` only

I read the canonical Forgejo issue and CEO-review ruling independently, then reviewed the committed 22-file delta rather than relying on the coder handoff. All 22 reviewed worktree blobs matched the committed revision. No non-ignored source change outside `term-control-center/` or change in the #264 Kody area was delivered. The coder handoff records no Git operations, and I found no contrary evidence.

## Decision summary

CP-1 is not ready to advance. The production stdout sink, basic tmux grace failure, ordinary dead-group reuse retirement, partial-pane cleanup, retry respawn behavior, and all four context-brief transition writers work. However, verification is not fail-closed for every agent pane, a post-registration exit can leave a group silently `running`, the lane reuse path can strand a replacement behind sessions whose tmux panes are all dead, concurrent retries can orphan a full pane set, successful spawn records lack reasons, and brief state is not surfaced through the API/UI. Several required regression tests also remain insensitive to removal of the wiring they claim to protect.

## Atomic acceptance matrix

| Check | Result | Independent evidence |
|---|---|---|
| Stable committed checkpoint and allowed scope | PASS | Branch ref is `a2b0b12`; parent is the required base; 22 worktree blobs matched the commit; changed paths are under `term-control-center/`. |
| C-1: all 11 full-suite failures pre-existing | PASS | Every current failure reproduced against pristine `ce25224`; see the one-by-one table below. |
| FR-1: runtime stdout sink | PASS | Executed `build/server/index.js`, launched a failing real tmux group, and observed JSON `spawn_attempt` plus `spawn_outcome` on stdout. |
| FR-1: every attempt/outcome has a reason and every supported spawn path logs | FAIL | Successful outcomes omit `reason`; PTY launch emitted zero spawn records. See CP1-F005. |
| FR-2: tmux grace detects an early exit | PASS, partial | Instant-exit launch becomes `error` with a readable reason. |
| FR-2: fresh coms verification for all agent panes | FAIL | Only implementation groups receive a pool; context-brief can remain `running` without any registration, and Browser-QA omits the pre-spawn baseline. See CP1-F001. |
| FR-2: verification cannot pass with nothing alive | FAIL | A fresh registration followed by tmux exit left the group `running` with all tmux gone. See CP1-F002. |
| FR-2: partial-kill | PASS | Two-pane adversarial launch returned `error`, killed both tmux panes, and left zero sessions. |
| FR-2: launch response is nonblocking | PASS | Checked-in test uses a 600,000 ms coms deadline while launch/retry returns in under one second. |
| FR-2: failed-only retry freshly respawns | PASS, single request | Endpoint is token-guarded, rejects non-error groups, and checked-in test proves fresh session IDs rather than pane injection. |
| FR-2: retry concurrency | FAIL | Two overlapping retries both returned 200 and left one orphan pane set. See CP1-F004. |
| FR-2: readable UI reason | PASS for group failures | `statusReason` reaches `GroupLaunchError` and the group retry control. |
| FR-3: normal reusable-group path | PASS | Out-of-band tmux kill produces a fresh group; deleting the refresh call makes the regression test fail. |
| FR-3: lane reusable-group path | FAIL | All tmux panes were dead, but only one session was refreshed stale and the fresh lane stayed queued. See CP1-F003. |
| FR-4: pending/ready/degraded/failed reachable and logged | PASS | Independent sink capture observed all four `context_brief_transition` statuses. |
| FR-4: state surfaced | FAIL | State is only on disk/in logs; group summaries and UI expose no pending/ready/degraded brief state. See CP1-F006. |
| SessionSupervisor create/verify/liveness seam | PASS, with KISS finding | Creation and relevant liveness imports route through `sessionSupervisor.ts`; parameter structure violates the house budget. |
| C-3: extraction behavior preserved | PASS | Attach-token executable logic is unchanged; digest/salt helpers are unchanged; continuity/store tests pass 7/7. Launch context and preparation preserve prior ordering/data. |
| C-4: lane scope | PASS | The lane delta is limited to a liveness-refresh call and import; it does not implement CP-2 lane-gate routing. |
| C-5: stale-registration guard | FAIL, partial | Initial implementation wiring snapshots/rejects the old session ID, but dynamic Browser-QA calls verification without a baseline. |

## C-1 — baseline reproduction of all 11 current failures

Current full suite: **1374 passed, 11 failed, 1385 total**. Each row below reproduced at pristine base `ce25224`; no CP-1-only failure was found.

| # | Current failing test | Baseline reproduction |
|---:|---|---|
| 1 | `rejects fabricated wrapper readiness without a signed payload` | PASS — same `7 !== 0`. |
| 2 | `requires a signed payload before wrapper readiness is accepted` | PASS — same `7 !== 0`. |
| 3 | `rejects replayed signed wrapper readiness payloads` | PASS — same `7 !== 0`. |
| 4 | `accepts a valid signed wrapper readiness payload` | PASS — same `7 !== 0`. |
| 5 | `fix-loop launch wiring carries selected findings into task details` | PASS — same missing `/Task details: ${task.body}/` source-regex match. |
| 6 | `Browser-QA pane launches preserve the same-url evidence fallback contract` | PASS — same `missing_allowed_target`. |
| 7 | `coworker lane proposals receive a server-derived current precondition fingerprint` | PASS — same HTTP `400 !== 200`. |
| 8 | `lane execution rejects lanes outside configured slots` | PASS — same hard-cap message returned before expected slot error. |
| 9 | `verification sandbox allows required verification commands and denies everything else` | PASS — same `deny_sandbox_start`. |
| 10 | `verification sandbox permits a configured filesystem tool for in-scope mutation tests` | PASS — same `deny_sandbox_start`. |
| 11 | `verification sandbox requires a valid Git worktree` | PASS — same `deny_sandbox_start`. |

The baseline archive itself lacks a valid checkout context, so the exact failing cases were also run from a valid Git cwd while importing pristine baseline files. Logs are `/tmp/agentops/term1-363/baseline-*.log`; current-suite evidence is `/tmp/agentops/term1-363/cp1-current-full-suite.log`.

## Open findings

### CP1-F001 — Agent-pane coms verification is incomplete

- **Severity:** high
- **Evidence:** `server/launchGroup.ts:41` creates a verification pool only when `mode === 'implementation'`; `:80` immediately records success for every other mode. A long-lived fake context-brief pane wrote no registration yet remained `running` with no reason (`cp1-adversarial.out`). Dynamic Browser-QA calls `verifyComsRegistrations` at `:210` without taking/passing a pre-spawn registration baseline. Initial implementation groups do take and use a baseline correctly.
- **Affected paths:** `server/launchGroup.ts`, `server/launchRequestPreparation.ts`, `server/sessionSupervisor.ts`, launch tests.
- **Requested bounded action:** derive the expected coms pool and pre-spawn role snapshot for every launched agent pane, including context-brief/draft and Browser-QA; keep the group non-successful until fresh tmux plus coms verification completes; preserve the nonblocking HTTP contract. Add checked-in tests in which a live non-registering context-brief pane errors and an old Browser-QA registration cannot satisfy a new pane.
- **Decision impact:** blocks FR-2 and C-5.

### CP1-F002 — Registration/liveness has a TOCTOU fail-open path

- **Severity:** high
- **Evidence:** an implementation wrapper registered a fresh, live PID after the grace check, then exited. After 300 ms the group remained `running`, had no `statusReason`, and every recorded tmux session was absent (`cp1-adversarial.out`). `verifyComsRegistrations` only waits for registry/PID state and logs success; it does not refresh tmux liveness before success, and ordinary `/groups` summaries do not refresh physical tmux state.
- **Affected paths:** `server/sessionSupervisor.ts`, `server/launchGroup.ts`, `server/index.ts`.
- **Requested bounded action:** close the verification TOCTOU window with a final/stabilized tmux check and make observed group summaries fail closed when tmux is gone, without introducing the CP-3 periodic sweep. Ensure async verification failure also completes all group-level cleanup. Add a deterministic register-then-exit regression test that asserts `error`, a true-cause reason, and pane cleanup.
- **Decision impact:** blocks FR-2 and V2.

### CP1-F003 — Lane liveness refresh short-circuits and strands a dead lane

- **Severity:** high
- **Evidence:** `refreshGroupLiveness` at `server/launchGroup.ts:162` uses `Array.every`, so it stops after the first dead pane and does not mark later dead panes stale. In an adversarial lane launch, all four tmux sessions were independently confirmed dead; the next lane launch showed the old group as `error` with recoverability `[stale, recovered, recovered, recovered]` and a replacement group as `not_started` with no panes (`cp1-adversarial-lane-summary.json`). The unrefreshed sessions continued to occupy lane capacity.
- **Affected paths:** `server/launchGroup.ts`, `server/laneOrchestrator.ts`, lane integration tests.
- **Requested bounded action:** refresh every pane before reducing to aggregate liveness, and retire or otherwise remove the all-dead lane from capacity before starting its replacement. Add a tmux lane regression test proving all-dead state yields a fresh running group rather than reuse or a permanently queued group.
- **Decision impact:** blocks FR-3 on the required lane path.

### CP1-F004 — Concurrent failed-group retries orphan panes

- **Severity:** high
- **Evidence:** `retryGroupHandler` has no per-group in-flight/CAS guard around `retireGroup` plus `startWorkspaceGroup`. With a realistic delayed Lead shutdown, two concurrent authenticated retries both returned 200; one group remained with one referenced pane while two pane sessions existed, leaving one orphan (`cp1-retry-race.out`).
- **Affected paths:** `server/index.ts`, retry route tests.
- **Requested bounded action:** serialize or atomically claim retry per group. A concurrent request must reuse the in-flight result or return a bounded 409, and must never spawn a second pane set. Add a deterministic overlap test with delayed teardown and assert no orphan sessions.
- **Decision impact:** blocks the FR-2 retry requirement.

### CP1-F005 — FR-1 records are incomplete

- **Severity:** medium
- **Evidence:** the deployed `npm start` executable path does install the sink and a real failure emitted both records (`cp1-runtime-server.log`). However, successful `spawn_outcome` records omit `reason` (`sessionSupervisor.ts:59,89`), and PTY launch produced `spawnRecords: 0` (`cp1-adversarial.out`) because logging is only in the tmux supervisor path. The requirement is every spawn attempt/outcome with a reason.
- **Affected paths:** `server/sessionSupervisor.ts`, `server/launchGroup.ts`, `server/logging.ts`, spawn logging tests.
- **Requested bounded action:** emit attempt and terminal outcome records with non-empty reason codes for success and failure on both supported supervisor modes; retain one-line stdout JSON and avoid sensitive fields. Add success, PTY, and executable-startup assertions.
- **Decision impact:** blocks FR-1.

### CP1-F006 — Brief transition state is logged but not surfaced

- **Severity:** medium
- **Evidence:** independent capture reached and logged `pending`, `ready`, `degraded`, and `failed` (`cp1-brief-transitions.out`). The only state reader is the backend gate; `groupSummary`, shared launch summaries, `jobView`, and the React UI contain no brief-state field. Only group-level failure reason is visible.
- **Affected paths:** `server/contextBrief.ts`, group/API model, `src/jobView.ts`, `src/App.tsx`.
- **Requested bounded action:** expose the current brief status and applicable reason through the existing group/job response and render it in the job UI for all four states. Add API/model/UI assertions for the full transition set.
- **Decision impact:** blocks FR-4.

### CP1-F007 — Required regression guards are not reversion-sensitive

- **Severity:** high
- **Evidence:** in isolated scratch copies: (1) deleting the `verifySpawnGrace` call still left the instant-wrapper test passing; (2) deleting executable `installLogSink()` still left the logging-focused tests passing; and (3) removing the launch caller's stale-baseline argument still left all launch/spawn verification tests passing. By contrast, deleting the normal reuse refresh correctly failed its regression test. Logs: `cp1-mutation-grace.log`, `cp1-mutation-sink.log`, `cp1-mutation-baseline-wire.log`, and `cp1-mutation-reuse.log`.
- **Affected paths:** `tests/launchGroup.test.ts`, `tests/spawnVerification.test.ts`, `tests/server.test.ts`, `scripts/fake-pi-agent.sh`.
- **Requested bounded action:** make the delayed-within-grace exit, real executable sink wiring, and caller-level stale-baseline tests fail when their respective production wiring is removed. Add the functional regressions requested in CP1-F001 through CP1-F006; each fix must be proven by a failing mutation/revert check.
- **Decision impact:** independently blocks the V3 test-quality bar.

### CP1-F008 — CP-1 delta violates KISS parameter/file boundaries

- **Severity:** low
- **Evidence:** new `sessionSupervisor.ts` functions `verifyComsRegistrations`, `logOutcome`, and `pendingRoles` each take five parameters; new/modified `launchPane` takes seven. `index.ts` and `App.tsx` are legacy 1599/1124-line files and CP-1 adds retry/UI logic directly to them. New files otherwise stay below 300 lines, `launchGroup.ts` is 299 lines, nesting is bounded, comment density is below 5%, and no dead/commented-out code was found.
- **Affected paths:** `server/sessionSupervisor.ts`, `server/launchGroup.ts`, `server/index.ts`, `src/App.tsx`.
- **Requested bounded action:** use small request/context objects for the new verification and launch helper parameter sets, and extract only the CP-1 retry handler and launch-error UI additions into focused modules. Do not refactor unrelated legacy code.
- **Decision impact:** blocks the explicit checkpoint KISS gate.

## C-3 extraction review

- `attachToken.ts`: after ignoring the intentionally removed explanatory comment and the added export, the executable derivation is byte-for-byte the baseline logic: HMAC-SHA256 over `sessionId` with `base64url`, or 24 random bytes when no secret exists.
- Salt/hash behavior remains the baseline `randomBytes(16)` salt plus unchanged digest/verification helpers; call ordering changed only to obtain the created session object before populating the same fields.
- `attachTokenContinuity.test.ts` plus `sessionStore.test.ts`: 7/7 passed.
- `launchContext.ts`: prior artifact paths/content and write sequence are preserved.
- `launchRequestPreparation.ts`: freshness, context-brief decision persistence, scoped task construction, and implementation pool behavior preserve baseline ordering and values.

## Validation performed

- `npm run typecheck` — PASS.
- `npm run build` — PASS; only the existing non-module script and large-chunk warnings.
- Focused core tests — 15/15 PASS.
- Focused server reuse/retry tests — 2/2 PASS.
- Focused UI model tests — 3/3 PASS.
- Attach-token/store tests — 7/7 PASS.
- Full suite — 1374/1385 PASS; all 11 failures reproduced on baseline.
- Real built-server stdout launch — PASS for sink installation and failure records.
- Partial-spawn tmux cleanup — PASS.
- Context-brief transition capture — PASS for all four statuses/logs.
- Adversarial no-coms, post-registration exit, lane relaunch, and concurrent retry probes — findings recorded above.
- Scratch mutation checks — normal reuse guard sensitive; grace, startup-sink, and baseline-wiring guards insensitive.

Formal final bug-check is not applicable at CP-1; it remains required after the final PRD checkpoint.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "CP-1",
  "revision_reviewed": 0,
  "open_findings": 8,
  "finding_ids": [
    "CP1-F001",
    "CP1-F002",
    "CP1-F003",
    "CP1-F004",
    "CP1-F005",
    "CP1-F006",
    "CP1-F007",
    "CP1-F008"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "lead",
  "report_path": "/tmp/agentops/term1-363/cp1-verifier-verdict.md"
}
```
