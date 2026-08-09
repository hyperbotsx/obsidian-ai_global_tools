# Coder Handoff — Issue 145 Per-PRD worktree lifecycle

## Task
- GitHub issue / PRD: https://github.com/hyperbotsx/agentops-harness/issues/145
- Branch: `prd/per-prd-worktree-lifecycle-145`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-145`
- PRD status: Approved; CEO approved in canonical issue body.

## Pre-edit status
- `git status --short --branch`: `## prd/per-prd-worktree-lifecycle-145...origin/main`
- Pre-existing dirty files: none.
- Coms isolation preflight: `coder` registry entry exists under `/tmp/agentops/coms/agentops-prd-145`; `verifier` live in the same pool via `coms_list`.

## Scope controls
- Allowed paths: backend worktree provisioning/teardown logic, board/admin UI, Project metadata sync, launch validation/freshness/routing, tests/docs, lease/runtime isolation, migration/backfill, Git Town gated helpers, post-merge lifecycle support.
- Forbidden: PR creation, merge, deploy, PRD approval, implementation auto-start, destructive deletion without safety checks, force push/reset/clean/stash of operator work, secrets/raw transcripts.
- Research-first surfaces: none named by PRD.
- Stop condition: final verifier bug-check approval or human escalation.

## Verifier checkpoints
1. Provisioning checkpoint: deterministic per-PRD worktree and branch creation from latest main.
2. Project metadata checkpoint.
3. Start/resume freshness checkpoint.
4. Launch routing checkpoint.
5. Lease and ownership checkpoint.
6. Runtime isolation checkpoint.
7. Migration/backfill checkpoint.
8. Git Town integration checkpoint.
9. Parallel same-lane checkpoint.
10. Failure-path checkpoint.
11. Post-merge lifecycle trigger checkpoint.
12. Automation UX checkpoint.
13. Idempotency and locking checkpoint.
14. Teardown checkpoint.
15. Recovery/stale dashboard checkpoint.
16. Security/authority checkpoint.
17. Final validation checkpoint.

## Checkpoint 1 — Provisioning

### Implementation summary
- Added `agentops_harness.prd_worktree_provision` with deterministic `agentops-prd-<issue>` path generation.
- Added branch default/validation requiring `prd/` format and exact `-<issue>` suffix for provisioning.
- Added native `git fetch origin main`, `git rev-parse --verify origin/main`, and `git worktree add -b <branch> <path> origin/main` provisioning flow.
- Added safe reuse handling for existing dedicated worktrees only when the branch matches and status is clean.
- Added fail-closed handling for missing repository path, invalid branch names, wrong existing branch, dirty existing worktree, base fetch/resolve failures, and worktree-add failures.
- Added CLI surface: `agentops-harness prd-worktree prepare`.
- Documented the new CLI in `README.md`.
- Addressed verifier finding `F145-R1-001` by reducing the new provisioning result builder to three parameters.

## Checkpoint 2 — Project metadata

### Implementation summary
- Added `agentops_harness.prd_worktree_project` to plan and optionally execute Project text-field updates for `Worktree Path`, `Working Branch`, and `Base Branch`.
- Added fail-closed validation for missing Project IDs, missing field IDs, missing field values, invalid PRD branch format, and branches that do not end with the PRD issue number.
- Added idempotent no-op planning when current Project field values already match the prepared worktree metadata.
- Added ordered `gh project item-edit --text` execution with partial-failure reporting that stops after the first failed field update.
- Added CLI surface: `agentops-harness prd-worktree project-fields`; it plans by default and mutates only with explicit `--execute`.
- Documented the Project field sync command in `README.md`.
- Addressed verifier finding `F145-R3-001` by removing the unused Project field names constant.

## Checkpoint 3 — Start/resume freshness

### Implementation summary
- Added `agentops_harness.prd_worktree_freshness` to run the start/resume freshness gate before launch.
- The gate fetches the configured base ref, records `origin/main` SHA and branch HEAD before/after, validates the current PRD branch and exact issue suffix, checks dirty state, and compares `origin/main` against `HEAD`.
- Fresh branches return `fresh` without merging; stale dirty branches return `stale_dirty` and do not merge.
- Stale clean branches run non-rewriting `git merge --no-edit origin/main`, record `native-git-merge`, and return `fresh` after successful sync.
- Conflicted merges return `sync_conflict_needed` with conflict files from `git diff --name-only --diff-filter=U`.
- Fetch/read/compare/branch failures return `unknown` and fail closed.
- Added CLI surface: `agentops-harness prd-worktree freshness`.
- Documented the freshness command in `README.md`.
- Addressed verifier finding `F145-R5-001` by reducing the freshness result helper to three parameters via a small `FreshnessOutcome` value object.

