# Coder handoff — Issue 161

## Task

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/161
- Branch: `prd/ceo-review-low-friction-approval-autoclose-161`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-161`
- PRD status read from GitHub issue: approved by human/CEO.

## Pre-existing worktree state

- `git status --short --branch` before edits: clean on `prd/ceo-review-low-friction-approval-autoclose-161...origin/main`.
- Memory disabled per launch context; not used.

## Scope controls

Allowed paths for checkpoints 1-2:
- `src/agentops_harness/prd_author_github.py`
- `src/agentops_harness/prd_create.py`
- `src/agentops_harness/prd_create_fields.py`
- `src/agentops_harness/prd_create_request.py`
- `src/agentops_harness/review_server.py`
- `src/agentops_harness/ceo_review_intent.py`
- `src/agentops_harness/ceo_review_execute.py`
- `src/agentops_harness/ceo_review_apply.py`
- `src/agentops_harness/ceo_review_apply_types.py`
- `src/agentops_harness/ceo_review_evonome_apply.py`
- `src/agentops_harness/cli.py`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/approvalReviewCloseout.ts`
- `pipeline-diagram/board.html`
- focused tests under `tests/unit/` and `term-control-center/tests/`
- this run artifact folder

Forbidden/out of scope:
- PR creation, merge, deploy, trading, backtests
- autonomous PRD approval or implementation launch
- secrets/raw transcripts/private env dumps
- unrelated terminal/session teardown
- product route/navigation redesign outside PRD Studio authoring/review scope

## Checkpoints

1. Direct PRD creation checkpoint — clear PRD-write requests create draft GitHub issues/Project items immediately; ambiguous or unsafe requests ask/fail closed.
2. Approval intent checkpoint — phrase matching, active proposal binding, answer completeness, drift refusal, and no-mutation failures.
3. Apply execution checkpoint — internal execute path uses existing approval engine, audit records, isolated auth, and partial-failure verification.
4. Auto-close checkpoint — verified approval closes only current review group/session and returns to board with summary.
5. Regression/safety checkpoint — long command remains debug-only, unrelated sessions and forbidden actions remain untouched; final bug-check.

## Implemented checkpoint 1 — Direct PRD creation

Changed behavior:
- `prd_author_github.create_steps()` now plans direct draft issue creation for clear bounded requests instead of a terminal draft-confirmation step.
- `prd_create.create_prd_issue(..., direct=True)` skips the old terminal confirmation phrase while preserving profile routing, required label checks, final-body safety checks, issue creation, Project add, launch metadata body update, draft Project field application/readback, and draft-only behavior.
- Existing confirmed creation behavior remains available when `direct=False`.
- Direct creation now fails closed before `gh issue create` when required PRD/status/owner labels cannot be resolved; if the configured profile owner label is unavailable but the repo exposes exactly one `agent:` label, that single repo owner label is used.
- Direct creation re-checks semantic final draft sections before mutation so split/unsafe body drift cannot bypass an initially clear idea, while generated and benign-edited single-domain PRD bodies pass.
- Direct creation fails closed for minimal/incomplete bodies that lack required PRD metadata/sections instead of creating incomplete issues.
- Draft Project field handling now preflights configured fields before issue creation, maps Project 2-style draft status options, recognizes live `ProjectV2SingleSelectField` types, avoids text fallbacks for single-select fields, and read-backs `Working Branch`, `Worktree Path`, and `Base Branch`.
- Effective Project metadata is normalized into the final issue body for override/project-context creation so stale profile Project/tracker/owner lines are not retained.
- Direct creation request parsing moved to `prd_create_request.py`; new/modified helper signatures stay within KISS parameter limits and `prd_create.py` is under the 300-line target.
- `review_server` PRD authoring prompt now tells the authoring flow to clarify only when material scope/safety/profile/auth/project details are unclear, and to produce a final PRD for direct draft GitHub issue creation.
- `/prd/create` no longer requires a confirmation value; if one is supplied it must still be supported. Calls without confirmation use `direct=True`.
- Term Control PRD Author launch prompt now instructs direct GitHub draft creation for clear `write/create/make PRD` requests and repeats approval/PR/merge/deploy/trading/backtest boundaries.

