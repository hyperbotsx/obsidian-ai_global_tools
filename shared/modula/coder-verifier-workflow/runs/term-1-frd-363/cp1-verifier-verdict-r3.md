# CP-1 Verifier Verdict — Revision 3

## Review identity

- **Decision:** `approved`
- **Checkpoint:** CP-1, Spawn truth (FR-1 through FR-4)
- **Revision reviewed:** 3
- **Branch:** `prd/term-1-fully-functional-363`
- **Prior revision:** `a9388e7314b2c478105d7145fd5e051d4fcd15d5`
- **Committed revision:** `af1ed01a1e3957e0de3aae705596d4c0ff53d006`
- **Commit parent:** `a9388e7314b2c478105d7145fd5e051d4fcd15d5`
- **Commit subject:** `fix(term): observe lane and browser preflights`
- **Scope:** `term-control-center/` only

The branch is clean. Revision 3 contains exactly six changed files, all under the allowed scope, and every worktree blob matches the committed revision. No CP-2 through CP-7 behavior, periodic sweep, notification bus, Forge, multi-project, wake, or unrelated source change was introduced. The coder handoff records no Git operation; the commit was delivered by Git Manager.

## Decision summary

Both remaining findings are closed. Runtime-slot and Browser-QA decisions now observe physical pane state before acting, including the direct lane-slot, unrelated-capacity, partial-degradation, spawn, and feed-preparation boundaries. The F008 guard now survives harmless private renames and correct 299-line files while rejecting a real fifth private parameter.

The disclosed exported-function-declaration exemption is accepted as a known limitation. It does not hide a current revision-3 defect, and replacing it with private-name allowlisting would restore the brittleness F008 was opened to remove.

**CP-1 FR-1 through FR-4 are met. AC-2/class (a) is met. CP-1 may advance to CP-2.** Proactive detection after a successful spawn with no observer remains the binding CP-3/FR-9 item and is not an open CP-1 finding.

## Finding disposition

| Finding | Result | Independent evidence |
|---|---|---|
| `CP1-F002-i` lane runtime-slot/capacity observation | **CLOSED** | A fresh verifier probe called `runningLaneSlotLetters` alone after killing both panes: it returned `[]`, marked both sessions stale, and set the group to error. With one of two panes alive, it retained `ADHOC-363` and produced `stale/recovered`. The global-capacity-1 integration test also launched past an unrelated dead lane. Removing the exact common observation call failed all three regressions. |
| `CP1-F002-ii` Browser-QA preflight | **CLOSED** | With a physically dead recovered coder pane, independent calls produced zero spawn callbacks and zero preparation callbacks. An already-attached Browser-QA pane returned its existing summary with zero spawn calls. Replacing the shared observer with cached status failed both dead-pane tests; separately removing either entry-point guard failed its specific test. |
| `CP1-F008` structural guard brittleness | **CLOSED with accepted limitations** | A real fifth private parameter failed. Renaming `launchPane` and both call sites passed the structural tests and full typecheck. Padding the trailing-newline file to exactly 299 physical lines passed. No private function name is encoded. |

## F002 independent verification

### Lane decisions

The production decision common to `runningLaneSlotLetters`, `activeLaneGroupCount`, and `batchLaneGroupCount` now invokes `observedGroupStatus(group, sessions)` before reducing pane recoverability.

Fresh verifier evidence in `/tmp/agentops/term1-363/cp1-r3-verifier-probe.out` established:

- all panes physically dead: slot list `[]`, both sessions `stale`, group `error`;
- one of two panes physically dead: slot list `['ADHOC-363']`, recoverability `['stale', 'recovered']`;
- therefore the fix releases all-dead capacity without retiring a genuinely live slot in a partially degraded group.

The checked-in unrelated-lane test used global capacity 1 and passed. In an isolated scratch copy, removing only `observedGroupStatus(group, sessions)` from `laneOccupiesRuntimeSlot` made the direct-slot, partial-degradation, and unrelated-capacity tests all fail. Evidence: `/tmp/agentops/term1-363/cp1-r3-verifier-mutation-lane.log`.

### Browser-QA decisions

`startBrowserPane` observes before request construction, coms snapshot, or spawn. `prepareBrowserQaLaunch` observes before the route invokes feed activation. The pre-existing attached-pane early return remains before spawn, preserving idempotence.

