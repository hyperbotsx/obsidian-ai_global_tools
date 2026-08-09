# Coder handoff — Issue #167 AI Co-Worker Slot Queues

## Source of truth
- Canonical task: https://github.com/hyperbotsx/agentops-harness/issues/167
- Branch: `prd/ai-coworker-slot-queues-167`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-167`
- PRD status: approved / CEO approved in issue body and owner comment.
- Research-first surfaces: none.

## Initial state
- Pre-edit `git status --short --branch`: clean (`## prd/ai-coworker-slot-queues-167...origin/main`).
- Memory disabled per launch warning; not used as source of truth.

## Scope controls
- Allowed paths: `src/agentops_harness/**`, `pipeline-diagram/**`, `term-control-center/**`, `tests/**`, scoped docs if behavior changes, and this run folder.
- Forbidden without human approval: PR creation, merge, deploy, production preview, PRD approval, trading/backtests, deleting active tmux/session state, secrets/raw transcript persistence, unrelated rewrites.
- Validation target: focused unit tests first, then relevant Python + term-control-center suites as scope expands.
- Stop condition: final verifier implementation approval plus final verifier bug-check approval, or human escalation.

## Verifier checkpoints
1. Slot queue state model and no-default assignment behavior.
2. AI Co-Worker proposal/apply flow, including #103 allocation/delegation preview intents.
3. Manual slot edit and reorder validation.
4. Background launch of queue heads only.
5. No auto-advance after completion, PR merge, main sync, or terminal exit.
6. Board refresh and running animation.
7. Regression pass on PRD creation and launch metadata.

## Current checkpoint
Complete — final verifier bug-check approved.

### Plan
- Add explicit Slot A-D queue persistence helpers.
- Ensure generated board chips only get visible slot badges from explicit slot state, not missing/legacy sequencing groups.
- Ensure slot-plan application validation fails on missing/invalid slot IDs rather than defaulting to Slot A.
- Add focused tests for no-default-Slot-A behavior and explicit slot queue order.

## Changes
Checkpoint 1 implemented (approved by verifier):
- Added `src/agentops_harness/slot_queues.py` with explicit Slot A-D queue normalization, persistence helpers, duplicate/unknown-slot validation, and order-to-slot conversion that requires explicit slots.
- Updated `src/agentops_harness/lane_plan.py` so plan order normalization rejects missing/invalid groups instead of silently defaulting missing data to Slot A.
- Updated `pipeline-diagram/generate.py` so visible board slot badges come only from explicit `slot-queues.json`; legacy `plan-order.json` groups still drive ordering/blocking but no longer appear as user-visible slot assignment.
- Updated `pipeline-diagram/board.html` chip rendering to use `slot`/`data-slot` badges instead of `group`/`data-group` for visible slots.
- Added/updated tests for explicit queue order, duplicate rejection, missing/invalid slot IDs, and no-default visible Slot A behavior.

Checkpoint 2 implemented:
- Added AI Co-Worker chat intent routing for slot allocation language: `fill the slots`, `assign the slots`, `organize the next work`, PRD-to-slot/lane allocation, delegation, `schedule next N PRDs`, and explicit `#123 #124` requests.
- Slot allocation intents now produce a confirmation-gated preview (`pending_slot_plan_id`) and do not call the generic model text path or persist slot state.
- Added `apply slots` chat confirmation and `/coworker/slots/apply` endpoint with explicit confirmation + pending-plan-id checks; applying writes `slot-queues.json`, triggers board refresh, and starts no launches.
- Updated `pipeline-diagram/coworker-launcher.js` with an Apply slots button and pending slot plan tracking.
- Updated `pipeline-diagram/generate.py` to read project-scoped slot queues when present.
- Added tests for #103 allocation/delegation language returning previews instead of refusals, preview non-mutation, apply persistence, and apply endpoint confirmation guard.
- Revision 2 fixes verifier findings V167-CP2-F1 and V167-CP2-F2: slot previews now include per-PRD rationale/queue-behind reasons, chat apply returns an empty `pending_slot_plan_id`, and the launcher honors empty pending slot IDs instead of preserving stale values.

