---
name: project-prd-author
description: Create, revise, or plan project-aware PRDs; shape requirements; decide when no PRD is needed; recommend split-scope PRDs across frontend, backend, data, training, trading, admin, orchestration, deployment, or shared-schema work; and draft or update GitHub PRD issues from the active AgentOps Harness profile. Use for PRD authoring, PRD revision, requirements shaping, issue-body PRDs, GitHub Project PRD setup, and split-scope planning. Do not use for simple direct answers, PRD approval, implementation, deployment, PR creation, merging, trading, backtests, or bypassing human gates.
---

# Project PRD Author

## Essential Principles

1. GitHub issue bodies are the canonical PRD source when a PRD is created there; do not create repo-local live copies.
2. Project-specific values come from the active AgentOps Harness profile, not memory or hardcoded defaults.
3. The workflow drafts and routes PRDs only; it never approves PRDs, starts implementation, creates PRs, merges, deploys, or authorizes trading/backtests.
4. Split multi-owner work before drafting when separate PRDs reduce conflict, unsafe coupling, or authority ambiguity.
5. Ask clarification questions only when missing information materially affects PRD correctness or safety.

## When to Use

- A human asks to create, write, revise, or shape a PRD.
- A request needs requirements, ownership, dependencies, validation, or verifier checkpoints before implementation.
- A feature may span frontend, backend/API, data, training/model, trading/backtest, admin, orchestration, deployment, or shared schemas.
- A human asks to create or update a GitHub PRD issue.
- A PRD draft needs project-aware owner, worktree, preview, tracker, branch, or GitHub Project fields.

## When NOT to Use

- Simple strategy questions, status questions, or quick implementation clarifications that can be answered directly.
- PRD approval, CEO review decisions, implementation, branch creation, PR creation, merging, deployment, production readiness, paper trading, live trading, or backtest authorization.
- Tasks where no active profile is available and the target project is ambiguous; ask for the profile first.
- Long-lived source-of-truth PRD copies in product repositories; use the GitHub issue body when canonical.

## Phase 1: Intake Routing

**Entry criteria:** A request mentions a PRD, requirements shaping, planning, feature scope, or GitHub issue PRD work.

1. Classify the request as one of: `answer_directly`, `new_prd`, `update_existing_prd`, `split_prds`, `follow_up_prd`, `park_idea`, or `needs_clarification`.
2. Use `answer_directly` for simple questions where a PRD would slow the human down.
3. Use `park_idea` for future ideas that are not ready for planning.
4. Use `needs_clarification` only when missing facts materially affect ownership, safety, dependencies, validation, or acceptance criteria.

**Exit criteria:** The route is explicit, and non-PRD routes stop without drafting a full PRD.

## Phase 2: Clarification Gate

**Entry criteria:** Phase 1 returned `needs_clarification`, or a drafting route has material gaps.

1. Ask concise option-based questions where practical.
2. Prioritize problem/outcome, affected areas, owner, dependencies, validation, preview/manual QA, and authority boundaries.
3. If enough context exists, state assumptions and continue rather than asking low-value questions.

**Exit criteria:** Required facts are known, the draft can proceed under stated assumptions, or the workflow stops for the human answer.

## Phase 3: Project/Profile Routing

**Entry criteria:** The request still needs a PRD or split-scope plan.

1. Read the active AgentOps Harness profile before assigning repository, Project owner/number, tracker issue, labels, worktrees, preview URLs, branch pattern, Git Town preference, or domain overlays.
2. If no profile is active and multiple profiles may exist, fail closed and ask for the target profile.
3. Treat profile state and current GitHub state as fresher than memory.
4. Keep global skill source in the AI Global Tools vault; do not write project-local skill copies.

**Exit criteria:** The target repository, project, owner labels, worktree/code home, tracker, preview/manual QA expectation, and branch baseline are known or the workflow is blocked safely.

## Phase 4: Split-Scope Planning

**Entry criteria:** Profile routing is complete and the request may touch more than one ownership area.

1. Check the split rubric in [split-scope-rubric.md](split-scope-rubric.md).
2. Recommend split PRDs when separate ownership, worktrees, API/data contracts, deployment config, or validation gates make one PRD risky.
3. For each proposed PRD, state title, owner/agent label, worktree, dependency order, sequential vs parallel safety, integration points, and preview/manual verification.
4. Ask before creating multiple GitHub issues unless the human already requested issue creation.

**Exit criteria:** The workflow has either one PRD scope or a human-readable split plan with dependency order.

## Phase 5: Draft PRD

**Entry criteria:** One bounded PRD scope is ready, or the human selected one PRD from a split plan.

1. Render the standard sections from [prd-template.md](prd-template.md).
2. Apply relevant overlays from [domain-overlays.md](domain-overlays.md).
3. Include allowed actions, forbidden actions, acceptance criteria, suggested validation, verifier checkpoints, dependencies, and an explicit non-approval statement.
4. Keep GitHub issue URL and issue-numbered branch placeholders until the issue number exists.

**Exit criteria:** A complete draft exists with all required global sections unless a section is explicitly not applicable.

## Phase 6: Readiness Self-Review

**Entry criteria:** A draft PRD or split PRD plan exists.

1. Run the checklist in [readiness-checklist.md](readiness-checklist.md).
2. Fix missing non-goals, ownership, dependencies, acceptance criteria, validation, verifier checkpoints, forbidden actions, preview/manual QA, or approval boundaries.
3. If readiness depends on unknown facts, ask targeted questions instead of guessing.

**Exit criteria:** The draft is implementation-ready for human review, or the workflow is blocked on specific missing information.

## Phase 7: GitHub Issue Create/Update

**Entry criteria:** The human explicitly asked to write the PRD into GitHub or update an existing PRD issue.

1. Follow [github-issue-workflow.md](github-issue-workflow.md).
2. Create/update draft PRD issues only in the configured repository and GitHub Project.
3. Keep CEO approval as No/Draft unless a separate CEO review workflow has explicitly approved it.
4. Update the issue body with the final issue URL and issue-numbered branch name after issue creation.
5. Do not create repo-local live PRD copies.

**Exit criteria:** The GitHub issue and configured draft project fields reflect the reviewed PRD without setting approval fields.

## Quick Reference

| Route | Result |
|---|---|
| `answer_directly` | Answer without PRD |
| `new_prd` | Draft one PRD |
| `update_existing_prd` | Revise the canonical issue body |
| `split_prds` | Propose multiple PRDs with dependencies |
| `follow_up_prd` | Draft after active work or at a safe boundary |
| `park_idea` | Record or summarize as backlog/future idea |
| `needs_clarification` | Ask bounded questions first |

## Reference Index

| File | Purpose |
|---|---|
| [split-scope-rubric.md](split-scope-rubric.md) | Ownership split signals and output format |
| [prd-template.md](prd-template.md) | Required PRD sections and metadata header |
| [domain-overlays.md](domain-overlays.md) | Frontend, backend/API, data, training, trading, and admin prompts |
| [readiness-checklist.md](readiness-checklist.md) | Self-review before issue creation/update |
| [github-issue-workflow.md](github-issue-workflow.md) | Safe GitHub issue and Project field workflow |

## Success Criteria

- The route is explicit before drafting.
- Profile-derived values are cited or unknown values are called out.
- Split-scope work is recommended when safer than one PRD.
- Full PRDs include metadata, status, problem, goal, non-goals, dependencies, requirements, allowed actions, forbidden actions, acceptance criteria, validation, verifier checkpoints, and non-approval statement.
- GitHub writes happen only when requested and never set approval fields by default.
