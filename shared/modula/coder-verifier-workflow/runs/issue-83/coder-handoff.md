# Coder handoff — issue #83

PRD: GitHub issue #83 "B1-PRD: Unified design system + chrome consolidation"
PRD doc: `dev-plans/agentops/unified-design-system-consolidation.md`
Worktree: `agentops-laneB`  ·  coms pool: `agentops-laneB`
Branch: `prd/unified-design-system-chrome-consolidation-83`
Coder: Claude Code (interactive session). No Pi `coms_*` tools; communicates via durable artifacts and reads `verifier-report.md` directly.
Date: 2026-06-21

## Source of truth

Issue #83 / the PRD doc above. Predecessors #35 (visual system), #57 (nav shell), #60 (admin polish) — done but drifted; this PRD supersedes their drifted parts.

## Decisions

- Palette: unify on Term's blue (locked).
- Font: keep Berkeley Mono; trial license accepted for now. Only Regular weight ships — do not use faux-bold; build hierarchy from size/color/uppercase.
- Board-layout redesign: out of scope (separate follow-up PRD).

## Allowed paths

- `term-control-center/src/**` (styles, nav, App shell, terminal chrome)
- `term-control-center/server/adminCss.ts`, `term-control-center/server/adminHtml.ts` (admin tokens + nav)
- `pipeline-diagram/**` (`agentops-theme.css`, `global-nav.js`, `global-nav-ui.js`, `agentops-nav.js`, `board.html`, `wip.html`, `pipeline.html`)
- `docs/agentops-visual-system.md` (spec correction)
- a new shared tokens stylesheet (location decided in CP1)

## Forbidden paths / out of scope

Terminal/PTY behavior, auth, backend/launch APIs (`launchGroup.ts`, `launchPlan.ts`, `launchProfiles.ts`), board kanban redesign / alternative board view (separate follow-up PRD), any product code outside design/nav/content scope.

## Validation

- `/gate --ml` quality gate (TypeScript, Vite build, ESLint, import check) per repo CLAUDE.md.
- `term-control-center` Vite build succeeds.
- Visual diff: screenshots of all six surfaces before/after (palette + nav consistency).
- Token audit: no duplicate `:root --ao-*` blocks; no stray hex / ad hoc `font-size` / off-grid spacing on changed surfaces.
- Accessibility: visible keyboard focus, `prefers-reduced-motion`, mobile widths, safe-area insets preserved.

## Stop condition

Stop after final verifier bug-check approval, or on human escalation / `needs_human`.

## Verifier checkpoints

1. **Foundation — shared token source.** One canonical `agentops-tokens.css`: blue color tokens (from `term-control-center/src/styles.css`), plus a fixed type scale (`--fs-display/heading/body/label/meta`) and a 4px spacing scale. Consumed by term-control-center, pipeline-diagram, and admin CSS; duplicated `:root` blocks removed. (US-1; defines US-9/US-10 tokens)
2. **Palette + scale adoption.** Board/WIP/Pipeline/Admin render the blue palette (admin buttons blue, not gold); ad hoc sizes/spacing on changed surfaces replaced with tokens; hierarchy via size/color/case, not weight; board status-color legibility checked. (US-2, US-9, US-10)
3. **Single nav renderer + redesign.** Admin renders from `AgentOpsNavModel` (drop hardcoded nav); one slim consistent bar with a single subtle active state; consistent item set/order and one home for "Pipeline". (US-4, US-5)
4. **Term maximize mode.** First-class persisted "maximize terminals" toggle promoting the `?embed=1` reductions; hero collapsed by default; the stacked bars merged toward two. (US-6)
5. **Content density + microcopy.** Trim per-page heroes; legends → tooltips/on-focus; hide machine internals (PID/path) behind hover; lead with human names + status dots; directive empty states; copy hygiene. (US-8)
6. **Spec + quality floor.** Update `docs/agentops-visual-system.md` to the shipping blue palette + Berkeley Mono; verify the accessibility floor. (US-3, US-7)

## Comms

