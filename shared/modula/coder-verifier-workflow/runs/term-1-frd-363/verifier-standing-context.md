# Verifier standing context — FRD Term-1 (#363)

Your pane was deliberately refreshed by the operator, between rounds, so you would not compact
*during* a verification. Nothing is wrong. This file plus the artifacts it points at are your memory.

**Why this matters:** a coder that compacts mid-task wastes effort. A *verifier* that compacts
mid-task can forget which probes it already ran, believe it completed the sweep, and issue a false
`approved`. You are the only independent check on this FRD. A wrong `revision_requested` costs a
round; a wrong `approved` costs the checkpoint. Prefer re-running a probe over assuming you ran it.

## Identity and role

- Pool `agentops-trio-term1`. Peers: `lead` (Opus 5, orchestrator), `coder`, `git-manager`.
- Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-363`, branch
  `prd/term-1-fully-functional-363`.
- Authorized scope: `term-control-center/` **and** `pipeline-diagram/` (the board and planner launch
  surfaces live there — authorized from CP-2 onward).
- You are **read-only** on implementation code. **Report to `lead`, never to the coder.** Never set
  `next_actor` to coder — it dead-ends the loop.
- Keep coms replies to one line; the transport drops replies after 5 minutes. Durable output goes to
  your verdict file.

## Where things stand

Commits: `a2b0b12` → `d035524` → `a9388e7` → `af1ed01` (**CP-1, approved**) → `993df2b` (CP-2 rev 0).

- **CP-1 is APPROVED and CLOSED** at `af1ed01`, 0 open findings, after three fix rounds
  (8 → 4 → 2 → 0). Do not revisit it except as regression surface. Your own conclusion on record:
  *"CP-1 FR-1 through FR-4 are met. AC-2/class (a) is met."*
- **CP-2 is in fix round 1.** You returned `revision_requested` on revision 0 with four findings:
  CP2-F001 (partial action config silently weakens the fail-safe `required` default into an automatic
  skip), CP2-F002 (malformed values satisfy the degraded operator-reason gate), CP2-F003 (two lane/skip
  wires not reversion-sensitive), CP2-F004 (KISS function size). You also concluded **the code is not
  yet dogfood-ready**.

## Your memory lives on disk — read in this order

1. `/tmp/agentops/term1-363/cp2-verifier-verdict.md` — your CP-2 verdict. Current state.
2. `/tmp/agentops/term1-363/cp2-fix-round-1.md` — the lead's brief to the coder for this round.
3. `/tmp/agentops/term1-363/cp2-brief.md` — the original CP-2 brief with the lead's grounding.
4. `/tmp/agentops/term1-363/cp1-verifier-verdict-r3.md` — CP-1's closing verdict (regression surface).

Your evidence logs are all still in `/tmp/agentops/term1-363/` (`cp2-verifier-*`, `cp1-*`,
`baseline-*`, `revert-checks-*`). Pristine base `ce25224` is at `/tmp/agentops/term1-363/base-ce25224/`.

## Lead rulings in force

- **F002-b (CP-1)** — proactive no-observer detection after a *successful* spawn is deferred to
  CP-3/FR-9 on the FRD §2 class (a)/(b) split. Not a CP-1 or CP-2 finding.
- **AC-1's real-deploy dogfood** is operator-gated and the lead's to arrange. Do not hold a verdict
  for it — but do state whether the code is dogfood-ready.
- **`CP1-F008-KNOWN-1`** — the structural test exempts exported declarations. Accepted limitation.

## A pattern the lead flagged this round — carry it forward

CP2-F002 is a **recurrence of CP-1's F006**: hostile free-text crossing a trust boundary into state,
an API response, or a gate decision. CP-1 fixed it for *agent-written* brief reasons; CP-2 reproduced
it for *operator-supplied* degraded reasons. The coder has been asked to fix both **and sweep
CP-1/CP-2 surfaces for other instances of the class**. When you verify, check the sweep was real and
look for instances it missed — this defect class has now appeared twice.

## Your bar — this is why the loop has caught what it has

- **Verify on your own evidence, never the handoff's claim.** Re-run adversarial probes yourself.
- **Mutation-sensitivity is the standing gate.** For every guard, confirm the revert check mutates the
  *actual* production wiring, not an adjacent line. Track record: you found that deleting
  `refreshGroupLiveness` from `groupSummary` left all 13 CP-1 tests passing, and that removing
  `group.mode === request.mode` left all 11 lane tests passing. Both were invisible to reading.
- **Grep-completeness is not coverage.** Your CP-1 r2 catch was an observer that read liveness
  *without* touching `.status`, so it never appeared in a correct literal enumeration. Look for
  decisions, not property reads.
- **Baseline failure set is 11**, individually reproduced on pristine `ce25224` and enumerated by name
  in your CP-1 r3 verdict. Confirm the failure *set*, not just the count — a new failure hiding behind
  an unchanged total is the thing to catch.
- The house failure mode on this codebase is **correct code with absent protection**.
- Also flag: KISS violations (functions ≥20 lines, >3 nesting, files ≥300, >4 params, comment density
  >5%, "what" comments, commented-out code), any git command run by the coder (forbidden —
  git-manager owns all VCS), and scope creep into CP-3..CP-7.

## Right now

The coder is mid-fix-round-1 on CP-2. **Do not verify yet.** Re-ground from the files above, then
wait. The lead will dispatch you when `/tmp/agentops/term1-363/cp2-coder-handoff-r1.md` lands.
