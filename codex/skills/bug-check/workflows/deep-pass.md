# Deep Pass

Use this after the fast pass for the risk lanes that deserve more than a structural scan.

## Entry Criteria

- The fast pass identified risky flows, uncertain behavior, or missing coverage.

## Actions

1. Run the silent-bug sweep.
   Load `references/silent-bug-checklist.md` and inspect whether failures degrade into false success, stale state, dropped work, or hidden inconsistency.
2. Run the edge-case sweep.
   Load `references/edge-case-matrix.md` and apply only the meaningful dimensions to the risky surfaces.
3. Connect failures to tests.
   For each plausible bug or edge case, identify whether a test already covers it. If not, name the missing test shape.
4. Decide whether tooling helps.
   Load `references/tool-routing.md` and escalate only when manual review alone is too weak or too narrow.
5. Stop expanding when the marginal yield drops.
   The goal is efficient thoroughness, not endless search.

## Exit Criteria

- Silent-failure risks are either evidence-backed or ruled out.
- Edge-case gaps are explicit.
- Any escalated tooling has a clear reason.

## Deep-Pass Smells

- fallback branch that papers over a failed dependency
- retry loop that can double-apply or silently abandon work
- two sources of truth that can drift after a partial update
- boundary behavior that exists in code but not in tests
- UI state transition that implies success before backend truth is known
