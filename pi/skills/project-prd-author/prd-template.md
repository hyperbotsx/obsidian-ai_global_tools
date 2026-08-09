# Standard PRD Template

Use this structure for every non-trivial full PRD unless a section is explicitly not applicable.

```markdown
# PRD: <title>

> Canonical PRD source: this GitHub issue.
> Assigned agent: <agent label/process from profile>.
> Code home / implementation repo: `<repository slug or code home>`.
> Worktree: `<profile worktree or implementation override>`.
> GitHub Project: <profile project link>.
> Proposed working branch: `<slug>-<issue-number>`; the final branch name must end with the PRD issue number.
> Base branch: `<base branch>`.
> Issue URL: <known URL or TBD until created>.
> Tracker: <profile tracker issue>.
> Dependencies: <issue links or none>.
> Research-first surfaces: <volatile APIs/SDKs/provider docs/auth/rate limits/deprecations requiring pre-implementation research, or none>.

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

<Commands and manual checks expected for coder/verifier. Include the mandatory researcher freshness consult when Research-first surfaces are named.>

## 10. Verifier checkpoints

<Checkpoint-sized review slices.>

## 11. Implementation hygiene / Steward readiness

The implementation agent must keep the change easy to review and steward:

- Keep changes scoped to this PRD; avoid opportunistic rewrites.
- Follow existing repo patterns and KISS principles.
- Place new files in the appropriate product, test, docs, or run-artifact locations.
- Do not leave temporary files, run artifacts, commented-out code, or unused code outside approved locations.
- Avoid hardcoded product names, local-only paths, or environment assumptions.
- Update tests/docs only where behavior changes require it.
- Provide a final handoff with touched files, validation commands, known risks, and cleanup notes.
- For large or cross-cutting changes, request Steward review before final bug-check / PR prep.

## 12. Explicit non-approval statement

Completing this PRD only approves <scope after separate human approval>. It does not approve autonomous PRD approval, implementation outside scope, PR creation, merging, deployment, production readiness, backtests, paper trading, live trading, or bypassing human-confirmed action gates.
```

## Metadata Notes

- Replace placeholders after GitHub issue creation with the final issue URL and issue-numbered branch name.
- Use the exact launch-context labels `Worktree` and `Proposed working branch`; do not substitute `Worktree/code home` or `Working branch` as the only metadata labels.
- The final branch name must end with `-<issue-number>`.
- Keep approval fields Draft/No unless a separate CEO review workflow changed them.
- Pull owner, worktree, project, tracker, preview, and branch defaults from the active profile.
- Use `none` for Research-first surfaces when no volatile external dependency needs a mandatory freshness consult.
