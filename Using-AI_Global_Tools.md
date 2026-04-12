# Using AI_Global_Tools

## Non-repo-specific rule

This setup must work outside any particular repo.

Always treat the absolute vault path below as canonical, even if you are operating from another project, a temporary directory, or a different worktree:

- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools`

When asked to use a skill, workflow, prompt, or agent asset, resolve it from this vault first instead of searching the current repo for a local copy.

Resolution order:

1. tool-specific folders in this vault
2. shared folders in this vault
3. repo-local copies only when explicitly requested or when no canonical vault copy exists

## What is now global

The following are now sourced from this vault:

- Codex skills
- Claude Code skills
- Claude global system prompt
- Codex global developer instructions
- Claude MCP definitions
- Codex config file (including current MCP entries)
- shared prompt, agent, skill, and template documentation
- reusable LLM Wiki schema/templates
- shared `herdr` skill available to Claude, Codex, and Pi via vault symlinks

## Live bridges on this machine

### Claude Code

The `claude` command now resolves through a local wrapper in:

- `~/.local/bin/claude`

That wrapper automatically:

- appends `claude/prompts/system/claude-global.md`
- adds this vault as an accessible directory
- loads MCP config from `mcp/claude/mcp-config.json`
- uses `--strict-mcp-config` unless you explicitly override MCP flags yourself

### Codex

The `codex` command now resolves through a local wrapper in:

- `~/.local/bin/codex`

That wrapper automatically:

- exports `AI_GLOBAL_TOOLS_DIR=/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools`
- injects `codex/prompts/system/codex-global.md` as developer instructions

Also:

- `~/.codex/skills` -> vault symlink
- `~/.claude/skills` -> vault symlink
- `~/.codex/config.toml` -> vault symlink to `mcp/codex/config.toml`

## Where to edit things

### Add or edit Claude skills

Edit under:

- `claude/skills/`

### Add or edit Codex skills

Edit under:

- `codex/skills/`

### Add reusable prompts

Edit under:

- `shared/prompts/library/`
- `shared/prompts/system/`
- `claude/prompts/system/`
- `codex/prompts/system/`

### Add reusable shared skills

Canonical shared skills can live under:

- `shared/skills/`

Then runtime-specific skill paths can symlink back to them, as with:

- `shared/skills/herdr/`

### Use or adapt the LLM Wiki pattern

Start with:

- `LLM-Wiki-Pattern.md`
- `shared/templates/llm-wiki/`

Current live instance created from this pattern:

- `/mnt/hyperliquid-data/projects/obisidan/Evonome-vault`

### Add or edit MCP definitions

Edit under:

- `mcp/claude/mcp-config.json`
- `mcp/codex/config.toml`
- `mcp/bin/`

## Secrets location

Secrets are intentionally **not** stored in the vault.

Use:

- `~/.config/ai-global-tools/mcp-secrets.env`

There is also a template here:

- `~/.config/ai-global-tools/mcp-secrets.env.example`

## Backups

Pre-migration backups were stored in:

- `~/.local/share/ai-global-tools-backups/`

## How to check it later

```bash
type -a claude
type -a codex
readlink -f ~/.claude/skills
readlink -f ~/.codex/skills
readlink -f ~/.codex/config.toml
```

## Practical rule

If you want a reusable agent tool to become global, add it to this vault first.

If a user says things like:

- "use the bug-check skill"
- "use the Claude pre-pr skill"
- "run that Codex workflow"

then the agent should first look in:

- `claude/skills/`
- `codex/skills/`
- `shared/skills/`
- related prompt/docs folders in this same vault

and should not assume a repo-local copy is authoritative.
