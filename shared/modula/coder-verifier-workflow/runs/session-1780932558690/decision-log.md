# Decision Log

## 2026-06-08T15:33:43Z — PRD intake

- Source PRD: https://github.com/hyperbotsx/SoldierOne/issues/940
- PRD issue: 940
- Agent label: `agent:evonome-admin`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-harness`
- Branch: `prd/worktree-branch-ownership-enforcement-940`
- Pre-existing dirty files: none from `git status --short --branch`
- Preview target: not configured for this worktree
- Browser QA / DevTools: not required for Checkpoint 1 because this is CLI/docs policy work

## Scope confirmation

Allowed paths for Checkpoint 1:

- `src/agentops_harness/` ownership policy code
- `tests/unit/` ownership policy tests
- `docs/` workflow documentation
- `profiles/evonome.example.yaml` documented example mapping
- `README.md` command listing if a CLI surface is added
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/` handoff artifacts

Forbidden paths:

- Product application code, routes, navigation, deployment config, raw transcripts, secrets, local machine profiles outside explicit test tempdirs, and unrelated workflow areas

Validation commands:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_ownership.py tests/unit/test_cli.py`
- `git diff --check`

Stop condition:

- Checkpoint 1 is ready when mapping and branch naming policy are implemented, documented, tested, and handed off for verifier review.

Checkpoint plan:

1. Mapping and branch naming policy review.
2. Preflight fail-closed behavior review.
3. Coder/verifier metadata integration review.
4. Final authority-boundary bug-check and evidence review.

## 2026-06-08T15:40:07Z — Checkpoint 1 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next checkpoint: Checkpoint 2 preflight fail-closed behavior review

## 2026-06-08T15:44:01Z — Checkpoint 2 implementation

- Added deterministic PRD preflight core and CLI command.
- Preflight blocks missing labels, conflicting labels, missing issue number, wrong worktree, missing expected worktree, PRD-numberless branches, unknown dirty files, and ephemeral files without clean handling.
- Configured ephemeral artifacts can continue only when clean-ephemeral handling is enabled.
- Browser QA remains not required because changes are CLI/docs/tests only.

## 2026-06-08T15:48:19Z — Checkpoint 2 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next checkpoint: Checkpoint 3 coder/verifier metadata integration review

## 2026-06-08T15:51:06Z — Checkpoint 3 implementation

- Added coder/verifier metadata validation for PRD number, branch, worktree, agent label, checkpoint, and preflight status.
- Extended handoff mirror metadata events with agent label and preflight status.
- Added CLI validation command and tests for coder handoff and verifier report artifacts.
- Browser QA remains not required because changes are CLI/docs/tests only.

## 2026-06-08T15:55:21Z — Checkpoint 3 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-CP3-001`
- Required fix: prevent stale verifier reports from passing metadata validation or emitting false current-checkpoint mirror events.

## 2026-06-08T15:56:56Z — Checkpoint 3 revision 4

- Metadata validation now uses report-local checkpoint fields for verifier reports.
- Verifier report validation requires report-local Machine Status fields and compares report checkpoint/revision to sibling coder-ready when present.
- Handoff mirror event construction now preserves verifier-report-local checkpoint truth instead of inherited handoff checkpoint.
- Added stale-report regression tests.

## 2026-06-08T16:01:47Z — Checkpoint 3 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next checkpoint: final authority-boundary bug-check and evidence review

## 2026-06-08T16:02:26Z — Final checkpoint readiness

- Re-ran full unit suite and whitespace validation.
- Prepared final authority-boundary evidence for verifier review.
- Remaining broader PRD areas are documented as known gaps because this implementation followed the three explicit verifier checkpoints from the PRD.

## 2026-06-08T16:06:38Z — Final verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-FINAL-001`, `V-FINAL-002`
- `V-FINAL-002` is bounded and actionable in code.
- `V-FINAL-001` requires either implementing remaining PRD acceptance criteria or explicit human rescope.

## 2026-06-08T16:07:37Z — Final revision 6 and human escalation

- Fixed `V-FINAL-002` by preventing verifier-report mirror events from inheriting checkpoint when report-local `Checkpoint reviewed` is missing.
- Added regression coverage for missing report-local checkpoint mirror events.
- Validation passed: targeted mirror/metadata/CLI tests, full tests, and `git diff --check`.
- `V-FINAL-001` remains a scope decision and is escalated to the human.

