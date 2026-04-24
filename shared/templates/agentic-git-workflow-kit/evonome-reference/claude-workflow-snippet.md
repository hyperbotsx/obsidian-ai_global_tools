# Claude workflow snippet

Use this snippet pattern inside a repo-specific `CLAUDE.md` when you want the repo workflow to be authoritative.

## Workflow Authority (CRITICAL)

- `<repo-workflow-path>` is the canonical repo workflow for sprint branches, manual agent worktrees, preview deployment, PR handling, merge wrap-up, and deployment alignment.
- Agents must read `<repo-workflow-path>` completely before starting a new sprint, creating branches or worktrees, opening PRs, merging, or deploying.
- These workflow rules stay in force unless the user **explicitly** says they may be overridden for the current task. Convenience, urgency, implication, or silence do **not** count as overrides.
- Agents must actively guide the user into the workflow: create the correct sprint branch from `dev-main`, keep coding work off `main` and `dev-main`, prefer the `scripts/git/*` helpers when applying the workflow mechanically, use preview during development for browser-visible changes, and finish with the required sync and preview reset steps.

## Branch Naming Policy (CRITICAL)

- Long-lived branches:
  - `main`
  - `dev-main`
- Sprint branches created from `dev-main`:
  - `feat/<slug>`
  - `fix/<slug>`
  - `chore/<slug>`
  - `docs/<slug>`
- Agent branches created from the active sprint branch:
  - `agent/<sprint-slug>/<slice>`
- Slugs must be short, descriptive, and kebab-case.
- Never start new coding work directly on `main` or `dev-main`.
