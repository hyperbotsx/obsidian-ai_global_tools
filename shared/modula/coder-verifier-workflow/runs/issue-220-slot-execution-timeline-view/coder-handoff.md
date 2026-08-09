# Coder handoff — Issue #220 execution timeline view

## Source of truth
- Canonical issue/PRD: https://github.com/hyperbotsx/agentops-harness/issues/220
- Context brief: `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-220-0dfd1ab872de/artifacts/project-context-brief.md`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-220`
- Branch: `prd/slot-execution-timeline-view-220`
- Operator continuation authorization: user authorized bounded peer workflow, checkpoints, ordinary verifier revisions, required researcher consults, and Steward review. Human gates for scope expansion, approval, PR, merge, deploy, trading, and backtests remain required.

## Pre-edit status
- `git status --short --branch`: clean (`## prd/slot-execution-timeline-view-220...origin/main`).
- Pre-existing dirty files: none.
- Direct GitHub issue retrieval was attempted before planning but is blocked by GitHub API rate limiting. This handoff relies on the sourced context brief above and the dated, source-cited Researcher consult below.
- Researcher consult, 2026-07-19: a per-project ordered configuration may select a subset of established `A–D` slots, defaulting to all four; do not implement or claim `E+` capacity without human clarification. Timeline must not copy Board launch/session logic; a small shared bridge is preferred, while a documented guarded Board deep-link remains an additive alternative.

## Scope boundaries
Allowed source surfaces for the approved Timeline feature:
- `pipeline-diagram/` generated model, static Timeline page, shared navigation/freshness integration, public asset symlinks, sync/readme checks.
- `src/agentops_harness/slot_queues.py`, `lane_plan.py`, and focused Python tests for per-project configured slot capacity and project-bound execution-plan data.
- `term-control-center/` project cache promotion, configured lane/launch consumers, shared launch/session bridge if needed, and focused TypeScript tests.
- This run artifact folder only for handoff, requests, reports, and sanitized QA evidence.

Forbidden:
- Board retirement, #215 full freshness/failure-state redesign, direct slot edits, autonomous approval/launch/replan/apply, production auth/deploy/nginx changes, generated runtime data, credentials, raw transcripts, PR creation, merge, deployment, trading, or backtests.

