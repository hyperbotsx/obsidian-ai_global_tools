# Coder handoff — issue #187 Discovery Backlog PRD composition

## Task
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/187
- Branch: `prd/discovery-backlog-prd-composition-187`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-187`

## Preflight
- Initial git status: clean (`## prd/discovery-backlog-prd-composition-187...origin/main`).
- Pre-existing dirty files: none.
- Allowed scope: Issue Logger, Discovery Backlog, AI Co-Worker issue-to-PRD composition, confirmation-gated PRD planner kickoff, tests/docs/run artifacts needed for #187.
- Forbidden scope: PR/merge/deploy/approval/trading/backtests; autonomous GitHub issue creation; PRD issue creation outside PRD Studio confirmation; source issue closure without explicit confirmation.
- Stop condition: final verifier bug-check approval after steward review because cross-cutting surfaces/artifacts changed.

## Research freshness summary
- Mandatory consult completed 2026-07-01 via `researcher`.
- GitHub: local `gh` is 2.63.2; use `gh issue create --label ... --body-file ...`, then `gh project item-add`, then `gh project item-edit` per field. Do not rely on `gh issue create --type`; local help lacks it. Preflight labels because `gh issue list --label missing` can look like an empty backlog.
- Repo labels present: `bug`, `enhancement`, `documentation`, `question`, `type:prd`, `agent:agentops`, `status:approved`, `status:draft`, `status:review-needed`. Missing semantic labels include `backlog`, `planned`, `investigation`, `ux`, `ops`, `improvement`, `feature`; missing labels must fail closed or require explicit fallback.
- Project 3 fields: Status (`Todo`, `In progress`, `Done`), Priority (`P0`, `P1`, `P2`), Size (`XS`..`XL`), Working Branch, Worktree Path, Base Branch. No dedicated Discovery Backlog/issue-type/source/sent-to-planner fields.
- PRD Studio: plus/new-PRD launches terminal PRD Studio Planner through `pipeline-diagram/board.html` -> `/launch` mode `prd-planning`; planner prompt receives `task.initialIdea`. Composer should seed this path, not call legacy `/prd/create` directly.

## Checkpoints
1. Issue Logger intent handling, active-session context capture, issue draft rendering, redaction, and preview behavior.
2. Confirmation-gated GitHub issue creation, label mapping, Project/profile scoping, and missing-label fail-closed behavior.
3. Discovery Backlog UI visibility, filtering, manual issue drafting/editing, and status/duplicate transitions.
4. Plus/new-PRD page option to generate from backlog issues while preserving freeform idea path.
5. AI Co-Worker backlog review and numbered issue-to-PRD proposal preview.
6. Grouping/splitting/parking rules and standalone recommendations.
7. Per-issue acceptance criteria and verifier checkpoint guidance in combined PRD seeds.
8. Confirmation-gated proposal selection and PRD maker/planner session kickoff.
9. Traceability from logged issue to source PRD/session to planner session to PRD issue.
10. Idempotency, duplicate prevention, and approval boundary regression pass.

## Current checkpoint
- Final verifier bug-check requested after implementation approval and steward cleanup.

## Changed files
- `src/agentops_harness/issue_logger.py`
- `src/agentops_harness/discovery_backlog.py`
- `src/agentops_harness/backlog_prd_composer.py`
- `src/agentops_harness/review_server.py`
- `pipeline-diagram/coworker-launcher.js`
- `pipeline-diagram/board.html`
- `tests/unit/test_review_server_coworker.py`
- `tests/unit/test_pipeline_board_generation.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-187-discovery-backlog-prd-composition/coder-handoff.md`

## Implemented in checkpoint 1
- Added AI Co-Worker Issue Logger intent recognition for approved phrases including `add to issue list`, `add to discovery backlog`, `park this for later`, `log this bug for later`, `save this as a follow-up idea`, `draft an issue for this`, and `ask coder to help explain this issue`.
- Added preview-only issue draft generation with title, type, body, semantic labels, project/session source context, and board references.
- Stored pending issue drafts in the AI Co-Worker session without calling the model or mutating GitHub.
- Reused existing Co-Worker redaction so issue drafts do not persist secrets or terminal blocks.
- Added clarification signaling for underspecified/redacted-only requests.

## Implemented in checkpoint 2
- Added confirmation-gated issue creation execution for pending Issue Logger drafts with exact confirmation text `create issue`.
- Added live label preflight through `gh label list` and fail-closed missing-label results before any `gh issue create` call.
- Added GitHub issue creation via `gh issue create --body-file --label` plus Project v2 linkage via `gh project item-add` after issue creation.
- Added project/profile scoping through `require_project_context` / active project resolution before creation.
- Added `/coworker/issues/create` to the Co-Worker surface allowlist and HTTP handler, returning blocked results for missing confirmation/labels.
- Added tests covering confirmed creation request shape, missing-label fail-closed behavior, pending draft retention on block, and route confirmation gating.

## Implemented in checkpoints 3-10
- Discovery Backlog list endpoint (`/coworker/backlog`) backed by GitHub Issues with live `backlog` label preflight and fail-closed missing-label result.
- Co-Worker UI controls for Create issue, Discovery Backlog, PRD proposal preview, and confirmation-gated PRD ideas.
- Confirmation-gated issue update/close/duplicate helper path for backlog issue edits.
- Plus/new-PRD page option `Generate PRD from backlog issues` that preserves freeform idea flow and seeds PRD Studio Planner from the first proposal preview.
- Backlog-to-PRD composer that groups open backlog issues, parks underspecified issues, returns numbered proposal groups, rationale, owner/surface, dependency notes, risk notes, seed idea prompt, and per-issue verifier checkpoints.
- Confirmation-gated selected proposal kickoff (`/coworker/backlog/kickoff`) that starts selected PRD Studio planner sessions only after exact `create PRD ideas` confirmation.
- Traceability in PRD seeds via source issue numbers/URLs and per-issue checkpoint guidance; source issues are not closed or marked implemented by planner kickoff.
- Duplicate/idempotency guardrails: pending issue drafts/proposals are consumed after successful creation/kickoff; repeat confirms require a matching pending id and cannot silently repeat.

