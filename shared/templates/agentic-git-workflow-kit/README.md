# Agentic Git workflow kit

This template kit captures a working pattern for one human plus multiple coding agents using:

- a shared development worktree
- correctly named sprint branches from `dev-main`
- manual top-level agent worktrees
- `agent/<sprint-slug>/<slice>` branches
- preview deployment during development
- post-merge sync back to `main`, `dev-main`, and preview baseline
- shell helpers and Lazygit bindings that both Claude-style agents and Codex-style agents can call

## Reference implementation

The `evonome-reference/` folder contains a concrete implementation taken from the Evonome repo.

Use it as the point of reference when:
- creating a repo-specific workflow doc
- wiring Claude / Codex project instructions to that workflow doc
- adding helper scripts for new sprint branches and agent worktrees
- adding repo-local Lazygit commands

## Template contents

- `evonome-reference/REPO_WORKFLOW.md`
- `evonome-reference/claude-workflow-snippet.md`
- `evonome-reference/codex-instructions.md`
- `evonome-reference/lazygit-config.yml`
- `evonome-reference/scripts/git/README.md`
- `evonome-reference/scripts/git/new-sprint`
- `evonome-reference/scripts/git/spawn-agent`
- `evonome-reference/scripts/git/integrate-agent`
- `evonome-reference/scripts/git/cleanup-agent`
- `evonome-reference/scripts/git/common.sh`

## Adoption pattern

1. Write a repo-specific workflow doc.
2. Point project instruction files at that workflow doc.
3. Keep the strict override rule: workflow stays in force unless the user explicitly overrides it.
4. Adapt the path constants in the helper scripts to the repo’s canonical roots.
5. Copy or adapt the Lazygit config into a repo-local `.lazygit.yml`.
6. Keep the shared vault copy up to date when the pattern improves.