## 2026-06-08T16:19:58Z — Human decision to continue remaining criteria step by step

- Human asked to continue step by step.
- Implemented next bounded slice: local profile init/loading and validation.
- Added `agentops-harness init` for generated and non-interactive config-file profile setup.
- Added simple profile loading and `prd-preflight --profile` mapping usage.
- Profile setup writes to config-root profiles, validates configured paths and preview URLs, and skips preview/archive/historical/temp worktree candidates.
- Remaining `V-FINAL-001` areas after this slice: actual ephemeral cleanup, Git Town probing, manual session adoption, post-merge sync, merge-conflict validation, and parallel-plan classification.

## 2026-06-08T16:25:09Z — Slice 1 verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-SLICE1-001`, `V-SLICE1-002`
- Required fixes: block missing worktrees root/implementation override paths and make profile-backed preflight consume profile preview URLs and AgentOps Harness admin override.

## 2026-06-08T16:27:22Z — Slice 1 revision 8

- Added root existence validation and implementation override path validation.
- Added profile preview URL override support in PRD preflight.
- Added profile AgentOps Harness admin implementation override support in PRD preflight.
- Added regression tests for the verifier findings.

## 2026-06-08T16:30:50Z — Slice 1 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T16:33:12Z — Slice 2 implementation

- Implemented actual configured ephemeral artifact cleanup for PRD preflight.
- Tracked ephemeral artifacts are restored with `git restore`.
- Untracked ephemeral artifacts are removed.
- Unknown dirty paths remain blocked by preflight.
- Added unit and CLI tests for cleanup behavior.

## 2026-06-08T16:36:48Z — Slice 2 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE2-001`
- Required fix: make CLI fail closed when cleanup fails instead of reporting successful preflight.

## 2026-06-08T16:37:23Z — Slice 2 revision 10

- `prd-preflight --clean-ephemeral` now returns blocked/nonzero when cleanup returns errors.
- Cleanup errors are included in the rendered preflight result.
- Added CLI regression test for tracked restore failure.

## 2026-06-08T16:40:07Z — Slice 2 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T16:41:49Z — Slice 3 implementation

- Implemented read-only Git Town availability/configuration check.
- Added `agentops-harness git-town-check` markdown/json command.
- Check reports preferred Git Town commands when configured and fail-closed fallback explanation when unavailable or misconfigured.
- Added unit and CLI tests for configured, unavailable, misconfigured, and missing-worktree cases.

## 2026-06-08T16:46:22Z — Slice 3 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE3-001`
- Required fix: use installed Git Town CLI-compatible `git town --version` probe instead of unsupported `git town version`.

## 2026-06-08T16:46:56Z — Slice 3 revision 12

- Updated Git Town availability probe to `git town --version`.
- Updated tests for the command shape.
- Verified real `agentops-harness git-town-check --worktree . --format json` returns `status=ok` in this configured worktree.

## 2026-06-08T16:49:27Z — Slice 3 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T16:51:25Z — Slice 4 implementation

- Implemented manual session `adopt` and `refresh` validation commands.
- Adoption validates worktree existence, PRD-numbered branch naming, branch existence/current branch, and required coder/verifier evidence.
- Added unit and CLI tests for valid adoption, wrong branch, missing evidence, refresh, and markdown error output.

## 2026-06-08T16:55:13Z — Slice 4 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE4-001`
- Required fix: adoption must fail closed when handoff evidence metadata contradicts requested branch/worktree/session.

## 2026-06-08T16:56:04Z — Slice 4 revision 14

- Adoption now parses coder handoff branch/worktree metadata and compares it to requested session values.
- Adoption blocks missing handoff branch/worktree metadata.
- Added regression tests for mismatched handoff branch and missing handoff metadata.

## 2026-06-08T16:58:22Z — Slice 4 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE4-001` still open for mismatched PRD issue metadata.
- Required fix: adoption must fail closed when handoff PRD/GitHub issue metadata contradicts requested issue.

## 2026-06-08T16:59:16Z — Slice 4 revision 15

