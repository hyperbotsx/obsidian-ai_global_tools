# Coder Handoff — PRD #62 Post-Merge Branch and Worktree Teardown and Workspace Tidiness

## Source of truth
- Canonical issue: https://github.com/hyperbotsx/agentops-harness/issues/62
- Current branch: `prd/post-merge-teardown-workspace-tidiness-62`
- Proposed #62 branch from the issue: `prd/post-merge-teardown-workspace-tidiness-62`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneC`

## Pre-edit state
- `git status --short --branch`:
  - `## prd/post-merge-teardown-workspace-tidiness-62`
  - `?? dev-plans/agentops/coder-verifier-workflow/runs/issue-32-project-action-config/`
  - `?? dev-plans/agentops/coder-verifier-workflow/runs/issue-62-post-merge-teardown-workspace-tidiness/`
  - `?? dev-plans/agentops/coder-verifier-workflow/runs/issue-66-merge-sync-closeout-reliability/`
- Pre-existing dirty files are the preserved run-artifact folders above; treat them as out-of-scope unless this PRD explicitly updates its own #62 handoff/artifacts.
- Issue state: open PRD; body says `PRD status: Approved`, `CEO approved: Yes`, `Ready for implementation: Yes`.

## Allowed scope
- `term-control-center/server/`
- `term-control-center/shared/`
- `term-control-center/tests/`
- `pipeline-diagram/board.html`
- `src/agentops_harness/`
- `tests/unit/`
- run artifacts under `dev-plans/agentops/coder-verifier-workflow/runs/issue-62-post-merge-teardown-workspace-tidiness/`

## Forbidden scope
- No PR creation, merge, deploy, approval, or human-gate bypass.
- No teardown before confirmed merge+sync.
- No deletion of `main`, dev-main, or any non-PRD branch.
- No force-removal of worktrees with unknown dirty content.
- No deletion of canonical evidence; archive instead.

## Validation target
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run test`
- `npm --prefix term-control-center run build`
- `PYTHONPATH=src python3 -m pytest tests/unit -q`
- `git diff --check`

## Stop condition
Implement all #62 functional requirements and acceptance criteria, get verifier checkpoint approvals plus final bug-check approval, keep the validation commands green, then pause without opening a PR.

## Verifier checkpoints
1. Teardown action wiring, gating after merge/sync(/closeout), and concurrency guard.
2. Remote branch deletion safety (PRD branch only, post-merge only).
3. Worktree removal composed with kill/session cleanup and dirty-worktree refusal.
4. Local branch deletion safety and idempotency.
5. Artifact archival and retention behavior.
6. Fail-closed reasons, diagnostics, and re-run idempotency.
7. Tests, docs, and manual QA evidence.

## Current checkpoint
- All checkpoints approved.
- Final verifier bug-check approved on revision 2 (`bug_check_status: passed`).
- Stop condition reached: implementation complete, validations green, no PR created.

## Checkpoint 1 changes
- Added completion-state support for `tearing_down` / `teardown_done` and persisted `teardown` results.
- Wired `/completion-actions/teardown` into `term-control-center/server/completionRoutes.ts`.
- Added `term-control-center/server/completionTeardownRoutes.ts` with the teardown concurrency guard and bounded placeholder executor.
- Extracted `term-control-center/server/completionActionSequence.ts` so `completionRoutes.ts` stays back under the 300-line ceiling while the new teardown-era action builder remains shared.
- Updated merged/closeout action builders so teardown appears in sequence and validation queue stays disabled until teardown completes.
- Updated the closeout success notification copy to point operators at teardown instead of implying the item disappears immediately.
- Updated the board action-center UI wiring for the new teardown action and summary text.
- Added focused tests for teardown gating, duplicate-press coalescing, persistence, UI wiring, and the new closeout-to-teardown handoff copy.

## Changed files for checkpoint 1
- `term-control-center/shared/completion.ts`
- `term-control-center/server/completionStore.ts`
- `term-control-center/server/completionLifecycleRoutes.ts`
- `term-control-center/server/completionCloseoutRoutes.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/completionActionSequence.ts`
- `term-control-center/server/completionTeardownRoutes.ts`
- `pipeline-diagram/board.html`
- `term-control-center/tests/completion-routes.test.ts`
- `term-control-center/tests/completion-store.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`

## Validation run for checkpoint 1
- ✅ `npm --prefix term-control-center run typecheck`
- ✅ `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion.test.ts tests/completion-routes.test.ts tests/completion-store.test.ts tests/completion-route-action-config.test.ts tests/boardGuardrails.test.ts`
- ✅ `npm --prefix term-control-center run build`
- ✅ `git diff --check`

## Verifier status
- ✅ Checkpoint 1 approved on revision 2.
- ✅ Checkpoint 2 approved on revision 2.
- ✅ Checkpoint 3 approved on revision 2.
- ✅ Checkpoint 4 approved on revision 1.
- ✅ Checkpoint 5 approved on revision 1.
- ✅ Checkpoint 6 approved on revision 1.
- ✅ Checkpoint 7 approved on revision 2.
- ✅ Final verifier bug-check approved on revision 2.
- ✅ Steward hygiene review returned clean and recommended proceeding to final verifier bug-check.
- Verdict path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-62-post-merge-teardown-workspace-tidiness/verifier-report.md`
- Approved findings addressed: `V62-CHK1-001`, `V62-CHK1-002`, `V62-CHK2-001`, `V62-CHK3-001`, `V62-CHK7-001`, `V62-BUG-001`, `V62-BUG-002`

