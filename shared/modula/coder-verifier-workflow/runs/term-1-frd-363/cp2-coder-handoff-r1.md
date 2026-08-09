# CP-2 Coder Handoff — Revision 1

## Source and scope

- Base: `993df2b`
- Lead brief: `/tmp/agentops/term1-363/cp2-fix-round-1.md`
- Verifier verdict: `/tmp/agentops/term1-363/cp2-verifier-verdict.md`
- Findings addressed: CP2-F001 through CP2-F004.
- No git, deploy, CP-3 through CP-7, or Kody-path work.

## CP2-F001 — partial config no longer weakens the default

**Status: fixed.**

The canonical parser now distinguishes whole-config omission from a partial supplied config:

- Omitted `ProjectActionConfig.contextBrief` still resolves to the fail-safe `{ policy: 'required', scope: 'unknown', surfaces: [] }`.
- A supplied config must explicitly provide valid `policy`, `scope`, and array-valued `surfaces`.
- Missing fields, null/non-object configs, invalid surface values, and skip without a bounded non-empty reason are rejected.
- Valid supplied configs pass through with their exact declared values.
- Skip reasons are trimmed, non-empty, and at most 500 characters.

Coverage:

- Direct canonical parser and action-config tests cover missing policy/scope/surfaces, null, non-object, invalid surface, missing/blank/501-character skip reasons, valid caller config, and whole-config omission.
- Planning-handoff HTTP coverage carries the same malformed matrix, including an entirely missing config.

Exact mutation:

- Scratch mutation restored only `contextBriefSurfaces(value.surfaces ?? [], errors)`.
- `/tmp/agentops/term1-363/revert-checks-cp2-r1/F001-parser/revert.log`
- Result: the missing-surfaces case was accepted and the focused contract test exited 1.

## CP2-F002 — operator reason is real bounded text

**Status: fixed.**

Added `shared/boundedText.ts` as the shared trust-boundary primitive:

- raw strings only,
- trim before use,
- reject empty/whitespace,
- default maximum 500,
- configurable larger bound for deliberate long-form fields.

The HTTP adapter no longer coerces arbitrary JSON through `String(...)`. `continueContextBrief` accepts `unknown`, validates and normalizes it itself, and does so before degraded-state mutation or phase-two launch.

HTTP coverage proves:

- empty, whitespace, null, object, array, number, and 501 characters return 400;
- none of those values changes pending state or starts phase two;
- exactly 500 characters succeeds;
- a spaced valid reason is persisted trimmed;
- a reason supplied on the already-ready path is ignored, the ready state remains ready, and no degraded metadata is written.

Direct shared-validator coverage is in `tests/boundedText.test.ts` and independently covers empty, whitespace, null, object, array, number, trimming, exactly 500, and 501.

Exact mutations:

1. Replaced only `boundedText(transition.reason)` with the old coercive `String(...).trim()` path.
   - `F002-reason/revert.log`: object/array/number/501 HTTP matrix failed.
2. Replaced the same call with a type/length check that did not trim.
   - `F003-trim/revert.log`: raw persisted reason retained surrounding whitespace.
3. Removed only the validator’s `text.length <= limit` condition.
   - `shared-validator/revert.log`: the direct 501-character unit assertion failed.

All paths are under `/tmp/agentops/term1-363/revert-checks-cp2-r1/`.

## CP2-F003 — missing reversion-sensitive wires

**Status: fixed.**

### Lane reuse mode identity

Added `required gate does not reuse a matching live implementation group`:

- starts from a live implementation group with the same issue/worktree/branch/lane identity,
- capacity is one,
- required-gated execution must retain that implementation and create a separate queued `context-brief` group.

Removing only `group.mode === request.mode` makes the implementation satisfy brief reuse and the test fails.

- Evidence: `F003-mode/revert.log`.

### Skip decision attachment

Added `skip routing preserves its exact decision and skipped state`:

- sends an explicit valid skip config through `contextBriefLaunch`,
- runs the real launch preparation path,
- asserts exact `{ decision: 'skip', reason, operatorOverride: true }` task metadata,
- asserts persisted `skipped` state with the same reason.

Removing only the skip branch’s `contextBriefDecision` attachment fails the test.

- Evidence: `F003-skip/revert.log`.

### Reason trimming

The HTTP persistence assertion now reads the raw state file, not only the normalized API view. The non-trimming mutation fails as described under F002.

## CP2-F004 — KISS

**Status: fixed.**

- `resolveProjectActionConfig`: 19 physical lines; Context-Brief resolution is in `resolveContextBrief`.
- Server ready E2E callback: 15 lines.
- Malformed HTTP-reason callback: 14 lines.
- Trim HTTP callback: 11 lines.
- Project-action parse callback: 8 lines after fixture extraction.
- Failed-transition test callback: 8 lines; `exerciseBlockedTransitions`: 14 lines.
- `tests/laneOrchestrator.test.ts`: 299 lines.
- All changed focused product files remain below 300 lines; new functions are at most four parameters with shallow nesting.

No legacy/unrelated refactor was performed.

## Trust-boundary sweep

### Search method

Searched CP-1/CP-2 production surfaces with `rg` for:

- `reason`, `statusReason`, `operatorText`, `resolution`, and `message`,
- `String(request.body...)` and direct body fields,
- persistence/API/gate consumers in launcher validation, Context-Brief state/transition, launch summaries, planning intake/briefs/receipts, page-bot messaging, and session restoration.

Inspected:

- `shared/launcher.ts`,
- `contextBrief.ts`, `contextBriefTransition.ts`, `contextBriefLaunch.ts`,
- `launchGroup.ts`, `sessionStore.ts`,
- `planningIntakeStore.ts`, `planningBrief.ts`, `plannerReceiptStore.ts`,
- `pageBotInjection.ts`, `pageBotRuntime.ts`,
- relevant `index.ts` routes.

