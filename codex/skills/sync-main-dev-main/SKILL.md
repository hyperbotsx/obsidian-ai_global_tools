---
name: sync-main-dev-main
description: "Update the canonical local main checkout and the Evonome-data dev-main worktree from origin/main. Use when the user says sync main, update main and dev-main, pull github main locally, refresh local baselines, or after a PR is merged to main."
---

# Sync main and dev-main

Refresh both local baselines from GitHub `origin/main` without disturbing active work.

## Targets

- Canonical local main checkout: `/mnt/hyperliquid-data/projects/repos/SoldierOne`
- Dev worktree: `/mnt/hyperliquid-data/projects/worktrees/Evonome-data`
- Remote source of truth: `origin/main`

## Hard rules

1. Fetch `origin/main` first.
2. Never overwrite uncommitted work in `Evonome-data`.
3. Never force-update `dev-main` while another worktree has it checked out unless that worktree is the intended target.
4. Preserve untracked files unless the user explicitly asks to clean them.
5. If a normal worktree command fails in `/mnt/hyperliquid-data/projects/repos/SoldierOne` because it is configured as bare, use explicit `--git-dir=.git --work-tree=.` commands.
6. Report the final commit SHA and any leftover untracked files.

## Procedure

### 1. Inspect both targets

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome-data
git status --short --branch
git branch --show-current

cd /mnt/hyperliquid-data/projects/repos/SoldierOne
git --git-dir=.git --work-tree=. status --short --branch
```

Stop if `Evonome-data` has uncommitted tracked changes and ask the user how to handle them.
Untracked files are okay to leave in place.

### 2. Fetch GitHub main

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome-data
git fetch origin main
```

### 3. Update local main checkout

Use explicit git-dir/work-tree commands because this checkout may be configured as a bare repo with a working tree:

```bash
cd /mnt/hyperliquid-data/projects/repos/SoldierOne
git --git-dir=.git fetch origin main
git --git-dir=.git --work-tree=. reset --hard origin/main
git --git-dir=.git --work-tree=. status --short --branch
git --git-dir=.git --work-tree=. log -1 --oneline --decorate
```

Do not run `git clean` unless the user explicitly asks.

### 4. Update `Evonome-data` dev-main

If `Evonome-data` is already on `dev-main`:

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome-data
git reset --hard origin/main
git status --short --branch
git log -1 --oneline --decorate
```

If `Evonome-data` is on another branch and clean:

```bash
cd /mnt/hyperliquid-data/projects/worktrees/Evonome-data
git switch dev-main
git reset --hard origin/main
git status --short --branch
git log -1 --oneline --decorate
```

If switching would disturb work, stop and ask the user whether to stash, commit, or keep the current branch untouched.

### 5. Final response

Return a concise summary:

- local main path and final commit
- `dev-main` path and final commit
- whether both match `origin/main`
- any untracked files left untouched
