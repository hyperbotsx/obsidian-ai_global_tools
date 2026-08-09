# Coder Handoff

## Task

- GitHub issue: `https://github.com/hyperbotsx/SoldierOne/issues/940`
- PRD: `GitHub issue #940`
- Branch: `prd/worktree-branch-ownership-enforcement-940`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-harness`
- Agent label: `agent:evonome-admin`
- Checkpoint: `Final PRD #940 completion review fixes`
- Worktree/branch preflight passed: `yes`

## Scope

Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690`
Verifier socket: `/tmp/agentops/pi-verifier-agentops-harness.sock`
Preview target: `not configured for this worktree`
Preview URL: `not applicable`
Preview deploy command: `not configured`
Browser QA / DevTools required: `no`
Browser QA target URL/path: `not applicable`

Allowed paths:

- `src/agentops_harness/prd_ownership.py`
- `src/agentops_harness/prd_preflight.py`
- `src/agentops_harness/handoff_metadata.py`
- `src/agentops_harness/ai_maestro_handoff_mirror.py`
- `src/agentops_harness/profile_setup.py`
- `src/agentops_harness/ephemeral_cleanup.py`
- `src/agentops_harness/git_town.py`
- `src/agentops_harness/session_adoption.py`
- `src/agentops_harness/post_merge_sync.py`
- `src/agentops_harness/merge_conflict.py`
- `src/agentops_harness/parallel_plan.py`
- `src/agentops_harness/cli.py`
- `tests/unit/test_prd_ownership.py`
- `tests/unit/test_prd_preflight.py`
- `tests/unit/test_handoff_metadata.py`
- `tests/unit/test_ai_maestro_handoff_mirror.py`
- `tests/unit/test_profile_setup.py`
- `tests/unit/test_ephemeral_cleanup.py`
- `tests/unit/test_git_town.py`
- `tests/unit/test_session_adoption.py`
- `tests/unit/test_post_merge_sync.py`
- `tests/unit/test_merge_conflict.py`
- `tests/unit/test_parallel_plan.py`
- `tests/unit/test_cli.py`
- `docs/worktree-branch-ownership.md`
- `docs/operations.md`
- `README.md`
- `profiles/evonome.example.yaml`
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/`

Explicit non-goals:

- No product application code, routes, navigation, deployment config, raw transcripts, secrets, PR creation, merge, or tracker update.
- No autonomous branch creation; branch already matched PRD #940 before work began.
- Final PRD #940 completion review requested; no PR creation requested.

## Dirty Tree Before Editing

- none; `git status --short --branch` showed only `## prd/worktree-branch-ownership-enforcement-940`

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Mapping and branch naming policy review | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| 2 | Preflight fail-closed behavior review | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| 3 | Coder/verifier metadata integration review | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| Final bug-check | `after full implementation` | `needs_human` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 1 | Profile init/loading validation | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 2 | Ephemeral artifact cleanup | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 3 | Git Town detection and fallback policy | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 4 | Manual session adoption/refresh validation | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 5 | Post-merge sync verification | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 6 | Merge-conflict ownership validation | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 7 | Parallel PRD plan classification | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| V-FINAL-001 slice 8 | Interactive init prompt UX | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |
| Final completion review | PRD #940 completion bug-check | `ready` | `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md` |

## Changed Files

