# FRD Term-2 — Terminal view ↔ design prototype: 100% visual parity

Status: draft v1 · 2026-07-29 · owner: Erik + Lead · priority: #1 pair with FRD Term-1 (this is the styling half)
Canonical FRD: **forge issue #364** (https://forge.modulastack.com/ModulaStack/modulastack/issues/364, `type:prd` + `status:approved`, **CEO approved: yes — 2026-07-29**); this vault copy is the working draft.
Companion: FRD Term-1 — forge issue #363 (backend/features/wiring — same audit). Sequencing: Term-1 CP-1..CP-3 first (a board of dead jobs cannot be styled into health); Term-2 may start once Term-1 CP-3 lands and run in parallel after that.
Design sources of truth: `dev-plans/drafts/modula-stack-design-prototype.html` (published at proto.modulastack.com) · `dev-plans/drafts/page-briefs/01-workspace.md` · `10-global-shell.md` · prototype-reference gate (`prototype-reference-gate-workflow.md`).

## 1. Problem

The Terminal is the daily working surface, and it must look and feel like the design source of truth — the operator's explicit order (2026-07-29) is a **100% match of the terminal view** to the prototype. Today the match is partial by design history: F1/F2 shipped tokens + nav shell, R1 (#294) reskinned the workspace *frame* onto them, and five prototype surfaces were formally deferred because their behavior didn't exist (`r1-scope-deferrals.md`). The result is a workspace that is token-correct but structurally short of the prototype: no gauges, no renew chip, no jobs-mode switch, no card chips, no context menu, and residual component-level divergences. This FRD closes the terminal view (Workspace page + global shell) to full parity. It supersedes, for this one view, the "converge only as a byproduct of slices" posture in `page-briefs/00-index.md` §vertical-slices — by operator decision, visual parity of the daily surface is now its own deliverable.

## 2. Grounded facts (verified 2026-07-29)

