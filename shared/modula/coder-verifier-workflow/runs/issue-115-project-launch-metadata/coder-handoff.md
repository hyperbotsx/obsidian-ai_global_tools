# Coder handoff — Issue #115 project launch metadata

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/115
- PRD status: approved in issue body.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-115`
- Branch: `prd/create-prd-project-launch-metadata-115`

## Pre-edit status
- `git status --short --branch`: clean (`## prd/create-prd-project-launch-metadata-115...origin/main`).
- Pre-existing dirty files: none.
- Researcher freshness consult: not sent because no `researcher` peer is live in this coms pool; implementation is grounded in existing repo code/tests.

## Scope boundaries
Allowed paths from PRD:
- AgentOps Harness app, PRD Studio, terminal creation, launch/remediation, and tests for launch metadata/project placement/freshness/regeneration.
- Repo-owned helper functions, command contracts, and docs for metadata normalization/audit/repair.

Forbidden:
- No PR creation, merge, deploy, backtest, trading, autonomous PRD approval, human-gate bypass, or global Pi/hyper-pi skill mutation.

Validation targets
- Focused Python unit tests around PRD creation / PRD authoring.
- Focused TypeScript tests around launch metadata fix, launch contract, and implementation worktree sync.
- Broader package tests only if affected surfaces require it.

Stop condition
- Stop after final verifier bug-check approval or human escalation; do not create PR.

## Verifier checkpoints
1. Creation placement checkpoint: approved revision 2.
2. Project field checkpoint: approved revision 1.
3. Normalization checkpoint: approved revision 2.
4. Setup/repair checkpoint: approved revision 2.
5. Branch freshness checkpoint: approved revision 1.
6. #99 integration checkpoint: approved revision 1.
7. Final validation checkpoint: approved revision 2; final bug-check passed.
8. Human-requested worktree provisioning follow-up: approved revision 1; final bug-check passed.

## Current checkpoint
- Checkpoint 6 approved by verifier.
- Steward review completed with cleanup recommended for generated caches only.
- Final bug-check revision 1 found `F115-FINAL-001`; bounded fix applied.
- Final verifier bug-check revision 2 approved with zero open findings.
- Human requested a follow-up fix so launch can produce PRD worktrees/branches from PRD metadata; bounded fix applied and verifier-approved.
- Removed `.pytest_cache/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/` after validation.

## Changes made
### Checkpoints 1-2
- Added `src/agentops_harness/prd_launch_metadata.py` with `LaunchMetadata`, canonical PRD branch/worktree helpers, placeholder helpers, body normalization, and body read-back matching.
- Updated PRD author rendering to emit exact `Worktree` label with `agentops-prd-<issue>` placeholder instead of legacy `Worktree/code home`.
- Updated GitHub PRD issue planning to use the same branch helper as final create stamping and to propose canonical per-PRD `Worktree Path` values.
- Threaded selected active Project `worktrees_root` from `review_server.py` into PRD plan, digest, and create flows so selected Project root wins over profile defaults.
- Updated `create_prd_issue` to add Project placement, exact launch metadata body stamping, issue-body read-back, Project field writes/read-back, and fail-closed `PrdCreateError` behavior after issue creation if metadata setup fails.
- Added `set_launch_metadata_fields` with Project field read-back verification in `ceo_review_evonome_apply.py`.

### Checkpoint 3
- Updated `term-control-center/server/launchMetadataFix.ts` so the board auto-fix path normalizes legacy body labels (`Worktree/code home`, `Working branch`, etc.) into exact `Worktree` and `Proposed working branch` lines.
- Changed launch metadata fix target derivation to canonical `prd/<slug>-<issue>` branch and `<worktreesRoot>/agentops-prd-<issue>` path instead of preserving legacy/non-`prd/` branch or lane worktree body values.
- Made auto-fix write the normalized issue body before Project field updates, then require Project field read-back to match target metadata exactly.
- Updated `term-control-center/tests/launchMetadataFix.test.ts` expectations to cover legacy-label removal and canonical body/Project field targets.
- Fixed `F115-R3-001` by making TypeScript and Python Project item lookup repository-aware so duplicate issue numbers from other repositories in the same Project are not mutated/read back.

