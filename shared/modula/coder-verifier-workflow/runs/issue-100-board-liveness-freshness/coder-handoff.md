# Issue #100 coder handoff

## Scope / source
- PRD: GitHub issue #100, `B2-PRD: Board liveness & freshness — current-on-load, auto-refresh, manual refresh, staleness indicator`.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`.
- Branch: `feat/board-liveness-freshness-100`.
- Pre-existing dirty files: none (`git status --short --branch` was clean before edits).
- Memory note from launch: memory disabled/advisory only; PRD/repo/verifier evidence are authoritative.

## Allowed / forbidden scope confirmed
- Allowed: `pipeline-diagram/generate.py`, generated-view static HTML/assets, `global-nav.js` / `review-notify.js` reconciliation, small shared freshness JS/CSS under pipeline assets, thin authenticated #99 queue wrapper, focused tests/docs.
- Forbidden: parallel regeneration queue, direct browser `generate.py` execution, #99 lifecycle semantics rewrite, cached project-promotion slowdown/removal, project dropdown/search layout rework, GitHub mutation behavior, deployment, PR creation, merge, production rollout.
- Stop condition: final verifier implementation + bug-check approval, or human escalation.

## Verifier checkpoints from PRD
1. Contract checkpoint: #100 consumes #99 queue/status and does not add parallel generation.
2. Freshness module checkpoint: age formatting, stale thresholds, state transitions, cache-busted timestamp checks, reload-loop guard.
3. Auto-refresh checkpoint: left-open views detect newer generated timestamp and auto-refresh for general changes.
4. Manual refresh checkpoint: Refresh now queues through #99, debounces, polls, reloads on newer timestamp, handles failure/timeout.
5. Recent-work preservation checkpoint: cached project promotion, project-switch loading/error behavior, dropdown/search layout stay intact.
6. All-views/reconciliation checkpoint: Board/WIP/Pipeline share mechanism; old duplicate reload toast removed/delegated.
7. Final validation checkpoint: tests, generated outputs, bug-check, production-only smoke notes.

## Implementation summary
- Added `pipeline-diagram/freshness.js`, a shared Board/WIP/Pipeline liveness layer that:
  - displays `updated X ago` immediately from page-specific generated timestamp;
  - injects a compact freshness control and `Refresh now` button;
  - performs cache-busted/no-store generated data checks on load and every 30 seconds;
  - updates visible age at least once per minute;
  - marks stale after 5 minutes and critical after 15 minutes;
  - auto-queues critical stale refresh via the #99 queue/status path when authenticated;
  - reloads only for strictly newer generated timestamps or active-project mismatch, with `sessionStorage` reload-loop guards;
  - debounces overlapping browser refresh attempts while queued/running;
  - polls #99 refresh status and surfaces queued/running/success/failure/timeout/unchanged states.
- Included `freshness.js` on `board.html`, `wip.html`, and `pipeline.html`; added `pipeline-diagram/public/freshness.js` symlink via the existing asset sync script.
- Added thin authenticated/CSRF-protected server wrapper: `POST /api/admin/pipeline-refresh/:projectId`.
  - It reuses `queuePipelineRefresh(runtime.settings.file, activeProjectId, reason)`.
  - It is limited to the active project from `projectSelection(...)` and returns the same sanitized public status.
  - It does not spawn `generate.py` directly and does not add a second queue.
- Retired the old approval-specific board-version reload toast from `review-notify.js`; review/completion notifications remain there, snapshot freshness moved to `freshness.js`.
- Changed generator timestamp precision to seconds (`%Y-%m-%d %H:%M:%S`) so manual refreshes can observe a strictly newer timestamp promptly.
- Updated `pipeline-diagram/README.md` to document `freshness.js` ownership and the removal of approval-specific reload toast semantics.
- Hardened existing generator unit helpers against ambient `AGENTOPS_PROJECT_ID` in the test process.

## Changed files
- `pipeline-diagram/freshness.js` (new)
- `pipeline-diagram/public/freshness.js` (new symlink)
- `pipeline-diagram/board.html`
- `pipeline-diagram/wip.html`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/review-notify.js`
- `pipeline-diagram/generate.py`
- `pipeline-diagram/README.md`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/tests/admin.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/review-request-r1-implementation.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/review-request-r2-f100-r1-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/review-request-r3-final-bug-check.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/review-request-r4-final-bug-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/steward-request-r1-final-hygiene.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/steward-request-r2-cleanup-recheck.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-100-board-liveness-freshness/verifier-report.md`

