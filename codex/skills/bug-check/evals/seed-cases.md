# Seed Cases

Use this file to accumulate known good evaluation cases for the `bug-check` skill.

## Record Format

For each case, keep:
- scope source: PR, commit range, or touched-file set
- expected bug class: silent bug, regression, edge case, cross-file flow
- expected finding count
- known true positives
- known false positives
- expected missing-test gaps

## Starter Case Types

- silent fallback returns stale cached data as fresh
- partial write updates storage but not cache or index
- duplicate request applies side effects twice
- invalid input coerces to permissive default
- timeout path reports success without completing work
- frontend optimistic update never rolls back on backend failure
