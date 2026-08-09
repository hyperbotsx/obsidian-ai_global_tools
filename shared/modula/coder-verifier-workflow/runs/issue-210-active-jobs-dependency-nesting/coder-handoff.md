# Coder Handoff — Issue #210 Active Jobs Dependency Nesting

## Scope
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/210
- Branch: `prd/active-jobs-dependency-nesting-210`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-210`
- Pre-existing dirty files before editing: none (`git status --short --branch` was clean).

## Allowed / forbidden / stop condition
- Allowed: Term Control Active Jobs state, routes, sidebar and board UI, scoped tests, user documentation, and this run artifact.
- Forbidden: GitHub Project mutations; automatic launch/pause/termination; PR, merge, deployment, approval, trading, or backtesting actions; raw terminal output, credentials, tokens, cookies, or secrets in persisted state.
- Stop condition: final verifier bug-check approval after required Steward hygiene review. This task is phased: A dependency edges and resolution; B named groups and selection; C operator aids.
- Operator continuation authorization is recorded for the remaining bounded scope: suggestions, regression review, Steward hygiene review, final validation, and verifier bug-check.

## Researcher consult
- Required by engineering standards before selecting state/test structure. Completed 2026-07-14 via the live `researcher` peer.
- State is project-indexed, versioned, validated persisted data; React UI persistence will use a pure initializer plus effect-based writes.
- UI will use immutable functional updates. Drag/drop remains an enhancement with explicit directional confirmation; native controls provide keyboard and touch alternatives.
- Sources: React `useState`/`useEffect` (accessed 2026-07-14); W3C WCAG 2.2 SC 2.1.1 and 2.5.7 (Recommendation 2024-12-12); MDN Web Storage API (accessed 2026-07-14).

## Planned verifier checkpoints
1. State model — project-scoped durable dependency records; self/cycle rejection; clear only on verified completion. **Approved at revision 2.**
2. Sidebar dependency UI — clear nested rendering, project-scoped confirmed drag/drop, and keyboard/menu fallback. **Approved at revision 10.**
3. Collapsible grouping — desktop range selection, touch Select mode, named folder creation, collapse/expand (including all), rename, remove-member, dissolve, notes/pins persistence, status rollups, safe bulk actions, completed folding, and non-mutating title-keyword suggestions. **Approved at revision 25.**
4. Completion integration — verified closeout/merged-synced release and explicit Resume, Keep paused, and Dismiss prompt controls. **Approved at revision 14.**
5. Stale/missing session handling — a retained edge with a non-active blocker displays `blocker session closed; merge not verified`. **Approved at revision 10.**
6. Regression — reopen, search, filtering, completion actions, attach behavior.
7. Final bug-check — after Steward placement/hygiene review.

## Initial architecture evidence
- Current active-jobs views are `term-control-center/src/App.tsx` and `pipeline-diagram/board.html`.
- Existing session persistence owns `groups.json` through `term-control-center/server/sessionStore.ts`; PRD requires a clearly distinct namespace, so no new state will be added to `groups.json`.
- Existing durable completion state is `term-control-center/server/completionStore.ts` and already distinguishes verified `merged_synced` / `closeout_done` from `dismissed`.
- The Phase A store is intentionally separate from `groups.json`: `term-control-center/server/jobDependencyStore.ts` persists only project-indexed dependency edges in `job-dependencies.json` with mode `0600` and no task/session/log data.

## Changed files
- `term-control-center/server/jobDependencyStore.ts` — durable project-scoped dependency model, validation, self/cycle rejection, clear transition, and verified-completion release transition.
- `term-control-center/tests/jobDependencyStore.test.ts` — persistence/project isolation, self/cycle rejection, clear behavior, verified-only auto-release, and malformed-data recovery tests.
- `term-control-center/server/jobDependencyRoutes.ts` — authenticated project-scoped read/create/clear routes; dependency creation requires both current jobs to belong to the selected project.
- `term-control-center/server/index.ts` — creates the separate durable dependency store and registers the routes.
- `term-control-center/tests/jobDependencyRoutes.test.ts` — route-level project-scope and verified-release coverage.
- `term-control-center/server/jobFolderStore.ts` and `server/jobFolderRoutes.ts` — separate project-scoped durable folder state and authenticated CRUD routes; never use session `groups.json`.
- `term-control-center/src/jobGrouping.ts` — pure nesting, search, selection, rollup, and resume helpers.
- `term-control-center/src/jobView.ts` — Active Jobs view helpers for job metadata, attention, mode, role, and session-safe presentation; it owns no completion-state classifier.
- `term-control-center/src/App.tsx` and `src/styles.css` — Active Jobs integration and shared layout styles.
- `term-control-center/src/JobSidebar.tsx`, `src/JobSidebar.css`, `src/JobFolder.css`, and `src/JobResumeBanner.tsx` — dependency/folder sidebar, canonical completion overlay consumption, and explicit resume-choice UI; styles are split by sidebar versus folder responsibility, each below the 300-line KISS limit.
- `term-control-center/src/resumeChoice.ts`, `src/useResumePrompts.ts`, `src/folderBulk.ts`, `src/JobFolderHeader.tsx`, and `src/JobFolderLayoutActions.tsx` — pure explicit-choice/bulk intents, failure-tolerant local resume-prompt persistence, folder header/controls, and explicit layout controls.
- `term-control-center/src/jobFolderActions.ts` — project-scoped overlay and folder/dependency mutations with bounded error feedback.
- `term-control-center/src/folderSuggestions.ts` and `src/JobFolderSuggestions.tsx` — deterministic title-keyword suggestions and their explicit-create-only UI; no suggestion mutates state until the operator clicks Create.
- `term-control-center/tests/jobFolderStore.test.ts`, `tests/jobFolderRoutes.test.ts`, `tests/jobGrouping.test.ts`, `tests/jobFolderActions.test.ts`, `tests/resumeChoice.test.ts`, `tests/folderBulk.test.ts`, `tests/folderSuggestions.test.ts`, and `tests/terminalJobSidebar.test.ts` — durable folder, route, UI-helper, pin-ordering, overlay-isolation, mutation-error, resume-intent, bulk-action, suggestion, and sidebar interaction tests.
- `docs/agentops-terminal-sessions.md` — operator-facing dependency and folder behavior, including scoped local persistence and no session/GitHub mutation.

## Revision fixes
- Addressed `F210-CP1-001`: a dependent now has exactly one blocker. A second distinct blocker is rejected until the existing dependency is cleared; malformed persisted duplicate-parent data preserves the first valid edge; release removes only the resolved edge even for malformed in-memory input.
- Addressed `F210-CP4-001`: creation now uses the same visibility boundary as Active Jobs and rejects exited dependents or blockers, while persisted relationships remain readable after later session exit.
- Addressed UI findings `F210-CP23-001` through `F210-CP23-012`: visual folders are now in the distinct `jobFolder` namespace and `job-folders.json`; member additions merge rather than replace; folder names/notes redact credential-like text; sidebar rendering/actions moved into focused modules with one stylesheet owner; folders render structurally with collapsed-match counts; selection is visible-row/project scoped and row-tappable on touch; overlay failures retain last state only within the active project; historical folder members remain extendable; and folder/job pin plus note controls and pin ordering are exposed.
- Revision 4 addresses `F210-CP23-007` through `F210-CP23-013`: sidebar and folder styles are split into 204- and 127-line files; a folder with a pinned member is deterministically promoted over unpinned folders; the synchronous `overlayForProject` render guard returns an empty overlay on a project mismatch; a mocked dependency-cycle mutation confirms direction-explicit copy, bounded notice, and refresh; and the changed-files/test references above use the actual `jobFolder` names (no `jobGroup` files exist).
- Revision 5 addresses `F210-CP23-014`: the mocked mutation test now delegates fixture setup, request/response assertions, and global cleanup to named helpers; every function is below the KISS 20-line limit without reducing coverage.
- Revision 6 completes the remaining basic dependency/folder interactions: a PRD can be dragged onto another row only as an explicit, direction-confirmed wait relationship; folders expose rename and remove-member controls; and a missing/exited blocker remains visibly waiting with a merge-not-verified warning.
- Revision 7 addresses `F210-CP23-015`, `F210-CP5-001`, and `F210-CP23-016`: drag interaction is disabled outside a single active project; stale health includes missing, exited/error, and stale/unrecoverable pane recovery states; and the checkpoint/touched-file handoff inventory is reconciled.
- Revision 8 adds the pure drag source-to-dependent/target-to-blocker mapping regression and reconciles revision-7 validation/status evidence.
- Revision 9 corrects the sidebar integration assertion to cover the drag adapter and guarded dependent handoff.
- Revision 11 adds explicit Resume, Keep paused, and Dismiss controls for verified-unblocked jobs. Resume is an operator click that reopens the existing job; it never auto-launches a session. Keep paused and Dismiss hide the prompt without mutating sessions or GitHub state.
- Revision 12 addresses `F210-CP4-002`: project-scoped pending prompts merge new release events, survive empty polls and browser refresh, and dequeue only after an explicit choice; pure reducer tests cover retention/removal/project isolation and UI tests cover the local persistence surface.
- Revision 13 addresses `F210-CP4-003` and `F210-CP4-004`: a pure intent controller, used by the sidebar, makes Resume the only reopen action and keeps pause/dismiss non-mutating; storage writes are caught so queue behavior remains in memory when persistence is denied.
- Revision 15 adds explicit per-folder bulk actions: Open all terminals attaches only existing member jobs after a click; Check status and Request updates remain local informational aids and never launch, mutate, or bypass human gates.
- Revision 16 addresses `F210-CP3-001` through `F210-CP3-003`: folder selection is filtered by a pure helper and sent through one real existing-session bulk attach callback; pure action tests cover historical-member filtering and local notices; the cumulative inventory lists the new modules.
- Revision 17 addresses `F210-CP3-004`: the attach plan filters out groups with no safe panes before selecting the primary group, active group identity, workspace panes, and attached-job count; pure tests cover all-safe, mixed, and no-safe cases.
- Revision 18 adds explicit project-scoped Collapse all folders and Expand all folders controls that mutate only local folder collapse state after an operator click.
- Revision 19 addresses `F210-CP3-005` and `F210-CP3-006`: mocked action coverage verifies project-scoped changed-folder PATCH requests, exact boolean payloads, local refresh/no-notice behavior, and handoff inventory/status now records the layout module and complete bulk actions.
- Revision 20 adds an explicit Hide done control for folder members. It hides recognized verified-completion states from the visible range without changing membership or history.
- Revision 22 addressed `F210-CP3-008`; verifier requested a bounded rework of `F210-CP3-007` and `F210-CP3-009`.
- Revision 23 addresses `F210-CP3-007` and `F210-CP3-009`: the canonical overlay fixture uses the valid `awaiting_completion` state, asserts requests for every supplied current job ID, and reconciles file ownership plus checkpoint approvals.
- Revision 24 implements PRD requirement 36: deterministic suggestions use a shared non-generic title keyword among ungrouped jobs and expose only explicit Create controls within one active project; the UI does not auto-create folders or alter sessions, dependencies, GitHub, or human gates.
- Revision 25 addresses `F210-CP3-010`: suggestions require the current project's successfully loaded, non-stale overlay; unloaded, failed, and cross-project overlays suppress all suggestion controls, preventing membership moves from stale folder data.
- Revision 27 addresses `F210-CP6-001` and `F210-CP6-002`: route-test setup/assertions are delegated to named sub-20-line helpers without coverage loss, and the validation ledger records the exact focused command plus accurately scopes the obsolete dependency-resolution failure as historical.
- Revision 28 addresses Steward hygiene findings: removed generated `term-control-center/build/`, `term-control-center/dist/`, and `pipeline-diagram/__pycache__/` artifacts; documented the distinct `job-dependencies.json` and `job-folders.json` state files, permissions, and privacy-limited fields.
- Revision 29 addresses `F210-FINAL-001` and `F210-FINAL-002`: existing-folder assignment and remove-member controls require a successfully loaded, non-stale overlay, and canonical completed folding includes `validation_queued` alongside the verified terminal lifecycle states.

## Validation
- PASS: `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/jobDependencyStore.test.ts` (5/5 passed after `F210-CP1-001` fix).
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/jobDependencyStore.test.ts tests/jobDependencyRoutes.test.ts` (6/6 passed using a temporary, removed symlink to the repository-shared `node_modules`).
- PASS: `cd term-control-center && npm run build` (typecheck, Vite client build, server build passed using a temporary removed symlink to repository-shared `node_modules`).
- PASS: focused folder/group/sidebar suite (37/37 at revision 6, including drag/folder control and stale-blocker regression coverage, using a temporary removed symlink to repository-shared `node_modules`).
- PASS: `cd term-control-center && npm run build` at revision 6 (typecheck, Vite client build, and server build; temporary removed symlink).
- PASS: revision 7 focused grouping/sidebar suite (36/36), `cd term-control-center && npm run typecheck`, and `git diff --check`.
- FAIL: revision 8 focused grouping/sidebar suite (36/37; stale sidebar drag assertion); `cd term-control-center && npm run typecheck` and `git diff --check` passed.
- PASS: revision 9 focused grouping/action/sidebar suite (38/38), `cd term-control-center && npm run typecheck`, and `git diff --check` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 11 focused grouping/action/sidebar suite (39/39) and `cd term-control-center && npm run build` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 12 focused grouping/action/sidebar suite (40/40) and `cd term-control-center && npm run build` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 13 focused grouping/action/sidebar/resume-choice suite (42/42) and `cd term-control-center && npm run build` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 15 terminal sidebar suite (17/17) and `cd term-control-center && npm run typecheck` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 16 folder-bulk/sidebar suite (19/19) and `cd term-control-center && npm run typecheck` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 17 folder-bulk suite (3/3) and `cd term-control-center && npm run typecheck` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 18 terminal sidebar suite (18/18) and `cd term-control-center && npm run typecheck` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 19 folder-layout/sidebar suite (20/20), `cd term-control-center && npm run typecheck`, and `git diff --check` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 20 grouping suite (24/24) and `cd term-control-center && npm run typecheck` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 21 grouping suite (25/25), `cd term-control-center && npm run typecheck`, and `git diff --check` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 23 completion-overlay/grouping suite (28/28), `cd term-control-center && npm run typecheck`, and `git diff --check` (temporary removed symlink to repository-shared `node_modules`).
- PASS: revision 24 focused suggestion/sidebar/grouping/action suite (49/49), `cd term-control-center && npm run typecheck`, and `git diff --check` (repository-shared dependency link).
- PASS: revision 25 focused suggestion/sidebar/grouping/action suite (51/51), `cd term-control-center && npm run typecheck`, and `git diff --check` (temporary dependency link removed after validation).
- PASS: `npm --prefix term-control-center run build` (typecheck, Vite client build, and server build; temporary dependency link removed after validation).
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/jobDependencyStore.test.ts tests/jobDependencyRoutes.test.ts tests/jobFolderStore.test.ts tests/jobFolderRoutes.test.ts tests/jobFolderActions.test.ts tests/jobGrouping.test.ts tests/folderBulk.test.ts tests/folderSuggestions.test.ts tests/resumeChoice.test.ts tests/terminalJobSidebar.test.ts` (72/72; dependency/folder stores and routes, overlays, grouping, bulk attach, resume choices, suggestions, sidebar static integration, and documentation; temporary dependency link removed after validation).
- BLOCKED/PRE-EXISTING: `npm --prefix term-control-center run test` exceeded the 180-second and 600-second bounded validation timeouts after reporting 211 passing existing tests and no failure. The full suite did not reach completion; the focused Issue #210 regression suite and full build pass.
- HISTORICAL: before the repository-shared dependency setup used for the current validation, a server typecheck reported missing `node-pty`/`react-dom` types and existing implicit-any errors. It is superseded for the current scope by the passing full build above and is not a current validation block.
- PASS: Steward cleanup verification removed all requested generated artifacts; `git diff --check` passed.
- PASS: final-fix focused overlay/grouping/sidebar suite (49/49) and `cd term-control-center && npm run typecheck`; temporary dependency link removed after validation.
- PASS: final exact Issue #210 regression command (73/73) and `npm --prefix term-control-center run build`; generated build/dist artifacts and the temporary dependency link were removed after validation.

## Verifier status
- Checkpoint 1 approved at revision 2; `F210-CP1-001` was addressed.
- Checkpoint 4 backend API slice approved at revision 2; `F210-CP4-001` was addressed.
- Checkpoints 2 and 5 were approved at revision 10; revision-8 failure and revision-9 passing evidence are recorded above.
- Checkpoint 4 completion integration, including the Resume prompt UI, was approved at revision 14.
- Folder bulk-action operator-aid slice was approved at revision 17.
- Folder layout-action operator-aid slice was approved at revision 19.
- Revision 22 resolved `F210-CP3-008`; revision 23 was approved for `F210-CP3-007` and `F210-CP3-009`.
- Revision 24 requested `F210-CP3-010`; revision 25 was approved.
- Checkpoint 3 is approved at revision 25.
- Revision 26 requested `F210-CP6-001` and `F210-CP6-002`; revision 27 was approved for regression.
- Steward cleanup was approved in the revision-28 verifier recheck.
- Final verifier bug-check approved at revision 29 with `bug_check_status: passed`; `F210-FINAL-001` and `F210-FINAL-002` were addressed.
- Stop condition reached. No PR, commit, merge, deployment, approval, trade, or backtest was created.

## Notes / risks for verifier
- The API writes only explicit operator-created dependency records; it does not mutate sessions or launch/pause/terminate jobs.
- Release criteria deliberately excludes `dismissed`; it accepts only verified `merged_synced`, closeout, teardown, or validation-queued lifecycle states.
