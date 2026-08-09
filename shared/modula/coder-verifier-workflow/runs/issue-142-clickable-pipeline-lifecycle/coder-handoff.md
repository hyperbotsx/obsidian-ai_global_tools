# Coder Handoff — Issue #142 Clickable Pipeline Lifecycle

## Source of truth
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/142
- PR: https://github.com/hyperbotsx/agentops-harness/pull/178
- Branch: `prd/b7-prd-clickable-implementation-pipeline-lifecycle-142`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-142`
- PRD status: Approved; CEO approved.

## Pre-edit state
- `git status --short --branch`: clean, `## prd/b7-prd-clickable-implementation-pipeline-lifecycle-142...origin/main`
- Pre-existing dirty files: none.
- Research-first surfaces: none named in PRD.

## Scope
Allowed paths for this implementation:
- `pipeline-diagram/board.html`
- `term-control-center/shared/`
- `term-control-center/server/`
- `term-control-center/tests/`
- `src/agentops_harness/activity_center_completion.py`
- `src/agentops_harness/activity_center_models.py`
- `tests/unit/test_activity_center.py`
- `dev-plans/agentops/open-prd-sweep-ledger-2026-06-28.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-142-clickable-pipeline-lifecycle/`

## Forbidden scope
- No actual PR creation, merge, sync, closeout, teardown, deploy, PRD approval, trading, or backtesting by the coder.
- No hardcoded Project numbers, tracker IDs, local-only issue metadata, or personal credentials.
- No new autonomous lifecycle authority; each mutating UI action remains one operator click plus one confirmation.
- No product routes or deployment config changes unless needed for the approved lifecycle UI/orchestration surface.

## Checkpoints
1. Pipeline eligibility and clickable affordances: Implement remains status-only; eligible post-Implement stages expose clickability, states, and repeated-click protection.
2. PR action gate: one PR confirmation triggers existing prepare/open-PR route with no second draft approval.
3. Merge and Sync split: merge click preserves readiness checks; sync click runs post-merge local main/dev-main sync after merge evidence.
4. Closeout and teardown gates: closeout/teardown stages preserve evidence gates and confirmation.
5. Refresh/idempotency/profile/auth/guardrails: refresh queues, active profile/live project config, isolated auth, no forbidden authority.
6. Final validation and bug-check.

## Checkpoint 1 implementation summary
- Expanded the top-right implementation pipeline from `Implement → PR → Merge → Sync Main → Done` to `Implement → PR → Merge → Sync Local → Closeout → Teardown`.
- `Implement` remains status-only; later stages render as buttons only when their lifecycle action is idle/error and eligible.
- Pipeline classes now distinguish unavailable, available, running, succeeded, failed, and current states.
- Pipeline clicks reuse the same completion-action dispatcher and confirmation prompts as the action center.
- Revision 2 fixed `F142-R1-001`: clickable idle/error stages now become `current` rather than `pending unavailable`, `closeout_done` anchors Teardown as the active eligible phase, and prepare-PR failures anchor retry/failure styling to the PR stage.
- Revision 3 fixed `F142-IMPL-001` by making unknown/uncomputed mergeability checkable in the presented UI action while preserving live server refresh/blocking.
- Revision 3 partially fixed `F142-IMPL-002` by adding a completion lifecycle GitHub env helper that requires `AGENTOPS_GITHUB_TOKEN`, strips ambient operator GitHub env/prompting, and is used by prepare PR / PR read / branch push / merge read+mutation paths.
- After verifier escalated the remaining Git credential-helper push risk, the human approved the bounded follow-up; revision 4 now gives branch push a non-persisted agent-token Git credential helper, clears inherited credential helpers via command-scope Git config, disables system/global Git config, and maps SSH remotes to HTTPS for that push.
- PR confirmation explicitly states pre-PR checks, scoped commit, push, and PR creation/reuse happen after the single confirmation with no second draft approval.
- Split completion lifecycle orchestration so `merge-main` records merged PR evidence and `sync-main` separately runs/resumes the existing local main/dev-main sync workflow.
- Closeout and teardown remain blocked until merge+sync and closeout evidence respectively.
- Completion store, shared completion types, activity center summaries, notifications, and tests now understand `merged` and `syncing` states plus `sync_main` actions.
- Updated the shared sweep ledger entry for #142 with current worktree/branch and validation evidence.