Changed files:
- `src/agentops_harness/prd_author_github.py`
- `src/agentops_harness/prd_create.py`
- `src/agentops_harness/prd_create_fields.py`
- `src/agentops_harness/prd_create_request.py`
- `src/agentops_harness/review_server.py`
- `term-control-center/server/launchPlan.ts`
- `tests/unit/test_prd_author_github.py`
- `tests/unit/test_prd_create.py`
- `src/agentops_harness/ceo_review_intent.py`
- `tests/unit/test_ceo_review_intent.py`
- `tests/unit/test_ceo_review_execute.py`
- `tests/unit/test_ceo_review_apply.py`
- `tests/unit/test_ceo_review_apply_cli.py`
- `term-control-center/server/approvalReviewCloseout.ts`
- `term-control-center/tests/approvalReviewCloseout.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `pipeline-diagram/board.html`

## Implemented checkpoint 2 — Approval intent

Changed behavior:
- Added `ceo_review_intent.evaluate_approval_intent()` for the no-mutation approval-intent gate.
- Normalizes `approve prd`, `approve`, and harmless case/punctuation (for example `Approve PRD.`) to the existing apply confirmation value `approved by human`.
- Refuses approval intent unless there is exactly one active proposal with matching proposal IDs.
- Refuses non-final, incomplete-answer, blocked, missing/malformed proposal ID, literal `unknown` proposal IDs, missing current state, missing audit dir, missing explicit clean preview, and drifted current-state cases before any mutation path.
- Keeps unrelated/generic text such as `yes` ignored rather than approval.
- CEO review launch prompt now explicitly says: `Reply approve prd or approve to apply this approval package`, and scopes that phrase to the current complete/current/previewed/applyable proposal only.

## Implemented checkpoint 3 — Apply execution

Changed behavior:
- Added `ceo_review_execute.execute_approval_intent()` as the internal approval-intent execution path: it evaluates the accepted phrase/proposal/current-state/preview/audit gate, then calls existing `apply_confirmed_proposal(..., execute=True, mutation_sink=...)` with the normalized `approved by human` confirmation.
- Added a narrow runtime CLI surface: `agentops-harness ceo-review approve-intent --approval-text ... --proposal-file ... --current-state-json ... --audit-dir ... --preview-status ready_for_external_apply --execute --format json`, wired to the production isolated-auth mutation sink.
- Refused approval intent returns without invoking the apply path or mutation sink.
- `ApplyResult` and audit payload now include `canonical_approval_verified`.
- Execution audits carry accepted human phrase, normalized confirmation, proposal state digest, mutation preview status, execution result, and `auto_close_triggered=false` for checkpoint 3.
- After any execution sink return or partial failure, the apply path re-reads canonical GitHub issue state and treats the result as executed only when `status:approved` and `CEO approved: Yes` are verified; otherwise it remains `execution_refused`.
- Existing dry-run/execute behavior remains available for debug/manual CLI flows.
- Apply request/options/audit helper dataclasses moved to `ceo_review_apply_types.py`; changed checkpoint helper signatures now stay within KISS parameter limits.

## Implemented checkpoint 4 — Auto-close

Changed behavior:
- Added exact review-group closeout helper `closeApprovedReviewGroup()` that only closes matching `mode: 'prd-review'` groups for the approved PRD issue number and exact group id/project/task metadata.
- Added Term Control route `POST /approval-review/closeout`, reusing existing lifecycle/killGroup semantics and preserving unrelated implementation/browser/coder/verifier groups.
- CEO review launch prompt now includes the active review group id and instructs closeout only after `approve-intent` returns `status=executed` with `canonical_approval_verified=true`.
- Board approval closeout now calls the exact approval-review closeout route with group id and task metadata, removes the closed group from local remembered state, closes the active terminal modal only when it was the closed review group, refreshes groups, and surfaces retry guidance on cleanup failure.
- Approval banner/closeout message now include the approved PRD number, audit path when available, and exact group/session identifiers on cleanup failure; history/audit remains available and raw transcripts are not persisted.

## Validation

Passed:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_create.py tests/unit/test_prd_create_direct.py tests/unit/test_prd_author_github.py tests/unit/test_review_server_coworker.py tests/unit/test_ceo_review_intent.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_execute.py tests/unit/test_ceo_review_apply_cli.py -q` → 113 passed.
- `cd term-control-center && node --import tsx --test tests/approvalReviewCloseout.test.ts` → 3 passed.
- `cd term-control-center && node --import tsx --test --test-name-pattern "board closes approved CEO review sessions|PRD review launch prompt|PRD Author launch prompt supports direct" tests/boardGuardrails.test.ts tests/launchPlan.test.ts` → 4 passed.
- `git diff --check` → passed.

