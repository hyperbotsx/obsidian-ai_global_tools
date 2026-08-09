# CP-1 Verifier Verdict — Revision 2

## Review identity

- **Decision:** `revision_requested`
- **Checkpoint:** CP-1, Spawn truth (FR-1 through FR-4)
- **Revision reviewed:** 2
- **Branch:** `prd/term-1-fully-functional-363`
- **Prior revision:** `d0355244e3e224b02a9e0e07449be7d82f1f7c72`
- **Committed revision:** `a9388e7314b2c478105d7145fd5e051d4fcd15d5`
- **Commit parent:** `d0355244e3e224b02a9e0e07449be7d82f1f7c72`
- **Commit subject:** `fix(term): harden spawn observation boundaries`
- **Scope:** `term-control-center/` only

I reviewed the committed 18-file revision. All 18 worktree blobs match the commit, and the complete non-generated `term-control-center/` inventory has no unexpected or missing source files.

## Lead ruling applied

I did **not** re-raise proactive no-observer detection after a successful spawn. The measured class (b) residual—approximately 3.5–7 seconds with active UI polling and unbounded with no observer—is accepted as deferred to CP-3/FR-9.

The CP-1 class (a) exit bar is now met: exits before grace, inside grace, while awaiting registration, and at the registration deadline boundary fail to `error`, preserve the true cause, clean panes, and are test-enforced. Revision 2 still cannot advance because the bounded F002-b mitigation missed real observation consumers, and the F008 structural test still encodes brittle internal names/line counting.

## Finding disposition

| Finding | Result | Independent evidence |
|---|---|---|
| `CP1-F002-a` exit while awaiting registration | **CLOSED** | Polling checks tmux before every sleep and after loop exit. Independent 10/70/115/120 ms boundary kills all reported `pane exited while awaiting coms registration`; a live pane at deadline reported the registration timeout. |
| `CP1-F002-b` proactive no-observer detection | **DEFERRED per Lead** | Not raised as a CP-1 finding. |
| `CP1-F002-b` refresh-backed consumer routing | **OPEN** | Literal `.status` reads are enumerated correctly, but lane slot/capacity observers bypass the accessor and return stale running state. Browser-QA preflight also spawns before observing group state. |
| `CP1-F006` hostile brief-state boundary | **CLOSED** | Non-string/missing/empty/oversized values are omitted at the server summary boundary; 500/501 limits behave correctly; valid Unicode/control strings remain strings and serialize safely. |
| `CP1-F007` observation and registration-wait guards | **CLOSED** | New summary test calls only `groupSummary`; replacing `observedGroupStatus` with raw `group.status` fails `running !== error`. Await-registration mutation also fails for the intended cause. |
| `CP1-F008` structural guard | **OPEN** | AST defeats comments and enforces `<=4`, but exact internal function names and an off-by-one trailing-newline line count will reject harmless future refactors. |

## Open findings

### CP1-F002 — Consumer enumeration is syntactically complete but operationally incomplete

- **Severity:** high
- **Literal audit result:** a TypeScript-checker audit found every direct `SessionGroup.status` property read. Outside `groupStatus.ts`, the remaining direct accesses are lifecycle assignments; the two job route reads are on already-materialized summaries. That portion of the handoff is accurate.
- **Missed observation:** `laneOccupiesRuntimeSlot` at `server/laneOrchestrator.ts:252-258` decides running slot/capacity from cached session `recoverability` without first invoking `observedGroupStatus` or `refreshGroupLiveness`. It is used by `runningLaneSlotLetters`, `activeLaneGroupCount`, and `batchLaneGroupCount`.
- **Independent proof:** after killing the only tmux pane while leaving its session marked `recovered`, `runningLaneSlotLetters` returned `['A']`, raw group state remained `running`, and recoverability remained `recovered`. Only a later `groupSummary` changed the group to `error`/`stale`, after which the same slot reader returned `[]`. Evidence: `/tmp/agentops/term1-363/cp1-r2-missed-lane-consumer.out`.
- **Impact:** this is an actual observer, not the deferred no-observer window. It can falsely block execution-slot reduction through `runningLaneSlots` and can make unrelated dead lanes continue consuming `activeLaneGroupCount`/batch capacity.
- **Secondary missed decision:** `browserQaPaneHandler`/`startBrowserPane` does not observe the existing implementation group before spawning. With a physically dead recovered coder pane, the helper spawned and attached a Browser-QA pane before the returned summary finally marked the group `error`; the new browser session was still present at return (`cp1-r2-missed-browser-preflight.out`).
- **Requested bounded action:** refresh/observe at the start of the common lane runtime-slot decision so all three callers see physical state, while still counting genuinely live panes in partially degraded groups. Add a dead-tmux regression that calls only `runningLaneSlotLetters` and a lane-capacity regression for an unrelated dead lane. Require a live observed implementation group before Browser-QA side effects and assert the spawn callback is not invoked for a dead group. Demonstrate exact-call mutations. No timer, sweep, or notification bus is requested.
- **Decision impact:** the Lead-ruling in-scope half of F002-b remains incomplete; routed observations can still report/act on stale running state.

