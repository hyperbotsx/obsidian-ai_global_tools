# Shared skills

This folder holds canonical skills that should be reused across multiple runtimes.

## Pattern

- keep one canonical skill package here
- symlink it into runtime-specific skill folders when appropriate
- include supporting reference files alongside `SKILL.md` when the skill depends on them

## Installed shared skills

- `herdr/` — herdr workspace/tab/pane control skill, with `SOCKET_API.md` reference
- `create-pr/` — push branch + open GitHub PR via `git town propose` with house formatting (Greptile tag, no AI mentions). Symlinked into `claude/skills/create-pr` and `codex/skills/create-pr`.
