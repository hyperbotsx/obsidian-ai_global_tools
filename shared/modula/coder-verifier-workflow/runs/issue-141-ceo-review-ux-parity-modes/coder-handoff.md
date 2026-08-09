# Coder Handoff — Issue 141 CEO review UX parity

## Task
- GitHub issue / PRD: https://github.com/hyperbotsx/agentops-harness/issues/141
- Branch: `prd/ceo-review-ux-parity-modes-141`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`
- PRD status: Approved; CEO approved in issue body/comments.

## Pre-edit status
- `git status --short --branch`: `## prd/ceo-review-ux-parity-modes-141...origin/main`
- Pre-existing dirty files: none.

## Scope controls
- Allowed paths: CEO review launch/runtime isolation, per-review artifact metadata, launch/session behavior, targeted Term Control tests, and docs/operator copy needed for runtime configuration.
- Forbidden: PRD approval mutations without human confirmation, implementation auto-start, target implementation worktree switching/cleaning/stashing, personal GitHub credential fallback, PR creation, merge, deploy, trading, backtests, raw transcript/secrets storage, Phase 2/3 completion claims before Phase 1 verification.
- Research-first surfaces: none in PRD.
- Validation commands: targeted Term Control launch-plan tests, Term Control typecheck, additional targeted tests as verifier requests.
- Stop condition: final verifier bug-check approval or human escalation.

## Verifier checkpoints
1. Phase 1 review-runtime isolation checkpoint.
2. Phase 1 branch-collision regression checkpoint.
3. Phase 1 concurrent review checkpoint.
4. Phase 2 mode-selection checkpoint.
5. Phase 2 guided questionnaire checkpoint.
6. Phase 2 assisted draft checkpoint.
7. Phase 2 human-answer payload checkpoint.
8. Phase 2 preview/apply gate checkpoint.
9. Phase 2 fail-closed/drift checkpoint.
10. Phase 3 post-approval session closeout checkpoint.
11. Phase 3 stale-agent roster checkpoint.
12. Security/auth checkpoint.
13. Parity checkpoint.
14. Final validation checkpoint.

## Current checkpoint implementation summary
- Implemented Phase 1 runtime isolation through `term-control-center/server/ceoReviewRuntime.ts` and `term-control-center/server/launchPlan.ts`:
  - `prd-review` launch plans now resolve a dedicated CEO review runtime from `TERM_CONTROL_CEO_REVIEW_WORKTREE` and `TERM_CONTROL_CEO_REVIEW_REF`.
  - CEO review pane cwd and wrapper path use the review runtime, not the target PRD implementation worktree.
  - Review runtime validation fails closed when missing, on the wrong ref, dirty, missing isolated agent GitHub auth, or relying only on operator `GH_TOKEN` / `GITHUB_TOKEN`.
  - Implementation launch behavior remains unchanged: target worktree/branch and clean-worktree checks still apply for `implementation` mode.
