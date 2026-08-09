# Coder Handoff — Issue 167 Kody Review Fixes

## Source of truth
- PRD issue: https://github.com/hyperbotsx/agentops-harness/issues/167
- PR: https://github.com/hyperbotsx/agentops-harness/pull/183
- Kody review comments addressed:
  - 3495474596 — overflow lane labels raised before lane cap merge.
  - 3495474693 — project_id path traversal for slot queue and launch-plan paths.
  - 3495474800 — explicit chat move could be dropped by soft-overlap policy.
  - 3495474924 — duplicate issue-state reads during slot launch.

## Pre-edit state
- Branch: `prd/ai-coworker-slot-queues-167`
- Pre-existing dirty files: none (`git status --short --branch` was clean before edits).

## Scope controls
- Allowed paths: `src/agentops_harness/lane_plan.py`, `src/agentops_harness/review_server.py`, focused tests under `tests/unit/`, this run artifact folder.
- Forbidden paths: routes/navigation outside the reviewed slot workflow, deployment, secrets, raw transcripts, PR creation/merge/deploy.
- Stop condition: all Kody findings fixed, verifier approves implementation and bug-check, then commit fixes and trigger another Kody review.

## Checkpoint
Single bounded checkpoint: Kody review remediation for PR #183.

## Changes made
- `src/agentops_harness/lane_plan.py`
  - Keeps missing group validation fail-closed.
  - Defers A-D slot enforcement until after lane cap merging.
  - Maps overflow model group labels into available Slot A-D names.
- `src/agentops_harness/review_server.py`
  - Validates project-scoped pipeline paths with `require_project_context()` before constructing slot queue or slot launch plan paths.
  - Applies explicit chat move/assign commands with `override_overlaps=True`.
  - Caches selected slot issue states during launch and reuses them for completion checks, validation, and launch lane-plan generation.
  - Refactored cache propagation after verifier finding `F167-KODY-R1-001` so changed functions stay within the KISS parameter-count limit.
- `tests/unit/test_lane_plan.py`
  - Covers overflow group labels mapping into A-D after lane cap.
- `tests/unit/test_review_server_coworker.py`
  - Covers explicit move overlap override.
  - Covers project_id traversal rejection on empty queue update.
  - Covers launch issue-state caching.

## Validation
- `PYTHONPATH=src pytest -q tests/unit/test_lane_plan.py tests/unit/test_slot_queues.py tests/unit/test_review_server_coworker.py` — passed, 79 tests after the verifier-requested KISS fix.
- `PYTHONPATH=src python3 -m compileall -q src/agentops_harness tests/unit/test_lane_plan.py tests/unit/test_slot_queues.py tests/unit/test_review_server_coworker.py` — passed after the verifier-requested KISS fix.
- `git diff --check` — passed.
- `PYTHONPATH=src:. pytest -q` — failed with 4 unrelated pre-existing/environment failures after the verifier-requested KISS fix:
  - `tests/unit/test_agent_github_health.py::test_agent_github_check_rejects_config_dir_without_agent_token`
  - `tests/unit/test_ai_maestro_handoff_emit.py::HandoffEmitTests::test_emit_sends_to_unix_socket_when_available`
  - `tests/unit/test_github_cli_env.py::test_agent_gh_env_uses_dedicated_config_and_strips_ambient_tokens`
  - `tests/unit/test_github_cli_env.py::test_agent_gh_env_can_inject_dedicated_token`

## Risks / notes
- `prepare_sequence_plan()` still rejects missing group values; only explicit non-A-D labels are normalized after lane-cap processing.
- Project-scoped slot paths now require a known project id; unknown/traversal ids fail closed with HTTP 400 via existing `ProjectContextError` handling.
- No commits made yet.
