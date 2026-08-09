# Coder Handoff — Issue #48 Project-Scoped Pi Agent Memory Banks

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/48
- Branch: `prd/project-scoped-pi-agent-memory-banks-48`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Pre-edit state
- `git status --short --branch`: `## prd/project-scoped-pi-agent-memory-banks-48...origin/main`
- Pre-existing dirty files: none.
- Issue state/labels: open PRD with `status:approved`.
- Implementation preflight: worktree root and remote match `hyperbotsx/agentops-harness`; branch ends in `-48`; worktree was clean before edits.

## Allowed paths / scope
- `docs/` for provider-selection, setup, rollback, safety, reset/export, and troubleshooting docs.
- `term-control-center/server/`, `term-control-center/shared/`, `term-control-center/src/`, and `term-control-center/tests/` for memory config schema, admin APIs/UI, launch/session metadata, doctor/isolation tests, reset/export controls, and tests.
- `pipeline-diagram/` only if launch payloads or visible metadata need project memory context.
- `src/agentops_harness/` and `tests/unit/` only for implementation preflight/profile/approval-review hardening required by this issue.
- Run artifacts under this folder.

## Forbidden scope
- No third-party Pi package install/update without reviewed implementation approval.
- No global memory injection, cloud memory sync, cross-project recall, raw transcript persistence, secrets, credentials, tokens, cookies, or identity headers.
- No repo-local memory data unless explicitly configured, path-validated, gitignored, and shown in admin.
- No hardcoded Project 2, tracker `#862`, one repository, one worktree, or local-only path defaults where active project/profile state should be used.
- No PR creation, merge, deployment, infrastructure mutation, trading, backtesting, or PRD approval.

## Required validation
- `python3 -m pytest tests`
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run test`
- `npm --prefix term-control-center run build`
- `git diff --check`

## Mandatory research refresh
Completed via researcher consult on 2026-06-20 before implementation edits.
- Selected MVP provider: `@samfp/pi-memory@1.5.0`, because it has no npm `engines` constraint, supports `localPath`, and provides direct search/write tools. AgentOps must force `perTurnInjection: false` and verify bounded one-shot startup injection during the provider gate because the package default is per-turn injection.
- Fallback: `pi-persistent-intelligence@0.11.2` for stricter governance, secret scanning/redaction, tombstones, strict mode, and privacy purge.
- Rejected for MVP: `pi-total-recall@1.8.1`, because it requires Node 24+ while `scripts/agentops/pi-agent.sh` pins Node v22.22.3, and session-search indexes the global Pi session store unless project filters are enforced.
- Pi package behavior: `pi install -l` writes project `.pi/settings.json`; project packages install under `.pi/npm/`; project package identity overrides same global package identity.
- Sources cited by Researcher: https://pi.dev/packages/@samfp/pi-memory, https://pi.dev/packages/pi-total-recall, https://github.com/Mont3ll/pi-persistent-intelligence, Pi package/settings docs.

## Checkpoint plan
1. Research/provider checkpoint: provider choice and fallback are documented with runtime/isolation/install/rollback/safety findings.
2. Memory model checkpoint: project ID, memory root, config schema, path validation, doctor/export/reset primitives.
3. Launch checkpoint: sessions receive only selected-project memory config, advisory policy, warnings, and metadata.
4. Admin checkpoint: project-scoped memory settings/status plus enable/disable/doctor/isolation/export/reset controls.
5. Isolation checkpoint: A/B leakage, disabled memory, missing provider, bad path, wrong-project launch, reset/export scope tests.
6. Safety checkpoint: redaction/blocking, no global/cloud/cross-project recall, memory-as-advisory policy, package gate docs.
7. Profile/project checkpoint: CEO/Approval Review and launch preflight remain active-project/profile-based with no hardcoded Project 2/tracker `#862` mutation plans.
8. Steward hygiene review, then final verifier bug-check.

## Current checkpoint
- Final verifier bug-check approved at revision 15. Stop condition met.

## Implementation summary — checkpoint 1
- Added `docs/agentops-project-memory.md` documenting the provider gate, selected provider, fallback, launch policy, storage policy, install command, rollback command, and forced `perTurnInjection: false` requirement for `@samfp/pi-memory`.
- No third-party package was installed or enabled.