## Validation so far
- `node --check pipeline-diagram/freshness.js && node --check pipeline-diagram/review-notify.js && python3 -m py_compile pipeline-diagram/generate.py` — passed.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/admin.test.ts` — passed (25/25).
- `cd term-control-center && npm run typecheck` — passed.
- `git diff --check` — passed.
- Attempted `cd term-control-center && npm test -- --test-name-pattern "freshness|manual pipeline refresh endpoint"`; Node test runner executed broader suites and timed out after 120s with pre-existing/unrelated server/tmux/planning test failures. Targeted `tests/admin.test.ts` passed after that.
- After F100-R1-001 fix: `node --check pipeline-diagram/freshness.js` — passed.
- After F100-R1-001 fix: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/admin.test.ts` — passed (25/25).
- After F100-R1-001 fix: `cd term-control-center && npm run typecheck` — passed.
- After F100-R1-001 fix: `python3 pipeline-diagram/deploy/sync-public-assets.py --check && git diff --check` — passed.
- Final validation: `pytest -q tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py` — passed (6/6).
- Final validation: `cd term-control-center && npm run build` — passed; Vite emitted existing non-module script and chunk-size warnings.
- After BUG100-R3 fixes: `node --check pipeline-diagram/freshness.js && python3 -m py_compile pipeline-diagram/generate.py` — passed.
- After BUG100-R3 fixes: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/admin.test.ts` — passed (26/26).
- After BUG100-R3 fixes: `cd term-control-center && npm run typecheck` — passed.
- After BUG100-R3 fixes: `pytest -q tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py` — passed (6/6).
- After BUG100-R3 fixes: `cd term-control-center && npm run build` — passed; Vite emitted existing non-module script and chunk-size warnings.
- After BUG100-R3 fixes: `python3 pipeline-diagram/deploy/sync-public-assets.py --check && git diff --check` — passed.

## Verifier finding fixes
- `F100-R1-001`: `freshness.js` now preserves the visible snapshot project id from `window.PIPELINE_PROJECT_ID` before updating `window.AGENTOPS_ACTIVE_PROJECT_ID`; active-project mismatch reload compares active selection against that visible id. Added focused test coverage for visible project mismatch even when the nav override already differs.
- `BUG100-R3-001`: critical-stale auto-refresh no longer latches `criticalQueued` until a CSRF-backed queue attempt can start; `bootstrapProject(...)` triggers another freshness check after auth/project selection resolves so stale-on-load recovery queues even when the first data check wins the auth race. Added VM coverage for delayed auth bootstrap.
- `BUG100-R3-002`: generated timestamps are now timezone-aware UTC ISO-8601 strings, and `parseTimestamp(...)` treats timezone-bearing values as absolute instants before falling back to local parsing for legacy timestamps. Added ISO age/parse coverage.

## Steward review
- Steward initially requested cleanup:
  - `HYG-100-001`: deleted ignored cache artifacts `.pytest_cache/`, `pipeline-diagram/__pycache__/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/`.
  - `HYG-100-002`: added `verifier-report.md` to the evidence/changed-file list for the run folder.
- Steward cleanup recheck: `CLEAN`.

## Verifier status
- Implementation checkpoints 1-6 approved at revision 2 after `F100-R1-001` fix.
- Final bug-check revision 3 requested fixes for `BUG100-R3-001` and `BUG100-R3-002`; fixes implemented.
- Final bug-check revision 4 approved with `bug_check_status=passed`.

## Notes / risks
- The freshness module is intentionally fail-closed: stale static snapshots remain visible if checks or queue calls fail.
- Manual refresh requires an authenticated admin session and CSRF token from `/api/admin/session`; unauthenticated pages show a sign-in-required state for refresh actions.
- Project switch remains owned by `global-nav.js` and `PUT /api/admin/project-selection`; no project-switch wait-for-generation path was added.
- Production smoke remains human/deploy-gated per PRD: verify visual placement on ops.evono.me desktop/mobile and controlled failure/timeout state.
