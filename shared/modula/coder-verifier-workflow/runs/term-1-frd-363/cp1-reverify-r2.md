# CP-1 re-verification dispatch (revision 2) — verifier

Coder handoff: `/tmp/agentops/term1-363/cp1-coder-handoff-r2.md`. All four remaining findings
(F002, F006, F007, F008) claimed fixed, no disagreements. Git Manager is committing on top of
`d035524` — verify the new committed revision.

Verdict to `/tmp/agentops/term1-363/cp1-verifier-verdict-r2.md`, then `coms_send` to `lead`:
`cp-1 r2 verdict ready`. Report to lead, never to the coder.

## Lead ruling you must verify against — not the one you wrote

I split F002 rather than accepting it whole, on the FRD §2 class (a)/(b) taxonomy:

- **F002-a** (pane dies *while awaiting registration*, wrong cause reported) — CP-1 scope, must be
  fixed and guarded now.
- **F002-b** (pane registers, lives, then dies) — the spawn succeeded; a session dying later is
  class (b), which is CP-3/FR-9's sweep. **I deferred proactive no-observer detection to CP-3.**
  In scope for CP-1 was only: keep summary-time refresh, guard it, and route every direct
  `group.status` consumer through the refresh-backed accessor.

So do **not** re-raise F002-b's no-observer window as an open CP-1 finding. It is recorded against
task CP-3 with your measured numbers. What I *do* want from you on it:

1. **Audit the consumer enumeration for completeness.** The handoff lists ten categories rerouted
   and claims the only remaining raw `group.status` accesses are the authority inside
   `groupStatus.ts`, lifecycle transition *assignments*, and queued-lane status assignment. Go find
   a consumer they missed. A single unrouted read that returns stale `running` re-opens the hole the
   ruling depends on. This is the highest-value thing you can do this round.
2. **Confirm the deferral is honest** — that the residual really is bounded to "no observer at all",
   and that any observation path genuinely fails closed.

## Per-finding

- **F002-a** — confirm the poll-loop tmux check fires on every iteration *and* at loop exit, and the
  reason is the true cause. Probe a pane dying at various points: before grace, inside grace, after
  grace but before registration, and exactly at the deadline boundary.
- **F006** — bounded string, non-empty, ≤500 chars, state omitted otherwise. Probe hostile inputs
  beyond what the coder tested: arrays, nested objects, `null` vs `undefined`, unicode/control
  characters, and a reason that is exactly 500 vs 501. Confirm the omission is at the **server**
  boundary so every `/groups` consumer is protected, not just `GroupLaunchStatus`.
- **F007** — the new `reusableGroup` guard calls *only* `groupSummary` (the previous one called
  `refreshGroupLiveness` itself, which is why it was blind). Verify that is actually true of the new
  test, then re-run your own mutation: replace `observedGroupStatus` in `groupSummary` with raw
  `group.status` and confirm failure.
- **F008** — `cp1Structure.test.ts` is now AST-based at 39 lines. Verify it cannot be satisfied by
  comments or formatting, that the threshold is `<= 4` rather than an exact signature, and that it
  will not fight CP-2..CP-7 with brittle assumptions.

## New-surface risk

`sessionToken.ts` was extracted from `sessionStore.ts` to break a runtime dependency cycle. That is
attach-token code — the same security-relevant path you verified byte-identical in C-3. **Re-verify
it is still byte-identical** and that the cycle-breaking did not alter digest/salt behaviour or
import order semantics.

## Regression surface

Expect **1390 passed / 11 failed / 1401 total**, same 11 baseline failures, +3 net tests. Confirm the
failure *set* is unchanged, not just the count.

If everything closes, return `approved` with the machine-status block, and state explicitly that the
CP-1 exit bar (AC-2: silent `running`-with-nothing is impossible, test-enforced) is met for
class (a). If anything remains open, return `revision_requested` with bounded actions.
