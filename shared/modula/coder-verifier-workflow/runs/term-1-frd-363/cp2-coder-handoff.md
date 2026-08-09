# CP-2 Coder Handoff — Context-Brief end to end

## Source and scope

- Base: `af1ed01`
- Brief: `/tmp/agentops/term1-363/cp2-brief.md`
- Implemented FR-5 through FR-8 only.
- No git operations.
- No deploy, CP-3 sweep/recovery, CP-4 stores, CP-5 forge, CP-6 multi-project, CP-7 wake/renewal, or Kody-path work.

## FR-5 — launch surfaces produce `task.contextBrief`

**Status: implemented.**

### Exact payload contract and project defaults

- `shared/launcher.ts` now exports `validateContextBriefConfig`, backed by the existing canonical `ContextBriefConfig` parser. The action-config path therefore accepts exactly the existing contract rather than a duplicate schema:
  - policies: `auto|required|skip`,
  - all eight existing scopes,
  - all nine existing surfaces,
  - required reason for `skip`.
- `ProjectActionConfig` now carries nested `contextBrief?: ContextBriefConfig`.
- `resolveProjectActionConfig` exposes the config with source evidence.
- The fail-safe omitted-project default is `{ policy: 'required', scope: 'unknown', surfaces: [] }`; `required` routes to the brief regardless of unknown scope.
- `configuredLaunchTask` defaults implementation tasks without overriding a caller-supplied valid config.
- `configuredAuthoringTask` and `/launch-context` expose the selected project default to board/planner surfaces.
- Existing admin saves preserve a previously configured nested Context Brief value even though no new visual control was added.

### Board and coworker launch surfaces

- `pipeline-diagram/board.html` and its deployed light-board counterpart now load `/launch-context` and put `defaults.contextBrief` directly on the implementation task.
- Removed title/label keyword inference. Board tasks no longer fabricate policy/scope/surfaces from text.
- `pipeline-diagram/coworker-launcher.js` loads the same project launch context and carries `contextBrief` on both Execute-plan and Slot-launch requests.
- The authoritative lane task is independently defaulted again inside Term Control before gating, so the Python coworker hop cannot omit or weaken the configured policy.
- No visual layout/style was changed; the prototype-reference visual gate is therefore not applicable.

### Planner handoff surface

- Planning-intake GET responses include the project Context Brief default.
- `pipeline-diagram/planning-intake.js` posts that exact config in the handoff body.
- The handoff route validates the body through the canonical shared parser.
- The durable `handoff-to-authoring` conversation snapshot now contains `task.contextBrief`, and the response echoes the carried config.
- This remains the existing authoring handoff (it does not fabricate an implementation cohort); FR-7 owns the actual brief-to-implementation transition.

### FR-5 regression and exact-wiring evidence

All mutations were scratch-only under `/tmp/agentops/term1-363/revert-checks-cp2/`:

| Guard | Exact production mutation | Result |
|---|---|---|
| Action config canonical parser | Removed `contextBriefField(value.contextBrief)` from `parseActionConfig` | `FR5-action-parse/revert.log`: valid config disappeared and invalid skip no longer threw. |
| Configured implementation default | Replaced the saved-project default expression with raw `task.contextBrief` | `FR5-launch-default/revert.log`: headless launch no longer produced a brief group. |
| Launch-context default | Removed `contextBrief` from `configuredAuthoringTask` | `FR5-launch-context-default/revert.log`: admin/launch-context assertion received `undefined`. |
| Direct launch gate | Replaced only `contextBriefLaunch(configured)` in `launchHandler` with accepted implementation | `FR5-direct-gate/revert.log`: first group was implementation instead of Context Brief. |
| Main board task wiring | Replaced only `contextBrief: defaults.contextBrief` with `undefined` | `FR5-board/revert.log`: surface test failed. |
| Light board task wiring | Same exact mutation in the deployed light-board copy | `FR5-board-light/revert.log`: surface test failed. |
| Coworker launch payload | Replaced only `contextBrief: context.contextBrief` with `undefined` | `FR5-coworker/revert.log`: surface test failed. |
| Planner UI handoff | Replaced the exact JSON body with `{}` | `FR5-intake-ui/revert.log`: surface test failed. |
| Planning GET default | Replaced only the `configuredContextBrief` result with `undefined` | `FR5-intake-view/revert.log`: HTTP response assertion failed. |
| Planning route validation | Replaced only `validateContextBriefConfig(request.body?.contextBrief)` with an accepting raw value | `FR5-intake-validation/revert.log`: missing config incorrectly returned HTTP 200. |
| Durable handoff snapshot | Removed only `task: { contextBrief }` from the snapshot | `FR5-intake-snapshot/revert.log`: persisted snapshot assertion failed. |

## FR-6 — lane launches use the same gate

**Status: implemented.**

- Extracted the existing launch decision into focused `server/contextBriefLaunch.ts` (26 lines).
- Both normal `/launch` requests and each configured lane request call this same function.
- Lane request construction now applies the selected project default before the gate.
- A run decision changes the lane request to `mode: context-brief` with the Sol-profile brief pane; a skip decision carries `contextBriefDecision` into implementation.
- Queued lane placeholders preserve the gated request mode.
- Lane reuse now includes mode identity, preventing an implementation group from masquerading as a reusable brief group.
- Lane capacity semantics remain intact: the Context Brief group occupies the lane until continuation replaces it with implementation.

