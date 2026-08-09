---
name: kiss
description: House KISS coding standards — size defaults with an escape hatch, structure rules, and the strict commenting discipline. Use when writing or reviewing code, or when asked to apply/check KISS compliance. Triggers on kiss, kiss check, kiss review, apply kiss, coding standards, simplify per kiss.
---

# KISS Coding Standards

Portable canonical copy of the house KISS rules. The worktrees `CLAUDE.md`
(`/mnt/hyperliquid-data/projects/worktrees/CLAUDE.md`) carries the same section for
auto-loading — **update both together** when the rules change.

## Structure rules

- Functions ≤ 30 lines (default, see escape hatch), single responsibility
- Max 3 nesting levels (use guard clauses/early returns)
- Max 3-4 parameters per function
- Files ≤ 500 lines (default, see escape hatch)
- Flat structures over deep inheritance
- Standard libraries before exotic dependencies
- Delete unused code, don't comment it out

**Size limits are defaults, not hard rules** *(operator decision, 2026-08-09)*: a
cohesive component may exceed them when splitting would create artificial coupling —
scattering one state machine across files makes code harder to reason about, not
simpler. Exceeding a default is a deliberate act: say so in the PR and name the seam
you'd split on when it becomes real. The pressure still points toward small; the
numbers are review triggers, not commandments.

*Origin of the escape hatch:* modula-runner CP-1 (2026-08-09) — 18 adversarial review
rounds were fast *because* functions were small and single-responsibility, but the old
hard 300-line file cap forced a knowing violation on a cohesive connection state
machine. Splitting mid-review would have made the code worse and reset review
convergence.

## Commenting rules

**The golden rule: naming > documentation.** If you feel the urge to comment, rename
the functions and variables until the comment feels redundant.

Zero redundancy: never explain *what* the code does — refactor for clarity instead.

Three permissible comment types:

| Type | Purpose | Example |
|------|---------|---------|
| Legal/Header | Required license or authorship | `# Apache 2.0 License` |
| The "Why" | Business logic, external constraints, workarounds, invariants the code cannot show | `# API requires v2 headers for legacy support` |
| Technical debt | Temporary hacks or future work | `# TODO: refactor after DB migration` |

Before finalizing, DELETE: comments repeating function/variable names, marker comments
(`# --- Variables ---`), commented-out code (git history holds it), "what" comments,
and changelog comments (git blame holds it).

Comment density target: < 5%. A well-named 70-line file with 0 comments passes; a
100-line file with 40 comment lines fails.

## Applying as a review pass

When asked for a KISS check on a diff or file set:

1. Flag functions/files over the defaults — then judge, don't auto-fail: is there a
   real seam, or would splitting create artificial coupling? Over-default without a
   stated reason in the PR is a finding; over-default with a named future seam is
   compliant use of the escape hatch.
2. Flag nesting > 3 levels, parameter counts > 4, dead/commented-out code.
3. Flag every "what" comment and any comment restating its neighbor.
4. Prefer renames over comment additions in your suggested fixes.

## Non-negotiables that ride along

- No hardcoded product names in code, databases, or identifiers — brand renders from
  config (`APP_NAME`) only.
- Pre-commit: no thinking-out-loud comments, no commented-out code, density < 5%.
