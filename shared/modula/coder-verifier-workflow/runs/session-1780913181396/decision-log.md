# Decision Log

## 2026-06-08T10:11:41Z - Checkpoint 1 scope

- Source PRD: GitHub issue #925, read with `gh issue view 925 --repo hyperbotsx/SoldierOne`.
- Pre-edit status: clean branch `prd/human-confirmed-orchestration-assistant-925`; no pre-existing dirty files.
- Implemented only checkpoint 1: action allowlist and non-executing human confirmation UX.
- Deferred dry-run proposal persistence and confirmed-action execution to later checkpoints.
- Browser QA / DevTools not required because this checkpoint is CLI/docs only and preview target is not configured.
- Did not update tracker #862 because GitHub issue comments are mutating external actions and no separate explicit confirmation was provided for that write in this coder session.

## 2026-06-08T10:11:41Z - Safety choices

- Added `evonome-orchestrator-action policy` for allowlist review.
- Added `evonome-orchestrator-action confirm-template` as a non-executing UX renderer with `executed=false`.
- Kept all action policy code in AgentOps Harness.
- Added tests for dry-run default, allowlist refusal, forbidden hints, missing confirmation fields, CLI help, and non-execution.

## 2026-06-08T10:19:08Z - Verifier revision

- Addressed `V-925-CP1-001` by adding `proposal_id` to confirmation input, JSON output, markdown output, CLI arguments, missing-field checks, docs, README examples, and tests.
- Addressed `V-925-CP1-002` by expanding forbidden authority-boundary hints for autonomous CEO approval, CEO approval, approval-field edits, and adding unit/CLI/semantic smoke coverage.
- Kept revision bounded to checkpoint 1 policy/UX; no execution path or external mutation was added.

## 2026-06-08T10:24:48Z - Verifier revision 3

- Addressed remaining `V-925-CP1-002` PR-creation gap by adding forbidden detection for autonomous PR creation, PR creation, PR create, `gh pr create`, and pull-request creation wording.
- Added unit and CLI tests for PR creation refusal.
- Reran compile, scoped tests, full tests, CLI smokes, PR-creation semantic probe, diff check, token scan, and preflight.

## 2026-06-08T10:30:33Z - Checkpoint 2 dry-run proposals

- Started checkpoint 2 after verifier approved checkpoint 1 revision 3.
- Added dry-run proposal generation from re-read issue state via `evonome-orchestrator-action propose`.
- Added optional outside-repo proposal persistence and repo-local proposal directory refusal.
- Updated proposal schema, docs, README examples, and tests.
- Kept proposal records non-executing with `dry_run_only=true`, `requires_confirmation=true`, and `executed=false`.

## 2026-06-08T10:38:34Z - Checkpoint 2 revision

- Addressed `V-925-CP2-001` by carrying repo identity from issue URL/`gh` read into normalized source state, repo-qualified proposal targets, and default command previews with `--repo owner/repo`.
- Addressed `V-925-CP2-002` by making forbidden proposal requests fail closed before save/render as proposal records, with stable JSON and markdown refusal outputs.
- Addressed `V-925-CP2-003` by restricting `propose` to supported issue-comment/tracker proposal actions until branch-specific proposal fields are implemented.
- Added tests for exact repo target preview, forbidden proposal JSON/markdown refusal, unsupported action refusal, and successful proposal schema validation smoke.

## 2026-06-08T10:46:57Z - Checkpoint 3 harmless confirmed action

- Started checkpoint 3 after verifier approved checkpoint 2 revision 2.
- Added `evonome-orchestrator-action confirm` for a narrow harmless confirmed action that writes only a local audit record outside the repo.
- Supported confirmed actions are limited to `record_slack_confirmation` and `record_canvas_confirmation` proposals.
- Added explicit `--confirm`, exact summary, human note, audit-dir, and state-digest drift checks.
- Added unit and CLI coverage for success, missing confirmation flag, summary mismatch, drift refusal, and repo-local audit directory refusal.