Environment/setup notes:
- `npm --prefix term-control-center ci` was run because `term-control-center/node_modules` was absent; no tracked package files changed.

Known unrelated validation blockers:
- `npm --prefix term-control-center run typecheck` fails on pre-existing `tests/contextRenewal.test.ts` rootDir/allowImportingTsExtensions errors involving `pi-packages/agentops-context-renewal/lib/policy.ts` outside `term-control-center` rootDir.
- Full `cd term-control-center && node --import tsx --test tests/launchPlan.test.ts` has unrelated environment-sensitive failures for isolated review auth/browser QA allowlist/profile expectations. The targeted changed PRD Author prompt test passes.

## Findings addressed

Revision 2:
- `F161-R1-001`: required label resolution now fails closed instead of silently degrading; single repo `agent:` label fallback covers active AgentOps Harness label shape.
- `F161-R1-002`: direct mode re-runs creation safety against the final draft before mutation.
- `F161-R1-003`: draft field setup applies configured draft Project fields and read-backs Base Branch with Working Branch and Worktree Path.
- `F161-R1-004`: removed the six-argument direct gate helper and split direct vs confirmed safety helpers.

Revision 3:
- `F161-R2-001`: final safety now accepts the generated single-domain body and checks extracted intent text for edited/mismatched bodies.
- `F161-R2-002`: draft Project field preflight runs before issue creation; single-select writes require valid mapped options and no longer fall back to text writes.
- `F161-R2-003`: launch/body metadata normalization rewrites effective assigned agent, GitHub Project, Base branch, and tracker lines for override/project-context creation.

Revision 4:
- `F161-R3-001`: scope safety now parses scope-bearing sections after Non-goals and blocks split/unsafe Functional requirements before mutation.
- `F161-R3-002`: single-select detection now handles live GitHub `ProjectV2SingleSelectField` strings and tests command generation for option IDs.
- `F161-R3-003`: incomplete/minimal bodies now fail closed before mutation unless they are the generated full PRD body.
- `F161-R3-004`: direct creation entrypoint was split into focused helpers and `EffectiveProjectContext`; `prd_create.py` is now 293 lines.

Revision 5:
- `F161-R4-001`: final-body safety now classifies only semantic scope sections (`title`, `problem`, `goal`, `functional requirements`, `acceptance criteria`) and filters metadata/URL/worktree/tracker/preview/hygiene boilerplate. Added benign-edited PRD regression that creates successfully.
- `F161-R4-002`: moved create request/override parsing into `prd_create_request.py`, changed creation APIs to keyword options, and kept new/modified helpers under 20 lines and no more than 4 counted parameters. `prd_create.py` is now 289 lines.

## Research consult

- Consulted researcher before the third fix attempt on recurring body-safety/Project field issues. Guidance: keep exact generated-body fast path, parse scope-bearing sections excluding boilerplate-negative sections for edited bodies, compare domains, normalize single-select type strings by checking alphanumeric `singleselect`, preflight select option IDs before issue creation, and never text-write single-select fields.

## Steward review

- Steward reviewed changed-file placement and run artifacts after checkpoint 4 approval.
- Placement approved for Python helpers/tests, Term Control helper/tests, board update, and run artifact folder.
- No secret-like values found in run folder; secret-content hygiene notes were false positives from token variable names/test placeholders.
- Cleaned ignored Python caches: `.pytest_cache/`, `src/agentops_harness/__pycache__/`, `tests/unit/__pycache__/`.
- Removed ignored validation/cache artifacts after final verifier approval, including Python `__pycache__` folders and `term-control-center/node_modules/`.

