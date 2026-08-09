# Coder handoff — Issue #103 agentic AI co-worker

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/103
- PRD status: approved in issue body.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-103`
- Branch: `prd/a3-prd-agentic-ai-co-worker-103`

## Pre-edit status
- `git status --short --branch`: clean (`## prd/a3-prd-agentic-ai-co-worker-103...origin/main`).
- Pre-existing dirty files: none.
- Memory warning: memory disabled; current PRD/repo/GitHub/verifier evidence wins.

## Scope boundaries
Allowed for current checkpoint:
- `pipeline-diagram/board.html`
- `pipeline-diagram/deploy/*` docs/checks
- co-worker mount/static asset tests under `tests/unit` and `term-control-center/tests`
- Standard coder/verifier run artifacts under this folder

Forbidden:
- No PR creation, merge, deploy, PRD approval, trading, paper/live trading, backtests, public service exposure, secrets handling, raw transcripts, or project-local skill changes.
- No live `ops.evono.me` mutation or smoke check without separate explicit human confirmation.

Validation targets:
- Focused Python deploy/board tests.
- Static asset sync check after local generation.
- Local HTTP asset smoke check.
- Focused term-control static tests and typecheck where dependencies are available.

Stop condition:
- Stop after final verifier bug-check approval or human escalation; do not create PR.

## Verifier checkpoints from PRD
1. Asset/mount checkpoint.
2. Surface checkpoint.
3. Agentic-launch checkpoint.
4. Parallel-lane checkpoint.
4a. Board grouping checkpoint.
5. Authority checkpoint.
6. Grounding checkpoint.
7. Nav UI checkpoint.
8. Regression/security checkpoint.

## Current checkpoint
- Checkpoint 1: Asset/mount integrity readiness — verifier approved revision 1.
- Checkpoint 2: Single conversational surface — verifier approved revision 1.
- Checkpoint 3: Agentic-launch checkpoint — verifier approved revision 2.
- Checkpoint 4: Parallel-lane checkpoint — verifier approved revision 2 after addressing `F103-C4-001`.
- Checkpoint 4a: Board grouping checkpoint — verifier approved revision 2 after addressing `F103-C4A-001`.
- Checkpoint 5: Authority checkpoint — verifier approved revision 1.
- Checkpoint 6: Grounding checkpoint — verifier approved revision 2 after addressing `F103-C6-001`.
- Checkpoint 7: Nav UI checkpoint — verifier approved revision 1.
- Checkpoint 8: Regression/security checkpoint + final bug-check — verifier approved revision 1; bug-check passed.
- Researcher freshness consult completed before checkpoint 1 edits. Summary: existing `coworker-launcher.js` mounts and exports `window.AgentOpsCoworker`; `sync-public-assets.py` tracks page script/style refs; `asset-smoke-check.py` already detects HTML fallback for JS/CSS; safest checkpoint path is cache-busting board ref, regression tests, local smoke, and live smoke docs without deployment.
- Checkpoint 6 researcher consult completed before verifier review. Summary: keep grounding bounded to `coworker_prompt()` and unit tests; reuse `project_context`, generated `completed-data.js`/`wip-data.js`, board/matrix/plan data, memory checkpoint redaction/isolation, and codebase signals; keep summaries short/advisory and never include raw issue bodies, terminal output, or transcripts.
- Checkpoint 7 researcher consult completed before verifier review. Summary: keep nav fix bounded to shared nav panel height/scroll behavior; target `global-nav-ui.js`, mirror Term Control parity in `src/nav.css`, preserve z-index/bottom-sheet positioning, and avoid board layout/body scrolling changes.
- Steward hygiene review completed before final verifier bug-check. Decision: clean; changed-file placement and run artifact placement appropriate; no raw transcript/secrets artifact, generated output, or cleanup required.

## Changes made
- Bumped the board co-worker static asset query from `issue-72-cp1` to `issue-103-cp1` so reviewed deploys invalidate stale/fallback-prone cached references.
- Added Python deploy integrity tests proving:
  - the smoke checker fails when board-referenced `coworker-launcher.js` is served as HTML;
  - public asset sync tracks the queried co-worker asset reference.
