# Fast-lane pilot run #1 — pre-flight handoff (Term-2 #364)

Prepared by an Opus 4.8 session on 2026-08-09. **Run #1 must execute on Opus 5** (operator
decision) — this note exists so the Opus 5 session skips the grounding + collision diligence
already done here and starts building CP-1 immediately.

## Status: BLOCKED on executor tier only

Grounding read ✓, collision check ✓, both operator gates resolved. Nothing built, no lane
provisioned, no `/goal` set — deliberately left clean for the Opus 5 session to own.

## Operator decisions (2026-08-09)

1. **Collision → proceed on fresh main.** The four dormant branches below are treated as
   abandoned; build off `origin/main`. Optional cleanup (operator, not required to start):
   prune them so they stop tripping future collision checks.
2. **Model → re-launch on Opus 5.** Do not run on Opus 4.8. Record `Opus 5 / Claude Code`
   in the tracker row.

## Grounding read result

- **FRD #364** (forge issue = canonical source; `status:approved`, CEO-approved 2026-07-29):
  5-checkpoint visual-parity slice for the Terminal view (Workspace page + global shell) vs
  the design prototype. Lands as a **PR stack**, branch per CP.
- **Start condition satisfied**: Term-1 #363 CP-3 landed (CP-6 slices A–E merged).
- **Binding FRD conditions** (do not violate):
  - Gauge/renew surfaces ship the prototype's **empty** states until the Term-1 **FR-29**
    context-percent feed exists. **Never bind to the hardcoded-0 registry value** (P-7,
    `server/comsAdapter.ts:208,255`).
  - **No dead controls** — every rendered control acts or is visibly disabled-with-reason
    per the prototype's own states (AC-3).
  - Named exclusions: **drag-reorder mechanics** (E2/#—), **narrated-terminal look**
    (FRD Term-3 #405). Ship only static drag affordances; preserve current
    drag-onto-job wait-dependency behavior unchanged.
  - Per **ruling 5R.1**: every CP brief is built region-by-region from the prototype source
    (`dev-plans/drafts/modula-stack-design-prototype.html`), never from memory. Embed the
    governing markup+CSS block, map prototype custom props onto live token names (P-1: mostly
    1:1), list that region's out-of-scope elements with owners.
  - Per **5R.3**: each region's AC is a same-viewport screenshot pair (app vs prototype,
    dark+light, desktop + 1100px). Use the API/headless capture harness, not the flaky
    interactive-extension path.

## Design sources of truth (all present, verified paths)

- Prototype: `dev-plans/drafts/modula-stack-design-prototype.html` (proto.modulastack.com)
- `dev-plans/drafts/page-briefs/01-workspace.md`
- `dev-plans/drafts/page-briefs/10-global-shell.md`
- Prototype-reference gate: `prototype-reference-gate-workflow.md` (referenced by FRD P-9)
- Vault working draft: `AI_Global_Tools/shared/modula/frd-term-2-prototype-parity.md`

## Collision check (done — this is the pre-cleared result)

Only **one genuinely-live lane**: `prd/lead-cp3-outbound-391` (PR **#472**, open). It is
**server-side only** (`leadDispatch/leadHistory/leadResidency/leadRuntime.ts` + tests) — it
touches **no** `term-control-center/src` file and specifically **not** `WorkspaceLeadDock.tsx`.
No overlap with any CP. CP-4 must style `WorkspaceLeadDock.tsx` only; **do not touch lead
server runtime** (that's #391's).

Four **dormant** branches own CP files but are abandoned (no open PR, no merge, 16–20 days
stale, superseded by the nav-shell/R1 work already in main) → **cleared to build over**:

| Branch | State | Owns (collides with) |
|---|---|---|
| `prd/nav-shell-275` | on-origin, no PR, 2026-07-23 | CP-1: `App.tsx`, `styles.css`, `navShell.css`, `navDrawer.css`, `registry.ts`, all `navigation/*` |
| `prd/terminal-orchestration-batch-resume-211` | local-only, 2026-07-22 | CP-2: `JobSidebar.tsx` + `.css` |
| `prd/terminal-selection-stability-218` | on-origin, no PR, 2026-07-20 | CP-3: `TerminalPane.tsx`, `styles.css` |
| `prd/term-diff-view-improvements-249` | local-only, 2026-07-22 | CP-4: `DiffInspector` family, `styles.css` |

## Per-CP file ownership map (collision-check pre-done for each)

- **CP-1 Envelope + global shell** (FR-1..4): `src/styles.css`, `src/navShell.css`,
  `src/navDrawer.css`, `navigation/{NavShell,JobSwitcher,AccountMenu,NavDrawer,Statusline}.tsx`,
  `navigation/registry.ts` (drawer labels → prototype taxonomy for **existing** surfaces only,
  no dead links), `src/App.tsx` (remove/relocate the app-only PipelineTimeline+StatusBadge
  header strip, `App.tsx:296`), new topbar renew chip `#renew-chip-m` (hidden until FR-29),
  shared shell propagation `public/agentops-shell*.{js,css}` + `agentops-tokens.css` (P-8).
- **CP-2 Sidebar** (FR-5..8): `src/JobSidebar.tsx` + `.css` — card anatomy (dots, `.job-refs`
  chips, folders, `.dep-stack` rail, resume banner, 304px), `.rail-dots` collapsed rail,
  jobs-mode picker (feeds: groups + `/kody-review/sessions` + CEO-review), context menu
  wrapping existing actions via `WorkspaceJobModals.tsx` shells. Drag exclusion on record.
- **CP-3 Terminal pane + modebar** (FR-9..12): `src/TerminalPane.tsx` (live-dot, role+number,
  model-chip from pane profile, 4-bar gauge+% → FR-29 empty state, status chip, SVG gear),
  `src/WorkspaceModebar.tsx` (per-view tabs, `.mode-add`, `.renew-chip`, `.session-state` =
  pane count + group age), enable desktop per-pane prompt composer (`MobileInputBar`,
  desktop-hidden at `workspacePane.css:218`, restyle to `.input-block`, P-11),
  `WorkspaceConsultPane.tsx` CSS parity + wire behind pair-tab semantics (P-12).
- **CP-4 Diff, FRD tab, dock, modals** (FR-13..16): `DiffInspector` family (adopt full-width
  mode-tab placement, keep richer aids), new read-only FRD tab `.frd-shell` viewer (from task
  body/issue on the group), `WorkspaceLeadDock.tsx` + css (**CSS parity only** to `.lead-panel`;
  behavior #391-owned), `WorkspaceJobModals.tsx` content/copy parity. Amendment system is
  out-of-scope/unowned — name it in FR-18.
- **CP-5 Full-sweep audit** (FR-17,18): region-by-region screenshot pairs; FR-18 parity note
  (drag E2, narrated #405, unbuilt menu destinations, unowned FRD amendment system, lead
  residuals, gauge/renew awaiting FR-29).

Note: `styles.css` is touched by CP-1/CP-3/CP-4 — fine within one sequential stacked lane,
but it makes those CPs order-dependent.

## Lane setup (turnkey — from the run brief)

```
git -C /mnt/hyperliquid-data/projects/repos/agentops-harness fetch origin
git -C /mnt/hyperliquid-data/projects/repos/agentops-harness worktree add \
  -b frd364-cp1 /mnt/hyperliquid-data/projects/worktrees/agentops-frd364 origin/main
# inside the worktree:
git branch --unset-upstream
git push -u origin frd364-cp1
git config git-town-branch.frd364-cp1.parent main
# CP2+: git town append frd364-cp<N>  (stack lives in this one worktree)
```

Stack window: **depth 3** (per `docs/fast-lane-pilot.md`). Build CP-1/2/3, open PRs, drain
reviews before CP-4/5. Stack-stop on any contract/interface review finding. Batch fixes,
`git town sync` once per batch. Merge bottom-up, operator's word only.

## /goal (set at session start)

```
/goal FRD Term-2 #364 complete: AC-1..AC-6 met; region-by-region screenshot pairs
(dark/light × desktop/1100px) saved to run artifacts; /gate --ml green; regression tests
exist for every touched seam and pass; PRs open as a bottom-up stack (window ≤3); advisory
review rounds clean or every finding addressed; tracker row appended to docs/fast-lane-pilot.md
in the top PR. Do NOT merge — stop at review-clean and report.
```

## Tracker row (top PR of the stack, `docs/fast-lane-pilot.md`)

Fill run #1: date · Term-2 #364 · **Opus 5 / Claude Code** · PRs in stack · wall-clock ·
review rounds to clean · % survived unchanged · verdict. A run without a row didn't happen.