- Adoption now parses handoff PRD/GitHub issue metadata and compares it to requested `--issue`.
- Adoption blocks missing or contradictory PRD issue metadata.
- Added regression test for mismatched handoff issue.

## 2026-06-08T17:01:27Z — Slice 4 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE4-001` still open for mixed GitHub issue/PRD issue metadata.
- Required fix: adoption must parse explicit handoff issue fields and reject contradictory issue metadata.

## 2026-06-08T17:02:23Z — Slice 4 revision 16

- Adoption now requires both `GitHub issue` and `PRD` handoff fields to be present and consistent.
- Adoption rejects mixed issue metadata before adopting or refreshing a manual session.
- Added regression test for contradictory handoff issue fields.

## 2026-06-08T17:05:09Z — Slice 4 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE4-001` still open for unparseable required issue metadata.
- Required fix: adoption must treat unparseable explicit issue fields as invalid evidence.

## 2026-06-08T17:05:58Z — Slice 4 revision 17

- Adoption now rejects unparseable `GitHub issue` or `PRD` handoff fields.
- Added regression test for unparseable PRD issue field.

## 2026-06-08T17:08:43Z — Slice 4 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T17:11:03Z — Slice 5 implementation

- Implemented post-merge local main/dev-main sync verification/apply command.
- Command blocks missing targets, dirty targets, and targets whose HEAD does not match expected GitHub main commit.
- `--apply` runs fetch, checkout main, and pull --ff-only before verification.
- Added unit and CLI tests for verified, dirty, wrong commit, and apply paths.

## 2026-06-08T17:15:15Z — Slice 5 verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-SLICE5-001`, `V-SLICE5-002`
- Required fixes: support profile-backed sync targets; require commit-shaped expected commit; fail closed on git command failures.

## 2026-06-08T17:17:44Z — Slice 5 revision 19

- `post-merge-sync` now supports `--profile` targets with explicit path overrides.
- Expected commit must be a non-empty commit SHA.
- Non-git targets and failed git status commands block instead of false-verifying.
- Apply mode stops after first sync command failure.
- Added regression tests for profile targets, empty expected commit, non-git targets, and fetch failure ordering.

## 2026-06-08T17:21:16Z — Slice 5 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T17:22:55Z — Slice 6 implementation

- Implemented merge-conflict ownership validation command.
- Command validates owning worktree exists, branch includes PRD issue number, conflicted files are provided, and risky conflict files require verifier review.
- Added unit and CLI tests for valid, wrong branch, missing worktree, risky files, and markdown output.

## 2026-06-08T17:26:17Z — Slice 6 verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-SLICE6-001`, `V-SLICE6-002`
- Required fixes: compare the worktree against explicit owner evidence and verify the actual current git branch.

## 2026-06-08T17:27:31Z — Slice 6 revision 21

- Added `--expected-worktree` ownership evidence to merge-conflict check.
- Merge-conflict validation now blocks wrong existing directories, missing expected owner evidence, non-git worktrees, and current branch mismatches.
- Added regression tests for wrong existing worktree and branch mismatch.

## 2026-06-08T17:31:17Z — Slice 6 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T17:32:45Z — Slice 7 implementation

- Implemented parallel PRD plan classification command.
- Plans declare issue, worktree, branch, and path scope with `issue|worktree|branch|path1,path2` syntax.
- Classification requires coordination for missing plan data, branch names without issue numbers, shared worktrees, shared branches, and overlapping paths.
- Added unit and CLI tests for compatible plans, conflicts, invalid specs, and markdown/json output.

## 2026-06-08T17:35:45Z — Slice 7 verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-SLICE7-001`, `V-SLICE7-002`, `V-SLICE7-003`
- Required fixes: use PRD-required classifications, detect parent/child and high-risk path overlap, and validate PRD branches robustly.

## 2026-06-08T17:37:01Z — Slice 7 revision 23

- Parallel plan status now uses `safe_parallel`, `parallel_with_coordination`, and `sequential_recommended`.
- Added parent/child path overlap and high-risk shared-area detection.
- Reused PRD branch validation to reject substring and non-`prd/` branch false positives.
- Added regression tests for parent/child overlap, high-risk paths, substring branch false positives, and missing `prd/` prefix.

