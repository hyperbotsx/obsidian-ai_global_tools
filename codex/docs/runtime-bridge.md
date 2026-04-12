# Codex runtime bridge

The `codex` command is wrapped locally so that normal launches treat `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools` as the global source of truth for Codex prompts, skills, workflows, agent docs, MCP definitions, and reusable templates.

Normal launches:

- expose `AI_GLOBAL_TOOLS_DIR` pointing at this vault
- attempt to inject `codex/prompts/system/codex-global.md` via a config override
- use `~/.codex/config.toml` as a symlink to the vault-managed config file
- use `~/.codex/skills` as a symlink to the vault-managed skills directory

Canonical runtime lookup order:
1. `AI_Global_Tools/codex/`
2. `AI_Global_Tools/shared/`
3. repo-local copies only when explicitly requested or no canonical copy exists

Repo-local `.codex`, skill copies, or prompt mirrors should be treated as compatibility shims rather than source-of-truth assets unless the user explicitly overrides that rule.
