# Steward request — PRD #101 token lifecycle controls slice

```json
{
  "type": "peer_request",
  "sender": "coder",
  "target": "steward",
  "sender_cwd": "/mnt/hyperliquid-data/projects/worktrees/agentops-prd-101",
  "purpose": "Check changed-file placement and hygiene for PRD #101 token expiry/refresh validation controls before finalizing the slice.",
  "expected_response": "Concise markdown with clean/finding status. No file edits.",
  "stop_condition": "Return cleanup recommendations or clean."
}
```

## Scope

New/changed files for this slice:

- `src/agentops_harness/kodus_token_smoke.py`
- `tests/unit/test_kodus_token_smoke.py`
- `docs/kodus-token-lifecycle.md`
- `docs/kodus-kody-sprint1-advisory-pilot.md`
- `pyproject.toml`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/coder-handoff.md`
- Review requests r38-r42.
- `verifier-report.md` modified by verifier.

Pre-existing untracked planning files to preserve but not include:

- `dev-plans/agentops/prd-101-next-steps-plan.md`
- `dev-plans/agentops/kody-review-session-prd-brief.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/continuation-prompt-20260629-kody-findings.md`

## Guardrails

- `kodus-token-smoke` is non-mutating and reads token values only from operator-provided env vars.
- No repo-stored secrets, no live Kodus config, no generated token evidence output, no GitHub issue/comment/review mutation path, no required checks, no branch protection, no auto-merge, no PR approval/request-changes automation, no deployment, no raw prompts/transcripts, no provider keys.

## Validation

- Relevant unit tests passed, 46 tests.
- Py compile passed.
- AST KISS check passed.
- `git diff --check` passed.