Checkpoint 3 implemented (approved by verifier after human-approved r3):
- Added `apply_manual_slot_queues()` and `/coworker/slots/update` to save full explicit slot queue replacements, enabling clear/move/reorder/assign operations through a confirmation-gated API.
- Added validation before slot persistence for duplicate/unknown slots (via shared queue normalization), approved/launch-ready PRD status, `prd/` working branch, `/agentops-prd-<num>` worktree suffix, completed PRDs, and currently running PRDs when term-control group state is available.
- Applied the same validation to chat/button slot application so invalid pending previews fail before persistence.
- Added focused tests for clear/move/reorder persistence and invalid launch metadata blocking.
- Revision 2 fixes verifier finding V167-CP3-F1 and partially addresses V167-CP3-F2: added explicit chat commands for manual slot edits (`clear slot A`, `move/assign #N to slot B`, `reorder slot A #...`) that persist through the update path, added hard blocker order validation from `plan-order.json`, and added soft overlap default-unassign behavior with an override path.
- Verifier returned `needs_human` on V167-CP3-F2 because soft overlap paths were read from `plan-order.json`, but normal sequencing apply persists paths in `lane-plan.json`; human approved another bounded revision.
- Revision 3 fixes V167-CP3-F2 by sourcing overlap paths from `lane-plan.json` with `plan-order.json` paths only as a fallback, keeping `plan-order.json` lightweight. Added regression coverage that writes normal sequencing outputs via `write_sequencing_outputs()` and proves soft-overlap default-unassign works without paths in `plan-order.json`.

Checkpoint 4 implemented:
- Added slot launch intents in AI Co-Worker chat: `start work`, `start integration`, `begin implementation`, `launch the slots`, `launch slot A`, `continue slot A`, and `launch next in slot A`.
- Added `/coworker/slots/launch` endpoint with explicit `launch` / `launch slots` confirmation for one-slot launches.
- Slot launch reads persisted `slot-queues.json`, validates slots, writes a temporary `lane-plan.json` from the selected slot queues, and calls term-control-center `/launch` with `laneExecution.selectedLanes`.
- Launch all filled slots selects each filled Slot A-D; launch one slot selects only that slot. Because term-control lane execution launches the queue head per lane, queued PRDs behind the head remain idle.
- Slot launch response summarizes launched count, queued launch groups, reused count placeholder, queue heads, still-waiting PRDs, blocked list, empty slots, groups, and validation.
- Existing running queue heads are allowed through validation so term-control can reuse/summarize rather than being blocked before launch.
- No terminal modal auto-open is introduced; chat/endpoint paths return JSON/assistant text only.
- Revision 2 fixes verifier findings V167-CP4-F1/F2/F3: slot launch now writes `slot-launch-lane-plan.json` and passes `laneExecution.lanePlanPath` instead of overwriting canonical `lane-plan.json`; reused queue heads are computed from pre-launch running groups; `coworker_chat()` intent dispatch was extracted into `coworker_intent_response()` to restore KISS function size.
- Revision 3 fixes verifier findings V167-CP4-F4/F5: one-slot launch now validates only selected slot queues for running/completed state so other running slots do not block the selected slot; `validate_slot_queues()` and `slot_launch_response()` now take compact context dictionaries to stay within KISS parameter limits.

Checkpoint 5 implemented (approved by verifier after r3):
- Slot launch responses now explicitly include `auto_advance: false`, `next_up`, and reply text stating next queued PRDs require explicit go-ahead.
- Slot launch does not mutate `slot-queues.json`; launched heads remain in persisted queue state until the operator explicitly edits/clears/reorders the queue.
- Added regression coverage proving a head launch leaves the slot queue unchanged and exposes the next queued PRD as `next_up` rather than launching/removing it.
- Revision 2 fixes verifier finding V167-CP5-F1: explicit `continue slot A` / `launch next in slot A` paths now skip completed persisted heads only after explicit go-ahead, launch the next launch-ready PRD from the temporary launch plan, and still leave `slot-queues.json` unchanged.
- Revision 3 fixes verifier finding V167-CP5-F2: skipped completed heads are treated as satisfied blockers for explicit continue/launch-next validation, so normal dependent queues (`#71 blocked_by #70`) can continue after #70 is complete without mutating persisted slot state.

Checkpoint 6 implemented (approved by verifier):
- Added client-side slot-launch notification from AI Co-Worker chat/action responses when `queue_heads` is present.
- Board now exposes `window.onCoworkerSlotLaunch`, which refreshes term-control groups and reuses existing `markRunningChips()` behavior so launched PRD cards show the running animation/state.
- No terminal modal auto-open is introduced; the Co-Worker launcher only notifies the board to refresh groups.
- Added focused static tests proving the launcher calls the board refresh hook and does not open terminal groups.