## 2026-06-08T17:39:54Z — Slice 7 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE7-002` remains partially resolved.
- Required fix: include dependency manifests/lockfiles and build/test/deployment config in high-risk shared-area detection.

## 2026-06-08T17:40:25Z — Slice 7 revision 24

- Expanded high-risk detection to include `package.json`, lockfiles, common JS/TS build config files, Docker config, TypeScript config, and generic config suffixes.
- Added regression tests for `package.json` and `vite.config.ts`.

## 2026-06-08T17:42:48Z — Slice 7 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE7-002` remains partially resolved for common Python dependency, CI, and deployment config variants.

## 2026-06-08T17:43:23Z — Slice 7 revision 25

- Expanded high-risk detection to include Python dependency/lock files, GitHub workflow config, Docker compose YAML variants, and Dockerfile variants.
- Added regression tests for `requirements.txt`, `.github/workflows/ci.yml`, and `Dockerfile.dev`.

## 2026-06-08T17:47:13Z — Slice 7 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE7-002` remains partially resolved for paper/live behavior, shared model, component, and chart paths.

## 2026-06-08T17:47:50Z — Slice 7 revision 26

- Expanded high-risk detection to include paper/live behavior, model, component, and chart path segments.
- Added regression tests for paper/live behavior and shared model/component/chart paths.

## 2026-06-08T17:49:37Z — Slice 7 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder for next remaining `V-FINAL-001` slice.

## 2026-06-08T17:51:43Z — Slice 8 implementation

- Added `agentops-harness init --interactive` prompt flow.
- Interactive init asks for profile name, worktrees root, and confirmation before writing a local profile.
- Added CLI tests for accepting defaults and canceling the write.

## 2026-06-08T17:55:32Z — Slice 8 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE8-001`
- Required fix: interactive init must let humans configure worktree mappings, preview URLs, post-merge sync targets, and Git Town preference/detection with validation before writing.

## 2026-06-08T17:58:08Z — Slice 8 revision 28

- Interactive init now prompts through worktree mappings, preview URLs, post-merge sync targets, Git Town preference, and final write confirmation.
- Interactive init validates configured values before writing and fails closed on invalid overrides.
- Added tests for full default prompt flow, cancellation, and invalid preview override.

## 2026-06-08T18:02:47Z — Slice 8 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE8-001` remains open for missing Git Town detection in the interactive wizard.

## 2026-06-08T18:03:46Z — Slice 8 revision 29

- Interactive init now runs Git Town detection for each selected worktree before writing.
- Git Town detection statuses are surfaced in profile init warnings.
- Added regression test proving detection runs for all selected worktrees and appears in output.

## 2026-06-08T18:06:33Z — Slice 8 verifier revision request

- Verifier decision: `revision_requested`
- Finding: `V-SLICE8-001` remains open because default markdown output omitted Git Town detection warnings.

## 2026-06-08T18:07:08Z — Slice 8 revision 30

- Profile init markdown now renders warnings.
- Added regression test that default interactive markdown output shows Git Town detection statuses.

## 2026-06-08T18:08:58Z — Slice 8 verifier approval

- Verifier decision: `approved`
- Open findings: `0`
- Next actor: coder to prepare final PRD #940 completion review.

## 2026-06-08T18:09:07Z — Final completion review request

- All bounded `V-FINAL-001` slices are verifier-approved.
- Full validation rerun: `PYTHONPATH=src python3 -m pytest && git diff --check` passed with 256 tests.
- Requested final verifier review for PRD #940 completion.

## 2026-06-08T18:13:47Z — Final completion verifier revision request

- Verifier decision: `revision_requested`
- Findings: `V-FINAL-003`, `V-FINAL-004`
- Required fixes: enforce `--show-preview-target` when no preview mapping exists and add profile-backed ephemeral artifact config.

## 2026-06-08T18:16:27Z — Final completion revision 32

- `prd-preflight --show-preview-target` now fails closed when no preview URL is configured.
- Local profiles now include `ephemeral_globs`, render/load that field, and generated profiles include the coder/verifier run artifact pattern.
- Profile-backed preflight now combines profile ephemeral globs with CLI `--ephemeral-glob` values.
- Updated example profile and added regression tests for preview target enforcement, profile-backed ephemeral globs, and mixed dirty fail-closed behavior.
