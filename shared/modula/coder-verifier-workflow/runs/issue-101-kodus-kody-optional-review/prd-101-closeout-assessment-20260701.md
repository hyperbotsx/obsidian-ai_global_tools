# PRD #101 closeout assessment — 2026-07-01

## Source of truth

- GitHub PRD issue: https://github.com/hyperbotsx/agentops-harness/issues/101
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-101`
- Branch inspected: `prd/kody-rule-pack-101`
- Current main merge commit reported by operator/verifier: `a522e78` from PR #196

## Pre-edit status

`git status --short --branch` before this assessment showed:

```text
## prd/kody-rule-pack-101...origin/prd/kody-rule-pack-101
?? dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/continuation-prompt-20260629-kody-findings.md
?? dev-plans/agentops/kody-review-session-prd-brief.md
?? dev-plans/agentops/prd-101-next-steps-plan.md
```

Preserved untracked planning files remain in place.

## Scope boundaries for this checkpoint

Allowed:

- Read PRD #101, related GitHub issues/PRs, docs, and run artifacts.
- Write a planning-only closeout assessment in this run folder.
- Ask verifier for checkpoint review before any commit or GitHub mutation.

Forbidden:

- No product code, routes, workflows, branch protection, required checks, PR approval/request-changes automation, auto-merge, deployment, secrets, tokens, raw prompts/transcripts, runtime config, live Kodus config, or debt issue mutation.
- No closing PRD #101 or creating follow-up GitHub issues without explicit human instruction.

Validation for this checkpoint:

- Read-only GitHub issue/PR inspection through `gh`.
- Local docs/artifact inspection.
- `git status --short --branch` after writing this assessment.

Stop condition:

- Stop after verifier agrees this assessment is accurate, or escalate to human if verifier finds PRD closeout ambiguity.

## Completed PRD #101 scope

| PRD area | Evidence | Assessment |
| --- | --- | --- |
| Sprint 0 feasibility gate | PR #177, docs and run artifacts in the issue #101 run folder | Complete for local sandbox pilot. Claude primary and Codex fallback were validated through the local OpenAI-compatible gateway; log privacy mitigation and queue/rate-limit behavior were recorded. |
| Kody advisory/non-blocking posture | PRs #177, #184, #189, #196 | Preserved. No required checks, branch-protection changes, auto-approve/request-changes, merge automation, or production rollout were added. |
| Manual optional post-PR trigger | PR #177 and follow-up fixes in PR #182 | Complete for the first slice, including live PR-state guard, async trigger path, and duplicate-comment rollback on webhook relay failure. |
| Observable Kody review sessions/fix loop | Follow-up PRD #179, merged PR #184, `docs/kody-review-sessions.md` | Split and implemented as a separate PRD slice. Issue #179 is closed. |
| `kodus-agent` CLI facade | PR #189, `docs/kodus-agent.md` | Complete for MVP commands: request, status, summary, export, unsupported cancel, advisory-only outputs. |
| Kody rule pack and repo overlay process | PR #196, `docs/kody-rule-pack.md` | Complete as inactive advisory rules plus activation/tuning/rollback guidance. Rules are not in an auto-synced path. |
| Debt issue pilot controls | PR #196, `docs/kodus-debt-dry-run.md`, `kodus-debt-dry-run` | Complete for dry-run/manual-approval proposal generation only. No GitHub issue mutation path was added. |
| Token replacement smoke helper and runbook | PR #196, `docs/kodus-token-lifecycle.md`, `kodus-token-smoke` | Complete for non-secret replacement-token smoke and documented forced-expiry/revoke procedure. |

## Remaining closeout gaps

1. **Actual operator-run token expiry or forced-expiry evidence is still incomplete.**
   - PR #196 intentionally added safe controls and a helper, but did not run the live expiry/revoke scenario because it requires operator-owned credentials and live Kodus configuration outside the repository.
   - `docs/kodus-token-lifecycle.md` still states actual expiry/refresh remains incomplete until a near-expiry or forced-expiry test runs.

2. **Broader CLI-as-local-gateway subscription terms approval is not explicitly closed in PRD #101.**
   - The sandbox pilot has evidence and merged implementation slices, but issue #101's original CEO comment approved Sprint 0 only and deferred broader Sprint 1+ rollout unless evidence and human decisions were recorded.
   - If the operator considers merged pilot PRs sufficient acceptance, record that explicitly in the PRD closeout comment. Otherwise track a follow-up legal/provider-terms decision.

3. **PRD #190 covers the larger Git Manager / Code Reviewer workflow and remains open.**
   - This appears to split broader Kody review-loop coordination into a separate approved PRD.
   - It should be referenced as follow-up scope rather than treated as a blocker for the already-implemented PRD #101 pilot slices.

## Recommendation

Do **not** close PRD #101 automatically from this coder checkpoint.

Safe next human choices:

1. **Run token lifecycle validation now** using the `docs/kodus-token-lifecycle.md` forced-expiry/revoke path, then add sanitized evidence to the issue #101 run folder and closeout comment.
2. **Split the token lifecycle validation and provider-terms decision into explicit follow-up issue(s)**, then close PRD #101 with a comment linking merged PRs and the follow-up(s). Token lifecycle validation has been split to https://github.com/hyperbotsx/agentops-harness/issues/198.
3. **Keep PRD #101 open** until the operator can run the token expiry/revoke scenario with non-repo secrets.

## Draft follow-up issue: token lifecycle evidence

Title:

```text
PRD #101 follow-up: operator-run Kodus token expiry/revoke validation evidence
```

Body:

```markdown
## Goal

Complete PRD #101 token lifecycle evidence with an operator-run near-expiry or forced-revoke Kodus GitHub token test using the safe runbook in `docs/kodus-token-lifecycle.md`.

## Scope

- Use an operator-owned test token outside the repository.
- Run `kodus-token-smoke --require-write` for replacement-token validation.
- Configure/revoke/replace token only in local Kodus/runtime secret storage outside the repo.
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

## Draft PRD #101 closeout comment, if human chooses split/close

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