Checkpoint 7 validation pass (approved by verifier):
- Ran PRD creation and launch metadata regression suites alongside all slot/coworker/board focused suites.
- Confirmed PRD creation tests still pass with launch metadata injection/readback and do not interact with slot queue persistence.
- Confirmed launch metadata audit/repair tests still pass with `prd/` branch and `/agentops-prd-<num>` worktree expectations used by slot validation.
- No additional product code changes were required for this checkpoint.

## Validation
- `PYTHONPATH=src:pipeline-diagram pytest tests/unit/test_slot_queues.py tests/unit/test_lane_plan.py tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py -q` → 40 passed.
- `PYTHONPATH=src:pipeline-diagram pytest tests/unit/test_review_server_coworker.py -q` → 38 passed (checkpoint 1 run).
- `PYTHONPATH=src:pipeline-diagram python3 -m py_compile src/agentops_harness/slot_queues.py src/agentops_harness/lane_plan.py src/agentops_harness/review_server.py pipeline-diagram/generate.py && PYTHONPATH=src:pipeline-diagram pytest tests/unit/test_review_server_coworker.py tests/unit/test_slot_queues.py tests/unit/test_lane_plan.py tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py -q && node --check pipeline-diagram/coworker-launcher.js` → 82 passed (checkpoint 2 r1), 83 passed after r2 fixes, 85 passed after checkpoint 3 r1, 89 passed after checkpoint 3 r2 fixes, 90 passed after human-approved CP3 r3, 93 passed after checkpoint 4 r1/r2 fixes, 94 passed after checkpoint 4 r3 fixes, 95 passed after checkpoint 5 r1, 96 passed after checkpoint 5 r2, 97 passed after checkpoint 5 r3, 98 passed + node syntax check after checkpoint 6.
- `PYTHONPATH=.:src:pipeline-diagram pytest tests/unit/test_prd_create.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_review_server_coworker.py tests/unit/test_slot_queues.py tests/unit/test_lane_plan.py tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py -q` → 126 passed for checkpoint 7 regression.
- Attempted `PYTHONPATH=src:pipeline-diagram pytest ... tests/unit/test_prd_launch_metadata.py ...`; blocked because that test file does not exist, then retried with actual metadata test files and `PYTHONPATH=.:src:pipeline-diagram` for intra-test imports.
- Steward final hygiene review returned clean after cache cleanup; removed `.pytest_cache/`, `pipeline-diagram/__pycache__/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/`.
- Final validation: `PYTHONPATH=src:pipeline-diagram python3 -m py_compile src/agentops_harness/slot_queues.py src/agentops_harness/lane_plan.py src/agentops_harness/review_server.py pipeline-diagram/generate.py && PYTHONPATH=.:src:pipeline-diagram pytest tests/unit/test_prd_create.py tests/unit/test_prd_launch_metadata_audit.py tests/unit/test_prd_launch_metadata_repair.py tests/unit/test_review_server_coworker.py tests/unit/test_slot_queues.py tests/unit/test_lane_plan.py tests/unit/test_pipeline_generate.py tests/unit/test_pipeline_board_generation.py -q && node --check pipeline-diagram/coworker-launcher.js && git diff --check` → 126 passed plus syntax/whitespace checks passed.
- Final verifier bug-check approved: decision `approved`, open findings `0`, bug-check status `passed`; report path `dev-plans/agentops/coder-verifier-workflow/runs/issue-167-ai-coworker-slot-queues/verifier-report.md`.
- `cd term-control-center && npm test -- tests/coworkerLauncher.test.ts` → blocked/fails before running tests because `term-control-center/node_modules` is missing and Node cannot import `tsx`; no `node_modules` directory is present in this worktree.
- Initial Python test attempt without `PYTHONPATH` failed to import local package/module; rerun with repo test path succeeded.

## Risks / notes
- Manual slot edit/reorder is implemented as a full-queue API replacement with validation; drag/drop UI affordances remain minimal and can build on `/coworker/slots/update`.
- Launch from slots is now implemented through chat/endpoint background launch. Existing `Execute plan` launch preview path remains separate for legacy pending implementation plans.
- Human decision received: use `lane-plan.json` as the overlap path source and do not expand the `plan-order.json` contract.
- Existing `plan-order.json` grouping remains available for sequencing order/dependency logic but is intentionally not displayed as a slot badge without explicit `slot-queues.json` state.
