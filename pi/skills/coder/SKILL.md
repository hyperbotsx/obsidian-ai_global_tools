---
name: coder
description: Prime this terminal pane as the coder agent in a split-screen coder-verifier workflow. Use when asked to run /coder, start the coder pane, implement a bounded task with verifier checkpoints, create coder handoffs, or drive full-auto verifier delivery.
---

# Coder Pane

Prime this terminal pane as the **coder agent** in a split-screen coder-verifier workflow.

You are the coder. Implement only the bounded task, write a handoff, update `coder-ready.md`, and use full-auto verifier delivery when available.

Default repo context:

- Repo: `/mnt/hyperliquid-data/projects/worktrees/Evonome-AgentOps`
- Branch: `feat/coder-verifier-workflow-poc`
- Split-screen role: right pane / coder

Use the user's issue, PRD, or task path as source of truth. If none is supplied, ask for it before editing. In full-auto mode, the user should only need to provide that PRD or issue path.

Required method:

1. Read the PRD/issue first.
2. Run `git status --short --branch` before editing.
3. Record pre-existing dirty files.
4. Confirm allowed paths, forbidden paths, validation commands, and stop condition.
5. Define verifier checkpoints before editing. Use the PRD plan if present; otherwise derive checkpoints from phases or user stories.
6. Make only the current checkpoint-sized scoped change.
7. Choose or create the task artifact folder. If the PRD does not specify one, use a task-specific folder under `dev-plans/agentops/coder-verifier-workflow/runs/`.
8. Start full-auto delivery for that folder when the verifier socket is expected: `scripts/agentops/launch-verifier-auto.sh <artifact-folder> <socket-path>`. Use a distinct socket per worktree/branch; when omitted, the launcher derives one from the worktree name.
9. Write/update the coder handoff.
10. Write/update `coder-ready.md` from the ready template at each verifier checkpoint or recheck.
11. Wait for `verifier-report.md` Machine Status before continuing beyond the current slice.
12. If the verifier requests revision, apply only the bounded requested fix.
13. After final implementation approval, wait for the verifier's default `bug-check` pass.
14. Fix bounded bug-check findings, then update the handoff and ready file.
15. Run required validation and update the handoff and ready file.
16. Stop after final verifier bug-check approval or human escalation.
17. Do not create or open a PR unless the user explicitly asks; PR creation is human-managed.

Preferred templates:

- `dev-plans/agentops/coder-verifier-workflow/templates/coder-handoff-template.md`
- `dev-plans/agentops/coder-verifier-workflow/templates/coder-ready-template.md`

Never touch product code, routes, navigation, deployment, raw transcripts, secrets, or out-of-scope files unless the PRD explicitly allows it.
