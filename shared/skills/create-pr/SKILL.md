---
name: create-pr
description: "Push the current branch, open a GitHub PR using git-town, then automatically trigger an advisory Kody/Kodus review. Triggers on: update github, create pr, make pr, push pr, open pr, submit pr, propose."
---

# Create PR

One canonical skill for both Claude Code and Codex. Same name, same behaviour, same output.

The whole job is: **`git town propose` with our standard title and body**. Do not improvise extra steps.

## Hard rules

1. **NEVER mention Claude, Claude Code, Codex, OpenAI, Anthropic, or any AI tool** in commits, PR title, or PR body.
2. **NEVER add `Co-Authored-By` lines** to commits.
3. **NEVER add automated review tags to the PR title or body**. Kody is triggered after PR creation through the `kodus-agent` facade unless the user explicitly opts out.
4. **ALWAYS show the drafted title and body to the user and wait for confirmation** before running `git town propose`.
5. **NEVER merge** — only open the PR.
6. Use conventional commit format for the title: `type(scope): description`, max 70 chars.
7. For Evonome PRD work, opening the PR must be followed by PRD closeout updates.
8. Kody/Kodus review is advisory only; never make it a required check or approval gate.

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

### 5. Evonome PRD closeout

After `git town propose` returns the PR URL, if the branch/PR came from an Evonome PRD issue or names a PRD number:

1. Ensure the PR body references the PRD with a closing keyword, for example `Resolves hyperbotsx/SoldierOne#977`, so GitHub populates the Project `Linked pull requests` field.
2. Update GitHub Project 2 for the PRD item:
   - `Status` → `Done`
   - `Pipeline Status` → `Done`
   - `PR URL` → the PR URL when that custom field exists
3. Close the PRD issue as completed.
4. Update the tracker source, usually tracker issue `#862`, with the PRD number, PR URL, PR state, and final validation summary. If a repo-local tracker file is used for the run, update that too.
5. Fail visibly on any unavailable field, missing PRD number, or mutation error.

### 6. Trigger advisory Kody review

After the PR is open and closeout updates are complete, trigger Kody unless the user explicitly opted out:

```bash
repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
pr=<PR number from git town propose output or gh pr view>
branch=$(gh pr view "$pr" --repo "$repo" --json headRefName --jq .headRefName)
sha=$(gh pr view "$pr" --repo "$repo" --json headRefOid --jq .headRefOid)

if command -v kodus-agent >/dev/null 2>&1; then
  kodus-agent request_review --repo "$repo" --pr "$pr" --branch "$branch" --head-sha "$sha"
else
  cd /mnt/hyperliquid-data/projects/repos/agentops-harness && \
    PYTHONPATH=src python3 -m agentops_harness.kodus_agent request_review \
      --repo "$repo" --pr "$pr" --branch "$branch" --head-sha "$sha"
fi
```

If the Kody trigger fails, keep the PR open and report the Kody failure as non-blocking `needs_human` follow-up.

### 7. Return the PR URL

Print the URL, PRD closeout result, and Kody trigger result. Stop. Do not auto-merge.

## Forbidden in PR text

- AI tool names (Claude, GPT, Copilot, Codex, etc.)
- `Co-Authored-By` lines
- "Generated with" badges or links
- Internal conversation context or debug notes

## When the user says any of these, run this skill

`update github`, `create pr`, `make pr`, `open pr`, `push pr`, `submit pr`, `propose`, `prd`.

No analysis, no planning, no extra checklists. Draft → confirm → `git town propose` → PRD closeout → Kody trigger → return URL.
