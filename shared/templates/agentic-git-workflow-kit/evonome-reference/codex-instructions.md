# SoldierOne Codex Instructions

## Workflow Authority

- `docs/evonome/REPO_WORKFLOW.md` is the canonical repo workflow for sprint branches, manual agent worktrees, preview deployment, PR handling, merge wrap-up, and deployment alignment.
- Read `docs/evonome/REPO_WORKFLOW.md` before starting a new sprint, creating branches or worktrees, opening PRs, merging, or deploying.
- These workflow rules stay in force unless the user explicitly says they may be overridden for the current task.
- Convenience, urgency, implication, or silence do not count as overrides.

## Default Paths

- Shared development worktree: `/mnt/hyperliquid-data/projects/worktrees/Evonome`
- Public main checkout: `/mnt/hyperliquid-data/projects/repos/SoldierOne`
- Preview deploy root: `/mnt/hyperliquid-data/projects/worktrees/Evonome-preview`
- Agent worktree parent: `/mnt/hyperliquid-data/projects/worktrees/Evonome-agents`

## Required Default Behavior

- Start new coding work from `dev-main` using a correctly named sprint branch.
- Never start new coding work directly on `main` or `dev-main`.
- Use `scripts/git/new-sprint`, `scripts/git/spawn-agent`, `scripts/git/integrate-agent`, and `scripts/git/cleanup-agent` when following the repo workflow.
- Use preview during development for browser-visible work unless the user explicitly says to skip it.
- After merge, sync local `main`, sync local `dev-main`, and reset preview to `dev-main` unless the user explicitly says otherwise.
- Use manual top-level worktrees for parallel code-writing. Never use hidden nested worktree isolation.

## Branching Model

- Long-lived branches:
  - `main`
  - `dev-main`
- Sprint branches:
  - `feat/<slug>`
  - `fix/<slug>`
  - `chore/<slug>`
  - `docs/<slug>`
- Agent branches:
  - `agent/<sprint-slug>/<slice>`

## PR And Review Rules

- Open one PR per sprint branch unless the user explicitly wants a different split.
- Include `@greptile review` in the PR body and in re-review requests.
- Do not mention Codex, OpenAI, Claude, or Anthropic in commits or PR text.
- Use conventional commit messages.

## EVONOME Runtime Policy

- `evonome.com` root remains the holding page.
- `evonome.com/app` must only reflect `/mnt/hyperliquid-data/projects/repos/SoldierOne` on `main`.
- `preview.evonome.com/app` should normally reflect the default `dev-main` baseline.
- The only approved preview override is `./deploy-preview` from the active sprint branch.
- `./deploy-dev-main` resets preview to the default `dev-main` baseline.
- `./deploy-main` is the only command that should affect the public domain.
- Run `./deploy-status` before any domain-affecting change when there is any doubt.
