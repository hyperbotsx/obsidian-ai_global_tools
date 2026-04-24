# Workflow Git Scripts

These scripts implement the default Evonome branch and worktree workflow for both Claude-style agents and Codex-style agents.

## Scripts

- `scripts/git/new-sprint <type> <slug>`
  - syncs `dev-main` from `origin/main` in the shared development worktree
  - creates the new sprint branch in `/mnt/hyperliquid-data/projects/worktrees/Evonome`
- `scripts/git/spawn-agent <slice>`
  - creates `agent/<sprint-slug>/<slice>` from the current sprint branch
  - creates a manual top-level worktree under `/mnt/hyperliquid-data/projects/worktrees/Evonome-agents`
- `scripts/git/integrate-agent <slice>`
  - squash-merges the agent branch into the current sprint branch
  - leaves the result staged and uncommitted for review
- `scripts/git/cleanup-agent [--force] <slice>`
  - removes the manual agent worktree
  - deletes the temporary local `agent/...` branch
  - prunes stale worktree metadata

## Expectations

- `new-sprint` requires a clean shared worktree at `/mnt/hyperliquid-data/projects/worktrees/Evonome`
- the other scripts require a clean current worktree and a valid sprint branch
- sprint branches must follow `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, or `docs/<slug>`
- agent branches always use `agent/<sprint-slug>/<slice>`

## Lazygit

The matching Lazygit commands live in `.lazygit.yml` at the repo root.

## Shared Vault Reference

The reusable template kit for this workflow lives in the Obsidian AI Global Tools vault at:

`/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/obsidian-ai_global_tools/shared/templates/agentic-git-workflow-kit/README.md`
