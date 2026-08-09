# Modula agent lifecycle: fail-closed teardown invariant (harvest)

Status: draft v1 · 2026-07-29 · owner: Erik + Lead
Source: hard-won on **E0 #355 CP-6** (9 revisions, 4 distinct LIFECYCLE bugs). The trio IS Modula's reference workflow, so this is a **product requirement for Modula's runner/lifecycle layer**, not a one-off.

Related: `frd-agent-comms-contract-draft.md`, `frd-agent-wake-renewal-driver-draft.md`, E0 Lead runtime FRD (#355).

## The invariant
Every path that DESTROYS an agent's container (group / session / worktree) must **fail-closed stop the standing agent BEFORE destruction**. If the stop is not proven successful, destruction MUST NOT proceed: return an error and PRESERVE the container for a bounded retry.

## Why — the 4 bugs it generalizes
CP-6's final bug-check uncovered the same class at four different callsites, each a separate revision:
- **LIFECYCLE-001:** the stop signal resolved on process `exit`/`error` before stdout was drained (lost the final turn), AND a child kill-error was treated as success. Fix: resolve *success* only on stdio `close` (drained); a kill-error is a discriminated FAILURE, never success.
- **LIFECYCLE-002:** a failed-stop child could be replaced by an interleaved start/send during the retry window. Fix: quarantine the failed child; block start/send from replacing it until a close-confirmed retry clears it.
- **LIFECYCLE-003:** explicit DELETE/retire routes fire-and-forget the stop, reporting success + deleting the container regardless. Fix: await stop; on failure return error (HTTP 409) + preserve state.
- **LIFECYCLE-004:** a container-destruction path with NO stop call at all (dead-matching-group replacement). Fix: route through the awaited fail-closed retirement helper; centralize non-agent cleanup behind a helper that DEFENSIVELY REJECTS agent-bearing containers.

## The completeness lesson (the meta-bug)
Auditing "every `stop()` callsite" is the WRONG axis — it misses destruction paths that have no stop call at all (that was LIFECYCLE-004, found only after an audit that was "textually complete" on the stop-callsite axis). The correct completeness axis is **"every CONTAINER-DESTRUCTION path"** (kill / delete / retire): enumerate each and confirm it either (a) awaits a fail-closed agent stop, or (b) is structurally incapable of holding an agent (mode-constrained + defensively rejected). Verify by enumerating destruction sites, not stop-callers.

## Acceptance
No destructive container-removal can report success while its agent remains alive; a failed stop always preserves the container for retry; a later real termination retry succeeds and only then removes it.
