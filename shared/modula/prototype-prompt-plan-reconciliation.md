# Prompt for the prototype agent — Plan Reconciliation surface

Hand this over as-is. It is self-contained.

---

Add the **Plan Reconciliation** surface to the prototype. It comes from FRD #301 (PL6 provisional, "Plan
Reconciliation"), is owned by the **Planner** page bot, and exists to stop silent plan drift: FRDs get
created inside *and outside* the app, and the master PRD plus the wave plan quietly stop describing the
product. Nothing here is a new agent or a new page — it is new state on surfaces that already exist.

Build four things.

## 1. Drift chip in the board toolbar

Sits beside the existing Replan chip and behaves like it: **amber, mono, compact**.

```
⟲ Plan drift? · 3 FRDs unreconciled
```

Appears only when the count is ≥1. Clicking opens the Planner chat rail with the reconciliation proposal
focused. Show a zero-state variant only in the design file, not in the live layout.

## 2. Needs-you card — "FRDs have landed"

A card in the existing Needs-you band, same construction as the other attention cards (the left-rail accent
exception applies here). Content:

- Title: `3 FRDs landed since your last plan`
- Sub-line listing sources compactly, because "outside the app" is the whole point:
  `2 in GitHub · 1 draft in a PR`
- Primary action `Review drift`, secondary `Dismiss`.

Use dots + text for state on this card, never colour alone.

## 3. Reconciliation proposal in the Planner chat rail

This is the main new artifact. It reuses the **existing plan-proposal message shape** (slot lines, team
chips, gate notes, Approve/Modify affordances) — do not invent a second proposal visual. It has three
stacked sections inside one message:

**a) What landed** — one row per FRD: cut code if assigned, title, source badge (`in-app` / `GitHub` /
`PR draft`), and a provenance link. Include a drift-class tag per row, and make the classes visually
distinguishable because they mean different things:

| Tag | Meaning |
|---|---|
| `missing from plan` | exists, not in any wave |
| `landed, plan stale` | merged, plan still shows pending |
| `superseded` | replaced by a newer FRD |
| `PRD-silent` | adds a capability the PRD does not describe |
| `PRD-contradiction` | **conflicts with the PRD — must read differently from the others** |

`PRD-contradiction` is not a normal row: it is a product decision, not an amendment. Give it a distinct,
heavier treatment and replace its inline action with `Route to review`. It must never look like something
you can casually approve.

**b) Proposed PRD amendment** — a compact per-section diff against the master PRD (sections are numbered
1–17; amendments typically touch two or three). Show section number and heading, the proposed text change,
and the **§17 Revision-log entry** that names the originating FRD. Collapsed by default, expandable per
section. The revision-log line should read as the audit record it is.

**c) Proposed wave delta** — the changes to the flight plan: inserts with target wave and slot, reorders,
done-marks, supersessions. Mirror the existing Plans-tab delta view rather than inventing new language.
Add a plain-language footnote that approval creates a new plan version and **activates nothing**.

Message-level actions: **Approve plan update** · **Modify** · **Dismiss**. Approval is a chat act — no
confirm-phrase gate. After approval, show the receipt inline the way other receipted acts do.

`Dismiss` needs a small reason capture (one line, free text) because a dismissal is recorded and suppresses
that item from being raised again.

## 4. Plans tab — reconciliation history

Add reconciliation entries to the existing Plans sub-tab version list, so a plan version can show *why* it
changed: which FRDs drove it, which PRD sections were amended, who approved, and when. Dismissed items get
a muted row with their reason, so a decision to leave something out stays visible rather than disappearing.

## Rules to respect

- Brand and product name come from config — **never hardcode a product name** in the prototype.
- Visual state = dots + text on dense rows; the left-rail accent is allowed only on Needs-you attention cards.
- Reuse the Replan chip, plan-proposal message, Needs-you card, and Plans delta view. New visual vocabulary
  only for the drift-class tags and the contradiction treatment.
- The Planner proposes; the operator decides. Nothing in this surface may read as automatic.
- Keep the empty/zero states in the design file so we remember them, but do not clutter the live layout.

## What not to build

No new page or nav entry. No wave activation controls (that belongs to the plan engine). No FRD authoring
or approval UI — this surface only reconciles what already exists.
