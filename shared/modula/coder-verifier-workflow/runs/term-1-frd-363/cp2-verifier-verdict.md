# CP-2 Verifier Verdict — Context-Brief end to end

## Review identity

- **Decision:** `revision_requested`
- **Checkpoint:** CP-2, FR-5 through FR-8
- **Revision reviewed:** 0
- **Branch:** `prd/term-1-fully-functional-363`
- **Prior revision:** `af1ed01a1e3957e0de3aae705596d4c0ff53d006`
- **Committed revision:** `993df2b5531669ac2cc5f354b940edd9baebeb0d`
- **Commit parent:** `af1ed01a1e3957e0de3aae705596d4c0ff53d006`
- **Commit subject:** `feat(term): wire context brief launch gate end to end`
- **Authorized scope:** `term-control-center/` and `pipeline-diagram/`

The worktree is clean. The 22 changed paths are confined to the authorized roots, all changed worktree blobs match the committed revision, no Kody-area path changed, and no CP-3 through CP-7 feature was introduced. The coder handoff records no Git operation.

## Decision summary

The main architecture is real: board/planner producers use project defaults without title/label inference; the lane path independently applies its authoritative project default; required lanes become Context-Brief groups; queued mode and mode-aware reuse work in production; ready continuation starts verifier, coder, researcher, steward, and Lead before retiring the brief; phase-two failure preserves the brief; and empty, whitespace, and null degraded reasons are blocked.

CP-2 cannot close yet. A partial action config can silently weaken the fail-safe `required` default into an automatic skip, malformed degraded reasons can satisfy the operator-reason gate, and two consequential lane/skip wires have no checked-in reversion-sensitive protection. Small new KISS regressions also remain.

**The code is not yet dogfood-ready.** The remaining AC-1 gap is implementation plus the separately operator-gated deploy/dogfood step, not deployment alone.

## Six-claim disposition

| Claim | Result | Independent evidence |
|---|---|---|
| **C-1 fail-safe default** | **FAIL** | Whole-config omission defaults to `required`; malformed objects and `skip` without reason reject; valid caller config is honored. But `{ policy: 'auto', scope: 'tiny' }` is accepted because missing `surfaces` becomes `[]`, then routes to unaudited `skip`. |
| **C-2 no title/label inference** | **PASS** | Repo-wide production search found no remaining title/label-to-scope/surface inference. Both boards use `defaults.contextBrief`; coworker/planner carry loaded config. The only routing inference is from declared config fields in `contextBriefRoute`, as intended. |
| **C-3 double defaulting** | **PASS** | Hand-crafted lane inputs with valid skip, invalid skip, and omitted metadata all produced the authoritative default-required Context-Brief request. A configured project skip with a reason produced implementation plus an exact skip decision. |
| **C-4 lane semantics** | **PASS behavior / FAIL guard completeness** | Run produces mode `context-brief` and its pane; skip carries a decision; queued placeholders retain gated mode; a live implementation group is not reused as a brief. The reuse identity and skip-decision wires lack checked-in mutation-sensitive tests. |
| **C-5 ready continuation** | **PASS** | Real HTTP test starts four implementation roles and one Lead, then removes the brief group. Direct event order is `start` then `retire`; rejected phase two leaves retire count zero. Exact handler-wiring and phase-order mutations fail. |
| **C-6 degraded reason** | **FAIL** | Empty, whitespace, and null return 400 with zero phase-two starts. A reason on a ready path is ignored and ready state remains intact. Object and 501-character JSON reasons are nevertheless accepted as degraded reasons. |

## Open findings

### CP2-F001 — Partial action config silently weakens the fail-safe default

