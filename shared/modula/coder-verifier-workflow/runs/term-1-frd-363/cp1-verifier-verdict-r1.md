# CP-1 Verifier Verdict — Revision 1

## Review identity

- **Decision:** `revision_requested`
- **Checkpoint:** CP-1, Spawn truth (FR-1 through FR-4)
- **Revision reviewed:** 1
- **Branch:** `prd/term-1-fully-functional-363`
- **Prior revision:** `a2b0b121f82e02a190011d5240ab4bd7c8d596aa`
- **Committed revision:** `d0355244e3e224b02a9e0e07449be7d82f1f7c72`
- **Commit parent:** `a2b0b121f82e02a190011d5240ab4bd7c8d596aa`
- **Commit subject:** `fix(term): close spawn verification gaps`
- **Scope:** `term-control-center/` only

I reviewed the committed 24-file revision, not just the handoff. All 24 reviewed worktree blobs match the committed tree. The complete non-generated `term-control-center/` file inventory matches the expected base plus committed additions: no extra or missing source file was found. No out-of-scope or #264 Kody-area path changed.

## Decision summary

Revision 1 materially improves CP-1 and closes four findings outright. The all-mode pool wiring, lane retirement, concurrent retry serialization, and structured logging now work under independent probes. The main F002 race remains, however: stabilization only catches exits before its one final check. A pane exiting after that check leaves raw backend state `running` with no live tmux for an unbounded period when no summary observer is active. A pane exiting before it registers also waits until the coms deadline and reports registration timeout rather than the real tmux-exit cause. Brief-state surfacing works for valid state but its supposedly safe reader accepts an object-valued reason that crashes the React surface. Regression protection still does not guard the summary-observation wiring, and the KISS structural test is trivially bypassable while typecheck remains green.

## Original finding disposition

| Finding | Result | Independent evidence |
|---|---|---|
| `CP1-F001` all agent panes receive fresh coms verification | **CLOSED** | Direct production-function probe verified implementation, context-brief, PRD review, planning draft, authoring draft, and page-bot-control pools plus injected env. A live non-registering context-brief now reaches `error`; stale Browser-QA registration is rejected. |
| `CP1-F002` registration/tmux TOCTOU | **OPEN** | Exits inside stabilization are caught, but an exit after the final check leaves raw state `running`; pre-registration death is not checked during polling. |
| `CP1-F003` lane liveness short-circuit/capacity | **CLOSED** | Every dead pane becomes stale; all-dead lane is removed and replaced without queueing. Removing the retirement call fails the lane test for the old group remaining present. |
| `CP1-F004` concurrent retry | **CLOSED** | Independent overlap probe returned one 200 and one bounded 409, with one referenced session and no orphan. `finally` releases the claim on exceptions. |
| `CP1-F005` incomplete FR-1 records | **CLOSED** | PTY now emits an attempt; success/failure outcomes have reasons; the real built executable emits `supervisor/server_startup` after sink installation. |
| `CP1-F006` brief state not surfaced | **OPEN** | Valid states are surfaced and absent state is truly omitted, but malformed agent-written reason data crosses the API type boundary and crashes rendering. |
| `CP1-F007` insensitive regression guards | **OPEN** | Most supplied mutations target the right production wiring, but removal of the critical summary refresh still passes 13 focused CP-1 tests; no post-final-exit guard exists. |
| `CP1-F008` KISS boundaries | **OPEN** | Production structure is corrected, but `cp1Structure.test.ts` can be satisfied by a comment while the actual function violates the parameter budget and typecheck passes. |

## Open findings

### CP1-F002 — Stabilization narrows but does not close spawn liveness races