## Checkpoint 2 changes
- Added `src/agentops_harness/post_merge_teardown.py` with a bounded teardown executor scaffold that already enforces remote-branch safety guards.
- Added `src/agentops_harness/post_merge_teardown_support.py` to keep the teardown logic file under the KISS file-size ceiling while sharing render/path/command helpers.
- Added CLI support for `post-merge-teardown` in `src/agentops_harness/cli.py`.
- Tightened the PR head metadata guard to fail closed when `head.repo.full_name` is missing, and regression-locked missing-head-repo, fork-head, and protected-head refusal cases.
- Added focused unit coverage for merged-state re-checks, protected-branch refusal, fail-closed dirty-worktree blocking, archive preservation, idempotent absent-target handling, and destructive-cwd assertions.

## Changed files for checkpoint 2 so far
- `src/agentops_harness/post_merge_teardown.py`
- `src/agentops_harness/post_merge_teardown_support.py`
- `src/agentops_harness/cli.py`
- `tests/unit/test_post_merge_teardown.py`
- `tests/unit/test_cli.py`

## Validation run for checkpoint 2
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit/test_post_merge_teardown.py tests/unit/test_cli.py -q`
- ✅ `git diff --check -- src/agentops_harness/cli.py tests/unit/test_cli.py src/agentops_harness/post_merge_teardown.py src/agentops_harness/post_merge_teardown_support.py tests/unit/test_post_merge_teardown.py`
- ✅ `python3 -m py_compile src/agentops_harness/post_merge_teardown.py src/agentops_harness/post_merge_teardown_support.py`

## Checkpoint 3 changes (in progress)
- Added `term-control-center/server/completionTeardown.ts` to perform runtime group cleanup, tmux-survival verification, and CLI execution from the configured local-main checkout.
- Updated teardown route/config wiring so the action is disabled when local-main config is missing or project resolution fails.
- Passed the term-control-center state dir through to the teardown CLI for archive-root consistency.
- Added focused term-control-center tests for executor cleanup behavior, tmux fail-closed behavior, and teardown config guardrails.

## Changed files for checkpoint 3 so far
- `term-control-center/server/completionTeardown.ts`
- `term-control-center/server/completionTeardownRoutes.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/completionRouteActionConfig.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/completion-teardown.test.ts`
- `term-control-center/tests/completion-route-action-config.test.ts`
- `term-control-center/tests/completion-routes.test.ts`

## Validation run for checkpoint 3 so far
- ✅ `npm --prefix term-control-center run typecheck`
- ✅ `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion-routes.test.ts tests/completion-route-action-config.test.ts tests/completion-teardown.test.ts tests/completion-store.test.ts tests/boardGuardrails.test.ts`
- ✅ `git diff --check -- term-control-center/server/completionTeardown.ts term-control-center/server/completionTeardownRoutes.ts term-control-center/server/completionRoutes.ts term-control-center/server/completionRouteActionConfig.ts term-control-center/server/index.ts term-control-center/tests/completion-teardown.test.ts term-control-center/tests/completion-route-action-config.test.ts term-control-center/tests/completion-routes.test.ts`

## Checkpoint 4 changes (in progress)
- Expanded `tests/unit/test_post_merge_teardown.py` to cover mismatched-issue branch refusal, protected `dev` refusal, checked-out local-HEAD refusal, and `git branch -d` fallback to `-D` after the merged re-check.

## Changed files for checkpoint 4 so far
- `tests/unit/test_post_merge_teardown.py`

## Validation run for checkpoint 4
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit/test_post_merge_teardown.py tests/unit/test_cli.py -q`