- Added review runtime env metadata for launched CEO reviewer panes: runtime worktree/ref, target implementation worktree/branch, artifact dir, repository/project, isolated auth mode.
- Addressed verifier R1 auth finding: CEO review pane env now sets `GH_CONFIG_DIR`/`AGENTOPS_GH_CONFIG_DIR` to the isolated config path and maps `GH_TOKEN`/`GITHUB_TOKEN` to `AGENTOPS_GITHUB_TOKEN` when present, or empty strings when auth is config-dir-only, so ambient operator tokens are not inherited.
- Addressed verifier R1 KISS finding: extracted review-runtime validation/auth env helpers into `ceoReviewRuntime.ts` and collapsed launch prompt plumbing around a `LaunchContext` object so new helper signatures stay within parameter budget.
- Added explicit branch-collision regression coverage that `prd-review` does not require the target implementation worktree to exist, and already covers dirty/mismatched target implementation worktrees.
- Added concurrent review launch-plan coverage proving separate PRD reviews share the configured runtime but receive distinct per-session artifact directories/proposal paths and target issue URLs.
- Implemented Phase 2 mode-selection checkpoint: PRD Studio Approval Review now shows a low-friction mode picker with **Guided Questionnaire** and **Assisted Draft Review**, persists the last safe mode in local storage, carries `ceoReviewMode` in the review task payload, validates the allowed values, and prompts the CEO reviewer with the selected mode. Revision fix: CEO review entrypoints now open the mode picker instead of auto-starting new review launches; existing live reviews can still be focused before setup.
- Implemented Phase 2 guided questionnaire engine checkpoint: real `ceo-review --mode questions` output now includes exactly four deterministic, grounded answer choices for every CEO review question. Choices reference the loaded issue number/title, labels, comments count, project item count, and evidence hint, then render in JSON/markdown for the CEO reviewer/app flow.
- Implemented Phase 2 assisted draft checkpoint: `ceo-review --mode propose-answers` already generates all draft answers up front, and the answer package now includes structured Assisted Draft controls for accept all, accept individual, and amend individual flows before `human-answers` finalization. Revision fix: accept-all now produces one `human-answer` entry per expected question, per-answer accept controls carry a ready human-answer entry, and per-answer amend controls carry an editable prefix.
- Implemented Phase 2 human-answer payload checkpoint coverage: guided choice answers and assisted accept-all answers both finalize through the same `human-answers` report shape with matching expected question IDs, answer counts, approval status, and non-executing mutation package status.
- Implemented Phase 2 preview/apply gate revision fix: preview/apply now accepts only complete `mode == "human-answers"` proposals; draft `propose-answers` payloads are not saved as applyable files and are refused at apply time. CLI apply tests now generate saved proposal files from explicit `--human-answer` entries. KISS recheck fixes: split CLI apply tests into `tests/unit/test_ceo_review_apply_cli.py`, bringing `tests/unit/test_ceo_review_apply.py` down to 276 lines, then extracted helpers so new CLI test functions stay under the 20-line limit.
- Implemented Phase 3 post-approval session closeout checkpoint: after successful board `/review/apply`, the app now attempts to close the matching live `prd-review` terminal group, refreshes terminal groups, preserves the approval/audit/history banner, and surfaces a retryable cleanup-needed banner if session closeout fails after approval succeeds. Revision fix: successful closeout now synchronously prunes the deleted group from `termGroupsCache`, re-renders chip/session state, and closes the active terminal modal/iframe when it was showing the closed review group.
- Implemented Phase 3 stale-agent roster checkpoint: normal active session counts, chip highlights, and same-issue reopen paths now use `isNormalActiveGroup`, which excludes stale/recovery panes; stale/recoverable groups remain visible only in the explicit session recovery list with stale/recovery copy. Final bug-check fix: `error` groups and panes marked `unrecoverable` are also classified as recovery/not-normal.
- Addressed final auth bug-check: CEO review launch now requires `AGENTOPS_GITHUB_TOKEN` and no longer accepts config-dir-only auth. Pane and Python gh environments map only the isolated token into `GH_TOKEN`/`GITHUB_TOKEN`, strip enterprise/host/repo ambient variables, and disable prompts to prevent operator credential/keyring fallback.
- Updated CEO reviewer prompt to distinguish GitHub-state CEO review runtime from implementation-worktree workflows and forbid switching/cleaning/occupying the target implementation worktree.
- Kept per-review artifacts isolated through the existing per-group context directory; CEO review proposal/current-state/audit paths are derived from the per-session context path.
- Updated PRD review group reuse so same-PRD review relaunches are keyed by canonical issue/project rather than target worktree/branch; implementation reuse still requires matching worktree/branch.
- Documented required CEO review runtime env configuration in `docs/admin-configuration.md`.

## Changed files
- `term-control-center/server/ceoReviewRuntime.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/shared/launcher.ts`
- `pipeline-diagram/board.html`
- `src/agentops_harness/ceo_review.py`
- `tests/unit/test_ceo_review.py`
- `src/agentops_harness/ceo_review_apply.py`
- `src/agentops_harness/github_cli_env.py`
- `src/agentops_harness/health.py`
- `tests/unit/test_agent_github_health.py`
- `tests/unit/test_ceo_review_apply.py`
- `tests/unit/test_ceo_review_apply_cli.py`
- `tests/unit/test_ceo_review_answers.py`
- `docs/admin-configuration.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-141-ceo-review-ux-parity-modes/coder-handoff.md`

