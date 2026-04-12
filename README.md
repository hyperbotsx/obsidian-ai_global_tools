# AI_Global_Tools

This vault is the source of truth for reusable agent tooling across Claude Code and Codex.

## Canonical resolution rule

Treat this absolute path as the master location regardless of the current repo or working directory:

- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools`

When an agent is asked to use a skill, workflow, prompt, agent definition, template, or MCP definition, resolve it from this vault first.

Lookup priority:

1. tool-specific canonical folder in this vault (`claude/` or `codex/`)
2. shared canonical folder in this vault (`shared/`)
3. legacy repo-local copies only if the user explicitly asks for them or no canonical vault copy exists

Repo-local duplicates should be treated as mirrors, compatibility shims, or legacy copies unless explicitly declared authoritative by the user.

## Canonical contents

- `shared/prompts/system/`
- `shared/prompts/library/`
- `shared/agents/`
- `shared/skills/`
- `shared/templates/`
- `claude/skills/`
- `claude/prompts/system/`
- `codex/skills/`
- `codex/prompts/system/`
- `mcp/`

Notable reusable pattern docs:

- `LLM-Wiki-Pattern.md`
- `shared/templates/llm-wiki/`
- `shared/skills/herdr/`

## Safety boundary

This vault is intended for reusable tooling content, not secrets.

Keep these **outside** the vault:

- API keys
- auth tokens
- credential JSON files
- transient logs, history, and session state
- secret-bearing MCP environment values

## Runtime bridges

The user home directory still contains the live runtime locations expected by the CLIs, but those locations now point back here where possible via symlinks and launch wrappers.
