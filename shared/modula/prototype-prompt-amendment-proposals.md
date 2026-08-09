# Prompt for the prototype agent — cross-role amendment proposals (prototype + master PRD)

Hand this over as-is. It covers two jobs: a prototype surface, and a master-PRD amendment.
Note for the operator: this deliberately does **not** build a designer↔PRD-author channel. See the
"why not a bilateral channel" note inside — the shape matters more than the feature.

---

We need to close a drift seam: work that happens in one role's surface (design) has product implications
that never reach the canonical spec (the master PRD), and vice versa. Today the only thing carrying them is
a human remembering. Two jobs below.

## Job 1 — prototype surface

**Do not build a new page, and do not build a bilateral designer↔PRD-author channel.** A channel per agent
pair does not scale (designer↔PRD, PRD↔planner, reviewer↔PRD, …). Instead extend the **existing amendment
proposal surface** already specced for Plan Reconciliation (FRD #301) so it accepts proposals from more
sources than FRDs.

Three additions:

**1. Source badges.** The reconciliation proposal's "what landed" rows already carry a source badge
(`in-app` / `GitHub` / `PR draft`). Add **`design`** as a source, so a design-originated amendment appears
in the same queue, in the same shape, under the same approval gate as an FRD-originated one. One inbox, one
proposal shape, one revision log.

**2. Materiality on the row.** A design change only belongs in the PRD when it changes **product
capability, a contract, or a user-visible promise**. Layout, spacing, colour and copy tweaks must never
reach the PRD, or the revision log becomes noise and people stop reading it. So a `design`-sourced row
shows *what kind* of change it is, reusing the existing drift-class vocabulary:

- `PRD-silent` — the design introduces a capability the PRD does not describe → amendment proposed
- `PRD-contradiction` — the design conflicts with something the PRD states → **route to review**, never
  auto-amend (keep the existing heavier treatment for this class)
- `cosmetic` — **new class, and the important one**: no PRD implication. Show it as acknowledged and
  filtered out, so the operator can see the system considered it and correctly declined to escalate.

**3. A "needs a surface" list, kept separate from amendments.** The reverse direction is *not* a PRD edit.
When the PRD describes something with no design behind it, that is a **work request**, not an amendment.
Render it as its own short list — "PRD statements with no surface yet" — with an action to raise a design
task. Do not mix these rows into the amendment queue; they have a different outcome and a different owner.

Everything else stays as specced for #301: proposals never self-approve, approval is a receipted chat act,
dismissal captures a reason and suppresses that item, and every applied amendment writes an attributable
§17 revision-log entry naming its origin.

Rules: brand and product name from config, never hardcoded. Dots plus text for state, never colour alone.
Reuse existing controls; the only new vocabulary is the `cosmetic` class and the "needs a surface" list.

## Job 2 — master PRD amendment

Amend the master PRD (`docs/product-prd.md`) to describe this as a product capability. Keep it short — the
PRD is ~116 lines across 17 sections and should stay that dense.

- **§3 Operating model** (or §4 Agent roles, whichever reads better): add that roles may raise
  **amendment proposals** against the master PRD when their work implies a change to product capability, a
  contract, or a user-visible promise. Proposals are always human-gated, never auto-applied, and carry
  their originating source. The reverse direction — a PRD statement lacking a surface — is raised as a
  design work request, not an amendment.
- **§6 Planning: PRD and FRDs**: add that the PRD has a reconciliation path, so it converges with what is
  actually being built rather than drifting from it, and that amendments are attributable.
- **§17 Revision log**: add an entry for this amendment itself, naming its origin (this proposal). The log
  entry is the audit record — treat it as the point of the feature, not paperwork.

Do **not** widen this into a spec for the mechanism; the FRD owns that. The PRD only needs to state that
the capability exists, that it is human-gated, and that amendments are attributable.

## Why not a bilateral channel (keep this reasoning)

The value is not "designer can message the PRD author." It is that **every role writes into one
amendment pipeline with one gate and one audit trail**. A bilateral channel gives you N² pipes, no shared
ledger, no suppression of declined items, and no single place for the operator to see everything awaiting a
decision. The pipeline already exists for FRDs — design is simply another producer into it.