## 2026-06-08T10:55:35Z - Checkpoint 3 revision

- Addressed `V-925-CP3-001` by requiring `--current-state-json` for every confirmed action and refusing `current_state_missing` when absent.
- Addressed `V-925-CP3-002` by validating dry-run proposal invariants before execution: `dry_run_only=true`, `executed=false`, `requires_confirmation=true`, `confirmation.executed=false`, and non-refused confirmation.
- Addressed `V-925-CP3-003` by removing Slack confirmation execution support until allowlisted #935 user/channel metadata is wired in; checkpoint 3 now executes only `record_canvas_confirmation` local-audit proposals.
- Updated docs/README and reran checkpoint 3 validation.

## 2026-06-08T11:01:15Z - Checkpoint 3 schema validation revision

- Addressed remaining `V-925-CP3-002` by adding explicit required-field checks for top-level proposal fields and nested confirmation fields before confirmed execution.
- Missing schema/PRD-required fields now return stable `invalid_proposal_record` refusal instead of executing or crashing.
- Added tests for missing `created_at`, `proposal_id`, `target`, `command_preview`, `rollback_note`, and `missing_fields`.

## 2026-06-08T11:07:42Z - Checkpoint 3 value/type validation revision

- Addressed remaining `V-925-CP3-002` invalid value/type/path traversal gap.
- Added schema-equivalent value checks for safe non-empty `proposal_id`, non-empty `target`, object `policy` with string `action_id`, string confirmation fields, and list `missing_fields`.
- Hardened `action_id()` against malformed policy values so invalid proposals refuse instead of crashing.
- Added tests and smokes for empty/unsafe proposal IDs, empty target, string `missing_fields`, and string `policy`.

## 2026-06-08T11:12:29Z - Checkpoint 3 malformed confirmation revision

- Addressed remaining `V-925-CP3-002` malformed non-object `confirmation` crash.
- Hardened refusal payload construction to tolerate non-dict confirmation values.
- Added tests and CLI smoke for `confirmation` as string/list returning stable `invalid_proposal_record` refusal.

## 2026-06-08T11:16:21Z - Checkpoint 3 top-level malformed proposal revision

- Addressed remaining `V-925-CP3-002` top-level non-object proposal crash.
- Added an early top-level proposal object/type check in `confirm_proposal` before any `.get()` access.
- Added tests and CLI smoke for top-level string/list proposal JSON returning stable `invalid_proposal_record` refusal.

## 2026-06-08T11:23:28Z - Final authority-boundary health/status checkpoint

- Started final checkpoint after verifier approved checkpoint 3 revision 6.
- Added read-only `evonome-orchestrator-action health` output for dry-run mode, supported proposal actions, supported confirmed actions, proposal/audit directory status, degraded reasons, and recovery notes.
- Added repo-local proposal/audit path degradation to support fail-closed operations.
- Added docs, README example, unit tests, and CLI health smokes.

## 2026-06-08T11:30:59Z - Final fail-closed revision

- Addressed `V-925-FINAL-001` by adding guarded proposal read/parse, current-state read/parse, and audit-write failure handling with stable non-zero refusal payloads.
- Addressed `V-925-FINAL-002` by rendering `propose` source-state failures through JSON/markdown refusal renderers and validating issue JSON is an object.
- Added tests and smokes for malformed/missing proposal files, malformed/missing current-state files, audit write failure, malformed issue JSON, and non-object issue JSON.

## 2026-06-08T11:36:21Z - Final proposal persistence revision

- Addressed `V-925-FINAL-003` by catching proposal persistence `OSError` failures.
- Proposal storage paths that are outside repo but unusable now return stable `proposal_write_failed` refusal with non-zero exit.
- Added unit and CLI coverage for `--proposal-dir` pointing to an existing file.