## Checkpoint 5 changes (in progress)
- Added an explicit regression test that the archive destination is populated before any teardown runner command is allowed to execute.

## Changed files for checkpoint 5 so far
- `tests/unit/test_post_merge_teardown.py`

## Validation run for checkpoint 5
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit/test_post_merge_teardown.py tests/unit/test_cli.py -q`

## Checkpoint 6 changes (in progress)
- Added `term-control-center/tests/completion-teardown.test.ts` coverage for blocked CLI diagnostics after cleanup.
- Added `term-control-center/tests/server.test.ts` coverage that the production `/completion-actions/teardown` route runs the configured CLI from local-main cwd and clears the live session group.

## Changed files for checkpoint 6 so far
- `term-control-center/tests/completion-teardown.test.ts`
- `term-control-center/tests/server.test.ts`

## Validation run for checkpoint 6
- ✅ `npm --prefix term-control-center run typecheck`
- ✅ `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion-teardown.test.ts tests/server.test.ts`

## Checkpoint 7 changes (in progress)
- Recorded the operator command example and archive-root behavior directly in this allowed run artifact instead of repo docs.
- Full validation suite now passes end-to-end.

## Changed files for checkpoint 7 so far
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-62-post-merge-teardown-workspace-tidiness/coder-handoff.md`

## Validation run for checkpoint 7
- ✅ `npm --prefix term-control-center run typecheck`
- ✅ `npm --prefix term-control-center run test`
- ✅ `npm --prefix term-control-center run build`
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit -q`
- ✅ `git diff --check`

## Final bug-check fixes in progress
- Fixed the artifact-only happy path by cleaning archived dev-plan artifact paths from the worktree before `git worktree remove`.
- Fixed action-center retry after prior worktree removal by skipping repository-remote verification when the original worktree path is already absent, allowing the CLI's idempotent absent-target handling to run.
- Added a real-git teardown test for an artifact-only linked worktree and a direct executor retry test for the missing-worktree rerun path.

## Validation rerun after final bug-check fixes
- ✅ `npm --prefix term-control-center run typecheck`
- ✅ `npm --prefix term-control-center run test`
- ✅ `npm --prefix term-control-center run build`
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit -q`
- ✅ `git diff --check`

## Operator command example
```bash
agentops-harness post-merge-teardown --issue-number 62 --repo hyperbotsx/agentops-harness --pr https://github.com/hyperbotsx/agentops-harness/pull/62 --branch prd/post-merge-teardown-workspace-tidiness-62 --worktree /path/to/worktrees/agentops-laneC --local-main /path/to/worktrees/agentops-harness --archive-root ~/.local/state/agentops/term-control-center --format json
```

## Archive root note
- Archive destination pattern: `$XDG_STATE_HOME/agentops/term-control-center/teardown-archive/<repo>/issue-<n>/dev-plans/agentops/coder-verifier-workflow/runs/`
- Fallback when `XDG_STATE_HOME` is unset: `~/.local/state/agentops/term-control-center/teardown-archive/...`

## Manual QA evidence
- Production teardown route coverage: `term-control-center/tests/server.test.ts` proves `/completion-actions/teardown` runs the configured CLI from local-main cwd, clears the live group, and leaves completion state at `teardown_done`.
- Executor fail-closed coverage: `term-control-center/tests/completion-teardown.test.ts` proves blocked CLI diagnostics are surfaced after cleanup and that surviving tmux panes block teardown before CLI execution.

## Researcher consult summary
- Keep teardown in plain `git` + `gh`, not Git Town; Git Town's `ship`/`delete` semantics are too opinionated for a bounded teardown executor.
- Use `git worktree remove` for a still-present linked worktree and `git worktree prune` only to clean stale metadata for a worktree that is already missing.
- All destructive worktree commands should run from a different known repo cwd via `git -C <repo> ...`, identify the target by absolute path, and fail closed on main-worktree, locked-worktree, moved-worktree, or broad prune ambiguity.
- For remote branch deletion, prefer explicit merged-state verification plus a second-step ref delete when teardown runs after merge; `gh pr merge --delete-branch --match-head-commit <sha>` is the safest one-shot only when merge and delete happen together.
- Branch-protection/ruleset failures, fork-head differences, and merge-queue timing must surface loudly.
