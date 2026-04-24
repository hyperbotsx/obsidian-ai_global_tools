# Evonome Repo Workflow

This document is the default operating workflow for branch creation, multi-agent development, preview deployment, PR handling, merge wrap-up, and deployment alignment in this repository.

## Authority And Override Rule

These rules are mandatory by default for all coding agents and human operators working in this repo.

Agents must not relax, reinterpret, or skip this workflow unless the user explicitly says that the workflow may be overridden for the current task.

Accepted override examples:
- "Override the normal workflow for this task."
- "Skip preview deploy for this task."
- "Use a non-standard branch name for this task."
- "Do not reset preview to dev-main after this merge."

Not accepted as overrides:
- urgency
- convenience
- implied permission
- silence
- "just do it"
- "ship it fast"
- "it is probably fine"

When in doubt, the workflow stays in force.

## Goals

1. Keep `main` and `dev-main` clean and predictable.
2. Make sprint branches deterministic and easy to find.
3. Give parallel coding agents isolated worktrees and isolated branches.
4. Use `preview.evonome.com/app` early during development to catch browser-visible issues.
5. Always finish with the correct sync back to `main`, `dev-main`, and preview state.

## Canonical Roots

| Purpose | Path | Notes |
|---|---|---|
| Public main checkout | `/mnt/hyperliquid-data/projects/repos/SoldierOne` | Deploy-only root for `main` |
| Shared development worktree | `/mnt/hyperliquid-data/projects/worktrees/Evonome` | Default root for normal sprint work |
| Preview deploy root | `/mnt/hyperliquid-data/projects/worktrees/Evonome-preview` | Deploy-only root for preview infrastructure |
| Agent worktree parent | `/mnt/hyperliquid-data/projects/worktrees/Evonome-agents` | Manual top-level worktrees for parallel agents |

## Canonical Branches

### Long-Lived Branches

- `main` is the merged source of truth.
- `dev-main` is the always-refreshable local integration baseline and must track `origin/main` after each merge.

### Sprint Branches

Create sprint branches from `dev-main`.

Use these prefixes:
- `feat/<slug>` for feature work
- `fix/<slug>` for bug fixes and regressions
- `chore/<slug>` for tooling, infra, refactors, and maintenance
- `docs/<slug>` for docs-only work

Slug rules:
- kebab-case only
- short and descriptive
- usually 2 to 6 words
- no spaces
- no random suffixes unless the user explicitly wants them

Examples:
- `feat/strategy-builder-canvas`
- `fix/preview-auth-redirect`
- `chore/lazygit-agent-workflow`
- `docs/repo-workflow`

### Agent Branches

Agent branches always branch from the active sprint branch.

Format:
- `agent/<sprint-slug>/<slice>`

Rules:
- `<sprint-slug>` is the part after the sprint branch prefix
- `<slice>` is a short ownership label like `ui`, `api`, `tests`, `docs`, `cleanup`, `attempt-a`
- every agent gets a unique branch
- never check out the same branch in more than one worktree

Examples:
- sprint branch: `feat/strategy-builder-canvas`
- agent branches:
  - `agent/strategy-builder-canvas/ui`
  - `agent/strategy-builder-canvas/api`
  - `agent/strategy-builder-canvas/tests`

## Start-Of-Work Routine

Agents should guide this routine every time a new coding sprint starts.

### 1. Confirm Scope

- Find the PRD in `tasks/prd/_current/` when the task is PRD-backed.
- Decide whether the work belongs on an existing sprint branch or a new sprint branch.
- If the repo has a dirty tree unrelated to the current task, stop and clarify before changing branches.

### 2. Never Start Coding On `main` Or `dev-main`

Coding work must not begin directly on `main` or `dev-main`.

If the current branch is `main` or `dev-main` and the task is a new coding sprint, create the correct sprint branch first.

### 3. Prepare `dev-main`

