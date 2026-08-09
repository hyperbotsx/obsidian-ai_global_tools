# Prototype prompt — reviewer options rename (no-custody alignment)

Operator decision 2026-08-08 (PRD §10 amended same day): reviews run on the runner; a
"Modula hosted reviewer" that reads customer code server-side contradicts the no-custody
doctrine. Paste the block below to the prototype agent.

---

Small copy/consistency fix in `dev-plans/drafts/modula-stack-design-prototype.html`,
Admin → Git → reviewer settings. Source of truth: `docs/product-prd.md` §10 (amended
2026-08-08).

1. The **Reviewer** select currently offers `Modula hosted reviewer / Greptile /
   Self-hosted reviewer / None`. Change the options to:
   `Built-in Reviewer · runs on your runner` (default) / `Greptile` /
   `Self-hosted Kodus` / `None`.
2. Update the field's `.desc`: "Reviews always run on your runner — the code under review
   never leaves your machine. Built-in needs no extra infrastructure; Greptile uses your
   own account; self-hosted Kodus points at a stack beside your forge."
3. The **Reviewer endpoint** field's desc mentions "the Modula hosted reviewer" — reword to
   apply to Greptile / self-hosted Kodus only; the built-in Reviewer needs no endpoint
   (hide or disable the field when Built-in is selected, matching existing show/hide
   patterns in the Git panel).
4. Scope: this panel only; both themes; no other pages.