Regression: `lane launch requests pass through the Context Brief gate` starts a real fake-agent tmux lane and asserts `mode === 'context-brief'`, one Context Brief pane, and the required project default.

Exact mutation: replaced only `contextBriefLaunch(configured)` in `laneLaunchRequest` with the ungated configured request. `FR6-lane-gate/revert.log` failed with actual `implementation` versus expected `context-brief`.

## FR-7 — ready brief continues to implementation roles plus Lead

**Status: implemented and headlessly exercised.**

The pre-existing transition remains the implementation:

1. Direct launch without caller metadata receives project `required` defaults.
2. HTTP `/launch` visibly starts a Context Brief group with one Context Brief pane.
3. A ready brief/state is written with the exact route decision.
4. HTTP `/groups/:id/context-brief/continue` validates the artifact.
5. Phase two starts verifier, coder, researcher, and steward.
6. `startWorkspaceGroup` starts the separate Lead runtime.
7. The Context Brief group is retired only after phase-two success.

`tests/server.test.ts` proves this path through the real HTTP adapters with a real fake-agent process and injected live Lead spawner. It asserts four implementation roles, one Lead start, and brief-group retirement. Unit coverage also asserts the default phase-two role list and brief path.

Exact mutation: replaced only the handler’s `startImplementation: launch => startWorkspaceGroup(launch, context)` callback with a context-brief-shaped stub. `FR7-continue-wiring/revert.log` failed because phase two remained `context-brief`.

The real-deploy/browser dogfood AC-1 remains operator-gated as stated in the brief; no deployment was attempted.

## FR-8 — degraded continuation requires operator reason

**Status: implemented and guarded.**

The existing server transition already rejected degraded continuation unless `reason` was non-empty, and the HTTP adapter trims the operator input. Added a direct regression that calls `continue_without_brief` with an empty reason and proves:

- HTTP-equivalent result status is 400,
- the error identifies the operator-reason requirement,
- phase two is not started.

Exact mutation: removed only the non-empty reason guard. `FR8-operator-reason/revert.log` failed by reaching the forbidden retirement/launch path.

No reason is inferred from route metadata, scope, or prior state.

## Files changed

Production:

- `pipeline-diagram/board.html`
- `pipeline-diagram/public/board-light.html`
- `pipeline-diagram/coworker-launcher.js`
- `pipeline-diagram/planning-intake.js`
- `term-control-center/shared/launcher.ts`
- `term-control-center/server/adminActionConfigClient.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/contextBriefLaunch.ts` (new)
- `term-control-center/server/index.ts`
- `term-control-center/server/laneOrchestrator.ts`
- `term-control-center/server/planningIntakeStore.ts`
- `term-control-center/server/projectActionConfig.ts`

Tests:

- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/contextBrief.test.ts`
- `term-control-center/tests/contextBriefModel.test.ts`
- `term-control-center/tests/contextBriefSurfaces.test.ts` (new)
- `term-control-center/tests/coworkerLauncher.test.ts`
- `term-control-center/tests/laneOrchestrator.test.ts`
- `term-control-center/tests/planningIntakeRoutes.test.ts` (new)
- `term-control-center/tests/planningIntakeStore.test.ts`
- `term-control-center/tests/projectActionConfig.test.ts`
- `term-control-center/tests/server.test.ts`

## Validation

Passed:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm run build`
- Core focused suite: **41/41 passed**.
  - `/tmp/agentops/term1-363/cp2-focused-final.log`
- Headless HTTP brief → continue → implementation+Lead: **1/1 passed**.
  - `/tmp/agentops/term1-363/cp2-e2e-final.log`
- Admin/configured launch-context test: **1/1 passed**.
  - `/tmp/agentops/term1-363/cp2-admin-final.log`
- `node --check pipeline-diagram/coworker-launcher.js`
- `node --check pipeline-diagram/planning-intake.js`
- Fourteen exact-production-wiring scratch mutations all failed their intended regression.
  - `/tmp/agentops/term1-363/revert-checks-cp2/`

Full suite:

- `cd term-control-center && npm test`
- **1401 passed / 11 failed / 1412 total**.
- `/tmp/agentops/term1-363/cp2-full-suite-final.log`
- The 11 failures exactly match the CP-1 approved baseline: four wrapper/coms fixture failures, fix-loop source expectation, Browser-QA missing-target fixture, coworker fingerprint fixture, lane hard-cap ordering expectation, and three sandbox `deny_sandbox_start` failures.

Build log: `/tmp/agentops/term1-363/cp2-build-final.log` (only the existing Vite warnings).

## Deviations and disagreements

None. The deploy/browser dogfood exit criterion was not run because the brief explicitly assigns that operator-gated step to Lead. Planning intake remains an authoring handoff, while carrying the exact future implementation Context Brief policy as required; it does not claim to start an approved implementation before one exists.

## Commit intent

Subject: `feat(term): wire context brief launch gate end to end`

Why: produce project-defaulted Context Brief metadata from board/planner surfaces, gate lane launches through the same decision, and prove ready/degraded continuation behavior through production HTTP wiring.