## Findings addressed
- `V187-CP1-001`: extracted Issue Logger intent/draft/preview helpers from the oversized `review_server.py` into focused module `src/agentops_harness/issue_logger.py`; `review_server.py` now retains only the AI Co-Worker session hook/import for this feature.
- `V187-CP2-001`: blocked confirmed creation for drafts still requiring clarification and added coverage proving no target/label lookup or creator call occurs.
- `V187-CP2-002`: added pre-`gh issue create` target setup validation for repository/project owner/project number and coverage proving incomplete Project setup blocks creation.
- `V187-CP2-003`: reduced `execute_issue_creation` to 3 parameters by grouping labels/target/creator in a context dict.
- `V187-CP3-10-001`: added status filtering against GitHub issue state, richer edit/update handling, and safe duplicate transition requiring a duplicate target.
- `V187-CP3-10-002`: composer now parks duplicate/planned/fixed/stale/underspecified items and splits by type, owner, surface, and risk; missing surface defaults to standalone proposals.
- `V187-CP3-10-003`: UI now prompts for numbered proposal selection rather than hardcoding proposal 1; plus/new-PRD seed path shows numbered preview and requires selecting one proposal.
- `V187-CP3-10-004`: planner kickoff now launches sequentially, reports partial failures with per-group errors, and only clears pending proposal on full success.
- `V187-CP3-10-005`: reduced new checkpoint function signatures by grouping update/kickoff inputs in request/context dictionaries.
- `V187-CP3-10-006`: backlog listing/proposal now filters by active project/profile metadata (`- Project/profile:` marker or `project:<id>` label), excluding cross-project backlog issues by default.
- `V187-CP3-10-007`: backlog summaries, titles, proposal seeds, and edit payloads now use existing redaction via `redact_evidence` plus terminal-block redaction.
- `V187-CP3-10-001` follow-up: duplicate transition now writes a `Duplicate of #<target>` GitHub comment plus duplicate label instead of dropping the target.
- `V187-CP3-10-004` follow-up: partial planner kickoff records successful proposal ids and removes them from pending proposals so retry cannot relaunch already-started groups.
- `V187-CP3-10-008`: added pending issue draft edit route/helper/UI before GitHub creation; edited title/body/type/priority/status/labels are stored in the pending draft and used by confirmed creation. Type-only edits now keep the persisted body `## Type` section consistent.

## Validation
- `python -m pytest tests/unit/test_review_server_coworker.py -q` — failed: `python` not available.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q` — passed, 61 tests.
- `PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py` — passed after `V187-CP1-001` fix.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q` — passed after checkpoint 2, 64 tests.
- `PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py` — passed after checkpoint 2.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py` — passed after CP2 fixes, 66 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py` — passed after checkpoints 3-10, 83 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py && node --check pipeline-diagram/coworker-launcher.js` — passed after checkpoints 3-10 fixes, 87 tests plus compileall/node check.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py && node --check pipeline-diagram/coworker-launcher.js` — passed after second checkpoints 3-10 fixes, 90 tests plus compileall/node check.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py && node --check pipeline-diagram/coworker-launcher.js` — passed after V187-CP3-10-007/008 fixes, 91 tests plus compileall/node check.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py && node --check pipeline-diagram/coworker-launcher.js` — passed after type/body consistency fix, 92 tests plus compileall/node check.
- `V187-FINAL-001`: fixed Co-Worker action UI error handling so non-2xx fail-closed/partial responses surface `reply` / `response_text` / `reason` plus top-level and nested `label_resolution` missing labels/fields instead of opaque HTTP status only.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 - <<'PY' ... compile changed modules ... PY && node --check pipeline-diagram/coworker-launcher.js && git diff --check` — passed after final bug-check fix, 93 tests plus compile/diff checks.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 - <<'PY' ... compile changed modules ... PY && node --check pipeline-diagram/coworker-launcher.js && git diff --check` — passed after nested missing-label/field UI fix, 93 tests plus compile/diff checks.
- Steward pre-final review — cleanup recommended for generated caches only.
- `rm -rf .pytest_cache src/agentops_harness/__pycache__ tests/unit/__pycache__ pipeline-diagram/__pycache__` — completed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py tests/unit/test_pipeline_board_generation.py -q && PYTHONPATH=src python3 -m compileall -q src/agentops_harness/review_server.py src/agentops_harness/issue_logger.py src/agentops_harness/discovery_backlog.py src/agentops_harness/backlog_prd_composer.py && node --check pipeline-diagram/coworker-launcher.js` — final pre-bug-check validation passed, 92 tests plus compileall/node check.
- Generated caches removed again after final validation.

## Notes / risks
- Current live repo is expected to fail closed on real Discovery Backlog creation/listing until the `backlog` label exists or a separately approved fallback is implemented.
- Planner kickoff uses the existing term-control `/launch` path with PRD Studio planning mode. It does not create/approve GitHub PRD issues.
- Final steward review is still required before verifier bug-check because new modules, run artifacts, and UI affordances were added.
