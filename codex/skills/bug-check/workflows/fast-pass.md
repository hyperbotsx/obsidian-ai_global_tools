# Fast Pass

Use this workflow for the cheap, high-yield review before deep analysis.

## Entry Criteria

- A bounded scope exists from an audit report, diff, touched-file list, or named subsystem.

## Actions

1. Contract the scope.
   Focus on changed files, direct callers/callees, and nearby tests. Do not fan out into the whole repo unless the call chain forces it.
2. Read for intent and invariants.
   Identify what each changed unit claims to preserve: state transitions, input validation, cache behavior, ordering assumptions, or UI truthfulness.
3. Run cheap structural searches.
   Look for recent additions or risky edits around:
   - broad exception handling
   - fallback defaults
   - missing await or unjoined async work
   - cache invalidation gaps
   - config branching
   - optimistic UI or derived state changes
4. Compare code to tests.
   Check whether the changed behavior already has a relevant test. Missing tests are part of the review output.
5. Capture candidate findings, not final findings.
   Note suspicious locations and why they matter, but defer confidence tags until verification.

## Exit Criteria

- Obvious regressions and cheap bug candidates are captured.
- The remaining risk is narrowed to a smaller set of functions, flows, or modules.
- You know whether to continue into silent-bug review, edge-case review, or tool escalation.

## Common Fast-Pass Wins

- changed error-handling branch now returns success-shaped data
- new optional field is parsed but not propagated
- store update and UI derivation are out of sync
- config flag added in one layer but not honored in another
- test coverage stops before the newly introduced boundary
