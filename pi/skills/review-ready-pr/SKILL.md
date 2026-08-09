---
name: review-ready-pr
description: Prepare and create a review-ready GitHub PR after context audit and bug check, then automatically trigger an advisory Kody/Kodus review. Use when the branch is ready for PR drafting and push. Enforces no AI mentions and asks for confirmation before opening the PR.
---

# Review-Ready PR

Use this after the branch has already gone through context audit and bug review.

## Rules

1. Never mention Claude, Codex, OpenAI, Anthropic, or any AI tool in commits, PR title, or PR body.
2. Never add Co-Authored-By lines.
3. Do not add automated review tags to the PR title or body; Kody is triggered after PR creation through the `kodus-agent` facade unless the user explicitly opts out.
4. Ask for confirmation before creating the PR.
5. Never merge automatically.
6. Kody/Kodus review is advisory only; never make it a required check or approval gate.
7. For Evonome PRD work, PR creation is not complete until PRD closeout fields and tracker evidence are updated.

## Flow

### Phase 1. Branch and cleanliness check

Run:

```bash
git branch --show-current
git status --short
git rev-list --count dev-main...HEAD
git diff --stat dev-main...HEAD
```

Rules:
- Do not open a PR from `main` or `dev-main`.
- If there are uncommitted tracked changes, stop and ask whether to commit first.
- If there are no commits ahead of `dev-main`, stop.

### Phase 2. Final gate

If available, run the local quality gate first:

```bash
/gate --ml
```

If that command is unavailable, say so and continue with a note.

Then collect the branch summary:

```bash
git log --oneline dev-main...HEAD
git diff --name-only dev-main...HEAD
git diff --stat dev-main...HEAD
```

### Phase 3. Draft the PR

Build a concise PR using this format:

```markdown
## Summary
- Bullet 1
- Bullet 2
- Bullet 3

## Changes
### Backend
- `path` — short explanation

### Frontend
- `path` — short explanation

### Docs / Scripts
- `path` — short explanation

## Test plan
- [x] Context audit completed
- [x] Bug check completed
- [x] Local quality gate completed or explicitly skipped
- [ ] Manual verification

```

PR title must use conventional commit format:

- `feat(scope): description`
- `fix(scope): description`
- `refactor(scope): description`
- `docs(scope): description`
- `chore(scope): description`

Keep the title under 70 characters.

### Phase 4. Confirmation

Show the draft title and body to the user.
Ask for explicit confirmation before creating the PR.

### Phase 5. Push and create

After confirmation, run:

```bash
git push -u origin $(git branch --show-current)
```

Then create the PR:

```bash
gh pr create --title "<title>" --body "<body>"
```

Capture the PR URL.

### Phase 6. Trigger advisory Kody review

After the PR is open, trigger Kody unless the user explicitly opted out:

```bash
repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
pr=<PR number from gh pr create output or gh pr view>
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

If the Kody trigger fails, keep the PR open and report the Kody failure as a non-blocking `needs_human` follow-up.

### Phase 7. Evonome PRD closeout

If the work came from an Evonome PRD issue or the branch/PR identifies a PRD number:

1. Ensure the PR body references the PRD with a closing keyword, for example `Resolves hyperbotsx/SoldierOne#977`, so GitHub populates the Project `Linked pull requests` field.
2. Update GitHub Project 2 for the PRD item:
   - `Status` → `Done`
   - `Pipeline Status` → `Done`
   - `PR URL` → the PR URL when that custom field exists
3. Close the PRD issue as completed.
4. Update the project tracker source, usually tracker issue `#862`, with the PRD number, PR URL, PR state, and final validation summary. If a repo-local tracker file is used for the run, update that too.
5. Report any failed closeout mutation explicitly instead of claiming completion.

Return the PR URL and closeout result.

## Output Requirements

Before creation, show:
- current branch
- commits ahead of `dev-main`
- changed file summary
- proposed PR title
- proposed PR body

After creation, show:
- PR URL
- Kody trigger result, including trigger comment URL and webhook relay status when available
- PRD closeout result, including Project 2 `Done`, `Linked pull requests`, `PR URL`, issue closure, and tracker update status when applicable

## Notes

- If repo instructions require a different base branch, follow repo instructions in addition to this skill.
- If the user asks only for drafting, stop before `gh pr create`.
