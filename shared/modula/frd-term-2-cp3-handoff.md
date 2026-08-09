# FRD Term-2 #364 — CP-3 handoff

Written 2026-08-09 at the end of the session that shipped CP-1 and CP-2.
Supersedes `frd-term-2-run1-handoff.md` (that one covered starting run #1).

## Where the stack is

| PR | Checkpoint | State |
|---|---|---|
| #478 | CP-1 envelope + global shell | **merged** — 2 review rounds, 1 finding |
| #479 | CP-2 sidebar parity | **merged** — 6 review rounds, 11 findings |
| #481 | untrack the trial-licensed font | **merged** (hotfix) |
| — | CP-3 pane + modebar | branch `frd364-cp3`, pushed, **no PR yet** |

Branch `frd364-cp3` in worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-frd364`,
parent `main`, synced, working tree clean. **Continue on it — do not create a new
branch or worktree.**

## Done on CP-3 so far

- **FR-9** pane head: live-dot that breathes only while healthy, role in weight +
  its number, model-chip seam, 4-bar gauge in its empty state, SVG gear.
- **FR-10** per-pane prompt composer (P-11: it existed and worked, hidden off phone).
- Responsive shell repair — the topbar reserved a 320px search column and pushed
  the account controls off screen below 760px; `.app-shell` also set a row gap at
  ≤1024px *or any coarse pointer*, so full-bleed was broken on tablets and touch.
- Berkeley Mono wired as `--mono-accent`, binary gitignored, provisioned by
  `term-control-center/scripts/extract-accent-font.mjs`.

## Remaining in CP-3

- **FR-11 modebar**: `.mode-add` bound to the existing add-browser-qa-pane action,
  `.renew-chip` desktop variant (hidden until the Term-1 FR-29 feed exists — never
  bind to the hardcoded-0 registry value, P-7), `.session-state` = pane count +
  group age.
- **FR-12 consult pane**: CSS parity, wired behind existing pair-tab semantics.
  P-12: `WorkspaceConsultPane.tsx` is built but `App.tsx` never sets
  `showConsultPane`.

Then CP-4 (diff, FRD tab, Lead dock CSS only — behaviour is #391-owned, modals)
and CP-5 (parity audit, parity note, pilot tracker row).

## Open operator decision

**Trial font in git history.** #481 removed the binary from the tree and added a
guard, but commit `a0c1f97` still contains it, on the forge and the GitHub mirror.
Purging needs `git filter-repo` + force push + mirror reset, which rewrites every
SHA and invalidates open PRs and ~76 worktrees. Recommendation: leave it unless
the licence terms make historical presence itself a problem.

## FRD premises that proved wrong — verify before building on any other

1. **P-1 is wrong.** The token layer was not verbatim-identical: `--ui` was Inter
   where the design is Instrument Sans (every glyph was the wrong face), and the
   chrome surfaces were tokens in neither layer.
2. **The topbar renew chip is phone-only** — `display:none` until ≤760px. The
   desktop renewal prompt belongs to the modebar (FR-11).
3. **The model-chip has no data source.** The client never fetches
   `/launch-profiles` and `PaneState` carries no model id. "Pane profile data
   exists" refers to the profile, not a model.

The FRD's line anchors are also stale (the prototype was edited post-approval).
Grep the class hooks instead of trusting line numbers.

## The lesson from CP-2's six rounds

Nine of eleven findings share one root cause: **parity work replaced working
behaviour with prototype-faithful behaviour and dropped something the app already
did** — touch access, folder scoping, selection scoping, menu targeting,
canonical-vs-view data, review lifecycle, attention colour. One was data loss
(mode-trimmed folders feeding a full-membership PATCH).

The prototype is a static mock of a desktop happy path. The app has touch users,
folders, dependencies, review lifecycles and mutation endpoints it never modelled.
Before replacing an affordance, list what it currently does. This belongs in the
CP-5 tracker row as a named risk of parity work, not just a round count.

## QA setup (rebuild after a fresh session)

Ports **3042/3043** — 3032/3033 belong to another live worktree; capturing there
QAs someone else's build.

```bash
cd term-control-center
cat > vite.qa.config.mjs <<'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
const API = 'http://127.0.0.1:3042'
const routes = ['/health', '/sessions', '/groups', '/launch-context', '/kody-review', '/term-config.js', '/page-bot', '/launch-profiles', '/api/admin']
export default defineConfig({
  base: './', plugins: [react()],
  server: { host: '127.0.0.1', port: 3043, strictPort: true,
    proxy: { ...Object.fromEntries(routes.map(r => [r, API])), '/ws': { target: 'ws://127.0.0.1:3042', ws: true } } },
})
EOF
npx vite --config vite.qa.config.mjs      # delete this file before committing
```

The dev environment has **no jobs**, so cards, chips and menus cannot be seen
without fixtures. A fixture backend serving `/groups` with populated jobs (issue
numbers, review buckets, ceo-reviewer panes) makes the captures meaningful — write
one to a scratch path and run it on 3042. Set `QA_THEME=light` for light captures.

Capture with:
```bash
node term-control-center/scripts/capture-parity.mjs \
  --url http://127.0.0.1:3043/ --out <run>/captures/app --name cp3 \
  --viewports desktop,narrow,phone
```
`runs/` is gitignored — receipts must be `git add -f`'d or reviewers cannot open
what the PR cites.

## Continuation prompts

### /fast-lane

```
/fast-lane Continue FRD Term-2 (forge issue #364), pilot run #1, Opus 5 on Claude Code.

State: CP-1 (#478) and CP-2 (#479) are merged to main; hotfix #481 merged. Work
continues on the EXISTING branch frd364-cp3 in worktree
/mnt/hyperliquid-data/projects/worktrees/agentops-frd364 — do not create a new
worktree or branch. Its parent is main and it is synced. No PR is open for it yet.

Done on cp3: FR-9 pane head (live-dot, role+number, model seam, 4-bar gauge in
its empty state, SVG gear), FR-10 per-pane prompt composer, responsive shell
repair (topbar/frame below 1100px and 760px), Berkeley Mono wired as --mono-accent
with the binary gitignored and provisioned by
term-control-center/scripts/extract-accent-font.mjs.

Remaining in CP-3:
- FR-11 modebar: .mode-add bound to the existing add-browser-qa-pane action,
  .renew-chip desktop variant (hidden until the Term-1 FR-29 feed exists — never
  bind to the hardcoded-0 registry value), .session-state = pane count + group age.
- FR-12 consult pane: CSS parity, wired behind existing pair-tab semantics.
  P-12: WorkspaceConsultPane.tsx is built but App.tsx never sets showConsultPane.

Rules that bind: build every region from the prototype source, never memory
(5R.1 — the FRD's line anchors are stale, grep the class hooks instead). No dead
controls. Verify each FRD "grounded fact" before building on it — three have
already proved wrong (P-1 tokens, the topbar renew chip is phone-only, and the
model-chip has no data source). Use scripts/capture-parity.mjs for receipts and a
fixture backend on ports 3042/3043 — 3032/3033 belong to another live worktree.
Compare test failures by NAME against an origin/main baseline, not by count.
Do not merge.
```

### /goal

```
/goal FRD #364 CP-3 complete: FR-9..FR-12 all shipped on frd364-cp3 — pane head,
per-pane composer, modebar (.mode-add, .renew-chip, .session-state) and the
consult pane wired behind existing semantics. Artifacts required: capture-parity
screenshots for pane + modebar at desktop/narrow/phone in dark and light under
runs/frd-364-term2-parity/captures/ (force-added, runs/ is gitignored); contrast
gate green; typecheck and vite build clean; a regression test for every seam
touched; full suite showing NO failure absent from the origin/main baseline,
compared by test name; PR open against main with the review round clean or every
finding addressed. Do NOT merge — stop at review-clean and report.
```
