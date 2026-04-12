# AI Global Tools Home

Welcome to your master vault for reusable agent tooling.

## Start here

- [[obsidian-ai_global_tools/README]] — purpose and safety boundary
- [[Using-AI_Global_Tools]] — how Claude, Codex, and Pi consume this vault
- [[Global-Agent-Source-of-Truth-Plan]] — migration plan and decisions
- [[LLM-Wiki-Pattern]] — concrete operating model for persistent LLM-maintained wikis
- [[obsidian-ai_global_tools/shared/templates/llm-wiki/README]] — reusable LLM Wiki templates
- [[obsidian-ai_global_tools/mcp/README]] — canonical MCP layout

## Runtime bridges

### Claude Code
- Wrapper: `~/.local/bin/claude`
- Skills source: `[[claude/skills]]`
- System prompt: `[[claude/prompts/system/claude-global]]`
- MCP config: `[[mcp/claude/mcp-config.json]]`
- Notes: `[[claude/docs/runtime-bridge]]`

### Codex
- Wrapper: `~/.local/bin/codex`
- Skills source: `[[codex/skills]]`
- Global prompt: `[[codex/prompts/system/codex-global]]`
- Config source: `[[mcp/codex/config.toml]]`
- Notes: `[[codex/docs/runtime-bridge]]`

### Pi
- Skills source: `[[pi/skills]]`
- Agents source: `[[pi/agents]]`
- Notes: `[[pi/docs/runtime-bridge]]`

## Canonical edit locations

### Shared
- `[[shared/prompts/system/global-operator-principles]]`
- `[[shared/prompts/library/README]]`
- `[[shared/agents/README]]`
- `[[shared/skills/README]]`
- `[[shared/skills/herdr/SKILL]]`

### Claude-specific
- `[[claude/skills]]`
- `[[claude/prompts/system/claude-global]]`
- `[[claude/prompts/library]]`

### Codex-specific
- `[[codex/skills]]`
- `[[codex/prompts/system/codex-global]]`
- `[[codex/prompts/library]]`

### MCP
- `[[mcp/README]]`
- `[[mcp/claude/mcp-config.json]]`
- `[[mcp/codex/config.toml]]`
- `[[mcp/bin]]`

### Pi-specific
- `[[pi/skills]]`
- `[[pi/agents]]`

## Safety boundary

Keep these **outside** the vault:

- API keys
- auth tokens
- credential JSON files
- secret-bearing MCP env values
- transient logs, session history, and caches

External secrets file:

- `~/.config/ai-global-tools/mcp-secrets.env`

## Quick verification

```bash
type -a claude
type -a codex
readlink -f ~/.claude/skills
readlink -f ~/.codex/skills
readlink -f ~/.codex/config.toml
readlink -f ~/.pi/agent/skills
readlink -f ~/.pi/agent/agents
```

## Recommended workflow

1. Edit reusable content in this vault first.
2. Let wrappers and symlinks make the CLIs consume it.
3. Keep secrets and auth state outside the vault.
4. Document any new global tool in the relevant runtime-bridge or MCP note.

## Suggested next notes to add

- prompt patterns by task type
- standard code review prompt pack
- debugging checklists
- project bootstrap templates
- MCP server operating notes

## Live LLM Wiki instance

Current instantiated wiki:

- `/mnt/hyperliquid-data/projects/obisidan/Evonome-vault`
