---
name: autofix-pr-loop
description: Run audit-context-building, then bug-check, fix actionable bugs without user prompts, repeat until no more actionable findings remain or progress stalls, then commit, push, and open a review-ready PR automatically. Use on a sprint branch when you want an autonomous hardening pass and PR creation.
---

# Autofix PR Loop

This skill chains your review workflow into one non-interactive closeout pass.

## Invocation Means Approval

If the user invokes this skill, treat that as approval to:
- analyze the branch
- edit code
- run checks
- create commits
- push the branch
- open a PR

Do not pause for confirmation unless you hit a destructive or ambiguous situation that cannot be resolved safely.

## Required Skills

Before starting, read these skills in full:
- `~/.codex/trailofbits-skills/plugins/audit-context-building/skills/audit-context-building/SKILL.md`
- `~/.codex/skills/bug-check/SKILL.md`
- `~/.pi/agent/skills/review-ready-pr/SKILL.md`

Load any referenced files from those skills when needed.

## Guardrails

1. Never run this from `main` or `dev-main`.
2. Never mention Claude, Codex, OpenAI, Anthropic, or any AI tool in commits or PR text.
3. The only allowed Codex mention is the PR review tag `@codex`.
4. Always include `@greptile review` in the PR body.
5. Use conventional commit format.
6. Prefer small, direct fixes over rewrites.
7. Stop infinite loops. Default maximum is 3 fix-check rounds.
8. Do not create a PR if hard build or test failures remain unresolved.

## Phase 1. Preconditions

Run:

```bash
git branch --show-current
git status --short
git rev-parse --verify dev-main
```

Rules:
- If the current branch is `main` or `dev-main`, stop.
- If `dev-main` does not exist locally, stop and explain.
- If merge conflicts exist, stop.

## Phase 2. Build context

Run the `audit-context-building` workflow against the current repo state.

Scope rules:
- Base local review scope on `dev-main...HEAD` plus current dirty changes.
- Focus on changed code, immediate callers/callees, contract boundaries, and nearby tests.
- Keep a compact internal audit map for later bug-check passes.

Output a short context summary only.
Do not spend the full answer budget on the audit report.

## Phase 3. Bug-check and fix loop

Default maximum: 3 rounds.

In each round:

1. Run the `bug-check` workflow on the current scoped diff.
2. Classify findings:
   - **actionable**: `confirmed` or `probable` with a concrete failure mechanism
   - **non-actionable**: `needs_repro`, style-only notes, or speculative concerns without evidence
3. If there are no actionable findings, exit the loop.
4. Fix all actionable findings directly without asking the user.
5. After fixes, run the smallest relevant verification set for the touched area, such as:
   - targeted tests
   - typecheck
   - lint
   - build
   - import or syntax checks
6. Re-run `bug-check` on the updated diff.

Progress rules:
- If the same actionable finding survives two rounds, make one targeted final attempt.
- If no meaningful progress is made, stop the loop and report the remaining issue instead of looping forever.
- Prefer fixing root causes over patching symptoms.

## Phase 4. Final quality gate

First try:

```bash
/gate --ml
```

If unavailable, note that and fall back to the minimum relevant checks for the changed stack.

Minimum fallback checks:
- frontend: typecheck, build, lint if configured
- backend: syntax/import checks and relevant tests if available

If final hard failures remain, do not create a PR.
Report what is blocking.

## Phase 5. Commit preparation

Summarize the final diff:

```bash
git log --oneline dev-main...HEAD
git diff --name-only dev-main...HEAD
git diff --stat dev-main...HEAD
git status --short
```

Then:
- stage all intended files
- write one conventional commit covering the final branch state
- keep the commit message concise and scope-specific

Commit title rules:
- `fix(scope): description`
- `feat(scope): description`
- `refactor(scope): description`
- `docs(scope): description`
- `chore(scope): description`

If the branch already contains earlier commits, add one final clean commit rather than rewriting history.

## Phase 6. PR creation

Follow the conventions from `review-ready-pr`, but do not pause for confirmation.
This skill invocation is the confirmation.

PR rules:
- Base branch should be `main`
- push current branch with upstream if needed
- PR body must include:
  - concise summary
  - changed areas grouped by backend, frontend, docs/scripts as applicable
  - test plan with completed checks
  - `@greptile review`
  - `@codex`

Use:

```bash
git push -u origin $(git branch --show-current)
gh pr create --base main --title "<title>" --body "<body>"
```

## Output format

At the end, report:
- branch name
- number of fix-check rounds completed
- findings fixed
- remaining non-actionable concerns, if any
- final checks run and status
- final commit hash and message
- PR URL

## Stop Conditions

Stop without creating a PR if any of these are true:
- branch is `main` or `dev-main`
- merge conflicts exist
- no safe path to resolve repeated findings
- hard build or test failures remain
- GitHub push or PR creation fails

When stopping, give a short blocker report and the exact next action needed.