| # | Fact | Evidence |
|---|---|---|
| P-1 | The token layer is already verbatim-identical to the prototype (palette, radius, fonts, six font sizes), emitted to CSS by script | `term-control-center/src/theme/tokens.ts:1-80` ("extracted verbatim from the design prototype"), `scripts/emit-tokens.ts` → `public/agentops-tokens.css`; prototype `:root` block matches value-for-value |
| P-2 | R1 (#294, merged 8d60fe51c) reskinned the existing workspace surfaces onto tokens/shell: frame, panes, sidebar cards-as-they-exist, Lead dock shell, three modal shells | `src/workspaceFrame.css`, `workspacePane.css`, `JobSidebar.css`, `workspaceLeadDock.css`, `workspaceJobModals.css`; memory: "prototype gap is E2-E5 work, not a defect" |
| P-3 | Five prototype surfaces were formally deferred from R1 because they had no behavior to reskin: jobs-mode switch (E5/W-5), job context menu (E2/W-2), context gauges + renew chip (E3/W-3), PR/FRD card chips (E5/W-5), drag-reorder with insertion line + dependent locking (E2/W-2) | `dev-plans/agentops/coder-verifier-workflow/runs/issue-294-workspace-reskin/r1-scope-deferrals.md` (status-in-app cited per surface) |
| P-4 | The prototype's terminal view consists of: topbar (brand menu-trigger, **topbar job switcher**, renew chip, search, avatar/account menu), workspace sidebar (jobs-mode picker, job cards, folders, new-job, collapse), main header (renew chip), mode tabs, terminal panes with per-pane **context gauge + status chip**, prompt surface, diff views (unified + side-by-side), FRD panel | prototype lines 2076-2129 (shell), 2116-2264 (sidebar), 2264-2517 (main + terminals + gauges, e.g. `#coder-gauge` at 2358-2364), 2517-2677 (diff), per-view anchors `#coder · #research · #git · #diff · #diffsplit` (page brief 01 header) |
| P-5 | Page brief 01 §3 defines what must be *real* vs illustration: real — drag-reorder, folder collapse, gauge states, renew chip lifecycle, jobs-mode switch, resume button, context menu, both diff modes, prompt autosize; illustration-only — scrollback content, coms lines, dep-stack logic | `dev-plans/drafts/page-briefs/01-workspace.md:24-28` |
| P-6 | Current component inventory: `App.tsx` (1098), `TerminalPane.tsx`, `JobSidebar.tsx`, `WorkspaceModebar.tsx`, `WorkspaceLeadDock.tsx`, `DiffInspector` family, `navigation/` (NavShell, NavDrawer, JobSwitcher, AccountMenu, Statusline) — every prototype region has a home component; none is missing wholesale | `term-control-center/src/*.tsx` listing |
| P-7 | Real data for the deferred visuals mostly exists — heartbeat classifier computes per-role status/quiet-time, `/kody-review/sessions` is fetched but unused by any sidebar mode, card-chip metadata (issue URL, review state) is present but unrendered — **except context percent**: `context_used_pct` is hardcoded 0/null server-side (`server/comsAdapter.ts:208,255`); the real number lives only inside the pi runtime. Term-1 FR-29 builds the feed; the gauge binds to it | coms audit; `server/heartbeatSweep.ts`; deferral record rows 1 and 4 |
| P-10 | The most visible whole-page divergence is the **layout envelope**: the app floats bordered/rounded cards on a padded, grid-textured background (`src/styles.css:26,73`, `src/navShell.css:1`); the prototype is full-bleed edge-to-edge (`.app` rows `58px 1fr 30px`, no padding — prototype line 105) | proto-gap audit |
| P-11 | The prototype's always-visible per-pane **prompt composer** (`.input-block`, prototype 485) exists in the app only as `MobileInputBar`, hidden on desktop (`display:none`, `src/workspacePane.css:218`) — the input wiring already works; desktop input currently goes straight into xterm | proto-gap audit |
| P-12 | The consult pane (`.consult`, prototype 1834) is **built but unwired**: `WorkspaceConsultPane.tsx` reproduces it with placeholder content, but `App.tsx` never sets `showConsultPane` | proto-gap audit |
| P-13 | Missing surfaces in the terminal view: topbar **`.global-search`** (prototype 2095; the app's NavShell center column is empty — `NavShell.tsx:10`), modebar **`.renew-chip` + `.session-state`** ("4 agents · 11m active") + **`.mode-add`** (prototype 2266+), pane-head **`.model-chip` / 4-bar `.gauge` / breathing `.live-dot` / SVG gear** (prototype 435, 2281 — grep-confirmed absent), the in-context **FRD tab** (`.frd-shell`, prototype 2619 — zero matches in src), and the sidebar `.rail-dots` collapsed rail + `.dep-stack` dependency rail (prototype 2132, 298) | proto-gap audit |
| P-14 | Two placement/IA divergences: the app's diff is a **sidecar** in the cockpit grid (`src/styles.css:302`) vs the prototype's full-width mode-tab view (2507/2559); the nav drawer taxonomy (board/matrix/timeline/term/wip/… — `src/navigation/registry.ts:61`) differs from the prototype menu (FRD Studio / Planner / Workspace / IDE / PR Reviews / Ledger / Activity — prototype 4922). The app also injects a header pipeline strip (`PipelineTimeline` + `StatusBadge`, `App.tsx:296`) the prototype does not have | proto-gap audit |
| P-15 | The Lead dock (`WorkspaceLeadDock.tsx`) is **app-only** — the prototype's terminal view has no dock equivalent (it models Lead interaction via FRD amendments). E0/#355 functionality: reconcile styling, do not remove | proto-gap audit |
| P-8 | The shell is shared across both frontends (Vite app + `pipeline-diagram/` static pages) via `public/agentops-shell*.{js,css}` + `agentops-tokens.css` — shell parity propagates to all pages without touching R2 scope | `term-control-center/public/`, `pipeline-diagram/agentops-shell*.css` |
| P-9 | The prototype-reference gate requires each implementation brief to carry the prototype's actual markup/CSS and to name exclusions explicitly | `prototype-reference-gate-workflow.md` rules 1-3 |

## 3. Goals

1. **The workspace page and global shell are visually indistinguishable from the prototype** — structure, spacing, typography, states, both themes — for everything the app can truthfully render.
2. **The five deferred surfaces appear** — visually complete per prototype, bound to the real signals that already exist (P-7), with the prototype's own zero states where an engine is missing. No dead controls: every rendered control either acts or is visibly disabled-with-reason per the prototype's states.
3. **One shell** — parity lands in the shared shell assets so the terminal view and the static pages carry the same chrome.

## 4. Non-goals

- Other pages' content: board/planner (R2 — gated on PL2/PL3), validation, reviews, activity, settings, IDE, FRD Studio, prototype-viewer and PRD-doc views inside the prototype file.
- **Drag-reorder mechanics** (insertion line, order model, dependent locking) — E2/W-2 owns the behavior; this FRD ships only the prototype's static affordances (cursor/handles) and names the exclusion on-screen-honestly (current drag-onto-job wait-dependency behavior is preserved unchanged).
- Renewal *flow* (threshold → modal → pack/re-anchor → queued renewal): the engine is Term-1 CP-7 + W-3/E3; this FRD ships the chip/gauge visuals and threshold states bound to live percent, and the chip opens the modal shell with the prototype copy once Term-1's renewal endpoint exists (else hidden — never a dead button).
- Teams modal content (E1), effort self-adjust (E5), CP-0 conditions intake (E5), the consult pane's ephemeral-summon behavior (E-lane; §6 wires it behind existing semantics only).
- **The narrated-terminal look** (prototype scrollback is a narrated activity mock, prototype 465; the app renders real xterm PTY output — ANSI ramp already themed via `tokens.ts:114`). Making real output read as the prototype's narrated log is a large functional build, not styling.
- Prototype menu destinations that do not exist yet (FRD Studio, IDE, Activity as designed) — the drawer adopts prototype labels/order for existing surfaces only; no dead links.
- No backend features beyond thin read-only bindings of already-present signals (P-7); anything needing new state/engines stays with its owning FRD — the one cross-FRD data dependency is the context-percent feed (Term-1 FR-29).

## 5. Design rulings

### 5R.1 — Parity is briefed region-by-region from the prototype source, never from memory.
Per the prototype gate (P-9): each checkpoint's coder brief embeds the governing prototype markup + CSS block (grep the `data-*` hooks / class names, read the rule block), maps prototype custom properties onto the live token names (check, don't copy — P-1 makes most 1:1), and lists that region's out-of-scope elements with owners. The parity audit at the end walks the same region list.

### 5R.2 — Deferred surfaces: visually complete, minimally bound, honestly empty.
Resolution of the R1 deferral (P-3) against the operator's 100% order:
- **Context gauges + status chips** — render per prototype (`.gauge-wrap`/`.gauge`/`#coder-gauge-pct`, states ok/near/over) bound read-only to the Term-1 FR-29 context-percent feed + heartbeat status (P-7: today's registry value is hardcoded 0 — never bind to that). No feed yet / non-registered agent ⇒ prototype's empty gauge state.
- **Renew chip** (topbar + main variants) — appears at threshold from the same feed; action wired to Term-1's renewal trigger when present.
- **Jobs-mode switch** (Active / PR Review / CEO Review) — full picker per prototype; list filtering wired to existing feeds (groups + `/kody-review/sessions` + CEO-review groups). This intentionally pulls the *visual + filter* slice of W-5 forward; deeper feed semantics stay E5.
- **PR / FRD card chips** — pure rendering of present metadata (issue number, PR/review state) per prototype card spec.
- **Job context menu** — prototype menu structure wrapping the existing always-visible row actions (pin, wait-on, clear-wait, remove-with-what-is-kept statement via the R1 modal shells); no new mutations.
- **Drag insertion-line** — excluded (§4), listed in the on-record parity note.

### 5R.3 — Parity is verified by side-by-side capture, not eyeballs-from-memory.
Each region's AC is a same-viewport screenshot pair (app vs prototype, dark + light, desktop + the prototype's 1100px/mobile breakpoints) reviewed in the run artifacts. The capture path uses the API/headless harness from Term-1 (AC-11) plus the existing browser plumbing — the flaky interactive-extension path from the dogfood is not the verification vehicle.

## 6. Region inventory → work map

| Region (prototype anchor) | Current home | Status today | Work class |
|---|---|---|---|
| **Layout envelope**: full-bleed `.app` grid, plain body (105) | `styles.css:26,73`, `navShell.css:1` | divergent — padded floating cards on textured bg (P-10) | structural CSS (highest visual impact) |
| Topbar: brand menu-trigger, caret, hover states (2076) | `NavShell`/`agentops-shell` | exists, verify-detail | CSS polish |
| Topbar job switcher `#job-switcher` + grouped job menu (2079-2096) | `navigation/JobSwitcher.tsx` | exists, structure differs | structural CSS |
| Topbar center `.global-search` (2095) | `NavShell.tsx:10` center column | absent — column empty (P-13) | new visual, bound to job/nav filtering |
| Topbar renew chip `#renew-chip-m` (2097) | — | absent (P-3) | new visual + Term-1 FR-29 feed |
| Header pipeline strip (`PipelineTimeline`/`StatusBadge`) | `App.tsx:296` | app-only, not in prototype (P-14) | remove/relocate per prototype |
| Search `#top-search`, avatar + user menu w/ `um-head` identity (2098-2108) | `AccountMenu.tsx` | exists — identity block/items differ | CSS + copy |
| Sidebar: jobs-mode picker `#jobs-mode` (2119-2127) | static "Active jobs" header | absent (P-3) | new visual + filter (existing feeds) |
| Sidebar: job cards, dots, `.job-refs` chips, folders, `.dep-stack` rail, `.rail-dots` collapsed rail, 304px width (2128-2264, 276-298) | `JobSidebar.tsx` + css | partial (R1) — chips/dep-rail/rail-dots absent, width 13-17rem | structural CSS + chip rendering |
| Modebar: per-view tabs + `.mode-add` + `.renew-chip` + `.session-state` (2266+) | `WorkspaceModebar.tsx:33` | partial — pair-tabs exist; add/renew/session-state absent (P-13) | structural + binding (session-state = pane count + group `createdAt`; mode-add → existing browser-qa pane action) |
| Terminal pane head: `.live-dot`, role, `.model-chip`, 4-bar `.gauge`+%, status, gear (435, 2281-2364) | `TerminalPane.tsx:150` | partial (R1) — model-chip/gauge/live-dot/gear absent (P-13) | structural + binding (model id exists on pane; gauge = Term-1 FR-29) |
| Per-pane prompt composer `.input-block` (485) | `MobileInputBar`, desktop-hidden (P-11) | built, hidden — wiring works | enable + restyle per prototype |
| Consult pane `.consult` (1834) | `WorkspaceConsultPane.tsx` | built, unwired (P-12) | CSS parity + wire behind existing pair-tab semantics; prototype's ephemeral-summon model stays E-lane |
| Diff unified + split as full-width mode-tab views (2507-2677) | `DiffInspector` family (sidecar, `styles.css:302`) | exists, richer than prototype; placement differs (P-14) | adopt prototype placement, keep extra features |
| FRD tab `.frd-shell` in-context spec (2619-2677) | — | absent (P-13) | read-only FRD viewer from existing task body/issue; select-to-amend → Lead dock = stretch (endpoint exists: `/lead/message`) |
| Lead dock (E0) | `WorkspaceLeadDock.tsx` + css | live, app-only (P-15) | CSS polish; recorded as deliberate divergence |
| Job modals (new/add/remove) shells | `WorkspaceJobModals.tsx` | shells shipped (R1) | content/copy parity |
| Context menu on job rows | always-visible controls | absent (P-3) | structural + rewire existing actions |
| Statusline (509), nav drawer, deep links | `navigation/*`, `navDrawer.css:180` | exists — drawer taxonomy differs (P-14) | CSS polish; relabel/reorder to prototype for surfaces that exist |

## 7. Functional requirements & checkpoints

Vertical-slice per region; every CP brief embeds its prototype spec (5R.1) and lands its screenshot pairs (5R.3).

**CP-1 — Envelope + global shell parity.** FR-1 the layout envelope goes full-bleed per prototype (P-10) — remove card floats, page padding, textured body; FR-2 topbar to prototype structure/states: brand trigger, job switcher + grouped menu, **global-search in the center column** bound to job/nav filtering, avatar menu with identity block; the app-only header pipeline strip is removed or relocated per prototype (P-14); FR-3 topbar renew chip (visual, fed by Term-1 FR-29 when present, hidden until then); FR-4 drawer + statusline + shared-shell propagation (P-8); drawer relabeled/ordered to the prototype taxonomy **for surfaces that exist** — no dead links to unbuilt pages. 
**CP-2 — Sidebar parity.** FR-5 card anatomy (dots, `.job-refs` chips, folders, `.dep-stack` rail, resume banner, 304px width) per prototype; FR-6 `.rail-dots` collapsed rail; FR-7 jobs-mode picker with real filtered feeds (groups + `/kody-review/sessions` + CEO-review); FR-8 context menu wrapping existing actions (incl. remove-with-what-is-kept via R1 modal shells); drag-mechanics exclusion noted on record. 
**CP-3 — Terminal pane + modebar parity.** FR-9 pane head anatomy: breathing live-dot, role + number, model-chip (pane profile data exists), 4-bar gauge + percent (Term-1 FR-29 feed; prototype empty state until data), status chip, SVG gear; FR-10 the per-pane **prompt composer**: enable the existing hidden input bar on desktop and restyle to `.input-block` (P-11 — wiring already works); FR-11 modebar to prototype: per-view tabs, `.mode-add` (bound to the existing add-browser-qa-pane action where applicable), `.renew-chip`, `.session-state` (pane count + group age from existing state); FR-12 consult pane CSS parity, wired behind existing pair-tab semantics (P-12). 
**CP-4 — Diff, FRD tab, dock, modals.** FR-13 diff adopts the prototype's full-width mode-tab placement (keeping the app's richer review aids); FR-14 the FRD tab ships as a read-only in-context viewer of the canonical FRD (issue body/task data already on the group); select-to-amend → Lead dock is a stretch item (endpoint exists); FR-15 Lead dock visual parity, recorded as deliberate app-over-prototype divergence (P-15); FR-16 modal content/copy parity. 
**CP-5 — Full-sweep parity audit.** FR-17 region-by-region walk of §6 with screenshot pairs (dark/light × breakpoints), fixing residuals; FR-18 closing **parity note** (house convention; the R1 deferral record is the template) naming: drag mechanics (E2), narrated-terminal look (excluded), prototype menu destinations not yet built, Lead dock divergence, and any gauge/renew surfaces still awaiting the Term-1 feed.

## 8. Acceptance criteria

- **AC-1** Side-by-side captures for every §6 region are indistinguishable in structure, spacing, type, color and states (dark + light, desktop + 1100px), with differences only where §4 names an exclusion.
- **AC-2** The five deferred surfaces render per prototype: live gauges/status on real panes, renew chip at threshold, jobs-mode switch filtering three real lists, metadata chips on cards, context menu carrying the existing actions.
- **AC-3** No dead controls: every interactive element acts, or is disabled with the prototype's disabled treatment; engine-less states show the prototype's zero states verbatim.
- **AC-4** Both themes pass the existing contrast gate (`scripts/check-contrast.ts`); no horizontal scroll at any prototype breakpoint.
- **AC-5** The static pages pick up the same shell chrome without R2 content changes (P-8).
- **AC-6** Parity note filed with the run, naming the E2-owned drag mechanics (and anything else) as the only open items.

## 9. Verification tier

Lead + Coder + Verifier (+ Git Manager). Verifier reviews each CP against the embedded prototype spec and the screenshot pairs; browser-qa pane optional per CP (policy `auto`). The FRD's own launches run through the in-app path once Term-1 CP-2 lands — this FRD is itself dogfood for Term-1.