## Implementation summary — checkpoint 2
- Added `term-control-center/server/projectMemory.ts` with the project memory config schema, default per-project state root, provider pin/settings adapter, root validation, doctor health checks, redaction, scoped write/search/export/reset helpers, and fail-closed flags for per-turn injection, cross-project recall, and cloud sync.
- Added `term-control-center/server/adminProjectMemory.ts` plus authenticated admin routes for memory detail/update/doctor/isolation-test/export/reset under `/api/admin/projects/:id/memory`.
- Extended project registry records with a `memory` object while preserving existing active-project settings updates.
- Added `term-control-center/tests/projectMemory.test.ts` for default roots, unsafe flags, repo-local gitignore enforcement, scoped search/export/reset, secret redaction, and provider gate settings.
- Updated `docs/agentops-project-memory.md` with the memory schema and route-level model.

## Revision 4 fixes for checkpoint 2 findings
- `V48-CP2-001`: `updateProject()` now preserves existing memory config when ordinary project settings edits omit `memory`; regression coverage added.
- `V48-CP2-002`: create/update/memory-update paths reject duplicate memory roots across project IDs; isolation checks fail on duplicate roots and check every other project; regression coverage added for duplicate roots.
- `V48-CP2-003`: `pi-persistent-intelligence` fallback settings now use `governance.mode: strict` and `retrieval.injectionMode: wakeup`; regression coverage asserts the shape.
- `V48-CP2-004`: admin route registration is split into asset/auth/project/memory/utility helpers while keeping existing auth/CSRF guards.

## Implementation summary — checkpoint 3
- Added `MemoryLaunchConfig` to the shared launch task context.
- Added server-side selected-project launch resolution for implementation, planning, and authoring sessions; implementation launches now attach memory from the configured project and reject repository/worktree mismatches when project config exists.
- Launch prompts, task context files, and pane environments now include memory provider/root/enabled/isolation/warnings and the memory-as-advisory policy.
- Tmux and PTY launch paths receive `AGENTOPS_MEMORY_*` environment variables.
- Added launch tests for advisory memory prompt/env metadata and selected-project memory resolution.
- Updated docs with launch resolution behavior and `AGENTOPS_MEMORY_*` metadata.

## Implementation summary — checkpoint 4
- Added a Memory settings fieldset to the admin project editor showing enabled state, provider, root, repo-local opt-in, health, and export/isolation output.
- Added `term-control-center/server/adminMemoryClient.ts` and composed it into admin assets so the admin UI can save memory settings, run doctor/isolation checks, export, and reset via authenticated project-scoped APIs.
- Wired admin project load/open/save/new flows to populate memory UI without including memory in ordinary project settings saves.
- Added admin tests for visible memory settings, client asset hooks, auth/CSRF protection, doctor/export/reset routes, and project-scoped memory updates.
- Updated docs with admin visibility and controls.

## Implementation summary — checkpoint 5
- Added regression coverage that the memory isolation primitive checks every configured peer project and finds no sentinel in other project roots.
- Added wrong-project launch coverage for repository and worktree mismatches when project config exists.
- Added unsupported provider rejection coverage and retained bad path, disabled/default memory, missing-provider doctor warning, A/B search, export, and reset scope coverage.
- Ran the combined admin/launch/memory test subset to exercise the isolation and admin paths together.

## Revision 8 fix for checkpoint 5 finding
- `V48-CP5-001`: default memory config now has explicit disabled coverage and `writeMemoryCheckpoint()` is asserted to reject disabled memory writes.

## Implementation summary — checkpoint 6
- Added safety docs covering rejected per-turn injection, cross-project recall, cloud sync, unsupported providers, bad roots, non-gitignored repo-local roots, write redaction, and launch-time disabling for errored memory.
- Added tests that per-turn injection is rejected, disabled memory writes are blocked, errored enabled memory is disabled at launch with a warning, and secret-like values are redacted from exported memory.
- Retained launch prompt tests proving memory is advisory and current PRD/repo/config/GitHub/verifier evidence win.

## Evidence summary — profile/project checkpoint
- Existing CEO Review answer tests cover active Project 3 metadata and assert answers do not include hardcoded `Project 2` or `#862` where selected project/profile state should be used.
- Existing PRD preflight tests cover approved issue state, repository matching, branch suffix, wrong worktree, and dirty-risk fail-closed behavior.

