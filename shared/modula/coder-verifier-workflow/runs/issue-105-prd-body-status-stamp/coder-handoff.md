# Coder handoff — Issue #105 PRD body status stamp

## Source of truth
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/105
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-105`
- Branch: `prd/c1-prd-stamp-prd-body-status-105`

## Pre-edit state
- `git status --short --branch`: clean branch `prd/c1-prd-stamp-prd-body-status-105...origin/main`.
- Pre-existing dirty files: none.
- Memory: disabled/advisory per launch warning; not used.

## Scope controls
- Allowed paths: `src/agentops_harness/prd_closeout.py`, `src/agentops_harness/prd_closeout_github.py`, focused closeout body-stamp helper/tests, run artifacts under this folder.
- Forbidden scope: PR creation, merge, deploy, trading/backtests, human-gate bypass, retroactive mass rewrite of closed PRDs, unrelated routes/navigation/product code/secrets/transcripts.
- Stop condition: final verifier implementation approval plus final bug-check approval, or human escalation.

## Verifier checkpoints
1. Stamp checkpoint: closeout stamps PRD body status fields, timestamp, and merged PR URL.
2. Robustness checkpoint: header blockquote and `## Status` formats are handled, only known fields change, second run is no-op.
3. Fail-safe checkpoint: ambiguous/unparseable bodies warn and do not block close/comment/Project mutations.
4. Regression checkpoint: existing closeout safeguards, Project field edits, evidence comment, and repository isolation remain unchanged.

## Implementation summary
- Added `src/agentops_harness/prd_closeout_body.py` with table-driven body stamping for recognized fields in the header blockquote or a single `## Status` section.
- `Implementation status`, `Status`, and `PRD status` become `Done`; `Ready for implementation` becomes `No — implemented`.
- Existing `Implemented at`/`Closed at` and `Implementation PR`/`Merged PR` fields are updated on first stamp; an already completed body with the same implementation PR is a no-op on later retries even when the new closeout timestamp differs.
- If metadata is absent, `Implemented at` and `Implementation PR` are added to the recognized status block.
- Absent core status fields are skipped rather than invented; metadata is added when at least one recognized status field exists.
- Ambiguous bodies (multiple `## Status` sections or duplicate recognized fields inside one target block), missing bodies, read/edit failures, and no-recognized-field bodies produce concise warnings and the rest of closeout proceeds.
- `execute_closeout` now delegates body read/edit to `src/agentops_harness/prd_closeout_body_github.py`, optionally edits before the evidence comment, includes body-stamp status in the evidence comment, and preserves existing closeout readback behavior.
- `build_closeout_plan` mutation list now includes `stamp PRD body status fields` for preview visibility.

## Verifier finding fixes
- F105-R1-001: added `PRD status` recognition and representative `## Status` regression coverage.
- F105-R1-002: preserved existing implemented/closed timestamps on already completed same-PR reruns; retry idempotency test now uses a later timestamp.
- F105-R1-003: extracted GitHub issue body read/edit/comment-status helpers into `prd_closeout_body_github.py`; `prd_closeout_github.py` is now 292 lines.
- HYG-105-R2-001: removed generated ignored caches: `.pytest_cache/`, `src/agentops_harness/__pycache__/`, `tests/unit/__pycache__/`, and `pipeline-diagram/__pycache__/`.

## Changed files
- `src/agentops_harness/prd_closeout.py`
- `src/agentops_harness/prd_closeout_body.py`
- `src/agentops_harness/prd_closeout_body_github.py`
- `src/agentops_harness/prd_closeout_github.py`
- `tests/unit/test_prd_closeout_body.py`
- `tests/unit/test_prd_closeout_github.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-105-prd-body-status-stamp/coder-handoff.md`

## Validation evidence
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_closeout_body.py tests/unit/test_prd_closeout_github.py tests/unit/test_prd_closeout.py` — passed, 31 tests before verifier fixes; passed, 32 tests after verifier fixes.
- `python3 -m py_compile src/agentops_harness/prd_closeout.py src/agentops_harness/prd_closeout_body.py src/agentops_harness/prd_closeout_body_github.py src/agentops_harness/prd_closeout_github.py tests/unit/test_prd_closeout_body.py tests/unit/test_prd_closeout_github.py` — passed.
- `git diff --check -- src/agentops_harness/prd_closeout.py src/agentops_harness/prd_closeout_body.py src/agentops_harness/prd_closeout_body_github.py src/agentops_harness/prd_closeout_github.py tests/unit/test_prd_closeout_body.py tests/unit/test_prd_closeout_github.py` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit -q` — failed in 4 unrelated environment-sensitive tests (`test_agent_github_health.py`, `test_ai_maestro_handoff_emit.py`, `test_github_cli_env.py`); 942 passed.
- `git status --ignored --short | grep -E '(__pycache__|\.pytest_cache)' || true` — passed after cleanup; no cache paths listed.

## Batch validation ledger directive
- Evidence is recorded in this handoff for the shared batch validation ledger/log window from the PRD directive.

## Final verifier status
- Revision 3 verdict: approved.
- Bug-check status: passed.
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-105-prd-body-status-stamp/verifier-report.md`.

## Open items
- None for coder. Human-managed next steps only; no PR was created.
