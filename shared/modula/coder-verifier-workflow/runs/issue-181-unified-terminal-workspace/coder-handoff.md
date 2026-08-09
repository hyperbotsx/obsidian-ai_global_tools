# Coder Handoff — Issue #181 Unified Terminal Workspace and Parallel PRD Sessions

## Source of truth
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/181
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-181`
- Branch: `prd/unified-terminal-workspace-parallel-prd-sessions-181`

## Scope controls
- Allowed: `term-control-center` frontend components/styles/tests, terminal session lifecycle/launch group/session store/recovery code needed for parallel PRD draft/planner sessions, board-to-terminal launch links only where needed, behavior docs only where needed, run artifacts.
- Forbidden: PRD approval, CEO approval semantics changes, split-screen removal, existing board destination removal, making Kody/Kodus blocking, secrets/raw transcripts/full sensitive logs persistence, PR creation/merge/deploy/trading/backtests.
- Validation: `cd term-control-center && npm run typecheck && npm test && npm run build`; targeted tests per checkpoint when full validation is blocked by pre-existing/env issues.
- Stop condition: final verifier implementation approval plus verifier bug-check approval after steward review, or human escalation.

## Verifier checkpoints
1. Selection checkpoint — terminal selection/autoscroll changes; verify small/large selection preservation and copy snapshot behavior where feasible.
2. Unified layout checkpoint — terminal workspace layout, header, nav compaction, actions menu, pane maximize/restore; split-screen remains intact.
3. Sidebar and notification checkpoint — active jobs sidebar expanded/collapsed states, switching, selected state, attention indicators, accessibility labels.
4. Pipeline/Kody checkpoint — unified pipeline/timeline and `Kodus Review` state mapping; unavailable Kody/Kodus fails safe.
5. Parallel PRD session checkpoint — server/session lifecycle changes; multiple draft/planner sessions coexist and recover.
6. Final regression checkpoint — validation commands/manual QA, no unrelated board/CEO/merge behavior changes.

## Pre-existing worktree state
- `git status --short --branch` before edits: clean (`## prd/unified-terminal-workspace-parallel-prd-sessions-181...origin/main`).
- Ignored local artifacts after validation: `term-control-center/node_modules/`, `term-control-center/dist/`, `pipeline-diagram/__pycache__/`.

## Freshness / research consult
- Researcher consult completed before coding.
- Key guidance recorded: xterm 5.5 exposes `onSelectionChange`, `hasSelection()`, `getSelection()`, `getSelectionPosition()`, `select()`, and scroll APIs; do not call app-level `scrollToBottom()` while dragging or while `terminal.hasSelection()` is true; snapshot selected text and range; browser selection release/cancel can arrive via mouse/pointer/cancel/blur paths and `selectionchange` is async; React 19 terminal state should keep imperative xterm/drag/follow-tail refs outside React state; Kody/Kodus should surface advisory `not started`/`unavailable` when live status is absent and never stale `passed`.

## Checkpoint 1 — Selection implementation summary
- Added an xterm selection lock in `TerminalPane.tsx` that pauses follow-tail while a mouse selection is active or xterm reports a selection.
- `OUTPUT` handling now preserves the pre-write viewport with `scrollToLine(viewportY)` while selection is locked and only auto-scrolls to bottom when replaying or when no selection lock is active and the terminal was already at bottom.
- `terminalSelection.ts` now stores the latest validated selection snapshot in a `WeakMap` keyed by terminal and exposes `preservedTerminalSelection()` so copy actions can fall back to the snapshot if xterm clears the live selection.
- Mouse selection cleanup now handles `pointercancel`, `lostpointercapture`, and window `blur` in addition to document capture `mouseup`.
- Updated existing terminal static coverage for selection lock, snapshot fallback, cancel paths, and no scroll-to-bottom while selecting.

## Changed files
- `term-control-center/src/TerminalPane.tsx`
- `term-control-center/src/terminalSelection.ts`
- `term-control-center/src/terminalTouchSelection.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-181-unified-terminal-workspace/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-181-unified-terminal-workspace/review-request-r1-selection.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-181-unified-terminal-workspace/review-request-r2-selection-fixes.json`

## Validation log
- PASS: `npm --prefix term-control-center ci`
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit`
- PASS: `cd term-control-center && npm run build:client`
- PASS: `cd term-control-center && node --import tsx --test tests/termBasePath.test.ts tests/terminalJobSidebar.test.ts`
- BLOCKED/pre-existing: `npm --prefix term-control-center run typecheck` fails in server config because `tests/contextRenewal.test.ts` imports `../../pi-packages/agentops-context-renewal/lib/policy.ts` outside `rootDir` and without `allowImportingTsExtensions`.
- BLOCKED/pre-existing/env: `npm --prefix term-control-center test` starts but reports unrelated admin/auth/pipeline-generator failures and timed out at 120s; failures include 401/403/201 expectation mismatches in `tests/admin.test.ts` and `ModuleNotFoundError: completed_work` when importing `pipeline-diagram/generate.py` from `term-control-center`.

## Revision 2 fixes for verifier findings
- F-181-SEL-001: Removed the subtract-one coordinate conversion and now preserves xterm selection positions as returned by `getSelectionPosition()` for `terminal.select()` restore. Kept exclusive end-boundary length computation. Added focused static coverage that no `point.x - 1` / `point.y - 1` conversion remains.
- F-181-SEL-002: Added a `settling` selection state so xterm clear events during intentional mouseup restore do not erase the pending snapshot, while later selection-clear events delete the WeakMap snapshot, clear state, and mark copy unavailable.
- F-181-KISS-001: Removed the unused duplicate `copyTerminalSelection` export and now-unused `writeClipboardText` import from `terminalTouchSelection.ts`.

## Revision 2 validation
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/termBasePath.test.ts tests/terminalJobSidebar.test.ts && npm run build:client`
- PASS: `git diff --check`

