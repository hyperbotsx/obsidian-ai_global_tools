# FRD: R1 — Workspace Reskin onto Tokens + Shell (W-1)

> Canonical FRD source: the GitHub issue created from this draft (labels `type:prd`, `status:draft`).
> Assigned agent: `agent:agentops`. Code home: `hyperbotsx/agentops-harness`.
> Proposed branch: `prd/workspace-reskin-<issue#>` off `main`; worktree `agentops-prd-<issue#>`.
> Umbrella: #267 Modula Stack Design Rollout — R1 in `dev-plans/drafts/page-briefs/00-index.md` (Phase 1 Reskins; needs F1+F2 only, both merged). Spine note: R1 is the priority reskin — the E0 Lead addition (masterplan delta, "highest-priority addition") needs F4 + **R1's workspace dock**.
> Brief: `dev-plans/drafts/page-briefs/01-workspace.md` (draft v1, decisions §9). Prototype (source of truth for look/feel): `dev-plans/drafts/modula-stack-design-prototype.html` — views `#coder`, `#research`, `#git`, `#diff`, `#diffsplit`, renew modal, New job / Add agent / Remove job modals.
> Dependencies: F1 tokens + F2 nav shell (merged). Does NOT depend on F3/F4/PL*. Unblocks: E0 (Lead panel dock), E2-E5 land on the reskinned surface.
> Research-first surfaces: `term-control-center/src/TerminalPane.tsx` + selection/clipboard/jump modules, workspace page components, `DiffPatchView`, `DiffReviewAids`, `diffState`/`diffReviewState`, sidebar/job-card components, renew chip UI, `src/navigation/registry.ts` + `npm run nav:emit` byte-parity pipeline, F1 token definitions, F2 shell components (consume, don't modify).

- **Status:** draft (CEO review optional gate before implementation)
- **Date:** 2026-07-24

## 1. Problem

The workspace — the room where implementation happens — still renders in the legacy visual system while F1 (tokens) and F2 (nav shell) have been merged for weeks. Every Phase-3 execution-depth FRD (E0 Lead dock, E2 sidebar placement, E3 renewal UX, E4 prompt surface, E5 pane identity) is specced against the reskinned surface, so the longer R1 waits the more E-work builds on the wrong substrate. The E0 Lead — flagged the highest-priority masterplan addition — cannot land without R1's dock.

## 2. Goals (design-only, strangler-fig: presentation replaced, behavior preserved)

1. **Reskin the workspace page onto F1 tokens + F2 shell** per the prototype: pane grid, mode tabs (Coder+Verifier · Researcher+Steward · Git Manager · Diff), sidebar job cards with gauges, renew chip, jobs-mode switch (Active / PR Review / CEO Review), context menu, and the three modals (New job, Add agent, Remove job).
2. **Real interactions carried over intact** (brief §3): drag-reorder with insertion line, folder collapse (Wave B / Done), gauge states, renew-chip lifecycle, resume button, context menu, unified ↔ split diff with review aids (pin hunks, reviewed-file fingerprints, outline jump), pane prompt autosize.
3. **Lead panel dock + ephemeral consult panes** (masterplan delta → R1): the collapsible job-chat side-panel dock and the researcher/steward ephemeral consult-pane surfacing model ship as DESIGN surfaces — E0 wires the live Lead agent later; R1 delivers the dock it mounts into.
4. **BrowserPane tab removed from the workspace** (brief §9.4 decision): the tab goes; the CDP screencast/proxy plumbing stays untouched (it becomes the QA live-view engine, brief 06).
5. Visual rules honored: color via text + dots on dense cards, left rails reserved for board attention cards, brand from config (no hardcoded product names), maximum terminal real estate (operator preference).

## 3. Non-goals (bounded per MW-16 — these are E-lane FRDs)

- Sidebar dependency placement/drag persistence engine (E2/W-2), renewal continuation-pack backend (E3/W-3), uniform prompt surface rework (E4/W-4), per-pane model identity/effort self-adjust/add-agent/jobs-mode feeds (E5/W-5), Teams (E1/W-6), live Lead agent (E0).
- No backend/orchestration changes; no new routes; no changes to F2 shell components themselves (consume only).
- No board/planner/intake surfaces (PL1/PL2 territory — hard boundary).

## 4. Parallel-lane coordination (PL1 #288 and PL2 #293 run concurrently)

- R1 stays strictly on workspace-page surfaces; PL1 owns board/#plan chat surfaces; PL2 CP-1/2 is backend. Expected file overlap ≈ nav `registry.ts` only — entries are APPEND-ONLY, keep `nav:emit` byte-parity green, and rebase-before-propose resolves ordering.
- If the reskin exposes a needed change in a shared F2 shell component, that is a cross-lane lead↔lead negotiation, not a local edit.

## 5. Phasing (checkpoints)

- **CP-1:** tokens + shell adoption for the page frame: mode tabs, pane grid, topbar/job-switcher integration. Zero functional regression (all panes/prompts/switching work identically).
- **CP-2:** sidebar reskin (job cards, gauges, waves/folders, renew chip, context menu, jobs-mode switch) + the three modals.
- **CP-3:** diff views (unified/split + review aids) reskin + Lead dock + ephemeral consult-pane surfacing + BrowserPane tab removal + polish pass against the prototype.

## 6. Acceptance

- Zero functional regression across brief §2 flows 1-3, 5-6, 9-10 (enter job, mode tabs, pane prompt, reorder, sidebar modes, context menu, diff review) — verified by exercising each flow.
- No legacy styles remain on the page (token adoption complete); side-by-side match with prototype views `#coder`/`#research`/`#git`/`#diff`/`#diffsplit` and the modals.
- Lead dock renders (collapsed by default) with a stub content region; consult-pane surfacing pattern demonstrated.
- BrowserPane tab absent; CDP plumbing untouched (grep-verified).
- Nav registry byte-parity + full house gates green (node test/typecheck/build; pytest untouched surfaces).

## 7. Risks / open decisions

- **D-R1-1 — dock scope:** ship dock as pure layout stub (recommended) vs pre-wiring F4 conversation plumbing. Recommend stub — E0 owns the wiring; pre-wiring risks PL-lane collision on conversation stores.
- Brief 01 is **draft v1** (not frozen like brief 02): §9 decisions are settled but §5/§10 boundaries were refined by the masterplan delta — the FRD cut above is authoritative; flag any brief-vs-FRD ambiguity to the lead rather than guessing.
- Reskin-scale diffs are wide but shallow — review discipline is visual verification + regression flows, not line-by-line semantics; verifier bounds accordingly.

## 8. Dogfood setup (this run)

Quartet in a fresh worktree, **isolated coms pool `agentops-trio-r1`** (MW-21/22 preflight: canonical names or stop). Lead model: operator's choice at `/model` — Opus 5 recommended (extends the PL2 trial sample; design-lead work is well inside its envelope). Ponytail: operator may set DYNAMIC per MW-18 — reskin checkpoints are largely mechanical, the profile Ponytail helps with; verifier watches over-minimization (MW-3/MW-13) regardless. Coder emits commit-intents (zero git); git-manager owns VCS + advisory-loop mechanics (MW-23); push/merge human-gated. Harvest frictions to `modula-workflow-requirements.md`.
