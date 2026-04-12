---
name: evonome-review-orchestrator
description: "Orchestrate Evonome code review using one bounded context audit followed by bug-check and selective deep tracing. Triggers on: review Evonome PR, audit Evonome diff, review Genesis changes, run context audit then bug check, Evonome regression review, Evonome bug-finding workflow. Use for polyglot Evonome reviews across backend, frontend, and related tests."
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
argument-hint: "[scope, PR, diff, subsystem, or area]"
---

# Evonome Review Orchestrator

Run the efficient-but-accurate Evonome review procedure.

This skill is a **workflow wrapper** for Evonome reviews. It tells Codex when to build context, when to bug-check, when to deepen analysis, and when to stop. It does **not** replace `audit-context-building` or `bug-check`; it orchestrates their use for Evonome's polyglot application surfaces.

## Essential Principles

1. **One Context Audit per bounded review scope.**
   Do a single context-building pass for the selected PR, diff, subsystem, or execution slice. Do not run a heavyweight context audit for every Ralph/Wiggum phase.

2. **Depth is selective, not uniform.**
   Not every file needs line-by-line micro-analysis. Reserve deep tracing for risky functions, cross-boundary flows, orchestration logic, and suspicious call chains surfaced during review.

3. **Evonome is polyglot and boundary-heavy.**
   Reviews must account for backend Python, frontend TypeScript/React, and optional Rust runtime edges when the active path crosses them.

4. **Context precedes bug claims.**
   First map entrypoints, callers/callees, invariants, trust boundaries, and nearby tests. Only then move into silent bug review, regression review, and targeted verification.

5. **Tool escalation must fit the bug class.**
   Use property tests, fuzzing, integration checks, or specialized static-analysis tools only when the failure mode justifies them.

6. **KISS review is advisory, not blocking.**
   Soft simplicity checks can flag obviously overgrown functions, deeply nested logic, or very long multi-responsibility files, but these are maintenance signals unless they directly contribute to a correctness bug.

## When to Use

- The user asks to review an Evonome PR, diff, subsystem, or sprint branch
- The user wants `context audit + bug check` for Evonome
- The review spans both backend and frontend surfaces
- The user wants a bounded, repeatable review workflow for Genesis, datafeed, memory, training, or orchestration changes
- The task is to find regressions, silent bugs, contract drift, or missing tests in Evonome code

## When NOT to Use

- The task is only to build architecture understanding with no review intent yet — use `audit-context-building`
- The task is only to perform post-context bug discovery on an already-scoped diff — use `bug-check`
- The task is a narrow static-analysis pattern hunt — use Semgrep or another specialized tool
- The task is implementation rather than review — use the normal planning / implementation workflow instead

## Evonome Risk Surface Quick Map

### Backend review hotspots

- `backend/app/api/`
- `backend/app/services/`
- `backend/app/ml/`
- selected files under `backend/tests/` adjacent to the touched surface

### Frontend review hotspots

- `frontend/src/genesis/`
- `frontend/src/prototype/`
- `frontend/src/services/`
- stores, hooks, chart config, and contract-mapping layers

### Optional Rust hotspots

- `indicators-rs/`
- `strategy-wasm/`

Only expand into Rust when the active runtime path, build path, or changed diff actually crosses those crates.

## Sequential Pipeline

### Phase 1. Intake & Scope Bounding

**Entry criteria:**
- The user named a PR, commit range, diff, subsystem, feature area, or review target.

**Actions:**
1. Identify the bounded review scope.
2. Prefer one of these scope anchors:
   - `dev-main...HEAD`
   - a PR diff
   - a named subsystem
   - a selected PRD execution slice
3. Build the smallest sufficient touched-file set.
4. Separate likely code-risk paths from docs, archives, generated artifacts, and unrelated churn.

**Exit criteria:**
- The review scope is explicit.
- The likely in-scope code paths are named.
- Unrelated churn is excluded from primary review attention.

### Phase 2. Context Audit Routing

**Entry criteria:**
- A bounded scope exists.

**Actions:**
1. Run the `audit-context-building` methodology against the bounded scope.
2. Produce a compact internal audit map containing:
   - entrypoints
   - callers/callees
   - state/data flow
   - trust boundaries
   - key invariants
   - nearby tests
3. For large scopes, keep the audit broad but shallow at first.
4. For smaller/high-risk scopes, trace deeper into the critical paths immediately.

**Exit criteria:**
- There is an explicit context baseline for the review.
- The highest-risk modules and call chains are identified.
- The review can proceed without “gist-level” guessing.

### Phase 3. Risk Clustering

**Entry criteria:**
- Context Audit is complete enough to distinguish hotspots from peripheral files.

**Actions:**
1. Classify risky surfaces into review clusters, such as:
   - backend API/service contract drift
   - orchestration/state-machine bugs
   - frontend/backend schema mismatch
   - stale state or silent UI failure
   - parser/input/config bugs
   - dataflow or temporal leakage risk
2. Mark which clusters require:
   - standard bug-check only
   - deep micro-analysis
   - later tool escalation