A final search confirms the permissive `surfaces ?? []`, `String(request.body?.reason...)`, local `boundedReason`, and truthiness-only transition guard are gone.

### Findings fixed

1. **Context config and decision reasons** — now use shared bounded/trimmed text.
2. **Agent-written Context-Brief state reason/statusReason** — reader uses the shared validator; writer omits invalid status reasons.
3. **Group and pane statusReason API output** — `groupSummary` and `paneSummary` strip malformed/oversized runtime or restored values before JSON exposure.
4. **Planning decision question/resolution** — both are bounded to 500 before persistence; persisted decision validation applies the same rule.
5. **Planning brief plain-text fields** — bounded to 20,000, matching the existing long task-text contract. Structured arrays/objects remain JSON-typed and are rendered through JSON serialization.
6. **Operator page-bot messages and injected messages** — bounded to 20,000 before conversation persistence; injection receipt edit notes are bounded to 500.
7. **Planner receipt reasons** — now use the 500-character reason bound instead of the generic 4096-character text rule. Internally generated operator text retains its existing 4096 bound.
8. **Internally propagated intake errors** — normalized through bounded reason text before rejected receipts.

### Sweep regressions and exact mutations

Each retained guard has an exact production-wiring scratch mutation:

| Surface | Evidence |
|---|---|
| Shared validator limit | `shared-validator/revert.log` |
| Brief-state reader | `sweep-state-read/revert.log` |
| Brief-state writer statusReason | `sweep-state-write/revert.log` |
| Group summary statusReason | `sweep-group-reason/revert.log` |
| Pane summary statusReason | `sweep-pane-reason/revert.log` |
| Planning decision question | `sweep-question/revert.log` |
| Planning decision resolution | `sweep-resolution/revert.log` |
| Planning brief plain text | `sweep-planning-text/revert.log` |
| Operator page-bot message | `sweep-pagebot-send/revert.log` |
| Injected page-bot message | `sweep-pagebot-inject/revert.log` |
| Injection edit note | `sweep-edit-note/revert.log` |
| Planner receipt reason | `sweep-receipt-reason/revert.log` |

All exited non-zero for the intended assertion, not compilation failure.

### Found but not changed

- **Session-store raw restored statusReason validation:** identified. Raw store schema hardening is explicitly CP-4. CP-1/CP-2 summaries now sanitize it before API exposure, closing the current checkpoint’s trust-boundary effect without taking CP-4 scope.
- **Planner agent replies:** the planner runtime already enforces a 16 KiB line limit and 32-line turn limit before its persistence callback.
- **Kody `needsHumanReason`:** forbidden Kody surface; untouched.
- **Completion/closeout, pipeline-refresh, and admin-only reasons:** outside CP-1/CP-2. The inspected admin refresh reason is already sliced to 80 characters, but no later-checkpoint refactor was taken.

## Files changed in revision 1

Production:

- `term-control-center/shared/boundedText.ts` (new)
- `term-control-center/shared/launcher.ts`
- `term-control-center/server/contextBrief.ts`
- `term-control-center/server/contextBriefTransition.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/pageBotInjection.ts`
- `term-control-center/server/plannerReceiptStore.ts`
- `term-control-center/server/planningBrief.ts`
- `term-control-center/server/planningIntakeStore.ts`
- `term-control-center/server/projectActionConfig.ts`

Tests:

- `term-control-center/tests/boundedText.test.ts` (new)
- `term-control-center/tests/briefStateSafety.test.ts`
- `term-control-center/tests/contextBrief.test.ts`
- `term-control-center/tests/laneOrchestrator.test.ts`
- `term-control-center/tests/pageBotInjection.test.ts`
- `term-control-center/tests/plannerReceiptBounds.test.ts` (new)
- `term-control-center/tests/planningIntakeRoutes.test.ts`
- `term-control-center/tests/planningIntakeStore.test.ts`
- `term-control-center/tests/projectActionConfig.test.ts`
- `term-control-center/tests/server.test.ts`

## Validation

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- Focused CP-1/CP-2 boundary/gate suite: **66/66 passed**.
  - `/tmp/agentops/term1-363/cp2-r1-focused-final.log`
- HTTP reason matrix and ready-path suite: **3/3 passed**.
  - latest command rerun after final normalization cleanup
- Direct boundary/sweep suite: **25/25 passed**.
- Exact production-wiring scratch checks: **17/17 failed as intended**.
  - `/tmp/agentops/term1-363/revert-checks-cp2-r1/`

Full suite:

- `cd term-control-center && npm test`
- **1412 passed / 11 failed / 1423 total**.
- `/tmp/agentops/term1-363/cp2-r1-full-suite.log`
- The 11 failures exactly match the approved baseline set: four wrapper/coms fixture failures, fix-loop source expectation, Browser-QA missing-target fixture, coworker fingerprint fixture, lane hard-cap ordering expectation, and three sandbox `deny_sandbox_start` failures.

Final build log: `/tmp/agentops/term1-363/cp2-r1-build-final.log` (only existing Vite warnings).

## Deviations and disagreements

None. Store-file schema validation remains assigned to CP-4; this round sanitizes its status-reason output at the CP-1 API boundary rather than expanding into CP-4.

## Commit intent

Subject: `fix(term): harden context brief trust boundaries`

Why: reject partial gate metadata, require real bounded operator reasons, protect lane/skip wiring with mutation-sensitive regressions, and close the same reason/free-text trust-boundary class across CP-1/CP-2 surfaces.
