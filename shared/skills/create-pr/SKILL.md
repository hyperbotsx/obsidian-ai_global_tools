---
name: create-pr
description: "Push the current branch and open a GitHub PR using git-town, with consistent formatting and no AI mentions. Triggers on: update github, create pr, make pr, push pr, open pr, submit pr, propose."
---

# Create PR

One canonical skill for both Claude Code and Codex. Same name, same behaviour, same output.

The whole job is: **`git town propose` with our standard title and body**. Do not improvise extra steps.

## Hard rules

1. **NEVER mention Claude, Claude Code, Codex, OpenAI, Anthropic, or any AI tool** in commits, PR title, or PR body.
2. **NEVER add `Co-Authored-By` lines** to commits.
3. **NEVER add automated review tags unless the user explicitly requests them**.
4. **ALWAYS show the drafted title and body to the user and wait for confirmation** before running `git town propose`.
5. **NEVER merge** — only open the PR.
6. Use conventional commit format for the title: `type(scope): description`, max 70 chars.

## Prerequisites

- `git-town` must be installed (`brew install git-town` or see https://www.git-town.com/install).
- Repo must be initialised once: `git town config setup` (interactive — main branch, perennial branches, hosting platform).
- `gh` CLI must be authenticated (`gh auth status`).

If `git town` is not installed or the repo isn't initialised, stop and tell the user.

## The job

### 1. Verify state
```bash
git status --short
git rev-list --count main...HEAD   # use main, or dev-main if that's the parent
git log --oneline main...HEAD
git diff --stat main...HEAD
```
If there are uncommitted changes, ask the user whether to commit them first. Do not auto-commit without confirmation.

### 2. Draft the PR

Title (max 70 chars, conventional commit):
```
type(scope): short description
```

Body:
```
## Summary
- Bullet 1 (what changed and why)
- Bullet 2
- Bullet 3

## Changes
### Backend
- `path/file.py` — what changed

### Frontend
- `path/Component.tsx` — what changed

### Scripts / Docs
- `path/file` — what changed

## Test plan
- [x] Type checks pass
- [x] Build succeeds
- [x] Lint / syntax checks pass
- [ ] Manual verification items (if any)

```

Omit any section that has nothing to report.

### 3. Confirm with user

Show the drafted title and body. Wait for explicit go-ahead.

### 4. Open the PR

```bash
git town propose --title "<title>" --body "<body>"
```

`git town propose` handles: syncing the parent branch, pushing the current branch with upstream tracking, and opening the PR via `gh`. Do not run `git push` or `gh pr create` separately.

### 5. Return the PR URL

Print the URL. Stop. Do not auto-merge, do not run further commands.

## Forbidden in PR text

- AI tool names (Claude, GPT, Copilot, Codex, etc.)
- `Co-Authored-By` lines
- "Generated with" badges or links
- Internal conversation context or debug notes

## When the user says any of these, run this skill

`update github`, `create pr`, `make pr`, `open pr`, `push pr`, `submit pr`, `propose`, `prd`.

No analysis, no planning, no extra checklists. Draft → confirm → `git town propose` → return URL.
