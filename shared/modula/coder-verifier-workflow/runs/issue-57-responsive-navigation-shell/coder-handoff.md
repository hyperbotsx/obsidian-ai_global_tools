# Coder handoff — PRD #57 Responsive AgentOps Navigation Shell

## Scope source

- Canonical issue: https://github.com/hyperbotsx/agentops-harness/issues/57
- Title: `B1-PRD: Responsive AgentOps Navigation Shell`
- Branch: `prd/responsive-agentops-navigation-shell-57`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`
- Base: `origin/main`

## Pre-edit status

- `git status --short --branch` before edits: clean on `prd/responsive-agentops-navigation-shell-57...origin/main`.
- Pre-existing dirty files: none.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-57-responsive-navigation-shell/`

## Scope guardrails

### Allowed paths

- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/README.md`
- `pipeline-diagram/board.html`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/wip.html`
- `pipeline-diagram/completion-center.js`
- `pipeline-diagram/review-notify.js`
- `term-control-center/index.html`
- `term-control-center/src/**` for new navigation modules and CSS
- `term-control-center/server/adminAssets.ts`
- `term-control-center/server/adminCss.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/tests/**` for nav/admin/embedded guardrails
- new shared nav data/artifact files needed for #57

### Forbidden paths/actions

- No PR creation, merge, deploy, or approvals.
- No backend mutation-path expansion.
- Do not load the vanilla notification stack into Term or Admin.
- Preserve stable IDs/classes/attributes in PRD §4.1 unless all consumers/tests are updated in-scope.
- Do not change unrelated board cards, pipeline graph behavior, terminal panes, or admin forms beyond nav integration.

## Validation commands

- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center test`
- `npm --prefix term-control-center run build`
- `git diff --check`

## Stop condition

Implement all #57 requirements and acceptance criteria, get verifier approval through the PRD checkpoints plus final bug-check, keep the required validations green, then pause before any PR action.

## Planned verifier checkpoints

1. Information architecture and grouped desktop header.
2. Mobile bottom tabs and More bottom sheet behavior, including bottom-edge de-confliction.
3. Preservation of the full stable contract in PRD §4.1 and existing JS hooks.
4. Cross-surface consistency across Board/WIP/Pipeline/Term/Admin, with Term/Admin Activity as cross-links only.
5. Accessibility, keyboard, safe-area, touch-target, and embedded-mode checks.
6. Guardrail-test rewrite, documentation, and validation evidence.

## Research consult

- Required before implementation because the PRD names research-first surfaces.
- Completed 2026-06-20 via `researcher`.
- Summary recorded before code edits:
  - Use `viewport-fit=cover` and explicit `env(safe-area-inset-top|bottom, 0px)` padding for fixed top/bottom nav surfaces.
  - Treat mobile keyboard movement as a `window.visualViewport` problem when fixed bottom UI is present.
  - Keep touch targets at least `44px` where practical.
  - Prefer a modal-dialog/disclosure pattern for the More sheet rather than ARIA `menu`; preserve Escape close and focus return to the opener.
  - Use one shared bottom-edge offset token so tab bar, sheet, completion center, floating panels, and toasts do not each pin independently to `bottom: 0`.
  - Researcher flagged mobile/touch assistive-technology gaps as a manual-QA priority.
- Sources cited by researcher:
  - MDN `env()` (2026-05-14)
  - MDN viewport meta (2026-04-22)
  - MDN VisualViewport (2026-06-02)
  - Apple UI Design Dos and Don’ts (current)
  - WCAG 2.2 / W3C target-size guidance
  - WAI dialog/disclosure navigation guidance
  - MDN `HTMLDialogElement.showModal()` (2026-01-26)

## Coms preflight

- Project/worktree namespace: `agentops-laneB`
- `coms_list` in this pool shows the required peers: `verifier`, `researcher`, `steward`.
- Coder identity assumption for outbound review requests: `coder@agentops-laneB` in the local worktree pool.
- First-send evidence will be attached in `review-request-r1-information-architecture.json`.

## Checkpoint 1 — information architecture and grouped desktop header

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/agentops-nav.js`
- `pipeline-diagram/global-nav-ui.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/board.html`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/wip.html`
- `pipeline-diagram/public/agentops-nav.js`
- `pipeline-diagram/public/global-nav-ui.js`
- `term-control-center/index.html`
- `term-control-center/public/agentops-nav.js`
- `term-control-center/src/App.tsx`
- `term-control-center/src/main.tsx`
- `term-control-center/src/nav.css`
- `term-control-center/src/navigation/ProjectSwitcher.tsx`
- `term-control-center/src/navigation/TopNav.tsx`
- `term-control-center/src/navigation/navModel.ts`

### What changed

- Added a shared navigation model in `pipeline-diagram/agentops-nav.js` and exposed it to the Term app through a public symlinked asset.
- Replaced the old equal-weight desktop row in `pipeline-diagram/global-nav.js` with a grouped command-header shell driven from the shared model.
- Split the Term React nav into dedicated modules and CSS so `App.tsx` no longer owns nav markup/state.
- Wired Term and vanilla surfaces to load the shared nav model asset before rendering.
- Switched the relevant HTML entrypoints to `viewport-fit=cover` so later mobile/safe-area work can anchor on the correct viewport contract.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/agentops-nav.js` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.