## Changed Files
- `dev-plans/agentops/open-prd-sweep-ledger-2026-06-28.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-142-clickable-pipeline-lifecycle/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-142-clickable-pipeline-lifecycle/verifier-report.md`
- `pipeline-diagram/board.html`
- `src/agentops_harness/activity_center_completion.py`
- `src/agentops_harness/activity_center_models.py`
- `term-control-center/server/completionActionSequence.ts`
- `term-control-center/server/completionCloseoutRoutes.ts`
- `term-control-center/server/completionGithubEnv.ts`
- `term-control-center/server/completionRouteActionConfig.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/completionStore.ts`
- `term-control-center/server/completionTeardownRoutes.ts`
- `term-control-center/server/mergeMain.ts`
- `term-control-center/server/preparePr.ts`
- `term-control-center/server/projectActionConfig.ts`
- `term-control-center/shared/completion.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/completion-routes.test.ts`
- `term-control-center/tests/completion.test.ts`
- `term-control-center/tests/mergeMain.test.ts`
- `term-control-center/tests/preparePr.test.ts`

## Findings Addressed
- `F142-R1-001`: fixed pipeline phase/class derivation for closeout-done teardown eligibility and prepare-PR failure/retry placement; added board guardrail assertions for these cases.
- `F142-IMPL-001`: changed presented PR-open actions so unknown/uncomputed mergeability remains clickable/checkable; route refresh still blocks if the live PR remains non-mergeable.
- `F142-IMPL-002`: added isolated completion GitHub env handling and tests proving ambient `GH_TOKEN`/`GITHUB_TOKEN` fallback is rejected while `AGENTOPS_GITHUB_TOKEN` is mapped into command env. After human-approved follow-up, branch push also gets command-scope Git credential isolation (`credential.helper=` reset, GitHub-only helper sourced from `AGENTOPS_GITHUB_TOKEN`, SSH-to-HTTPS rewrite, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`).
- `F142-FINAL-001`: passed the same isolated Git credential env into `agentops-harness post-merge-sync` for initial and resumed sync paths, and added coverage that sync receives credential-helper reset / GitHub-only helper / prompt-disable config and rejects ambient operator token fallback.

## Validation Results
- ✅ `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/preparePr.test.ts tests/mergeMain.test.ts tests/completion.test.ts tests/completion-routes.test.ts tests/completion-store.test.ts tests/boardGuardrails.test.ts` using a temporary `term-control-center/node_modules` symlink to `/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules`; symlink removed after validation. Latest rerun after final sync credential isolation fix passed 106/106.
- ✅ `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py -q` (9/9).
- ✅ `git diff --check -- <changed files>`.
- ⚠️ `npm --prefix term-control-center run typecheck` is blocked by pre-existing missing React/xterm type packages in this worktree.
- ⚠️ `npx --no-install tsc -p tsconfig.server.json --noEmit` with the temporary borrowed `node_modules` symlink now reaches only pre-existing `tests/contextRenewal.test.ts` out-of-root `.ts` import errors; the new completion status/action/auth type errors were fixed.

## Verifier Status
- Checkpoint 1 revision 1: revision requested, `F142-R1-001`.
- Checkpoint 1 revision 2: approved by verifier; compact verdict reported 0 open findings.
- Final implementation checkpoints 2-9 revision 1: revision requested for `F142-IMPL-001` and `F142-IMPL-002`.
- Final implementation checkpoints 2-9 revision 2: verifier returned `needs_human` for `F142-IMPL-002` after bounded auth fix; report path `dev-plans/agentops/coder-verifier-workflow/runs/issue-142-clickable-pipeline-lifecycle/verifier-report.md`.
- Human decision: approved bounded follow-up to hard-fail/replace Git credential resolution for branch push instead of accepting the prior state.
- Final implementation checkpoints 2-9 revision 3: approved by verifier; compact verdict reported 0 open findings and `bug_check_status: pending`; next actor steward.
- Steward review: cleanup recommended for ignored caches; `.pytest_cache/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/` removed after validation reruns. `verifier-report.md` is intentionally retained as a durable run artifact.
- Final bug-check revision 1: verifier requested `F142-FINAL-001` for sync command inherited Git credentials; bounded fix applied.
- Final bug-check revision 2: approved by verifier; compact verdict reported 0 open findings and `bug_check_status: passed`; next actor human.
