# PRD #101 closeout decision packet — 2026-07-01

This packet is draft text only. Do not post to GitHub, close issues, or create follow-up issues without explicit operator approval.

## Current closeout posture

PRD #101 has delivered the advisory Kody/Kodus pilot foundations through merged PRs #177, #182, #184, #189, and #196. The only material PRD #101 gap that still requires live operator action is actual token expiry or forced-revoke evidence. Broader Git Manager / Code Reviewer workflow is split into PRD #190.

## Option 1 — Keep PRD #101 open

Use when the operator wants actual token expiry/revoke evidence before closing.

Next action:

1. Run the forced-revoke or natural-expiry path from `docs/kodus-token-lifecycle.md`.
2. Fill `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/token-lifecycle-evidence-template-20260701.md` with sanitized evidence.
3. Ask verifier to review the evidence.
4. Post a closeout comment only after verifier approval and operator confirmation.

## Option 2 — Split remaining token evidence into a follow-up issue

Use when the operator accepts the implemented pilot controls but wants credential validation tracked separately.

Status: completed. Follow-up issue created at https://github.com/hyperbotsx/agentops-harness/issues/198.

Draft follow-up issue title:

```text
PRD #101 follow-up: operator-run Kodus token expiry/revoke validation evidence
```

Draft follow-up issue body:

```markdown
## Goal

Complete PRD #101 token lifecycle evidence with an operator-run near-expiry or forced-revoke Kodus GitHub token test using `docs/kodus-token-lifecycle.md`.

## Scope

- Use an operator-owned test token outside the repository.
- Run `kodus-token-smoke --require-write` for replacement-token validation.
- Configure, revoke, and replace the token only in local Kodus/runtime secret storage outside the repo.
- Trigger one advisory Kody review before and after expiry/revoke/replacement.
- Record sanitized evidence only.

## Forbidden

- No repo-stored tokens, `.env` files, screenshots with token values, raw terminal logs, raw prompts/transcripts, branch protection changes, required checks, auto-approval/request-changes, auto-merge, or automatic debt issues.

## Acceptance criteria

- Expired/revoked token fails closed or cannot post/read GitHub data.
- Replacement token passes smoke and one advisory Kody review.
- Logs/artifacts do not contain token values.
- No automatic issue creation, required checks, branch-protection change, approval/request-changes, or merge behavior is observed.
- Sanitized evidence is linked back to PRD #101.
```

## Draft PRD #101 closeout comment if split is accepted

```markdown
PRD #101 closeout assessment after PR #196:

Merged implementation evidence:
- PR #177: Sprint 0 feasibility, local Claude/Codex gateway pilot, sandbox/runbook, advisory trigger.
- PR #182: sandbox console-output sanitization fix.
- PR #184 / issue #179: observable Kody review sessions and explicit fix-loop UX/state.
- PR #189: `kodus-agent` advisory CLI facade.
- PR #196: inactive rule pack, debt dry-run/manual-approval controls, token smoke helper/runbook.

Guardrails preserved: Kodus/Kody remains optional and advisory; no required checks, branch protection changes, auto-merge, PR approval/request-changes automation, automatic debt issue creation, repo-stored secrets, raw prompts/transcripts, or runtime config were added.

Remaining scope is split/deferred: operator-run token expiry/revoke validation is tracked in #198, and any broader provider-terms decision must be recorded before broader rollout.
```

## Option 3 — Close PRD #101 without split

Not recommended unless the operator explicitly accepts token expiry/revoke validation as deferred outside PRD tracking. If chosen, the closeout comment should state the deferral plainly and preserve the no-broader-rollout boundary.

## PR description addendum for the next PR from this branch

```markdown
### Additional PRD #101 planning artifacts

- Refreshed `dev-plans/agentops/prd-101-next-steps-plan.md` to reflect merged PRs #184, #189, and #196.
- Added a sanitized token lifecycle evidence template for future operator-run expiry/revoke validation.
- Added a closeout decision packet with draft follow-up issue and closeout comment text.

These are planning/run artifacts only. No product code, routes, workflows, branch protection, required checks, auto-merge, approval/request-changes automation, automatic debt issues, secrets, runtime config, raw prompts/transcripts, or live token evidence were added.
```