- **Severity:** high
- **What revision 1 fixed:** `verifyComsRegistrations` now waits a configurable interval and checks tmux once at `server/sessionSupervisor.ts:66-68`; `groupSummary` refreshes physical liveness on observation at `server/launchGroup.ts:159`.
- **Post-final evidence:** with 20 ms grace, 20 ms stabilization, and a wrapper exiting at 200 ms, the group reached `running` at 110 ms. After the wrapper exited, raw group state was still `running` while tmux was absent. Calling `groupSummary` then changed it to `error` with `coder pane tmux session is missing`. Evidence: `/tmp/agentops/term1-363/cp1-r1-post-final-race.out`.
- **Window size:** the configured stabilization interval only defines when the final check occurs; it does not bound the later stale-running interval. With an active UI, `/groups` polling normally observes it within approximately 3.5–7 seconds. With no active observer, the interval is unbounded. Several backend consumers also read `group.status` directly rather than through `groupSummary`.
- **Pre-registration evidence:** a wrapper that survived the 20 ms grace, exited at 150 ms, and never registered did not fail until 489 ms under a 400 ms deadline. Its reason was `coder pane did not register with coms before the deadline`, not the true tmux-exit cause. Evidence: `/tmp/agentops/term1-363/cp1-r1-exit-before-registration.out`; `pendingRoles` at `server/sessionSupervisor.ts:87` never checks tmux.
- **Requested bounded action:** during registration polling, fail immediately when any expected tmux session disappears and record the exit cause. Make the post-success state fail closed without depending on an optional UI observer—either use an event-backed supervisor notification or route every status-sensitive backend consumer through one refresh-backed status accessor without adding the CP-3 periodic sweep. Add deterministic tests for (1) exit while awaiting registration and (2) exit after the final stabilization check, asserting truthful backend state before manually calling `groupSummary`.
- **Decision impact:** FR-2 and the explicit V2 bar remain open.

### CP1-F006 — Brief-state reader accepts unsafe runtime data

- **Severity:** medium
- **What revision 1 fixed:** all valid transitions surface through summaries and UI. A group with no state has no own `contextBriefState` property, and `Lead renewal reloads only its live route context` passes.
- **Evidence:** `readContextBriefState` validates only the status enum at `server/contextBrief.ts:41-48`; it does not validate `reason` or `statusReason`. A valid-status state file containing an object reason produced `reasonRuntimeType: object` in the group response (`cp1-r1-malformed-brief.out`). Passing that response to `GroupLaunchStatus` throws `Objects are not valid as a React child` (`cp1-r1-malformed-brief-render.out`). The ready-state file is agent-written, so this is an actual runtime trust boundary.
- **Requested bounded action:** require a bounded string reason/statusReason before exposing state, otherwise omit the state or emit a safe fallback. Apply the same runtime validation to `/groups` consumers or normalize at the server boundary. Add malformed/missing reason tests proving API serialization and rendering remain safe.
- **Decision impact:** FR-4 surfacing is not yet robustly closed.

### CP1-F007 — Critical observation wiring remains unprotected

- **Severity:** high
- **Mutation audit:** the supplied F001, F002, F003, F004, F005-PTY, F005-reason, F006, baseline, grace, and executable-sink mutations all touch their actual production dependency and fail for the intended assertion. The separate all-dead-lane test also fails when `retireDeadLaneGroups` is removed.
- **Missing guard evidence:** in a fresh scratch copy, deleting only `refreshGroupLiveness(group, sessions)` from `groupSummary` left all 13 focused launch, reuse, Browser-QA, and retry tests passing. Evidence: `/tmp/agentops/term1-363/cp1-r1-mutation-observation.log`.
- **Why it matters:** summary-time refresh is the only revision-1 mitigation after the final F002 check. The checked `reusableGroup` test explicitly calls `refreshGroupLiveness` before `groupSummary`, so it cannot detect removal of summary observation. There is also no test for an exit after stabilization.
- **Requested bounded action:** add a direct group-summary/API regression that begins with a physically dead tmux pane still marked recovered and fails if the observation refresh is removed. Add the post-final and pre-registration-exit guards requested in CP1-F002, and demonstrate each by mutating its exact production call/branch.
- **Decision impact:** the mandatory reversion-sensitive V3 gate remains open.

### CP1-F008 — Structural guard is brittle and trivially bypassed

