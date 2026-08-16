---
name: prd-author
description: Author and maintain the master PRD — the one living, operator-driven single-source-of-truth product document, kept at the right altitude and prevented from drifting. Use when editing the master PRD or raising a PRD amendment. Covers section altitude (product what/why, not feature detail), amendment discipline through the human gate, provenance/attribution, two-way reconciliation with the plan and FRDs, and protected invariants. Language- and product-agnostic.
---

# PRD Author

The master PRD's one job is to be the single source of truth for what the product is, for whom, and
why. Its failure mode is **drift** — decisions get made downstream (in FRDs, PRs, design) that never
flow back, and the document and the product diverge. This doctrine keeps the PRD *true*: at the right
altitude, changed only through the gate, attributed, and reconciled with what actually exists.

Its bias, unlike a feature spec, is **stability and convergence, not completeness — the best PRD edit
is the smallest one that keeps the document true.**

It is **one doctrine, two consumers**: the *Author* (scope `master-prd`) receives it as an editing
overlay, and the *amendment/reconciliation pipeline* enforces `prd-rules.yaml` beside this file.

## Terminology

- **PRD** = the one master document per project (`docs/product-prd.md`). **This skill governs it.**
- **FRD** = every per-feature doc, traced back to a PRD section (governed by `frd-author`).
- The distinction is fixed and load-bearing (below). Do not let the two vocabularies blur.

## How to invoke

- Claude Code: `/prd-author` · Codex: `$prd-author` · Pi/OpenCode: `/skills` picker.

## The altitude rule (the one that matters most)

The PRD says **what the product is and why**; an FRD says **how one feature works**. The commonest
way to ruin a master PRD is to let feature detail leak in.

- **Belongs:** vision, users/deployment, operating model, roles, the load-bearing invariants (§15
  authority floor, §14 security posture), the settings taxonomy, and the open questions not yet
  decided.
- **Does NOT belong:** feature mechanics, acceptance criteria, implementation/UI detail. **If a
  passage could be an FR, it belongs in an FRD** — propose moving it out and leave a one-line PRD
  pointer.

The PRD is the project's constitution + steering document: it earns its keep by being *current and
stable*, not long. A section grows only when the *product definition* changed — never when a feature
was built (that's an FRD tracing back, not a PRD edit). `prd-rules.yaml` holds the per-section
belongs / does-not-belong map.

## Amendment discipline — how to change a living doc safely

- **Nothing auto-applies.** Any producer (an FRD, a PR, a design change) may *raise* an amendment; the
  operator confirms. Never a silent edit.
- **Carry the origin.** Every proposal names its originating source; every applied amendment writes a
  **§17 revision-log entry naming its origin and date** — this is the "what changed / why / who" record
  that prevents drift.
- **Cosmetic is filtered, not escalated.** Layout, spacing, colour, and copy-wording changes are
  acknowledged, never gated. Anything that changes a **capability, a contract, an invariant, or a
  user-visible promise** is substantive and goes through the gate. (`prd-rules.yaml` declares the
  split — do not guess case by case.)
- **The reverse gap is a work request, not an amendment:** a PRD statement with no surface behind it
  is raised as a design/plan work request.
- **Amend the spec first, then act.** When intent evolves, the PRD updates before the guardrail or the
  build follows it — never patch around a stale PRD.

## Provenance & attribution

Who wrote a passage is load-bearing: an operator-written section and an agent-drafted one carry
**different authority**, and the document must never make them look alike.

- Operator edits are marked, attributed, and carry their **previous wording** (recoverable in place);
  agent drafts are marked as such.
- The PRD keeps **named version snapshots**, read-only and restorable; a restore is itself a
  revision-stamped edit.
- When the plan and the build disagree, provenance is what tells you which to trust.

## Reconciliation — the anti-drift routine

Run two-way, **on demand and after each FRD approval or PR merge** (not on a timer):

- A **PRD section with no plan item / no surface** → a promise nothing schedules → raise a design/plan
  work request.
- A **built surface / plan item with no PRD section** → the definition doesn't describe what exists →
  raise an amendment proposal.

Both surface as **proposals, never automatic edits.** The PRD *converges* with what is built rather
than drifting from it. Boundary: the board owns execution state, the Implementation Plan owns
order/lanes, the PRD owns *definition* — never let the three become competing sources of truth.

## Less-is-more

- **Bloat is a smell** — a section drifted into feature detail, restating another, or accreted dead
  history is flagged. Prefer the smallest edit that keeps the doc true.
- **Open Questions over premature detail** — undecided things live in §16 with a decision owner;
  deciding is an operator act, not speculative prose elsewhere.
- **Feature detail leaves for an FRD** — flag and propose the move; do not auto-create the FRD.

## Protected invariants — never weakened by a routine amendment

An amendment that would do any of these is **refused**; changing them requires an explicit,
recorded operator decision:

- **The §15 authority floor** — grant no autonomous approval / PR / merge / deploy / trading. (Gated,
  future, or non-goal framing is fine; *granting* is refused, as the FRD reviewer's hard floor refuses
  it.)
- **The product-naming rule** — no hardcoded product name in examples; `APP_NAME` config only.
- **The fixed PRD/FRD terminology.**

## Notes

- Feeds Modula's existing §3 amendment-proposal pipeline and the reconciliation checker — it adds no
  parallel approval path. Sibling of `frd-author` (feature specs); shares the anti-bloat + provenance
  DNA, differs in altitude (living product definition vs green-field feature).
- The machine-readable altitude map, amendment/cosmetic rules, invariant checks, and reconciliation
  directions live in `prd-rules.yaml` (a Modula engine extension, not part of the Agent Skills
  standard) — the enforcement half of the contract.