From the shared development worktree:

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome
git fetch origin main
git branch -f dev-main origin/main
git switch dev-main
```

Only do this when the shared worktree is clean enough for the branch move.

### 4. Create The Sprint Branch

```bash
git switch -c <type>/<slug>
```

Example:

```bash
git switch -c feat/strategy-builder-canvas
```

### 5. Confirm Preview State When It Matters

If preview ownership is unclear or the task is likely to use preview soon:

```bash
./deploy-status
```

## Default Development Mode

For normal sprint work:
- use the shared development worktree
- keep work on the sprint branch
- do not create a new worktree for every sprint
- do not develop inside deploy-only roots

Preferred human tooling:
- use LazyGit as the human review and integration cockpit
- use Git Town only as optional human workflow assistance, not as the agent worktree orchestrator

## Workflow Automation

Use these repo scripts when following the workflow mechanically:
- `scripts/git/new-sprint <type> <slug>`
- `scripts/git/spawn-agent <slice>`
- `scripts/git/integrate-agent <slice>`
- `scripts/git/cleanup-agent [--force] <slice>`

The matching LazyGit command bindings live in `.lazygit.yml` at the repo root.

## Preview Deployment During Development

Preview deployment is part of the normal development loop for frontend and full-stack work.

### Standard Rule

After a meaningful checkpoint, and before asking for review on browser-visible work, deploy the active sprint branch to preview:

```bash
./deploy-preview
```

This should normally happen from the active sprint branch in the shared development worktree.

### Why

`preview.evonome.com/app` is the fastest way to catch:
- frontend regressions
- browser-only bugs
- route issues
- asset problems
- API integration problems that do not show up in unit tests alone

### Important Behavior

`./deploy-preview` can include tracked and untracked working tree changes from the source worktree. That means preview can reflect an intentional uncommitted checkpoint.

Use that on purpose, not by accident.

### Safety Rules

- Never run `./deploy-preview` when the user intends to update `evonome.com/app`.
- Never run `./deploy-preview` from the public main checkout.
- Never run `./deploy-preview` from the preview deploy root.
- If preview ownership is unclear, run `./deploy-status` first.

### Preferred Preview Source In Parallel Work

If parallel agent branches exist, preview should normally reflect the integrated sprint branch, not a raw agent branch, unless the user explicitly wants to inspect an agent branch directly.

## Parallel Agent Workflow

Use this when multiple coding agents should work in parallel on the same sprint.

### Non-Negotiable Rules

- Never use hidden nested worktrees created by tool isolation.
- Never use `isolation: "worktree"` when spawning agents.
- Never let multiple agents edit the same hotspot files unless the user explicitly wants competing attempts.
- Never hand work between agents through `git stash`.

### Allowed Model

Use manual top-level worktrees under:

```text
/mnt/hyperliquid-data/projects/worktrees/Evonome-agents
```

### Create An Agent Worktree

From the shared development worktree:

```bash
mkdir -p /mnt/hyperliquid-data/projects/worktrees/Evonome-agents
git worktree add \
  /mnt/hyperliquid-data/projects/worktrees/Evonome-agents/<sprint-slug>-<slice> \
  -b agent/<sprint-slug>/<slice> \
  <type>/<slug>
```

Example:

```bash
mkdir -p /mnt/hyperliquid-data/projects/worktrees/Evonome-agents
git worktree add \
  /mnt/hyperliquid-data/projects/worktrees/Evonome-agents/strategy-builder-canvas-ui \
  -b agent/strategy-builder-canvas/ui \
  feat/strategy-builder-canvas
```

### Good Parallel Slices

- `ui`
- `api`
- `tests`
- `docs`
- `cleanup`
- `attempt-a`
- `attempt-b`

### Hotspots That Need Single Ownership

Only one agent should own each of these at a time unless the user explicitly requests competing attempts:
- lockfiles
- DB migrations
- shared route registries
- shared schema files
- deployment files
- env templates
- high-churn central config

### Integration Back To The Sprint Branch

Integrate agent branches sequentially into the sprint branch.

Default integration method:

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome
git switch <type>/<slug>
git merge --squash --no-commit agent/<sprint-slug>/<slice>
```

Then:
- inspect the staged result
- run targeted checks
- commit on the sprint branch with a clean message

Preferred default: squash integration.

Use cherry-pick only when selective history matters.

