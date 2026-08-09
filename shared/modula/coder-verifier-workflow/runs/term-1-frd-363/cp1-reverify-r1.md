# CP-1 re-verification dispatch (revision 1) — verifier

The coder's revision-1 handoff is at `/tmp/agentops/term1-363/cp1-coder-handoff-r1.md`. All eight of
your findings are claimed fixed, with no disagreement recorded. The Git Manager is committing on top
of `a2b0b12` — verify the new committed revision.

Write the verdict to `/tmp/agentops/term1-363/cp1-verifier-verdict-r1.md`, then `coms_send` to
`lead` with `cp-1 r1 verdict ready`. Report to lead, never to the coder.

## Bar for this round

You called `revision_requested` on eight findings. Re-verify each one **closed on its own evidence**,
not on the handoff's say-so. I have already confirmed that all 11 logs under
`revert-checks-final/` show `# pass 0 # fail 1`, so the revert checks were really run — what I have
**not** confirmed is that each one mutates the *right* thing. That is your job:

- For each finding, check the revert check targets the **actual production wiring** that fix depends
  on, not an adjacent or trivially-coupled line. A mutation that fails a test for the wrong reason is
  no better than an insensitive test.
- Re-run your own adversarial probes rather than trusting the new tests. Specifically re-run the four
  that produced findings: no-coms context-brief pane, register-then-exit, all-dead lane relaunch,
  and concurrent retry overlap.

## Per-finding focus

- **F002 (the one that matters most)** — the claimed fix is a "stabilization interval + final tmux
  check". A fixed interval narrows a race; it does not necessarily close it. Probe whether a wrapper
  can still exit *after* the final check and leave the group `running`. If the window is merely
  smaller, say so explicitly and size it — I would rather ship a known-bounded window documented
  than an unbounded one believed closed.
- **F001** — verify *every* launch mode now gets a pool and a pre-spawn baseline: implementation,
  context-brief/review, draft, page-bot-control, and dynamic Browser-QA. Any mode still short-
  circuiting to success is the original defect surviving under a new name.
- **F003** — confirm the `Array.every` short-circuit is gone on **all** paths, and that a retired
  all-dead lane genuinely releases capacity rather than just changing status.
- **F004** — confirm the in-flight claim cannot deadlock or wedge a group permanently in "retry in
  flight" if the retry throws midway. A guard that leaks its claim on the error path converts a race
  into a permanent outage.
- **F006** — the handoff notes brief state is *omitted* when absent to preserve deep-equality for the
  Lead renewal test. Confirm that omission is genuinely invisible to existing consumers and did not
  paper over a real serialization regression.
- **F008 / `cp1Structure.test.ts`** — a structural test asserting file/parameter seams is good, but
  check it cannot be satisfied trivially and does not encode brittle assumptions that will fight
  CP-2..CP-7.

## Regression surface

Full suite should be **1387 passed / 11 failed / 1398 total** with the same 11 baseline failures you
already reproduced on `ce25224`. Confirm the count and that the failure *set* is unchanged — a new
failure hiding behind the same total is the thing to catch. Note the suite grew by 13 tests; confirm
they are the claimed CP-1 additions.

If everything closes, return `approved` with the machine-status block. If anything remains open,
return `revision_requested` with bounded actions as before.