### Revision 2 fix for `V57-KISS-001`

- Split shared vanilla nav helpers/CSS into `pipeline-diagram/global-nav-ui.js` and kept `pipeline-diagram/global-nav.js` as the smaller orchestration layer.
- Added `pipeline-diagram/public/global-nav-ui.js` and loaded it before `global-nav.js` on Board/Pipeline/WIP.
- Removed the superseded Term nav selectors from `term-control-center/src/styles.css` so the new shell styling lives in `term-control-center/src/nav.css`.
- Current line counts after the split:
  - `pipeline-diagram/global-nav.js` — 209 lines
  - `pipeline-diagram/global-nav-ui.js` — 218 lines

### Revision 2 validation

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/agentops-nav.js` — passed.
- `node --check pipeline-diagram/global-nav-ui.js` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `git diff --check` — passed.

### Known limits before later checkpoints

- Stable-hook validation, admin consistency, accessibility hardening, and guardrail-test rewrites remain for later checkpoints.

## Checkpoint 2 — mobile bottom tabs and More bottom sheet behavior

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/global-nav-ui.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/completion-center.js`
- `term-control-center/src/nav.css`
- `term-control-center/src/navigation/TopNav.tsx`

### What changed

- Finished the mobile shell on vanilla and React surfaces: mobile top bar, bottom tab bar, and a More sheet/dialog entry path.
- Added shared bottom-edge offset handling so mobile overlays sit above the bottom tab bar instead of colliding with it.
- Closed the More sheet before opening Reviews / Updates / Live Sessions so those bottom-edge surfaces do not stack over one another.
- Extended `completion-center.js` with exported `close()` / `isOpen()` helpers and focus-return on Escape so the new shell can dismiss the updates panel cleanly.
- Shifted mobile toast/select-bar/list positioning through the nav CSS token instead of independent `bottom: 0` ownership.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/agentops-nav.js` — passed.
- `node --check pipeline-diagram/global-nav-ui.js` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `node --check pipeline-diagram/completion-center.js` — passed.
- `git diff --check` — passed.

## Checkpoint 3 — stable contract and existing JS hooks

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/agentops-nav.js`
- `pipeline-diagram/global-nav-ui.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/completion-center.js`

### What changed

- Reworked the vanilla nav internals so the stable hook elements stay mounted in the DOM even when panels are closed.
- Kept `reviews-btn`, `reviews-list`, `completion-center-btn`, `term-sessions-btn`, `term-sessions-count`, `create-open`, `select-mode`, and `chat-open` continuously addressable for existing board/notifier code.
- Preserved `.reviews-badge`, `.nav-item`, and `data-persistent-nav` wiring while explicitly anchoring mobile/desktop auxiliary panels off the stable trigger elements.
- Left the board/review/completion scripts untouched except for the bounded `completion-center.js` close/isOpen helpers needed by the new shell.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/agentops-nav.js` — passed.
- `node --check pipeline-diagram/global-nav-ui.js` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `node --check pipeline-diagram/completion-center.js` — passed.
- Static contract scan with `rg` confirmed all required stable IDs/classes/attributes remain present across the nav/notifier sources.
- `git diff --check` — passed.

### Revision 5 fix for `V57-HOOK-001`

- Kept the legacy hook IDs mounted in the nav panel, but changed auxiliary surface positioning to fall back to the visible `Activity` / `More` trigger when the inner stable button is hidden inside a closed panel.
- This preserves the existing `reviews-btn` / `completion-center-btn` / `term-sessions-btn` IDs for the old scripts while keeping the opened review/update/live-session UI anchored to a visible control in the new shell.

### Revision 5 validation

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `git diff --check` — passed.

## Checkpoint 4 — cross-surface consistency across Board/WIP/Pipeline/Term/Admin

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `term-control-center/server/adminHtml.ts`
- `term-control-center/src/navigation/TopNav.tsx`
- `term-control-center/src/navigation/navModel.ts`
- `pipeline-diagram/agentops-nav.js`

### What changed

- Kept Term Activity entries as simple cross-links to `/board.html` through the shared nav model and React shell.
- Extended the static Admin nav to match the new shell language more closely with cross-links for Board, WIP, Pipeline, Term, Activity, and an active Admin state, while staying server-rendered/static.
- Preserved the π-only visible brand and the existing back-to-app affordance on Admin.
- Added `viewport-fit=cover` to the Admin HTML shell so the responsive nav treatment uses the same viewport contract as the other surfaces.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `./term-control-center/node_modules/.bin/tsx - <<'NODE' ... adminPage() cross-link assertion ... NODE` — passed.
- `git diff --check` — passed.

### Revision 7 fix for `V57-XSURF-001`

- Updated the Admin `Term` link and `Back to app` affordance from `/` to `/term/` so the static Admin shell points at the shared Term surface used by the nav model and hosted routing.

### Revision 7 validation

- `npm --prefix term-control-center run typecheck` — passed.
- `./term-control-center/node_modules/.bin/tsx - <<'NODE' ... adminPage() /term/ assertion ... NODE` — passed.
- `git diff --check` — passed.

## Checkpoint 5 — accessibility, keyboard, safe-area, touch-target, and embedded mode

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/global-nav-ui.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/completion-center.js`
- `term-control-center/src/navigation/TopNav.tsx`
- `term-control-center/src/styles.css`

