# Coder Handoff — Issue #119 Terminal Page Active Jobs Sidebar

## Source of truth
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/119
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-119`
- Branch: `prd/d3-prd-terminal-page-active-jobs-119`

## Scope controls
- Allowed: `term-control-center/src/App.tsx`, `term-control-center/src/styles.css`, safe reuse/light extension of `GET /groups`, tests, terminal session docs, run artifacts.
- Forbidden: raw terminal output/transcripts/secrets/env/attach-token display, per-pane sidebar rows, new persistence store, new realtime infra, kill/restart/relaunch/pause/job-control actions, unrelated board/co-worker/routes/deploy changes, PR/merge/deploy/trading/backtests.
- Validation: `npm --prefix term-control-center run test`; `npm --prefix term-control-center run build`.
- Stop condition: final verifier implementation approval plus final verifier bug-check approval, or human escalation.

## Verifier checkpoints
1. Data checkpoint — sidebar consumes existing group metadata safely and exposes only safe group-level fields.
2. Layout checkpoint — desktop sidebar renders one row per job and remains absent/collapsed in embedded or narrow contexts.
3. Switching checkpoint — clicking a job opens or recovers the correct session group without job-control side effects.
4. Regression checkpoint — existing split-pane pair views remain unchanged.
5. Project isolation checkpoint — sidebar filters to the active project and does not leak other project sessions.
6. Responsive/security checkpoint — mobile behavior works and no sensitive data is exposed.

## Pre-existing worktree state
- `git status --short --branch` before edits: clean (`## prd/d3-prd-terminal-page-active-jobs-119...origin/main`).

## Implementation summary
- Added a non-embedded `/term/` active-jobs sidebar that polls existing `/groups` metadata and renders one row per session group.
- Rows are filtered to the active project from the current launch group or `/launch-context`, exclude exited groups, highlight the active group, and show safe group-level labels only.
- Clicking a row swaps the main terminal workspace to the selected recovered group using existing pane attach metadata; it does not call DELETE, browser-qa launch, restart, kill, or other job-control routes.
- Desktop layout places the sidebar left of the terminal workspace. Narrow layouts show a fixed `Jobs` drawer; embedded/compact/maximized/browser-focused terminal layouts do not render the sidebar.
- Existing pair switcher/focused-pane stack behavior is retained; switching jobs preserves the current effective pair where possible.
- Added docs for sidebar safety/navigation behavior and a focused test file for grouping, project filtering, active highlight, responsive drawer, and no job-control row actions.

## Changed files
- `term-control-center/src/App.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/terminalJobSidebar.test.ts`
- `term-control-center/vite.config.ts`
- `docs/agentops-terminal-sessions.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-119-terminal-active-jobs/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-119-terminal-active-jobs/validation-ledger-log.md`

## Validation log
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts`
- PASS: `npm --prefix term-control-center run build`
- FAIL/blocked unrelated: `npm --prefix term-control-center run test` still reports pre-existing/environment failures in launch/runtime tests unrelated to sidebar files, including runtime browser profile expectation mismatches, PRD review auth expectation, and server launch fixture 400s for issue 1019 branch/worktree validation. Targeted sidebar and existing term base tests pass.

## Risks / manual QA
- Manual browser QA not run yet. Needs operator/verifier confirmation on `/term/` with multiple live groups, row switching, embedded board/modal terminal absence, and cross-project filtering.
- `/groups` still returns existing attach metadata for recovery; sidebar rendering only uses safe labels and never displays tokens or terminal output.

## Revision 2 fixes for verifier findings
- F119-R1-001: Sidebar now filters to attachable groups only, excludes empty `not_started`/non-attachable rows, merges existing board `evonome-term-groups` remembered attach metadata before filtering, and saves only attachable groups back to that existing browser store.
- F119-R1-002: `/groups` non-OK responses and fetch exceptions now set an explicit `Jobs unavailable.` state instead of rendering `No active jobs.`
- Added focused assertions for attachability filtering, remembered attach metadata merge, and unavailable-state rendering.

## Revision 2 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts`
- PASS: `npm --prefix term-control-center run build`

## Revision 3 fix for verifier finding
- F119-R2-001: Remembered attach metadata saving now merges current attachable groups into the existing `evonome-term-groups` store and preserves unrelated fresh groups by id instead of replacing the store with the active-project subset.
- `fetchActiveJobs` now saves the merged full `/groups` set, then filters visible rows for the active project.
- Added focused assertion that saving sidebar jobs preserves other remembered groups.

## Revision 3 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts`
- PASS: `npm --prefix term-control-center run build`
- Operator error note: one combined shell command attempted `npm --prefix .. run build` from inside `term-control-center`, which failed because the repo root has no package.json; reran the required root-relative build command successfully afterward.

## Steward hygiene review
- Steward response: clean.
- Steward found changed-file placement appropriate for UI, CSS, tests, docs, and run artifacts.
- Steward found no raw logs/transcripts/secrets in run artifacts.
- Steward noted ignored local build/cache artifacts (`term-control-center/dist/`, `term-control-center/node_modules/`, `pipeline-diagram/__pycache__/`) are untracked/ignored and require no cleanup.

## Final verifier status
- Revision 4 verdict: approved.
- Final bug-check status: passed.
- Open findings: 0.
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-119-terminal-active-jobs/verifier-report.md`.

## Localhost demo follow-up
- Added `term-control-center/vite.config.ts` proxies for `/groups` and `/launch-context` so the Vite dev server can show the new sidebar while proxying existing Term Control backend metadata.
- Added focused test assertion for those dev proxies.
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts`
- PASS: `npm --prefix term-control-center run build`
- Started Vite-only demo server on `http://127.0.0.1:3033/`, proxying backend `127.0.0.1:3032`; `/groups` probe returned 4 groups including #118 and #119.
- Cleanup after verifier hygiene request: stopped the temporary Vite demo process and removed transient localhost log/pid files from the run directory.
