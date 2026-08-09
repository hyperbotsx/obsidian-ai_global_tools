# CP-1 fix round 2 — coder

Verdict: `/tmp/agentops/term1-363/cp1-verifier-verdict-r1.md` — 4 closed (F001, F003, F004, F005),
4 open (F002, F006, F007, F008). Committed base is now `d035524`.

Good work on round 1: every one of the eleven revert checks was audited and ten of them were
confirmed to mutate the right production wiring. The four remaining items are real. Read the verdict
for evidence and file:line anchors.

---

## LEAD RULING ON F002 — read this before you touch anything

The verifier reports two distinct defects under F002. **They are not the same class and I am
splitting them.** The FRD is explicit (§2): *"Two distinct failure classes — do not conflate:
(a) orchestration (spawn gate never produces a live agent), (b) session management (dead sessions
unrecovered). F-1..F-6 are class (a); F-7..F-12 class (b)."* CP-1 owns class (a). CP-3 owns class (b).

**F002-a — pane dies while awaiting coms registration. IN SCOPE. Fix it.**
A wrapper that survives grace, exits at 150ms and never registers currently waits out the full
deadline and reports `did not register with coms before the deadline` — the wrong cause.
`pendingRoles` (`sessionSupervisor.ts:87`) never checks tmux. The registration poll loop is already
running; check tmux liveness on each iteration and fail immediately with the true exit cause. This
is squarely "the spawn never produced a live agent" and reporting a false reason is exactly the
observability defect CP-1 exists to remove.

**F002-b — pane registers, goes live, then dies later. SPLIT.**
The spawn *succeeded*. A session that dies afterwards is a dead session, which is class (b) and is
literally what CP-3/FR-9's liveness sweep is specified to catch. I am not pulling the sweep — or an
event-backed supervisor notification — into CP-1. But I am not letting it rot either. In scope now:

- Keep the `groupSummary` refresh (it is a real mitigation) **and** give it the regression guard it
  currently lacks — that is F007 below.
- **Enumerate every backend consumer that reads `group.status` directly** rather than through
  `groupSummary`, and route them through the one refresh-backed accessor. The verifier says
  "several"; find them all and list them in your handoff. This is bounded, enumerable work and it is
  the genuinely broken part — a consumer reading raw stale `running` is a lie the UI would have
  caught.
- Do **not** add a periodic sweep, a timer, or a notification bus.

What remains after that — proactive detection with *no* observer at all — is CP-3's sweep. Document
the residual window in your handoff with the verifier's measured numbers (~3.5–7s with an active UI
observer; unbounded with none) and state plainly that CP-3/FR-9 closes it. I would rather ship a
measured, documented, handed-off window than an unbounded one we believe is closed.

---

## F006 — brief-state reader accepts unsafe runtime data (fix, medium)

`readContextBriefState` (`contextBrief.ts:41-48`) validates the status enum but not `reason` /
`statusReason`. The state file is **agent-written**, so this is a live trust boundary. An object-
valued reason reaches the API and then throws `Objects are not valid as a React child` in
`GroupLaunchStatus`.

Require a bounded string for reason/statusReason before exposing state; otherwise omit the state or
emit a safe fallback. Normalize at the server boundary so every `/groups` consumer is protected, not
just the one component. Add malformed and missing-reason tests proving both API serialization and
rendering stay safe. FR-4 says state must be *surfaced* — a surface that crashes on hostile input is
not surfaced.

## F007 — the summary-observation wiring has no guard (fix, high — this is the gate again)

Deleting `refreshGroupLiveness(group, sessions)` from `groupSummary` leaves **all 13** focused CP-1
tests passing. The existing reuse test calls `refreshGroupLiveness` itself before `groupSummary`, so
it structurally cannot detect the removal.

Add a direct group-summary/API regression that starts from a physically dead tmux pane still marked
`recovered` and fails if the observation refresh is removed. Also add the guard for F002-a
(exit-while-awaiting-registration). Prove each by mutating its exact production call or branch.

Summary refresh is now the *only* mitigation for the window I deferred to CP-3 — so it must be the
best-guarded line in this checkpoint, not the least.

## F008 — the structural test is trivially bypassable (fix or delete, low)

`cp1Structure.test.ts:12-15` regexes raw source. In a scratch copy `launchPane` was given five
parameters and the one-parameter signature was left in a **comment** — the structural test and the
full typecheck both passed.

A bypassable test is worse than no test: it is false assurance, the same disease as F007. Two honest
options, pick one:

1. **Preferred** — parse TypeScript AST declarations and assert real parameter counts against the
   house threshold (3–4, not an exact-string match); use AST import declarations for the extraction
   boundaries; compute line counts robustly. Prove it with a bypass mutation using >4 optional
   parameters that does not rely on comments or formatting.
2. **Acceptable** — delete the test. The FRD never required it; it was your own initiative. Deleting
   is strictly better than keeping something that certifies nothing.

If option 1 runs past roughly 40 lines, take option 2 and say so. Do not spend a fix round building
a linter.

---

## Not in this round

No CP-3 sweep/Recover/Archive, no CP-4 store hardening, no CP-2 gate input surface or lane routing,
nothing forge/multi-project/wake. Do not disturb the four closed findings.

## When done

Write `/tmp/agentops/term1-363/cp1-coder-handoff-r2.md`: per-finding status, revert-check result for
each new guard, the full enumerated list of direct `group.status` consumers you rerouted, the
documented F002-b residual window, and which F008 option you took and why. Disagreements stated, not
skipped. Then `coms_send` to `lead`: `cp-1 r2 handoff ready`.
