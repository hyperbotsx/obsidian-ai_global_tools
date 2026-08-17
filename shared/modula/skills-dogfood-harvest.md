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
| machine-lint-pack | variant-files | 0 | 0 | 0 | 0 | — | (already blocks) |
| machine-lint-pack | type-strictness | 0 | 0 | 0 | 0 | — | no (advisory) |
| machine-lint-pack | dead-code | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | async-correctness | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | deprecated-pattern | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | banned-api | 0 | 0 | 0 | 0 | — | no |
| machine-lint-pack | test-smell / shallow-tests | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | secrets | 0 | 0 | 0 | 0 | — | (already blocks) |
| security-per-pr | dep-vuln | 0 | 0 | 0 | 0 | — | (already blocks high/crit) |
| security-per-pr | injection (cross-file taint) | 0 | 0 | 0 | 0 | — | (blocks high-confidence) |
| security-per-pr | authz | 0 | 0 | 0 | 0 | — | no (agent-judgment) |
| security-per-pr | error-leakage | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | transport/headers | 0 | 0 | 0 | 0 | — | no |
| security-per-pr | route-exposure | 0 | 0 | 0 | 0 | — | no |
| ai-ci-gate-pack | duplication | 0 | 0 | 0 | 0 | — | no (tool-gated) |
| ai-ci-gate-pack | dependency-freshness | 0 | 0 | 0 | 0 | — | no |
| ai-ci-gate-pack | integration-completeness | 0 | 0 | 0 | 0 | — | no |
| ai-ci-gate-pack | test-quality (mutation) | 0 | 0 | 0 | 0 | — | no (tool-gated) |
| review-for-absence | scope-analysis | 0 | 0 | 0 | 0 | — | n/a (lens, advisory) |
| review-for-absence | untested-change | 0 | 0 | 0 | 0 | — | n/a |
| review-for-absence | missing-integration | 0 | 0 | 0 | 0 | — | n/a |
| review-for-absence | missing-test-scenarios | 0 | 0 | 0 | 0 | — | n/a |
| review-for-absence | architectural-alignment | 0 | 0 | 0 | 0 | — | n/a |

*(Only the coder/verifier-facing skills are tallied. Lead/runner skills — frd/prd/impl-plan-author, vision-keeper,
enforcement-hooks — are dogfooded on Lead/authoring work; add rows if/when we dogfood those.)*

---

## Log (append-only; newest first)

_No live observations yet — **AC-C2 (per-finding dismiss/restore) is the first dogfood slice.**_

<!-- Row format:
### <date> · <slice/PR> · <cohort>
- `<skill>#<check>` — **<TP|FP|MISS|NOISE>** — what it flagged; evidence (file:line / test); outcome (fixed / dismissed-w-reason / deferred / new-rule-candidate).
-->

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
