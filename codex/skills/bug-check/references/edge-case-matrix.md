# Edge-Case Matrix

Apply this only to the risky functions, modules, or flows identified in the fast pass.

## Core Dimensions

| Dimension | Examples | What To Inspect | Test Expectation |
|---|---|---|---|
| Empty / Missing | empty list, empty string, absent file, missing record | assumptions about presence, indexing, default branches | explicit reject, no-op, or safe empty result |
| Null / None | `None`, `null`, optional field omitted | dereferences, fallback logic, schema adaptation | handled intentionally, not accidentally coerced |
| Zero / One | `0`, `1`, single-item collections | division, pagination, loop bounds, first-item logic | correct boundary behavior |
| Min / Max Boundary | smallest and largest allowed values | range checks, truncation, overflow, slicing | boundary checked and test-covered |
| Duplicate / Replayed Input | repeated request or same key twice | idempotency, dedupe, retry safety | no double-write or duplicate side effect |
| Missing Config | absent env, partial config, stale feature flag | fallback defaults, startup assumptions, split config paths | fail closed or surface configuration error |
| Timeout / Cancellation | request timeout, aborted task, partial response | cleanup, retry, stale fallback, caller-visible status | timeout is explicit, not disguised as success |
| Stale State / Concurrency | outdated cache, concurrent edit, out-of-order event | version checks, invalidation, last-write wins | deterministic or guarded outcome |
| Time / Locale | timezone boundary, DST, locale formatting | date math, serialization, parsing, UI display | consistent across zones and formats |
| Precision / Rounding | floats, decimals, currency, percentages | comparisons, aggregation, display rounding | stable and intentional precision rules |
| Partial Failure | second write fails, one dependency unavailable | rollback, compensating logic, visible downgrade | safe recovery or explicit failure |

## Where This Matters Most

Prioritize the matrix for:
- parsers and normalizers
- state transitions
- persistence and cache coordination
- API adapters and schema bridges
- scheduling, timing, and background jobs
- UI flows with optimistic updates or derived state

## Coverage Rule

For each meaningful edge case, record one of:
- `covered by existing test: <test file or test name>`
- `missing test: <suggested test shape>`

Do not list trivial cases just to look thorough. The matrix is for risk concentration, not paperwork.
