# Modula product-skills — dogfood harvest log

**Purpose.** A durable, cross-cohort record of what the Modula product skills (`agentops-harness/skills/*`)
actually catch when we dogfood them on our own trio (coder + verifier) work. It exists because the skills'
central promise — *"start every gate advisory, measure its false-positive rate, then make it blocking"* — has
**no measurement mechanism in the skill files**. This log **is** that mechanism. It feeds two consumers:

1. The skills' **advisory→blocking graduation** decision (a check earns "blocking" only when its live FP rate is
   low over enough observations).
2. The **L1 built-in reviewer** (#620) — real catches/misses here are candidate checks + fixtures for the engine.

Single location (vault working artifact, not a skill — no repo mirror). Related: [[l1-620-reviewer-lane]] ·
`agentops-harness/skills/README.md` (the three-layer model) · `l1-620-cpc-plans/`.

## How to record (every dogfood cohort appends)
- The **coder** and **verifier** each add a short "Skills dogfood" block to their handoff/report: per skill-check
  that fired — what it caught, or that it was a false positive.
- The **Lead** reconciles those blocks into this log at closeout: one **log row** per observation, and increment
  the **tally**. Keep the tally honest — only *live* observations count toward graduation (retrospectives are
  parked separately below).
- **Verdict vocabulary** (per observation):
  - `TP` — true positive: flagged a real defect that was then fixed/addressed.
  - `FP` — false positive: flagged something that was not a defect (dismissed with reason).
  - `MISS` — a defect that shipped/was caught by *something else* (Kody, tests, the operator) that this skill's
    doctrine *should* have caught → a coverage gap / candidate new rule.
  - `NOISE` — advisory chatter that was neither wrong nor useful (low signal).
- **Graduation heuristic (proposed):** a check is a *blocking candidate* after **≥10 live observations** with an
  **FP rate < ~10%** and at least one TP. Fewer than that → stays advisory. This heuristic is itself under test.

---

## Per-check tally (the FP-rate ledger)

| Skill | Check / gate | Obs | TP | FP | MISS | FP rate | Blocking candidate? |
|---|---|---|---|---|---|---|---|
| machine-lint-pack | swallowed-errors | 0 | 0 | 0 | 0 | — | (already blocks, conf≥high) |
| machine-lint-pack | variant-files | 1 | 0 | 0 | 0 | 0% | (already blocks) |
| machine-lint-pack | type-strictness | 0 | 0 | 0 | 0 | — | no (advisory) |
| machine-lint-pack | dead-code | 1 | 1 | 0 | 0 | 0% | no (1 self-review TP) |
| machine-lint-pack | async-correctness | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | deprecated-pattern | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | banned-api | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | test-smell / shallow-tests | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | secrets | 0 | 0 | 0 | 0 | — | (already blocks) |
| security-per-pr | dep-vuln | 0 | 0 | 0 | 0 | — | (already blocks high/crit) |
| security-per-pr | injection (cross-file taint) | 0 | 0 | 0 | 0 | — | (blocks high-confidence) |
| security-per-pr | authz | 1 | 0 | 0 | 0 | 0% | no (agent-judgment) |
| security-per-pr | error-leakage | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | transport/headers | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | route-exposure | 0 | 0 | 0 | 0 | — | no |
| ai-ci-gate-pack | duplication | 0 | 0 | 0 | 0 | — | no (tool-gated) |
| ai-ci-gate-pack | dependency-freshness | 0 | 0 | 0 | 0 | — | no |
| ai-ci-gate-pack | integration-completeness | 1 | 1 | 0 | 0 | 0% | no (tool-gated; 1 doctrine TP) |
| ai-ci-gate-pack | test-quality (mutation) | 0 | 0 | 0 | 0 | — | no (tool-gated) |
| review-for-absence | scope-analysis | 0 | 0 | 0 | 0 | — | n/a (lens, advisory) |
| review-for-absence | untested-change | 0 | 0 | 0 | 0 | — | n/a |
| review-for-absence | missing-integration | 1 | 0 | 0 | 0 | 0% | n/a (corroborated the TP) |
| review-for-absence | missing-test-scenarios | 0 | 0 | 0 | 0 | — | n/a |
| review-for-absence | architectural-alignment | 0 | 0 | 0 | 0 | — | n/a |

*(Only the coder/verifier-facing skills are tallied. Lead/runner skills — frd/prd/impl-plan-author, vision-keeper,
enforcement-hooks — are dogfooded on Lead/authoring work; add rows if/when we dogfood those.)*

---

## Log (append-only; newest first)

<!-- Row format:
### <date> · <slice/PR> · <cohort>
- `<skill>#<check>` — **<TP|FP|MISS|NOISE>** — what it flagged; evidence (file:line / test); outcome (fixed / dismissed-w-reason / deferred / new-rule-candidate).
-->

### 2026-08-17 · AC-C2 per-finding dismiss/restore (backend) · PR #676 (merged e91351b9) · cohort coms-620cpc2 (coder Opus 4.8 + verifier Sonnet 5)
First live dogfood slice. **FP count across all skills: 0.** One real defect caught pre-review; the rest were
preventive applications that shaped the code with no false alarms.

- `ai-ci-gate-pack#integration-completeness` — **TP** — a naive "add `dismissReason` to `sanitizeFinding`" form
  always attached the key, which broke the CP-B AC-B1 `builtinReviewProvider` byte-identical trust-boundary test
  (a no-reason finding must round-trip unchanged). Caught at write time by running the adjacent consumer's test
  because the field lands on the *shared* sanitize path. Fixed with a conditional spread
  (`...(dismissReason ? {dismissReason} : {})`). Evidence: `builtinReviewProvider.test.ts` AC-B1;
  `server/kodyReview.ts` sanitizeFinding. **This is the highest-value data point so far** — it validates the
  small-PR + integration-completeness doctrine: a shared-path field change silently breaks a sibling contract, and
  only running the *consumer's* test surfaces it. Candidate fixture for the L1 built-in reviewer.
- `review-for-absence#missing-integration` — corroborated the above (verifier independently traced whether
  `restoreFinding`'s `dismissReason: undefined` actually clears on disk → through `patchFinding` → `sanitizeFinding`
  → `JSON.stringify` drops undefined keys → confirmed clean). Confirm, not an independent new catch.
- `machine-lint-pack#variant-files` — **NOISE (correct surface)** — flagged the `patchFinding` vs `markSelected`
  near-duplicate for a judgment call; adjudicated keep-separate (set→fixed-status map vs one-fingerprint→arbitrary
  patch — coincidental similarity, not shared meaning; duplication-beats-wrong-abstraction). The check firing was
  *correct* (it should surface near-dups); the resolution was no-change. Not an FP.
- `security-per-pr#authz` + injection/error-leakage — preventive-clean — new mutation routes placed behind the
  existing `guard`; untrusted operator `reason` sanitized (`cleanText`) + bounded (reused `REASON_TEXT_LIMIT`) at
  both route-input and persistence; error strings interpolate only the finding `status` **enum**, never the reason.
  No defect in this PR. **Coverage-gap candidate (surfaced, out-of-scope):** the *pre-existing* sibling
  `/kody-review/dismiss` (`kodyStatusHandler`) stores `request.body?.reason` **raw and unbounded** — the new code is
  strictly stricter. A later hardening PR should bound the session-level reason the same way; noted as a
  security-per-pr latent-gap candidate on existing code (parallels the #671 AC-C1 retrospective signal).
- `machine-lint-pack#async-correctness` — preventive-clean — the D-C2-1 design (no `await` between session load and
  `store.update`) is precisely this check's doctrine; verifier confirmed by tracing the full `*Sync` store/lock
  chain. Doctrine directly prevented a read-modify-write clobber race. No flag needed → not tallied, noted as a
  doctrine-shaped-design win.
- **Non-defect review advisory (not a skill flag):** `boundedReason` (truncates) sits next to shared `boundedText`
  (rejects) — same prefix, opposite over-limit behavior. Truncation is correct here; flagged for the next reader.
  Minor naming/readability nit → candidate for a future `machine-lint-pack` readability/naming-collision rule, but
  weak signal; not tallied.

**Takeaways:** (1) the integration-completeness TP is the single most useful catch — feed it to the L1 reviewer as a
fixture. (2) Zero FPs across a real slice is encouraging but N is tiny; keep accumulating before any advisory→blocking
move. (3) Two latent-gap candidates on *pre-existing* code (sibling raw reason; boundedReason naming) — hardening
backlog, not this lane.

### 2026-08-17 · AC-C2 per-finding dismiss/restore (FRONTEND) · PR #679 (merged 7aeee67a) · Lead-solo (no cohort)
The frontend half was Lead-built solo (operator chose Lead-build over a cohort), so the skills ran as a **self-review
lens**, not a coder/verifier split. Recorded because a doctrine catch is data regardless of who applied it.
- `machine-lint-pack#dead-code` — **TP (self-review)** — I first added a `dismissed: boolean` to the render
  `ReviewFinding`, then the dead-code/narrow-interface lens flagged that nothing reads it (membership in
  `dismissedFindings` + the hardcoded CSS class already carry the signal; `dismissReason` carries the reason).
  Removed before commit. Interface-bloat catch, pre-PR. Evidence: `reviewBoard.ts` ReviewFinding.
- `review-for-absence#scope-analysis` — surfaced the **non-blocking-rollup dismiss gap** (a medium/low
  `actionable_bug` is routed but, being rolled up, isn't individually dismissable from the UI). Not a defect — a
  conscious scope boundary documented in the PR + a follow-up candidate. Classified NOISE-adjacent / scope-signal.
- Kody: clean, zero inline findings on the head. Guardrail tests (not a skill) caught the 3 intentional invariant
  flips (incl. the "no per-finding write control" pin) — updated consciously; a reminder that deterministic pins +
  the absence lens are complementary.
- False positives: none.

---

## Retrospective (pre-dogfood) observations — NOT counted in the tally
Data points from before the skills were dogfooded live, kept separately so they don't skew FP rates. Useful as
coverage-gap signals only.

- **#671 (AC-C1, 2026-08-17) — coverage-gap candidate.** Kody caught a real safety bug: a malformed
  `session.maxLoopCount` (NaN/Infinity/≤0) could disable the survivor escalation. **Would any product skill have
  caught it at write time?** `machine-lint-pack` — no rule for "validate a numeric bound read from persisted/config
  state." `security-per-pr` — its untrusted-input doctrine is framed around *external* input, arguably a stretch to
  internal config. `review-for-absence` — plausibly ("missing validation on the new field / missing edge tests").
  **Signal:** consider a `machine-lint-pack` "unvalidated-config-bound" rule, or sharpen `review-for-absence`'s
  missing-test lens for numeric-bound edges. Track whether the live dogfood corroborates this gap.
