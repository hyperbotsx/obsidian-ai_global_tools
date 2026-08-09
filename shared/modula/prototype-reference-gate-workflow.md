# Prototype reference — mandatory gate for FRDs and implementation briefs

Status: active from 2026-07-26 · owner: Lead · applies to every Modula Stack FRD, plan and implementation brief
Companion to `context-brief-phase0-workflow.md`. Both are pre-implementation gates; this one covers design truth, that one covers codebase truth.

## The rule

1. **Every FRD must reference the prototype when written.** Cite the specific prototype region and the page brief section that governs the surface.
2. **Every implementation brief for UI work must carry the prototype's actual spec** — markup structure, class names, CSS values, zero states, interaction rules — not an inference from neighbouring code.
3. **Name what is out of scope.** The prototype shows the end state and will be ahead of any single FRD. Explicitly list which prototype elements this checkpoint does *not* build, and why.

## Sources of truth

- `dev-plans/drafts/modula-stack-design-prototype.html` — named "design source of truth" in `dev-plans/drafts/page-briefs/00-index.md`.
- `dev-plans/drafts/page-briefs/01-workspace.md` … `10-global-shell.md` — each page brief's §3 "Design spec" opens with "Per prototype" and adds the deltas to build next pass.

## Why — the evidence

On PL2 #293 CP-3 the Lead briefed the Plans UI from the FRD's *summary* of the brief plus the existing board CSS, without opening either source. The brief said "follow the `#plan` bottom-sheet drawer pattern".

The prototype actually specifies:
- a board panel — `<div class="board-shell" data-board-panel="plans">` → `<section class="band">` → `.plans-list` grid of `.plan-ver` cards with `.pv-top` / `.pv-sub` / `.pv-tag`
- content shaped as **"version history — a plan version shows WHY it changed"**, not a plain expandable diff
- a specified zero state: *"v1 · initial plan — no reconciliations yet"*
- elements belonging to later work: reconciliation tags, `.plan-ver.dismissed` entries, the ⟳ Replan and ⟲ Plan drift chips

Two of those the Lead had wrong (drawer vs panel, diff vs why-history), one it had never heard of (dismissals), and one it correctly excluded only because FRD §3 happened to list it as a non-goal. The correction was cheap **only because the operator asked "are we referring to the prototype?" mid-task**. Nothing in the workflow would have caught it.

## How to apply

Before briefing any UI work:
1. Read the page brief §3 for that surface.
2. Read the prototype markup **and** CSS for it — grep the `data-*-panel` / class names, then read the rule block.
3. Put the real class/structure spec in the brief. Tell the coder to map prototype custom properties onto whatever the live page actually defines, since names may differ — check, do not copy blindly.
4. State the out-of-scope list with the reason (usually: a later FRD owns it, per the current FRD's non-goals).

**Integration with the Context Brief:** the brief's *affected surfaces* section must cite the prototype region for any UI surface in scope. That makes design truth part of the same pre-implementation artifact as codebase truth, rather than a separate thing the Lead may forget.

## Product requirement — this belongs inside Modula, not just in our process

Modula will render the prototype **as an in-app feature**, and it is already designed: the prototype's own `.proto-shell` block is captioned *"Prototype page: the living design prototype rendered in-app, Designer bot beside it"* — a two-column grid with a 400px Designer bot rail.

So the product must:
- **Link the prototype from FRDs and plans**, at authoring time and at execution time. An FRD's UI scope should resolve to a prototype region the way it already resolves to a repository path.
- Make the link **navigable in both directions** — from an FRD/plan to the governing prototype region, and from a prototype region to the FRDs that implement it.
- Treat the prototype as **versioned design truth**, so an FRD cites the region *as of* a prototype version and drift becomes visible rather than silent.

Harvest note: this is the same class of gap as the Context Brief — a gate the app enforces (or should) that our hand-run trio bypasses. Both should migrate from Lead-owned manual gates to launcher-enforced ones.
