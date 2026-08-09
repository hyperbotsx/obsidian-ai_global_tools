# Prototype prompt — adopt the site typography (Archivo + Instrument Sans)

Operator decision 2026-08-08: site and app share one type system.
Paste the block below to the prototype agent working on
`dev-plans/drafts/modula-stack-design-prototype.html`.

---

Adopt the decided brand typography in the design prototype
(`dev-plans/drafts/modula-stack-design-prototype.html`): **Archivo** for headings,
**Instrument Sans** for UI/body. The Betatron wordmark and the `--mono` stack stay exactly
as they are.

1. **Embed both fonts as base64 data-URI `@font-face` blocks** (same pattern as the existing
   Betatron block — the prototype must stay a portable single file). Variable woff2 sources,
   latin subset (~65KB total):
   - Archivo (wght 300–900): https://fonts.gstatic.com/s/archivo/v25/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxI.woff2
   - Instrument Sans (wght 400–700): https://fonts.gstatic.com/s/instrumentsans/v4/pxiTypc9vsFDm051Uf6KVwgkfoSxQ0GsQv8ToedPibnr0SZe1Q.woff2
   Declare `font-weight: 300 900` / `400 700`, `font-display: swap`.
2. **Body/UI:** change the `--ui` token to `"Instrument Sans", Inter, system-ui, …` (keep the
   existing fallbacks). Everything that inherits `--ui` follows automatically.
3. **Headings:** add `h1, h2, h3 { font-family: "Archivo", var(--ui); }`. Do NOT apply Archivo
   to chips, labels, buttons, or anything set in `--mono`.
4. **Regression sweep:** Instrument Sans has different metrics than Inter — check the tight
   surfaces in BOTH themes for wrapping/overflow: topbar crumbs + job switcher, drawer items,
   statusline, kanban card titles, settings field rows, modal buttons. Fix with the existing
   truncation patterns (ellipsis), never by shrinking font sizes globally.
5. Acceptance: one pass through workspace, planner, studio, ceoreview, reviews, ledger, admin
   in dark + light; no clipped labels; wordmark unchanged; file still opens standalone
   (file://) with correct fonts and no network requests.