### What changed

- Added `aria-current="page"` for active nav links in both the vanilla and React shells.
- Improved focus return for auxiliary panels by routing completion/review/live-session dismissal back to the visible nav anchor instead of a hidden inner trigger.
- Kept Escape handling on the More sheet / desktop panels / completion center aligned with the new focus-return behavior.
- Fixed embedded Term layout so the π-only embedded nav row and the pane switcher no longer compete for the same grid row.
- Continued using 44px targets and safe-area-aware bottom/top spacing from the new shell CSS.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `node --check pipeline-diagram/global-nav-ui.js` — passed.
- `node --check pipeline-diagram/completion-center.js` — passed.
- `git diff --check` — passed.

### Revision 9 fix for `V57-A11Y-001`

- Tightened the vanilla focusable collector so desktop Activity/More focus loops ignore descendants hidden by `[hidden]` / `aria-hidden`, keeping initial focus and Tab wrapping constrained to the visible panel contents.

### Revision 9 validation

- `node --check pipeline-diagram/global-nav-ui.js` — passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.

## Checkpoint 6 — guardrail-test rewrite, documentation, and validation evidence

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/README.md`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `term-control-center/tests/admin.test.ts`

### What changed

- Rewrote the nav guardrails to assert the new shell contract instead of the retired horizontal-scroll / no-hamburger contract.
- Updated the Term base-path/embedded tests for the extracted `TopNav` component, the shared nav model, and the new embedded three-row layout.
- Added the `/term/` Admin link expectations to the admin test.
- Updated `pipeline-diagram/README.md` to describe the shipped grouped desktop header, bottom tab bar, and More sheet behavior.

### Final validation evidence for #57

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (244 tests).
- `npm --prefix term-control-center run build` — passed.
- `git diff --check` — passed.
- Build notes: existing Vite warnings remain for the non-module `term-config.js` / `agentops-nav.js` scripts in `index.html` and a chunk-size warning after client build; build still completed successfully.

### Revision 11 fix for `V57-GUARD-001`

- Extended the rewritten guardrails to assert the Escape/focus-return path and the `reviews-list` anchor relationship through `AgentOpsNavAnchor` / `anchorFor('reviews-btn')`.
- Added explicit assertions for the completion-center visible-anchor return helper and the hidden-descendant focus-loop filter.
- Reran the full validation set after the guardrail expansion.

### Revision 11 validation

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (244 tests).
- `npm --prefix term-control-center run build` — passed.
- `git diff --check` — passed.

## Final gate cleanup after checkpoint 6

### Findings addressed

- `V57-GUARD-001`
- `S57-HYGIENE-001`
- `S57-HYGIENE-002`

### Cleanup performed

- Expanded `boardGuardrails.test.ts` to assert Escape/focus-return wiring and the `reviews-list` anchor relationship through `AgentOpsNavAnchor` / `anchorFor('reviews-btn')`.
- Removed generated `term-control-center/dist/` after the validation rerun.
- Marked the intended new deliverables with `git add -N` so diff-based final review covers the real implementation scope without creating a commit.

### Final rerun after cleanup

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (244 tests).
- `npm --prefix term-control-center run build` — passed.
- Removed `term-control-center/dist/` after the build rerun.
- `git diff --check` — passed.
- `git ls-files --others --exclude-standard` — clean.

## Final verifier result

- Final cleanup confirmation + bug-check revision 12: `approved`
- Bug-check status: `passed`
- Open findings: `0`
- Final report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-57-responsive-navigation-shell/verifier-report.md`
- Status: ready to prepare PR, but paused per instruction before any PR action.
- No PR created. No merge. No deploy.

## Post-approval PR prep

- User later explicitly requested PR creation for #57.
- Before opening the PR, rebased `prd/responsive-agentops-navigation-shell-57` onto current `main` because `main` had advanced with PR #74 (`feat(term): add live branch diff inspector`) and the nav branch touched overlapping Term/board/test files.
- Rebase produced one content conflict in `term-control-center/src/App.tsx`; resolved it by preserving the new responsive `TopNav` shell while keeping the already-merged diff inspector wiring (`DiffInspector`, diff toggle props, and docked layout path).
- Re-ran the full validation suite after the rebase/integration fix.
- `/gate --ml` was not available in this worktree (`/gate: No such file or directory`).

### Post-rebase validation

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (255 tests after integrating current `main`).
- `npm --prefix term-control-center run build` — passed.
- Removed `term-control-center/dist/` after the build rerun.
- `git diff --check` — passed.