### CP1-F008 — AST guard still fights harmless refactors

- **Severity:** low
- **What is fixed:** the 39-line test uses real TypeScript AST declarations/imports, ignores decoy comments/formatting, and correctly rejects five parameters with a `<=4` threshold. The product files themselves satisfy the KISS budget.
- **Exact-name brittleness:** a scratch-only rename of private `launchPane` to `spawnPane`, including both call sites and with identical one-parameter behavior, passed the full TypeScript typecheck but failed the structural test with `missing function launchPane`. This internal name is not a CP-1 architecture contract and may legitimately change during CP-2..CP-7. Evidence: `cp1-r2-structure-rename.log` and `cp1-r2-structure-rename-typecheck.log`.
- **Line-count brittleness:** `lineCount` uses the AST end position. On the current trailing-newline file, the test reports 278 lines while the file has 277 newline-terminated lines. A permitted 299-line file would be treated as 300 and rejected. Evidence: `cp1-r2-structure-linecount.out`.
- **Requested bounded action:** traverse actual function-like AST nodes in the CP-1 modules and enforce the four-parameter maximum without requiring private function names. Correct line counting for a trailing newline. Keep the AST import-boundary assertions. Prove a harmless rename/format change passes while a real fifth parameter fails.
- **Decision impact:** the explicit “will not fight CP-2..CP-7” F008 bar remains open.

## F002-a boundary verification

| Timing | Result |
|---|---|
| Immediate/before grace | `error`; pane-exited reason. |
| Delayed exit inside grace | `error` before registration polling. |
| After grace, before registration | Failed at about 200 ms under a 400 ms deadline with `coder pane exited while awaiting coms registration`; zero sessions. |
| Poll-loop kills at 10, 70, and 115 ms | Early true-cause exit result. |
| Kill scheduled at 120 ms deadline boundary | True-cause exit result from the loop-exit check. |
| No kill through deadline | Correct `did not register with coms before the deadline` result. |

Evidence: `cp1-r2-spawn-boundaries.log`, `cp1-r2-exit-before-registration.out`, and `cp1-r2-registration-boundary.out`.

**AC-2/class (a) conclusion:** silent `running`-with-nothing is impossible for the spawn-gate failure class and is regression-tested.

## F006 hostile-state verification

At the server boundary:

- Arrays, nested objects, `null`, missing values, empty strings, whitespace-only strings, and a 501-character reason are omitted.
- A normal Unicode reason and exactly 500 characters are retained.
- Optional `statusReason`: absent falls back to valid `reason`; `null` and 501 characters omit the whole state; exactly 500 is retained.
- NUL, zero-width, and embedded control values remain accepted because they are bounded non-empty strings; they remain JSON-serializable strings and cannot become an object React child. No executable/markup interpretation was found.
- Omission happens in `readContextBriefState` before `groupSummary` constructs the API object, protecting all `/groups` consumers.

Evidence: `cp1-r2-brief-boundary.out`, `cp1-r2-brief-statusreason-boundary.out`, and 12/12 focused brief/UI tests.

## F007 regression sensitivity

- `tests/reusableGroup.test.ts` constructs a physically dead tmux pane still marked `recovered` and invokes only `groupSummary`.
- My fresh scratch mutation replaced only `observedGroupStatus(group, sessions)` with raw `group.status`; the targeted test failed with zero passes and `running !== error` (`cp1-r2-mutation-summary.log`).
- The registration-wait mutation targets `exitedPendingRole`; the true-cause test regresses to the old timeout reason.

F007 is closed.

## Session-token extraction

- `tokenDigest` and `tokenMatches` function bodies in `sessionToken.ts` are byte-identical to their revision-1 definitions, including 16 random salt bytes, SHA-256 input `${salt}:${token}`, hex digest, and truthiness checks.
- The crypto import is identical.
- `sessionSupervisor` now imports the leaf module directly; `sessionStore` re-exports it. `groupStatus` imports `launchGroup` types only, so the cycle break introduces no runtime initialization dependency.
- Attach-token continuity/session-store tests pass 7/7.

Evidence: `cp1-r2-token-compare.out` and `cp1-r2-token-tests.log`.

## Regression and scope

- Full suite: **1390 passed / 11 failed / 1401 total**.
- The 11 failing test names exactly match revision 1 and the verifier-confirmed baseline set.
- Net suite growth is the expected **+3**: five new test names replacing two prior names.
- `npm run typecheck` and `npm run build` pass with only existing Vite warnings.
- New/changed focused modules are below 300 lines with low comment density; no new dead/commented-out code was found.
- No CP-3 sweep or proactive no-observer mechanism was introduced. No CP-2 lane-gate, store-hardening, forge, multi-project, or later-checkpoint scope was added.

Formal final bug-check remains not applicable at CP-1.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "CP-1",
  "revision_reviewed": 2,
  "open_findings": 2,
  "finding_ids": [
    "CP1-F002",
    "CP1-F008"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "lead",
  "report_path": "/tmp/agentops/term1-363/cp1-verifier-verdict-r2.md"
}
```
