# FRD Term-2 #364 — CP-4 handoff

Written 2026-08-09 at the end of the session that shipped CP-3.
Supersedes `frd-term-2-cp3-handoff.md`.

## Where the stack is

| PR | Checkpoint | State |
|---|---|---|
| #478 | CP-1 envelope + global shell | **merged** — 2 rounds, 1 finding |
| #479 | CP-2 sidebar parity | **merged** — 6 rounds, 11 findings |
| #481 | untrack the trial-licensed font | **merged** (hotfix) |
| #483 | CP-3 pane + modebar parity | **merged** — 2 rounds, 1 finding |
| — | CP-4 diff, FRD tab, dock, modals | not started |

`main` is at `c31e274`. Canonical checkout updated, `frd364-cp3` deleted remote-side,
mirror synced. The worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-frd364`
is free — its local `frd364-cp3` is merged and can be replaced. **Create `frd364-cp4`
off `main` there; do not make a new worktree.**

## What CP-3 shipped

FR-9 pane head, FR-10 per-pane composer, FR-11 modebar (`.mode-add` → the existing
open-Browser-QA action, `.session-state` = pane count + group age, `.renew-chip` desktop
variant unfed), FR-12 consult pane CSS parity, plus the responsive shell repair and
Berkeley Mono as `--mono-accent`.

Receipt: `qa-receipts/frd-364/cp3-modebar-and-consult.md`. Captures:
`dev-plans/agentops/coder-verifier-workflow/runs/frd-364-term2-parity/captures/app/cp3-modebar-*`.

## CP-4 scope (FRD §7, quoted — do not paraphrase from memory)

- **FR-13** diff adopts the prototype's full-width mode-tab placement, **keeping the app's
  richer review aids**.
- **FR-14** the FRD tab ships as a read-only in-context viewer of the canonical FRD (issue
  body / task data already on the group). Select-to-amend → Lead dock is a **stretch**
  item (`/lead/message` exists). The prototype's full amendment system — author-coloured
  margin bars, amendment cards with Lead dispositions, away-jump bar, added post-approval
  in `b8fab30`/#377 — is **out of scope and currently unowned**; name it in the FR-18
  parity note.
- **FR-15** Lead panel styled to the prototype `.lead-panel` spec — chat-panel chrome,
  picker styling, collapse-to-tab, per-job scope line. **Behaviour unchanged and
  #391-owned.**
- **FR-16** modal content/copy parity.

## Rules that bind

- **Build every region from the prototype source, never memory** (5R.1). The FRD's line
  anchors are stale — grep the class hooks (`.frd-shell`, `.lead-panel`, `.diff*`).
- **No dead controls.** A control that cannot act is absent, not inert.
- **Verify every "grounded fact" before building on it.** Four have already proved wrong or
  needed correcting: P-1 (tokens were not verbatim-identical), the topbar renew chip is
  phone-only, the model-chip has no data source, and P-15 itself was corrected on 2026-08-05.
- **Never fabricate content to fill a surface.** CP-3's consult pane was carrying an
  invented question, answer and source count; it now renders only from a real
  `ConsultState` and therefore renders nothing. FR-14's viewer must read the real issue
  body/task data or show an empty state — never sample FRD text.
- **Compare test failures by NAME against an `origin/main` baseline, not by count.**
  `./scripts/verify.sh` does this properly via the merge-base; use it, not a manual diff.
- **Do not merge.** Operator's word only.

## The CP-3 lesson, worth more than its round count

Two of the three defects CP-3 fixed came from **looking at the captures**, not from tests:
a narrow pane clipped its own name to a bare status dot, and a newly-added session-state
pushed the Diff tab into the tab row's scroll overflow. Neither was test-visible.

The single review finding was a **widened-surface regression**: FR-10 made the prompt
composer full-time on desktop, and the composer cleared its textarea even when the socket
was closed and the send silently no-oped — so Send during connect/recovery/disconnect
destroyed the prompt. Same shape as nine of CP-2's eleven findings.

**So: after widening any surface, list what it now touches that it did not before.** CP-4
widens the diff placement and restyles the Lead dock — both sit on live behaviour.

## Operator constraint (2026-08-09) — read before touching the dock

Almost every page of the app has a sidebar with an AI assistant in it; the assistants
differ per page but **the sidebar shell and the assistant dock must be reusable
components**, not per-page forks. `PageBotPanel` (`PageBotPanelContract`) is already the
shared assistant — reuse it, never fork it. `WorkspaceLeadDock` is a 24-line shell over it
and its `workspace-lead-*` chrome is **not** shared; `JobSidebar` is job-specific with no
generic page-sidebar shell underneath.

FR-15 is the natural moment to generalise the dock shell — but its **behaviour is
#391-owned**, so raise it as a decision rather than reshaping it unilaterally. Also note
the Term view is being renamed **Workspace** in the final app.

## Carried deferrals (for the FR-18 parity note)

1. **Consult pane has no feed.** Consults travel agent-to-agent over the coms transport;
   the term server publishes nothing. E-lane's ephemeral-summon work.
2. **430px horizontal overflow.** `TerminalArea` gives every pane `minSize={260}` and only
   toggles `visible`, so a four-pane group reserves ~1040px. Pre-existing on main; AC-4 is
   clean at the design's real breakpoints (760/1100/1600). Candidate fix
   `minSize={phoneMode ? 0 : 260}` needs its own resize verification.
3. **Gauge / renew chip / model chip** still await the Term-1 FR-29 feed.
4. **Trial font in git history** — commit `a0c1f97` still contains the binary; purging needs
   `filter-repo` + force push. Open operator decision.

## QA setup (rebuild each session)

Ports **3042/3043** — 3032/3033 belong to another live worktree. Write a fixture backend
serving `/groups`, `/kody-review/sessions`, `/launch-context`, `/completion-states` and
`/term-config.js` (the last sets `window.__TERM_CONTROL__`, including `defaultTheme` — that
is the only way to get light captures; there is no theme query param). Put it in a scratch
path, and a `vite.qa.config.mjs` proxying those routes to 3042 — **delete that config before
committing.** The dev environment has no jobs, so nothing renders without fixtures.

```bash
node term-control-center/scripts/capture-parity.mjs \
  --url 'http://127.0.0.1:3043/?group=<url-encoded group json>' \
  --out dev-plans/agentops/coder-verifier-workflow/runs/frd-364-term2-parity/captures/app \
  --name cp4-<region> --viewports desktop,narrow,phone
```

`runs/` is gitignored — `git add -f` the captures or reviewers cannot open what the PR
cites. The browser-extension path cannot reach the local dev server; headless is the
verification vehicle (and the script says so).

## Gates

`./scripts/verify.sh` (green = python suite, compileall, typecheck, whitespace, and the TS
suite at merge-base baseline parity) plus `npm --prefix term-control-center run
check:contrast`. Component-only accent/warning/danger fail the 4.5:1 text floor — carry
state with a dot or use `--fg`, never coloured body text.

## Note on the pilot tracker

`docs/fast-lane-pilot.md` run-log row is still empty by design: the lane puts it on the
**top PR of the stack**, which is CP-5. CP-4 does not carry it.