The verifier probe confirmed callback counts of zero at both dead-group entry points and zero spawn calls for an already-attached Browser-QA pane. Mutation evidence:

- cached `group.status` in place of physical observation: both dead-pane regressions fail;
- removal of the `startBrowserPane` guard: spawn-boundary regression fails;
- removal of the preparation guard: preparation-boundary regression fails.

Evidence: `/tmp/agentops/term1-363/cp1-r3-verifier-mutation-browser-observer.log`, `cp1-r3-verifier-mutation-browser-start.log`, and `cp1-r3-verifier-mutation-browser-prepare.log`.

## F008 judgement and KISS review

The 38-line structural test recursively visits non-exported function-like AST nodes in `launchGroup.ts` and `sessionSupervisor.ts`, enforces at most four parameters, retains AST import-boundary checks, and discounts only the terminal empty line segment.

Independent scratch checks proved:

- five parameters on the real private `launchPane` declaration fail with `FunctionDeclaration exceeds the four-parameter limit`;
- `launchPane` to `spawnPane` passes both structural tests and full typecheck;
- a trailing-newline `launchGroup.ts` with exactly 299 physical lines passes.

Evidence: `/tmp/agentops/term1-363/cp1-r3-verifier-mutation-f008-five.log`, `cp1-r3-verifier-f008-rename.log`, and `cp1-r3-verifier-f008-lines.log`.

### Accepted known limitations

- **`CP1-F008-KNOWN-1` — exported function declarations are exempt.** Existing public APIs `startLaunchGroup` and `startBrowserQaPane` already exceed the private-helper budget. A future author could evade this nice-to-have test by exporting a function declaration. This is explicit, does not conceal a current defect, and has no checkpoint decision impact.
- **`CP1-F008-KNOWN-2` — one new integration-test callback spans 23 physical lines.** It is bounded fixture setup/assertion/cleanup around the global-capacity probe, has shallow nesting, and follows the neighboring integration-test pattern. This literal house-target deviation is recorded as non-blocking test structure rather than reopening a closing product checkpoint.

Changed focused product files are 81 and 267 lines; new production functions are under 20 lines, have at most three parameters, and remain shallow. `server/index.ts` is a pre-existing 1,580-line legacy file; revision 3 adds only an import and routes one existing callback through the focused helper. No redundant comments, commented-out code, new dead code, or comment-density issue was found.

## Regression and validation

- Focused Browser-QA, lane, and structural suites: **15/15 passed**.
- `npm run typecheck`: **passed**.
- `npm run build`: **passed**, with only the existing Vite script/chunk warnings.
- Full suite: **1395 passed / 11 failed / 1406 total**.
- The 11 failing names are exactly identical, in order, to the revision-2 verifier failure set; no new failure replaced an old one:
  1. `pi-agent refuses to launch when no pi-coms-local copy can be verified (QW-3)`
  2. `pi-agent wrapper preserves PI_COMS_MODEL_LABEL into the launched pi process`
  3. `pi-agent wrapper honors draft-scoped coms project overrides`
  4. `pi-agent loads only the named bridge when its prerequisites exist`
  5. `fix-loop launch wiring carries selected findings into task details`
  6. `Browser-QA pane can be added to a running implementation group`
  7. `coworker lane proposals receive a server-derived current precondition fingerprint`
  8. `lane execution rejects lanes outside configured slots`
  9. `production IDs are finite and validation IDs require the test harness`
  10. `plan isolates namespaces and reconstructs the exact environment`
  11. `worktree is the only writable real-data bind and protected children are read-only`
- Net suite growth from revision 2 is the expected **+5** tests.

Evidence: `/tmp/agentops/term1-363/cp1-r3-verifier-focused.log`, `cp1-r3-verifier-typecheck.log`, `cp1-r3-verifier-build.log`, `cp1-r3-verifier-full-suite.log`, and `cp1-r3-verifier-failure-names.txt`.

Formal final bug-check is not applicable at CP-1 and remains due after the final PRD checkpoint.

## Machine Status

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "CP-1",
  "revision_reviewed": 3,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "not_applicable",
  "next_actor": "lead",
  "report_path": "/tmp/agentops/term1-363/cp1-verifier-verdict-r3.md"
}
```