- `src/agentops_harness/prd_ownership.py`: adds default agent-label worktree policy, preview URL lookup, PRD branch proposal, branch validation, and policy renderers.
- `src/agentops_harness/prd_preflight.py`: adds deterministic PRD execution preflight data model, fail-closed checks, preview target enforcement, dirty/ephemeral classification, and markdown/json renderers.
- `src/agentops_harness/handoff_metadata.py`: validates coder/verifier artifacts and fails stale verifier reports against sibling coder-ready checkpoint/revision.
- `src/agentops_harness/ai_maestro_handoff_mirror.py`: includes agent label/preflight status and preserves verifier-report-local checkpoint truth.
- `src/agentops_harness/profile_setup.py`: adds generated and config-file profile initialization, profile loading, path/preview/ephemeral config rendering, canonical worktree scanning, and noncanonical candidate skipping.
- `src/agentops_harness/ephemeral_cleanup.py`: adds configured ephemeral artifact cleanup planning, tracked restore, and untracked removal.
- `src/agentops_harness/git_town.py`: adds read-only Git Town availability/configuration detection, preferred command output, and fallback rules.
- `src/agentops_harness/session_adoption.py`: adds manual session adopt/refresh validation for worktree, branch, and evidence.
- `src/agentops_harness/post_merge_sync.py`: adds post-merge local main/dev-main sync apply and verification checks.
- `src/agentops_harness/merge_conflict.py`: adds PRD branch/worktree conflict ownership validation and risky conflict file detection.
- `src/agentops_harness/parallel_plan.py`: classifies parallel PRD plans for shared worktrees, shared branches, branch issue mismatches, and path overlap.
- `src/agentops_harness/cli.py`: adds ownership policy, init with interactive prompts, Git Town check, session adopt/refresh, post-merge sync, merge-conflict check, parallel plan check, preflight cleanup, and handoff metadata check commands.
- `tests/unit/test_profile_setup.py`: covers generated profile writing, noncanonical worktree skipping, config-file validation, preview URL validation, and JSON output.
- `tests/unit/test_ephemeral_cleanup.py`: covers cleanup planning plus tracked restore and untracked removal.
- `tests/unit/test_git_town.py`: covers configured, unavailable, misconfigured, and missing-worktree Git Town checks.
- `tests/unit/test_session_adoption.py`: covers valid manual adoption, wrong branch number, missing evidence, refresh, and markdown errors.
- `tests/unit/test_post_merge_sync.py`: covers verified targets, dirty targets, wrong commits, apply command sequence, and markdown output.
- `tests/unit/test_merge_conflict.py`: covers valid conflict checks, wrong branch, missing worktree, risky verifier-required files, and markdown output.
- `tests/unit/test_parallel_plan.py`: covers compatible plans, shared worktrees, overlapping paths, missing issue in branch, empty plan lists, invalid specs, and markdown output.
- `tests/unit/test_cli.py`: covers new CLI pass/block paths, interactive init accept/cancel flows, profile-backed preflight, preflight cleanup, Git Town command output, session adoption CLI, post-merge sync CLI, merge-conflict CLI, and parallel plan CLI.
- Other tests/docs/profile/README listed above support the policy, preflight, metadata, and profile setup surfaces.
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/decision-log.md`: records approvals, findings, human continuation decision, and slice decisions.

## Validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_setup.py tests/unit/test_cli.py && git diff --check`: `pass` (29 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (189 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_setup.py tests/unit/test_cli.py tests/unit/test_prd_preflight.py && git diff --check`: `pass` (44 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (193 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_ephemeral_cleanup.py tests/unit/test_cli.py tests/unit/test_prd_preflight.py && git diff --check`: `pass` (41 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (196 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_ephemeral_cleanup.py tests/unit/test_cli.py tests/unit/test_prd_preflight.py && git diff --check`: `pass` (42 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (197 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_git_town.py tests/unit/test_cli.py && git diff --check`: `pass` (35 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_git_town.py tests/unit/test_cli.py && git diff --check && PYTHONPATH=src python3 -m agentops_harness.cli git-town-check --worktree . --format json`: `pass` (real CLI returned `status=ok`)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (203 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_session_adoption.py tests/unit/test_cli.py && git diff --check`: `pass` (36 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (209 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_session_adoption.py tests/unit/test_cli.py && git diff --check`: `pass` (38 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (211 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_session_adoption.py tests/unit/test_cli.py && git diff --check`: `pass` (39 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (212 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_session_adoption.py tests/unit/test_cli.py && git diff --check`: `pass` (40 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (213 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_session_adoption.py tests/unit/test_cli.py && git diff --check`: `pass` (41 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (214 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_post_merge_sync.py tests/unit/test_cli.py && git diff --check`: `pass` (37 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (220 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_post_merge_sync.py tests/unit/test_cli.py && git diff --check`: `pass` (41 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (224 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_merge_conflict.py tests/unit/test_cli.py && git diff --check`: `pass` (39 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (230 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_merge_conflict.py tests/unit/test_cli.py && git diff --check`: `pass` (41 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (232 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_parallel_plan.py tests/unit/test_cli.py && git diff --check`: `pass` (42 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (240 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_parallel_plan.py tests/unit/test_cli.py && git diff --check`: `pass` (46 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (244 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_parallel_plan.py tests/unit/test_cli.py && git diff --check`: `pass` (48 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (246 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_parallel_plan.py tests/unit/test_cli.py && git diff --check`: `pass` (51 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (249 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_parallel_plan.py tests/unit/test_cli.py && git diff --check`: `pass` (53 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (251 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_cli.py && git diff --check`: `pass` (37 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (253 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_cli.py && git diff --check`: `pass` (38 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (254 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_cli.py tests/unit/test_profile_setup.py && git diff --check`: `pass` (45 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (255 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_cli.py tests/unit/test_profile_setup.py && git diff --check`: `pass` (46 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (256 full tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (256 full tests; diff check passed for final completion review)
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py tests/unit/test_profile_setup.py tests/unit/test_cli.py && git diff --check`: `pass` (63 targeted tests; diff check passed)
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass` (262 full tests; diff check passed)

## Assumptions

- The profile setup slice may be reviewed independently from the other remaining `V-FINAL-001` acceptance criteria.
- Interactive init prompts are implemented for profile name, worktrees root, and write confirmation.
- Profile checks are read-only until writing the generated profile under the configured local config root outside the repository.
- Profile-backed preflight now uses profile preview URL mappings and the `agentops_harness` admin implementation override when present.

## Known Gaps

- No known implementation gaps remain in the PRD #940 scope.
- Final completion is not claimed until verifier approves this final review.

## Verifier Pairing

- Required: `yes`
- Reason: full-auto coder/verifier workflow requires checkpoint approval before continuing.
- Coder ready file: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-ready.md`
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md`

## Coder Decision

`ready_for_verifier`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1 | initial Checkpoint 1 implementation | policy code, CLI, tests, docs/profile/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 2 | Checkpoint 2 implementation | preflight core, CLI/docs/tests updates | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 3 | Checkpoint 3 implementation | metadata validation core, mirror metadata fields, CLI/docs/tests updates | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 4 | `V-CP3-001` stale verifier report finding | `src/agentops_harness/handoff_metadata.py`, `src/agentops_harness/ai_maestro_handoff_mirror.py`, `tests/unit/test_handoff_metadata.py`, `tests/unit/test_ai_maestro_handoff_mirror.py` | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 5 | final authority-boundary evidence review | all changed files | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 6 | `V-FINAL-002` missing report-local checkpoint mirror finding | `src/agentops_harness/ai_maestro_handoff_mirror.py`, `tests/unit/test_ai_maestro_handoff_mirror.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `needs_human_for_V_FINAL_001` |
| 7 | human decision to continue; `V-FINAL-001` slice 1 profile init/loading | `src/agentops_harness/profile_setup.py`, `src/agentops_harness/cli.py`, `tests/unit/test_profile_setup.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 8 | `V-SLICE1-001` and `V-SLICE1-002` fixes | `src/agentops_harness/profile_setup.py`, `src/agentops_harness/prd_preflight.py`, `src/agentops_harness/cli.py`, `tests/unit/test_profile_setup.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 9 | `V-FINAL-001` slice 2 ephemeral artifact cleanup | `src/agentops_harness/ephemeral_cleanup.py`, `src/agentops_harness/cli.py`, `tests/unit/test_ephemeral_cleanup.py`, `tests/unit/test_cli.py`, docs, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 10 | `V-SLICE2-001` cleanup failure propagation | `src/agentops_harness/cli.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 11 | `V-FINAL-001` slice 3 Git Town detection and fallback policy | `src/agentops_harness/git_town.py`, `src/agentops_harness/cli.py`, `tests/unit/test_git_town.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 12 | `V-SLICE3-001` Git Town version probe fix | `src/agentops_harness/git_town.py`, `tests/unit/test_git_town.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 13 | `V-FINAL-001` slice 4 manual session adoption/refresh validation | `src/agentops_harness/session_adoption.py`, `src/agentops_harness/cli.py`, `tests/unit/test_session_adoption.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 14 | `V-SLICE4-001` mismatched evidence fail-closed fix | `src/agentops_harness/session_adoption.py`, `tests/unit/test_session_adoption.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 15 | `V-SLICE4-001` PRD issue evidence mismatch fix | `src/agentops_harness/session_adoption.py`, `tests/unit/test_session_adoption.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 16 | `V-SLICE4-001` mixed issue metadata fix | `src/agentops_harness/session_adoption.py`, `tests/unit/test_session_adoption.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 17 | `V-SLICE4-001` invalid issue metadata fix | `src/agentops_harness/session_adoption.py`, `tests/unit/test_session_adoption.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 18 | `V-FINAL-001` slice 5 post-merge sync verification | `src/agentops_harness/post_merge_sync.py`, `src/agentops_harness/cli.py`, `tests/unit/test_post_merge_sync.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 19 | `V-SLICE5-001` and `V-SLICE5-002` post-merge sync fixes | `src/agentops_harness/post_merge_sync.py`, `src/agentops_harness/cli.py`, `tests/unit/test_post_merge_sync.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 20 | `V-FINAL-001` slice 6 merge-conflict ownership validation | `src/agentops_harness/merge_conflict.py`, `src/agentops_harness/cli.py`, `tests/unit/test_merge_conflict.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 21 | `V-SLICE6-001` and `V-SLICE6-002` merge-conflict fixes | `src/agentops_harness/merge_conflict.py`, `src/agentops_harness/cli.py`, `tests/unit/test_merge_conflict.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 22 | `V-FINAL-001` slice 7 parallel PRD plan classification | `src/agentops_harness/parallel_plan.py`, `src/agentops_harness/cli.py`, `tests/unit/test_parallel_plan.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 23 | `V-SLICE7-001` through `V-SLICE7-003` parallel plan fixes | `src/agentops_harness/parallel_plan.py`, `tests/unit/test_parallel_plan.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 24 | `V-SLICE7-002` high-risk shared-area fix | `src/agentops_harness/parallel_plan.py`, `tests/unit/test_parallel_plan.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 25 | `V-SLICE7-002` remaining high-risk shared-area variants | `src/agentops_harness/parallel_plan.py`, `tests/unit/test_parallel_plan.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 26 | `V-SLICE7-002` paper/live model/component/chart high-risk fix | `src/agentops_harness/parallel_plan.py`, `tests/unit/test_parallel_plan.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 27 | `V-FINAL-001` slice 8 interactive init prompt UX | `src/agentops_harness/cli.py`, `tests/unit/test_cli.py`, docs/README, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 28 | `V-SLICE8-001` interactive init field coverage fix | `src/agentops_harness/cli.py`, `src/agentops_harness/profile_setup.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 29 | `V-SLICE8-001` Git Town detection fix | `src/agentops_harness/cli.py`, `src/agentops_harness/profile_setup.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 30 | `V-SLICE8-001` default markdown warning surfacing fix | `src/agentops_harness/profile_setup.py`, `tests/unit/test_cli.py`, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `approved_by_verifier` |
| 31 | final PRD #940 completion review request | handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `revision_requested` |
| 32 | `V-FINAL-003` and `V-FINAL-004` fixes | `src/agentops_harness/prd_preflight.py`, `src/agentops_harness/profile_setup.py`, `src/agentops_harness/cli.py`, `profiles/evonome.example.yaml`, tests, handoff artifacts | `PYTHONPATH=src python3 -m pytest && git diff --check` | `ready_for_verifier` |
