# Coder Handoff

## Task

- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/21
- PRD: GitHub issue #21 body is the canonical PRD source.
- Branch: `feat/term-control-center-21`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Current checkpoint: `8 - Coder/verifier launch profiles`

## Scope

Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1`
Backend URL: `http://127.0.0.1:3032`
Vite dev URL: `http://127.0.0.1:3033`
Browser QA / DevTools required: optional; no browser tool run in this slice

Allowed paths:

- `term-control-center/**`
- `.gitignore`
- `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/*`
- `/mnt/hyperliquid-data/projects/worktrees/PORTS.md`

Explicit non-goals:

- No pipeline-diagram modal integration yet.
- No nginx/deployment/Python review-service changes.
- No LAN/public bind or production packaging artifact.
- No PR creation, merge, or deployment.
- No arbitrary browser-provided command execution.

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Architecture checkpoint | revision requested then superseded | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 2 | Terminal checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 3 | Split-pane checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 4 | Lifecycle checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 5 | Performance checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 6 | Polish checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 7 | Security and packaging-readiness checkpoint | approved, bug-check passed | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| 8 | Coder/verifier launch profiles: default verifier-left/coder-right, allowlisted wrapper launch, missing-wrapper error | revision 15 ready after verifier-requested fixes | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |
| Final bug-check | after checkpoint 8 approval | pending | `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md` |

## Changed Files

- `.gitignore`: ignores Node dependencies for the new subproject.
- `term-control-center/package.json`: dependencies/scripts for the standalone local app, including client/server typecheck in the build path.
- `term-control-center/package-lock.json`: locked npm dependency graph.
- `term-control-center/index.html`: loads `/term-config.js` before the Vite app bundle.
- `term-control-center/vite.config.ts`: proxies `/term-config.js`, `/health`, `/sessions`, and `/ws` to the local backend in dev.
- `term-control-center/scripts/dev.mjs`: starts Vite and backend watcher together.
- `term-control-center/server/index.ts`: allowlisted launch profiles, `scripts/agentops/pi-agent.sh <role>` launch from configured worktree for coder/verifier/researcher, shell fallback, local token/security, session lifecycle/performance behavior.
- `term-control-center/shared/protocol.ts`: `profile` field on `INIT`, attach fields, ACK, replay marker, validation.
- `term-control-center/src/App.tsx`: default verifier-left/coder-right panes, persisted pane profiles, profile-preserving restart, split/focus/close/theme/actions, and smaller extracted React helpers for KISS compliance.
- `term-control-center/src/TerminalPane.tsx`: sends launch profile in `INIT`, tokenized WebSocket URL, WebGL fallback, ACKs, session attach, input/output/resize/kill behavior, and extracted toolbar/callback helpers for KISS compliance.
- `term-control-center/src/styles.css`: dark/light tokens, command palette, status badges, focus rings, responsive layout.
- `term-control-center/tests/protocol.test.ts`: protocol parser tests for profile, attach fields, ACK, invalid messages.
- `term-control-center/tests/server.test.ts`: token-protected REST tests, missing-wrapper profile error, PTY/lifecycle/performance integration tests.
- `term-control-center/README.md`: current scope, topology, protocol, runtime notes, validation.
- Run artifacts in `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/`.

## New Launch Profile Behavior

- New browser state defaults to two panes:
  - left: `verifier`
  - right: `coder`
- `INIT` accepts only allowlisted profiles: `shell`, `coder`, `verifier`, `researcher`.
- `shell` launches the configured local shell.
- `coder`, `verifier`, and `researcher` launch `<TERM_CONTROL_WORKTREE>/scripts/agentops/pi-agent.sh <profile>`.
- `TERM_CONTROL_WORKTREE` selects the target worktree. If unset, the backend falls back to `TERM_CONTROL_CWD`, option `cwd`, or the parent of `term-control-center`.
- If the target worktree lacks `scripts/agentops/pi-agent.sh`, the backend returns a clear `ERROR` message and does not spawn arbitrary commands.
- Restart preserves a pane's profile; New Pane still creates a normal shell pane.