- Strengthened co-worker launcher static test coverage for `window.AgentOpsCoworker` export and immediate mount/render call.
- Fixed stale Python board-generation test loader/signature issues so focused board tests run from repo root.
- Updated live deployment instructions to require separate human approval and include post-deploy co-worker mount checks, without performing any live deploy.
- Changed the nav `Chat` button to open `window.AgentOpsCoworker.open()` instead of reopening the legacy selected-PRD Discuss panel.
- Removed the stale `reopenLastDiscuss` default-chat path.
- Renamed the selected PRD action to `💬 Discuss selected` and updated its clear-state copy so retained Discuss behavior is explicit and not the default chat surface.
- Added static regression coverage proving nav Chat is wired to the co-worker and not Discuss.
- Added deterministic co-worker NL intent parsing for `implement the next N PRDs` with preview-only launch plans stored on the co-worker session.
- Preview plans select actionable board PRDs, run the existing sequencing planner, normalize to one PRD per launch lane for per-PRD sessions, and display branch/worktree metadata without writing plan files, mutating GitHub Project fields, or launching agents.
- Confirmed execution now accepts the pending co-worker plan id/session id, writes sequencing/lane outputs, updates each selected PRD's `Working Branch` and `Worktree Path` via existing read-back helper, then calls the existing TCC `/launch` lane execution path.
- The co-worker launcher tracks pending plan ids returned by chat and includes session/pending ids in explicit action payloads.
- Fixed `F103-C3-001` by drift-checking the pending preview against a current issue-state re-read at confirmation time; if branch/worktree metadata differs, execution now fails before plan writes, Project metadata updates, or `/launch`.
- Fixed `F103-C3-002` by extracting co-worker chat session setup and launch-intent response helpers so `coworker_chat()` is back under the KISS function-size limit.
- Added parallel-safety verdict and coordination warnings to the co-worker launch preview.
- Added a confirmation-time safety gate that blocks plan writes, Worktree Path updates, and `/launch` when the current re-read plan is not `safe_parallel`, preventing same-file/conflicting-surface work from being launched in parallel by default.
- Fixed `F103-C4-001` by treating selected in-plan `blocked_by` dependency edges as `sequential_recommended` conflicts so dependent PRDs cannot launch as concurrent lanes by default.
- Added a separate `Parallel Launch` board surface above the existing grid, with Slot A-D cards derived from visible approved `Now` PRDs across product/domain rows.
- Kept the board grid rendering through `renderLane(lane)` and the original lane titles/worktree context so product/domain rows remain the primary portfolio grouping.
- Slot cards show PRD number/title, domain row, branch/worktree context, a parallel-safety verdict, why the candidate is safe, coordination warnings, empty-slot reasons, per-slot launch buttons, and an AI Co-Worker plan entry point.
- Fixed `F103-C4A-001` by making empty slots explain when additional ready PRDs are visible only in already-used domain rows, rather than showing a vague no-visible-candidate reason.
- Added static board regression coverage proving the domain grid remains and the Parallel Launch slot surface is additive, plus a Node-backed focused test for the same-row/one-per-domain empty-slot branch.
- Hardened co-worker execute so `/coworker/execute` requires an existing matching pending plan id, not just a direct execute click against the current lane plan.
- Enforced pending launch plan project matching even when the execute request omits `project_id`, preserving strict project isolation.
- Cleared the pending launch plan after a successful confirmed execute so one preview receives one launch confirmation.
- Updated the launcher to block Execute until a co-worker launch preview exists, and to clear the pending plan id after successful execution.
- Extended Term Control Center's co-worker surface guard to honor `surface: "coworker"` request bodies as well as the `x-agentops-surface` header.
- Added focused authority regression coverage for model-text non-mutation, pending-plan requirements, cross-project rejection, one-confirmation clearing, and TCC mutation-route denial.
- Extended co-worker grounding to include project-scoped codebase signals from the configured checkout (repo/config markers, board assets, Python package, and Term Control surfaces) without invoking new indexing or external services.
- Extended project memory grounding with `codebaseLayer`/isolation metadata and up to three redacted, project-id-filtered checkpoint recall lines from the existing memory checkpoint log.
- Added implemented-versus-planned grounding by summarizing generated completed-work rows, WIP rows, and visible planned board items with existing co-worker sanitization/redaction.
- Added checkpoint 6 tests proving codebase signals appear, cross-project memory is excluded, secret-like memory/board text is redacted, and completed/WIP/planned summaries are present.
- Fixed `F103-C6-001` by making completed/WIP generated data strictly scoped for non-empty `project_id`; missing scoped files now return empty summaries instead of falling back to root generated data, while legacy no-project calls still use root data.
- Made the shared desktop nav panel and mobile More sheet viewport-bounded with vertical scrolling, overscroll containment, and iOS momentum scrolling so all More/Activity/Board-tool entries remain reachable without browser zoom-out.
- Added mobile `positionList()` max-height/overflow settings for auxiliary lists opened from the More sheet.
- Mirrored nav overflow reachability rules in Term Control Center nav CSS for shell parity.
- Extended static nav guardrail tests to assert scrollable viewport-bounded More sheet behavior and no horizontal nav scrolling.

