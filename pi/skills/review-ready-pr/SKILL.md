---
name: review-ready-pr
description: Prepare and create a review-ready GitHub PR after context audit and bug check. Use when the branch is ready for PR drafting and push. Enforces no AI mentions and asks for confirmation before opening the PR.
---

# Review-Ready PR

Use this after the branch has already gone through context audit and bug review.

## Rules

1. Never mention Claude, Codex, OpenAI, Anthropic, or any AI tool in commits, PR title, or PR body.
2. Never add Co-Authored-By lines.
3. Do not add automated review tags unless the user explicitly requests them.
4. Ask for confirmation before creating the PR.
5. Never merge automatically.

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

Return the PR URL.

## Output Requirements

Before creation, show:
- current branch
- commits ahead of `dev-main`
- changed file summary
- proposed PR title
- proposed PR body

After creation, show:
- PR URL

## Notes

- If repo instructions require a different base branch, follow repo instructions in addition to this skill.
- If the user asks only for drafting, stop before `gh pr create`.