## Review And PR Workflow

### Local Review Before Push

Before pushing or opening a PR:
- run the local quality gate when available
- run task-relevant tests
- review the final sprint diff
- use preview for browser-visible verification

Preferred quality gate command:

```bash
/gate --ml
```

### PR Model

- open the final PR from the sprint branch to `main`
- do not open per-agent PRs unless the user explicitly asks for them
- keep agent branches temporary and local by default

### Commit And PR Rules

- use conventional commit format: `type(scope): description`
- never add `Co-Authored-By` lines
- never mention Claude, Claude Code, Codex, OpenAI, or Anthropic in commits or PR text

### Review Fixes

When fixing review comments across multiple PRs:
1. process one PR at a time
2. stash only if a human-owned dirty tree makes it unavoidable
3. check out the relevant PR branch
4. apply fixes, commit, push
5. return to the prior branch cleanly

## Merge And Wrap-Up Workflow

This is the required finish sequence after a PR is merged or when the user decides the sprint branch is the merged source of truth.

### 1. Sync The Public Main Checkout

```bash
cd /mnt/hyperliquid-data/projects/repos/SoldierOne
git checkout main
git pull --ff-only
```

### 2. Deploy Public Only When Intended

If the user intends to update `evonome.com/app`, run from the public main checkout:

```bash
./deploy-status
./deploy-main
```

Do not use `./deploy-main` for preview.

### 3. Sync `dev-main` In The Shared Development Worktree

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome
git fetch origin main
git branch -f dev-main origin/main
git switch dev-main
```

### 4. Reset Preview Back To `dev-main`

If preview had been pointed at the sprint branch during development, restore the default preview baseline:

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome
./deploy-dev-main
./deploy-status
```

This is the default finish path after merge. Skip it only when the user explicitly says preview should stay elsewhere.

### 5. Clean Up Sprint And Agent Branches

After the shared worktree is safely back on `dev-main`, delete completed local branches and remove temporary agent worktrees.

Typical cleanup:

```bash
git branch -d <type>/<slug>
git worktree remove /mnt/hyperliquid-data/projects/worktrees/Evonome-agents/<sprint-slug>-<slice>
git branch -D agent/<sprint-slug>/<slice>
git worktree prune
```

## Deployment Safety Rules

- `./deploy-main` is only for the public site.
- `./deploy-preview` is only for feature preview.
- `./deploy-dev-main` restores preview to the default `dev-main` baseline.
- `./deploy-status` is the first command to run when deployment state is unclear.
- `/mnt/hyperliquid-data/projects/repos/SoldierOne` and `/mnt/hyperliquid-data/projects/worktrees/Evonome-preview` are deploy-only roots.

## Shared Vault Reference

The reusable template kit for this workflow lives in the Obsidian AI Global Tools vault:

`/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/obsidian-ai_global_tools/shared/templates/agentic-git-workflow-kit/README.md`

Future repos can copy or adapt the template kit from there while keeping repo-specific paths and deploy commands local.

## Agent Behavior Contract

Agents working in this repo must do the following by default:

1. Guide the user onto the correct sprint branch before coding starts.
2. Create correctly named sprint branches from `dev-main` for new work.
3. Keep coding work off `main` and `dev-main`.
4. Use manual top-level worktrees and `agent/...` branches for real parallel code-writing.
5. Recommend and run `./deploy-preview` during development for browser-visible work unless the user explicitly says not to.
6. Finish with the full wrap-up flow: merge readiness, main sync, `dev-main` sync, preview reset, and cleanup.
7. Ask for an explicit override before deviating from this workflow.

## Operational Summary

If you need the shortest possible version of the workflow:

1. Start from `dev-main`.
2. Create a correctly named sprint branch.
3. Develop in the shared worktree.
4. Use manual top-level agent worktrees only for parallel work.
5. Deploy to preview during development.
6. Open the final PR from the sprint branch.
7. Merge to `main`.
8. Sync the public `main` checkout.
9. Sync `dev-main`.
10. Reset preview to `dev-main`.
11. Clean up temporary branches and worktrees.
