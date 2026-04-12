# Source of Truth Resolution Rules

Canonical root:

- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools`

## Global rule

This path is the master location for reusable:

- skills
- workflows
- prompts
- agent definitions
- templates
- MCP definitions
- shared tooling docs

This rule applies regardless of:

- current repo
- worktree
- cwd
- temporary execution directory
- whether the agent is operating in Claude, Codex, or another compatible tool

## Resolution order

When asked to use a skill, workflow, prompt, or shared agent asset:

1. check the tool-specific folder in this vault first
2. then check the shared folder in this vault
3. only use a repo-local copy if the user explicitly requests it or if no canonical vault copy exists

## Canonical lookup roots

### Claude

- `claude/skills/`
- `claude/prompts/`
- `claude/docs/`

### Codex

- `codex/skills/`
- `codex/prompts/`
- `codex/docs/`

### Shared

- `shared/skills/`
- `shared/prompts/`
- `shared/agents/`
- `shared/templates/`

### MCP

- `mcp/claude/`
- `mcp/codex/`
- `mcp/bin/`

## Interpretation rule

Repo-local copies should be treated as:

- mirrors
- compatibility shims
- experiments
- legacy copies

They should not be assumed to be authoritative unless the user explicitly says so.

## Maintenance rule

If a reusable skill or workflow changes, update the canonical copy in this vault first.
