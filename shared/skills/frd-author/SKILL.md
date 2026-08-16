---
name: frd-author
description: Author professional, right-sized Functional Requirements Documents (FRDs) set up for agentic execution. Use when drafting or reviewing an FRD/feature spec. Covers the canonical section skeleton, concrete goals, explicit constraints and non-goals, verifiable acceptance criteria (Given/When/Then), effort-tiered right-sizing (less is more — empty AND padded sections are smells), and the quality-rubric criteria. Language- and stack-agnostic.
---

# FRD Author

A spec an agent can build from is **goals + constraints + verifiable acceptance criteria**. Drop any
one and the agent fills the gap with a guess that looks fine in the diff and breaks on the case
nobody wrote down. This doctrine makes Modula author FRDs that carry all three, in the order
downstream agents consume them, sized to the work — never padded, never thin.

It is **one doctrine, two consumers**: the *Author* receives it as a generation overlay, and the
*requirements gate* (the FRD-Reviewer packet + the five-artifact gate) enforces it from
`requirements.yaml` beside this file. They cannot diverge because they ship together.

## Terminology (Modula's fixed distinction)

- **PRD** = the one master document per project (`docs/product-prd.md`). Not governed here (v1).
- **FRD** = every per-feature planning doc, traced to a PRD section. **This skill governs FRDs.**
- Note: the `ralph-tui-prd` skill calls a *feature spec* a "PRD" — in Modula that is an **FRD**. Do
  not mix the two vocabularies.

## How to invoke

- Claude Code: `/frd-author` · Codex: `$frd-author` · Pi/OpenCode: `/skills` picker.

## The skeleton

Write to the canonical section order in `template.md` — **why → what → how → proof → escape**:
Header · SUMMARY · Problem · Goal · Non-goals · Constraints · Functional requirements (FR-N) ·
Acceptance criteria (AC-N) · Design/approach · Verifier checkpoints (CP-N) · Validation plan ·
Rollback · Open questions · Decisions (D-N) · Revision log. Each section has a purpose and a
"done when" test in `template.md`. Which sections are *required* depends on the effort tier (below);
`requirements.yaml` is the machine-readable matrix.

## Authoring rules

- **Goals are concrete, not aspirational.** "A new user reaches the dashboard in ≤3 steps after
  signup," not "make onboarding delightful." Test: could a machine observe it?
- **Constraints and non-goals are explicit.** Name the stack, the boundaries, and what is out of
  scope. An out-of-scope line is a *fence* — without it, a long-running agent adds features nobody
  asked for.
- **Acceptance criteria are verifiable.** Each AC is a condition an agent can confirm by running a
  test, hitting an endpoint, or reading a file. Prefer **Given / When / Then**. "POST /login with a
  wrong password returns 401 and `{error:'Invalid credentials'}`," not "login works." Assert the
  *promise*, cite the FR it satisfies, and when unsure whether something is a promise or an
  incidental artifact, **file it as an open question, not an assertion** (the write-side of
  `acceptance-specs`).
- **Requirements are atomic and MUST-phrased.** One obligation per FR; split any compound " X and Y ".
  Name the actor — no passive voice that hides who must do what.
- **Ambiguity is marked, not guessed.** Underspecified points get an inline
  `[NEEDS CLARIFICATION: …]` marker and route to Open questions; the draft is not handed off with any
  unresolved — clarify before design, the same rule as the armed planning brief.
- **The why lives where the reader looks** — in the FRD/decision line, not lost in chat.

## Right-sizing — less, but load-bearing

Read the planning brief's `effort_classification.level` and include only the sections that tier
requires (`requirements.yaml`). **Both directions are smells:** an empty required section *and* a
padded or restating one. The ≤8-line **SUMMARY** is mandatory at every tier so the long form can be
skipped by agents that only need to re-anchor.

- **XS** (one-file fix): Header, SUMMARY, Problem, Goal, Non-goals, FR-N, AC-N.
- **S**: + Non-goals, Constraints, Verifier checkpoints.
- **M**: + Design/approach, Validation plan, Rollback, Open questions.
- **L** (structural/risky): full skeleton incl. Decisions and correctness properties.

**Escalate-with-reason valve:** the tier sets the *default*; the author may add a normally-omitted
section with a one-line reason (`escalated: touches the auth seam`) — the whole-tier sibling of the
KISS size-limit escape hatch. The valve only adds; it never drops a tier-required section.

### Re-tiering when scope drifts

The tier is a **living classification, not a one-time stamp.** While drafting, watch for **drift
signals** — the draft, relative to its tier, gains a second surface, a persistent-state/schema
change, a new operator decision, a rollback need, or FR-count over the tier's soft cap. On crossing,
do **not** keep drafting at the stale tier and do **not** silently upgrade. Ask one question: **same
feature, just bigger — or now more than one feature?**

- **Same feature, bigger → re-tier proposal** (XS→S→M→L): a one-line operator confirm amends
  `effort_classification`; the newly-required sections unlock.
- **More than one feature → split proposal:** route to `domain_classification.split_recommendation`
  and the new-FRD path — never cram two features into one FRD.

Re-tiering goes **up by default** (a downgrade drops sections — explicit operator action only), and
is always a **proposal through the human gate**, never an autonomous jump.

## Quality-rubric criteria (score pass / warn / fail)

The checklist the FRD is scored against — the concrete form of the Studio "rubric n/10" chips:

1. **Problem clarity** — a stranger understands the pain and why it matters.
2. **Goal observability** — the outcome is observable, not aspirational.
3. **Non-goals present** — the fence is drawn.
4. **FR atomicity** — each FR is one testable obligation, MUST-phrased.
5. **AC verifiability** — every AC is runnable/observable; every FR has ≥1 AC.
6. **Traceability** — every FR traces to a PRD section.
7. **Ambiguity resolved** — no unresolved `[NEEDS CLARIFICATION]` at approval.
8. **Right-sized** — sections match the tier; no empty required, no padding.
9. **Authority floor honored** — grants no autonomous approval/PR/merge/deploy/trading.
10. **Reversibility** — rollback/recovery present wherever the change mutates state.

## Requirements-smell fixes

When the smell detector flags a requirement, apply the fix:

- **Vague term** (fast/easy/simple/seamless/robust/intuitive…) → an observable threshold or a concrete AC.
- **Unresolved TBD/TODO** → a `[NEEDS CLARIFICATION]` open question with an owner, or resolve it.
- **Compound requirement** (" X and Y ") → split into two atomic FRs.
- **Passive voice** → name the actor ("the system MUST…", "the user MUST be able to…").

## Notes

- Feeds Modula's existing gates rather than replacing them: criterion 6 → evidence matrix, 5 →
  `acceptance-specs`, 4/7 → requirements-smells, 9 → the FRD-Reviewer forbidden-scope blocker.
- The machine-readable tier matrix, rubric criteria, and smell→fix map live in `requirements.yaml`
  (a Modula engine extension, not part of the Agent Skills standard) — the enforcement half of the
  one-selection-two-consumers contract.
