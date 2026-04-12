# AI_Global_Tools setup plan

## What I found

- **Codex** auto-discovers skills from `$CODEX_HOME/skills`, which defaults to `~/.codex/skills`.
- **Claude Code** is currently using user skills from `~/.claude/skills`.
- Claude Code supports hidden but real flags for:
  - `--system-prompt-file`
  - `--append-system-prompt-file`
  - `--plugin-dir`
- Your current user-specific state includes secret-bearing files such as auth, credentials, and MCP settings. Those should **not** be moved into the Obsidian vault.

## Proposed vault layout

```text
AI_Global_Tools/
  README.md
  Global-Agent-Source-of-Truth-Plan.md
  shared/
    prompts/
      system/
      library/
    agents/
    templates/
  mcp/
    README.md
    bin/
    codex/
    claude/
  codex/
    skills/
    prompts/
      system/
      library/
    docs/
  claude/
    skills/
    prompts/
      system/
      library/
    docs/
```

## Safe implementation path

- [x] Scaffold the vault folders and index docs.
- [x] Copy your current Codex skills into `AI_Global_Tools/codex/skills/`.
- [x] Copy your current Claude Code skills into `AI_Global_Tools/claude/skills/`.
- [x] Replace `~/.codex/skills` with a symlink to the vault copy.
- [x] Replace `~/.claude/skills` with a symlink to the vault copy.
- [x] Create a **Claude wrapper** in `~/.local/bin/claude` so every Claude Code session appends a canonical system prompt file from the vault, adds the vault as an accessible directory, and points at the vault-backed MCP config.
- [x] Create a **Codex wrapper** in `~/.local/bin/codex` that keeps a stable pointer to the vault and injects a codex-global instruction file via config override.
- [x] Move the **MCP server definitions** into vault-managed files and helper scripts.
- [x] Keep auth, credentials, session history, logs, and **MCP secrets/API keys** outside the vault.
- [x] Verify both `claude` and `codex` resolve through the wrappers, that the skills directories are symlinked to the vault, and that MCP config is sourced from the vault.

## Important safety boundary

The vault should be the source of truth for:

- skills
- prompt library
- system prompt documents
- reusable agent docs

The vault should **not** be the source of truth for:

- API keys
- auth tokens
- credential JSON files
- transient sessions/logs/history
- raw secret-bearing MCP env values

## Recommended first content

- `shared/prompts/system/global-operator-principles.md`
- `claude/prompts/system/claude-global.md`
- `codex/prompts/system/codex-global.md`
- `shared/prompts/library/README.md`
- `shared/agents/README.md`
- `mcp/README.md`
- `mcp/claude/mcp-config.json`
- `mcp/codex/config.toml`
- `README.md` as the master index for the vault

## Decision note

The only potentially experimental piece is the **Codex global prompt injection**. Skills centralization is straightforward; Claude global prompt injection is also straightforward; MCP centralization is straightforward **if secrets remain outside the vault** and vault-managed wrapper scripts read those secrets from external environment or external non-vault files. If the Codex runtime does not cleanly honor the config override, I will still leave Codex using the vault-backed skills and vault-backed MCP/config docs as its source of truth and document the remaining limitation clearly.
