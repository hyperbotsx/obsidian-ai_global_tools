# Coder Handoff

- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/154`
- PRD: `GitHub issue #154 - D6-PRD: Closed Loop Runner Foundation for AgentOps Harness`
- Branch: `prd/d6-prd-closed-loop-runner-foundation-154`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-154`
- Agent label: `agent:agentops`
- Checkpoint: `Checkpoint 5 - Final integration and bug-check checkpoint`
- Worktree/branch preflight passed: `yes`

## Scope and constraints

Allowed paths for this checkpoint:

- `src/agentops_harness/cli.py`
- `src/agentops_harness/loop_*.py`
- `src/agentops_harness/activity_center.py`
- `src/agentops_harness/activity_center_loop.py`
- `src/agentops_harness/activity_center_sources.py`
- `schemas/loop-*.schema.json`
- `tests/fixtures/loop-*.json`
- `tests/unit/test_loop_contract.py`
- `tests/unit/test_activity_center.py`
- `docs/closed-loop-runner.md`
- `README.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-154/**`

Forbidden/out-of-scope paths remain product code, deployment, raw transcripts, secrets, AI Global Tools skills, GitHub mutation code paths, automatic agent launch, PR creation, merge, deployment, backtests, paper/live trading, and non-AgentOps repositories.

Pre-existing dirty files before editing: none (`git status --short --branch` showed a clean branch tracking `origin/main`).

## Verifier checkpoints

1. Spec and state contract checkpoint.
2. Oracle and stateless artifact checkpoint.
3. Diff guard, isolation, and reward-hacking checkpoint.
4. Read-only visibility and documentation checkpoint.
5. Final integration and bug-check checkpoint.

## Checkpoint 1 changes

Implemented read-only LoopSpec and LoopRunState foundation:

- Added `src/agentops_harness/loop_models.py`, `loop_spec.py`, and `loop_state.py`.
- Added `agentops-harness loop plan --spec ...` and `agentops-harness loop status --run ...`.
- Added LoopSpec and LoopRunState JSON schemas.
- Added valid, invalid, and ready-state fixtures.
- Added unit tests for valid plan rendering, invalid fail-closed behavior, CLI JSON/markdown behavior, and read-only status rendering.
- Added `docs/closed-loop-runner.md` and README command entries.

No oracle execution, diff guard, event writer, GitHub mutation, Activity Center mutation, or agent launch behavior was introduced in checkpoint 1.

Checkpoint 1 verifier verdict: approved, revision 1, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened.

Checkpoint 2 verifier verdict after revision 2: approved, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Checkpoint 2 changes

Implemented deterministic oracle and stateless artifact foundation:

- Added `src/agentops_harness/loop_events.py` and `src/agentops_harness/loop_oracle.py`.
- Added `agentops-harness loop oracle --spec ... --format json`.
- Oracle runner executes configured command arrays with per-command timeout, captures exit code/stdout/stderr summaries, writes bounded redacted logs, and returns machine-readable JSON.
- Oracle repeat mode uses `validation_repeat_count`; mixed pass/fail attempts return `flaky` and write an `oracle_failed` state with `budget_brake_state.reason=flaky_oracle`.
- Added durable `events.jsonl` with schema version, stable event ID, sequence, loop/run IDs, actor/action/status, timestamp, artifact refs, and redaction marker.
- Added persisted `loop-run-state.json` under the configured artifact folder.
- Added `schemas/loop-event.schema.json`.
- Extended tests for passing command/log redaction/event/state output, failing command exit code reporting, and deterministic flaky substitute.

Generated checkpoint artifacts are under `dev-plans/agentops/coder-verifier-workflow/runs/issue-154/`: `events.jsonl`, `loop-run-state.json`, and `oracle/0001-loop-plan-attempt-1.log`.

Checkpoint 2 revision 1 verifier verdict: revision requested with findings `F154-C2-001` and `F154-C2-002`.

Checkpoint 2 revision 2 fixes:

- Addressed `F154-C2-001` by introducing `OracleContext` and `AttemptData` dataclasses, reducing new helper parameter counts to the project limit (`append_event` now has 2 parameters; `attempt_result` 2; `write_log` 3).
- Addressed `F154-C2-002` by including the durable event sequence in oracle log filenames and adding a regression test for duplicate command IDs plus repeated oracle invocations.
- Regenerated checkpoint oracle artifacts so the JSONL event references `oracle/0001-loop-plan-attempt-1.log`, not the superseded overwritten path.

Checkpoint 3 verifier verdict after revision 2: approved, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Checkpoint 3 changes

Implemented diff guard, isolation surfacing, and reward-hacking checks:

- Added `src/agentops_harness/loop_diff_guard.py`.
- Added `agentops-harness loop diff-guard --spec ... --format json` with optional `--changed-file` fixtures/tests.
- Diff guard enforces allowed, forbidden, and immutable paths, automatically treating the configured artifact folder as an allowed run-artifact root.
- Added suspicious validation-surface detection for tests, fixtures, schemas, CI/workflow files, quality-gate/package files, and similar reward-hacking surfaces unless explicitly allowlisted by `LoopSpec.reward_hacking_allowlist`.
- Diff guard appends a JSONL event and updates `loop-run-state.json` with `diff_guard_result` and `diff_guard_failed` status when blocked.
- Diff guard output includes isolation network policy/enforcement and marks `network_enforcement=placeholder` as `documented_placeholder` rather than implying OS-level sandboxing.
- Extended tests for allowed changes, forbidden/immutable path failures, suspicious test changes, unique oracle log references, and placeholder isolation surfacing.
- Updated docs and README command list for diff guard.

Generated checkpoint artifacts were regenerated after oracle + passing diff guard. `events.jsonl` now has an oracle event and a diff_guard event with unique artifact references.

Checkpoint 3 revision 1 verifier verdict: revision requested with findings `F154-C3-001` and `F154-C3-002`.

Checkpoint 3 revision 2 fixes:

- Addressed `F154-C3-001` by running automatic changed-file discovery in `LoopSpec.worktree`, detecting nonzero `git status`/OS errors, and failing closed with `changed_file_discovery_failed` when discovery is unavailable.
- Addressed `F154-C3-002` by recomputing persisted state status from current oracle/diff outcomes; a later passing diff guard now clears stale `diff_guard_failed` state when oracle results are clean.
- Added regression tests for no-git discovery failure and fail-then-pass state recovery.
- Updated `tests/fixtures/loop-valid.json` to use portable `worktree`/`working_directory` value `.` so automatic diff discovery runs in the current repository when using the fixture.

## Isolation / research

No external Playwright, GitHub Projects v2 mutation, provider-specific API behavior, or volatile external SDK behavior was added. No researcher freshness consult was required. Network enforcement is explicitly represented as `placeholder` in fixtures and CLI output warns that no OS-level sandboxing is implied.

## Validation run

Checkpoint 1:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_cli.py -q` — passed (`57 passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli loop plan --spec tests/fixtures/loop-valid.json --format json` — passed, status `passed`, network enforcement `placeholder` warning present.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop plan --spec tests/fixtures/loop-invalid.json --format json; test $? -eq 1` — passed, invalid spec returned blocked/errors.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop status --run tests/fixtures/loop-run-state.ready.json --format json` — passed, status `ready_for_verifier`, read-only warning present.

Checkpoint 2:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_cli.py -q` — passed (`60 passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli loop plan --spec tests/fixtures/loop-valid.json --format json >/tmp/loop-plan.json && PYTHONPATH=src python3 -m agentops_harness.cli loop oracle --spec tests/fixtures/loop-valid.json --format json >/tmp/loop-oracle.json && PYTHONPATH=src python3 -m agentops_harness.cli loop status --run dev-plans/agentops/coder-verifier-workflow/runs/issue-154/loop-run-state.json --format json >/tmp/loop-status.json && python3 - <<'PY' ...` — passed; statuses were `passed`, `ready_for_verifier`, `ready_for_verifier`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop plan --spec tests/fixtures/loop-invalid.json --format json; test $? -eq 1` — passed, invalid spec returned blocked/errors.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-154/coder-handoff.md --format json` — passed after checkpoint 2 update.

Checkpoint 2 revision 2:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_cli.py -q` — passed (`61 passed`).
- Parameter-count audit over `src/agentops_harness/loop_*.py` — passed; no helper exceeds 4 parameters.
- Function-length audit over `src/agentops_harness/loop_*.py` — passed; no function exceeds 20 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop oracle --spec tests/fixtures/loop-valid.json --format json` — passed; regenerated status `ready_for_verifier` and unique log path `oracle/0001-loop-plan-attempt-1.log`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop status --run dev-plans/agentops/coder-verifier-workflow/runs/issue-154/loop-run-state.json --format json` — passed; status `ready_for_verifier`.

Checkpoint 3:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_cli.py -q` — passed (`64 passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli loop diff-guard --spec tests/fixtures/loop-valid.json --format json` — passed; status `passed`, isolation status `documented_placeholder`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop status --run dev-plans/agentops/coder-verifier-workflow/runs/issue-154/loop-run-state.json --format json` — passed; status `ready_for_verifier`, diff guard status `passed`.
- Unit tests cover forbidden/immutable path failures and unallowlisted suspicious test changes returning `diff_guard_failed`.
- Parameter/function audit over `src/agentops_harness/loop_*.py` — passed; no helper exceeds 4 parameters or 20 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-154/coder-handoff.md --format json` — passed after checkpoint 3 update.

Checkpoint 3 revision 2:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_cli.py -q` — passed (`66 passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli loop diff-guard --spec tests/fixtures/loop-valid.json --format json` — passed; status `passed`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop oracle --spec tests/fixtures/loop-valid.json --format json` then `loop diff-guard` — passed and regenerated a two-event JSONL artifact.
- Regression tests cover no-git discovery failure and fail-then-pass state recovery.
- Parameter/function audit over `src/agentops_harness/loop_*.py` — passed; no helper exceeds 4 parameters or 20 lines.

Checkpoint 4 verifier verdict after revision 2: approved, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Checkpoint 4 changes

Implemented read-only visibility and documentation support:

- Added `src/agentops_harness/activity_center_loop.py` to map a `LoopRunState` JSON file into a read-only Activity Center item.
- Integrated optional `loop_state_path` and `AGENTOPS_LOOP_STATE_JSON` support into `build_activity_summary`.
- Loop activity item metadata includes `mode=read_only`, loop/run IDs, checkpoint, status, and artifact paths; target kind is `loop_state`.
- Loop status bucket mapping is display-only: `ready_for_verifier` -> ready, attention statuses -> needs_attention, `done` -> done, remaining statuses -> running.
- Added Activity Center unit coverage proving loop state surfaces as read-only and carries no approval authority language.
- Expanded `docs/closed-loop-runner.md` with Activity Center visibility, stateless iteration, verifier role, isolation placeholder, reward-hacking guard, and human-gate boundaries.

Checkpoint 4 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_activity_center.py tests/unit/test_cli.py -q` — passed (`75 passed`).
- `AGENTOPS_LOOP_STATE_JSON=dev-plans/agentops/coder-verifier-workflow/runs/issue-154/loop-run-state.json PYTHONPATH=src python3 - <<'PY' ...` — passed; one loop item surfaced with bucket `ready` and metadata mode `read_only`.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-154/coder-handoff.md --format json` — passed after checkpoint 4 update.

Checkpoint 4 revision 1 verifier verdict: revision requested with findings `F154-C4-001` and `F154-C4-002`.

Checkpoint 4 revision 2 fixes:

- Addressed `F154-C4-001` by removing the explicit `loop_state_path` public parameter and consuming loop visibility only through `AGENTOPS_LOOP_STATE_JSON`; refactored path handling so `build_activity_summary` remains within parameter/function-length limits while preserving existing positional and keyword path callers.
- Addressed `F154-C4-002` by adding a concise Brake semantics section covering invalid specs, oracle failure/timeouts, flaky repeats, forbidden/suspicious diffs, log/artifact bounds, max iteration/runtime/per-command/repeat fields, missing-verifier escalation, and future budget placeholders.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py tests/unit/test_cli.py -q` — passed (`60 passed`).
- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_activity_center.py tests/unit/test_cli.py -q` — passed (`75 passed`).
- Activity Center KISS audit — passed; changed Activity Center helpers are within parameter and function-length limits.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-154/coder-handoff.md --format json` — passed after checkpoint 4 revision 2 update.

## Checkpoint 5 integration validation

Final integration/status validation performed before steward review:

- `PYTHONPATH=src python3 -m agentops_harness.cli loop plan --spec tests/fixtures/loop-valid.json --format json` — passed; status `passed`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop oracle --spec tests/fixtures/loop-valid.json --format json` — passed; status `ready_for_verifier`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop diff-guard --spec tests/fixtures/loop-valid.json --format json` — passed; status `passed`.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop status --run dev-plans/agentops/coder-verifier-workflow/runs/issue-154/loop-run-state.json --format json` — passed; status `ready_for_verifier`, diff guard `passed`.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_activity_center.py tests/unit/test_cli.py -q` — passed (`75 passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli doctor` — passed with non-blocking warnings for optional GitHub Project/scope and external skills env verification.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-154/coder-handoff.md --format json` — passed after final integration update.
- `gate --ml` / `/gate --ml` — unavailable in this environment.
- `PYTHONPATH=src python3 -m pytest tests -q` — failed with 4 unrelated pre-existing/environment-sensitive failures: `test_agent_github_check_rejects_config_dir_without_agent_token`, `test_emit_sends_to_unix_socket_when_available` (AF_UNIX path too long under current runtime path), `test_agent_gh_env_uses_dedicated_config_and_strips_ambient_tokens`, and `test_agent_gh_env_can_inject_dedicated_token`.
- `PYTHONPATH=src python3 -m pytest tests -q -k 'not agent_github_check_rejects_config_dir_without_agent_token and not emit_sends_to_unix_socket_when_available and not agent_gh_env_uses_dedicated_config_and_strips_ambient_tokens and not agent_gh_env_can_inject_dedicated_token'` — passed (`968 passed, 4 deselected, 53 subtests passed`).

Generated run artifacts were cleaned and regenerated once after final oracle + diff-guard validation. Current run artifact set: `coder-handoff.md`, `verifier-report.md`, `events.jsonl`, `loop-run-state.json`, and `oracle/0001-loop-plan-attempt-1.log`.

Final bug-check revision 1 verifier verdict: revision requested with findings `F154-FBC-001` and `F154-FBC-002`.

Final bug-check revision 2 fixes:

- Addressed `F154-FBC-001` by removing oracle working-directory fallback to `.`; missing/non-directory `isolation_policy.working_directory` now fails closed as `oracle_failed`, writes an actionable error, and does not execute the command.
- Addressed `F154-FBC-002` by expanding secret redaction to quoted JSON/YAML-style secret keys such as `{"api_key":"..."}` before writing logs/summaries.
- Added regression tests for missing oracle working directory and JSON/quoted secret redaction.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_loop_contract.py tests/unit/test_activity_center.py tests/unit/test_cli.py -q` — passed (`77 passed`).
- Loop helper KISS audit — passed; no function exceeds 4 parameters or 20 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli loop oracle --spec tests/fixtures/loop-valid.json --format json` then `loop diff-guard` — passed and regenerated a two-event JSONL artifact.

Steward pre-final review returned `cleanup_recommended`. Cleanup/clarification applied:

- Added Activity Center files/tests and `dev-plans/agentops/coder-verifier-workflow/runs/issue-154/**` to the handoff allowed-path inventory.
- Kept issue-scoped run artifacts because verifier checkpoints and final bug-check need durable handoff, report, event, state, and oracle evidence.
- Cleaned ignored local test caches where present.

Steward cleanup recheck returned `clean`; non-blocking note: ignored `src/agentops_harness/__pycache__` may be recreated by validation and is not tracked.

## Known risks / next work

- Current schema validation is dependency-free internal validation plus checked-in JSON Schema documents; no `jsonschema` runtime dependency is added.
- Oracle runner currently falls back to the current directory if `isolation_policy.working_directory` is missing on disk; no OS-level network sandbox is implied and the placeholder is surfaced in plan/diff output.
- Activity Center consumes are now read-only via `AGENTOPS_LOOP_STATE_JSON`; no launch, approval, GitHub mutation, or verifier-evidence authority is added.