- **Severity:** high
- **Evidence:** `shared/launcher.ts:219` parses `value.surfaces ?? []`. The canonical type and checkpoint contract require `surfaces[]`, but an action config containing only `{ policy: 'auto', scope: 'tiny' }` is normalized to `{ policy: 'auto', scope: 'tiny', surfaces: [] }`. `contextBriefRoute` then returns `{ decision: 'skip', reason: 'declared_small_scope', operatorOverride: false }`.
- **Independent probe:** `/tmp/agentops/term1-363/cp2-verifier-config-probe.out` records the accepted partial input and automatic skip. The same probe confirms whole-config omission becomes `{ policy: 'required', scope: 'unknown', surfaces: [] }`, valid explicit skip is honored with its reason, and null/skip-without-reason inputs reject.
- **Affected paths:** `term-control-center/shared/launcher.ts`, `term-control-center/server/projectActionConfig.ts`, config/handoff tests.
- **Requested bounded action:** require an explicit array-valued `surfaces` field for a supplied Context-Brief config; continue defaulting only when the entire project config is omitted. Add canonical parser/action-config/HTTP handoff coverage for each missing required field, null/non-object, invalid surface, and skip without reason. Preserve valid caller config unchanged and prove the omitted whole config still routes required. Demonstrate an exact parser mutation.
- **Decision impact:** C-1 and FR-5 are not fail-safe; an incomplete project setting can bypass the brief without an operator reason.

### CP2-F002 — Malformed values satisfy the degraded operator-reason gate

- **Severity:** high
- **Evidence:** `server/index.ts:774` coerces arbitrary JSON with `String(request.body?.reason || '').trim()`, while `contextBriefTransition.ts:20` checks only truthiness. An object becomes `[object Object]`; no 500-character bound is applied.
- **Independent HTTP proof:** empty, whitespace, and null correctly returned 400 and created no degraded state. `{ "fabricated": true }` crossed the reason gate as `[object Object]`; a 501-character string also crossed it. The probe used an intentionally invalid launch task to stop before phase-two spawn, and both malformed cases had already written a degraded state, proving the operator gate was passed. Evidence: `/tmp/agentops/term1-363/cp2-verifier-http-reason-probe.out` and `cp2-verifier-transition-probe.out`.
- **Affected paths:** `term-control-center/server/index.ts`, `term-control-center/server/contextBriefTransition.ts`, Context-Brief HTTP/unit tests.
- **Requested bounded action:** accept only a raw string reason, trim it, require non-empty content, and enforce the existing 500-character safety bound before state mutation or phase-two start. Add HTTP regressions for empty, whitespace, null, object/array/number, exactly 500, and 501 characters; confirm a reason on the ready path is not persisted as degraded metadata. Mutating the adapter/domain validation must fail the relevant regression.
- **Decision impact:** FR-8's operator-reason gate is bypassable with fabricated non-text metadata.

### CP2-F003 — Explicit FR-6 wires are behaviorally correct but not reversion-sensitive

- **Severity:** high
- **What is protected:** removing the common lane gate fails the real lane regression; forcing queued placeholders back to implementation also fails an existing queue/reuse assertion. The ready-handler callback and phase-two order are mutation-sensitive.
- **Missing guard 1:** removing only `group.mode === request.mode` from `server/laneOrchestrator.ts:213` left all 11 checked-in lane tests passing. The mutated production then handed the existing implementation group back instead of creating the required queued brief; the independent adversarial probe failed because no brief group existed. Evidence: `/tmp/agentops/term1-363/cp2-verifier-mutation-reuse-mode.log` and `cp2-verifier-mutation-reuse-probe.log`.
- **Missing guard 2:** removing only the `contextBriefDecision` attachment from the skip branch in `server/contextBriefLaunch.ts:20` left all 19 focused Context-Brief/model/lane tests passing. Evidence: `/tmp/agentops/term1-363/cp2-verifier-mutation-skip-decision-focused.log`.
- **Related C-6 gap:** removing HTTP reason trimming still passes the CP-2 end-to-end test; the supplied empty-string unit mutation does not protect whitespace normalization. Evidence: `/tmp/agentops/term1-363/cp2-verifier-mutation-reason-trim-targeted.log`.
- **Requested bounded action:** add (1) a lane test with a live implementation group matching a required-gated request, proving it is not reused as a brief and making removal of mode identity fail; (2) a configured-skip lane/direct test asserting the exact decision survives into the implementation task and skipped-state path; and (3) the HTTP reason-boundary tests in F002. Provide exact-call/branch mutation results.
- **Decision impact:** the mandatory reversion-sensitive checkpoint bar is not met independently of the two production defects.