## Checkpoint 2 — Unified layout/header/action/maximize summary
- Replaced the non-embedded terminal page's full global `TopNav` + `Agent workspace` hero/action row with a compact terminal header.
- Header includes a burger-style terminal nav menu sourced from the existing nav model (`primaryPages`, Activity Center link, and `moreItems`) and removes the project dropdown from the terminal workspace.
- Header identity uses active session/group metadata (`jobTitle`, mode, role summary) with a fallback to launch-group metadata rather than pane title only.
- Session actions (`New pane`, `Split pane`, `Open Browser-QA`, `End session`, split direction, diff, command palette) moved into a compact `Actions` details menu; destructive End Session still calls the existing confirmation-gated route.
- Pane-level maximize/restore control added to each `TerminalPane` toolbar; maximizing sets the clicked pane active and displays only that pane until restore while preserving persisted maximize state and the prior session layout state.
- Updated app/CSS static coverage for compact terminal header, action menu, and per-pane maximize behavior.

## Checkpoint 2 changed files
- `term-control-center/src/App.tsx`
- `term-control-center/src/TerminalPane.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/termBasePath.test.ts`

## Checkpoint 2 validation
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit`
- PASS: `cd term-control-center && node --import tsx --test tests/termBasePath.test.ts tests/terminalJobSidebar.test.ts`
- PASS: `cd term-control-center && npm run build:client`
- PASS: `git diff --check`

## Checkpoint 2 revision 2 fix
- F-181-LAYOUT-001: `TerminalArea()` now routes `maximized` through `FocusedPaneStack`, so the standard two-pane coder/verifier workspace shows only the active/maximized pane instead of leaving the Allotment split visible. Static coverage now asserts both the TerminalArea branch and the visible-pane guard include maximized mode.
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/termBasePath.test.ts tests/terminalJobSidebar.test.ts && npm run build:client && git diff --check`

## Checkpoint 2 revision 3 fix
- F-181-LAYOUT-002: `AllotmentShell()` now short-circuits maximized mode to the terminal-only view before browser or diff split wrappers, preserving `browserOpen`/`diffOpen` state for restore without sharing maximized terminal space.
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/termBasePath.test.ts tests/terminalJobSidebar.test.ts && npm run build:client && git diff --check`

## Checkpoint 3 — Sidebar and notification summary
- Added desktop sidebar collapse/expand state while keeping the active jobs sidebar visible by default in non-compact split-screen terminal workspace.
- Collapsed sidebar keeps clickable job rows with a short PRD/draft/group identifier and attention indicator; expanded rows retain full title, status, mode/type, role summary, and time.
- Added accessible labels/titles for job rows and collapse/expand controls.
- Added attention mapping from existing local group/pane state: red `issue` for group error/stale/unrecoverable pane/error pane, green `human` for `waiting_for_review` or `revision_requested`; red issue state takes priority.
- Added focused static coverage for collapse controls, short IDs, accessible labels, attention priority, and pulse styling.

## Checkpoint 3 changed files
- `term-control-center/src/App.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/terminalJobSidebar.test.ts`

## Checkpoint 3 validation
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts && npm run build:client && git diff --check`

## Checkpoint 4 — Pipeline/Kody summary
- Added a compact `PipelineTimeline` to the terminal header for the selected active job/session.
- Implementation jobs render `Implement`, `PR`, `Kodus Review`, `Merge`, `Sync Main`, `Code Review`, and `Done` steps.
- PRD planning/authoring/review jobs render an adapted authoring pipeline (`Plan`, `Author`, `CEO Review`, `Done`) within the same terminal header component.
- `Kodus Review` uses a fail-safe `unavailable` state with tooltip text when no live Kody/Kodus status exists; it never defaults to stale success.
- Pipeline state recomputes from the selected active group/launch group so switching jobs updates the timeline with the same metadata source as the identity header.
- Added static coverage for supported pipeline states, required step names, `Kodus Review` unavailable fallback, and compact header styling.

## Checkpoint 4 changed files
- `term-control-center/src/App.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/termBasePath.test.ts`

