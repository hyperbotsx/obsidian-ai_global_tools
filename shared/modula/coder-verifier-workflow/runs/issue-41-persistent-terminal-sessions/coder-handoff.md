# Coder Handoff: Issue #41 Restart-Safe Persistent Agent Terminal Sessions

## Task source

- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/41
- Branch: `feat/persistent-terminal-sessions-41`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Status: final verifier bug-check approved.

## Pre-edit status

- `git status --short --branch`: clean before task work.
- Pre-existing dirty files: none.
- Current artifact changes: handoff plus verifier report from architecture checkpoint.

## Scope controls from PRD

Allowed paths:

- `term-control-center/` server, client, shared protocol, and tests.
- `pipeline-diagram/board.html` only for stale/recovered session UX and launch/reopen behavior.
- `scripts/agentops/` only if wrapper/supervisor integration requires it.
- AgentOps docs/runbooks and safe cleanup tooling for local terminal session state.
- Run artifacts under this folder.

Forbidden:

- PR creation, merge, deploy, production-readiness claims, PRD approval, trading, paper trading, backtesting.
- Public unauthenticated terminal endpoints or bypassing token/same-origin/profile/worktree checks.
- Arbitrary browser-supplied shell command execution.
- Persisting raw terminal transcripts, prompts, operator PRD idea text, secrets, API keys, cookies, private credentials, or plaintext attach tokens when avoidable.
- Broad process killing outside supervised sessions created by this feature.

Required validation:

- `cd term-control-center && npm run typecheck`
- `cd term-control-center && npm test`
- `bash -n scripts/agentops/pi-agent.sh` if wrapper changes.
- `git diff --check`
- Manual restart/stale smoke tests from PRD when implementation reaches validation checkpoint.

Stop condition:

- Stop after final verifier bug-check approval or human escalation. Do not open PR unless explicitly asked.

## Verifier checkpoints

1. Architecture checkpoint: persistence/supervisor strategy, state model, security boundaries, metadata privacy, cleanup plan, restart/deploy implications.
2. Backend recovery checkpoint: persisted metadata, supervisor mapping, service restart recovery, token refresh handling, stale detection.
3. Frontend UX checkpoint: reopen flow, stale/recovered states, action semantics, no duplicate relaunch.
4. Validation/docs checkpoint: automated tests, manual smoke tests, runbook updates, final regression.

## Research-first summary

Researcher was consulted before implementation for tmux/session supervision, node-pty reattach limits, xterm.js reconnect, WebSocket token rotation, and local metadata boundaries.

Key findings:

- Use tmux as durable session owner; Node/node-pty should own short-lived `tmux attach` clients only.
- `node-pty` does not provide a portable API to reattach to an existing PTY after the owning process dies.
- xterm.js should reconnect by receiving a bounded tmux `capture-pane` replay at attach time, not by storing transcripts in app metadata.
- `/term-config.js` should stay same-origin and `Cache-Control: no-store`; stale WebSocket tokens should fail closed and clients should refetch bootstrap config before retrying.
- Persist minimal process metadata under a user-private state directory (`0700` dir, `0600` files), not transcripts, prompts, env, secrets, or plaintext attach tokens.

## Architecture decision for checkpoint 1

Chosen v1 design: supervised tmux-backed pane sessions plus persisted group metadata.

### Supervisor model

- Create one tmux session per browser pane, not one multi-pane tmux window. This keeps each browser terminal mapped to one agent process and avoids exposing tmux pane multiplexing UI inside xterm.
- Use a per-worktree tmux socket namespace such as `agentops-<worktree-slug-or-hash>`.
- Use deterministic tmux session names scoped to AgentOps-created sessions, e.g. `agentops_<worktreeHash>_<groupShort>_<role>_<sessionShort>`.
- Launch long-running role agents inside tmux. Node attaches to tmux via node-pty using `tmux -L <socket> attach-session -t =<sessionName>`.
- On service shutdown or browser close, kill only the node-pty tmux client, not the tmux session, unless the user chooses Kill.

### Metadata model

Persist group metadata outside Node memory, defaulting to `TERM_CONTROL_STATE_DIR` or an XDG state path such as `$XDG_STATE_HOME/agentops/term-control-center`.

Persist only:

- group ID, mode, task identity (`issueNumber`/`issueUrl` or `draftId`), repository, worktree path, branch, status.
- pane metadata: session ID, role/profile, model profile ID, cwd, launch timestamps, tmux socket/session name, tmux pane ID if available, recoverability state, last status reason.
- attach token hash/salt or equivalent verifier, never plaintext attach token when avoidable.

Do not persist:

- raw terminal output, transcripts, prompts, operator PRD idea text, auth tokens, plaintext attach tokens, env vars, API keys, cookies, private credentials.

Launch context privacy boundary:

- Existing `/tmp/agentops/term-context/<groupId>/task-context.md` handling must be changed before durable recovery lands.
- Durable restart metadata must not point to, copy, or depend on raw prompt/context files.
- PRD-authoring `initialIdea` and launch prompt text must either stay only in process input/argv for the initial launch or be written to a user-private ephemeral file with deterministic cleanup, never into durable state.
- Backend tests must assert persisted state/context files do not contain `initialIdea`, launch prompt text, auth tokens, attach tokens, terminal transcripts, env secrets, or known test-secret sentinels.

### Recovery flow

- Server startup loads persisted metadata, validates state-dir permissions, and reconciles each pane with tmux state using `has-session`/`list-panes`.
- `/groups` returns persisted groups with `recovering`, `recovered`, `stale`, or `unrecoverable` pane/group recoverability.
- `/launch` checks persisted metadata plus tmux before launching. If the same task/worktree/branch has live supervised panes, return the existing group with `reused: true`; do not duplicate agents.
- WebSocket `INIT` with a known `sessionId` + valid attach token hash can recover a missing in-memory session by spawning a new node-pty tmux attach client.
- On attach, server sends `READY`, then a bounded `capture-pane -p -e -J -S -200` replay marked as replay data, then streams live output from the tmux attach client.
- If tmux is absent for a persisted pane, return a precise error/recoverability reason and mark stale/unrecoverable instead of relaunching silently.

### Action semantics

- Close: browser detach only; do not kill tmux-supervised process.
- Kill: terminate the specific AgentOps-created tmux session/pane and update metadata to exited/unrecoverable.
- Restart: explicit user action that first kills the supervised pane/group, then launches a new supervised pane; never duplicate a live recovered pane.

### Cleanup plan

Default TTLs:

- Stale metadata TTL: 7 days after `lastSeenAt` when tmux session is absent.
- Ephemeral launch-context TTL: 24 hours after group creation, or immediate removal once all panes are launched if implementation no longer needs the file.
- Live tmux sessions are never killed by TTL cleanup.

Startup/interval cleanup:

- Reconcile persisted metadata against tmux with `tmux -L <worktreeSocket> has-session -t =<sessionName>`.
- If tmux is present, mark pane `recovered`/`recoverable` and refresh `lastSeenAt`.
- If tmux is absent, mark pane `stale` with reason `tmux_session_missing` and keep metadata until stale TTL or explicit operator cleanup.
- After stale TTL, delete only the stale metadata record and any matching ephemeral context file; do not kill processes.

Operator cleanup contract:

- Add a protected server cleanup action or local script that supports list/dry-run before delete.
- Dry-run lists group ID, pane role, worktree, tmux socket, tmux session name, recoverability reason, and whether the tmux session currently exists.
- Delete mode removes stale metadata and matching ephemeral context files only when tmux is absent.
- Kill mode, if added, must require an explicit group/pane ID and must target only tmux session names loaded from validated AgentOps metadata in the per-worktree socket namespace.

Precise tmux targeting rule:

- Every cleanup command must use the persisted per-worktree socket name and exact-session target: `tmux -L <worktreeSocket> has-session -t =<sessionName>` or `tmux -L <worktreeSocket> kill-session -t =<sessionName>`.
- Never use wildcard `tmux kill-server`, broad `kill-session -a`, process-name matching, or shell-globbed session names.

### Restart/deploy implications

- Node restarts rotate runtime auth tokens as today; clients reload/refetch `/term-config.js` for the fresh token.
- Browser localStorage/session records remain hints only. Server persisted metadata and tmux supervisor state are authoritative.
- A deploy restart should not kill tmux sessions because Node owns only transient attach clients.

## Backend checkpoint implementation notes

Changed files:

- `term-control-center/server/tmuxSupervisor.ts`: tmux socket/session naming, create/attach/capture/kill helpers with exact-session targeting.
- `term-control-center/server/sessionStore.ts`: private state-dir metadata store, hashed attach-token verifier, task sanitization that omits `initialIdea`, persisted provider/model profile/effort.
- `term-control-center/server/sessionRecovery.ts`: extracted persisted restore/reconcile and tmux attach/replay orchestration out of the server entrypoint.
- `term-control-center/server/launchGroup.ts`: tmux-backed launch-group panes by default, sanitized public pane summaries, stale groups summarize as error instead of safe-to-relaunch exited, no raw operator idea in launch context files.
- `term-control-center/server/index.ts`: persisted group restoration wiring, stale tmux detection, close-vs-kill semantics for supervised sessions, default supervisor mode `tmux` with test override.
- `term-control-center/tests/server.test.ts`: regression coverage for sanitized launch responses, launch-context privacy, tmux restart recovery/no duplicate relaunch, stale no-relaunch, restored model metadata.

Frontend checkpoint implementation:

- `pipeline-diagram/board.html`: merges remembered browser attach tokens into authoritative `/groups` records after server restart, labels recovered/recovering/stale sessions, and opens reused stale groups without relaunching.
- `term-control-center/src/App.tsx`: carries pane recoverability from launch URLs into initial pane status and disables profile-only restart for attached workspace panes.
- `term-control-center/src/TerminalPane.tsx`: maps stale/unrecoverable backend recovery errors to explicit pane statuses, preserves recovered state on READY, and disables Restart for recovered workspace panes to avoid bare unsupervised relaunch.
- `term-control-center/tests/boardGuardrails.test.ts`: covers token-hint merge, recovered/recovering/stale labels, and no-relaunch recovery messaging.
- `term-control-center/tests/termBasePath.test.ts`: covers stale/unrecoverable/recovered terminal pane state handling and restart-disable behavior.

Validation/docs checkpoint implementation:

- `docs/agentops-terminal-sessions.md`: documents tmux restart strategy, state path, privacy boundaries, recovery states, action semantics, cleanup commands, deployment implications, and known limits.
- `term-control-center/scripts/term-session-cleanup.mjs`: exact-target cleanup/list script for metadata, stale deletion, and explicit group/pane tmux kill.
- `term-control-center/tests/boardGuardrails.test.ts`: covers runbook and cleanup script guardrails against broad tmux/process killing.

## Validation so far

- `gh issue view 41 --repo hyperbotsx/agentops-harness ...`: read PRD source.
- `git status --short --branch`: clean before artifact creation.
- `tmux -V`: `tmux 3.4` is available locally.
- `cd term-control-center && npm run typecheck`: pass.
- `cd term-control-center && npm run typecheck && npm test`: pass, 130 tests.
- `cd term-control-center && npm run build:server`: pass.
- `node term-control-center/scripts/term-session-cleanup.mjs --state-dir <tmp> --context-root <tmp> --delete-stale --json`: pass; synthetic stale metadata removed and matching context directory deleted.
- `git diff --check`: pass.

## Revision notes

Revision 2 addresses verifier findings:

- `V-41-ARCH-001`: added concrete 7-day stale metadata TTL, 24-hour ephemeral launch-context TTL, dry-run/list/delete cleanup behavior, and exact tmux targeting rules.
- `V-41-ARCH-002`: added explicit launch-context privacy boundary and planned tests to ensure state/context files do not contain raw prompts, operator idea text, tokens, secrets, or transcripts.

Backend revision 2 addresses verifier findings:

- `V-41-BE-001`: stale tmux groups now summarize as `error` and `/launch` reuses the stale group instead of silently relaunching; added stale no-relaunch regression test.
- `V-41-BE-002`: persisted/restored pane metadata now includes provider, `modelProfileId`, and effort; restart test asserts restored groups keep these fields and omit command/prompt data.
- `V-41-BE-003`: moved recovery-specific restore/reconcile/attach/replay orchestration into `term-control-center/server/sessionRecovery.ts`.

Frontend revision 2 addresses verifier findings:

- `V-41-FE-001`: recovered/recovering recoverability is now preserved in board labels and terminal pane state instead of collapsing to generic running/connecting.
- `V-41-FE-002`: Restart is disabled for attached recovered workspace panes to prevent profile-only unsupervised relaunch or live-session duplication; Close and Kill remain available.

Validation/docs notes:

- Added runbook documentation and cleanup script per acceptance criterion 9.
- Cleanup script uses only exact tmux `has-session`/`kill-session -t =<sessionName>` targets from metadata; no broad kill commands.
- Full live-browser smoke was not run in this terminal-only harness. Equivalent local validation is covered by automated tmux restart/stale tests plus board/term static guardrail tests. Manual browser smoke remains recommended before deployment.
- Local smoke evidence: `recovers tmux launch groups after service restart without duplicate relaunch`, `does not relaunch matching stale tmux groups`, `cleanup keeps paneSessionIds consistent for partially stale groups`, board token-merge/recovery guardrails, and terminal recovery-state guardrails all pass.
- Steward pre-final hygiene review: clean; no placement/artifact cleanup needed before final verifier bug-check.
- Final bug-check revision addressed `V-41-FINAL-001`: partial stale cleanup now rewrites `paneSessionIds` from remaining panes; regression test added.
- Final verifier bug-check: approved/passed at revision 2.

## Next implementation slice after verifier approval

Validation/docs checkpoint slice:

1. Add/update runbook documentation for restart-survival strategy, local state location, cleanup behavior, deployment implications, and known limits.
2. Add safe cleanup tooling/API if required by verifier for the docs checkpoint.
3. Run final automated validation plus manual restart/stale smoke test where possible.
4. Request Steward structure/hygiene review before final verifier bug-check because this task added server modules, tests, board UX, and run artifacts.