## Revision 12 fix for implementation preflight finding
- `V48-CP9-001`: implementation launch validation now requires both canonical approved status and the `status:approved` label before launch.
- `V48-CP9-001`: launch plan construction now rejects implementation launches when the target worktree is dirty before any panes are started.
- Added launch-path regression coverage for unapproved issue state and dirty-risk worktrees, plus updated launch fixtures to start from clean git state.

## Revision 13 fix for implementation preflight finding
- `V48-CP9-002`: pipeline board generation now keeps the full issue label list on PRD chips, so launch metadata includes canonical `status:approved` issue labels.
- `V48-CP9-002`: board task payloads prefer the label-derived chip `status` before Project `Status`/`Pipeline Status`, preserving valid Project 3 launches whose project status is `Todo`.
- Added regression coverage that a Project 3 chip with `projectStatus: Todo` keeps `status: approved` and `labels: ['status:approved']`, plus a static board payload guardrail.

## Revision 15 fixes for final bug-check findings
- `V48-FBC-001`: legacy active settings saves now validate preserved memory against the new settings before persisting, and implementation/authoring launch resolution revalidates persisted project memory before exposing launch metadata.
- `V48-FBC-001`: added regression coverage that stale repo-local memory roots are rejected during legacy settings save and again at launch if an invalid registry record exists.
- `V48-FBC-002`: enabled memory without health now initializes to warning health (`memory doctor has not passed`) and launch metadata disables explicit disabled health instead of reporting enabled+disabled.
- `V48-FBC-002`: added regression coverage for enabled memory without health producing warning launch metadata.

## Changed files
- `docs/agentops-project-memory.md`
- `pipeline-diagram/board.html`
- `pipeline-diagram/generate.py`
- `term-control-center/shared/launcher.ts`
- `term-control-center/server/projectMemory.ts`
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminProjects.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/adminAssets.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminClient.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/tmuxSupervisor.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/completion-server.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/server.test.ts`
- `tests/unit/test_pipeline_board_generation.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-48-project-scoped-pi-memory/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-48-project-scoped-pi-memory/review-request-r1-provider-research.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-48-project-scoped-pi-memory/review-request-r2-provider-research-fix.json`

## Validation results
- `git diff --check`: passed.
- `npm --prefix term-control-center test`: passed, 243 tests.
- `npm --prefix term-control-center run build`: passed; Vite emitted the existing non-blocking chunk-size warning.
- `npm --prefix term-control-center run typecheck`: passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts tests/admin.test.ts tests/server.test.ts`: passed, 62 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts tests/launcher.test.ts tests/server.test.ts`: passed, 82 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launcher.test.ts tests/launchPlan.test.ts tests/server.test.ts tests/completion-server.test.ts`: passed, 73 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_ceo_review_answers.py tests/unit/test_prd_preflight.py tests/unit/test_pipeline_board_generation.py`: passed, 31 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_prd_preflight.py`: passed, 17 tests.
- `python3 -m py_compile pipeline-diagram/generate.py tests/unit/test_pipeline_board_generation.py`: passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py`: passed, 15 tests.

## Verifier status
- Checkpoint 1 revision 1 requested fix: `V48-CP1-001`.
- Checkpoint 1 revision 2 approved.
- Checkpoint 2 revision 3 requested fixes: `V48-CP2-001`, `V48-CP2-002`, `V48-CP2-003`, `V48-CP2-004`.
- Checkpoint 2 revision 4 approved.
- Checkpoint 3 revision 5 approved.
- Checkpoint 4 revision 6 approved.
- Checkpoint 5 revision 7 requested fix: `V48-CP5-001`.
- Checkpoint 5 revision 8 approved.
- Checkpoint 6 revision 9 approved.
- Profile/project checkpoint revision 10 approved.
- Implementation preflight checkpoint revision 11 requested fix: `V48-CP9-001`.
- Implementation preflight checkpoint revision 12 requested fix: `V48-CP9-002`.
- Implementation preflight checkpoint revision 13 approved (verifier report recorded approved; coms JSON envelope was malformed but report machine status is approved).
- Final bug-check revision 14 requested fixes: `V48-FBC-001`, `V48-FBC-002`.
- Final bug-check revision 15 approved with `bug_check_status: passed`.