3. Note nearby tests per cluster.

**Exit criteria:**
- The review has named risk clusters.
- High-risk paths are separated from low-risk supporting files.

### Phase 4. Bug Check Routing

**Entry criteria:**
- The scope is bounded and the risk clusters are known.

**Actions:**
1. Run the `bug-check` methodology against the scoped diff/surface.
2. Prioritize:
   - silent failures
   - regressions
   - edge cases
   - missing caller updates
   - frontend/backend contract drift
   - false-success behavior
3. Keep findings tied to the bounded scope and its immediate dependencies.

**Exit criteria:**
- Candidate findings are identified.
- Open questions are narrowed to concrete call chains or boundaries.

### Phase 5. Selective Deep Tracing

**Entry criteria:**
- Bug Check surfaced risky functions, suspicious call chains, or unresolved high-risk areas.

**Actions:**
1. Re-enter ultra-granular micro-analysis only for risky functions/modules.
2. Apply line-by-line or block-by-block tracing to:
   - orchestration code
   - stateful service flows
   - external/API boundaries
   - frontend state/store/runtime contract layers
   - suspicious backend/frontend handoff paths
3. Propagate assumptions and invariants across the call chain instead of treating files in isolation.

**Exit criteria:**
- High-risk concerns are either strengthened, ruled out, or reduced to concrete repro questions.

### Phase 6. Soft KISS Maintenance Sweep

**Entry criteria:**
- The main correctness/regression review is already complete enough that maintainability notes will not distract from active bug risk.

**Actions:**
1. Run a light KISS pass on the touched scope only.
2. Flag only obvious complexity hotspots, such as:
   - functions that are clearly too long to scan comfortably
   - files that have become unwieldy or visibly multi-purpose
   - deeply nested control flow that resists quick understanding
3. Treat these as advisory findings:
   - `maintenance candidate`
   - `refactor follow-up`
   - `opportunistic cleanup while already editing`
4. Do **not** treat KISS findings as blockers unless they are directly causing or hiding a bug.

**Exit criteria:**
- Any obvious maintainability hotspots in the touched scope are noted.
- The review still keeps correctness and regression findings as higher priority.

### Phase 7. Verification Selection

**Entry criteria:**
- At least one credible concern, testing gap, or risky boundary has been identified.

**Actions:**
1. Choose the smallest relevant verification set.
2. Escalate selectively based on bug class:
   - targeted tests for known logic paths
   - integration checks for cross-surface behavior
   - E2E checks for user-visible orchestration
   - property tests or fuzzing for parser/invariant-heavy inputs
3. Avoid running heavyweight tooling by habit.

**Exit criteria:**
- Verification choices are justified by the failure mode.
- The review is supported by evidence rather than intuition alone.

### Phase 8. Findings & Handoff Output

**Entry criteria:**
- The review has either confirmed findings, narrowed open questions, or clear testing gaps.

**Actions:**
1. Output correctness and regression findings first, ordered by severity.
2. Then list open questions or unresolved assumptions.
3. Then list testing gaps and suggested test shapes.
4. Then list any KISS/maintainability notes as advisory follow-ups.
5. Keep the final summary compact and actionable.

**Exit criteria:**
- The review output is usable for fixes, follow-up verification, or PR discussion.

## Evonome Review Intensity Guide

| Scope size | Recommended procedure |
|---|---|
| Small localized change | Lightweight Context Audit + Bug Check + targeted verification |
| Medium feature slice | One bounded Context Audit + Bug Check + selective deep tracing on hotspots |
| Large or risky polyglot change | Broad bounded Context Audit + risk clustering + Bug Check + deep tracing only on critical paths |

## Practical Decision Rules

- If the main problem is **not understanding the subsystem yet**, start with Context Audit.
- If the scope is already understood and you need **bugs/regressions now**, route into Bug Check.
- If a suspicious finding depends on hidden assumptions, return to selective deep tracing.
- If the issue is clearly parser/config/invariant-heavy, consider property-based testing or fuzzing.
- If the issue is cross-stack and user-visible, prefer integration or E2E verification.
- If a touched file is obviously overgrown, note it for soft KISS follow-up, but do not let that displace higher-signal bug review.

## Reference Index

- `AI_Global_Tools/codex/skills/trailofbits-audit-context-building/SKILL.md`
- `AI_Global_Tools/codex/skills/bug-check/SKILL.md`
- `AI_Global_Tools/codex/skills/trailofbits-designing-workflow-skills/SKILL.md`
- `obsidian-evonome/tasks/prd/_current/prd-ralph-wiggum-quality-gate-workflow.md`

## Success Criteria

- The review starts from a bounded Evonome scope.
- Context Audit happens once per scope, not once per Ralph/Wiggum phase.
- Bug Check runs after context is explicit.
- Deep tracing is reserved for risky functions/modules/call chains.
- Soft KISS findings are advisory only and never outrank correctness/regression issues.
- Verification escalation matches the bug class.
- The final output is actionable, severity-ordered, and evidence-backed.
