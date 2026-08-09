# CP-1 re-verification dispatch (revision 3) — verifier

Read `/tmp/agentops/term1-363/verifier-standing-context.md` first if you have not already — your pane
was refreshed and that file plus your three prior verdicts are your memory.

Coder handoff: `/tmp/agentops/term1-363/cp1-coder-handoff-r3.md`. Both remaining findings (F002
consumer routing, F008 brittleness) claimed fixed, no disagreements. Git Manager is committing on top
of `a9388e7`.

Verdict to `/tmp/agentops/term1-363/cp1-verifier-verdict-r3.md`, then `coms_send` to `lead`:
`cp-1 r3 verdict ready`. Report to lead, never to the coder.

## This is a closing round — scope your effort accordingly

Findings have gone 8 → 4 → 2. Only two were open, both narrow, one of them low severity on a test
the FRD never required. **Do not go looking for new categories of work.** Verify these two closed,
confirm nothing regressed, and call it. If you find something genuinely serious that is in CP-1 scope
and class (a), of course raise it — but a fourth round on polish is not in anyone's interest.

## F002-i / F002-ii — the two missed observers you found

Re-run your own probes; do not trust the handoff:

- `runningLaneSlotLetters` called **alone** after killing tmux → must return `[]`, sessions stale.
- An unrelated physically dead lane must not consume launch capacity (their test uses global
  capacity 1).
- **A partially degraded lane must keep its live slot** — this is the case most likely to have been
  broken while fixing the others. The coder says the `some(...)` check stays pane-based deliberately.
  Verify a 2-pane lane with one dead pane still occupies a slot and does not get retired wholesale.
- Browser-QA: with a dead coder pane, neither the spawn callback nor the feed/preparation callback
  may fire. Confirm both entry points (`startBrowserPane` and `prepareBrowserQaLaunch`) are guarded,
  and that an already-attached Browser-QA pane stays idempotent.

## F008 — a disclosed limitation I want your judgement on, not a new round

The structural test now visits function-like AST nodes generically with no hardcoded private names,
and is proven in both directions: real fifth parameter fails; harmless rename and a legal 299-line
file both pass.

**The coder disclosed one loophole explicitly:** exported functions are exempted generically, because
two pre-existing exported APIs (`startLaunchGroup` 7 params, `startBrowserQaPane` 5) already exceed
the budget. So a future author could evade the parameter check by exporting a helper.

My position: **I am inclined to accept this.** The exemption is disclosed, the alternative
(name-based allowlist) re-introduces exactly the brittleness we just spent a round removing, and this
is a nice-to-have guard on a low-severity house rule. Tell me if you disagree and why — but unless
you think it actively hides a real defect, treat it as accepted and do **not** hold the checkpoint
for it. Record it as a known limitation in your verdict so it is on the record for CP-2..CP-7.

## Regression surface

Expect **1395 passed / 11 failed / 1406 total**, +5 net tests, same 11 baseline failures. Confirm the
failure *set*, not just the count. Also confirm no CP-2..CP-7 scope crept in and no git command was
run by the coder.

## Exit

If both close, return `approved` with the machine-status block, and state explicitly whether CP-1's
FR-1..FR-4 and AC-2 are met so I can gate the checkpoint and move to CP-2. If you return
`revision_requested`, keep the bounded actions genuinely minimal.