## Checkpoint 4 — Launch routing

### Implementation summary
- Updated Term Control implementation launch validation to require dedicated `/agentops-prd-<issue>` worktree paths for implementation launches.
- Updated implementation launch validation to require `prd/` branches with exact `-<issue>` suffixes.
- Replaced launch-time destructive reset behavior with the freshness-gate merge behavior: current branch must match, dirty stale worktrees block, stale clean worktrees merge `origin/main`, and wrong/non-PRD branches fail closed instead of switching.
- Launch group startup now attaches freshness evidence to task metadata and writes it into `/tmp/agentops/term-context/<group>/task-context.md` for coder/verifier visibility.
- Updated Term Control tests for dedicated worktree routing, PRD branch validation, non-destructive main merge, dirty fresh/stale blocks, wrong branch refusal, and freshness evidence.
- Addressed verifier finding `F145-R7-001` by checking clean status before returning `fresh` and adding a fresh-dirty launch-block test.

## Checkpoint 5 — Lease and ownership

### Implementation summary
- Added `agentops_harness.prd_worktree_lease` for durable non-secret per-PRD worktree lease records under the harness config root (`worktree-leases/`), outside git worktrees.
- Lease records include PRD issue number, repository, worktree path, branch, base branch, created timestamp, last launch/resume timestamp, last synced `origin/main` SHA, active session identifiers, lifecycle lock state, retention state, artifact folder, PR URL, and merge SHA.
- Added ownership mismatch protection for existing lease reuse based on issue/repo/worktree/branch/base branch.
- Added sensitive-marker validation blocking token/secret/password/credential/auth/cookie/transcript strings in lease payloads.
- Added atomic-ish private writes with `0600` permissions via temp-file replace.
- Added CLI surface: `agentops-harness prd-worktree lease` for create/update/load.
- Added tests proving deterministic pathing, no worktree dirtying, load/reuse, mismatch block, secret marker block, suffix validation, and no raw transcript fields.
- Addressed verifier finding `F145-R9-001` by splitting the oversized PRD worktree CLI parser into subcommand-specific helpers.

## Checkpoint 6 — Runtime isolation

### Implementation summary
- Added `agentops_harness.prd_worktree_runtime` to derive per-PRD runtime identifiers and fail closed for non-dedicated worktrees.
- Runtime resource output includes coms project identity, artifact root, temp dir, cache key, browser profile dir, and deterministic CDP/CDP-proxy/VNC ports.
- Added collision/invalid port guardrails and tests proving different PRDs get distinct ports/cache keys.
- Added Term Control launch integration so implementation launch derives runtime resources before panes start, attaches runtime context to task metadata, exports runtime/browser env values to panes, and uses derived browser ports/profile in Browser QA/frontend MCP setup.
- Strengthened validation so worktree basename must exactly match `agentops-prd-<issue>` and issue 145/1145 port derivation no longer collides.
- Added CLI surface: `agentops-harness prd-worktree runtime`.
- Documented the runtime command in `README.md`.

### Changed files
- `src/agentops_harness/prd_worktree_provision.py`
- `src/agentops_harness/prd_worktree_project.py`
- `src/agentops_harness/prd_worktree_freshness.py`
- `src/agentops_harness/prd_worktree_lease.py`
- `src/agentops_harness/prd_worktree_runtime.py`
- `src/agentops_harness/cli.py`
- `term-control-center/server/implementationWorktreeSync.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/frontendBrowserLaunch.ts`
- `term-control-center/server/runtimeIsolation.ts`
- `term-control-center/shared/launcher.ts`
- `tests/unit/test_prd_worktree_provision.py`
- `tests/unit/test_prd_worktree_project.py`
- `tests/unit/test_prd_worktree_freshness.py`
- `tests/unit/test_prd_worktree_lease.py`
- `tests/unit/test_prd_worktree_runtime.py`
- `term-control-center/tests/implementationWorktreeSync.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/runtimeIsolation.test.ts`
- `README.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r1-provisioning.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r2-f145-r1-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r3-project-metadata.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r4-f145-r3-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r5-freshness.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r6-f145-r5-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r7-launch-routing.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r8-f145-r7-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r9-lease-ownership.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r10-f145-r9-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r11-runtime-isolation.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r12-f145-r11-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r13-f145-r12-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r14-remaining-lifecycle.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r15-f145-r14-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r16-f145-r15-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r17-human-decision-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r18-f145-r17-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r19-f145-r18-fix.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-145-per-prd-worktree-lifecycle/review-request-r20-f145-fbc-001.json`

