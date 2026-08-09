# Coder handoff — Issue 148 Launch metadata hygiene

## Source of truth
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/148
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-148`
- Branch: `prd/launch-metadata-hygiene-repair-launch-148`

## Initial state
- Pre-edit status: clean (`git status --short --branch`).
- Research-first surfaces: none named in PRD.
- Memory: disabled/advisory only per launch prompt.

## Scope controls
- Allowed paths for current checkpoint: `src/agentops_harness/**`, `tests/unit/**`, run artifacts under this folder.
- Forbidden: PR creation, merge, deploy, approval changes, launch bypasses, worktree deletion/reset/clean/stash/force-push, raw transcripts/secrets.
- Stop condition: verifier approves checkpoint 1 or requests one bounded revision.

## Verifier checkpoints
1. Audit checkpoint — Project PRD audit detects missing/malformed worktree, branch, and base-branch metadata with expected values.
2. Single repair checkpoint.
3. Bulk repair checkpoint.
4. Safety/fail-closed checkpoint.
5. Authoring guardrail checkpoint.
6. Approval guardrail checkpoint.
7. Repair-and-launch checkpoint.
8. Evidence/UI refresh checkpoint.
9. Board hard-refresh shortcut checkpoint.
10. Project mirror checkpoint.
11. Regression checkpoint.
12. Final validation checkpoint.

## Current checkpoint: 1 — Audit

### Revision 2 fixes
- Addressed `F148-R1-001`: parsed Project status separately, kept Done/completed Project items visible as `read_only_done`, and excluded them from `repairable_items`.
- Addressed `F148-R1-002`: shortened the oversized parser test by extracting Project item fixture helpers.

Implemented a read-only launch metadata audit surface:
- New `src/agentops_harness/prd_launch_metadata_audit.py`:
  - Audits open `type:prd` Project items.
  - Normalizes `Worktree Path`, `Working Branch`, `Base Branch` field aliases from `gh project item-list` output.
  - Derives expected worktree as `<worktrees_root>/agentops-prd-<issue>`.
  - Derives expected branch as `prd/<slug>-<issue>`, preserving an existing stale branch slug when it safely ends with the issue suffix.
  - Flags lane-era `agentops-laneA`..`agentops-laneD` worktrees as `metadata_malformed`.
  - Flags non-`prd/` branches and branches not ending in `-<issue>`.
  - Reports `metadata_missing`, `metadata_malformed`, `ok`, and item statuses `healthy`, `repair_ready`, `unsupported_implementation_home`.
  - Renders JSON and Markdown with before/after values.
- CLI wiring in `src/agentops_harness/cli.py`:
  - `agentops-harness prd-worktree metadata-audit` reads Project items live or from `--items-json`.
- `src/agentops_harness/github_project.py` now requests `--limit 1000` for Project item listing so the audit does not silently rely on the small default page.
- Tests added in `tests/unit/test_prd_launch_metadata_audit.py`.

## Changed files
- `src/agentops_harness/prd_launch_metadata_audit.py`
- `src/agentops_harness/cli.py`
- `src/agentops_harness/github_project.py`
- `tests/unit/test_prd_launch_metadata_audit.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-148-launch-metadata-hygiene/coder-handoff.md`

## Validation
- `python -m pytest ...` failed because `python` is not installed in this environment.
- `git diff --check` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_prd_worktree_project.py tests/unit/test_cli.py` — passed, 69 tests.
- Revision 1 live read-only smoke: `PYTHONPATH=src python3 -m agentops_harness.cli prd-worktree metadata-audit --worktrees-root /mnt/hyperliquid-data/projects/worktrees --format json > /tmp/prd148-audit.json` — passed, summary: `status=ok`, `total_items=56`, `audited_items=56`, `healthy_items=3`, `repairable_items=51`, `blocked_items=53`.
- Revision 2: `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_prd_worktree_project.py tests/unit/test_cli.py` — passed, 70 tests.
- Revision 2 live read-only smoke: `PYTHONPATH=src python3 -m agentops_harness.cli prd-worktree metadata-audit --worktrees-root /mnt/hyperliquid-data/projects/worktrees --format json > /tmp/prd148-audit-r2.json` — passed, summary: `status=ok`, `total_items=56`, `audited_items=56`, `healthy_items=1`, `repairable_items=11`, `blocked_items=55`; sample Done Project items now show `read_only_done`.

## Checkpoints 2-4 — Single repair, bulk repair, safety/fail-closed

### Revision 4 fixes
- Addressed `F148-R3-001`: no-op execution now returns no-op without Project mutation or worktree preparation.
- Addressed `F148-R3-002`: missing repository is now `ambiguous_implementation_home` in audit and blocks repair planning.
- Addressed `F148-R3-003`: default repair safety now checks default lease records and blocks active sessions, lifecycle locks, ownership mismatch, existing dirty target worktrees, and existing wrong-branch target worktrees before mutation; worktree creation remains opt-in.
- Addressed `F148-R3-004`: bulk results now surface nested partial failures at top level with `partial_failure_count`, errors, and non-ok status; CLI exits nonzero for non-ok executed bulk results.
- Addressed `F148-R3-005`: replaced the 7-parameter repair helper with a grouped `RepairState` helper.

### Revision 5 fix
- Addressed `F148-R4-001`: repair planning now scans active lease records for any other PRD assigned to the target worktree path and blocks before Project updates.

### Revision 6 fix
- Addressed `F148-R5-001`: split lease/worktree safety helpers into `src/agentops_harness/prd_launch_metadata_repair_safety.py`; `prd_launch_metadata_repair.py` is now 271 lines.

Implemented backend/CLI repair planning and execution in `src/agentops_harness/prd_launch_metadata_repair.py`:
- Single repair plan/execute derives expected values from the audit result and updates only Project launch fields through existing `ProjectFieldSyncRequest` utilities.
- Explicit confirmation string is required for execution; preview is available without mutation.
- Bulk repair previews every supplied Project item and executes only `ready` items after bulk confirmation; no launch path is invoked.
- Done/completed, unsupported implementation-home, unapproved, lease mismatch, active session, lifecycle lock, and missing repository path for worktree preparation all fail closed.
- Optional worktree preparation reuses existing `prepare_prd_worktree` provisioning checks for dirty/wrong-branch/path conflicts.
- Durable JSONL evidence is written only when `evidence_path` is provided and includes issue, old/new values, actor/action source, timestamp, status, and blocker reason.
- CLI commands added: `prd-worktree metadata-repair` and `prd-worktree metadata-bulk-repair`.

Additional validation:
- Revision 3: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 65 tests.
- Revision 4: `git diff --check` — passed.
- Revision 4: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 70 tests.
- Revision 5: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 71 tests.
- Revision 5: `git diff --check` — passed.
- Revision 6: `wc -l src/agentops_harness/prd_launch_metadata_repair.py src/agentops_harness/prd_launch_metadata_repair_safety.py` — repair file 271 lines, safety file 85 lines.
- Revision 6: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 71 tests.
- Revision 6: `git diff --check` — passed.
- CLI plan smoke for `metadata-repair` on a #116-style lane item — passed, returned `status=ready` with expected `/worktrees/agentops-prd-116`, `prd/old-lane-116`, and `main`.

## Checkpoints 5-10 — Authoring/approval guardrails, repair-and-launch, refresh, mirror diagnostics

### Revision 8 fixes
- Addressed `F148-R7-001`: board setup now treats non-`prd/` branches, branches missing the issue suffix, and non-`agentops-prd-<issue>` worktree paths as repairable malformed metadata.
- Addressed `F148-R7-002`: repair-and-launch now performs a preview POST first, displays exact before/after values for `Working Branch`, `Worktree Path`, and `Base Branch`, and requires `window.confirm` before executing and launching.
- Addressed `F148-R7-003`: TS repair route now writes non-secret JSONL evidence for repair-and-launch executions.
- Addressed `F148-R7-004`: board startup detects native reload navigation and reloads `board-data.js` with a cache-busting query.
- Addressed `F148-R7-005`: mirror diagnostics UI now renders a visible expandable hidden/excluded item list with number/title/repository/status/reason for every hidden item.

### Revision 9 fixes
- Addressed `F148-R8-001`: TS repair now treats `Base Branch` as required metadata, repairs it to `main`, and validates read-back.
- Addressed `F148-R8-002`: confirmed TS repair failures now persist JSONL evidence with old/intended values and blocker reason.
- Addressed `F148-R8-003`: mirror diagnostics visibility keys now include repository plus issue number, so same-number cross-repo Project items are not silently omitted.

### Revision 10 fixes
- Addressed `F148-R9-001`: TS repair-and-launch no longer trusts stale issue-body Base Branch values; target Base Branch is always the required `main`, and body normalization rewrites stale Base branch lines to `main`.
- Addressed `F148-R9-002`: Project id and later confirmed repair exceptions now route through evidence-writing failure helpers once before/target context exists.
- Addressed `F148-R9-003`: refactored `fixLaunchMetadata` into smaller helpers; `term-control-center/server/launchMetadataFix.ts` is 261 lines and typecheck passes.

### Revision 11 fixes
- Addressed `F148-R10-001`: Project field-list failures after item/target context is known now write durable blocked repair evidence.
- Addressed `F148-R10-002`: removed unused `prdBodyValue` and `escapeRegExp` helpers from `launchMetadataFix.ts`.
- Addressed `F148-R10-003`: shortened the legacy metadata normalization test by extracting setup/assertion/evidence helpers.

Implemented follow-up surfaces:
- Authoring guardrail: existing PRD author GitHub plan already uses issue-numbered worktree/branch metadata for create placeholders and update issue-numbered fields; targeted tests retained.
- Approval guardrail: `src/agentops_harness/prd_studio_approval.py` now blocks Approval Review packets when Project launch metadata is missing/malformed for the selected issue/repository.
- Repair-and-launch: `term-control-center/server/launchMetadataFix.ts` can prepare/reuse the target per-PRD worktree before mutating fields when the route requests it, returns before/after field snapshots, and the board repair button is now labeled `Repair metadata, prepare worktree, then launch` for implementation launches. On successful repair with no missing fields, the board proceeds through the normal `/launch` path.
- Board refresh shortcut: `Cmd+Shift+R` / `Ctrl+Shift+R` on the board queues the existing pipeline refresh route, reloads `board-data.js` with a cache-busting query string, and shows refresh status.
- Project mirror diagnostics: `pipeline-diagram/generate.py` now emits `window.PIPELINE_MIRROR_DIAGNOSTICS` from Project membership, and `board.html` displays visible/total counts plus hidden reason counts and a sample hidden item.
- Documentation: `docs/worktree-branch-ownership.md` now documents required launch metadata and safe audit/repair commands.

Additional validation:
- `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_studio_approval.py tests/unit/test_prd_author_github.py tests/unit/test_pipeline_board_generation.py tests/unit/test_pipeline_generate.py tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 97 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- Revision 7: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 4 tests.
- Revision 8: `npm --prefix term-control-center run typecheck` — passed.
- Revision 8: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 5 tests.
- Revision 8: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_pipeline_board_generation.py tests/unit/test_prd_studio_approval.py` — passed, 10 tests.
- Revision 9: `npm --prefix term-control-center run typecheck` — passed.
- Revision 9: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 6 tests.
- Revision 9: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_pipeline_board_generation.py` — passed, 4 tests.
- Revision 9: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_studio_approval.py tests/unit/test_prd_author_github.py tests/unit/test_pipeline_board_generation.py tests/unit/test_pipeline_generate.py tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_cli.py` — passed, 98 tests.
- Revision 9: `git diff --check` — passed.
- Revision 10: `python3 - <<'PY' ... wc line check` — `term-control-center/server/launchMetadataFix.ts` is 261 lines.
- Revision 10: `npm --prefix term-control-center run typecheck` — passed.
- Revision 10: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 6 tests.
- Revision 10: `PYTHONPATH=src:. python3 -m pytest tests/unit/test_pipeline_board_generation.py` — passed, 4 tests.
- Revision 10: `git diff --check` — passed.
- Revision 11: `npm --prefix term-control-center run typecheck` — passed.
- Revision 11: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 7 tests.
- Revision 11: `git diff --check` — passed.
- Revision 11: line counts — `term-control-center/server/launchMetadataFix.ts` 252 lines; `term-control-center/tests/launchMetadataFix.test.ts` 199 lines.
- Steward pre-final hygiene review: `cleanup_recommended`; placement/artifacts clean, recommended ignored local cleanup only.
- Cleanup completed: removed ignored `.pytest_cache/`, Python `__pycache__`, generated pipeline diagram outputs, `term-control-center/build`, `term-control-center/dist`, and local `term-control-center/node_modules` after npm validation.
- Final targeted validation: `env -u AGENTOPS_GH_CONFIG_DIR -u AGENTOPS_GITHUB_TOKEN -u GH_TOKEN -u GITHUB_TOKEN TMPDIR=/tmp PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_prd_worktree_project.py tests/unit/test_prd_studio_approval.py tests/unit/test_pipeline_board_generation.py tests/unit/test_cli.py` — passed, 93 tests.
- Final TS validation before cleanup: `npm --prefix term-control-center run typecheck` — passed.
- Final TS targeted tests before cleanup: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed, 7 tests.
- Final build before cleanup: `npm --prefix term-control-center run build` — passed with existing Vite chunk/script warnings.
- Full unit sweep note: `PYTHONPATH=src:. python3 -m pytest tests/unit` collected 936 tests; failed only in environment-sensitive pre-existing areas (`AGENTOPS_GH_CONFIG_DIR`/`AGENTOPS_GITHUB_TOKEN` ambient overrides and long socket path). Re-run with token env unset and `TMPDIR=/tmp` reduced to 2 existing `test_github_cli_env.py` failures unrelated to issue 148 scope; targeted PRD #148 suite passes.

### Final bug-check revision 2 fixes
- Addressed `F148-FBC-001`: confirmed Python repair execution blockers now route through evidence writing when old/new metadata is known; added dirty-worktree blocked-evidence regression coverage.
- Addressed `F148-FBC-002`: Python bulk repair execution preserves Project item identity via `item_id`, preventing same-number cross-repo collisions; added regression coverage for external/harness duplicate issue numbers.
- Addressed `F148-FBC-003`: board hard-refresh now posts the refresh, polls the Term Control refresh-status endpoint until a terminal state, reloads cache-busted board data only after completion, and surfaces queued/running/failed/timeout states truthfully. Added static guardrail coverage for polling and server status route wiring.
- Revision 2 validation: `env -u AGENTOPS_GH_CONFIG_DIR -u AGENTOPS_GITHUB_TOKEN -u GH_TOKEN -u GITHUB_TOKEN TMPDIR=/tmp PYTHONPATH=src:. python3 -m pytest tests/unit/test_prd_launch_metadata_repair.py` — passed, 14 tests.
- Revision 2 validation: `npm --prefix term-control-center run typecheck` — passed.
- Revision 2 validation: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts tests/boardGuardrails.test.ts` — passed, 42 tests.
- Revision 2 validation: targeted Python PRD suite (`test_prd_launch_metadata_audit.py`, `test_prd_launch_metadata_repair.py`, `test_prd_worktree_project.py`, `test_prd_studio_approval.py`, `test_pipeline_board_generation.py`, `test_cli.py`) — passed, 95 tests.
- Revision 2 validation: `npm --prefix term-control-center run build` — passed with existing Vite script/chunk warnings.
- Revision 2 validation: `git diff --check` — passed.
- Final verifier bug-check revision 2: approved; `bug_check_status=passed`, no open findings.
- Post-approval cleanup: removed ignored local `term-control-center/node_modules`, build/dist, pytest cache, and Python `__pycache__` artifacts; tracked/untracked implementation and run artifacts remain.
- Full `npm --prefix term-control-center run test -- launchMetadataFix.test.ts` after installing dependencies ran the full test suite instead of filtering; it timed out after 180s with pre-existing unrelated failures in `launchPlan.test.ts`/`server.test.ts`, but the targeted `launchMetadataFix.test.ts` run above passed.
- `git diff --check` — passed.

## Notes / known follow-ups
- Full final validation and final bug-check remain pending.