## Risks / reviewer focus

- Verify extracted intent safety remains sufficient for genuinely edited unsafe bodies while allowing normal generated PRD boilerplate.
- Verify single `agent:` label fallback is acceptable for project-specific owner resolution when the profile owner label is not present in the target repository.
- Verify direct-created issues remain draft/unapproved and only receive PRD/status/owner labels, launch metadata, and configured draft Project fields.

## Checkpoint 2 revision history

Revision 2:
- `F161-C2-001`: preview evidence now fails closed by default; callers must pass explicit `ready_for_external_apply` status.
- `F161-C2-002`: proposal binding now requires non-empty top-level and `approval_ux` proposal IDs.

Revision 3:
- `F161-C2-002`: proposal IDs must match generated shape `ceo-review-[0-9a-f]{12}`; literal `unknown` IDs are refused even when both proposal fields match.

## Checkpoint 3 revision history

Revision 2:
- `F161-C3-001`: added `ceo-review approve-intent` CLI runtime surface and updated CEO review launch prompt with the internal apply command.
- `F161-C3-002`: execution audit now includes accepted phrase, normalized confirmation, state digest, preview status, execution result, and `auto_close_triggered=false`.
- `F161-C3-003`: successful callback return no longer implies verification; canonical readback is required before `canonical_approval_verified=true` or `status=executed`.
- `F161-C3-004`: moved apply request/options/audit context to dataclasses and reduced changed helper parameter counts.

Revision 3:
- `F161-C3-005`: review launch prompt now passes `--approval-text "<exact approval phrase>"` instead of hardcoding `approve prd`; CLI test covers `approve`.
- `F161-C3-006`: `execute_approval_intent()` catches proposal/current-state read failures and returns a structured refusal with no mutation sink call.
- `F161-C3-007`: collapsed `run_cli_apply` helper inputs so the modified test helper is within parameter limits.

Revision 4:
- `F161-C3-006`: `execute_approval_intent()` now also catches omitted `None` path cases; CLI regressions cover omitted `--proposal-file` and omitted `--current-state-json`.

## Checkpoint 4 revision history

Revision 2:
- `F161-C4-001`: launch prompt now ties successful verified `approve-intent` execution to `POST /approval-review/closeout` for the active review group.
- `F161-C4-002`: closeout now requires exact group id plus optional project/repository/worktree/branch metadata and refuses same-issue mismatches.
- `F161-C4-003`: cleanup-needed banner includes exact group id and session ids for manual cleanup/retry.

Revision 3:
- `F161-C4-004`: board refresh now detects when the current `prd-review` group disappears after in-pane closeout, closes the terminal modal, and shows a board toast that the operator returned to the board.

Revision 4:
- `F161-C4-005`: closeout route persists closeout metadata keyed by group id, writes a small `.closeout.json` sidecar next to the apply audit when `auditPath` is supplied, and parent-board disappearance toast now fetches that metadata to show `Approved #<prd>` plus audit path.

## Checkpoint 5 revision history

Revision 2:
- `F161-C5-001`: direct PRD creation now runs `agent_github_write_check()` after label/field preflight and before `issue create`, requiring repository write plus Project `viewerCanUpdate` verification before any GitHub mutation. Added regression coverage that unverified Project write scope makes no `gh issue create` call.

Revision 3:
- `F161-C5-002`: split direct PRD creation tests into `tests/unit/test_prd_create_direct.py` and refactored artifact fixture helpers so touched test files and helpers stay within KISS size targets.

## Checkpoint approvals

- Checkpoint 1 direct PRD creation approved by verifier at revision 5.
- Checkpoint 2 approval intent approved by verifier at revision 3.
- Checkpoint 3 apply execution approved by verifier at revision 4.
- Checkpoint 4 auto-close approved by verifier at revision 4.
- Checkpoint 5 regression/safety final bug-check approved by verifier at revision 3 (`bug_check_status=passed`).

## Next step

Final verifier approval received for checkpoint 5 revision 3 with bug-check passed. No PR was created; branch is ready for human-managed next steps.
