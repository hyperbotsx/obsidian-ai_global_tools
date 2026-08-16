---
name: review-for-absence
description: Review AI-generated code for what is MISSING, not only what is wrong — the failure mode is plausible incorrectness that compiles, lints, and passes tests yet skips an integration, a scenario, or the scope. Provides scope analysis, missing-integration and missing-test detection, a "what's missing?" template, and risk-tiered review depth. Use when reviewing a change or configuring review. Language- and app-type-agnostic.
---

# Review-for-Absence

Traditional review assumes correctness and hunts for bugs. AI code passes the automated checks and
still fails in production — not because a line is wrong, but because something is **absent**: an
integration that should exist, a scenario that should be tested, files the change should have
touched. This skill reorients review toward absence, and routes depth by risk so reviewers are not
drowned by volume.

It is a **methodology that composes the other skills**: the mechanizable absences are owned by the
gate packs (`machine-lint-pack`, `ai-ci-gate-pack`, `security-per-pr`); this skill owns the review
*lens* — scope, the "what's missing?" pass, and how deep to look.

## Shift review upstream

The cheapest review is of the spec, not the diff: two minutes on a tight FRD (constraints, existing
patterns, integration requirements) beats forty-five on a 500-line PR. Where an FRD or plan exists,
review it first; a gap caught in the spec never becomes code.

## Risk tiers — match depth to consequence

Do not give every change the same scrutiny:

- **Tier 1 — automated.** Formatting, lint, the gate packs' blocking gates. No human attention.
- **Tier 2 — quick scan.** Standard, well-tested changes. Scope + "what's missing?" pass, ~minutes.
- **Tier 3 — deep.** Auth, payments, data models, migrations, new external surface. Full attention,
  the absence lens below applied in full, plus `security-per-pr` STRIDE where it triggers.

## The absence lens

### 1. Scope — before reading the diff
From the FRD/spec, **list the file changes you expect**. Then compare to the actual diff. Flag both
directions: expected changes missing (a wired-in place the change forgot) and unexpected changes
present (scope creep, unrelated edits). Owned here — it needs the spec, not a tool.

### 2. Missing integration
Does new code wire into the systems the codebase runs on — logging, error tracking, auth, request
context, flags? Reviewer-lens confirmation of `ai-ci-gate-pack#integration-completeness`; report the
gate's finding, do not re-derive it by hand.

### 3. Missing test scenarios
Are the failure modes and edge/negative cases tested, or only the happy path fifteen times? Compose
`ai-ci-gate-pack#test-quality` (mutation depth) and `machine-lint-pack#shallow-tests` (smells); the
reviewer's job is to name the *scenarios* that are absent, not the metrics.

### 4. Architectural alignment
Does a new abstraction match existing patterns, or reinvent one under a new name? Compose
`machine-lint-pack#abstraction-bypass` and, for spec/vision alignment, `vision-keeper`.

## The "what's missing?" template

Every non-trivial PR answers three absence questions explicitly:

```
## What's missing?
- [ ] Expected integration points (logging, error tracking, auth, context, flags)
- [ ] Required test scenarios (failure modes, edge/negative cases)
- [ ] Architectural alignment (existing patterns, justified new abstractions, scope match)
```

## As the reviewer

Pick the tier from the change's risk. Review the spec before the diff. Run the scope comparison
first — it is the highest-yield, lowest-cost step. For the mechanizable absences, read the gate
packs' findings rather than re-checking by hand, and spend human/agent judgment on the scenarios and
alignment a tool cannot name. Findings route to the coder; a new round auto-triggers; the loop ends
at clean, never at merged.

## Notes

- This skill deliberately owns little and composes much — its value is the lens and the routing, not
  a fourth copy of checks the gate packs already run.
- Feeds the product's §10 review flow (advisory rounds, route-to-coder, loop-until-clean) and its
  risk-tiering aligns with launch routing's per-FRD risk read (§3).