## Checkpoint 4 validation
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts && npm run build:client && git diff --check`

## Checkpoint 4 verifier status
- Approved after verifier context reset.

## Checkpoint 5 — Parallel PRD draft/planner sessions summary
- Changed draft/planner replacement logic so `replaceDraftAuthoringGroups()` only targets the same logical draft/session via `sameTask()` instead of all draft groups sharing worktree and branch.
- This preserves unrelated draft/planner or draft/authoring sessions that share the configured authoring worktree/branch while still replacing the prior planning group when the same draft launches downstream authoring.
- Updated server coverage: a second draft planning launch now leaves the first draft authoring group running and verifies both distinct draft IDs remain present.
- Chosen isolation model: session-state isolation by unique draft ID is sufficient for current implementation scope because launch groups, panes, tmux sessions, task context files, and browser attach metadata are keyed by group/session IDs. This checkpoint did not find product artifact writes that require creating per-draft worktrees before authoring; if future PRD subagents write shared repo artifacts, that should trigger a bounded per-draft workspace design.
- Open PRD discovery answers: cleanup/replacement now targets same draft/session only; launch/recovery/reuse uses `sameTask()` including draft ID and project; subagents remain attached through group pane/session IDs.

## Checkpoint 5 changed files
- `term-control-center/server/index.ts`
- `term-control-center/tests/server.test.ts`

## Checkpoint 5 validation
- PASS: `cd term-control-center && node --import tsx --test --test-name-pattern 'parallel draft PRD Studio launches keep unrelated draft authoring groups|starts pre-issue PRD planning drafts as Planner only|PRD planning execute fails closed' tests/server.test.ts`
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts && npm run build:client && git diff --check`
- BLOCKED/pre-existing: `cd term-control-center && npx tsc -p tsconfig.server.json --noEmit` still fails because `tests/contextRenewal.test.ts` imports `../../pi-packages/agentops-context-renewal/lib/policy.ts` outside `term-control-center` rootDir and without `allowImportingTsExtensions`.

## Checkpoint 6 — Final regression validation summary
- Full required commands attempted.
- `npm --prefix term-control-center run typecheck` and `npm --prefix term-control-center run build` remain blocked by the pre-existing server typecheck issue in `tests/contextRenewal.test.ts` importing a `.ts` file outside `term-control-center` rootDir.
- `npm --prefix term-control-center test` was run for 180s and reached 481 subtests before timeout; many tests passed, while unrelated/pre-existing failures appeared in admin/auth/project action/server launch fixtures. The new parallel draft test passed as subtest 451.
- Focused validation for changed surfaces passes as recorded above.
- No PR/merge/deploy/CEO approval/trading/backtest behavior was changed.

## Final validation log
- FAIL/pre-existing: `npm --prefix term-control-center run typecheck` — `tests/contextRenewal.test.ts` imports `../../pi-packages/agentops-context-renewal/lib/policy.ts` outside rootDir and without `allowImportingTsExtensions`.
- FAIL/pre-existing: `npm --prefix term-control-center run build` — fails at the same typecheck blocker before client/server build.
- FAIL/pre-existing/timeout: `npm --prefix term-control-center test` — timed out after 180s; unrelated failures include admin/auth expectation mismatches, pipeline generator import path issue, project action config expectation, and server fixture launch validation mismatches. Relevant changed-surface tests passed, including subtest 451 for parallel draft sessions.
- PASS: `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit`
- PASS: `cd term-control-center && node --import tsx --test tests/terminalJobSidebar.test.ts tests/termBasePath.test.ts`
- PASS: `cd term-control-center && node --import tsx --test --test-name-pattern 'parallel draft PRD Studio launches keep unrelated draft authoring groups|starts pre-issue PRD planning drafts as Planner only|PRD planning execute fails closed' tests/server.test.ts`
- PASS: `cd term-control-center && npm run build:client`
- PASS: `git diff --check`

## Post-human localhost selection fix
- Human localhost QA reported terminal selection still selected smaller areas than intended.
- Bounded fix: `terminalSelection.ts` now remembers selection snapshots during mouse drag/settling without setting copy-ready or showing the copy popover until the release/settle path. This avoids the floating copy/paste menu appearing during an active drag and interfering with the intended selection range.
- Validation: PASS `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && node --import tsx --test tests/termBasePath.test.ts && npm run build:client && git diff --check`.

## Manual QA / risks
- Manual browser QA remains not completed by coder.
- Attempted local preview setup is recorded in `dev-plans/agentops/coder-verifier-workflow/runs/issue-181-unified-terminal-workspace/manual-qa/manual-qa-blocker.md`.
- Safe-stop reason: controlled `npm run dev:fake` did not become ready due a local `tsx` IPC `EADDRINUSE`, and port `3032` was already owned by a long-running backend not started for this checkpoint. I did not open the UI against that backend because default terminal panes could create/attach real sessions instead of isolated QA evidence.
- Human/operator preview is required for selection/copy, active-output selection, sidebar collapse/switching/attention, pane maximize/restore, pipeline/Kodus unavailable state, and two parallel draft sessions.
- Verifier checkpoint 6 revision 2 verdict: `needs_human` for `F-181-FINAL-001`; next actor is human.
- Selection behavior still relies on xterm public APIs; no raw terminal output or transcripts were persisted.
