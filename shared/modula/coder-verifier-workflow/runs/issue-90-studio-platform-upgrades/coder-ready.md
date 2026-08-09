# Coder Ready

## Coordination Status

- Checkpoint: `Final bug-check`
- Revision: `11`
- Requested verifier action: `recheck_finding`
- Timestamp: `2026-06-21T20:25:35Z`

## Review Inputs

- PRD: `GitHub issue #90 (canonical PRD source)`
- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/90`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades`
- Coder handoff: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/coder-handoff.md`
- Decision log: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/decision-log.md`

## Changed Files

- full cumulative changed-file set is listed in `coder-handoff.md`
- bounded final-fix files:
  - `src/agentops_harness/github_cli_env.py`
  - `src/agentops_harness/ceo_review_source.py`
  - `src/agentops_harness/ceo_review_mutations.py`
  - `src/agentops_harness/ceo_review_evonome_apply.py`
  - `src/agentops_harness/prd_create.py`
  - `docs/operations.md`
  - `tests/unit/test_github_cli_env.py`
  - `tests/unit/test_ceo_review_source.py`
  - `tests/unit/test_prd_create.py`
  - `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/coder-handoff.md`
  - `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/coder-ready.md`
  - `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/decision-log.md`

## Validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_github_cli_env.py tests/unit/test_ceo_review_source.py tests/unit/test_prd_create.py`: `pass`
- `PYTHONPATH=src python3 -m pytest tests/unit`: `pass`
- `npm --prefix term-control-center run test`: `pass`
- `npm --prefix term-control-center run typecheck`: `pass`
- `npm --prefix term-control-center run build`: `pass`
- `git diff --check`: `pass`

## Findings Addressed

- `V-FINAL-001`: agent-side `gh` invocations now use a dedicated `GH_CONFIG_DIR` / optional dedicated token env instead of inheriting the operator’s default `gh` auth context.

## Notes For Verifier

- Scope is a bounded final bug-check recheck only.
- The fix does not change product behavior beyond agent-side GitHub auth isolation.
- Dedicated runtime config is documented in `docs/operations.md` (`AGENTOPS_GH_CONFIG_DIR`, `AGENTOPS_GITHUB_TOKEN`).