## Findings Addressed

- `TCC-ARCH-001`, `TCC-ARCH-002`, `TCC-TERM-001`, `TCC-SPLIT-001`, `TCC-LIFE-001`, `TCC-PERF-001`, `TCC-POLISH-001`, `TCC-SEC-001` are addressed in prior approved/recheck-ready revisions.
- `TCC-PROFILE-001`: addressed in revision 15 by including `profile` in `sessionCredentials`, so browser `INIT` sends the pane launch profile.
- `TCC-PROFILE-002`: addressed in revision 15 by adding `npm run typecheck` and making `npm run build` run client/server typecheck before bundling/emitting.
- `TCC-KISS-002`: addressed in revision 15 by extracting smaller React/presentational helpers in `App.tsx` and `TerminalPane.tsx`; files remain under 300 lines.

## Validation

- `npm --prefix term-control-center run typecheck`: pass; client and server TypeScript checks pass.
- `npm --prefix term-control-center run build`: pass; includes typecheck; Vite warns the classic `/term-config.js` bootstrap script cannot be bundled as a module and the app chunk is >500 KB, no build failure.
- `npm --prefix term-control-center run test`: pass; 10 tests pass including profile parsing and missing-wrapper error.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass; 0 vulnerabilities.
- `git diff --check`: pass.
- Built server tokenized health smoke: pass; fetched `/term-config.js`, extracted token, then `/health` returned `{ "ok": true }` with `x-term-token`.

## Assumptions

- The default coder/verifier panes are intended for fresh browser state; existing localStorage pane state remains respected.
- This repo does not include `scripts/agentops/pi-agent.sh`; real coder/verifier launch testing should set `TERM_CONTROL_WORKTREE` to a worktree that has the wrapper, e.g. `/mnt/hyperliquid-data/projects/worktrees/Evonome-data` or `/mnt/hyperliquid-data/projects/worktrees/Evonome-AgentOps`.
- The backend must not copy or vendor the wrapper into `agentops-harness`.

## Known Gaps

- No browser manual QA was run for real pi coder/verifier launch.
- Windows PTY cleanup is not validated in this Linux worktree and remains a PRD acceptance criterion needing native Windows validation.
- Nginx/board modal integration remains out of this standalone local app scope.

## Coms Preflight

- Worktree identity basis: `agentops-term`; branch `feat/term-control-center-21`.
- `PI_COMS_DIR=/tmp/agentops/coms/agentops-term`.
- `coms_list(project="agentops-term")`: live `verifier` present.

## Verifier Pairing

- Required: yes.
- Reason: profile launch expands the terminal control-center behavior and needs final bug-check before browser testing.
- Coder ready file: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/coder-ready.md`
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/verifier-report.md`

## Prior Verifier Verdicts

- Checkpoint 2 revision 3: `approved`; bug-check `passed`.
- Checkpoint 3 revision 5: `approved`; bug-check `passed`.
- Checkpoint 4 revision 7: `approved`; bug-check `passed`.
- Checkpoint 5 revision 9: `approved`; bug-check `passed`.
- Checkpoint 6 revision 11: `approved`; bug-check `passed`.
- Checkpoint 7 revision 13: `approved`; bug-check `passed`.
- Open findings: `0`.

## Coder Decision

`ready_for_verifier`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1-13 | previous PRD checkpoints and fixes | see decision log | approved through checkpoint 7 | `approved` |
| 14 | checkpoint 8 coder/verifier launch profiles | `server/index.ts`, `shared/protocol.ts`, `src/App.tsx`, `src/TerminalPane.tsx`, tests, run artifacts | build/test/audit/diff-check/tokenized health smoke pass | `revision_requested` |
| 15 | verifier-requested checkpoint 8 fixes | `package.json`, `src/App.tsx`, `src/TerminalPane.tsx`, run artifacts | typecheck/build/test/audit/diff-check pass | `ready_for_verifier` |