### Checkpoint 4
- Added `ProjectFieldSetupRequest` planning/execution support in `src/agentops_harness/prd_worktree_project.py` for the two required launch metadata Project fields.
- Added explicit setup confirmation phrase `create launch metadata fields`; execution blocks without this confirmation.
- Planned setup commands use `gh project field-create <project> --owner <owner> --name <field> --data-type TEXT` for `Working Branch` and `Worktree Path` only when missing.
- Added CLI route `agentops-harness prd-worktree project-field-setup` with plan/execute, confirmation, existing-field inputs, and markdown/json output.
- Added tests for planning missing fields, blocking unconfirmed execution, executing after explicit confirmation, and failing when schema read-back still misses a required field.
- Fixed `F115-R4-001` by adding post-setup schema read-back via `gh project field-list <project> --owner <owner> --format json`; setup reports `executed` only when both required fields are present after setup.

### Checkpoint 5
- Updated `term-control-center/server/implementationWorktreeSync.ts` to explicitly require the implementation worktree basename to be `agentops-prd-<issueNumber>` before freshness sync.
- Existing launch validation already requires implementation branches to start `prd/` and end with the PRD issue number; sync still verifies the current worktree branch matches the recorded branch and blocks dirty/conflicting branches before agents start.
- Added push of refreshed stale-clean PRD branches after merging latest `origin/main` using `git push origin HEAD:<branch>`.
- Updated `term-control-center/tests/implementationWorktreeSync.test.ts` fixture paths to dedicated PRD worktrees and added assertion that stale-clean sync pushes the refreshed branch to origin.

### Checkpoint 6
- Added authenticated term-control `POST /pipeline-refresh/:projectId` route that calls the #99 shared `queuePipelineRefresh()` trigger with the selected project and reason.
- Changed PRD create completion in `review_server.prd_create_action()` to call `queue_shared_board_refresh()` instead of the legacy direct `refresh_board_async()` path.
- `queue_shared_board_refresh()` calls the term-control shared trigger without the coworker surface header and reports `{ok:false, blocked:true}` if the #99 trigger is unavailable, rather than running a local duplicate generation path.
- Added focused Python test proving PRD create refresh uses `/pipeline-refresh/<projectId>` with reason `prd-create-launch-metadata`.

### Final bug-check fix
- Fixed `F115-FINAL-001` by changing CEO approval Project writes to set `Worktree Path` to the canonical dedicated PRD worktree path `<worktrees_root>/agentops-prd-<issue>` instead of legacy owner-mapped worktrees.
- Added regression coverage proving `_resolve_project_writes()` preserves the canonical PRD worktree path for owner approval flows.

### Human-requested worktree provisioning follow-up
- Updated `term-control-center/server/worktreeProvision.ts` so deterministic PRD worktree provisioning uses `<worktreesRoot>/agentops-prd-<issue>` instead of branch-derived paths.
- Provisioning now rejects launch metadata whose requested worktree path does not match the canonical `agentops-prd-<issue>` path.
- Direct implementation launch now calls provisioning before pane/browser startup when the recorded canonical worktree is missing, using the selected Project local checkout, worktrees root, recorded branch, and issue number.
- Lane orchestration active-group lookup now uses the same canonical worktree helper, keeping lane provisioning/reuse aligned with #115 metadata.
- Added focused worktree provisioning tests for canonical path reuse and non-canonical path rejection.

## Revision 1 verifier findings addressed
- `F115-R1-001`: unified draft plan, rendered body placeholder, final body, and Project field branch naming through `LaunchMetadata`/`branch_name`.
- `F115-R1-002`: added issue-body read-back via `gh issue view --json body` and exact metadata line checks.
- `F115-R1-003`: threaded active Project `worktrees_root` into plan/create/digest paths and added focused tests.
- `F115-R1-004`: replaced 5-parameter new helper interfaces with a `LaunchMetadata` value object and 2-parameter helper calls.
- `F115-R3-001`: repository-aware Project item lookup added in `launchMetadataFix.ts` and `ceo_review_evonome_apply.py`; focused tests prove duplicate issue numbers select the configured repository item.
- `F115-R4-001`: setup execution now reads back Project schema and returns partial failure if required fields are still missing.
- `F115-FINAL-001`: approval-time Project `Worktree Path` writes now use canonical per-PRD worktree paths so approval cannot make launch metadata non-launchable.

