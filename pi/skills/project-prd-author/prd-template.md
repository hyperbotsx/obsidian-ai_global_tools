# Standard PRD Template

Use this structure for every non-trivial full PRD unless a section is explicitly not applicable.

```markdown
# PRD: <title>

> Canonical PRD source: this GitHub issue.
> Assigned agent: <agent label/process from profile>.
> Worktree/code home: `<profile worktree or implementation override>`.
> GitHub Project: <profile project link>.
> Proposed working branch: `<branch pattern; include issue number after creation>`.
> Base branch: `<base branch>`.
> Issue URL: <known URL or TBD until created>.
> Tracker: <profile tracker issue>.
> Dependencies: <issue links or none>.

## Status

- PRD status: Draft.
- CEO approved: No.
- Implementation status: Not started.
- Ready for implementation: No, pending approval.
- Owner: <agent/process>.
- Binding scope: <short scope>.

## 1. Problem

<What problem exists and who is affected.>

## 2. Goal

<Desired outcome in implementation-ready terms.>

## 3. Non-goals

<Explicitly out-of-scope work and risky actions not approved.>

## 4. Dependencies

<Upstream PRDs, contracts, data, approvals, or none.>

## 5. Functional requirements

<Numbered requirements.>

## 6. Allowed actions

<What implementation may do after approval.>

## 7. Forbidden actions

<What remains forbidden without separate approval.>

## 8. Acceptance criteria

<Testable completion criteria.>

## 9. Suggested validation

<Commands and manual checks expected for coder/verifier.>

## 10. Verifier checkpoints

<Checkpoint-sized review slices.>

## 11. Explicit non-approval statement

Completing this PRD only approves <scope after separate human approval>. It does not approve autonomous PRD approval, implementation outside scope, PR creation, merging, deployment, production readiness, backtests, paper trading, live trading, or bypassing human-confirmed action gates.
```

## Metadata Notes

- Replace placeholders after GitHub issue creation with the final issue URL and issue-numbered branch name.
- Keep approval fields Draft/No unless a separate CEO review workflow changed them.
- Pull owner, worktree, project, tracker, preview, and branch defaults from the active profile.