Validation targets:
- Focused deterministic Python timeline/config/generation tests.
- Focused TypeScript lifecycle/cache/nav/launch tests, then required typecheck/test/build when dependencies permit.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check`, asset smoke check, `git diff --check`, verifier final bug-check.

Stop condition:
- Final verifier bug-check approval after required Steward review; otherwise a true human escalation.

## Verifier checkpoints
1. Per-project execution-view configuration and project-bound plan inputs: default/subset A–D config, malformed config fail-closed, non-default lane tests, colliding project issue-number isolation.
2. Generated timeline model: exact queue order, approved-only lane membership, draft/unassigned shelf, blockers, completed trail, root/per-project output tests.
3. Static Timeline and live-state adapter: nav/freshness, only safe same-project live implementation state left of NOW, unavailable-state fallback.
4. Guarded interactions and deploy/static integration: issue/running actions, Start repair revalidation, Replan, cache promotion, accessibility/responsive asset checks.
5. Steward hygiene review, bounded cleanup/recheck, required final verifier bug-check.

## Current checkpoint
- Checkpoint 1 revision 6 was approved by verifier (`01KXWQAE08K7CSR623XJKWKCYY`). Checkpoint 2 revision 4 was approved by verifier with no open findings. Checkpoint 3 revision 5 was approved by verifier with zero open findings; the approved full report was not read. Checkpoint 4 revision 4 was approved with zero open findings; the approved full report was not read. Steward hygiene review completed clean. Final verifier bug-check revision 3 was approved (`bug_check_status: passed`, zero open findings); its approved full report was not read. Stop condition reached.

## Checkpoint 2 approval
- Verifier verdict: approved, checkpoint 2 revision 4, zero open findings, bug check not applicable. Per the transport contract, the approved full report was not read.

## Checkpoint 3 revision 5 verifier finding addressed
- `V220-CP3-007`: generator subprocess tests now set `PYTHONDONTWRITEBYTECODE=1`; removed `pipeline-diagram/__pycache__` and `.ruff_cache`, then reran targeted tests/typecheck/diff and confirmed no ignored cache remains.

## Checkpoint 3 revision 3 verifier findings addressed
- `V220-CP3-003`: exposed the Timeline adapter seam and added behavioral tests for an admitted group with no completion record (Implement) and a rejected live read preserving the generated lane model.
- `V220-CP3-004`: added shared bridge behavioral cases for normal, exited, and recoverable seed groups as well as implementation groups.
- `V220-CP3-005`: executes the shared React navigation model to verify Timeline primary reachability, Matrix More reachability, and Timeline active-key resolution.
- `V220-CP3-008`: grouped Timeline provenance into a context object (four parameters maximum), extracted live-admission/token-retry assertion helpers, and extracted promotion fixture setup; all changed callbacks remain below 20 lines.

## Checkpoint 3 revision 2 verifier findings addressed
- `V220-CP3-001`: Timeline now admits only `running`, healthy, attachable implementation groups whose project ID and repository exactly match generated provenance. Legacy mode requires an empty/`legacy-default` group project ID plus exact repository; missing/foreign project or repository metadata fails closed. `not_started`, error/stale/exited, and non-implementation modes are excluded.
- `V220-CP3-002`: Timeline retains every admitted group by group ID, excludes draft ghosts from NOW, explicitly labels approved-unassigned live work, and renders a visible order-only NOW divider between past/live work and future queue lanes.
- `V220-CP3-003`: the bounded completion-state route now exposes only a computed safe lifecycle stage; Timeline uses it, defaults a missing record to Implement, and renders unknown/error stages as Attention. Focused tests cover the stages, no record, bounded batch IDs, and token retry.
- `V220-CP3-004`: Board and Timeline now share the one token/retry/read bridge; Board preserves its exited seed-draft exclusion.
- `V220-CP3-005`: Matrix remains reachable in More while Timeline is added to primary navigation; the TypeScript key union carries both.
- `V220-CP3-006`: selected-project cache promotion deletes a prior root Timeline file and returns false if selected Timeline data is missing, preventing stale cross-project output.
- `V220-CP3-007`: removed ignored Python/Ruff cache directories; final validation used no-bytecode/no-cache settings and the final artifact check is clean.

## Checkpoint 2 revision 4 verifier finding addressed
- `V220-CP2-005`: moved `DEFAULT_TIMELINE_RETENTION_HOURS` below the import block in `pipeline-diagram/generate.py`, and extracted the timeline-retention parsing assertions in `term-control-center/tests/productPrd.test.ts` so the persistence test callback is under 20 lines.
- Current revision validation: the 36 focused Python timeline/generation tests pass, Ruff `E402` passes for `generate.py`, and `git diff --check` passes.

## Revision 6 verifier findings addressed
- `V220-CP1-007`: the expanded provenance callback is now an 11-line coordinator with small named fixture/assertion helpers (all under 20 lines).
- `V220-CP1-008`: the unmarked legacy exception is allowed only when there is no saved project configuration, the request is omitted/`legacy-default`, and the resolved file is exactly the root `pipeline-diagram/lane-plan.json`. Saved/native configurations reject unmarked root and scoped overrides. Matching marked root overrides succeed, foreign marked roots fail, and unknown explicit IDs remain rejected.
- `V220-CP1-002` and all other prior resolved findings remain resolved. Checkpoint 1 is approved; do not re-open its full verifier report.

## Touched files
- `pipeline-diagram/{README.md,agentops-nav.js,board.html,coworker-launcher.js,freshness.js,generate.py,live-sessions.js,timeline.html,timeline.js,deploy/asset-smoke-check.py,deploy/sync-public-assets.py}` plus managed `public/{live-sessions.js,timeline.html,timeline.js}` symlinks.
- `src/agentops_harness/{lane_plan.py,review_server.py,slot_queues.py}`.
- `tests/unit/{test_deploy_asset_integrity.py,test_pipeline_board_generation.py,test_pipeline_timeline_model.py,test_project_plan_isolation.py,test_review_server_coworker.py,test_slot_queues.py}`.
- `term-control-center/server/{adminAssets.ts,adminCapacityTransition.ts,adminClient.ts,adminConfig.ts,adminHtml.ts,adminPipeline.ts,adminProjects.ts,adminProjectSettingsClient.ts,completionRoutes.ts,laneOrchestrator.ts}` and `src/navigation/navModel.ts`.
- `term-control-center/tests/{admin.test.ts,boardGuardrails.test.ts,completion-route-action-config.test.ts,completion-routes.test.ts,coworkerLauncher.test.ts,heartbeatConfig.test.ts,heartbeatSweep.test.ts,launchMetadataFix.test.ts,launchProjectFallback.test.ts,productPrd.test.ts,projectMemory.test.ts,projectMemoryAdminUx.test.ts,projectMemoryProvider.test.ts,server.test.ts,timelineLiveState.test.ts}`.
- Run artifact only: `dev-plans/agentops/coder-verifier-workflow/runs/issue-220-slot-execution-timeline-view/{coder-handoff.md,verifier-report.md,review-request-r1-checkpoint-1.json,review-request-r1-checkpoint-3.json,review-request-r2-checkpoint-3.json,review-request-r3-checkpoint-3.json}`.

## Implementation summary
- Added typed per-project `executionSlotCount` configuration, defaulting to four established slots and rejecting invalid counts outside 1–4.
- Routed queue normalization, slot planning, launch selection, and lane-plan acceptance through the configured subset of `A–D`; runtime concurrency remains a separately bounded throttle.
- Made execution-plan inputs project-bound under `pipeline-diagram/projects/<projectId>/`, with a matching `projectId`-marked root mirror for current active-root compatibility. Readers refuse a root mirror belonging to another project, preventing issue-number collision leakage.
- Updated generated-board input loading to use the selected project's scoped plan/queues and fail closed to an empty queue rather than a foreign root queue.
- Updated focused tests for configured two-slot behavior, malformed settings, project-bound colliding issue numbers, root-mirror provenance, saved and unsaved unknown explicit projects, exact legacy root-plan compatibility, unmarked native override rejection, matching/foreign root-marker behavior, and deterministic timeline model/output coverage.
- Added the generated read-only timeline model: exact `type:prd` + `status:approved` queues, planner-sequenced needs-approval ghosts and approved-unassigned shelf, assignment-aware cross-slot blockers, sanitized configurable 24-hour completed trail, and root/per-project `timeline-data.js` serialization.
- Added the read-only static Timeline with shared nav and freshness support. It renders landed work, an explicit NOW section, configured queue lanes, blockers, and shelf without dates or duration estimates.
- Added a small shared `live-sessions.js` bridge. It keeps Board’s session predicate/project filter single-sourced and gives Timeline token-guarded `/term/groups` plus bounded `/term/completion-states` reads. Only healthy, attachable, same-project `implementation` groups whose PRD is in generated Timeline data render left of NOW; missing/failed live reads retain the generated model.
- Added Timeline project-cache promotion and managed public symlinks, and focused JavaScript/Python tests for the live-state guard, lifecycle labels, freshness/static wiring, deploy references, and cache promotion.
- Checkpoint 4 uses no duplicate launcher/token/session implementation: the shared live-session bridge creates token-free Board reopen/repair URLs; Board re-fetches the group and rejects foreign-project or unattached sessions. Timeline shows Start/Repair only for generated ready lane heads. Start requires an explicit confirmation and delegates to the existing Co-Worker slot-launch route with the expected issue number; that route revalidates the current queue head, blockers, approval, and launch metadata before launch. A drifted queue head fails closed. Repair opens the existing Board metadata-repair flow, disables generic launch in Timeline repair mode, and requires returning to Timeline Start for revalidation. Replan only opens a prefilled existing Co-Worker preview prompt; it never applies slots or launches work.
- Timeline interaction controls use semantic buttons, descriptive labels, focus-visible styling, a polite live status, narrow-screen single-column cards, and reduced-motion support. No direct slot edit, autonomous launch, approval, PR, merge, deploy, trading, or backtest behavior was added.
- Checkpoint 4 revision 2 addressed `V220-CP4-001` through `V220-CP4-005`: Admin now renders/fills/collects configured slot count and optional Timeline retention so unrelated saves preserve non-default values; lane Replan carries its selected slot into the preview-only prompt; Start awaits and truthfully reports accepted/cancelled/failed outcomes; focused VM/DOM tests verify action rendering, ready-head-only Start, blocked-card non-launchability, confirmed/cancelled outcomes, and Replan delegation; Board repair response handling is split into small helpers and Timeline repair mode still requires returning to Start for queue revalidation.
- Checkpoint 4 revision 3 addressed `V220-CP4-006` and `V220-CP4-007`: extracted Admin project-settings helpers into `adminProjectSettingsClient.ts`, leaving `adminClient.ts` at 294 lines with explicit `adminAssets.ts` ordering; refreshed this handoff’s touched surfaces, acceptance coverage, and Admin status.
- Checkpoint 4 revision 4 reconciles `V220-CP4-007` against the complete cumulative `git diff --name-only` and untracked implementation/test/static inventory; run artifacts are recorded separately.
- Required Steward hygiene review completed clean: changed files match their surfaces, Timeline public assets are managed symlinks, and no generated data, runtime JSON, cache, credential, transcript, or temporary artifact remains. No cleanup was required.
- Final bug-check revision 2 fixes: Timeline blockers now derive only from project-bound `plan_order`, preventing global curated-edge issue-number collisions; capacity reduction rejects a persisted disabled-slot queue before configuration writes; Timeline repair errors preserve the disabled generic Board Start control. Focused regression coverage covers all three paths.
- Final bug-check revision 3 addresses `V220-FINAL-004`: capacity-transition IO/validation moved to `adminCapacityTransition.ts`, leaving `adminProjects.ts` at 299 lines; curated-collision coverage moved to the smaller project-isolation suite, leaving `test_pipeline_timeline_model.py` at 290 lines.

## Acceptance criteria covered
- Default and non-default configured slot counts: covered by Python unit tests and lane execution configuration path.
- Malformed configuration: covered; non-integer/bool/out-of-range values fail closed.
- Project-bound planning inputs and colliding issue-number isolation: covered by writer/reader and generator provenance tests.
- No `E+` support is implemented or claimed; this remains a human clarification gate.
- Timeline serializer/model and root/per-project output: covered by checkpoint-2 tests.
- Timeline UI, safe live overlay, static nav/freshness wiring, cache promotion, public symlinks, guarded session reopening/launch repair, Replan interaction, and focused static/DOM accessibility coverage are covered through checkpoint 4. Real authenticated/live-session browser QA remains a final human-operated non-production check.

## Commands and results
- `gh issue view 220 --repo hyperbotsx/agentops-harness --json number,title,body,url,labels` — blocked: GitHub API rate limit exceeded.
- `git status --short --branch` — initial baseline clean; current expected checkpoint changes recorded above.
- `git rev-parse --show-toplevel && git branch --show-current` — passed; worktree and branch match task.
- Researcher peer request — completed; constraints recorded above.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_slot_queues.py tests/unit/test_lane_plan.py tests/unit/test_project_plan_isolation.py tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py tests/unit/test_review_server_coworker.py` — passed, 146 tests in 12.75s.
- With a temporary, lockfile-identical canonical `node_modules` symlink: `npm run typecheck` from `term-control-center` — passed.
- With the same temporary dependency symlink: `node --test-force-exit --import tsx --test --test-concurrency=1 --test-name-pattern 'lane execution|unsaved lane execution' tests/server.test.ts tests/launchProjectFallback.test.ts` — passed, 6 tests in 8.76s. `--test-force-exit` is required because fixture launch children deliberately keep Node handles open after all assertions complete. The symlink was removed after validation.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_pipeline_timeline_model.py tests/unit/test_pipeline_board_generation.py` — passed, 36 tests in 0.39s.
- Temporary canonical dependency symlink: `node --test-force-exit --import tsx --test --test-name-pattern 'timelineRetentionHours' tests/productPrd.test.ts` — passed, 1 test in the prior checkpoint-2 revision; symlink removed.
- `ruff check --select E402 pipeline-diagram/generate.py` — passed for checkpoint 2 revision 4.
- `git diff --check` — passed for checkpoint 2 revision 4 and checkpoint 3 revision 1.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_pipeline_timeline_model.py tests/unit/test_pipeline_board_generation.py tests/unit/test_deploy_asset_integrity.py` — passed, 39 tests in 0.16s for checkpoint 3 revision 1.
- Temporary canonical dependency symlink: `node --test-force-exit --import tsx --test --test-concurrency=1 tests/timelineLiveState.test.ts tests/completion-routes.test.ts tests/admin.test.ts tests/boardGuardrails.test.ts` — passed, 96 tests in 5.13s for checkpoint 3 revision 2. The symlink was removed after validation.
- Temporary canonical dependency symlink: `npm run typecheck` from `term-control-center` — passed for checkpoint 3 revision 2. The symlink was removed after validation.
- `node --check pipeline-diagram/live-sessions.js && node --check pipeline-diagram/timeline.js` — passed for checkpoint 3 revision 2.
- Temporary canonical dependency symlink: `node --test-force-exit --import tsx --test --test-concurrency=1 tests/timelineLiveState.test.ts tests/admin.test.ts` — passed, 32 tests for checkpoint 3 revisions 3 and 5; `npm run typecheck` also passed. The symlink was removed after validation.
- `python3 pipeline-diagram/deploy/sync-public-assets.py` created managed public symlinks for `timeline.html`, `timeline.js`, and `live-sessions.js`; direct static-link inspection passed.
- Checkpoint 4 focused Python validation: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py tests/unit/test_deploy_asset_integrity.py` — passed, 110 tests in 11.67s.
- Checkpoint 4 JavaScript syntax: `node --check pipeline-diagram/{live-sessions,timeline,coworker-launcher}.js` — passed.
- Checkpoint 4 revision 3 temporary canonical dependency symlink: `npm run typecheck`, then `node --test-force-exit --import tsx --test --test-concurrency=1 tests/admin.test.ts tests/productPrd.test.ts tests/timelineLiveState.test.ts tests/coworkerLauncher.test.ts tests/boardGuardrails.test.ts` — passed, 85 tests in 5.65s. The symlink was removed after validation.
- Checkpoint 4 static asset smoke: served a temporary local staging copy with only throwaway empty generated-data stubs; `python3 pipeline-diagram/deploy/asset-smoke-check.py http://127.0.0.1:18799 --timeout 5` passed. The staging directory, server, log, and generated stubs were removed.
- `git diff --check`, `ruff check --select E402 pipeline-diagram/generate.py`, and cache removal checks — passed. A full Ruff run is pre-existingly blocked by unused `apply_answers` in `src/agentops_harness/review_server.py`; no checkpoint-4 lint issue was reported.

