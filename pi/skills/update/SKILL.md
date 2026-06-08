---
name: update
description: Provide a non-invasive progress update during Evonome coder-verifier flows. Use when the user asks for /update, an update, progress, status, whether work is moving, what is next, or a quick human-readable plus technical summary without interrupting coder/verifier work.
---

# Update

## Essential Rules

1. Read-only only: do not edit files, send socket messages, deploy, run validation suites, create PRs, update issues, or change Git state.
2. Prefer local artifacts over GitHub/API calls so the update cannot block the active coder/verifier loop or hit rate limits.
3. Keep the answer concise and useful: a few plain-English sentences first, then technical bullets.
4. If artifacts are missing or inconsistent, report uncertainty instead of guessing.
5. Do not include raw transcripts, secrets, provider configuration, or long command output.

## When To Use

- The user asks for `/update`, progress, status, or whether the coder-verifier flow is moving.
- The user wants a non-interrupting summary during full-auto coder-verifier work.
- The user wants both an easy human-readable readout and a technical checkpoint summary.

## When Not To Use

- The user asks for verification, approval, rejection, or revisions; use the verifier workflow.
- The user asks for implementation; use the coder workflow.
- The user asks to create/update PRDs, GitHub issues, PRs, deployments, or code.

## Phase 1. Identify The Active Run

Entry criteria:
- User asks for a status/progress update.

Actions:
1. If the user supplied an artifact folder or file path, inspect that run.
2. Otherwise, find the most recently modified `coder-ready.md` under `dev-plans/agentops/coder-verifier-workflow/runs/`.
3. Read, when present:
   - `coder-ready.md`
   - `verifier-report.md`
   - `coder-handoff.md`
   - `decision-log.md`
4. Optionally run only light read-only shell checks such as `git status --short --branch` or `stat` when needed to compare timestamps.

Exit criteria:
- You have identified the active run or can explain why no run was found.

## Phase 2. Extract Status

Entry criteria:
- Active run artifacts were found.

Actions:
1. From `coder-ready.md`, extract current checkpoint, revision, requested verifier action, timestamp, changed files, validation claims, and notes.
2. From `verifier-report.md`, extract Machine Status: Decision, Checkpoint reviewed, Revision reviewed, Open findings, Bug-check status, and Next actor.
3. From `coder-handoff.md`, extract checkpoint table, known gaps, next pending checkpoint, branch, PRD, and non-goal boundaries.
4. From `decision-log.md`, extract the most recent checkpoint decision and gate truth.
5. If `coder-ready.md` is newer than `verifier-report.md`, say verifier review is probably pending.
6. If Machine Status is missing or invalid, say the flow may be blocked on verifier-report formatting.

Exit criteria:
- You can summarize progress, next actor, blockers, and safety boundaries.

## Phase 3. Respond

Entry criteria:
- Status facts were extracted or missing-artifact uncertainty is known.

Output format:

```markdown
Quick read: <2-4 human-readable sentences. Avoid jargon where possible. Say whether progress is happening and what is next.>

Technical status:
- PRD/run: <issue/branch/artifact folder if known>
- Latest coder checkpoint: <checkpoint/revision/requested action>
- Latest verifier status: <decision/open findings/next actor/bug-check status>
- Progress made: <approved/resolved checkpoints>
- Still blocked or pending: <remaining blockers or next checkpoint>
- Safety boundary: <validation/backtest/deployment/trading approval status>
```

Keep the response under 12 bullets unless the user asks for more detail.

Exit criteria:
- User receives a useful update without changing artifacts or interrupting the flow.
