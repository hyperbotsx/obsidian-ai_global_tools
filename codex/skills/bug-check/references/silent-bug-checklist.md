# Silent Bug Checklist

Use this after the fast pass when the code can fail without looking broken from the outside.

## What Counts As A Silent Bug

A silent bug is a failure that:
- returns success-shaped output on failure
- drops work without surfacing a hard error
- serves stale or partial state as if it were current
- hides the real cause behind broad exception handling or fallback logic

## Checklist

### Error Handling

Look for:
- `except Exception`, bare `except`, or broad `catch` blocks
- logging-only handlers that continue as success
- default return values on parse, fetch, or persistence failure
- retries that suppress the terminal failure

Ask:
- What real error path reaches this handler?
- Does the caller still believe the operation succeeded?
- Is the original error preserved, downgraded, or discarded?

### Async And Concurrency

Look for:
- dropped `await`s
- fire-and-forget tasks with no join, status check, or cancellation path
- timeout handlers that return stale cached data as if fresh
- concurrent writes with no dedupe, lock, or version check

Ask:
- Can work be lost after the caller proceeds?
- Can two in-flight operations overwrite each other?
- Can timeout or cancellation be mistaken for success?

### State, Cache, And Persistence

Look for:
- partial writes across multiple stores
- write succeeds but cache invalidation is skipped
- stale caches or memoized values reused across changing inputs
- "best effort" persistence with no caller-visible downgrade

Ask:
- What state becomes inconsistent if only half the flow succeeds?
- Does the next read observe stale, mixed, or phantom state?
- Is there any compensating action?

### Input, Validation, And Schema Drift

Look for:
- invalid input coerced to a convenient default
- missing config or env vars silently replaced with permissive behavior
- incompatible schema changes handled by lossy fallback parsing
- UI or API fields ignored without warning

Ask:
- Does invalid input take a path that looks valid?
- Does the system silently change meaning rather than reject?
- Is the config/runtime state split-brained across layers?

### Frontend And UX Masking

Look for:
- loading states cleared after failure without an error surface
- optimistic UI that never rolls back
- background refresh failure that leaves stale data labeled as current
- toasts or console errors without state correction

Ask:
- What does the user believe happened?
- Is visible UI state inconsistent with backend truth?
- Would monitoring catch this failure or is it only a user-visible lie?

## Escalation Clues

Escalate when you see:
- repeated pattern across files: `semgrep`
- untrusted input moving across layers: `codeql`
- invariants on serializers, parsers, or reducers: `property-based-testing`
- uncertain but suspicious finding: `fp-check`

## Output Rule

A silent-bug finding is not complete unless it states:
- why the system appears successful
- what work or truth is actually lost
- how the bug would be detected, if at all
