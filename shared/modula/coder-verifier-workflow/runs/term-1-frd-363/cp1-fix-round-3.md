# CP-1 fix round 3 — coder

**You compacted since round 2. Everything you need is on disk — read these, do not rely on memory:**

- This brief.
- `/tmp/agentops/term1-363/cp1-verifier-verdict-r2.md` — the current verdict, with evidence paths.
- `/tmp/agentops/term1-363/cp1-fix-round-2.md` — contains my **binding F002 split ruling**, still in force.
- `/tmp/agentops/term1-363/cp1-coder-handoff-r2.md` — your own round-2 handoff.

Base is now `a9388e7`. Three commits on the branch: `a2b0b12` → `d035524` → `a9388e7`. You do no git.

## Where CP-1 stands

Findings have gone 8 → 4 → **2**. Closed and staying closed: F001, F003, F004, F005, F002-a, F006,
F007, plus the session-token extraction verified byte-identical. **The class (a) exit bar is met** —
the verifier confirmed silent `running`-with-nothing is now impossible for the spawn-gate failure
class, across every timing boundary, and it is regression-tested. Do not disturb any of that.

Two findings remain.

---

## CP1-F002 — two real observers still read stale state (high)

Your literal enumeration was **correct** — a TypeScript-checker audit confirmed you found every
direct `SessionGroup.status` property read, and the remaining ones are legitimate lifecycle
assignments. That part of your handoff was accurate. The gap is operational, not syntactic: two
decisions observe liveness *without going through the accessor at all*, so they never appear in a
`.status` grep.

**F002-i — lane runtime-slot decision.** `laneOccupiesRuntimeSlot`
(`server/laneOrchestrator.ts:252-258`) decides slot occupancy from cached session `recoverability`
without calling `observedGroupStatus`/`refreshGroupLiveness`. It backs `runningLaneSlotLetters`,
`activeLaneGroupCount`, and `batchLaneGroupCount`. Proof: with the only tmux pane killed and the
session still marked `recovered`, `runningLaneSlotLetters` returned `['A']`; only a later
`groupSummary` flipped it, after which the same reader returned `[]`. Impact is real — dead lanes
keep consuming execution-slot and batch capacity.

Refresh/observe once at the start of the common runtime-slot decision so all three callers see
physical state. **Keep counting genuinely live panes in partially-degraded groups** — do not turn a
partially-alive group into a dead one.

**F002-ii — Browser-QA preflight.** `browserQaPaneHandler`/`startBrowserPane` spawns before
observing the existing implementation group. With a physically dead but `recovered` coder pane, it
spawned and attached a Browser-QA pane, and that session was still present at return. Require a live
*observed* implementation group before any Browser-QA side effect.

Regressions required: a dead-tmux test calling **only** `runningLaneSlotLetters`; a lane-capacity
test where an unrelated dead lane no longer consumes capacity; and a Browser-QA test asserting the
spawn callback is **not** invoked for a dead group. Exact-call mutations for each, as before.

**Scope guard, unchanged:** no timer, no sweep, no notification bus. The verifier explicitly did not
request one. Proactive no-observer detection remains CP-3/FR-9.

## CP1-F008 — the AST guard will fight CP-2..CP-7 (low)

The AST rewrite did its job: comments and formatting no longer defeat it, and a real fifth parameter
is correctly rejected. Two brittleness defects remain:

1. **Hardcoded private names.** Renaming `launchPane` → `spawnPane` (both call sites, identical
   behaviour, full typecheck green) fails with `missing function launchPane`. That name is not a
   CP-1 architecture contract and will legitimately change in later checkpoints.
2. **Off-by-one line count.** `lineCount` uses the AST end position and reports 278 for a 277-line
   trailing-newline file — so a *legal* 299-line file would be read as 300 and rejected.

Fix by making it **more generic, not more clever**: traverse function-like AST nodes in the CP-1
modules and enforce the four-parameter maximum without looking up private names; correct the
trailing-newline line count; keep the AST import-boundary assertions. Dropping the name lookup should
make the test *shorter*. Prove a harmless rename and a format change both pass, while a real fifth
parameter still fails.

If this cannot be done cleanly, delete the test — that option stands. It was never an FRD
requirement, and a guard that blocks legitimate refactors for six checkpoints costs more than it
protects.

---

## Not in this round

Nothing else. No CP-2 gate/lane routing, no CP-3 sweep/Recover/Archive, no CP-4 store hardening, no
forge, multi-project, or wake work. Do not touch the eight closed findings.

## When done

Write `/tmp/agentops/term1-363/cp1-coder-handoff-r3.md`: per-finding status, revert-check result for
each new guard, and any disagreement stated plainly. Then `coms_send` to `lead`:
`cp-1 r3 handoff ready`.