### Validation
- `python -m pytest tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q` — failed: `python` not found in environment.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q` — pass, 59 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_provision.py tests/unit/test_prd_preflight.py -q && git diff --check` — pass, 23 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_provision.py tests/unit/test_prd_preflight.py tests/unit/test_cli.py -q && git diff --check` — pass, 74 tests.
- `PYTHONPATH=src python3 -m agentops_harness.cli prd-worktree prepare --help | head -40` — pass.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_provision.py tests/unit/test_prd_preflight.py tests/unit/test_cli.py -q && git diff --check` — pass, 74 tests after `F145-R1-001` fix.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 66 tests.
- `PYTHONPATH=src python3 -m agentops_harness.cli prd-worktree project-fields --help | head -60` — pass.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 66 tests after `F145-R3-001` fix.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 73 tests.
- `PYTHONPATH=src python3 -m agentops_harness.cli prd-worktree freshness --help | head -50` — pass.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 73 tests after `F145-R5-001` fix.
- `npm --prefix term-control-center ci` — pass; installed ignored local Node dependencies for validation.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/implementationWorktreeSync.test.ts tests/launcher.test.ts` — pass, 36 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/implementationWorktreeSync.test.ts tests/launcher.test.ts && npm run typecheck && cd .. && git diff --check` — pass, 37 tests after `F145-R7-001` fix, TypeScript typecheck, and diff whitespace check.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_lease.py tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 81 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_lease.py tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 81 tests after `F145-R9-001` fix.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_runtime.py tests/unit/test_prd_worktree_lease.py tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && git diff --check` — pass, 86 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_runtime.py tests/unit/test_prd_worktree_lease.py tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && cd term-control-center && node --import tsx --test --test-concurrency=1 tests/runtimeIsolation.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts && npm run typecheck && cd .. && git diff --check` — pass, 87 Python tests, 41 Term Control tests, typecheck, and diff whitespace check after `F145-R11-001` fix.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/runtimeIsolation.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts && npm run typecheck && cd .. && git diff --check` — pass, 41 Term Control tests, typecheck, and diff whitespace check after `F145-R12-001` fix.
- `cd term-control-center && npm run typecheck` — pass.
- `git diff --check` — pass after Term Control changes.

## Reviews / findings
- Verifier R1: `revision_requested`, finding `F145-R1-001`.
- Verifier R2: `approved`, open findings 0.
- Verifier R3: `revision_requested`, finding `F145-R3-001`.
- Verifier R4: `approved`, open findings 0.
- Verifier R5: `revision_requested`, finding `F145-R5-001`.
- Verifier R6: `approved`, open findings 0.
- Verifier R7: `revision_requested`, finding `F145-R7-001`.
- Verifier R8: `approved`, open findings 0.
- Verifier R9: `revision_requested`, finding `F145-R9-001`.
- Verifier R10: `approved`, open findings 0.
- Verifier R11: `revision_requested`, finding `F145-R11-001`.
- Verifier R12: `revision_requested`, finding `F145-R12-001`.
- Verifier R13: `approved`, open findings 0.

## Findings addressed
- `F145-R1-001`: Reduced `build_result` from five parameters to three by deriving worktree path and resolved branch from `ProvisionRequest` inside the helper.
- `F145-R3-001`: Removed unused `PROJECT_FIELD_NAMES` constant from `prd_worktree_project.py`.
- `F145-R5-001`: Reduced freshness `result` helper from five parameters to three by grouping status/current/errors in `FreshnessOutcome`.
- `F145-R7-001`: Fresh implementation worktrees now run the same dirty tracked/untracked status guard before launch; added `syncImplementationWorktree refuses dirty fresh PRD worktrees` coverage.
- `F145-R9-001`: Split `add_prd_worktree_parser()` into short subcommand-specific parser helpers.
- `F145-R11-001`: Wired runtime resource derivation into Term Control launch, applied derived browser env/profile/ports, enforced exact worktree basename, and removed issue modulo port collisions.
- `F145-R12-001`: Reused `runtimeEnv()` from `launchPlan.ts` to remove duplicate runtime env mapping and make the helper live.

## Checkpoints 7–16 — Remaining lifecycle and guardrails

### Implementation summary
- Added migration/backfill support with `agentops_harness.prd_worktree_migration` and `agentops-harness prd-worktree migrate`; it prepares dedicated worktree metadata and Project field updates without auto-starting agents.
- Updated Git Town gating to require compatible `>=23.0.3`, prefer only non-interactive sync/propose helper commands, remove `ship` from preferred commands, and keep native git worktree as provisioning/removal source of truth.
- Added parallel same-lane coverage proving PRD issue numbers produce unique `agentops-prd-<issue>` paths.
- Hardened teardown branch cleanup by removing force-delete fallback; local branch deletion now blocks instead of `git branch -D` when normal safe delete fails.
- Added post-merge lifecycle orchestration with closeout planning, teardown execution, required merge/sync/verifier evidence checks, artifact-preserving teardown path, cleanup-needed state, and lifecycle lock guard.
- Added stale/recovery listing with `agentops_harness.prd_worktree_recovery` and `agentops-harness prd-worktree recovery`; it lists stale/recoverable leases without deleting anything.
- Added docs/README command examples for migration, recovery, and post-merge lifecycle.

### Additional changed files
- `src/agentops_harness/git_town.py`
- `src/agentops_harness/post_merge_teardown.py`
- `src/agentops_harness/prd_worktree_migration.py`
- `src/agentops_harness/prd_worktree_lifecycle.py`
- `src/agentops_harness/prd_worktree_recovery.py`
- `tests/unit/test_git_town.py`
- `tests/unit/test_post_merge_teardown.py`
- `tests/unit/test_prd_worktree_migration.py`
- `tests/unit/test_prd_worktree_lifecycle.py`
- `tests/unit/test_prd_worktree_recovery.py`

### Revision 15 fixes for verifier findings
- `F145-R14-001`: migration now has plan-vs-execute semantics; plan-only returns blocked readiness, `--execute` runs Project field mutations, lease write failures block readiness, and mismatched existing leases have regression coverage.
- `F145-R14-002`: post-merge lifecycle now parses verifier report Machine Status JSON, requires `decision=approved`, requires passed/approved bug-check status, requires verified closeout/noop, and requires synced main SHA to match merge SHA before teardown runs.
- `F145-R14-003`: teardown now checks active sessions, worktree cleanliness, and local branch safety before destructive branch deletion; dirty/active-session/unmerged branch tests assert no remote/local deletion and no worktree removal where applicable.
- `F145-R14-004`: lifecycle lock acquisition now uses atomic exclusive create, reads lease active-session/lock state before teardown, passes active-session evidence to teardown, and preserves `cleanup_needed` retention after failed teardown.
- `F145-R14-005`: production helper parameter-count issues were removed; teardown helpers were split into `tests/unit/post_merge_teardown_helpers.py` so `test_post_merge_teardown.py` is below 300 lines.

### Revision 17 fixes after human decision
- `F145-R14-002`: `post-merge-lifecycle` now uses `read_live_closeout()` before closeout mutation, validates live PR merge/base/head state, supports already-complete closeout as noop, requires Project closeout config, then runs `execute_closeout()` with live GitHub mutation/readback before teardown; the prior `--closeout-verified` self-attestation path was removed from CLI usage.
- `F145-R14-004`: Term Control implementation launch sync now reads the per-PRD lease from `AGENTOPS_HARNESS_CONFIG` and fails closed on `lifecycle_lock=locked` or `retention_state=cleanup_needed`.
- `F145-R14-005`: `post_merge_teardown.py` is under 300 lines, teardown/lifecycle tests are split into helper modules, and Python helper functions remain within KISS line/parameter limits.

### Additional validation
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_worktree_migration.py tests/unit/test_prd_worktree_recovery.py tests/unit/test_prd_worktree_lifecycle.py tests/unit/test_git_town.py tests/unit/test_post_merge_teardown.py tests/unit/test_prd_worktree_runtime.py tests/unit/test_prd_worktree_lease.py tests/unit/test_prd_worktree_freshness.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_worktree_provision.py tests/unit/test_cli.py -q && cd term-control-center && node --import tsx --test --test-concurrency=1 tests/runtimeIsolation.test.ts tests/implementationWorktreeSync.test.ts tests/launcher.test.ts && npm run typecheck && cd .. && git diff --check` — pass, 127 Python tests, 43 Term Control tests, typecheck, and diff whitespace check.

## Known risks / notes
- Implementation for checkpoints 1 through 16 is present. Verifier approved checkpoints 1–6 earlier, approved checkpoints 7–16 at revision 19, steward approved with no findings, and final verifier bug-check passed at revision 20. PRD #145 implementation is verified and PR-ready pending human PR authorization.
- No GitHub Project fields were mutated.
- No production worktrees or branches were created during validation; provisioning behavior is covered by injected-runner/unit and temp-git tests.
