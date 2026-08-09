Coder readiness changed. Re-check now.

Read first:
dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-ready.md

Then verify against:
dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-handoff.md
dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/decision-log.md
all changed files named in coder-ready.md

Run preflight first when available:
scripts/agentops/verifier-preflight.py dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690

For browser-visible checkpoints, apply Browser QA / DevTools verification against the resolved preview URL or record why it was skipped.

Run safe validation, including:
git diff --check

Update:
dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/verifier-report.md

Include the complete Machine Status block with decision, checkpoint reviewed, revision reviewed, open findings, bug-check status, and next actor. Do not edit coder-owned files.

--- CODER READY SNAPSHOT ---
# Coder Ready

## Coordination Status

- Checkpoint: `Final PRD #940 completion review`
- Revision: `32`
- Requested verifier action: `recheck_finding`
- Timestamp: `2026-06-08T18:16:27Z`

## Review Inputs

- PRD: `GitHub issue #940`
- GitHub issue: `https://github.com/hyperbotsx/SoldierOne/issues/940`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690`
- Coder handoff: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-handoff.md`
- Decision log: `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/decision-log.md`
- Verifier socket: `/tmp/agentops/pi-verifier-agentops-harness.sock`

## Changed Files

- `src/agentops_harness/prd_preflight.py`
- `src/agentops_harness/profile_setup.py`
- `src/agentops_harness/cli.py`
- `profiles/evonome.example.yaml`
- `tests/unit/test_prd_preflight.py`
- `tests/unit/test_profile_setup.py`
- `tests/unit/test_cli.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/decision-log.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/session-1780932558690/coder-ready.md`

## Validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py tests/unit/test_profile_setup.py tests/unit/test_cli.py && git diff --check`: `pass`
- `PYTHONPATH=src python3 -m pytest && git diff --check`: `pass`

## Findings Addressed

- `V-FINAL-003`: `--show-preview-target` now requires a configured preview URL and blocks missing mappings.
- `V-FINAL-004`: profiles now support persisted `ephemeral_globs`; generated/example profiles include coder/verifier run artifacts; profile-backed preflight consumes those globs.

## Notes For Verifier

- This is a final completion recheck for `V-FINAL-003` and `V-FINAL-004`.
- No PR creation, merge, or tracker update is requested.
- Preview target is not configured for this worktree; Browser QA is not required for this non-browser checkpoint.
--- END ---
