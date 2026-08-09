# Issue #99 coder handoff

## Scope / source
- PRD: GitHub issue #99, `B1-PRD: Admin 'Open'→'Edit' relabel + board regen triggers`.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`.
- Branch: `feat/board-regen-triggers-99` from `origin/main`.
- Preflight: `git fetch origin --prune`; #83 branch HEAD is an ancestor of `origin/main`; tree was clean before switching/resetting.

## Checkpoints
1. Admin label: project-list button now says `Edit`; existing `data-open-project`/`openProject` behavior remains unchanged.
2. Queue: `adminPipeline.ts` adds an in-memory debounced per-project async queue around `generate.py` with no overlapping same-project runs.
3. Project switch: active project selection queues regeneration and returns queue status instead of blocking on `generate.py`.
4. Lifecycle triggers: completion prepare-PR, merge-main, PRD closeout, and terminal lifecycle actions call the shared trigger after successful board-visible mutations/state transitions.
5. Final validation pending full `npm test`/build after verifier checkpoints.

## Queue/status contract for #100
- Trigger helper: `queuePipelineRefresh(settingsFile, projectId, reason)`.
- Status helpers: `pipelineRefreshStatus(projectId)`, `pipelineRefreshStatuses()`.
- Admin API:
  - `GET /api/admin/pipeline-refresh` -> `{ statuses: PipelineRefreshStatus[] }`
  - `GET /api/admin/pipeline-refresh/:projectId` -> `{ status: PipelineRefreshStatus }`
- Mutating responses that queue refresh include `pipelineRefresh`.
- `PipelineRefreshStatus` fields: `projectId`, `state`, `reason`, `detail`, `queuedAt?`, `startedAt?`, `finishedAt?`, `updatedAt`, `pending`, `results`.
- States: `queued`, `running`, `success`, `failed`, `timeout`, `skipped`.
- Result details are truncated/sanitized; no command env/secrets/raw transcript is exposed.

## Changed files
- `term-control-center/server/adminClient.ts`
- `term-control-center/server/adminPipeline.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/completionCloseoutRoutes.ts`
- `term-control-center/server/completionLifecycleRoutes.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/completion-routes.test.ts`

## Implementation summary
- Replaced the admin list label `Open` with `Edit` only.
- Added async queue with debounce, project-keyed status, timeout handling, disabled/skipped support, sanitized detail output, and existing synchronous `refreshPipelineData` retained for direct maintenance/test callers.
- Changed admin active project switch and settings save to enqueue regeneration with per-project `AGENTOPS_PROJECT_ID` instead of synchronous generation.
- Added authenticated status endpoints for admin callers/client freshness follow-up #100.
- Passed a pipeline refresh trigger into completion routes; successful prepare-PR, merge-main, PRD closeout, and lifecycle transitions queue project regeneration using `task.projectId || legacy-default`.
- Did not edit Lane A planner/gate files.

## Validation so far
- `cd term-control-center && npm test -- --test-name-pattern "admin static assets|pipeline refresh queue|active project selection|completion board-visible lifecycle"` — passed (the runner executed the full suite: 437 pass, 0 fail).
- `cd term-control-center && npm run typecheck` — passed.
- After verifier R1 fixes: `cd term-control-center && npm run typecheck && npm test -- --test-name-pattern "pipeline refresh queue|completion board-visible lifecycle|merge-main resumes|teardown action coalesces|prd-closeout supports safe retry"` — passed (runner executed full suite: 437 pass, 0 fail).
- Final: `cd term-control-center && npm run typecheck && npm test && npm run build` — passed; build emitted existing Vite warnings for non-module scripts/chunk size.
- Bug-fix validation: `cd term-control-center && npm run typecheck && npm test -- --test-name-pattern "pipeline refresh queue"` — passed (runner executed full suite: 437 pass, 0 fail).
- V99-FINAL-003 validation: `cd term-control-center && npm run typecheck && npm test -- --test-name-pattern "pipeline refresh queue records timeout"` — passed (runner executed full suite: 437 pass, 0 fail); no lingering `generate.py` processes found.
- Post-final-fix build: `cd term-control-center && npm run build` — passed; build emitted existing Vite warnings for non-module scripts/chunk size.
- `git diff --check` — passed.

## Verifier finding fixes
- `V99-R1-001`: broadened `sanitizeDetail` to redact common secret key/value, bearer token, `sk-*`, GitHub token, and URL credential forms; added queue regression assertions for `OPENAI_API_KEY`/bearer output.
- `V99-R1-002`: refactored completion route trigger plumbing through a `CompletionActionContext` instead of widening handler/action signatures; changed `completion-routes.test.ts` helper to use an overrides object for optional behaviors including `pipelineRefresh`.

## Final bug-check finding fixes
- `V99-FINAL-001`: async timeout now resolves status when the timer fires, regardless of cooperative child exit, and schedules SIGKILL cleanup after a configurable grace period. Regression uses a SIGTERM-ignoring generator.
- `V99-FINAL-002`: redaction now handles quoted key/value secret forms (for example `token:"..."`) and the queue regression asserts quoted secrets are not exposed.
- `V99-FINAL-003`: timeout status is exposed promptly via the queue entry while the same-project run remains internally busy until the child exits/SIGKILL cleanup completes; regression asserts an immediate same-project retry does not start a second generator during kill grace.

## Steward review
- Steward decision: clean. Changed files are scoped to expected server/admin/completion/test surfaces; issue #99 run artifacts are correctly placed and contain no logs/caches/raw transcripts/secrets.

## Verifier status
- Checkpoints 1-4 approved at revision 2.
- Final bug-check passed at revision 5.

## Unresolved risks / notes
- PRD Studio create/status routes appear to overlap with Lane A-owned planner route internals; I avoided those surfaces. The shared `queuePipelineRefresh` helper is available for #115/create-flow to call after project writes succeed.
- Queue state is in-memory by design and starts empty after process restart per PRD rollback guidance.
