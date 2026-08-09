# Coder Handoff — Issue #218 Terminal Scrollback, Selection, and Copy Stability

## Scope
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/218
- Branch: `prd/terminal-selection-stability-218`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-218`
- Pre-existing dirty files before editing: none (`git status --short --branch` clean)

## Allowed / forbidden / stop condition
- Allowed: terminal pane output/pinning path, selection/touch/clipboard/jump modules, tmux mouse/copy-mode configuration when research supports it, focused tests, terminal-interaction docs, and this run artifact folder.
- Forbidden: replay/ACK protocol semantics beyond pinning, scrollback-depth reduction, wholesale tmux mouse disablement without research evidence, non-explicit clipboard access, terminal-content persistence/logging, product routes/navigation/chrome redesign, PR/merge/deploy/approval/trading/backtest actions.
- Stop condition: final verifier bug-check approval, or human escalation for an out-of-scope/blocked decision.

## Checkpoints
1. Root-cause resolution design with research-backed tmux/xterm choice (FR-4) — approved at revision 2; V218-CP1-001 resolved.
2. Desktop selection and scroll-held behavior (AC-1–AC-3, AC-5) — implemented; review pending.
3. Touch selection and explicit copy behavior (AC-4, FR-9–FR-11) — pending.
4. Robustness/regressions across split/maximized views (AC-6–AC-8) — pending.
5. Steward hygiene review, then final verifier bug-check for replay/selection races, ACK safety, indicator edges, and scrollback performance — pending.

## Researcher consults
Mandatory freshness consults completed 2026-07-14 through the local researcher peer before implementation.

1. xterm.js/tmux selection design
   - Use xterm’s documented forced-selection gesture instead of host-level bare left-drag interception: Shift+drag on non-macOS and Option+drag with `macOptionClickForcesSelection: true` on macOS. The forced gesture suppresses PTY mouse events while preserving ordinary tmux/TUI mouse interaction.
   - Keep tmux `mouse on`; do not remove its bindings wholesale. Repair `WheelUpPane` in this exact order: (1) if `#{pane_in_mode}`, scroll up in existing copy mode; (2) otherwise if `#{mouse_any_flag}`, forward the wheel with `send-keys -M`; (3) otherwise enter copy mode and scroll up. This preserves both copy-mode scrollback and TUI wheel interaction.
   - Evidence: xterm 5.5.0 option/API and source (https://xtermjs.org/docs/api/terminal/interfaces/iterminaloptions/, https://github.com/xtermjs/xterm.js/blob/5.5.0/src/browser/services/SelectionService.ts, release 2024-04-05); tmux FAQ/recipe (https://github.com/tmux/tmux/wiki/FAQ#i-want-to-use-the-mouse-to-select-panes-but-the-terminal-to-copy-how, https://github.com/tmux/tmux/wiki/Recipes#send-up-and-down-keys-for-the-mouse-wheel; FAQ updated 2026-04-16).
2. iOS/iPadOS Safari clipboard
   - Call `navigator.clipboard.writeText(selectedText)` synchronously from the explicit Copy button’s user gesture. Do not defer it before its first call; prevent duplicate writes while pending.
   - On absent/rejected clipboard access, keep the explicit affordance and show a visible failure/native-copy fallback rather than failing silently. The existing asynchronous `execCommand` fallback after a rejection is not activation-reliable on Safari.
   - Evidence: WebKit Async Clipboard announcements (https://webkit.org/blog/10247/new-webkit-features-in-safari-13-1/, 2020-04-03; https://webkit.org/blog/10855/async-clipboard-api/, 2020-06-23) and User Activation API (https://webkit.org/blog/13862/the-user-activation-api/, 2023-02-15).

## Checkpoint 1 design
- Replace the current manual bare-left-button selection tracking with xterm-driven selection observation plus the documented forced-selection modifier. The selection lock begins on that modifier’s mouse-down and ends after mouse-up/selection settlement; touch selection receives the same lock callback for its active long-press selection interval.
- Treat a pane as held when selection is active or when it was already away from the bottom. For every live or replayed output write, snapshot `viewportY`, restore it when held, and pin only when the prior viewport was at bottom with no active selection. ACK behavior remains exactly non-replay only.
- Preserve the hold through resize reflow by snapshotting/restoring a held viewport around fitting; do not change protocol/replay payloads.
- Extend the current jump button into the scroll-held affordance: announce new output below while held, remain keyboard-accessible, and clear held/new-output state only through the explicit jump action.
- Retain one-finger touch scrolling; long press enters touch selection and blocks its competing scroll gesture only while selecting. Explicit Copy reports success/failure and serializes duplicate taps.
- Add a focused tmux binding assertion covering all three `WheelUpPane` branches in order: existing `pane_in_mode` copy-mode scroll, then `mouse_any_flag` application forwarding, then copy-mode entry/scroll fallback.
- Change only the focused terminal modules, tmux wheel binding, focused tests, styles needed for the affordance/touch target, and this run folder.

## Revision 2 research and fixes
- A focused researcher consult for V218-CP2-004 recommends browser-local Alt/Option+wheel scrolling, returning `false` from xterm’s custom wheel handler after `scrollLines`. Unmodified wheel remains xterm → tmux; tmux forwards it only to a TUI that has `mouse_any_flag`. The former no-TUI branch no longer enters invisible tmux copy mode. Source: xterm 5.5 Terminal/Viewport APIs and tmux recipe (https://xtermjs.org/docs/api/terminal/classes/terminal/, https://github.com/xtermjs/xterm.js/blob/5.5.0/src/browser/Terminal.ts, https://github.com/xtermjs/xterm.js/blob/5.5.0/src/browser/Viewport.ts, https://github.com/tmux/tmux/wiki/Recipes#send-up-and-down-keys-for-the-mouse-wheel).
- Addressed V218-CP2-001: exact `viewportY >= baseY` bottom semantics; live and replay one-line-up behavior is tested.
- Addressed V218-CP2-002: hold/pin intent is determined in the asynchronous write callback, so an operator scroll/jump between enqueue and completion wins; delayed tests assert both directions and live ACKs.
- Addressed V218-CP2-003: explicit jump clears xterm selection before returning to bottom, so the next write can resume pinning.
- Addressed V218-CP2-004: the supported desktop read path is Alt/Option+wheel local xterm scrolling; the indicator and jump now observe/control that path. Tmux retains copy-mode wheel scrolling only when already in manually entered copy mode and forwards normal wheel to active TUIs.
- Addressed V218-CP2-005: Meta/Ctrl menu handling now precedes forced-selection gating.
- Addressed V218-CP2-006: the output fixture uses a compact state object rather than a five-parameter helper.

## Changed files
- `term-control-center/src/terminalOutput.ts` — new, focused output hold/pin helper; replay follows the same callback-time hold rule and preserves non-replay-only ACKs.
- `term-control-center/src/terminalReadScroll.ts` — explicit Alt/Option browser-local reading gesture that preserves unmodified TUI wheel input.
- `term-control-center/src/TerminalPane.tsx` — wires output helper/new-output state, xterm forced selection on macOS, held resize restoration, and the labelled jump affordance.
- `term-control-center/src/terminalSelection.ts` — starts desktop selection tracking only for xterm’s forced modifier gesture.
- `term-control-center/src/terminalJumpToBottom.ts` — clears new-output state when the operator returns to bottom.
- `term-control-center/server/tmuxSupervisor.ts` — preserves existing copy-mode scrolling, then TUI mouse forwarding, then copy-mode entry for WheelUp.
- `term-control-center/src/styles.css` — makes the jump affordance at least 44px.
- `term-control-center/tests/terminalScrollHold.test.ts` — scripted live/replay output hold/pin tests.
- `term-control-center/tests/termBasePath.test.ts` — asserts the three-way tmux order and new terminal contracts.

## Validation
- PASS: `npm --prefix term-control-center run typecheck` using a temporary symlink to the existing shared dependency tree; removed after the command.
- PASS: `npm --prefix term-control-center run build:client` using the same temporary dependency symlink; Vite emitted only its existing non-module script and chunk-size warnings.
- PASS: focused terminal tests (34/34): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: ephemeral tmux 3.4 server accepted the actual `WheelUpPane` binding and rendered the intended copy-mode → TUI-forward → no-op nested `if`; server was removed after validation.
- PASS: `git diff --check`.
- INCOMPLETE: `npm --prefix term-control-center run test` first could not resolve `tsx` because this worktree intentionally has no local `node_modules`; rerun against the temporary shared dependency symlink ran without failures through test 211 but exceeded the 300-second command timeout before a final suite result.
- Required manual QA to record: desktop Chrome/Safari and iPad/iPhone Safari; scroll/read, select/copy during streaming, reconnect/replay, jump-to-bottom, split/maximized.

## Human escalation
Verifier checkpoint 2 revision 2 returned `needs_human`; implementation is stopped before touch, robustness, steward, and final bug-check work.

- `V218-CP2-002`: preserving a selection that began at the old bottom needs a generation-based mutable view-intent controller. The write callback runs after xterm advances its buffer/viewport, while callback-only state is necessary to honor a later scroll or jump.
- `V218-CP2-004`: the PRD’s no-regression clause does not authorize replacing ordinary shell wheel scrolling with Alt/Option+wheel without a human UX/requirements decision. A browser-local held indicator cannot truthfully represent tmux copy-mode state; preserving the normal path requires a larger approved design.
- `V218-CP2-007`: split the 22-line terminal test fixture if a further revision is authorized.
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-218-terminal-selection-stability/verifier-report.md`.

## Human authorization
On 2026-07-14, the operator authorized one additional bounded revision: retain normal wheel behavior, add the minimal tmux copy-mode state bridge needed for truthful held/jump state, implement the generation-based view-intent controller, and split the test fixture. This authorization permits the small scroll-state client/server contract but does not authorize replay/ACK semantic changes, PR/merge/deploy, or other excluded actions.

### Authorized revision implementation
- Added the `SCROLL_STATE`/`SCROLL_RESET` bounded protocol plumbing and tmux monitor wiring for copy-mode state.
- Added generation-based `ViewIntent` capture in terminal output, local scroll, selection, and jump paths.
- Restored ordinary WheelUp tmux copy-mode entry after the active-copy-mode and active-TUI branches.
- PASS: typecheck and focused terminal suite (34/34); `git diff --check` passes.

### Authorized revision follow-up (checkpoint 2, revision 5)
- Addressed `V218-CP2-002`: output writes now mark the persistent view-intent controller as writing. Passive xterm/DOM scroll observers use `recordScrollIntent`, which ignores output-caused scroll events until the write callback settles. Explicit selection, Alt/Option reading scroll, and jump actions retain direct intent generations, so later operator scroll/jump intent still wins.
- Addressed `V218-CP2-004`: `terminalHeldState.ts` now composes independent local/tmux held and new-output sources. `SCROLL_STATE` includes `newOutput`; tmux monitoring reports activity that arrives after entering copy mode. The client jump action clears both sources, performs local jump/selection clear, and sends `SCROLL_RESET`; the server exits copy mode and broadcasts the reset state immediately.
- Retained normal tmux WheelUp behavior: existing copy-mode scroll, active-TUI forwarding, then first-wheel copy-mode entry and scroll. No Alt/Option-only replacement applies.
- Addressed `V218-CP2-007`: removed the dead `MessageDeps` type, changed jump helpers to a cohesive callbacks object, and split the output test setup into small fixture helpers.
- Added intent-generation coverage for output scroll during selection-at-bottom, later user scroll, later jump, local/tmux state union, and tmux-held activity/new-output transitions.

### Revision 5 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral symlink to the shared dependency tree, removed after the command.
- PASS: focused terminal tests (38/38): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `git diff --check`.
- FAIL / human gate: verifier checkpoint 2 revision 5 returned `needs_human` with `V218-CP2-002`, `V218-CP2-004`, and `V218-CP2-008` open. The verifier report is the controlling detail. The retry/research budget is exhausted, so no further implementation is authorized.

### Human decision required
- `V218-CP2-002`: authorize a narrowly bounded distinction between output/programmatic scroll notifications and a real passive xterm scrollbar/trackpad scroll while a write is pending; current write guard correctly preserves selection but suppresses all passive scroll observations during output.
- `V218-CP2-004`: authorize the entry-interval sampling semantics for tmux copy-mode activity or a bounded repair that sets new-output when copy-mode entry and activity occur in the same monitor interval.
- `V218-CP2-008`: authorize the requested small KISS extraction: split `startTerminal`, convert the test options helper to one cohesive fixture/options input, and move checkpoint contract assertions out of the legacy catch-all test file.
- Touch, robustness, steward, final bug-check, full-suite conclusion, and manual device matrix remain pending until a human resolves this checkpoint decision.

### Operator-authorized checkpoint 2 revision 6
- Operator instructed continuation after the revision-5 human gate. Scope remains only `V218-CP2-002`, `V218-CP2-004`, and `V218-CP2-008`.
- Addressed `V218-CP2-002`: passive scroll tracking now records an operator-origin marker from viewport wheel, pointer, touch, or keyboard input. The output-write guard still rejects unmarked output/programmatic scroll events, while a marked passive local scroll is recorded as the later view intent. Tests exercise both the output observer and passive-operator path while output is pending.
- Addressed `V218-CP2-004`: tmux activity observed in the same poll that first reports copy mode now sets `newOutput`; this deliberately favors a truthful “new output below” indication over the harmless possibility that copy-mode entry coincides with unrelated pane activity. Tests cover the combined entry/activity transition and reset state.
- Addressed `V218-CP2-008`: extracted interaction setup into focused `terminalInteractions.ts`; `startTerminal` is now a small constructor, output test options are cohesive, and the new scroll contract assertions live in `terminalScrollContract.test.ts` rather than the legacy catch-all test.

### Revision 6 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (40/40): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build:client` (existing non-module script and chunk-size warnings only).
- PASS: `git diff --check`.
- Revision 6 verifier response: `revision_requested`; `V218-CP2-004` is resolved. `V218-CP2-002`, reopened `V218-CP2-007`, and `V218-CP2-008` received the bounded revision below under recorded continuation authorization.

### Checkpoint 2 revision 7
- Addressed `V218-CP2-002`: operator provenance is now gesture-scoped instead of one-shot. Alt/Option wheel and touch movement retain the marker through the gesture; native scrollbar dragging is marked only when pointer input begins in the scrollbar band and clears on pointer end/cancel. Output notifications never consume the marker, so a later user event records the final position. Tests cover output between two passive user scroll positions while a write is pending.
- Addressed `V218-CP2-007`: reduced `terminalFixture` below 20 physical lines.
- Addressed `V218-CP2-008`: restored `termBasePath.test.ts` below its 434-line baseline by moving checkpoint-specific output, wheel, selection, and read-scroll assertions to `terminalScrollContract.test.ts`. Converted `cleanup` to a single cohesive `TerminalCleanup` options object.

### Revision 7 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (43/43): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build:client` (existing non-module script and chunk-size warnings only).
- PASS: `git diff --check`.
- Revision 7 verifier response: `revision_requested`; `V218-CP2-007` and `V218-CP2-008` are resolved. One bounded continuation revision was authorized for `V218-CP2-002`.

### Checkpoint 2 revision 8
- Addressed `V218-CP2-002`: separated gesture lifetime from per-scroll provenance. User input queues `recordUser` after native scrollbar pointer movement or touch movement; only this path writes an operator view intent. Terminal/DOM scroll notifications always use `recordPassive`, which is ignored while an output write is active. Consequently output after the user’s final scroll cannot inherit a gesture flag or overwrite their held viewport.
- Native scrollbar drags now use pointer capture and document-level pointer-up/cancel cleanup, so release outside the viewport clears the gesture safely.
- `createScrollObserver` is exported only as the focused controller seam and is exercised by a test that performs final user intent followed by output passive scroll while writing; the held intent remains at the user’s line.

### Revision 8 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (44/44): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build:client` (existing non-module script and chunk-size warnings only).
- PASS: `git diff --check`.
- FAIL / human gate: verifier checkpoint 2 revision 8 returned `needs_human` with `V218-CP2-002` open. The controlling report records that the three authorized bounded continuation repairs and prior research budget are exhausted; no further implementation is authorized.

### Human decision required after revision 8
- Choose either: (1) authorize one further narrow repair plus behavioral input-mapping test for native scrollbar track/arrow clicks during streaming, or (2) explicitly re-scope/accept the documented limitation and record pointermove scrollbar drag, Alt/Option local wheel, and tmux wheel as the supported desktop read paths.
- The unresolved path is a native scrollbar track/arrow click that scrolls without `pointermove`: the passive observer correctly suppresses output-induced scroll while writing but therefore cannot identify that click as operator intent. Drag provenance, final-user-position preservation, pointer release cleanup, tmux bridge/wheel/reset, and all KISS findings are approved by the verifier.
- Touch, robustness, steward, final bug-check, full-suite conclusion, and manual device matrix remain pending until the human resolves checkpoint 2.

### Operator-authorized checkpoint 2 revision 9
- Operator authorized one narrow repair and behavioral test for native scrollbar track/arrow clicks during streaming.
- `pointerdown` in the scrollbar band now queues the same next-frame explicit user-intent snapshot as drag/touch movement. A pure `createScrollGesture` controller accepts an injected scheduler; the focused behavioral test executes a track click with no `pointermove`, applies the native viewport movement before the queued frame, then applies passive output scroll. The recorded held line remains the operator’s line.
- Pointer capture plus document-level release/cancel remains intact; output scroll remains passive and cannot inherit a user provenance flag.

### Revision 9 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (44/44): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build:client` (existing non-module script and chunk-size warnings only).
- PASS: `git diff --check`.
- Revision 9 verifier response: functional `V218-CP2-002` is resolved. Verifier requested only `V218-CP2-009` KISS cleanup.

### Checkpoint 2 revision 10
- Addressed `V218-CP2-009`: replaced the five-position-argument scrollbar helper with a three-argument helper receiving one cohesive gesture context object. Behavior is unchanged.

### Revision 10 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (44/44): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `git diff --check`.
- Checkpoint 2 revision 10 verifier result: `approved` (no open findings). The full report was not read after approval.

### Checkpoint 3 implementation — touch selection and copy
- Touch long-press selection now shares the desktop selection lock: entering touch selection records held local intent before selecting; leaving it recomputes held state from the retained xterm selection. One-finger move still cancels pending long press and retains native scroll behavior; active selection still prevents competing touch scroll.
- The explicit Copy control now reports a visible status if clipboard write plus the existing native fallback fails, rather than failing silently. Clipboard access remains only on the operator’s explicit Copy action.

### Checkpoint 3 validation
- PASS: `npm --prefix term-control-center run typecheck` with an ephemeral shared dependency symlink, removed after validation.
- PASS: focused terminal tests (44/44): `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/terminalScrollHold.test.ts term-control-center/tests/terminalHeldState.test.ts term-control-center/tests/terminalScrollContract.test.ts term-control-center/tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build:client` (existing non-module script and chunk-size warnings only).
- PASS: `git diff --check`.
- Revision 3 additions: executable `terminalTouchSelectionEvents.test.ts` drives pending-move cancellation, long-press lock ordering, active scroll prevention, touch end retention, held-output composition, and edge auto-scroll. Clipboard fallback cleanup is asserted on thrown fallback paths.
- PASS: typecheck; focused full checkpoint set 52/52; `git diff --check` passes.
- Revision 5: extracted retained-selection test harness; all executable touch test callbacks are below 20 lines. Typecheck and touch tests (5/5) pass.
- Checkpoint 3 verifier result: approved at revision 5. Required manual iPad/iPhone Safari validation remains pending for final validation.

## Checkpoint 4 implementation — robustness and regressions
- Added `term-control-center/tests/terminalRobustness.test.ts` to verify independent held/pinned output behavior for two split panes at the 50,000-line boundary, replay preservation without ACK, and that maximized/mobile focused layouts hide rather than replace the keyed terminal pane instances.
- Existing focused coverage continues to cover the wheel/TUI ordering, read-scroll behavior, selection/replay hold, output ACK flow, and touch/copy paths; no protocol, tmux, or production behavior changed in this checkpoint.

## Checkpoint 4 validation
- PASS: `npm --prefix term-control-center run typecheck`.
- PASS: `npm --prefix term-control-center run build`; existing Vite non-module-script and chunk-size warnings only.
- PASS: focused checkpoint suite, 55/55: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/terminalScrollHold.test.ts tests/terminalHeldState.test.ts tests/terminalScrollContract.test.ts tests/terminalTouchSelectionEvents.test.ts tests/terminalClipboardCopy.test.ts tests/terminalRobustness.test.ts tests/termBasePath.test.ts`.
- PASS: `git diff --check`.
- BLOCKED (pre-existing test harness behavior, no issue #218 edit): `npm --prefix term-control-center run test` was rerun with the shared `node_modules` symlink. It passed through test 211 (`coworkerGuard.test.ts`) but did not terminate after 900 seconds. Running `coworkerGuard.test.ts` alone reproduces that post-pass non-termination after its two passing assertions; `git show origin/main:term-control-center/tests/coworkerGuard.test.ts` and `server/index.ts` show the same code, so this is baseline and outside the allowed terminal scope. `coworkerLauncher.test.ts`, the next lexical file, passes alone (4/4).

### Checkpoint 4 revision 2
- Addressed `V218-CP4-001`: `TerminalArea` now retains one keyed `Allotment` tree in split, maximized, focused, and phone layouts. Pane visibility changes through Allotment’s `visible` property instead of replacing the `PaneSlot`/`TerminalPane` parent tree, preserving xterm/socket ownership while retaining resizable split behavior.
- Addressed `V218-CP4-002`: the robustness test now writes live and replayed 50,000-line payloads while a selection is active. It asserts the held viewport, non-replay-only ACK, and a constant two terminal writes/restores rather than treating fake-terminal wall-clock time as xterm responsiveness proof. Actual device/browser responsiveness remains pending manual QA.
- Addressed `V218-CP4-003`: verifier ran the 75-file suite excluding the non-terminating `coworkerGuard.test.ts`: 636/638 pass. The two failures reproduce on `origin/main` and are baseline environment/configuration expectations: Browser-QA `missing_allowed_target`, and recovered-model `codex-default` versus configured `codex-gpt-5-6-luna`.
- Addressed `V218-CP4-004`: removed the temporary `term-control-center/node_modules` symlink after validation; it is not an untracked worktree artifact.

### Checkpoint 4 revision 2 validation
- PASS: `npm --prefix term-control-center run typecheck` using a temporary shared dependency symlink, removed afterwards.
- PASS: `npm --prefix term-control-center run build` using the same temporary symlink; existing Vite warnings only.
- PASS: focused checkpoint suite 55/55, including split/focused ownership and 50k selected live/replay coverage.
- PASS: `git diff --check`.

### Checkpoint 4 revision 3
- Addressed the remaining `V218-CP4-001`: `TerminalWorkspace` now always renders one `term-workspace-shell` ancestor with stable `JobSidebar` and `AllotmentShell` child positions. Compact/maximized mode changes the shell class and sidebar `hidden` attribute rather than returning a different root, preserving the terminal subtree through desktop split → maximized and desktop → phone transitions.
- Addressed `V218-CP4-005`: robustness fixture helpers now take cohesive context objects rather than five positional arguments.
- Addressed `V218-CP4-006`: removed obsolete focused-layout CSS selectors and assertions; live layout validation now covers the stable compact workspace shell and Allotment visibility.

### Checkpoint 4 revision 3 validation
- PASS: `npm --prefix term-control-center run typecheck` using a temporary shared dependency symlink, removed afterwards.
- PASS: `npm --prefix term-control-center run build` using the same temporary symlink; existing Vite warnings only.
- PASS: focused checkpoint suite 55/55, including the outer workspace-ancestor transition regression.
- PASS: `git diff --check`.

### Checkpoint 4 revision 4
- Addressed `V218-CP4-007`: phone mode now selects the stable single-column workspace class while leaving the mobile Jobs drawer mounted. The compact selector now matches the collapsed-sidebar selector specificity and follows it, so hidden/collapsed Jobs state cannot constrain the terminal to a sidebar-width column.
- PASS: typecheck and the affected layout/robustness suite (34/34) with the temporary shared dependency symlink removed afterwards; `git diff --check` passes.
- Checkpoint 4 verifier result: approved at revision 4.
- Steward hygiene review: changed-file placement and run-artifact scope are clean. Removed generated `term-control-center/build/` and `term-control-center/dist/`; left unrelated pre-existing ignored `pipeline-diagram` outputs untouched. `git diff --check` passes.

## Final bug-check revision 4 fixes
- Addressed remaining `BC218-003`: desktop Browser/Diff sidecars retain a two-column grid and horizontal resize affordance; the existing phone/coarse media query now stacks the stable terminal and exclusive sidecar into two usable rows with 14rem minimums. Browser focus uses one row, and maximize continues to suppress the sidecar without remounting the terminal child.
- Added focused contracts for desktop Browser/Diff exclusivity, phone/coarse stacked rows, Browser focus, maximize, and retained terminal identity.
- PASS: typecheck; focused final-fix suite 38/38; `git diff --check`; temporary dependency symlink removed.
- Steward recheck found only the obsolete `.browser-hidden-terminal[hidden]` selector; removed it. Artifact scope remains clean; no build/dist/node_modules output.
- Final verifier bug-check revision 4: implementation and hygiene findings are clean (65/65 focused verifier suite). `V218-MANUAL-001` is a true human gate: the required Chrome, Safari, iPad Safari, and iPhone Safari manual matrix remains unexecuted in this environment.

## Final bug-check revision 3 fixes
- Addressed `BC218-003`: stable terminal shell now uses explicit two-column CSS grid sizing for one exclusive Browser-or-Diff sidecar. Browser focus becomes a one-column grid with only the terminal view hidden; maximized mode returns no sidecar while retaining the terminal child.
- Addressed `V218-FINAL-001`: removed the test-only always-true broadcast helper. The monitor broadcasts directly on every poll; the executable contract confirms unchanged re-entry state, direct broadcast, and no deduplication helper.
- PASS: typecheck; focused final-fix suite 37/37; `git diff --check`; temporary symlink removed.

## Final bug-check revision 2 fixes
- Addressed `BC218-001`: tmux monitor now broadcasts the current scroll state on every poll, rather than suppressing equal cached states. A reset followed by a quick copy-mode re-entry and a newly attached client both receive the next current-state broadcast even when the session cache is unchanged.
- Addressed `BC218-002`: `AllotmentShell` retains `TerminalArea` in one stable shell-pane position while browser, browser focus, diff, and maximize visibility change around it. It no longer switches terminal ancestors through BrowserShell or diff Allotment branches.
- Added focused delivery/re-entry and outer-shell continuity assertions; updated live layout contracts.
- PASS: `npm --prefix term-control-center run typecheck` with a temporary shared dependency symlink removed after validation.
- PASS: focused final-fix suite 37/37 (`terminalHeldState`, `terminalRobustness`, `termBasePath`).
- PASS: `git diff --check`.

## Required manual QA matrix
- Desktop Chrome: pending manual operator evidence — scroll-up read; select/copy during streaming; reconnect/replay; jump-to-bottom; split and maximized.
- Desktop Safari: pending manual operator evidence — same matrix.
- iPad Safari: pending manual operator evidence — one-finger scroll; long-press selection; explicit copy; streaming/replay; jump; split/maximized/pane switch.
- iPhone Safari: pending manual operator evidence — same touch matrix.
- This execution environment has no attached Safari/iPad/iPhone device session. No manual result is claimed; final approval must not treat the matrix as complete without operator/device evidence.

## Notes / risks
- Coms isolation preflight: `PI_COMS_DIR=/tmp/agentops/coms/agentops-prd-218`; current pool contains live `researcher`, `steward`, and `verifier` roles. This pane is launched as the `coder` role in the `agentops-prd-218` worktree.
- Memory is disabled and not used; current PRD, repository, GitHub state, and verifier evidence take precedence.

## 2026-07-19 coder reactivation — source-state gate
- Context brief: `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-218-47c15734d86e/artifacts/project-context-brief.md` (read; no skip).
- Canonical PRD reread: GitHub issue #218 via authenticated REST `gh api`; issue remains open/approved while its implementation status is stale.
- Worktree/branch: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-218` on `prd/terminal-selection-stability-218`; pre-edit status was clean. `HEAD` (`a7618c6`) is two commits ahead of and has no file diff from `origin/main` (`4bbc753`); its merge-base is `origin/main`. `c443d34` is not an ancestor of `origin/main`: it is the non-main parent of the local refresh merge `a7618c6`. Equal trees do not establish historical ancestry. This is no longer the stale divergent tree described in the context brief, but the brief's lifecycle and device-QA human gates remain unresolved.
- Allowed paths remain only the PRD terminal modules/tests/docs and this run folder. Forbidden paths/actions remain product chrome redesign, replay/ACK changes beyond pinning, scrollback reduction, session/persistence/auth changes, non-explicit clipboard access, GitHub mutation, PR/merge/deploy/approval/trading/backtest. Stop condition remains final verifier approval after the mandatory physical QA evidence, or human escalation.
- Checkpoints: source-state/lifecycle gate; existing checkpoints 1–4 and code final bug-check are historically approved; only the required human browser/device acceptance gate remains. No code checkpoint is authorized without a newly reproduced bounded defect and a human lifecycle decision.
- Touched files this reactivation: `dev-plans/agentops/coder-verifier-workflow/runs/issue-218-terminal-selection-stability/coder-handoff.md` only. No product code, tests, routes, navigation, deployment, generated output, or transcripts changed.
- Implementation summary/acceptance coverage: no new implementation. Existing verifier evidence records all automated AC coverage and a clean code bug-check; AC-1–AC-3 and AC-5–AC-9 remain covered by focused automated evidence. AC-4 and the physical portions of AC-6–AC-7 remain pending the required Chrome/Safari/iPad Safari/iPhone Safari matrix (`V218-MANUAL-001`).
- Commands/results: `git status --short --branch` clean before this artifact edit; `gh api repos/hyperbotsx/agentops-harness/issues/218` retrieved the canonical PRD; `git rev-parse`, `git merge-base`, `git rev-list --left-right --count`, `git show -s --format=%P HEAD`, `git merge-base --is-ancestor c443d34 origin/main` (non-zero), and `git diff --stat origin/main...HEAD` establish the source-state facts above. No product validation was rerun because no implementation change is permitted or made.
- Skipped checks/reason: focused/full automated suites and device/browser QA were not rerun in this reactivation; the former have no code delta, and the latter requires unavailable real Chrome/Safari/iPad/iPhone operator evidence. No result is claimed for the manual matrix.
- Known risks/human decision: issue lifecycle disagrees with merged implementation history, and `V218-MANUAL-001` remains a non-bypassable acceptance gate. A human must choose closeout/manual QA against current main or authorize a fresh, narrowly reproduced follow-up; code must not be reimplemented from the existing PRD alone.
- Cleanup: no temporary symlink, tmux server, build/dist, node_modules link, screenshot, log, or terminal content was created. Bounded standards exception: none.
- Isolation preflight: expected identity `coder@agentops-prd-218`; `PI_COMS_DIR=/tmp/agentops/coms/agentops-prd-218`; live local pool includes `verifier`, `researcher`, and `steward`. The source-state verifier review at revision 1 returned `needs_human`; `V218-SOURCE-001` was corrected above and verifier recheck revision 2 accepted that correction. `V218-LIFECYCLE-001`, `V218-VALIDATION-001`, and `V218-MANUAL-001` remain human-gated. No code is authorized and no final completion is claimed. Controlling report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-218-terminal-selection-stability/verifier-report.md`.
- Steward initial structure/hygiene input received: issue artifacts are correctly scoped; no repo-local dependency/build/dist/log/generated issue output was found; baseline ignored `pipeline-diagram` output remains governed by its `.gitignore`; no cleanup was needed. This structure-only input does not resolve lifecycle, current-main validation, or physical-device gates.

## 2026-07-19 operator-authorized closeout validation
- Operator selected closeout/validation against current main. This authorizes only the context brief's bounded current-main automated baseline and a verifier final bug-check; it does not authorize product edits, GitHub mutation, PR/merge/deploy, or bypassing physical browser/device QA.
- Pre-validation dirty files: this coder-owned handoff and the verifier-owned report from the source-state review; no product files are dirty. The active checkpoint is current-main closeout validation: typecheck, the seven focused terminal suites, build, diff check, then the full suite. A final verifier bug-check follows successful bounded validation; any failure is a bounded finding.
- Dependency handling: this worktree has no local `term-control-center/node_modules`; validation may use only an ephemeral symlink to `/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules`, removed before review. No manual Chrome/Safari/iPad/iPhone result will be claimed without human/device evidence.
- PASS: `npm --prefix term-control-center run typecheck`.
- PASS: focused current-main terminal suite, 57/57: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/terminalScrollHold.test.ts tests/terminalHeldState.test.ts tests/terminalScrollContract.test.ts tests/terminalTouchSelectionEvents.test.ts tests/terminalClipboardCopy.test.ts tests/terminalRobustness.test.ts tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build`; only the existing non-module script and >500 kB chunk warnings were emitted. `git diff --check` passes.
- INCOMPLETE: `timeout 900s npm --prefix term-control-center run test` exited 124 after reporting 311 passing subtests and no test failure. This matches the historical non-termination risk but is current-run evidence, not a passing full-suite result. No scope permits a repair without a verifier finding/human decision.
- Cleanup after validation: the temporary `term-control-center/node_modules` symlink and generated `term-control-center/build` and `term-control-center/dist` were removed; no matching test process remains. Artifact-only diff check passes.
- Final Steward hygiene review: `clean`. Only the established issue run folder changed; no secret-like data/raw transcripts, temporary dependency/build/dist/generated validation output, or misplaced artifacts remain. No cleanup is recommended. Baseline ignored `pipeline-diagram` output remains out of scope and `.gitignore`-governed.
- Current-main verifier final bug-check (checkpoint 5, revision 1): `needs_human`; closeout validation was executed, but code final approval is not granted. Open findings: `BC218-CURRENT-001` later selection/jump intent loses to an enqueued output write; `BC218-CURRENT-002` required layout transitions remount the terminal; `BC218-CURRENT-003` terminal-originated OSC 52 can mutate the clipboard without an explicit Copy action; `BC218-CURRENT-004` stale OSC selection can override a newer local selection; `BC218-CURRENT-005` jump affordance is below the required 44px touch target; `V218-FULLSUITE-001` full suite is incomplete; `V218-DOC-001` README omits current scroll/OSC contract; and `V218-MANUAL-001` physical matrix is pending.
- Human decision required: the closeout authorization explicitly excluded product edits. Authorize a bounded terminal/docs repair loop for the eight listed findings, or choose another disposition. Any repair must preserve live-only ACK behavior, stage OSC 52 until the explicit Copy action, add focused behavioral regressions, rerun current validation, pass Steward recheck/final verifier bug-check, resolve or explicitly approve the full-suite deviation, and retain the physical matrix as a human gate. No final completion is claimed.

## 2026-07-19 operator-authorized bounded repair loop
- Operator authorization: “please continue with bounded terminal/docs repair loops.” This authorizes only the eight current-main findings in the controlling verifier report; it does not expand to replay/ACK semantics beyond pinning, unrelated chrome/session/auth/persistence work, terminal-content persistence, GitHub mutation, PR/merge/deploy/approval, trading, or backtesting.
- Pre-existing dirty files before this repair-loop authorization: coder-owned `coder-handoff.md` and verifier-owned `verifier-report.md`; no product file is dirty.
- Checkpoint 6.1: resolve `BC218-CURRENT-001` in `terminalOutput.ts` with its two focused race regressions, preserving non-replay-only ACK behavior. Checkpoint 6.2: resolve `BC218-CURRENT-003`/`004` through the existing explicit copy path with ordering/failure tests. Checkpoint 6.3: resolve `BC218-CURRENT-002`/`005` with stable terminal identity and a 44px target regression. Checkpoint 6.4: resolve `V218-DOC-001` and closeout validation/full-suite disposition. Steward rechecks artifacts before the final verifier bug-check.
- Mandatory freshness consult completed 2026-07-19 before clipboard implementation: WebKit says async clipboard writes outside a user gesture reject; its current engine check is transient/window-scoped activation, not authority carried by asynchronous OSC/WebSocket receipt. W3C Clipboard API likewise treats writes as permission/activation-gated. Therefore OSC 52 receipt must only stage ephemeral text and expose Copy; `writeText` occurs synchronously in the direct visible Copy gesture, with accessible failure feedback and no automatic retry/logging. Sources: WebKit Async Clipboard (2020-06-23, https://webkit.org/blog/10855/async-clipboard-api/), WebKit User Activation (2023-02-15, https://webkit.org/blog/13862/the-user-activation-api/), WebKit source (2026-07-01, https://github.com/WebKit/WebKit/commit/73645abad282e4903019e36d01c753145fd79a14; device inclusion remains manual-QA), W3C Clipboard API WD (2026-06-24, https://www.w3.org/TR/clipboard-apis/). No standards exception is requested.
- Checkpoint 6.1 implementation: output completion now applies a newer `ViewIntent` generation before its enqueued fallback. A later explicit jump pins to bottom, while a later held selection restores its current intent viewport. Live-only ACK and replay no-ACK behavior are unchanged.
- Checkpoint 6.1 focused coverage: `terminalScrollHold.test.ts` now proves held → enqueued write → explicit jump does not restore the held line, and output advancement → later selection restores the later selection viewport. PASS: typecheck; output suite 7/7; `git diff --check`. Changed product files: `term-control-center/src/terminalOutput.ts`, `term-control-center/tests/terminalScrollHold.test.ts`.
- Checkpoint 6.1 revision 2 cleanup: removed the stale `term-control-center/node_modules` symlink identified by `V218-CP6.1-HYGIENE-001`; confirmed `node_modules`, `build`, and `dist` are absent, and reran `git diff --check` successfully. No product code changed in this revision. Verifier approved checkpoint 6.1 at revision 2; no full report was read after the approval.
- Context renewal: reread `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-218-47c15734d86e/artifacts/project-context-brief.md` in full before checkpoint 6.2. It confirms the bounded OSC policy belongs in the existing `TerminalPane`/clipboard path with focused tests, must remain an explicit operator-copy action, and cannot change replay/ACK, session lifecycle, persistence, or unrelated chrome.
- Checkpoint 6.2: OSC receipt now stages text only; it no longer mutates the system clipboard. A new local selection clears staged OSC text. PASS: typecheck, clipboard tests 3/3, `git diff --check`; temporary dependency link removed. Verifier review requested for `BC218-CURRENT-003` and `BC218-CURRENT-004`.
- Checkpoint 6.2 revision 2: replaced the source-string assertion with executable `stageOscClipboard` coverage proving receipt does not write the system clipboard, local-after-OSC resolves to local text, and OSC-after-local resolves to the later OSC text. PASS: typecheck; clipboard tests 4/4; `git diff --check`; temporary symlink manually removed.

### Checkpoint 6.3a — 44px jump target
- Addressed `BC218-CURRENT-005`: `.terminal-jump-bottom` now has exact `44px` minimum width and height. CSS pixels avoid relying on the browser default root `rem` size for the required touch target.
- Added the deterministic focused `terminalRobustness.test.ts` assertion for both minimum dimensions. This is a scoped style contract only; `BC218-CURRENT-002` terminal identity/layout repair remains a separate, high-risk checkpoint.
- PASS: `npm --prefix term-control-center run typecheck`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/terminalRobustness.test.ts` (5/5); `git diff --check`.
- Cleanup: the temporary shared `term-control-center/node_modules` symlink and any `build`/`dist` output were removed before review. No terminal content, logs, or generated validation artifact was retained.
- Pending verifier review: checkpoint 6.3a, revision 1, `BC218-CURRENT-005`.

### Checkpoint 6.3b preparation — stable terminal identity
- Fresh Researcher consult, 2026-07-19: React preserves state only while a component remains at the same parent/tree position with stable identity keys. The smallest permitted arrangement keeps each `TerminalPane` beneath one unconditional unkeyed terminal host, keeps pane keys identity-only, and changes classes/visibility rather than component types, ancestor positions, or portal targets. Its focused test recommendation is to prove mount/cleanup and xterm/socket identity through all required transitions; development StrictMode has an initial extra effect cycle, so it is not a transition remount. Sources retrieved 2026-07-19: React [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state), [useEffect](https://react.dev/reference/react/useEffect), [act](https://react.dev/reference/react/act), [StrictMode](https://react.dev/reference/react/StrictMode), and [createPortal](https://react.dev/reference/react-dom/createPortal).
- Current test dependencies do not include a supported DOM renderer (`jsdom`, `happy-dom`, `linkedom`, and `react-test-renderer` are absent; React warns against the deprecated renderer). The repair must not add a test dependency or redesign the pane split. The focused test will exercise a shared deterministic terminal-deck identity/visibility model used by `App.tsx`, replacing the current layout regex-only coverage; React DOM/browser identity remains in the required physical matrix.

### Checkpoint 6.3a result
- Verifier approved checkpoint 6.3a revision 1 (`BC218-CURRENT-005`, no open findings). Per the transport contract, the full approved report was not reread.

### Checkpoint 6.3b — stable terminal layout identity
- Addressed `BC218-CURRENT-002`: `TerminalWorkspace` now always keeps one `term-workspace-shell` with stable `JobSidebar` and `AllotmentShell` children. Compact, phone, maximize, Browser, Browser-focus, and Diff states change shell classes, `hidden`, or sidecar visibility rather than replacing the terminal ancestor.
- `AllotmentShell` now always retains `TerminalArea` in its first fixed shell slot. Browser and Diff remain exclusive siblings; maximize hides the sidecar. `TerminalArea` always retains the existing resizable `Allotment`, keyed by pane ID; `visible` changes through the existing Allotment API rather than swapping it for a focus grid.
- Added `terminalDeck.ts`, a 3-line deterministic pane-key/position/visibility model consumed by `App.tsx`; `terminalRobustness.test.ts` exercises split, maximize, focus, phone, Browser, Browser-focus, and Diff-equivalent visibility transitions and asserts stable pane key/position with only visibility changing. It replaces the former regression-prone layout regex tests. `termBasePath.test.ts` now checks the stable shell/deck contract rather than requiring the remounting branches.
- CSS restores the pre-existing terminal shell/sidecar grid around the stable terminal slot. Desktop Browser/Diff remains a two-column, horizontally resizable sidecar; coarse/phone layout stacks the terminal and sidecar into two 14rem-minimum rows. Browser focus hides the terminal slot without unmounting it.
- PASS: `npm --prefix term-control-center run typecheck`.
- PASS: focused seven-suite terminal checkpoint validation, 60/60: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/terminalScrollHold.test.ts tests/terminalHeldState.test.ts tests/terminalScrollContract.test.ts tests/terminalTouchSelectionEvents.test.ts tests/terminalClipboardCopy.test.ts tests/terminalRobustness.test.ts tests/termBasePath.test.ts`.
- PASS: `npm --prefix term-control-center run build`; only existing non-module-script and >500kB chunk warnings.
- PASS: `git diff --check`.
- Cleanup: temporary shared `term-control-center/node_modules` symlink and generated `build`/`dist` were removed after validation. No dependency was added, no terminal content/log was retained, and no replay/live ACK, session lifecycle, auth, persistence, or clipboard behavior changed.
- Pending verifier review: checkpoint 6.3b, revision 1, `BC218-CURRENT-002`. The mandatory physical Chrome/Safari/iPad/iPhone matrix remains a final human gate.

### Checkpoint 6.3b revision 2
- Addressed the verifier's bounded direct-child finding: `TerminalArea` now maps each keyed `Allotment.Pane` directly under `Allotment`, with `minSize` and `visible` on that direct child. `PaneSlot` was removed; it had incorrectly hidden the `visible` prop beneath a function component, which Allotment 1.20.5 does not register.
- Retained the stable shell ancestor, stable `terminalDeck` pane order/keys, and the executable visibility-transition coverage. `termBasePath.test.ts` now asserts the direct keyed `Allotment.Pane` contract, preventing regression to the nested-pane shape.
- PASS: typecheck; focused seven terminal suites 60/60; build (only existing non-module-script and chunk-size warnings); `git diff --check`.
- Cleanup: the temporary shared dependency symlink and generated `build`/`dist` output were removed before re-review. No dependency, protocol, clipboard, session, persistence, or terminal-content behavior changed.
- Pending verifier re-review: checkpoint 6.3b, revision 2, `BC218-CURRENT-002`.

### Checkpoint 6.3b result
- Verifier approved revision 2 (`BC218-CURRENT-002`, no open findings). Per the transport contract, the full approved report was not reread.

### Checkpoint 6.4 — terminal interaction documentation
- Addressed `V218-DOC-001` in the existing `term-control-center/README.md`; no duplicate documentation was created. The message contract now documents `SCROLL_STATE { held, newOutput }` and explicit `SCROLL_RESET`; runtime notes document composed local/tmux held state, explicit jump-only reset, live-only ACK/replay no-ACK, OSC 52 ephemeral staging, local-selection freshness, explicit Copy/shortcut clipboard authority, and visible/no-retry copy failure behavior.
- PASS: documentation assertions found each required contract term; `git diff --check` passes. No build, dependency link, generated output, or product code changed for this documentation slice.
- Pending verifier review: checkpoint 6.4, revision 1, `V218-DOC-001`. `V218-FULLSUITE-001` and `V218-MANUAL-001` remain separately open.

### Checkpoint 6.4 result and full-suite isolation
- Verifier approved checkpoint 6.4 revision 1 (`V218-DOC-001`, no open findings). Per the transport contract, the full approved report was not reread.
- Current full-suite rerun is INCOMPLETE, not passing: `timeout 900s npm --prefix term-control-center run test` exited 124 after 311 passing subtests and no reported failure. It reproduced the exact prior stopping point.
- Bounded isolation: `timeout 60s node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/coworkerGuard.test.ts` exited 124 after its two assertions passed. This source/hang is outside the authorized terminal/docs repair scope; no test-harness repair was made and no full-suite pass is claimed.
- Cleanup after each diagnostic: temporary shared `node_modules` symlink and `build`/`dist` are absent. Next required action is Steward recheck, then final verifier bug-check. The full-suite deviation and physical Chrome/Safari/iPad/iPhone evidence remain human gates.
- Final Steward recheck: `clean`. Terminal/docs changes, `terminalDeck.ts`, and issue-run review-request JSONs are correctly placed; no dependency/build artifacts, generated logs, raw terminal content, scope drift, or out-of-scope test repair was found. This recheck does not resolve the full-suite or device human gates.

### Final bug-check revision 2 — tmux reset cache
- Addressed `BC218-CURRENT-006`: `SCROLL_RESET` now invokes a session-scoped monitor-cache reset before broadcasting the cleared state. The tmux monitor deletes only that session's prior `TmuxScrollState`, so a quick copy-mode re-entry with no actual activity recomputes `{ held: true, newOutput: false }`; a later activity transition still sets `newOutput: true` and per-poll current-state broadcast remains unchanged.
- Added executable `terminalHeldState.test.ts` coverage for cached true → reset → quick inactive re-entry, plus an exact server routing assertion that `resetScroll` invokes `resetTmuxScroll(session)`.
- PASS: typecheck; focused seven terminal suites 61/61; build (only existing non-module-script and chunk-size warnings); `git diff --check`.
- Cleanup: temporary shared dependency symlink and generated `build`/`dist` removed before review. No replay/live ACK, clipboard, auth, session persistence, or protocol-shape change was made.
- Pending Steward recheck and verifier final bug-check revision 2. `V218-FULLSUITE-001` and `V218-MANUAL-001` remain human gates.
- Steward recheck for revision 2: `clean`. The session-scoped monitor-cache change remains in existing server modules; terminal-held-state coverage and run artifacts are correctly placed; no dependency/build/generated/log/raw-terminal output or scope drift was found.

### Final bug-check revision 3 — socket boundary cleanup
- Addressed `V218-FINAL-KISS-001`: `handleSocket` now accepts the cohesive `SocketRuntime` rather than six separate inputs. `createTermServer` constructs the runtime once from `sessions`, the existing state-save closure, and the monitor reset callback; WebSocket close/error handlers use `runtime.sessions`. No behavior changed.
- Updated the focused reset test to require the three-argument `handleSocket` signature while retaining exact-session reset coverage.
- PASS: typecheck; focused seven terminal suites 61/61; build (only existing non-module-script and chunk-size warnings); `git diff --check`.
- Cleanup: temporary shared dependency symlink and generated `build`/`dist` removed. Pending Steward recheck and final verifier bug-check revision 3; full-suite deviation and physical matrix remain human gates.
- Steward revision-3 recheck: `clean`. `SocketRuntime`, `terminalHeldState` test, and handoff changes are correctly placed; no dependency/build/dist/generated/log/raw-terminal artifact was found.

### Final verifier disposition — revision 3
- Final verifier bug-check revision 3 is **code-clean**: `BC218-CURRENT-006` and `V218-FINAL-KISS-001` are resolved; no scoped functional, security, silent-failure, edge-case, coverage, or KISS finding remains. The full final verdict is `needs_human`, not final acceptance.
- Required human gate `V218-FULLSUITE-001`: approve an explicit bounded validation deviation using the current evidence (full suite times out at 900 seconds after 311 passing subtests; the untouched current-main `coworkerGuard.test.ts` reproduces two passing assertions then non-termination), or authorize a separate out-of-scope server/test lifecycle repair. No full-suite pass is claimed.
- Required human gate `V218-MANUAL-001`: execute and record the complete Chrome, Safari, iPad Safari, and iPhone Safari matrix: streaming/replay scroll/selection/copy accuracy and failure; explicit jump; split/maximize/Browser/Diff/pane transitions; and physical 50k responsiveness. Any failure is a new bounded defect.
- Final validation receipt/report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-218-terminal-selection-stability/verifier-report.md`. No PR, merge, deploy, GitHub mutation, approval, trading, or backtest occurred. Stop condition reached: true human escalation for the two non-bypassable gates.

### Human validation-deviation decision
- On 2026-07-19, the operator approved the bounded `V218-FULLSUITE-001` validation deviation. This accepts the current evidence only: the required full suite times out after 900 seconds/311 reported passing subtests; the untouched current-main `coworkerGuard.test.ts` independently reproduces two passing assertions then non-termination; typecheck, build, `git diff --check`, focused terminal validation (61/61), and Steward rechecks pass. This approval does not claim a full-suite pass, authorize an out-of-scope harness repair, or relax any physical QA requirement.
- `V218-MANUAL-001` remains the sole final human acceptance gate: Chrome, Safari, iPad Safari, and iPhone Safari evidence must be executed and recorded before final completion.

### PR #257 advisory review fixes
- Kody review on draft PR #257 identified two bounded defects. First, sidecar `resize: horizontal` did not resize the fractional CSS grid track. The terminal shell now uses an auto-sized sidecar grid track with an explicit resizable sidecar width; coarse layouts retain their stacked layout and disable desktop horizontal resizing.
- Second, a selection-start/aborted gesture cleared staged OSC text before a real local selection existed. Clipboard staging now clears only in `keepSelection`, after a non-empty selection snapshot exists; selection locks still begin immediately to preserve output/viewport behavior.
- Added focused contracts for the sidecar grid track and delayed clipboard clearing. PASS: typecheck; affected focused suites 11/11; build with existing Vite warnings; `git diff --check`. Temporary dependency symlink and generated `build`/`dist` were removed.
- Pending verifier review, commit/push to draft PR #257, and requested Kody re-review. Physical QA remains required.

### PR #257 advisory review fixes revision 2
- Addressed `KODY257-SIDECAR-001`: Browser focus now explicitly clears the split-only width/max-width/horizontal-resize rules, so its single desktop grid track fills normally; split Browser/Diff remains resizable through the auto-sized second grid track, and coarse layouts retain their existing no-resize override.
- Addressed `KODY257-OSC-001`: staged OSC readiness is now a named callback. Clearing an absent/aborted local selection preserves staged Copy availability; a retained local selection or restored local selection clears staged OSC text and becomes the Copy source. Selection locking remains immediate. Added CSS/authority contracts.
- PASS: typecheck; focused seven terminal suites 62/62; build with only existing Vite warnings; `git diff --check`; dependency/build/dist cleanup complete.
- Pending verifier re-review, commit/push to draft PR #257, then explicit Kody re-review. Physical QA remains required.

### PR #257 advisory review fixes revision 3
- Moved the Browser-focus override after the equal-specificity split rule so focused Browser width/resizing now wins in the CSS cascade.
- Added `terminalSelectionClipboard.ts`, a production-consumed, executable selection authority seam: staged OSC remains copy-ready with no local selection; any retained/restored local selection clears staged text and remains copy-ready. Coverage now executes both authority transitions.
- PASS: typecheck; focused seven suites 63/63; build with existing Vite warnings; `git diff --check`; cleanup complete. Pending verifier re-review before push/Kody re-review.
