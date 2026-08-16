# FRD template — canonical skeleton

Copy the sections your effort tier requires (see `requirements.yaml` / SKILL.md §right-sizing).
`[R]` = required at every tier. `[tier]` = required from that tier up. Delete the guidance comments
(`<!-- … -->`) as you fill each section — a leftover guidance comment is padding, and padding is a
smell. Escalate a normally-omitted section with a one-line reason; never drop a tier-required one.

---

# FRD: <ID> — <Title>

<!-- Header block [R]: where the work lives. Done when every field is filled. -->
> Canonical FRD source: forge issue <#NNN> (`type:prd`, `status:draft`)
> PRD anchor: master PRD §<N> (the section this feature implements)
> Code home / repo: · Worktree/branch: <ends in the issue number> · Base branch: `main`
> Dependencies: · Team: · Effort tier: <XS|S|M|L>

## SUMMARY
<!-- [R]: ≤8 lines. The agent-facing digest, re-sent every iteration. Done when a compacted coder
     could re-anchor from this alone: what, why, the 1-3 load-bearing constraints, the done-signal. -->

## 1. Problem
<!-- [R]: the user-visible pain, in the customer's words. Done when a stranger understands why this
     is worth doing. No solution here. -->

## 2. Goal
<!-- [R]: the observable outcome. Done when it is stated as something a tool or person can observe
     ("reaches the dashboard in ≤3 steps"), not aspirational ("delightful onboarding"). -->

## 3. Non-goals
<!-- [R]: the fence. Done when it names what an agent on a long run must NOT add. -->

## 4. Constraints  [S]
<!-- Stack, boundaries, invariants the design must honor. Done when the design phase has no unstated
     freedom. (XS: fold the one or two constraints into the FRs instead.) -->

## 5. Functional requirements
<!-- [R]: what the system must do. One obligation per FR, MUST-phrased, actor named. -->
- **FR-1.** <Bold title.> The system MUST …
- **FR-2.** The user MUST be able to …

## 6. Acceptance criteria
<!-- [R]: verifiable conditions, cross-referenced to FRs. Done when each AC is runnable/observable
     and every FR has ≥1 AC. Prefer Given/When/Then. -->
- **AC-1** (FR-1): **Given** <state>, **When** <action>, **Then** <observable outcome>.

## 7. Design / approach  [M]
<!-- The *how* — architecture, data shapes, component boundaries, correctness properties (behavioural
     invariants the implementation must preserve). Appears only once requirements are settled. -->

## 8. Verifier checkpoints  [S]
<!-- CP-N mapping FRs/ACs → the gate the verifier runs. Table form is fine. -->
| CP | Covers | Gate |
|----|--------|------|
| CP-1 | FR-1, AC-1 | <suite/command green; AC-1 holds> |

## 9. Validation plan  [M]
<!-- Safe, scoped, runnable steps a verifier could execute without guessing. -->

## 10. Rollback / recovery  [M]
<!-- The undo path. Required whenever the change mutates state / is not trivially reversible. -->

## 11. Open questions  [M]
<!-- Ambiguities not yet resolved. Empty at approval, or each carries an owner + the gate that
     resolves it. Unresolved [NEEDS CLARIFICATION] markers land here. -->

## 12. Decisions  [L]
<!-- D-N: resolved operator decisions, dated. Mirrors the planning brief's resolved operator_decisions. -->
- **D-1** (<date>): <decision> — <rationale>.

## 13. Revision log  [L]
<!-- In-flight amendments, attributed and dated. Every post-approval edit is stamped. -->
