# CP-2 fix round 1 — coder

Verdict: `/tmp/agentops/term1-363/cp2-verifier-verdict.md` — `revision_requested`, 4 findings.
**I accept all four.** Base is `993df2b`. You do no git.

First, credit where due: C-2, C-3, C-4 behaviour, and C-5 all passed on independent probes. The
architecture is right — board/planner producers use project defaults with no title inference, the
lane path re-defaults authoritatively, continuation starts four roles plus Lead and retires the brief
only on success. The defects are at the input boundaries, not in the design.

---

## Read this before you touch anything: F001 and F002 are the same bug twice

Both findings are **unvalidated input silently weakening a gate**:

- **F001** — `shared/launcher.ts:219` does `value.surfaces ?? []`. A partial config
  `{ policy: 'auto', scope: 'tiny' }` is accepted, normalized to `surfaces: []`, and then
  `contextBriefRoute` returns `skip / declared_small_scope`. **An incomplete project setting bypasses
  the brief entirely, with no operator reason.** That is the exact fail-open the checkpoint exists to
  prevent.
- **F002** — `server/index.ts:774` does `String(request.body?.reason || '').trim()` and
  `contextBriefTransition.ts:20` checks only truthiness. An object becomes `[object Object]` and
  passes the operator-reason gate. A 501-character string passes too.

And note what F002 actually is: **a recurrence of CP-1's F006.** In CP-1 you fixed hostile
*agent-written* reason data crossing into the API by requiring a bounded non-empty string. F002 is
the identical defect class on *operator-supplied* reason data, in a different field. We fixed the
instance and not the class.

So do not ship two patches. Do this:

1. Fix both instances properly (details below).
2. **Then sweep for the class.** Find every other place a `reason`, `statusReason`, or free-text
   operator/agent field crosses a trust boundary into state, an API response, or a gate decision.
   Apply the same bounded-string validation. Report what you found in the handoff — including
   "nothing else" if that is genuinely the answer, with how you searched.
3. If a single shared validator is the honest way to express this, write one. If the cases are too
   different to share cleanly, say so and keep them separate — do not force a bad abstraction.

Keep the sweep bounded to CP-1/CP-2 surfaces. Do not go refactoring CP-3..CP-7 territory.

---

## CP2-F001 — partial config must not weaken the default (high)

Require an explicit array-valued `surfaces` when a Context-Brief config **is** supplied. Keep
defaulting only when the **entire** project config is omitted — the verifier confirmed whole-config
omission correctly yields `{ policy: 'required', scope: 'unknown', surfaces: [] }`, and that must
stay. Valid caller configs must pass through unchanged; invalid ones must be **rejected**, never
degraded to something permissive.

Coverage: canonical parser + action config + HTTP handoff, for each missing required field,
null/non-object, invalid surface value, and skip-without-reason. Prove the omitted whole config still
routes `required`. Exact parser mutation required.

## CP2-F002 — the operator-reason gate must accept only real text (high)

Accept only a raw string, trim it, require non-empty content, and enforce the 500-character bound —
the same bound CP-1 established for brief state. Validate before any state mutation or phase-two
start.

HTTP regressions: empty, whitespace, null, object, array, number, exactly 500, and 501 characters.
Also confirm a reason supplied on the **ready** path is not persisted as degraded metadata (the
verifier says this currently behaves correctly — keep it that way).

## CP2-F003 — two wires have no reversion-sensitive guard (high)

This is the standing checkpoint bar and it is unmet independently of the two defects above.

1. **Mode identity in lane reuse** — removing `group.mode === request.mode`
   (`server/laneOrchestrator.ts:213`) left all 11 lane tests passing. This was *your own find* in
   round 0; it deserves a guard. Add a lane test with a live implementation group matching a
   required-gated request, proving it is not reused as a brief.
2. **Skip-decision attachment** — removing the `contextBriefDecision` attachment from the skip branch
   (`server/contextBriefLaunch.ts:20`) left all 19 focused tests passing. Add a configured-skip
   lane/direct test asserting the exact decision survives into the implementation task and the
   skipped-state path.
3. **Reason trimming** — removing HTTP trimming still passes the E2E test; the existing empty-string
   unit mutation does not protect whitespace normalization. Covered by F002's boundary tests.

## CP2-F004 — KISS (low)

`resolveProjectActionConfig` (`projectActionConfig.ts:98-117`) is exactly 20 physical lines; the rule
is under 20. New/expanded test callbacks at `tests/server.test.ts:270-299` (30 lines),
`projectActionConfig.test.ts` first case (21), and the expanded failed-transition case in
`contextBrief.test.ts` (21) also cross it.

Extract only what is needed to bring the newly-crossed functions under target. Do not refactor legacy
files or unrelated tests.

---

## Not in this round

No CP-3..CP-7 work. Do not disturb what passed: the producer/inference audit, the authoritative lane
defaulting, mode-identity behaviour, or the continuation/retirement ordering.

## When done

`/tmp/agentops/term1-363/cp2-coder-handoff-r1.md` — per-finding status, revert-check result for each
new guard, **the results of the trust-boundary sweep**, and any disagreement stated plainly. Then
`coms_send` to `lead`: `cp-2 r1 handoff ready`. Interim handoff first if you cross ~80% context.
