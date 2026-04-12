---
name: bug-check
description: "Run a staged post-context bug review for changed code or audited scope. Triggers on: bug check, silent bug review, edge case review, regression audit, post-context review, find silent failures, check for regressions. Use after audit-context-building or when an audit report, diff, or touched-file scope already exists. Not for Semgrep-only scans, CodeQL-only scans, or context-building from scratch."
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[scope or area]"
---

# Bug Check

Run an efficient but thorough bug-checking pipeline after context has already been built.

Natural-language triggers include:
- `bug check`
- `bug check backend`
- `silent bug review on the current diff`
- `edge case review for genesis`
- `regression audit on the last PR`

## Essential Principles

1. Context comes first.
   If there is no audited scope, no recent diff, and no touched-file set, use `audit-context-building` first. Bug review without scope control becomes noisy and misses cross-file assumptions.
2. Start narrow, then deepen only where risk justifies it.
   Review touched files, immediate callers/callees, and relevant tests before escalating into broader scans.
3. Silent bugs get their own pass.
   Do not merge silent-failure review into a general "find bugs" sweep. Hidden failure paths need dedicated attention.
4. Edge cases must map to test coverage.
   Every meaningful edge case should end in either `covered by existing test` or `missing test`.
5. Findings are claims, not vibes.
   Every finding needs line references, trigger condition, failure mechanism, and a confidence tag.
6. Tool escalation is selective.
   Use Semgrep, CodeQL, property-based testing, fuzzing, `fp-check`, or `variant-analysis` only when the failure mode fits. Do not run everything by default.

## When to Use

- The user says `bug check`, `regression audit`, `silent bug review`, `edge case review`, or similar.
- An `audit-context-building` pass already exists.
- A PR, commit range, or current worktree diff defines the scope.
- The task is to find bugs, silent failures, regressions, or missing tests rather than to implement code immediately.

## When NOT to Use

- The main need is architectural understanding with no review scope yet. Use `audit-context-building`.
- The task is a pattern-only static scan. Use `semgrep`.
- The task is explicitly cross-file taint/dataflow analysis. Use `codeql`.
- The task is to verify a suspected finding and eliminate false positives. Use `fp-check`.
- The task is to find sibling variants of one confirmed bug. Use `variant-analysis`.

## Preferred Inputs

Load the smallest sufficient input set:
- Existing audit report such as `AUDIT_CONTEXT_*.md`
- Touched files from a PR, commit range, or current worktree diff
- Relevant tests for the in-scope modules
- Any prior bug reports, failing tests, or runtime symptoms

Keep the static review rubric first and append repo-specific audited context later so repeated invocations stay cache-friendly.

## Sequential Pipeline

### Phase 1. Intake

Entry criteria:
- There is at least one of: audited scope, diff, touched-file list, or a user-named subsystem.

Actions:
1. Read the audit report first if one exists.
2. Build the working scope from changed files plus current uncommitted files when relevant.
3. Pull in immediate callers, callees, and nearby tests only where needed.
4. Classify the scope into one or more review lanes:
   - single-file pattern bugs
   - cross-file or dataflow bugs
   - stateful or edge-case bugs
   - parser or input bugs
   - silent-failure paths

Exit criteria:
- The scope is explicit.
- The review lanes are named.
- The next phases are narrowed to the real risk areas.

### Phase 2. Fast Pass

Entry criteria:
- Phase 1 produced a bounded scope.

Actions:
1. Read [workflows/fast-pass.md](fast-pass.md).
2. Review changed files plus immediate call edges.
3. Run cheap structural checks first and note candidate findings.

Exit criteria:
- Low-cost regressions and obvious bug candidates are either captured or ruled out.
- Remaining uncertainty is concentrated into the deeper lanes.

### Phase 3. Silent-Bug Sweep

Entry criteria:
- Fast pass is complete or a silent-failure risk is already obvious.

Actions:
1. Read [workflows/deep-pass.md](deep-pass.md).
2. Read [references/silent-bug-checklist.md](silent-bug-checklist.md).
3. Inspect hidden-failure paths separately from visible crashes.
4. Track whether failures degrade into false success, stale state, or dropped work.

Exit criteria:
- Silent-failure candidates are documented with trigger conditions and observability notes.

### Phase 4. Edge-Case Sweep

Entry criteria:
- The risky functions, modules, or flows are known.

Actions:
1. Continue the flow from [workflows/deep-pass.md](deep-pass.md).
2. Read [references/edge-case-matrix.md](edge-case-matrix.md).
3. Apply the compact edge-case matrix only to the risky surfaces, not every file.
4. Mark each meaningful edge case as `covered by existing test` or `missing test`.

Exit criteria:
- Edge-case coverage gaps are explicit.
- Candidate findings tie back to specific boundaries or state transitions.

### Phase 5. Tool Escalation

Entry criteria:
- Manual review identified a class of bug that benefits from targeted tooling.

Actions:
1. Read [references/tool-routing.md](tool-routing.md).
2. Escalate to the minimum fitting tool:
   - `semgrep` for recurring local patterns
   - `codeql` for interprocedural or dataflow questions
   - `property-based-testing` or fuzzing for parser, invariant, and state-machine surfaces
   - `fp-check` for shaky findings
   - `variant-analysis` after a confirmed seed issue

Exit criteria:
- Tool usage is justified by bug class rather than habit.
- Escalation outputs narrow or strengthen the candidate findings.

### Phase 6. Verification

Entry criteria:
- There is at least one candidate finding or one clear testing gap.

Actions:
1. Read [workflows/verification.md](verification.md).
2. Tag each finding as `confirmed`, `probable`, or `needs_repro`.
3. Remove weak claims that do not survive line-by-line verification.

Exit criteria:
- Every surviving finding has evidence, mechanism, and confidence.

### Phase 7. Findings Output

Entry criteria:
- Verification is complete.

Actions:
1. Output findings first, ordered by severity.
2. Then list open questions or assumptions.
3. Then list testing gaps and suggested test shapes.
4. Keep summaries brief and do not front-load the answer with overview prose.

Exit criteria:
- The output is immediately actionable for fixes or follow-up verification.

## Quick Reference

### Finding Tags

| Tag | Meaning |
|---|---|
| `confirmed` | The failure mechanism is directly supported by the code and needs no extra repro to be credible. |
| `probable` | The failure mechanism is strong but still depends on one assumption or runtime detail. |
| `needs_repro` | The concern is plausible but not yet strong enough to present as a confirmed bug. |

### Minimum Finding Shape

Every finding should include:
- file and line reference
- severity
- trigger condition
- failure mechanism
- likely user or system impact
- test shape or repro idea

## Reference Index

- [references/silent-bug-checklist.md](silent-bug-checklist.md)
- [references/edge-case-matrix.md](edge-case-matrix.md)
- [references/tool-routing.md](tool-routing.md)
- [workflows/fast-pass.md](fast-pass.md)
- [workflows/deep-pass.md](deep-pass.md)
- [workflows/verification.md](verification.md)
- [evals/seed-cases.md](seed-cases.md)

## Success Criteria

- The review starts from an audited or otherwise explicit scope.
- The fast pass is completed before broad tooling escalations.
- Silent bugs and edge cases are reviewed in separate dedicated passes.
- Findings are evidence-backed and severity-ordered.
- Test coverage gaps are called out explicitly.
- False positives are reduced through verification rather than hidden behind cautious wording.
