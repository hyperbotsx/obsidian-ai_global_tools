# Decision Log

## Checkpoint 1 — Architecture checkpoint

- Timestamp: `2026-06-16T14:31:09Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Pre-existing dirty files: none (`git status --short --branch` showed only the branch before editing).
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: local-only terminal control center spike.
- Browser QA / DevTools: not required for checkpoint 1.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Validation run before review send:

- `git diff --check`: pass.

Forbidden without separate approval:

- `pipeline-diagram/` integration.
- `src/agentops_harness/**` and Python review-service behavior.
- nginx/deploy/public bind changes.
- Multi-pane/session persistence/auth/backpressure work from later phases.
- PR creation, merges, deployment, secrets, raw transcripts.

### Checkpoint plan

1. Architecture checkpoint — current slice.
2. Terminal checkpoint — one xterm pane ↔ one PTY with input/output/resize/kill.
3. Final verifier bug-check.

### Implementation decisions

- Isolated the spike in a new `term-control-center/` subproject to avoid touching the existing Python package and static board frontend during Phase 1.
- Reserved a single local service port (`3032`) for the Node backend that will own both HTTP and WebSocket traffic.
- Chose a narrow JSON protocol with `INIT`, `INPUT`, `RESIZE`, and `KILL` plus `READY`, `OUTPUT`, `EXIT`, and `ERROR` responses.
- Scoped the Phase 1 PTY lifecycle to one PTY per socket; socket close will kill the PTY until detach/reconnect work is implemented in a later checkpoint.
- Deferred Allotment, WebGL, reconnect, fan-out, auth token, and backpressure work to later PRD checkpoints.

## Checkpoint 2 — Terminal checkpoint

- Timestamp: `2026-06-16T14:54:20Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Pre-existing dirty files at continuation start: `.gitignore`, `term-control-center/`, and `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/`.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; automated PTY/WebSocket smoke covers the requested Phase 1 proof.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Forbidden without separate approval:

- `pipeline-diagram/` integration.
- `src/agentops_harness/**` and Python review-service behavior.
- nginx/deploy/public bind changes.
- Split-pane, detach/reconnect, multi-device, auth-token, WebGL, and backpressure work from later phases.
- PR creation, merges, deployment, secrets, raw transcripts.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.

### Implementation decisions

- Resolved `TCC-ARCH-001` by keeping Node HTTP+WS on reserved port `3032` and moving Vite dev to `3033` with proxying for `/health` and `/ws`.
- Resolved `TCC-ARCH-002` by keeping server compile output at `build/server/index.js`, matching `npm start`.
- Built the Phase 1 backend as one PTY per WebSocket connection. `INIT` spawns, `INPUT` writes, `RESIZE` clamps and forwards dimensions, and `KILL`/socket close kill and remove the session.
- Built a React xterm pane that opens in a measurable host, loads `FitAddon`, sends INIT and RESIZE messages, streams input/output outside React state, and exposes Kill/Restart actions.
- Added integration smoke coverage that starts the backend, opens a WebSocket, verifies PTY output, verifies resize through `stty size`, sends `KILL`, and asserts the session registry is empty.
- Kept auth, reconnect, fan-out, Allotment, WebGL, and backpressure deferred to later PRD phases.

## Revision 3 — KISS refactor for `TCC-TERM-001`

- Timestamp: `2026-06-16T15:00:11Z`
- Verifier finding addressed: `TCC-TERM-001`.
- Bounded path: `term-control-center/src/TerminalPane.tsx` plus run artifacts.

### Implementation decisions

- Removed the unused `fitRef` lifecycle ref from `TerminalPane.tsx`.
- Reduced helper plumbing by passing terminal event handlers as a small object to `wireTerminal`.
- Kept Phase 1 behavior unchanged: xterm input/output, fit/resize, kill, and restart paths remain intact.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.

## Verifier approval

- Timestamp: `2026-06-16T15:00:11Z`
- Checkpoint: `2 - Terminal checkpoint`
- Revision approved: `3`
- Decision: `approved`
- Open findings: `0`
- Bug-check status: `passed`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md`

## Checkpoint 3 — Split-pane checkpoint

- Timestamp: `2026-06-16T15:26:28Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Pre-existing dirty files at continuation start: approved Phase 1 files under `.gitignore`, `term-control-center/`, and the run artifact folder.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and backend health smoke passed.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Forbidden without separate approval:

- `pipeline-diagram/` integration.
- `src/agentops_harness/**` and Python review-service behavior.
- nginx/deploy/public bind changes.
- Detach/reconnect, multi-device, auth-token, WebGL, command palette, and backpressure work from later phases.
- PR creation, merges, deployment, secrets, raw transcripts.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Added Allotment as the split-pane substrate and imported its stylesheet at the React entrypoint.
- Implemented flat multi-pane state with stable pane IDs so adding, splitting, focusing, and resizing do not remount existing terminal panes.
- Added `New pane`, `Split pane`, close, focus, restart, and split direction toggle actions.
- Kept close semantics aligned with Phase 1 lifecycle: unmounting a terminal pane closes its WebSocket and backend socket cleanup kills the PTY.
- Persisted Allotment sizes to localStorage on drag end rather than every drag event.
- Deferred nested docking, reconnect, fan-out, auth, WebGL, command palette, and backpressure to later PRD phases.

## Revision 5 — Lifecycle fix for `TCC-SPLIT-001`

- Timestamp: `2026-06-16T15:30:46Z`
- Verifier finding addressed: `TCC-SPLIT-001`.
- Bounded paths: `term-control-center/src/App.tsx`, `term-control-center/src/TerminalPane.tsx`, and run artifacts.

### Implementation decisions

- Moved the latest `onStatus` callback into a `useRef` so `TerminalPane` can report status without making xterm/PTy setup depend on parent callback identity.
- Changed the terminal startup effect to mount once per pane instance, preserving PTY/xterm instances across parent rerenders, focus changes, split actions, and layout size changes.
- Updated pane status transitions to return the existing pane array when the status is unchanged, avoiding avoidable parent rerenders.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

## Verifier approval — Split-pane checkpoint

- Timestamp: `2026-06-16T15:30:46Z`
- Checkpoint: `3 - Split-pane checkpoint`
- Revision approved: `5`
- Decision: `approved`
- Open findings: `0`
- Bug-check status: `passed`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md`

## Checkpoint 4 — Lifecycle checkpoint

- Timestamp: `2026-06-16T15:43:31Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Pre-existing dirty files at continuation start: approved prior checkpoint files under `.gitignore`, `term-control-center/`, and the run artifact folder.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and backend health smoke passed.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Forbidden without separate approval:

- `pipeline-diagram/` integration.
- `src/agentops_harness/**` and Python review-service behavior.
- nginx/deploy/public bind changes.
- WebGL, command palette, service-wide auth/origin layer, and backpressure work from later phases.
- PR creation, merges, deployment, secrets, raw transcripts.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Moved the backend from socket-owned PTYs to a session registry keyed by server-generated session IDs.
- Added per-session attach tokens to permit refresh/reconnect without exposing arbitrary command creation in query params.
- Added detach timers so socket close keeps PTYs alive for a bounded TTL; explicit close/restart still send `KILL`.
- Added bounded in-memory output replay and replay markers for reattached clients.
- Added frontend persistence of pane `sessionId` and `attachToken` so browser refresh can reattach within the TTL.
- Added tests for reconnect replay and TTL expiry in addition to the existing PTY output/resize/kill smoke.

## Revision 7 — Last-pane close fix for `TCC-LIFE-001`

- Timestamp: `2026-06-16T15:47:59Z`
- Verifier finding addressed: `TCC-LIFE-001`.
- Bounded path: `term-control-center/src/App.tsx` plus run artifacts.

### Implementation decisions

- Changed last-pane close to replace the killed pane with a fresh pane and make that pane active.
- Multi-pane close behavior remains unchanged: removing an active pane focuses the next remaining pane.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

## Verifier approval — Lifecycle checkpoint

- Timestamp: `2026-06-16T15:47:59Z`
- Checkpoint: `4 - Lifecycle checkpoint`
- Revision approved: `7`
- Decision: `approved`
- Open findings: `0`
- Bug-check status: `passed`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md`

## Checkpoint 5 — Performance checkpoint

- Timestamp: `2026-06-16T15:56:36Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Pre-existing dirty files at continuation start: approved prior checkpoint files under `.gitignore`, `term-control-center/`, and the run artifact folder.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and backend health smoke passed.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Forbidden without separate approval:

- `pipeline-diagram/` integration.
- `src/agentops_harness/**` and Python review-service behavior.
- nginx/deploy/public bind changes.
- Command palette, service-wide auth/origin layer, and visual polish work from later phases.
- PR creation, merges, deployment, secrets, raw transcripts.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Added `@xterm/addon-webgl` and only activates it when WebGL2 is available.
- Disposes the WebGL addon on context loss so xterm falls back to its normal renderer.
- Added `ACK { bytes }` to the protocol and parser.
- Server batches PTY data every short interval before WebSocket fan-out.
- Client sends render ACKs from the xterm `write` callback for non-replay output.
- Server tracks pending bytes and `ws.bufferedAmount`; PTY output pauses above high watermarks and resumes below the low watermark.

## Revision 9 — Backpressure recovery fix for `TCC-PERF-001`

- Timestamp: `2026-06-16T16:02:10Z`
- Verifier finding addressed: `TCC-PERF-001`.
- Bounded paths: `term-control-center/server/index.ts`, `term-control-center/tests/server.test.ts`, and run artifacts.

### Implementation decisions

- Do not count output as live render-pending bytes when no WebSocket clients are attached.
- On attach, reset pending render pressure and resume any paused PTY before replaying buffered output.
- Added an integration test where a detached session emits more than the high watermark, reconnects, receives replay, accepts new input, and is explicitly killed.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

## Checkpoint 6 — Polish checkpoint

- Timestamp: `2026-06-16T16:07:20Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and backend health smoke passed.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Added a command-palette-style quick action surface with button, `Ctrl/Cmd+K`, and Escape/backdrop dismissal.
- Added focus mode by using Allotment pane visibility to show only the active pane when enabled.
- Added persisted dark/light theme tokens.
- Added per-pane status badges and retained active-pane global status.
- Kept the work inside the standalone app; no board modal, nginx, Python service, or deployment changes.

## Revision 11 — Shortcut fix for `TCC-POLISH-001`

- Timestamp: `2026-06-16T16:11:38Z`
- Verifier finding addressed: `TCC-POLISH-001`.
- Bounded path: `term-control-center/src/App.tsx` plus run artifacts.

### Implementation decisions

- Added `event.preventDefault()` when handling `Ctrl/Cmd+K` so the app quick actions palette does not race the browser address/search shortcut.
- Escape dismissal behavior remains unchanged.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite chunk-size warning.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server health smoke on `127.0.0.1:3032/health`: pass.

## Checkpoint 7 — Security and packaging-readiness checkpoint

- Timestamp: `2026-06-16T16:19:51Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and tokenized backend health smoke passed.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite bootstrap/chunk-size warnings.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server tokenized health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Added per-start local auth token generation and optional `TERM_CONTROL_AUTH_TOKEN` override.
- Added `/term-config.js` bootstrap for the browser app to receive the local token.
- Required the token for `/health`, `/sessions`, and `/ws`.
- Added WebSocket origin allowlist for local service/dev origins.
- Added configured cwd existence validation at server startup.
- Added tests for protected REST endpoints and token bootstrap.

## Revision 13 — Bootstrap header fix for `TCC-SEC-001`

- Timestamp: `2026-06-16T16:25:52Z`
- Verifier finding addressed: `TCC-SEC-001`.
- Bounded paths: `term-control-center/server/index.ts`, `term-control-center/tests/server.test.ts`, and run artifacts.

### Implementation decisions

- Added `Cache-Control: no-store` to `/term-config.js`.
- Added `Cross-Origin-Resource-Policy: same-origin` to `/term-config.js`.
- Extended the bootstrap config test to assert both security headers.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite bootstrap/chunk-size warnings.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server tokenized health smoke on `127.0.0.1:3032/health`: pass.

## Transport escalation — verifier non-JSON reply

- Timestamp: `2026-06-16T16:25:52Z`
- Checkpoint: `7 - Security and packaging-readiness checkpoint`
- Revision awaiting recheck: `13`
- Status: code fix for `TCC-SEC-001` implemented and validation passes.
- Coms issue: verifier returned a non-JSON response, then a retry also returned non-JSON (`(see attached image)`) and did not update `verifier-report.md`.
- Workflow decision: needs human/verifier transport intervention per coms contract malformed-reply rule.

## Verifier approval — Security and packaging-readiness checkpoint

- Timestamp: `2026-06-16T16:25:52Z`
- Checkpoint: `7 - Security and packaging-readiness checkpoint`
- Revision approved: `13`
- Decision: `approved`
- Open findings: `0`
- Bug-check status: `passed`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md`

## Checkpoint 8 — Coder/verifier launch profiles

- Timestamp: `2026-06-16T16:57:36Z`
- Source PRD: https://github.com/hyperbotsx/agentops-harness/issues/21
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
- Preview target: backend `http://127.0.0.1:3032`; Vite dev UI `http://127.0.0.1:3033`.
- Browser QA / DevTools: not run; build and tokenized backend health smoke passed.

### Scope confirmation

Allowed for this checkpoint:

- `term-control-center/**`
- `.gitignore`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`

Forbidden without separate approval:

- Copying or vendoring `scripts/agentops/pi-agent.sh` into this repo.
- Arbitrary browser-provided command execution.
- `pipeline-diagram/`, nginx/deploy, Python review-service behavior, PR creation, merge, or deployment.

### Validation run before review send

- `npm --prefix term-control-center run build`: pass; non-fatal Vite bootstrap/chunk-size warnings.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server tokenized health smoke on `127.0.0.1:3032/health`: pass.

### Implementation decisions

- Added allowlisted launch profiles to the protocol: `shell`, `coder`, `verifier`, `researcher`.
- Fresh browser state now defaults to two panes: verifier on the left and coder on the right.
- Coder/verifier/researcher profiles launch `<TERM_CONTROL_WORKTREE>/scripts/agentops/pi-agent.sh <profile>` from the configured target worktree.
- Missing wrapper returns a clear `ERROR` message instead of falling back to arbitrary command execution.
- Restart preserves the pane profile; New Pane creates a normal shell pane.

## Transport escalation — launch-profile checkpoint

- Timestamp: `2026-06-16T16:57:36Z`
- Checkpoint: `8 - Coder/verifier launch profiles`
- Revision awaiting review: `14`
- Status: code implementation complete and validation passes.
- Coms issue: verifier returned non-JSON twice and did not update `verifier-report.md` past revision 13.
- Workflow decision: needs human/verifier transport intervention before checkpoint 8 can be marked verifier-approved.

## Revision 15 — Verifier-requested launch-profile fixes

- Timestamp: `2026-06-16T18:40:00Z`
- Verifier findings addressed: `TCC-PROFILE-001`, `TCC-PROFILE-002`, `TCC-KISS-002`.
- Bounded paths: `term-control-center/package.json`, `term-control-center/src/App.tsx`, `term-control-center/src/TerminalPane.tsx`, and run artifacts.

### Implementation decisions

- Included the pane launch `profile` in `sessionCredentials`, so browser `INIT` now sends `coder`, `verifier`, or `researcher` instead of allowing the server to default to `shell`.
- Added `npm run typecheck` for client and server TypeScript contracts, and made `npm run build` execute typecheck before bundling/emitting.
- Extracted smaller React helpers from `App.tsx` and `TerminalPane.tsx`; both files are under 300 lines.

### Validation run before review send

- `npm --prefix term-control-center run typecheck`: pass.
- `npm --prefix term-control-center run build`: pass; non-fatal Vite bootstrap/chunk-size warnings.
- `npm --prefix term-control-center run test`: pass.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass.
- `git diff --check`: pass.
- Built server tokenized health smoke on `127.0.0.1:3042/health`: pass.
