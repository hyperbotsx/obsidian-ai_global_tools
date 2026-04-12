# MCP source of truth

This folder holds the canonical MCP definitions used by the local wrappers.

## What lives here

- launcher scripts in `bin/`
- Claude Code MCP config in `claude/mcp-config.json`
- Codex config in `codex/config.toml`

## What does **not** live here

- API keys
- bearer tokens
- raw secret environment values

Those belong in:

- `~/.config/ai-global-tools/mcp-secrets.env`

The local wrapper scripts load secrets from that external file when needed.