- **Severity:** low
- **What revision 1 fixed:** production functions now use request objects; focused modules are 25–159 lines; `launchGroup.ts` is 299 lines; retry/UI additions were extracted. Current CP-1 product structure passes the KISS budget.
- **Evidence:** `tests/cp1Structure.test.ts:12-15` searches raw source with exact regex strings. In a scratch copy, `launchPane` was changed to five parameters—one required plus four optional—and the exact one-parameter signature was placed in an inline comment. Both `cp1Structure.test.ts` and the full TypeScript typecheck passed. Evidence: `cp1-r1-structure-bypass.log` and `cp1-r1-structure-bypass-typecheck.log`.
- **Brittleness:** the test can be defeated by comments and also rejects harmless formatting or a two-parameter form even though the house maximum is 3–4. Its current revert proves only that one exact string disappeared.
- **Requested bounded action:** parse TypeScript AST declarations and assert the actual parameter counts against the house threshold; compute line counts robustly. Use AST import declarations for extraction boundaries rather than formatting-sensitive regex. Add a bypass mutation with more than four optional parameters and prove the structural test fails without relying on comments or exact formatting.
- **Decision impact:** the explicit F008 re-verification bar remains open.

## Independent adversarial probes required for revision 1

| Probe | Result |
|---|---|
| Live context-brief pane with no registration | PASS — `error`, accurate no-registration reason, pane cleanup. |
| Register then exit | FAIL beyond the fixed interval — caught when exit occurs inside stabilization; remains raw `running` when exit occurs after final check until observed. |
| All-dead lane relaunch | PASS — replacement starts, old lane retires, capacity releases; retirement-call mutation fails. |
| Concurrent retry overlap | PASS — statuses `[200, 409]`, one session, one referenced pane, zero orphans. |

Partial-spawn cleanup was also rerun: both tmux panes were killed, zero sessions remained, and the reason identified the coder pane exit.

## Revert-check assessment

Eleven supplied logs all contain one intended test failure. Inspection of the exact scratch diffs found:

- **Correct production targets:** non-implementation verification call, stabilized final tmux check, all-pane liveness aggregation, retry claim, PTY attempt publication, successful outcome reason, brief-state summary exposure, Browser-QA baseline argument, grace call, and executable sink installation.
- **Additional independent sensitivity proof:** removing lane retirement fails because the dead group remains; this covers the lane half not mutated by the supplied F003 check.
- **Insufficient target/guard:** the F008 raw-regex test is trivially satisfiable despite a real five-parameter declaration; summary observation and post-final liveness have no sensitive revert guard.

## Regression surface

- Full suite: **1387 passed / 11 failed / 1398 total**, exactly as dispatched.
- The failing set is byte-for-name identical to revision 0: four pi-agent/context-renewal fixture failures, Kody source-regex expectation, Browser-QA missing-target fixture, coworker fingerprint 400, lane hard-cap ordering, and three sandbox `deny_sandbox_start` failures.
- Suite growth is the claimed net **+13**: 14 new test names and one replaced/expanded reuse test name. No unrelated failure replaced a known failure.

## Validation performed

- `npm run typecheck` — PASS.
- `npm run build` — PASS; only existing Vite warnings.
- `npm test` — 1387/1398 PASS with the unchanged 11-failure set.
- Launch/liveness focused suite — 11/11 PASS.
- Browser stale-baseline test — PASS.
- Concurrent retry test — PASS.
- Valid brief surfacing, UI wiring, absent-property check, and Lead renewal — PASS.
- Real built executable startup sink record — PASS.
- All-mode pool/env derivation probe — PASS for six mode/surface categories.
- Independent no-coms, post-final-exit, pre-registration-exit, all-dead-lane, concurrent-retry, partial-kill, malformed-brief, observation-mutation, lane-mutation, and structural-bypass probes — results recorded above.
- KISS audit — production delta passes file/comment/parameter boundaries requested in F008; the structural test itself does not.

Formal final bug-check is not applicable at CP-1 and remains due after the final PRD checkpoint.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "CP-1",
  "revision_reviewed": 1,
  "open_findings": 4,
  "finding_ids": [
    "CP1-F002",
    "CP1-F006",
    "CP1-F007",
    "CP1-F008"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "lead",
  "report_path": "/tmp/agentops/term1-363/cp1-verifier-verdict-r1.md"
}
```
