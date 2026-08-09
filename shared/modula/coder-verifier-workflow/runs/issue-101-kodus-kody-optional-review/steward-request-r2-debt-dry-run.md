# Steward request — PRD #101 debt dry-run slice

```json
{
  "type": "peer_request",
  "sender": "coder",
  "target": "steward",
  "sender_cwd": "/mnt/hyperliquid-data/projects/worktrees/agentops-prd-101",
  "purpose": "Check changed-file placement and hygiene for PRD #101 debt issue dry-run/manual-approval controls before finalizing the slice.",
  "expected_response": "Concise markdown with clean/finding status. No file edits.",
  "stop_condition": "Return cleanup recommendations or clean."
}
```

## Scope

New/changed files for this slice:

- `src/agentops_harness/kodus_debt.py`
- `tests/unit/test_kodus_debt.py`
- `docs/kodus-debt-dry-run.md`
- `docs/kodus-agent.md`
- `pyproject.toml`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/review-request-r33-debt-dry-run.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/review-request-r34-debt-dry-run-revision.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/review-request-r35-debt-dry-run-bug-check.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/review-request-r36-debt-dry-run-bug-fix.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/verifier-report.md` modified by verifier.

Pre-existing untracked planning files to preserve but not include:

- `dev-plans/agentops/prd-101-next-steps-plan.md`
- `dev-plans/agentops/kody-review-session-prd-brief.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/continuation-prompt-20260629-kody-findings.md`

## Guardrails

- `kodus-debt-dry-run` is local dry-run only.
- No GitHub issue/comment/review mutation path, no automatic issue creation, no active Kody config, no required checks, no branch protection, no auto-merge, no PR approval/request-changes automation, no deployment, no secrets, no raw prompts/transcripts, no provider keys.

## Validation

- Relevant unit tests passed, 40 tests.
- Py compile passed.
- AST KISS check passed.
- `git diff --check` passed.
