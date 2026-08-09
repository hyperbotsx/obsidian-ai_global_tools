# Prototype prompt — Lead-authored FRD amendments

Copy-paste to the prototype developer. Source: PRD §6 "Lead-authored amendments" (added 2026-07-31),
revision log §17. Companion to the existing operator-comment annotation on the FRD tab.

---

**Task: show Lead-authored FRD amendments in the workspace FRD view.**

Context: an FRD stays live during implementation. Today the prototype shows the *operator* selecting
spec text and adding a comment, which routes to the job's Lead. We now need the reverse direction:
the **Lead itself amends the FRD mid-implementation**, and that change must be visible, attributed,
and surfaced rather than silently altering a document the operator believes is fixed.

Add three things to the workspace FRD tab.

**1. Lead amendment annotation.** Style it to match the existing operator-comment annotation already
in the prototype — same shape, same placement, same visual language — so the two read as one system.
The only differences are the author identity and the accent, so a reader can tell at a glance who
changed what. Each annotation shows:
- author: `Lead` (with the Lead's role colour/avatar treatment, distinct from the operator's)
- timestamp
- the prompting context — the checkpoint or finding that caused it, e.g. *"CP-5 · pre-implementation
  review"*
- the amendment text itself

**2. Changed-during-implementation highlighting.** An amended section is visually marked in the
document body as revised in flight — a margin state and/or section-level tint consistent with the
existing per-section margin states (✓/●/○) used on the Create FRD page. The operator must be able to
scan an approved FRD and immediately see which sections were changed after approval, and by whom.
Include an unamended section adjacent to an amended one so the contrast is legible.

**3. View switch on amendment.** When the Lead amends the FRD while the operator is in the workspace
**split-pane** view, the view switches to the FRD page and scrolls to the amended text. Show this as
an interaction in the prototype: trigger → view change → the amended section in view with its
annotation open. When the operator is on another page, the same event raises a **Needs-you** card
instead (existing notification pattern).

**Realistic content for the mock** — use the real case this came from:

> **Lead** · 2026-07-31 · *CP-5 · pre-implementation review*
> Amended §CP-5 scope: forge selection must be per-project registry config, not a process-level
> environment variable, so users can choose Forgejo or GitHub per project. Also rewording the FR-23
> grep-gate — as written it could be satisfied by deleting GitHub support entirely, which would
> remove the option rather than the hardcoding.

**Notes**
- This is prototype-only; not part of the current FRD (#363) implementation.
- Scope-widening proposals still take the disposition / new-FRD path — this pattern covers in-scope
  corrections to sections not yet built.
- The point of the highlighting is auditability: an orchestrator that edits the plan invisibly is
  indistinguishable from one that drifts from it. The annotation is the evidence that it didn't.