## Changed files
- `src/agentops_harness/review_server.py`
- `pipeline-diagram/board.html`
- `pipeline-diagram/coworker-launcher.js`
- `pipeline-diagram/deploy/INSTALL-ops.md`
- `pipeline-diagram/global-nav-ui.js`
- `term-control-center/server/index.ts`
- `term-control-center/src/nav.css`
- `term-control-center/tests/coworkerGuard.test.ts`
- `term-control-center/tests/coworkerLauncher.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `tests/unit/test_deploy_asset_integrity.py` (new)
- `tests/unit/test_pipeline_board_generation.py`
- `tests/unit/test_review_server_coworker.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-103-agentic-ai-coworker/*`

## Validation
- `python3 -m pytest tests/unit/test_deploy_asset_integrity.py tests/unit/test_pipeline_board_generation.py`
  - Result: `9 passed in 0.04s`.
- `python3 pipeline-diagram/generate.py`
  - Result: generated ignored local data files for asset sync/smoke validation (`9 open PRDs, 0 in progress, 56 completed`).
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check`
  - Initial before generation: failed because ignored generated `*-data.js` sources were absent.
  - After generation: passed.
- Local staging-like smoke:
  - Served `pipeline-diagram` with `python3 -m http.server <ephemeral> --bind 127.0.0.1`.
  - Ran `python3 deploy/asset-smoke-check.py http://127.0.0.1:<ephemeral>/`.
  - Result: passed.
- `npm --prefix term-control-center ci`
  - Result: installed dependencies; no vulnerabilities.
- `npm --prefix term-control-center run typecheck -- --pretty false`
  - Initial before dependency install: failed because React/xterm packages were absent.
  - After `npm ci`: passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/nginxProxy.test.ts`
  - Result: `9` tests passed.
- Checkpoint 2 validation:
  - `python3 -m pytest tests/unit/test_deploy_asset_integrity.py tests/unit/test_pipeline_board_generation.py`
    - Result: `10 passed in 0.05s`.
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/boardGuardrails.test.ts`
    - Result: `39` tests passed.
  - `git diff --check && python3 pipeline-diagram/deploy/sync-public-assets.py --check`
    - Result: passed.
- Checkpoint 3 validation:
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py tests/unit/test_deploy_asset_integrity.py`
    - Initial without `PYTHONPATH=src`: failed to import `agentops_harness`; rerun with `PYTHONPATH=src` passed, `35 passed in 4.70s`.
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_lane_plan.py tests/unit/test_review_server_coworker.py`
    - Result: `39 passed in 4.64s`.
  - `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`
    - Result: `5` tests passed.
  - Attempted broader `tests/server.test.ts` with coworker tests timed out after 180s and showed unrelated existing launch fixture failures around canonical worktree/branch expectations; focused coworker guard/launcher coverage passed.
  - `git diff --check`
    - Result: passed.
- Checkpoint 3 revision 2 validation:
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `40 passed in 4.64s`.
  - `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`
    - Result: `5` tests passed.
  - `git diff --check`
    - Result: passed.
- Checkpoint 4 validation:
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `41 passed in 4.68s`.
- Checkpoint 4 revision 2 validation:
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `42 passed in 4.68s`.
  - `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`
    - Result: `5` tests passed.
  - `git diff --check`
    - Result: passed.
- Checkpoint 4a validation:
  - Revision 1: `PYTHONPATH=src python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `51 passed in 4.65s`.
  - Revision 1: `git diff --check`
    - Result: passed.
  - Revision 1: `python3 pipeline-diagram/deploy/sync-public-assets.py --check`
    - Result: passed.
  - Revision 2: `PYTHONPATH=src python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `52 passed in 4.17s`.
  - Revision 2: `git diff --check`
    - Result: passed.
  - Revision 2: `python3 pipeline-diagram/deploy/sync-public-assets.py --check`
    - Result: passed.
- Checkpoint 5 validation:
  - `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `49 passed in 6.69s`.
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`
    - Result: `6` tests passed.
  - `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - `git diff --check`
    - Result: passed.
  - `python3 pipeline-diagram/deploy/sync-public-assets.py --check`
    - Result: passed.
- Checkpoint 6 validation:
  - Revision 1: `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `51 passed in 6.70s`.
  - Revision 1: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`
    - Result: `6` tests passed.
  - Revision 1: `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - Revision 1: `git diff --check`
    - Result: passed.
  - Revision 2 finding addressed: `F103-C6-001`.
  - Revision 2: `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_lane_plan.py`
    - Result: `52 passed in 6.70s`.
  - Revision 2: `git diff --check`
    - Result: passed.
- Checkpoint 7 validation:
  - `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts tests/termBasePath.test.ts`
    - Result: `63` tests passed.
  - `npm --prefix term-control-center run typecheck -- --pretty false`
    - Result: passed.
  - `git diff --check`
    - Result: passed.
- Checkpoint 8 / final validation:
  - Steward hygiene review over changed-file placement/run artifacts/secrets/generated output
    - Result: clean; no cleanup recommended.
  - `PYTHONPATH=src python3 -m pytest tests/unit`
    - Result: `995 passed, 2 failed` in `tests/unit/test_github_cli_env.py`; failures are pre-existing/unrelated to issue #103 changed files and assert `AGENTOPS_GH_CONFIG_DIR` monkeypatch behavior in `agentops_harness.github_cli_env`, which this PRD did not touch.
  - `npm --prefix term-control-center test`
    - Result: timed out after 300s after existing server launch-fixture failures around direct implementation launch branch/worktree expectations; focused co-worker/nav/security tests passed and this broad server fixture issue was already observed as unrelated during checkpoint 3.
  - `npm --prefix term-control-center run build`
    - Result: passed (`typecheck`, Vite client build, server `tsc`); Vite emitted existing non-blocking chunk-size/script bundling warnings.
  - `git diff --check`
    - Result: passed.

## Risks / notes
- No live deploy or `ops.evono.me` mutation was performed.
- `pipeline-diagram/generate.py` created ignored local generated data files only; they are not in git status.
- `term-control-center/node_modules` was installed locally for validation and is ignored.
- Discuss is retained only as an explicit selected-PRD sub-feature for now; deeper retirement/folding can continue if later verifier or PRD scope requires it.
- Checkpoint 4 adds an initial safe-parallel gate; richer serial-phase UX, grounding, authority hardening, and nav overflow remain for later checkpoints.
- Checkpoint 4a is a local/static board change only; no live deployment or GitHub Project mutation was performed.
- Checkpoint 5 hardened local/server authority gates only; verifier approved revision 1. No live deployment, GitHub Project mutation, agent launch, PR creation, or approved checkpoint 1-4a rework was performed.
- Checkpoint 6 grounding is advisory prompt context only; verifier approved revision 2. It does not run live indexing or mutate memory/codebase state.
- Checkpoint 7 changed nav scroll/height behavior only; verifier approved revision 1. No board layout, body scrolling, route/model, live deploy, or auth changes were made.
- Checkpoint 8 did not add implementation changes beyond handoff/ledger updates; broad validation exceptions are documented as unrelated existing failures.
- Final verifier checkpoint 8 / bug-check approved with 0 findings. Stop before PR as requested; no PR will be created.