### CP2-F004 — New CP-2 code crosses the KISS function-size target

- **Severity:** low
- **Evidence:** the CP-2 addition makes `resolveProjectActionConfig` 20 physical lines (`projectActionConfig.ts:98-117`); the house rule is under 20. New/expanded test callbacks are 30 lines at `tests/server.test.ts:270-299`, 21 lines in the first `projectActionConfig.test.ts` case, and 21 lines in the expanded failed-transition `contextBrief.test.ts` case.
- **What passes:** the new 26-line focused gate module is simple; changed focused product files remain below 300 lines; new production helpers have at most four parameters and shallow nesting. Legacy oversized `index.ts`, `shared/launcher.ts`, board HTML, and established test files were not newly created. No new redundant comments, commented-out code, dead branch, or comment-density issue was found.
- **Requested bounded action:** extract only the new resolution field and fixture/setup portions needed to bring the newly crossed functions under the target. Do not refactor legacy files or unrelated tests.
- **Decision impact:** blocks the explicit checkpoint KISS gate, but not FR behavior by itself.

## Claims verified as correct

### Producer and inference audit

- Main and light boards load `/launch-context` and place `defaults.contextBrief` on the task.
- The former `contextBriefConfig` and `contextBriefSurfaceMatches` keyword logic is gone from both pages.
- Production search found no alternative title/body/status/label keyword mapping in board, light board, coworker, planner, Term Control server, shared launcher, or React sources.
- Planning GET returns the project default; POST validates the canonical shape and persists the exact config at `snapshot.task.contextBrief`.
- The invalid planning-handoff request is rejected, though currently through Express's generic error path; this is not the permissive fallback C-1 forbids.

### Authoritative lane probe

`/tmp/agentops/term1-363/cp2-verifier-lane-probe.out` establishes:

- omitted lane metadata → required config, run decision, queued Context-Brief mode;
- valid caller skip and invalid caller skip injected at both root and `laneExecution` levels → ignored in favor of the required project default;
- configured project skip with reason → queued implementation mode with exact operator skip decision;
- existing live implementation group with the same issue/worktree/branch → retained separately while a Context-Brief placeholder is queued, proving mode identity is functional.

### Continuation and retirement

- Fresh HTTP E2E: Context-Brief pane → ready artifacts → continue → implementation roles `verifier`, `coder`, `researcher`, `steward` → one Lead start → brief group removed.
- An exact handler callback mutation regresses returned mode from implementation to context-brief.
- A scratch mutation that retires before `startImplementation` fails the existing phase-two failure regression.
- A supplied reason on an already-ready path does not replace ready state or the route decision.

## Regression and scope

- Focused CP-2 suites run by the verifier: **48/48 passed**.
- CP-1 launch/spawn/summary/Browser-QA regression suite: **20/20 passed**; the full lane suite also passed before mutations.
- `npm run typecheck`: **passed**.
- `npm run build`: **passed**, with only existing Vite script/chunk warnings.
- `node --check` for both changed pipeline JavaScript files: **passed**.
- Full suite: **1401 passed / 11 failed / 1412 total**.
- The 11 failing test names are exactly identical, in order, to the approved CP-1 revision-3 set. Net suite growth is the expected **+6**.
- No Kody path, CP-3 sweep/recovery, CP-4 store work, CP-5 Forge work, CP-6 multi-project work, or CP-7 wake/renewal work was added.

Evidence: `/tmp/agentops/term1-363/cp2-verifier-focused.log`, `cp2-verifier-e2e.log`, `cp2-verifier-cp1-regression.log`, `cp2-verifier-typecheck.log`, `cp2-verifier-build.log`, `cp2-verifier-full-suite.log`, and `cp2-verifier-failure-names.txt`.

Formal final bug-check is not applicable at CP-2.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "CP-2",
  "revision_reviewed": 0,
  "open_findings": 4,
  "finding_ids": [
    "CP2-F001",
    "CP2-F002",
    "CP2-F003",
    "CP2-F004"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "lead",
  "report_path": "/tmp/agentops/term1-363/cp2-verifier-verdict.md"
}
```
