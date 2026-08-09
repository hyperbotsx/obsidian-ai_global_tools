---
name: kody
description: "Trigger an optional advisory Kody/Kodus PR review from the CLI. Use when asked for /kody, kody review, trigger kody, start-review, rerun kody, or to request Kody review on an open GitHub PR. Works for Claude, Codex, and Pi agents."
---

# Kody Review Trigger

Trigger an advisory Kody/Kodus PR review for an open GitHub PR using the local `kodus-agent` facade. Kody is non-blocking and advisory only.

## Hard Rules

1. Never merge, approve, request changes, alter branch protection, or make Kody a required check.
2. Use authenticated `gh` and the local `kodus-agent` facade; do not post raw webhook payloads manually.
3. If the PR cannot be resolved, the PR is closed, or the Kody webhook relay fails, stop and report `needs_human`.
4. Do not store secrets, raw prompts, raw terminal logs, cookies, tokens, or environment dumps in artifacts.
5. If rerunning after an earlier Kody trigger, use `--force` only when the user asked to retry/rerun/force or when the prior trigger did not start a review.

## Phase 1. Resolve Target PR

Entry criteria: user asked to trigger or check a Kody review.

1. Resolve the repository:
   ```bash
   gh repo view --json nameWithOwner --jq .nameWithOwner
   ```
2. Resolve the PR number:
   - If the user supplied a PR number or URL, use it.
   - Else run:
     ```bash
     gh pr view --json number,url,state,headRefName,headRefOid
     ```
3. Confirm the PR is open:
   ```bash
   gh pr view <PR> --json state,url,headRefName,headRefOid
   ```

Exit criteria: you have `repo`, `pr`, `headRefName`, and `headRefOid` for an open PR.

## Phase 2. Trigger Kody

Entry criteria: target PR is open.

Run the facade from the installed command if available, otherwise from the global AgentOps harness source:

```bash
if command -v kodus-agent >/dev/null 2>&1; then
  kodus-agent request_review --repo <owner/repo> --pr <PR> --branch <headRefName> --head-sha <headRefOid>
else
  cd /mnt/hyperliquid-data/projects/repos/agentops-harness && \
    PYTHONPATH=src python3 -m agentops_harness.kodus_agent request_review \
      --repo <owner/repo> --pr <PR> --branch <headRefName> --head-sha <headRefOid>
fi
```

For an explicit retry/rerun/force request, add `--force`.

Exit criteria: command returns JSON with `status: requested` and a `commentUrl`.

## Phase 3. Confirm It Started

Entry criteria: Kody request returned successfully.

1. Wait briefly, then inspect PR activity:
   ```bash
   sleep 20
   gh pr view <PR> --repo <owner/repo> --json comments,reviews,statusCheckRollup,updatedAt
   ```
2. Treat any Kody/Kodus-authored comment, Kody PR summary, Kody review, or local `status: running` as triggered.
3. If no GitHub activity appears but `kodus-agent` reports local `status: running`, say it is locally running and GitHub output is pending.
4. If neither appears within a short wait, report `needs_human` with the trigger comment URL and webhook status.

## Phase 4. Report

Return:

- PR URL
- Kody trigger comment URL
- Webhook relay status
- Current Kody state: `requested`, `running`, `findings_ready`, `clean`, `failed`, or `needs_human`
- Any next action, such as “wait for review output” or “check Kody repo configuration”

## Quick Reference

| Intent | Command detail |
|---|---|
| First review | `request_review --repo <repo> --pr <PR> --branch <branch> --head-sha <sha>` |
| Retry/rerun | same command with `--force` |
| Status | `kodus-agent get_review_status --repo <repo> --pr <PR>` |
| Findings | `kodus-agent summarize_findings --repo <repo> --pr <PR>` |

## Success Criteria

- Kody trigger comment was posted through the facade.
- The webhook relay returned success, or failure is reported clearly.
- The user gets a concise status with the PR URL and trigger evidence.
