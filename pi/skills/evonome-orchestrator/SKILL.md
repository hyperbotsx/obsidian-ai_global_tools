---
name: evonome-orchestrator
description: Recall and apply the Evonome orchestration workflow for GitHub Project 2 status summaries, next-action recommendations, PRD approval boundaries, agent/worktree ownership, coder/verifier coordination, AI Maestro visibility, and Hermes memory/chat constraints. Use when asked for Evonome project status, what to do next, orchestration rules, PRD workflow, CEO review semantics, agent ownership, AI Maestro/Hermes operator integration, or durable workflow memory.
---

# Evonome Orchestrator

## Core Contract

```text
Assistant gathers, remembers, summarizes, and recommends.
Human approves direction.
Coder/verifier agents execute scoped implementation and verification.
GitHub Project 2 remains the source of truth.
```

Use this skill as a recall and recommendation layer. Do not treat local memory, AI Maestro, Hermes, dashboards, Telegram, or chat messages as approval authority.

## Source Hierarchy

1. GitHub PRD issue bodies are canonical PRD text.
2. GitHub Project 2 fields are canonical execution state.
3. Coder/verifier artifacts are canonical checkpoint evidence for active implementation.
4. Repo history and issue comments are supporting evidence.
5. AI Maestro and Hermes memory are recall/cache only.

If sources conflict, required evidence is missing, or unsupported runtime paths are requested, fail closed: state the uncertainty, cite the source gap, and ask before recommending execution.

## Project 2 Status Summaries

Before answering status, next-work, priority, or "what is there to do" questions, read GitHub Project 2 and relevant issues. Summarize in this order:

1. Active `status:in-progress` work.
2. Ready `status:ready-for-agent` work.
3. Blocked work and blockers.
4. PRDs needing CEO review.
5. Future backlog only when requested.

Preferred commands:

```bash
gh issue list --repo hyperbotsx/SoldierOne --state open --label status:in-progress --json number,title,labels,url
gh issue list --repo hyperbotsx/SoldierOne --state open --label status:ready-for-agent --json number,title,labels,url
gh issue list --repo hyperbotsx/SoldierOne --state open --label status:blocked --json number,title,labels,url
gh project item-list 2 --owner hyperbotsx --limit 100 --format json
```

Recommendations should identify the next safe human decision, not silently mutate GitHub, launch agents, deploy, create branches, open PRs, merge, or approve workflows.

## PRD and CEO Review Rules

- A `type:prd` GitHub issue is the live PRD source.
- The full PRD belongs in the issue body.
- Do not create repo-local or Obsidian PRD copies as live sources of truth.
- Do not create or update repo-local `.agents/skills`, `.pi/skills`, `.claude/skills`, or `.codex/skills` folders for global Evonome orchestration skills.
- `/ceo review` is the approval gate for PRDs unless the human explicitly states another approval path.
- CEO approval must be explicit before implementation starts.
- Approval state belongs in the PRD issue and Project 2 fields.
- New ideas become follow-up issues unless the human explicitly changes current scope.

## Agent and Worktree Ownership

Use one owning agent/worktree per PRD unless the human marks the work shared.

| Area | Agent label | Worktree |
|---|---|---|
| Discovery | `agent:evonome-discovery` | `/mnt/hyperliquid-data/projects/worktrees/Evonome-discovery` |
| Training | `agent:evonome-training` | `/mnt/hyperliquid-data/projects/worktrees/Evonome-training` |
| Trading | `agent:evonome-trading` | `/mnt/hyperliquid-data/projects/worktrees/Evonome-trading` |
| Data, Predict, data services | `agent:evonome-data` | `/mnt/hyperliquid-data/projects/worktrees/Evonome-data` |
| Admin hardening and ops | `agent:evonome-admin` | `/mnt/hyperliquid-data/projects/worktrees/Evonome-admin` |

If ownership is unclear, recommend an owner decision before execution.

## Coder/Verifier Workflow

- Coder and verifier are separate roles.
- The coder reads the PRD first, records dirty-tree state, implements only bounded checkpoint slices, writes handoff artifacts, and runs validation.
- The verifier independently reviews the handoff, diff, evidence, and final bug-check.
- Medium and larger PRDs need verifier checkpoints by phase or meaningful implementation slice.
- PR creation is human-managed; do not create or open PRs unless the user explicitly asks.
- Do not merge, deploy, or approve trading/backtest/paper/live workflows without separate explicit approval.

## Authority Boundaries

Allowed by default:

- Read Project 2 and PRD issues.
- Summarize status and evidence.
- Recommend next actions.
- Point to the correct agent/worktree.
- Draft safe prompts or handoff text for human approval.

Not allowed without separate explicit approval:

- Approving PRDs.
- Mutating Project 2 fields.
- Creating branches.
- Launching coder/verifier sessions.
- Opening or merging PRs.
- Deploying.
- Executing trading, backtests, paper trading, or live workflows.
- Storing secrets, credentials, raw transcripts, or private account data.

## AI Maestro and Hermes

AI Maestro may be used as a non-canonical dashboard, visibility layer, or message fabric. It may consume Project 2 summaries and carry notifications to agents, but it must not replace GitHub Project 2 or execute mutations as an authority source.

Hermes may be used as a sandboxed recall assistant or future operator communication bridge. Hermes memory can store stable workflow facts, but it must not approve PRDs, mutate GitHub, launch agents, deploy, or operate trading/backtest/paper/live workflows.

Telegram or any external chat channel is only a future operator interface. Chat messages can request summaries or propose instructions; they cannot approve PRDs or execute privileged actions unless a separate gateway PRD defines authentication, audit, and confirmation behavior.

## Memory Policy

Prefer one durable orchestration memory substrate for convenience. If both AI Maestro and Hermes are present, seed only stable workflow facts and avoid duplicating live state that can drift.

Good memory facts:

- Human remains final orchestrator.
- GitHub Project 2 is the execution source of truth.
- PRDs live in GitHub issue bodies.
- Correct worktree/agent ownership matters.
- Coder/verifier sessions remain separate.
- Orchestration help is read-only and recommendation-first by default.
- Safety and stability beat shortcut speed.
- Implementation should use simple, practical, verified slices.
- AI Maestro is first a read-only status and message layer.
- Hermes/Telegram needs a separate gateway PRD before operator-command execution.

Never store credentials, tokens, private account data, raw transcripts, or secrets in memory.

## Quality Bar

Evonome orchestration should be institutional-grade, deliberate, practical, tested, auditable, deterministic, maintainable, boring, stable, observable, low-friction, and low-maintenance after setup.

## AgentOps Harness Split

Global skills stay in the AI Global Tools vault. AgentOps Harness issue #936 may define a future repository for portable executable orchestration code, docs, manifests, schemas, tests, and adapters, but that repository is not the skill source of truth.