## Changed files
- `src/agentops_harness/prd_launch_metadata.py` (new)
- `src/agentops_harness/prd_author_render.py`
- `src/agentops_harness/prd_author_github.py`
- `src/agentops_harness/prd_create.py`
- `src/agentops_harness/ceo_review_evonome_apply.py`
- `src/agentops_harness/review_server.py`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchMetadataFix.ts`
- `term-control-center/tests/launchMetadataFix.test.ts`
- `term-control-center/server/implementationWorktreeSync.ts`
- `term-control-center/server/laneOrchestrator.ts`
- `term-control-center/server/worktreeProvision.ts`
- `term-control-center/tests/implementationWorktreeSync.test.ts`
- `term-control-center/tests/worktreeProvision.test.ts`
- `src/agentops_harness/prd_worktree_project.py`
- `src/agentops_harness/cli.py`
- `tests/unit/test_prd_worktree_project.py`
- `tests/unit/test_prd_create.py`
- `tests/unit/test_prd_author_github.py`
- `tests/unit/test_ceo_review_evonome_apply.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-115-project-launch-metadata/*`

## Validation
- Initial attempted Python command failed because `PYTHONPATH` was not set:
  - `pytest -q tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py`
  - Result: import errors for `agentops_harness`.
- Python focused validation:
  - `PYTHONPATH=src pytest -q tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_ceo_review_evonome_apply.py`
  - Pre-`F115-R3-001` result: `46 passed in 0.22s`.
  - After repository-aware lookup fix: `47 passed in 0.22s`.
  - Checkpoint 4 initial result including `test_prd_worktree_project.py`: `57 passed in 0.24s`.
  - Latest checkpoint 4 revision-2 result: `58 passed in 0.23s`.
- TypeScript focused validation:
  - `cd term-control-center && npm test -- tests/launchMetadataFix.test.ts`
  - Result: failed before executing tests because `term-control-center/node_modules` is absent and Node cannot import package `tsx`. The package script also expands to all tests.
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts`
  - Result: `37 passed` using PATH-resolved `tsx` from the canonical checkout and an isolated temp dir.
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/implementationWorktreeSync.test.ts tests/launcher.test.ts`
  - Result: `39 passed`.
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts`
  - Result: `76 passed`.
- Combined Python validation after checkpoint 6:
  - `PYTHONPATH=src pytest -q tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_prd_worktree_project.py tests/unit/test_review_server_coworker.py`
  - Result: `78 passed in 3.30s`.
- Final validation after Steward cleanup:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q -p no:cacheprovider tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_prd_worktree_project.py tests/unit/test_review_server_coworker.py`
  - Result: `78 passed in 3.97s`.
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts`
  - Result: `76 passed`.
  - `git diff --check`
  - Result: passed.
- Final bug-check revision 2 validation:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q -p no:cacheprovider tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_prd_worktree_project.py tests/unit/test_review_server_coworker.py`
  - Result: `79 passed in 3.94s`.
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts`
  - Result: `76 passed`.
  - `git diff --check`
  - Result: passed.
- Worktree provisioning follow-up validation:
  - `cd term-control-center && TMPDIR=<temp> tsx --test tests/worktreeProvision.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts`
  - Result: `81 passed`.
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q -p no:cacheprovider tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_prd_worktree_project.py tests/unit/test_review_server_coworker.py`
  - Result: `79 passed in 3.94s`.
  - `git diff --check`
  - Result: passed.

## Risks / notes
- `npm test` remains blocked in this worktree until `term-control-center/node_modules` is installed/restored; focused TS tests were executed with PATH-resolved `tsx`.
- `git diff --check`: passed.
- Steward review response is recorded at `dev-plans/agentops/coder-verifier-workflow/runs/issue-115-project-launch-metadata/steward-response-r1.md`.
- Generated cache cleanup was completed and a follow-up `find` confirmed `.pytest_cache/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/` are absent.
- No PRD approval, PR creation, merge, deploy, trading, or backtest actions were run.
