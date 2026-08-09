# Readiness Checklist

Run this before presenting a final draft or writing/updating a GitHub PRD issue.

## Core Checks

- Is the problem clear and specific?
- Is the goal implementation-ready?
- Are non-goals explicit?
- Is owner/agent label clear and profile-derived?
- Is implementation home/worktree clear and profile-derived?
- Are dependencies and sequencing clear?
- Are acceptance criteria testable?
- Is validation realistic for coder/verifier execution?
- Are verifier checkpoints included and checkpoint-sized?
- Does the PRD include implementation hygiene / Steward readiness instructions?
- Are forbidden actions explicit?
- Does the PRD accidentally approve risky actions?
- Should this be split into multiple PRDs?
- Does the branch name end with `-<issue-number>` once known?
- Is preview/manual verification required, optional, or not applicable?
- If volatile external surfaces are in scope, is Research-first surfaces populated or explicitly `none`?

## Fail Conditions

Do not create or update a GitHub issue yet when:

- The target project profile is unknown or ambiguous.
- The PRD would assign an owner, worktree, or Project field from memory instead of profile/GitHub state.
- A large multi-owner request is being forced into one PRD without warning the human.
- Non-goals, acceptance criteria, validation, verifier checkpoints, or implementation hygiene / Steward readiness are missing from a non-trivial PRD.
- Approval fields would be set without a separate CEO review workflow.

## Output

If the draft passes, state:

```text
Readiness self-review passed: owner, worktree, dependencies, acceptance criteria, validation, checkpoints, implementation hygiene, and approval boundaries are explicit.
```

If it fails, revise the draft or ask the smallest set of targeted questions needed to pass.
