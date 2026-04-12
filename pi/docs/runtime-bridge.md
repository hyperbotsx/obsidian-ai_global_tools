# Pi runtime bridge

Pi now uses `AI_Global_Tools` as the source of truth for its reusable skills and agents.

## Live runtime links

- `~/.pi/agent/skills` -> `AI_Global_Tools/pi/skills`
- `~/.pi/agent/agents` -> `AI_Global_Tools/pi/agents`

## Skill search order in Pi settings

1. `AI_Global_Tools/pi/skills`
2. `AI_Global_Tools/codex/skills`
3. `AI_Global_Tools/claude/skills`

This means Pi can use vault-managed Pi skills first, then reuse Codex and Claude skills from the same vault.

## Not moved into the vault

- auth/session state
- local binaries
- run history
- session logs
