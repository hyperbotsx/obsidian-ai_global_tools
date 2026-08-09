# Coder Handoff — Issue #29 Durable Completion Notification Center

## Task source

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/29
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Branch: `prd/durable-completion-notification-center-29`

## Pre-edit state

- `git status --short --branch` before editing: `## prd/durable-completion-notification-center-29...origin/main`
- Pre-existing dirty files: none.

## Scope controls

Allowed paths for this checkpoint:

- `term-control-center/server/*`
- `term-control-center/shared/*`
- `term-control-center/tests/*`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-29-durable-completion-notification-center/*`

Forbidden/out-of-scope for this checkpoint:

- No terminal/tmux persistence reimplementation; PRD #41 remains the owner.
- No raw transcripts, terminal output, launch prompts, cookies, secrets, tokens, attach tokens, or private credentials in durable completion state.
- No autonomous PR creation, merge, deploy, approval, trading, backtest authority.
- No UI/lifecycle integration beyond persistence contract until this checkpoint is reviewed.

Stop condition:

- Stop after verifier approval of checkpoint 1/2 (scope + persistence contract), before moving to notification-center UI or broader lifecycle integration.

## Verifier checkpoints from PRD #29

1. Scope + persistence contract: PRD #41 delegation, durable completion store schema, atomic writes, restart recovery, duplicate reconciliation, lifecycle persistence, no-secret/no-transcript tests.
2. Notification-center UI: desktop/mobile/iPad-visible center with persistent unresolved items and accessible controls.
3. Lifecycle: Prepare PR, PR open, merge, action-error, merged-synced, validation-queued, dismissed, and deferred transitions persist and render correctly.
4. Automatic completion: final verifier approval + bug-check-passed creates/reconciles events without manual POST in normal path.
5. Integration: PRD #34 closeout and PRD #47 validation-ledger hooks without over-owning either workflow.
6. Guardrail/final bug-check: no autonomous authority; mutating actions remain human-confirmed; regression review for lost notifications, stale UI, duplicates, corruption, mobile overlap, token leakage, action-gate bypass, wrong terminal relaunch.

## Mandatory research and codebase checks

Researcher consult completed before implementation. Summary:

- Browser storage is best-effort and may be private-session scoped or evicted; localStorage is synchronous, quota-limited, and should be hints only.
- Safari/WebKit may evict script-created storage under storage pressure or after periods without user interaction.
- Web notifications need secure context/permission and mobile reliability requires service-worker persistent notifications; OS action buttons should not be relied on cross-browser.
- Use an in-app durable notification center as authoritative UX; use polite live regions for arrivals; implement mutating action sheets as accessible dialogs with focus management and explicit human action.
- Sources cited by Researcher: MDN Web Storage/Storage quotas, WebKit storage policy update, MDN Notifications API, WebKit iOS/iPadOS Web Push, Apple web push docs, WAI-ARIA APG alert/dialog patterns, WCAG 2.2 target/focus guidance.

PRD #41 terminal recovery contract inspected:

- Terminal/tmux recovery remains delegated to supervised tmux sessions, persisted group metadata, token refresh via `/term-config.js`, stale/unrecoverable states, and no duplicate relaunch behavior.
- This checkpoint only persists completion/action records and does not change tmux/session recovery behavior.

## Current checkpoint changes

Implemented scope + persistence contract:

- Added `term-control-center/server/completionStore.ts` with:
  - server-side durable `completions.json` under `TERM_CONTROL_STATE_DIR` / term-control state dir,
  - private directory/file modes,
  - atomic temp-file write + rename,
  - schema versioning,
  - safe field allowlisting/scrubbing,
  - lifecycle-state derivation,
  - duplicate reconciliation by repository/issue/worktree/branch.
- Wired `createTermServer` to load durable completions on startup and persist completion map changes.
- Added shared lifecycle metadata fields for PRD #29 lifecycle states while preserving existing status compatibility.
- Adjusted completion event response to return the reconciled stored state.
- Isolated completion-server tests with per-test `TERM_CONTROL_STATE_DIR`.
- Added tests for restart recovery, duplicate reconciliation, lifecycle persistence, and no-secret/no-transcript storage.

Changed files:

- `term-control-center/server/completionStore.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/index.ts`
- `term-control-center/shared/completion.ts`
- `term-control-center/tests/completion-server.test.ts`
- `term-control-center/tests/completion-store.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-29-durable-completion-notification-center/coder-handoff.md`

## Revision 2 updates

Addressed verifier findings:

- `V29-CP1-001`: strengthened persistence text scrubbing for `Authorization: Bearer ...`, standalone bearer values, and `github_pat_...`; added regression coverage.
- `V29-CP1-002`: durable lifecycle derivation now reports `merge_ready` for open PR states with enabled merge actions; reload test updated for merge-ready persistence.
- `V29-CP1-003`: split the completion signal serializer into smaller helpers.

## Revision 4 updates

Addressed checkpoint 2 verifier findings:

- `V29-CP2-001`: completion polling now attempts term token bootstrap and server notification polling on normal load and when the Updates panel opens; degraded rendering is preserved when term-control is unavailable.
- `V29-CP2-002`: completion-center UI moved to `pipeline-diagram/completion-center.js`; `review-notify.js` is reduced to 232 lines and the new module is loaded before `review-notify.js` in board, pipeline, and WIP pages.

## Validation

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test` — passed, 156/156.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings about non-module `term-config.js` and chunk size only.
- `git diff --check` — passed.
- `node --check pipeline-diagram/review-notify.js` — passed.
- `node --check pipeline-diagram/completion-center.js` — passed.

## Checkpoint 2 changes — Notification-center UI

Implemented notification-center UI improvements in `pipeline-diagram/review-notify.js`:

- Persistent Updates button now opens an accessible server-backed completion center panel.
- Panel is labelled as a non-modal dialog with `aria-haspopup`, `aria-controls`, `aria-expanded`, `aria-labelledby`, keyboard Escape close, close button, focus handoff, and polite live status text.
- Completion center renders explicit loading, empty, degraded/unavailable, unresolved count, and action-error visual states.
- Mobile/iPad-sized viewport CSS keeps the center and toasts within safe-area bounds with minimum 44px tap targets and no terminal relaunch behavior.
- Completion item clicks still route through `window.onOpenCompletionTerm(notification.groupId, 'actions')` or deep-link to `board.html?completion=...`; no launch endpoint is called by notification rendering.
- Cold page load now bootstraps `/term-config.js` and polls `/completion-notifications` without requiring a preexisting token or `?completion=...` URL.
- Extracted the completion center into `pipeline-diagram/completion-center.js` to keep `review-notify.js` within KISS file-size limits (`review-notify.js`: 232 lines; `completion-center.js`: 175 lines).
- Added `term-control-center/tests/reviewNotify.test.ts` assertions for accessible states, mobile sizing, cold-load polling, and script load order.

Additional changed files for checkpoint 2:

- `pipeline-diagram/completion-center.js`
- `pipeline-diagram/review-notify.js`
- `pipeline-diagram/board.html`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/wip.html`
- `term-control-center/tests/reviewNotify.test.ts`

## Checkpoint 3 changes — Lifecycle transitions

Implemented lifecycle transition support for `deferred`, `dismissed`, and `validation_queued` while preserving existing Prepare PR, PR open, merge, action-error, and merged-synced behavior:

- Extended `CompletionActionId` with `validation_queued`, `defer`, and `dismiss`.
- Added server routes:
  - `POST /completion-actions/defer`
  - `POST /completion-actions/dismiss`
  - `POST /completion-actions/validation-queued`
- Human lifecycle actions persist terminal states and add action-result notifications.
- Terminal lifecycle states disable other idle/running actions after deferral, dismissal, or validation queueing.
- Existing `merged_synced` / `closeout_done` actions now expose `Queue Validation` for the later PRD #47 handoff checkpoint.
- Board completion action panel renders validation queued, dismissed, and deferred summaries and keeps each new mutation behind an explicit browser confirmation.
- Added tests for route lifecycle transitions and durable reload of terminal lifecycle states.

Additional changed files for checkpoint 3:

- `term-control-center/shared/completion.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/completionCloseoutRoutes.ts`
- `term-control-center/server/completionLifecycleRoutes.ts`
- `pipeline-diagram/board.html`
- `term-control-center/tests/completion-routes.test.ts`
- `term-control-center/tests/completion-store.test.ts`
- `term-control-center/tests/completion.test.ts`
- Existing test expectation updates in `completion-server.test.ts` and `server.test.ts` for new defer/dismiss actions.

Revision 5 findings addressed:

- `V29-CP3-001`: terminal lifecycle states (`dismissed`, `deferred`, `validation_queued`) are durable but filtered from active completion notifications; added shared regression coverage.
- `V29-CP3-002`: direct validation queueing is rejected until merged/synced evidence and an enabled validation action exist; route test covers pre-merge rejection and post-merge success.
- `V29-CP3-003`: extracted lifecycle route/transition code to `completionLifecycleRoutes.ts`; `completionRoutes.ts` is now 274 lines.

## Checkpoint 4 readiness — Automatic completion reconciliation

Automatic completion behavior is implemented through the existing completion discovery path:

- `GET /completion-notifications` calls `discoverCompletions(...)` for known launch groups that lack completion state.
- `discoverCompletionState(...)` scans bounded verifier report paths under `dev-plans/agentops/coder-verifier-workflow` and requires machine JSON with `decision: approved` plus `bug_check_status`/`bugCheckStatus: passed`.
- Discovered report evidence is converted into a canonical completion signal with the group's source-of-truth issue/repository/worktree/branch and child session IDs, then persisted through the durable store wrapper.
- `GET /completion-state/:id` can also discover a completion for a known group without requiring a manual POST.
- Existing coverage: `discovers approved verifier reports and exposes completion actions`, `restores durable completion notifications after server restart`, duplicate reconciliation/store tests, and source-of-truth spoofing tests.

No new code was needed after lifecycle fixes for this checkpoint; requesting verifier review against the current implementation and tests.

## Checkpoint 5 readiness — PRD #34 / PRD #47 integration hooks

Integration surfaces are present without taking ownership of dependent workflows:

- PRD #34: `POST /completion-actions/prd-closeout` is offered only after `merged_synced` evidence, calls the configured `prdCloseout` function, persists `closing_out`, `closeout_done`, and retryable closeout error states, and preserves merge evidence for safe retry.
- PRD #34 production wiring: `registerCompletionRoutes(...)` defaults to `runPrdCloseout`, while tests can inject a mock closeout runner.
- PRD #34 board path: the board action center renders `Close Out PRD` after merge/sync and shows closeout progress/failure/success.
- PRD #47: because issue #47 is still Draft / not CEO approved, this PRD does not implement the ledger. It exposes a bounded handoff hook instead: post-merge/post-closeout `Queue Validation` transitions the completion into durable `validation_queued` only after merge/sync evidence and an enabled validation action exist.
- PRD #47 handoff evidence stays in the completion record (`task`, `pr`, `merge`, `closeout`, verifier report path, bug-check status) without creating ledger rows or launching validation agents.

## Checkpoint 6 readiness — Guardrails

Guardrails preserved in this PRD:

- No browser client calls GitHub directly with privileged credentials; mutating actions remain server/token guarded.
- Board action buttons require explicit human clicks and browser confirmations for Prepare PR, Merge + Update Local, Close Out PRD, Queue Validation, Defer, and Dismiss.
- Notification polling/rendering does not trigger mutating endpoints.
- No autonomous deploy, approval, trading, backtest, validation-agent launch, or PRD #47 ledger mutation was added.
- PRD #41 terminal recovery is consumed only through reopen/reattach links; no terminal/tmux persistence was reimplemented.
- Completion persistence scrubs unsafe transcript/credential/token-like fields and stores only safe action/task metadata.
- Existing/static tests cover forbidden endpoints/action copy, action-gate preservation, token-gated routes, no duplicate relaunch, no unsafe durable fields, and no launch prompt/operator draft persistence.

Final bug-check revision fix:

- `V29-FINAL-001`: action-error states for Prepare PR, Merge + Update Local, and PRD Closeout now retain explicit human Defer/Dismiss resolution actions. Added route regression coverage proving failed action states expose resolution actions and can transition through lifecycle routes.

## Verifier status

- Revision 1: revision requested for `V29-CP1-001`, `V29-CP1-002`, `V29-CP1-003`.
- Revision 2: approved for checkpoint `1/2 - Scope + persistence contract`; open findings: 0.
- Revision 3: revision requested for `V29-CP2-001`, `V29-CP2-002`.
- Revision 4: approved for checkpoint `2 - Notification-center UI`; open findings: 0.
- Revision 5: revision requested for `V29-CP3-001`, `V29-CP3-002`, `V29-CP3-003`.
- Revision 6: approved for checkpoint `3 - Lifecycle transitions`; open findings: 0.
- Revision 7: approved for checkpoint `4 - Automatic completion reconciliation`; open findings: 0.
- Revision 8: approved for checkpoint `5 - Integration hooks`; open findings: 0.
- Revision 9: approved for checkpoint `6 - Guardrails`; open findings: 0.
- Revision 10: final bug-check requested fix `V29-FINAL-001`.
- Revision 11: final bug-check approved; bug-check status passed; open findings: 0.

## Notes for verifier

- Please review only checkpoint 1/2 scope + persistence contract.
- Terminal reopen/recovery behavior should remain PRD #41-owned; no tmux/session recovery code was changed.
- The durable store intentionally saves safe completion/action metadata only; it excludes unknown fields and redacts obvious token/credential strings in persisted strings/results.
