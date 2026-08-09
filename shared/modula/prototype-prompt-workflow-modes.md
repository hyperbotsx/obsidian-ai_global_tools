# Prototype prompt — Workflow modes (FRD Modes-1)

Source FRD: `AI_Global_Tools/shared/modula/frd-workflow-modes-draft.md` · 2026-08-08
Paste the block below to the prototype agent working on
`dev-plans/drafts/modula-stack-design-prototype.html`.

---

Implement **workflow mode selection** in the design prototype
(`dev-plans/drafts/modula-stack-design-prototype.html`, single file, hash routing). Source of
truth: `AI_Global_Tools/shared/modula/frd-workflow-modes-draft.md` (FRD Modes-1). Use only the
existing design system — tokens, `.field`/`.seg` controls, `.desc` helper text, mono chips,
modal patterns — no new colors or components, and verify both dark and light themes.

Four surfaces, in priority order:

1. **New-job modal — Mode selector (FR-1, FR-6).** Add a "Mode" field directly below the Team
   picker: a segmented control with `Fast · Lean · Strict · Flagship`, **Lean preselected**.
   Below it, a one-line `.desc` that swaps with the selection:
   - Fast — "One agent, deterministic gate only. For exploration and throwaway work."
   - Lean — "One strong agent; review-after with receipts. Recommended for most feature work."
   - Strict — "Coder + verifier checkpoint loops. For engine, protocol, and risky seams."
   - Flagship — "Full team plus fusion arbitration and every quality gate."
   Mode never alters the Team field's contents — the team supplies the lineup, the mode decides
   what activates (say this in the desc only if space allows).

2. **Mode chip on jobs (FR-4).** Active-job list items in the workspace sidebar and the kanban
   job cards get a small mono chip with the mode name (style like existing tag chips, muted;
   no color coding beyond the existing chip treatment). Seed the demo data so the visible jobs
   mix modes (mostly lean, one strict).

3. **Escalation affordance (FR-5).** In the job right-click context menu, add "Escalate mode…"
   opening a small confirm modal that offers **only higher** modes than the job's current one
   (ratchet — no de-escalation), with one confirm button and the standard modal chrome. On the
   demo level it just closes; no state machinery needed.

4. **Admin → Agents & Models (FR-1 default).** Reframe the existing quality-presets block as
   "Workflow modes": a per-project **Default mode** select (Lean preselected) above the existing
   add-on toggles; keep the toggles, they become the Flagship/add-on detail.

Keep scope to these four surfaces. Do not touch the statusline, drawer registry beyond what the
modal needs, or any other page. Acceptance: the modal renders the selector with live desc swap;
chips visible on at least three jobs; context menu shows the escalate entry with its modal;
admin shows the default-mode select — all in both themes.