## Validation
- `cd term-control-center && node --import tsx --test tests/launchPlan.test.ts` — pass (17 tests, before mode-selection tests were added).
- `cd term-control-center && node --import tsx --test tests/launchPlan.test.ts tests/launcher.test.ts tests/boardGuardrails.test.ts` — pass (80 tests).
- `cd term-control-center && npm run typecheck` — pass.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_ceo_review.py tests/unit/test_ceo_review_answers.py` — pass (28 tests).
- `PYTHONPATH=src python3 -m pytest tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_apply_cli.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_answers.py` — pass (54 tests).
- `PYTHONPATH=src python3 -m pytest tests/unit/test_agent_github_health.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_apply_cli.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review.py` — pass (61 tests).
- Earlier broad attempt `cd term-control-center && npm test -- --test-name-pattern="PRD review|implementation launch plan"` timed out after running unrelated full-suite tests; targeted launch-plan/typecheck passed. The broad run showed unrelated pre-existing/flaky server tmux/planner failures, not failures in the new launch-plan tests.

## Reviews / findings
- Verifier R1: `revision_requested`, findings `F141-P1-R1-001`, `F141-P1-R1-002`.
- Verifier R2: `approved`, open findings 0.
- Verifier R3 branch-collision checkpoint: `approved`, open findings 0.
- Verifier R4 concurrent review checkpoint: `approved`, open findings 0.
- Verifier R5 mode-selection checkpoint: `revision_requested`, finding `F141-P2-MODE-R1-001`.
- Verifier R6 mode-selection recheck: `approved`, open findings 0.
- Verifier R7 guided questionnaire checkpoint: `approved`, open findings 0.
- Verifier R8 assisted draft checkpoint: `revision_requested`, finding `F141-P2-DRAFT-R1-001`.
- Verifier R9 assisted draft recheck: `approved`, open findings 0.
- Verifier R10 human-answer payload checkpoint: `approved`, open findings 0.
- Verifier R11 preview/apply gate checkpoint: `revision_requested`, finding `F141-P2-GATE-R1-001`.
- Verifier R12 preview/apply gate recheck: `revision_requested`, finding `F141-P2-GATE-R2-001`.
- Verifier R13 preview/apply KISS recheck: `revision_requested`, finding `F141-P2-GATE-R3-001`.
- Verifier R14 preview/apply CLI KISS recheck: `approved`, open findings 0.
- Verifier R15 fail-closed/drift checkpoint: `approved`, open findings 0.
- Verifier R16 post-approval session closeout checkpoint: `revision_requested`, finding `F141-P3-CLOSEOUT-R1-001`.
- Verifier R17 post-approval session closeout recheck: `approved`, open findings 0.
- Verifier R18 stale-agent roster checkpoint: `approved`, open findings 0.
- Verifier R19 security/auth checkpoint: `approved`, open findings 0.
- Verifier R20 parity checkpoint: `approved`, open findings 0.
- Verifier R21 final validation checkpoint: `approved`, open findings 0.
- Steward pre-final hygiene review: `clean`; no cleanup requested.
- Verifier final bug-check R22: `revision_requested`, findings `F141-FINAL-001`, `F141-FINAL-002`.
- Verifier final bug-check R23 recheck: `approved`; bug-check passed, open findings 0.

## Findings addressed
- `F141-P1-R1-001`: CEO reviewer pane env now explicitly isolates GitHub auth and prevents ambient operator token fallback even when isolated auth is configured.
- `F141-P1-R1-002`: Review runtime validation/env logic extracted to a focused module; new launch prompt plumbing uses a context object instead of >4 parameter helper chains.
- `F141-P2-MODE-R1-001`: New CEO review entrypoints now present the mode picker and require the operator to press Start approval review; auto-start was removed from the review button and global `openReview()` path.
- `F141-P2-DRAFT-R1-001`: Assisted Draft controls are now structured/actionable instead of prose-only; tests prove accept-all finalizes all answers and accept/amend individual entries feed `human-answers` without approval mutation.
- `F141-P2-GATE-R1-001`: Draft `propose-answers` proposals are no longer applyable; only complete `human-answers` proposals can be saved/previewed/executed after explicit confirmation.
- `F141-P2-GATE-R2-001`: Split CLI apply coverage out of the oversized touched test file; apply test file is now under 300 lines while keeping all gate coverage.
- `F141-P2-GATE-R3-001`: Extracted CLI test helpers so the two new test methods are below the function-size limit.
- `F141-P3-CLOSEOUT-R1-001`: Successful closeout now clears the local terminal group cache/highlights and closes the active terminal iframe/modal for the deleted CEO review group.
- `F141-FINAL-001`: Config-dir-only CEO review auth now fails closed; isolated `AGENTOPS_GITHUB_TOKEN` is required and ambient gh token/keyring prompt variables are stripped/disabled.
- `F141-FINAL-002`: Partially unrecoverable/error terminal groups now route to recovery/not-normal roster handling instead of active counts/highlights/reopen paths.

## Known risks / notes
- Phase 1, Phase 2, Phase 3, security/auth, parity, final validation, steward hygiene, and final verifier bug-check are approved.
- The launch validation now requires isolated `AGENTOPS_GITHUB_TOKEN` and blocks config-dir-only/operator-token fallback; no approval mutation path was changed.
