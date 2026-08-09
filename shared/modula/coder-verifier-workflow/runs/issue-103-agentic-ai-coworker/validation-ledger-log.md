# Validation ledger log — Issue #103

## 2026-06-29 — Checkpoint 1 asset/mount integrity
- Scope: co-worker asset reference, deploy smoke coverage, local mount/static checks, live smoke instructions only.
- No live `ops.evono.me` deploy or mutation performed.
- `python3 -m pytest tests/unit/test_deploy_asset_integrity.py tests/unit/test_pipeline_board_generation.py` — passed, 9 tests.
- `python3 pipeline-diagram/generate.py` — generated ignored local data files for asset checks.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed after generation.
- Local HTTP smoke with `python3 deploy/asset-smoke-check.py http://127.0.0.1:<ephemeral>/` — passed.
- `npm --prefix term-control-center ci` — installed ignored local dependencies for validation.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed after dependency install.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/nginxProxy.test.ts` — passed, 9 tests.

## 2026-06-29 — Checkpoint 2 single conversational surface
- Scope: nav Chat opens AI co-worker; legacy Discuss retained only as explicit selected-PRD action.
- `python3 -m pytest tests/unit/test_deploy_asset_integrity.py tests/unit/test_pipeline_board_generation.py` — passed, 10 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/boardGuardrails.test.ts` — passed, 39 tests.
- `git diff --check && python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed.

## 2026-06-29 — Checkpoint 3 agentic launch
- Scope: NL `implement the next N PRDs` preview, pending plan id tracking, explicit execute writes launch metadata and calls existing lane `/launch`.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py tests/unit/test_deploy_asset_integrity.py` — passed after rerun with `PYTHONPATH=src`, 35 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_lane_plan.py tests/unit/test_review_server_coworker.py` — passed, 39 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts` — passed, 5 tests.
- Broader `tests/server.test.ts` attempt timed out after 180s with unrelated existing launch fixture failures; focused coworker/TCC guard coverage passed.
- `git diff --check` — passed.

## 2026-06-29 — Checkpoint 3 revision 2 fixes
- Findings addressed: `F103-C3-001`, `F103-C3-002`.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 40 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts` — passed, 5 tests.
- `git diff --check` — passed.

## 2026-06-29 — Checkpoint 4 parallel-lane safety gate
- Scope: preview exposes parallel-safety verdict; confirmation blocks unsafe/non-`safe_parallel` plans before writes, Worktree Path updates, or `/launch`.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 41 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts` — passed, 5 tests.
- `git diff --check` — passed.
## 2026-06-29 — Checkpoint 4 revision 2 fix
- Finding addressed: `F103-C4-001`.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 42 tests.
- `git diff --check` — passed.

## 2026-06-29 — Checkpoint 4a board grouping
- Scope: preserve product/domain board rows and add a separate Parallel Launch slot surface above the grid.
- Revision 1: `PYTHONPATH=src python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 51 tests.
- Revision 1: `git diff --check` — passed.
- Revision 1: `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed.
- Revision 2 finding addressed: `F103-C4A-001`.
- Revision 2: `PYTHONPATH=src python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 52 tests.
- Revision 2: `git diff --check` — passed.
- Revision 2: `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed.

## 2026-06-29 — Checkpoint 5 authority guardrails
- Scope: model text remains non-mutating; execute requires a matching pending co-worker plan; pending plans are project-bound and one-use; co-worker surface denylist is enforced in Python and Term Control Center.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 49 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts` — passed, 6 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `git diff --check` — passed.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed.
- No live `ops.evono.me` deploy/mutation, GitHub Project mutation, agent launch, PR creation, merge, trading, or backtest performed.
- Verifier decision: checkpoint 5 revision 1 approved with 0 open findings (compact coms verdict; full report not read by coder per workflow).

## 2026-06-29 — Checkpoint 6 grounding
- Researcher consult: reuse `coworker_prompt()`, `project_context`, generated completed/WIP/board/matrix/plan data, and memory checkpoint redaction/isolation; keep codebase grounding as bounded project-scoped signals and summaries, not live indexing.
- Scope: codebase and implemented-versus-planned grounding only; no new mutation route, live indexing, memory write, or raw transcript/terminal artifact.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 51 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts` — passed, 6 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `git diff --check` — passed.
- Revision 2 finding addressed: `F103-C6-001`; non-empty project completed/WIP grounding now uses only matching scoped generated files and does not fall back to root data.
- Revision 2: `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py` — passed, 52 tests.
- Revision 2: `git diff --check` — passed.
- Verifier decision: checkpoint 6 revision 2 approved with 0 open findings (compact coms verdict; full report not read by coder per workflow).
- No live `ops.evono.me` deploy/mutation, GitHub Project mutation, agent launch, PR creation, merge, trading, or backtest performed.

## 2026-06-29 — Checkpoint 7 nav overflow
- Researcher consult: keep scope to shared nav panel height/scroll behavior; target `global-nav-ui.js`, mirror Term Control CSS parity, preserve z-index/bottom-sheet positioning, and avoid page/body/board scroll changes.
- Scope: desktop/mobile More panel reachability and Term Control nav parity only.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts tests/termBasePath.test.ts` — passed, 63 tests.
- `npm --prefix term-control-center run typecheck -- --pretty false` — passed.
- `git diff --check` — passed.
- Verifier decision: checkpoint 7 revision 1 approved with 0 open findings (compact coms verdict; full report not read by coder per workflow).
- No live `ops.evono.me` deploy/mutation, GitHub Project mutation, agent launch, PR creation, merge, trading, or backtest performed.

## 2026-06-29 — Checkpoint 8 regression/security validation
- Steward hygiene review — clean; changed-file placement and run artifacts appropriate; no raw transcript/secrets artifact, generated output, or cleanup required.
- `PYTHONPATH=src python3 -m pytest tests/unit` — `995 passed, 2 failed`; failures are in untouched `tests/unit/test_github_cli_env.py` around `AGENTOPS_GH_CONFIG_DIR` monkeypatch expectations versus `agent_gh_env(source=...)` behavior.
- `npm --prefix term-control-center test` — timed out after 300s after existing direct-launch server fixture failures around branch/worktree expectations; focused issue #103 co-worker/nav/security tests passed, and this broad fixture class was already noted as unrelated earlier in the checkpoint 3 ledger.
- `npm --prefix term-control-center run build` — passed (`typecheck`, Vite client build, server `tsc`); existing non-blocking Vite warnings only.
- `git diff --check` — passed.
- Verifier decision: checkpoint 8 revision 1 approved; final bug-check passed with 0 open findings (compact coms verdict; full report not read by coder per workflow).
- No live `ops.evono.me` deploy/mutation, GitHub Project mutation, agent launch, PR creation, merge, trading, or backtest performed.
