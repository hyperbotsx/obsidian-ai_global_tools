# CP-2 re-verification dispatch (revision 1) — verifier

Coder handoff: `/tmp/agentops/term1-363/cp2-coder-handoff-r1.md`. All four findings claimed fixed,
no disagreements. Git Manager is committing on top of `993df2b`.

Verdict to `/tmp/agentops/term1-363/cp2-verifier-verdict-r1.md`, then `coms_send` to `lead`:
`cp-2 r1 verdict ready`. Report to lead, never to the coder.

## Read this first: the sweep was Lead-directed, not scope creep

This round is much larger than four findings — 11 production files. **I ordered that.** After you
raised F001 and F002, I told the coder they were the same defect class twice, and that F002 was a
recurrence of CP-1's F006 (hostile free-text crossing a trust boundary). I instructed it to fix both
instances, then **sweep CP-1/CP-2 surfaces for the whole class** rather than ship two patches.

It reports finding **eight** instances and adding a shared `shared/boundedText.ts` primitive. So do
not flag the sweep's breadth as creep. What I want from you instead is whether the sweep was
**honest and complete**.

## Priority 1 — audit the sweep

- **Completeness.** The coder lists its search method (rg over `reason`, `statusReason`,
  `operatorText`, `resolution`, `message`, `String(request.body...)`) and the files it inspected.
  Run your own independent search with different terms and find an instance it missed. Your CP-1 r2
  catch is the model: a *decision* that reads hostile data without ever matching the obvious grep.
  This class has now surfaced twice on its own; assume a third.
- **Correctness of the shared primitive.** `shared/boundedText.ts` is now a dependency of many call
  sites, so a flaw in it is a flaw everywhere. Verify: strings only, trim-then-check (not
  check-then-trim), empty/whitespace rejected, default bound 500, the configurable larger bound used
  only where deliberate. `tests/boundedText.test.ts` gives it direct coverage — confirm that coverage
  is real and mutation-sensitive, not just present.
- **Bound values are judgement calls, not facts.** The coder chose 500 for reasons, 20,000 for
  planning brief plain text and page-bot messages, and moved planner receipt reasons from 4096 down
  to 500. Sanity-check each: is anything now bounded *too tightly* such that legitimate content gets
  rejected? A validator that silently truncates or rejects real operator text is a new defect, not a
  fix.

## Priority 2 — the four findings

- **F001** — a supplied config must require explicit valid `policy`, `scope`, and array-valued
  `surfaces`; whole-config omission must still yield `{ required, unknown, [] }`. Re-run your own
  config probe, including the exact `{ policy: 'auto', scope: 'tiny' }` input that produced the
  automatic skip, and confirm it is now rejected rather than normalized.
- **F002** — re-run your HTTP reason matrix yourself: empty, whitespace, null, object, array, number,
  exactly 500, 501. Confirm 400 with no state mutation and no phase-two start, and that a reason on
  the ready path still does not write degraded metadata.
- **F003** — confirm both new guards are genuinely reversion-sensitive by mutating the exact
  production wiring yourself: `group.mode === request.mode` in `laneOrchestrator.ts`, and the
  `contextBriefDecision` attachment in `contextBriefLaunch.ts`.
- **F004** — spot-check the extractions did not change behaviour.

## Priority 3 — the deferral

The coder found session-store raw restored `statusReason` validation and **deliberately left it**,
on the grounds that raw store schema hardening is CP-4, while sanitizing its output at the CP-1 API
boundary now. I consider that the right call. Verify the sanitization genuinely closes the
*checkpoint's* exposure — i.e. malformed restored data cannot reach an API response or a gate
decision — so what remains for CP-4 is only the store file itself.

## Regression surface

Expect **1412 passed / 11 failed / 1423 total** (+11 tests), same 11 baseline failures by name.
Confirm the set, not just the count. Also confirm CP-1's approved behaviour is not regressed —
`launchGroup.ts` and `contextBrief.ts` were both touched this round, and those are CP-1 surfaces.

## Exit

If everything closes, return `approved` and state explicitly whether **the code is now
dogfood-ready** — last round you said it was not, and that determines whether I arrange the AC-1
deploy. If findings remain, keep the bounded actions minimal.
