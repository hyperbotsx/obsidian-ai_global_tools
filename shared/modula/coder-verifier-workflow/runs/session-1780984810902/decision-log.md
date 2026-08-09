# Decision Log

## 2026-06-09 checkpoint plan

- Source of truth: GitHub issue #945.
- Pre-existing dirty files: none.
- Preview target: not configured; Browser QA not required for checkpoint 1.
- Stop condition for this slice: schema/secret/multi-project source-of-truth tests pass, `python3 -m pytest tests/unit/test_profile_setup.py`, and `git diff --check` pass.
- Checkpoints derived from PRD section 9.

## 2026-06-09 checkpoint 1 ready

- Implemented generic profile schema validation in `src/agentops_harness/profile_schema.py`.
- Added non-interactive config secret scanning before profile write.
- Added tests for source-of-truth fields, secret-like values, safe auth references, role-scoped dangerous flags, and dashboard exposure metadata.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_schema.py tests/unit/test_profile_setup.py && git diff --check`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 V-945-CP1-001 revision

- Verifier requested raw text secret scanning for YAML list items and single-quoted secret-looking scalar values.
- Added list item parsing and single-quote stripping in `split_text_pair` helpers.
- Added regression test covering `- 'xoxb-real-token'` and `foo: 'ghp_real_token'`.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_schema.py tests/unit/test_profile_setup.py && PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 checkpoint 2 ready

- Checkpoint 1 approved by verifier with zero open findings.
- Non-interactive `init --profile <name> --config <file>` now runs strict schema validation, secret scanning, local path validation, and profile-name matching before writing.
- Validated full config YAML is preserved when written to `~/.config/agentops-harness/profiles/<profile>.yaml`.
- Added `agentops-harness profile list`, `profile show`, and `profile doctor`.
- `profile show` renders a redacted summary.
- `profile doctor` performs schema, secret, path, git repo, preview URL, dashboard exposure, and runtime availability checks without mutating external systems.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_schema.py tests/unit/test_profile_setup.py tests/unit/test_profile_commands.py tests/unit/test_cli.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 checkpoint 2 revision

- Verifier requested two revisions: no-config/interactive init must not write doctor-invalid profiles, and non-interactive init must block missing local main/dev-main/audit/run roots before write.
- Non-interactive init without `--config` now fails closed with a clear message to use `--config` or `--interactive`.
- Interactive init now prompts for required project source-of-truth fields, local/audit/run paths, role runtimes, and dashboard metadata, then writes full schema YAML through the same strict validator.
- Non-interactive config validation now applies doctor-equivalent local checks before writing.
- Added regressions for interactive-init then doctor success and pre-write blocking of missing local git repos and uncreatable audit roots.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_schema.py tests/unit/test_profile_setup.py tests/unit/test_profile_commands.py tests/unit/test_cli.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 checkpoint 2 redaction revision

- Verifier requested redaction of secret-looking scalar/list values in `profile show` and `profile doctor` summaries.
- Added scalar-value redaction for values matching `SECRET_VALUE_PREFIXES`, even when the containing key is not sensitive.
- Added regression coverage proving a blocked profile report does not echo a synthetic `xoxb-` value.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_profile_commands.py tests/unit/test_profile_schema.py tests/unit/test_profile_setup.py tests/unit/test_cli.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 checkpoint 3 ready

- Checkpoint 2 approved by verifier with zero open findings after redaction revision.
- Added profile-scoped path helpers for audit roots, run artifact proposal dirs, and Slack allowlists.
- `evonome-orchestrator-action propose --profile <name>` now stores proposals under the profile run artifacts root when no explicit proposal dir is provided.
- `evonome-orchestrator-action confirm --profile <name>` now writes local audit evidence under the profile audit root when no explicit audit dir is provided.
- `evonome-slack-gateway handle --profile <name>` now loads profile Slack allowlists and stores Slack proposals under a profile-scoped run artifact path.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_action_assistant_cli.py tests/unit/test_slack_gateway_policy.py tests/unit/test_profile_commands.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 checkpoint 3 revision

- Verifier requested fail-closed behavior for missing profiles, multiple profiles without selection, and Slack-disabled profiles.
- Added profile existence and configured-profile count helpers.
- Action assistant proposal/audit flows now refuse missing profiles and refuse no-profile mutating flows when multiple profiles exist.
- Slack gateway handle now refuses missing profiles, multiple-profile/no-profile requests, and profile-driven Slack use when `slack.enabled` is false or missing.
- Added regressions for missing profile, multiple profile, and Slack-disabled profile cases.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_action_assistant_cli.py tests/unit/test_slack_gateway_policy.py tests/unit/test_profile_commands.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.

## 2026-06-09 final review ready

- Checkpoint 3 approved by verifier with zero open findings.
- Final implementation validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.
- Ready for final verifier review and default wrong-project mutation / secret-leak bug-check.

## 2026-06-09 final bug-check revision

- Verifier found `V-945-FINAL-001`: explicit Slack allowlist CLI args could override selected profile allowlists.
- `evonome-slack-gateway handle --profile <name>` now refuses explicit `--allowed-user-id` or `--allowed-channel-id` overrides.
- Added regression proving override attempts do not capture profile-scoped proposals.
- Validation passed: `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_gateway_policy.py`.
- Validation passed: `PYTHONPATH=src python3 -m pytest && git diff --check`.