- Peers live in pool `agentops-laneB`: `verifier`, `researcher`, `steward` (Pi, gpt-5.4). Confirm before each review request: `ls /tmp/agentops/coms/agentops-laneB/projects/agentops-laneB/agents/`.
- Coder requests review by writing `coder-ready.md` here (checkpoint #, revision, requested action, PRD/issue refs, handoff path, changed files, validation results, finding IDs addressed) and notifying the verifier.
- Verifier writes `verifier-report.md` here ending with the machine-status block (Decision / Checkpoint reviewed / Revision reviewed / Open findings / Bug-check status / Next actor). Coder reads it for the verdict.
- One review request in flight at a time; no ping-pong. Steward hygiene review runs before the final verifier bug-check.

## CP1 — shared token source (implemented)

Token-file location decision: one canonical editable file, symlinked into each served web root — the surfaces are served by two independent servers (term + admin = one Express app; pipeline-diagram = a separate `python -m http.server` / nginx root at `pipeline-diagram/public`). This mirrors the repo's existing shared-asset convention for `agentops-nav.js` (canonical in `pipeline-diagram/`, symlinked into `term-control-center/public/`).

- Canonical (single editable source): `pipeline-diagram/agentops-tokens.css` (same home as the canonical nav model).
- `term-control-center/public/agentops-tokens.css` → symlink to `../../pipeline-diagram/agentops-tokens.css` (Express serves it at `/agentops-tokens.css` for term + admin; Vite emits `dist/agentops-tokens.css` from it).
- `pipeline-diagram/public/agentops-tokens.css` → symlink to the canonical (nginx web root).
- Contents: the blue `--ao-*` palette (verbatim from term `styles.css`), `--fs-display/heading/body/label/meta`, and the `--space-4/8/12/16/24/32` 4px scale.

Consumers wired; duplicated `:root --ao-*` blocks removed from `term-control-center/src/styles.css`, `term-control-center/server/adminCss.ts`, and `pipeline-diagram/agentops-theme.css`. Term `styles.css` keeps only its app-specific `--focus-border`/`--separator-border` aliases.

Expected side effect: admin + pipeline now consume the blue source, so those surfaces render blue at CP1 (the intended root-cause de-drift). Remaining hardcoded non-token values (inline `cssText` hex in `board.html`, ad hoc sizes/spacing) are CP2.

Scope note: three guardrail tests (`boardGuardrails.test.ts`, `admin.test.ts`, `termBasePath.test.ts`) asserted the old divergent token values in the exact files being consolidated; updated to assert the single blue source. The token guardrail now asserts the term asset is a symlink (`isSymbolicLink`), enforcing one editable source. `@font-face` left per-app (relative `src` differs); admin's missing `@font-face` and the stale `docs/agentops-visual-system.md` palette are CP6.

### Revision 2 — CP1-F001 resolved
Verifier (rev 1) requested a true single editable source instead of a manual mirrored pair. Replaced the `term-control-center/public/agentops-tokens.css` file copy with a symlink to the canonical (matching `agentops-nav.js`), dropped the "edit both" header, and changed the guardrail to assert the symlink. Rebuilt + retested.

Validation: `term-control-center` typecheck ✓, Vite client+server build ✓ (`dist/agentops-tokens.css` emitted from the symlink and linked), full test suite 332/332 ✓. No `/gate` script exists in this worktree; ran its constituent checks (no eslint config present).

## CP2 — palette + scale adoption (implemented)

Scope: Board/WIP/Pipeline (`board.html`, `wip.html`, `pipeline.html`, `global-nav-ui.js`, `activity-center.js`, `completion-center.js`, `review-notify.js`) and Admin (`adminCss.ts`). Term stays canonical.

- Color: every hardcoded color (hex + colored `rgba`) replaced with `--ao-*` tokens. The pipeline surfaces used a hardcoded slate/sky/status scheme (not the old gold); neutrals/accent → surface/text/accent tokens; status families → `--ao-success/warning/danger`. Dense status pills keep legibility via `color-mix(in srgb, var(--ao-X) N%, transparent)` tints (matching the existing `nav.css` pattern) rather than collapsing to one flat token; inverted "dark-on-light" status cases fixed to `var(--ao-bg)` text. Admin scrim `rgba(9,9,11,.86)` → bg tint.
- Type: faux-bold removed (only Berkeley Mono Regular ships); every `font-size` → `--fs-*` (admin `clamp()` display headings reduced to `--fs-display/heading`); hierarchy now via size/color/uppercase.
- Spacing: `padding`/`margin`/`gap` snapped to the `--space-*` 4px grid; values wrapped in `max()/env()/calc()` (safe-area insets) preserved untouched.
- Guardrail: `boardGuardrails.test.ts` `.chip.ready` assertion updated from the old green `rgba` to the tokenized `color-mix` form.

Audit (all CP2 surfaces): 0 stray hex, 0 colored rgba, 0 px font-size, 0 faux-bold, 0 off-grid simple spacing, 0 CSS syntax artifacts (no dangling tokens / `;;` / empty values / family-less `font:`).

Validation: typecheck ✓, Vite build ✓, full suite 332/332 ✓. Visual screenshots not captured — the pipeline `*-data.js` are generated by `generate.py` (gitignored, absent), so live rendering needs data; recommend visual QA with generated data at review. Static evidence above + the per-rule diff confirm token correctness and legibility.

### CP2 revision 2 — CP2-F001/F002/F003 resolved
- F001 (`wip.html`): lane border via `color-mix` instead of `+ '55'` on a CSS var (was invalid `var(--ao-accent)55`).
- F002 (`board.html`): alpha-white literals on `order-badge` + pre-override `.review-btn` retokenized; only black shadows remain.
- F003 (`global-nav-ui.js`): mobile sheet fixed padding snapped to `--space-*`, safe-area `env()` preserved.
- Commit `18d87f3`; re-audit clean (0 alpha-concat / 0 non-shadow 8-digit hex / 0 off-scale calc px); build + 332/332 ✓.

## CP3 — single nav renderer (implemented)

Admin now renders the shared `AgentOpsNavModel` instead of hardcoded markup, matching board/wip/pipeline.

- `adminHtml.ts`: replaced the hardcoded `<nav class="admin-nav">` (which had a different item order + a bespoke "Back to app") with `<div id="global-nav" data-page="admin">` + the shared nav bundle (`/agentops-nav.js`, `/global-nav-ui.js`, `/activity-center-actions.js`, `/activity-center.js`, `/global-nav.js`).
- `term-control-center/public/`: added symlinks for `global-nav.js`, `global-nav-ui.js`, `activity-center.js`, `activity-center-actions.js` → `../../pipeline-diagram/…` (so Express serves them; mirrors the existing `agentops-nav.js` symlink).
- `adminCss.ts`: removed the now-dead `.admin-nav`/`.admin-brand`/`.admin-nav-links`/`.admin-back` rules (incl. responsive variants), preserving the shared `.actions`/`.form-toolbar`/`button` selectors.
- `admin.test.ts`: nav assertions updated from the hardcoded markup to the model-driven container + bundle (+ `doesNotMatch` on the old `.admin-nav`/"Back to app").

Result: identical item set/order/placement on every surface — `Board · Term · WIP · Activity · More`, Pipeline in the one consistent More overflow, only the active item differs. Term keeps its React `TopNav` renderer (also model-driven). Verified visually on the preview server (`:8799/admin-preview.html`) — nav renders correctly. Build ✓, tests 332/332 ✓. Commit `37c3575`.

### CP2 revision 3 — CP2-F004/F005 resolved
- F004 (`board.html`): removed `font-weight: 500` on the authoring compact-row (emphasis via color).
- F005 (`wip.html`): tokenized the body safe-area padding → `max(var(--space-16), env(...)) var(--space-16) var(--space-32)`.
- Also tokenized `adminCss.ts` browse-modal safe-area padding to `var(--space-12)` (same class, consistency).
- Comprehensive re-audit: 0 non-400 font-weights, 0 function-wrapped raw-px spacing across all surfaces. Build + 332/332 ✓. Commit `716b948`.

## CP4 — Term maximize mode (implemented)

First-class, persisted "maximize terminals" toggle in normal `/term/`, promoting the existing `?embed=1` reductions (US-6).

- `App.tsx`: added a `maximized` state (persisted via `MAXIMIZE_KEY = term-control-center.maximize.v1`, mirroring the `pinned` load/save pattern; survives reload). `TermShell` now applies `.app-shell-embedded` when `compact = embedded || model.maximized`, so the existing embed reductions (hero `display:none`, slim `2.05rem` toolbar, collapsed gaps) drive the maximize state with zero new CSS.
- Navigation stays reachable: only the URL `embed=1` flag still swaps `TopNav` to the brand-only embedded nav; the maximize toggle keeps the full model-driven `TopNav` (verified `.ao-nav-shell` stays `display:block` when maximized).
- Toggle control: a `Maximize`/`Restore` button (`aria-pressed`) in the always-visible pane-switcher (`RoleSwitcher` + `PairSwitcher`, via a shared `MaximizeToggle`), so it stays reachable to restore while maximized. Also added a `Toggle maximize terminals` command-palette entry (`toggleMaximize`) for keyboard reach, alongside the existing focus/theme toggles.
- Preserves the #57 safe-area behavior (the embedded `terminal-host` keeps its `1.2rem` bottom padding; no `env()`/safe-area code touched). Smallest viable change: no `styles.css`/`nav.css` edits.
- Guardrail: added `termBasePath.test.ts` "maximize toggle promotes the embedded reductions as a persisted control" asserting the key, load/save, `compact` composition, embedded-class reuse, `aria-pressed`, and the `Restore`/`Maximize` label.

Validation: typecheck ✓, Vite client+server build ✓, full suite **333/333** ✓. Visual: served the fresh `dist/` build on `:8788` and drove Chrome — toggle hides the hero, keeps the nav, gives the terminal host a substantial vertical gain, and the state survives reload. Commit `4887bc1`.

## Pre-merge light gate (CP1–CP4 bundle)

Focused bug-check (4 parallel finder angles over `git diff main...HEAD` + 1-vote verify) before the Part-1 PR. Findings and dispositions:

- **Fixed** (commit `f2493c8`):
  - `pipeline.html` — `PALETTE` was tokenized to `var(--ao-*)` strings but is assigned to canvas `ctx.fillStyle` (pen/text ink); canvas can't resolve `var()`, so annotation ink/text rendered with the wrong/stale color. Now resolves the tokens to concrete colors via `getComputedStyle`. Verified live on `:8799/pipeline.html`: tokens resolve to `#f4f8fb/#ee8f9a/#7ea6d8/#8fe29a`, swatches render them.
  - `global-nav-ui.js` — `.sr-only` `margin:-1px` had been tokenized to the invalid `-var(--space-4)` (bad syntax **and** wrong magnitude); restored `margin:-1px` (a fixed a11y idiom, not a spacing token). Also removed the now-empty `.ao-nav-create { }` rule.
  - `App.tsx` — the maximize toggle was rendered in `?embed=1` mode where it's a no-op yet still persisted `maximized=true`, leaking into later normal sessions. Now the toggle (pane-switcher button + command-palette item) renders only outside embed mode, matching the US-6 AC ("toggle in normal /term/"). Guardrail updated.
- **Deferred (documented, not a regression):** the shared nav renders Reviews/Updates persistent buttons; admin (unlike board/wip/pipeline) omits `completion-center.js`/`review-notify.js`, so those two buttons are inert on admin. Admin never had them pre-CP3, it degrades gracefully (guarded, no crash), and wiring board-feature polling into the admin/Express surface carries cross-server risk not worth rushing into a testing PR. Tracked for Part 2 / follow-up.

Re-validated after fixes: build ✓, **333/333** ✓. Remaining gate step: steward hygiene pass on the bundle (peer agent, human-relayed) → then open the Part-1 PR.

## Part 2 — CP1–CP4 merged (PR #89)

Part 1 merged to `main` at `579fd38`. Part 2 work continues on branch `prd/unified-design-system-part2-83` off the updated main. Current main test baseline confirmed **371/371** before CP5.

## CP5 — content density + microcopy (implemented)

US-8: persistent text/controls trimmed to labels+values; explanation moved to hover/on-focus; machine internals behind hover. Smallest-viable per-surface edits; the newer board UI (chat launcher #85/72, overlap monitor #87/73, heartbeat/stall alerts #86/65) left intact.

Term (`App.tsx`, `TerminalPane.tsx`, `ValidationLedgerPage.tsx`, `styles.css`):
- Heroes → a single quiet title. Term `HeroCopy` dropped the `HyperPi local terminal` eyebrow + the `Local coder/verifier cockpit…` lede → just `<h1>Agent workspace</h1>`. Ledger hero dropped its eyebrow+lede → `<h1>Validation ledger</h1>` (functional source / action-message lines kept). Now-unused `.eyebrow`/`.lede` CSS deleted (incl. the light-theme `.lede` selector, merged into `.terminal-toolbar`).
- Status dots: new `.status-dot` (8px round, matching the existing wip `.card .dot` convention; success/warning/danger by status family). Terminal headers and pane tabs now lead with the dot + human name. RoleSwitcher dropped the ` · {status}` text (status → button `title` hover); PairSwitcher dropped the `coder:running verifier:ready` string for one dot per role-pane (full string kept on `title`). New `pairPanes` helper.
- Machine internals on hover: terminal toolbar dropped the always-visible `pane-meta` (PID • cwd); the meta now rides a `title` on the header span. Removed the now-dead `.app-shell-embedded .pane-meta` rule.

Admin (`adminHtml.ts`, `adminClient.ts`, `adminCss.ts`):
- Hero collapsed: dropped the `AgentOps admin` kicker + the descriptive sentence → `<h1>Configuration</h1>`.
- Redundant heading removed: the project list dropped the `Project list` eyebrow + the "Select a project to edit it…" narration → a single `<h2>Configured projects</h2>`.
- Field hints → on-focus: the three `.help` hints (Grounding path…, Display-only metadata…, GitHub Project loader) are hidden by default and revealed via `label:focus-within .help`.

Board (`board.html`):
- Legend-as-banner removed: the persistent `Now/Next/Later/Blocked` `.legend` paragraph (+ its CSS) deleted; the same explanations now ride `title` tooltips on the column headers via a `COL_HINTS` map (`h.title = COL_HINTS[key]`). The `What to work on next` H1 was already a single quiet title (left as-is). Newer board UI untouched.

Deferred nav fold-in (Reviews/Updates inert on admin) — resolved (Option B):
- Decision: gate the buttons off admin rather than wire the scripts in. Ground truth (grep): board+wip+pipeline all load `completion-center.js`+`review-notify.js`; only admin omits them. Wiring them into the Express :3032 surface would 404-poll — `review-notify.js` hits `/api/review/*` + `/board/version`, which exist only on the static board server's `/api` proxy (Python review_server), NOT on Express (Express has `/term/completion-notifications` but no `/review/*`). So both "leave inert" and "wire in" lose.
- Implemented: `hideOnPages: ['admin']` on the `reviews`/`updates` activity items (`agentops-nav.js`); `global-nav.js` `activityItems()` filter extended with `&& !(item.hideOnPages && item.hideOnPages.includes(pageKey))`. Buttons keep working on board/wip/pipeline (where wired); gone on admin (no inert controls, no cross-server polling). Labels/hooks still present in the model, so board guardrails stay green.

Guardrails: `termBasePath.test.ts` — dropped the dead `.app-shell-embedded .pane-meta` assertion; added "leads with human name + status dot, meta on hover" + "heroes collapse to a single quiet title". `boardGuardrails.test.ts` — added "Reviews/Updates gated off surfaces without the board feed scripts" + "board column meanings live on header tooltips, not a legend banner". `admin.test.ts` — hero assertion updated to the trimmed `<h1>Configuration</h1>`.

Validation: typecheck ✓, Vite client+server build ✓, full suite **375/375** ✓ (371 baseline + 4 new guardrails). Visual: served the fresh `dist/` on :8788 + drove Chrome — hero is a single `Agent workspace` title; pane tabs + terminal headers lead with a status dot + human name (red dots = error, no PTY backend in preview); no PID/path in the persistent header.

## CP6 — spec + quality floor (implemented)

US-3 (spec): rewrote `docs/agentops-visual-system.md` to shipping reality — the blue `--ao-*` palette (verbatim from `agentops-tokens.css`), Berkeley Mono for both UI + mono, the `--fs-*` type scale + `--space-*` 4px spacing scale, the square-corner rule (status dots the one circular exception), a content-density section (US-8), and the consolidated single-nav-model rule (incl. Reviews/Updates only where wired). Removed all stale `Inter` / `JetBrains Mono` / warm-neutral / old-hex (`#09090b`, `#c4a46c`) references.

US-7 (accessibility floor) — audited the four floor items across the changed surfaces:
- Visible keyboard focus: present (term `button:focus-visible`, shared `:focus-visible` in `agentops-theme.css` + `nav.css`, admin `:focus-visible`). New status dots are `aria-hidden` non-focusable; status stays reachable via the button `title` + the right-side status word. No change needed.
- prefers-reduced-motion: was ABSENT on every surface (board.html alone had 9 animation/transition rules). Added the standard guard (`*,*::before,*::after { animation/transition near-instant; scroll-behavior auto }`) to the three surface stylesheets: `agentops-theme.css` (board/wip/pipeline), term `styles.css`, admin `adminCss.ts`. Motion becomes instant for reduced-motion users without removing any element/feature (heartbeat/stall/spinner indicators still render, just static).
- Mobile widths: pane-switcher keeps flex+ellipsis with the leading dot; admin hints reveal on focus on touch too; board keeps its mobile `::before` column labels. Tradeoff: the board legend→tooltip move makes the column *explanation* hover-only on desktop — this is the US-8 PRD target ("tooltip on the column headers"); the column labels themselves still show on mobile.
- Safe-area insets (#57): untouched by CP5/CP6 (git diff shows no `env()`/safe-area edits).

Guardrails: `boardGuardrails.test.ts` — spec asserts blue tokens + Berkeley Mono and no stale font/hex; reduced-motion asserted in theme + term CSS. `admin.test.ts` — reduced-motion + `label:focus-within .help` asserted in `ADMIN_CSS`.

Validation: build ✓, full suite **377/377** ✓.

## Main sync / PR-readiness pass (2026-06-27)

Branch `prd/unified-design-system-part2-83` was synced with `origin/main` at `1b3b878` in commit `0e691cd`.

Conflict resolved:
- `term-control-center/src/TerminalPane.tsx` — preserved main's `ceo-reviewer` profile, `browserOpen` / `onBrowserOpen`, `BrowserLaunchButton`, and terminal URL link handling while keeping CP5's status-dot-first terminal header and hover-only machine meta. No persistent `pane-meta` was reintroduced.
- `term-control-center/src/styles.css` — kept the browser launch button styling and applied it to CP5's `.pane-head` wrapper.

Post-sync validation:
- `cd term-control-center && npm run build` ✓
- `cd term-control-center && npm test` ✓ (**434/434**)
- Repo-local quality gate: `/gate --ml` not available in this worktree.
- Focused static smoke ✓: terminal header leads with `status-dot` + title, meta remains on `title`, `BrowserLaunchButton` and URL opening are retained; board legend remains tooltip-only; admin hero/help-on-focus remains trimmed; Reviews/Updates are hidden on Admin and still loaded on Board/WIP/Pipeline.

Cleanup:
- Removed temp preview artifacts `pipeline-diagram/admin-preview.html` and `pipeline-diagram/projects/`.
- Restored unrelated dirty `dev-plans/prd-backlog.md` after confirming it was timestamp-only.
- Removed untracked issue-83 run artifacts (`coder-ready.md`, `pr-draft.md`, `verifier-report.md`) so they cannot leak into the PR.

## Status

- **CP1–CP4 all verifier-approved.** CP1 approved; CP2 **approved** at rev 3 (`716b948`, CP2-F004/F005 fixed, no findings); CP3 approved (`37c3575`); CP4 **approved** (`4887bc1`, no findings — browser check confirmed hero hides / nav reachable / terminal area grows ~852px→1066px / state survives reload; build + 333/333). Verdicts in `verifier-report.md`.
- **Plan change (human-directed):** CP1–CP4 shipped as "Part 1" (PR #89, merged). CP5–CP6 follow on `prd/unified-design-system-part2-83` as "Part 2".
- **CP5 + CP6 implemented and synced with current main.** Post-sync build + **434/434** tests pass; focused smoke checks pass.
- Steward hygiene requested cleanup of the unrelated backlog timestamp and untracked run artifacts; both are resolved.
- Final verifier review found `CP5-F001`: board column meanings were moved to mouse-only `title` attributes on non-focusable headers.
- `CP5-F001` fix: replaced header-only titles with reusable focusable `?` help buttons. Desktop headers now include a button with `aria-label`, `title`, and a focus/hover CSS tooltip sourced from `COL_HINTS`; mobile/touch cells also include the same button while remaining hidden on desktop. Guardrail updated to require focusable/on-demand help and forbid `h.title = COL_HINTS[key]`.
- Validation after `CP5-F001`: `cd term-control-center && npm test -- tests/boardGuardrails.test.ts` (script ran full suite) ✓ **434/434**; `cd term-control-center && npm run build` ✓.
- Final verifier re-review approved `CP5-F001` and final bug-check passed: open findings 0, bug-check status `passed`.
- Branch is PR-ready after final cleanup; do not open the Part-2 PR without human confirmation.
