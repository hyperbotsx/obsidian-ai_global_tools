---
name: create-branch
description: "Create a new development branch using Git Town from the latest main branch. Triggers on: create branch, start branch, new branch, branch for, create feature branch, start feature branch."
---

# Create branch

One canonical skill for starting new development branches safely with Git Town.

The whole job is: **create a properly named branch from the latest `main` using `git town hack`**. Start from current code on `main`. Do not improvise a custom git flow.

## Hard rules

1. **ALWAYS use Git Town** for branch creation.
2. **ALWAYS branch from the latest `main`** unless the user explicitly says to branch from something else.
3. **NEVER create the new feature branch from an outdated working branch**.
4. **NEVER discard or overwrite uncommitted work**.
5. **If the working tree is dirty, stop and ask the user whether to commit, stash, or move that work first**.
6. **Confirm the proposed branch name with the user if it is ambiguous**.
7. Prefer branch names like:
   - `feat/<slug>`
   - `fix/<slug>`
   - `chore/<slug>`
   - `docs/<slug>`

## Prerequisites

- `git town` must be installed.
- The repo must be configured for Git Town with `main` as the main branch.
- `origin/main` must be reachable.

If any prerequisite is missing, stop and tell the user what needs to be fixed.

## The job

### 1. Verify the repo is safe to branch from

Run checks like:

```bash
git status --short
git branch --show-current
git remote -v
git rev-list --left-right --count main...origin/main
git town --version
```

Interpretation:
- If there are uncommitted changes, stop and ask the user what to do.
- If `main` is behind `origin/main`, sync it before branching.
- If the current branch is not `main`, that is fine — `git town hack` can still create a branch off `main` — but only if the tree is clean.

### 2. Determine the branch name

If the user already provided a clear branch name, use it.

If the user gave only a feature description, convert it into a short kebab-case branch slug with the right prefix.

Examples:
- "create branch for feature xyz" → `feat/feature-xyz`
- "start a fix branch for candle parsing" → `fix/candle-parsing`
- "new docs branch for onboarding cleanup" → `docs/onboarding-cleanup`

If multiple names are plausible, show the best option and ask for confirmation.

### 3. Create the branch with Git Town

Primary command:

```bash
git town hack <branch-name>
```

This is the default and preferred path because it creates the branch off `main` and syncs relevant branches.

If Git Town reports that the repository still needs setup, stop and tell the user to initialise Git Town for the repo.

### 4. Verify the result

Run:

```bash
git branch --show-current
git status --short --branch
git town config get-parent || true
```

Confirm that:
- the current branch is the requested new branch
- the branch was created successfully
- the branch is based on `main`

### 5. Return a short handoff

Report:
- the branch name
- whether it was created from the latest `main`
- that development can now begin

## Expected behavior for trigger phrases

When the user says things like:
- `create branch for featurexyz`
- `start a branch for the next line of work`
- `make a new feature branch`
- `create feature branch for <task>`

then:
1. inspect repo state
2. ensure the tree is clean
3. derive or confirm the branch name
4. run `git town hack <branch-name>`
5. report success

No PR creation, no extra workflow steps, no manual `git checkout -b`.