## Skipped checks
- Broader TypeScript test/build checks remain unrun because `term-control-center/node_modules` is absent from this worktree. A temporary lockfile-identical canonical dependency link was used for the focused tests and typecheck, then removed.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` cannot fully pass in this clean source worktree because generated runtime data files (`board-data.js`, `completed-data.js`, `matrix-data.js`, `pipeline-data.js`, `timeline-data.js`, and `wip-data.js`) are intentionally absent and forbidden to commit. Its only reported failures are those missing generated sources; the new static public symlinks exist and resolve correctly.
- Human-operated browser QA against a real applied plan/live session remains unavailable in this non-production run. The bounded local static smoke used throwaway generated-data stubs; responsive/accessibility behavior now has focused source, VM, and deterministic DOM action coverage but not a real authenticated Term session. Two isolated Google Chrome headless preflight attempts (including a disposable profile) crashed with `Trace/breakpoint trap` before page execution; every temporary staging directory, server, log, profile, and core candidate was removed. This is an environment limitation, not a positive viewport receipt.

## Known risks and cleanup
- `E+` capacity/range naming is unresolved and requires human clarification before support or an FR-2-complete claim.
- The GitHub API rate limit prevents direct PRD body retrieval in this environment; the source-cited context brief (re-read during revision 3) and Researcher result are the available evidence.
- Checkpoint 4 uses the shared safe Term read bridge and existing Board/Co-Worker flows; no launcher duplication was introduced. Remaining real-session browser QA requires a human-operated non-production environment.
- The Admin UI now preserves the configured slot count and optional Timeline retention through unrelated project saves; it remains bounded to established A–D capacity.
- Cleanup: no generated data, caches, secrets, raw transcripts, or public-file copies have been created. Managed public symlinks are the only new public assets.

## Bounded standards exceptions
- None. The unavailable direct PRD API and absent worktree JavaScript dependencies are environment limitations, not standards exceptions; implementation remains bounded by the sourced context brief and Researcher result.
