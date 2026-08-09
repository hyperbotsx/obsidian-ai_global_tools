# Coder Handoff

## Task

- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/97`
- PRD: `GitHub issue #97 (canonical PRD source)`
- Branch: `feat/frontend-agent-live-chrome-viewer-97`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-harness`

## Scope

Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer`
Verifier socket: `not used`
Preview target: `ops.evono.me / local term-control-center surfaces as allowed by PRD validation`
Preview URL: `https://ops.evono.me`
Preview deploy command: `not run yet`
Browser QA / DevTools required: `yes`
Browser QA target URL/path: `Chrome/noVNC live viewer for frontend-expert delegate`

Allowed paths:

- `term-control-center/server/**` for browser feed backend, launch wiring, tmux/session visibility, and guarded routes
- `term-control-center/src/**` for viewer UI, toolbar wiring, layout, and styles
- `term-control-center/shared/**` for protocol/launcher metadata if required
- `term-control-center/tests/**` for targeted regression coverage
- `scripts/agentops/**` for Claude/coms label propagation and deploy-safe patch hooks
- `pipeline-diagram/deploy/**` only if needed for deploy-time patch hardening
- `term-control-center/README.md` or scoped docs only if implementation changes require them

Explicit non-goals:

- Public exposure of Chrome/CDP/VNC/terminal endpoints
- Logging or committing passwords, 2FA codes, cookies, tokens, screenshots, raw transcripts, or other private auth artifacts
- Product code, trading/backtests, unrelated navigation rewrites, or non-AgentOps repos

Stop condition for this slice: checkpoint 6 verifier approval for final regression/security is received, then request the verifier's final bug-check before any PR, merge, deploy, or closeout automation.

## Dirty Tree Before Editing

- `dev-plans/prd-backlog.md` (pre-existing unrelated dirty timestamp update carried into checkpoint 5; not touched in this slice)
- Checkpoint 5 resumed with the branch ahead of `origin/main` by 1 commit and no other pre-existing dirty scoped files besides `dev-plans/prd-backlog.md`.
- Checkpoint 6 resumed with `git status --short --branch --untracked-files=all` clean and branch ahead of `origin/main` by 2 commits at `fae9947`.

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Chrome launch and safety | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| 2 | noVNC/full-display backend | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| 3 | Viewer UI | `approved` revision 1 | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| 4 | Visible delegate pane | `approved` revision 1 | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| 5 | Coms label/deploy | `approved` revision 1 | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| 6 | Final regression/security | `approved` revision 2 | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |
| Final bug-check | `after full implementation` | `approved` per compact checkpoint 6 revision 2 verdict (`bug_check_status: passed`) | `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md` |

## Changed Files

Checkpoint 1 approved slice retained:

- `term-control-center/server/browserFeed.ts`: feed config now carries control-mode/capture-pause/runtime state in addition to the checkpoint 1 safety guards.
- `term-control-center/server/frontendBrowserLaunch.ts`: frontend-expert browser env/MCP helpers from checkpoint 1 remain unchanged in this slice.
- `term-control-center/server/launchPlan.ts`: checkpoint 1 frontend-expert Claude delegation wiring remains unchanged in this slice.
- `term-control-center/tests/browserFeed.test.ts`: extended from checkpoint 1 with runtime warning, control-mode, and capture-pause assertions.
- `term-control-center/tests/frontendBrowserLaunch.test.ts`: checkpoint 1 regression coverage retained unchanged.
- `term-control-center/tests/launchPlan.test.ts`: checkpoint 1 regression coverage retained unchanged.

Checkpoint 2 backend slice:

- `term-control-center/server/browserCdpProxy.ts`: upgraded the local CDP proxy to track and close live proxy sockets/requests when human-control pauses delegate browser access.
- `term-control-center/server/browserControlState.ts`: new durable control-lease state manager for `agent-control`, `human-control`, and `view-only`, now refactored into small helpers for KISS compliance.
- `term-control-center/server/browserNovncPage.ts`: new guarded noVNC HTML shell with embedded controls for human-control lease switching and status display, split into smaller page helpers.
- `term-control-center/server/browserRuntime.ts`: new noVNC/full-display backend runtime for guarded readiness, managed Chrome/display/VNC lifecycle orchestration, and websocket bridge wiring, now split into smaller helpers.
- `term-control-center/server/browserRuntimeSupport.ts`: shared browser-runtime support helpers for startup waiting, process cleanup, token/origin checks, and Chrome args.
- `term-control-center/server/browserRuntimeSurface.ts`: separated browser-feed route/summary/upgrade surface so the core runtime stays within the file-size KISS cap.
- `term-control-center/server/browserScreencast.ts`: new CDP screencast fallback transport with frame acking, reconnect handling, pause-on-human-control, and smaller KISS-compliant helpers.
- `term-control-center/server/browserStreamBackpressure.ts`: bounded slow-client policy for noVNC and CDP fallback streaming.
- `term-control-center/server/index.ts`: browser-feed routes and websocket upgrades now delegate to the browser runtime instead of returning 501 stubs.
- `term-control-center/tests/browserRuntime.test.ts`: new integration coverage for noVNC websocket proxying, noVNC cache headers, CDP screencast frames/acks, human-control proxy blocking, disconnect cleanup, and explicit runtime fallback warnings.
- `term-control-center/tests/browserStreamBackpressure.test.ts`: regression coverage for slow-client VNC cleanup and CDP frame dropping.
- `term-control-center/tests/server.test.ts`: updated guarded browser-feed route expectations from 501 stubs to authenticated fallback-state JSON.

Checkpoint 3 viewer UI slice:

- `term-control-center/src/BrowserPane.tsx`: new in-app live Chrome viewer that polls the guarded browser feed, embeds noVNC through proxied assets/websocket paths, supports CDP read-only frame fallback, exposes control-mode actions, shows status/fps/capture/lease/fallback state, and keeps human-auth capture pause guidance visible.
- `term-control-center/src/browserPaneState.ts`: shared browser-viewer state helpers for mode gating, websocket URL construction, status text, FPS derivation, and control button enablement.
- `term-control-center/src/App.tsx`: wires browser viewer state into the existing Allotment cockpit, opens terminal + Chrome split-screen from a frontend-expert pane, supports Chrome-only focused/full-screen mode using the embedded shell styling, and keeps hidden terminal panes mounted instead of killing sessions.
- `term-control-center/src/TerminalPane.tsx`: adds the frontend-expert-only `Chrome` toolbar button next to the pane label without changing destructive pane controls.
- `term-control-center/src/styles.css`: adds browser viewer, split/full-screen, toolbar, iPad/coarse-pointer, and compact embedded styles while preserving existing terminal/diff layout.
- `term-control-center/tests/browserPaneState.test.ts`: new unit coverage for noVNC/CDP gating, status text, control button state, proxy-prefixed websocket URLs, and CDP FPS/frame helpers.
- `term-control-center/tests/termBasePath.test.ts`: static regression coverage for `/term` proxy path handling, frontend-expert toolbar wiring, browser focused mode, and hidden-session preservation.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/coder-handoff.md`: updated checkpoint 3 scope, file list, validation, and status.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/decision-log.md`: checkpoint 3 ready-for-verifier entry.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/review-request-r5-checkpoint-3.json`: verifier review request payload for checkpoint 3.

Checkpoint 4 visible delegate slice:

- `term-control-center/server/launchPlan.ts`: frontend-expert Claude delegation prompt now explicitly uses `tmux_display="pane"` with `autoclose=true`, scopes the visible split to operator observability, and preserves the dedicated Chrome/control-mode fail-closed guidance.
- `term-control-center/tests/launchPlan.test.ts`: adds regression coverage that frontend-expert delegates use the visible autoclosing tmux pane and non-frontend peers do not inherit `tmux_display="pane"`.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/coder-handoff.md`: updated checkpoint 4 scope, research, validation, and status.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/decision-log.md`: checkpoint 4 ready-for-verifier entry.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/review-request-r6-checkpoint-4.json`: verifier review request payload for checkpoint 4.

Checkpoint 5 coms label/deploy slice:

- `term-control-center/server/launchPlan.ts`: `PI_COMS_MODEL_LABEL` now uses the configured Claude profile label, normalized to operator-facing labels like `Claude Opus 4.8`, instead of lower-case raw model ids like `Claude opus`.
- `scripts/agentops/pi-agent.sh`: role launches now run the pi-coms label patch best-effort before `exec pi` while preserving inherited `PI_COMS_MODEL_LABEL` and `PI_COMS_DIR` in the pane environment.
- `scripts/agentops/patch-pi-coms-local.sh`: patching now scans managed and temporary Pi npm extension caches under `.pi/agent` and `.hyper-pi`, verifies the package manifest, deduplicates real targets, patches partial/upstream states idempotently, and writes atomically.
- `term-control-center/tests/launchPlan.test.ts`: adds regression coverage for the normalized Claude coms label on Claude-backed launch plans and frontend-expert panes.
- `term-control-center/tests/agentopsComsLabel.test.ts`: new targeted regression coverage for temporary extension cache patching/idempotency, pi-agent env propagation, tmux env propagation, and the patch hook staying label-preserving.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/coder-handoff.md`: updated checkpoint 5 scope, research, validation, and status.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/decision-log.md`: checkpoint 5 ready-for-verifier entry.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/review-request-r7-checkpoint-5.json`: verifier review request payload for checkpoint 5.

Checkpoint 6 final regression/security validation slice:

- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/coder-handoff.md`: updated checkpoint 6 validation evidence, scope, status, and revision log.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/decision-log.md`: checkpoint 6 ready-for-verifier entry.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/review-request-r8-checkpoint-6.json`: verifier review request payload for checkpoint 6 revision 1.

Checkpoint 6 revision 2 bounded scope cleanup:

- `dev-plans/prd-backlog.md`: reverted to `origin/main` content in commit `3685ca7` to address `CHK6-SCOPE-001`; the file is no longer present in `git diff origin/main...HEAD`.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/coder-handoff.md`: updated revision 2 evidence.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/decision-log.md`: checkpoint 6 revision 2 ready-for-verifier entry.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/review-request-r9-checkpoint-6-fix.json`: verifier review request payload for checkpoint 6 revision 2.

## Validation

- `npm --prefix term-control-center run typecheck`: `passed`
- `npm --prefix term-control-center run build`: `passed` (existing Vite chunk-size warning only; build succeeded)
- `npm --prefix term-control-center run test`: `passed (405 tests)`
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/browserRuntime.test.ts tests/browserStreamBackpressure.test.ts tests/server.test.ts tests/browserPaneState.test.ts tests/termBasePath.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts`: `passed (103 tests)`
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launcher.test.ts tests/agentopsComsLabel.test.ts tests/launchPlan.test.ts`: `passed (38 tests)`; confirms implementation peer-role launch defaults, coder/verifier/researcher/steward contract coverage, pi-agent wrapper behavior, and coms label env propagation.
- `bash -n scripts/agentops/pi-agent.sh scripts/agentops/patch-pi-coms-local.sh`: `passed`
- Static regression/security check for browser-feed locality, noVNC/CDP gating, human-control capture pause, noVNC `no-store`, display-label-only coms env propagation, and absence of public browser/CDP/VNC bind patterns: `passed`
- Privacy artifact scan over branch diff for secret/cookie/screenshot/recording/raw-transcript artifact paths and common secret literals: `passed`
- `git diff --check`: `passed`
- `git diff --name-only origin/main...HEAD -- dev-plans/prd-backlog.md`: `passed` (no output after cleanup commit `3685ca7`)
- `git status --short --branch --untracked-files=all`: clean except branch ahead of `origin/main` by 2 commits before checkpoint 6 artifact updates; after bounded scope cleanup, branch is ahead by 3 commits with only run artifact updates and verifier report dirty.
- Manual live noVNC/iPad/frontend-expert/coms-panel smoke: `not run in this checkpoint`; automated and static validation confirms guards and label propagation. Live deployment/browser smoke remains blocked until checkpoint 6 and final bug-check approvals.

## Assumptions

- `origin/main` was already current after `git fetch origin main --quiet` during checkpoint 1 work.
- `coder` identity is this pane launched via `scripts/agentops/pi-agent.sh coder` in project/worktree `agentops-harness`, i.e. `coder@agentops-harness`.
- `coms_list` confirmed live local `researcher`, `steward`, and `verifier` peers in the `agentops-harness` pool before checkpoint 5 research/review requests.
- Research-first consults for tmux visible delegate behavior and pi-coms label propagation were completed before their respective implementation slices.
- Managed runtime defaults launch local `Xvfb`, `x11vnc`, Chrome, and the guarded CDP proxy; `TERM_CONTROL_BROWSER_RUNTIME_MANAGED=0` remains an explicit safe escape hatch for externally managed local test fixtures only.
- noVNC HTML is token-bearing and therefore must remain `Cache-Control: no-store` and `Cross-Origin-Resource-Policy: same-origin`.
- The React viewer builds its noVNC iframe with `/term`-prefixed asset and websocket paths when hosted behind the authenticated AgentOps `/term/` proxy; it does not expose VNC/CDP publicly or persist frames.

## Research Freshness Consult

- Date: `2026-06-25`
- Peer: `researcher`
- Summary:
  - Use `chrome-devtools-mcp` attached with `--browserUrl=http://127.0.0.1:9222` (or a local gated proxy in front of that port), not `claude --chrome`, for deterministic attachment to the launched dedicated Chrome session.
  - Launch Chrome on its own display with a non-default `--user-data-dir`; Chrome 136+ ignores remote debugging on the default profile.
  - Use embedded noVNC as the primary human surface; keep CDP screencast fallback-only because Chrome DevTools MCP screencast remains experimental.
  - Human-auth mode should detach/disable browser MCP access and stop screenshot/screencast/frame capture before handoff; delegate reasoning should be exposed via a read-only transcript/tmux mirror, not remote control.
  - iPad/iOS is supported by noVNC, but keyboard/fullscreen behavior has caveats; prefer `vnc.html`-level touch support patterns over `vnc_lite.html`.
- Sources cited by researcher:
  - Chrome remote debugging security note (2025-03-17): `https://developer.chrome.com/blog/remote-debugging-port`
  - Chrome DevTools MCP docs/README: `https://developer.chrome.com/docs/devtools/agents/get-started`, `https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/README.md`
  - Claude Code Chrome docs / CLI reference: `https://code.claude.com/docs/en/chrome`, `https://docs.anthropic.com/en/docs/claude-code/cli-reference`
  - noVNC docs/issues: `https://github.com/novnc/noVNC/blob/master/README.md`, `https://novnc.com/noVNC/docs/EMBEDDING.html`, `https://github.com/novnc/noVNC/issues/1996`, `https://github.com/novnc/noVNC/issues/878`

### Checkpoint 4 visible delegate consult

- Date: `2026-06-25`
- Peer: `researcher`
- Summary:
  - Use `tmux_display="pane"` only in the frontend-expert `claude_agent` delegation prompt, keep `autoclose=true`, and avoid a global `PI_CLAUDE_AGENT_TMUX_DISPLAY=pane` override.
  - The current pi-claude-agent tmux backend defaults to `detached`; `tmux_display="pane"` calls a visible `tmux split-window -d`, which makes the delegate visible without stealing focus.
  - Do not add a new Term Control Center input/control route for checkpoint 4; a read-only tmux attach mirror would require extra plumbing and can be deferred unless the visible split is rejected.
  - Risk: a visible tmux split is not a cryptographic read-only mirror, so the prompt now scopes it to operator observability and tells the frontend-expert not to ask the operator to type into the delegate pane.
- Sources cited by researcher:
  - pi-claude-agent README/source, package `v0.1.1`, checked `2026-06-25`: `https://github.com/liamvinberg/pi-claude-agent`
  - Claude Code permission modes docs, checked `2026-06-25`: `https://code.claude.com/docs/en/permission-modes.md`
  - tmux manual / read-only attach reference, checked `2026-06-25`: `https://github.com/tmux/tmux/blob/master/tmux.1`

### Checkpoint 5 pi-coms label propagation consult

- Date: `2026-06-26`
- Peer: `researcher`
- Summary:
  - Expand `patch-pi-coms-local.sh` scanning to include managed and temporary npm package copies under `.pi/agent` and `.hyper-pi`, plus `PI_COMS_LOCAL_DIR` and nvm/global fallbacks.
  - Run the patch best-effort from `pi-agent.sh` before `exec pi` because role launch is the last reliable local hook before coms registration; warn rather than failing normal launches for a display-only label patch.
  - A first launch after an extension cache wipe may still create a fresh temp package after the pre-launch patch runs, so repeated launch/deploy patching remains necessary.
  - Verify the package manifest, dedupe real targets, patch idempotently, and treat upstream/native `PI_COMS_MODEL_LABEL` support as already patched.
- Sources cited by researcher:
  - Local `scripts/agentops/pi-agent.sh` extension invocation: `-e npm:@giovani-junior-dev/pi-coms-local@0.1.1`
  - Pi package docs/source summary: npm extensions may live under user npm installs and temporary `<agentDir>/tmp/extensions/npm/*/node_modules/<pkg>` paths.
  - Local pi-coms source uses `ctx.model.id` for displayed registry/ping model while routing uses project/name/session endpoint, not the model label.
  - npm latest checked by researcher: `@giovani-junior-dev/pi-coms-local@0.1.1`, modified `2026-05-22`.

## Known Gaps

- Checkpoint 3 is verifier-approved; live noVNC/iPad manual smoke was not run in that slice.
- Checkpoint 4 visible delegate pane is verifier-approved; no live frontend-expert consult was launched in that slice.
- Checkpoint 5 coms label/deploy hardening is verifier-approved; live coms panel smoke was not run in that slice.
- Checkpoint 6 final regression/security validation revision 2 is verifier-approved after addressing `CHK6-SCOPE-001`.
- Final verifier bug-check is approved per the compact checkpoint 6 revision 2 verdict (`bug_check_status: passed`).
- Final PR/merge/deploy/test-instruction automation was not started because the current operator instruction forbids PR creation, merge, deployment, and public browser/CDP/VNC exposure during this continuation.

## Verifier Pairing

- Required: `yes`
- Reason: `User explicitly required coder-verifier workflow with PRD checkpoint reviews and final bug-check.`
- Coder ready file: `not used`
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-97-frontend-agent-live-chrome-viewer/verifier-report.md`

## Coder Decision

`final_verifier_bug_check_approved`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1 | `checkpoint 1 revision 3 addressing CHK1-SAFE-001 and CHK1-KISS-001` | `term-control-center/server/browserFeed.ts`, `term-control-center/server/frontendBrowserLaunch.ts`, `term-control-center/server/launchPlan.ts`, `term-control-center/tests/browserFeed.test.ts`, `term-control-center/tests/frontendBrowserLaunch.test.ts`, `term-control-center/tests/launchPlan.test.ts`, run artifacts | `npm --prefix term-control-center ci`; `npm --prefix term-control-center run typecheck`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts`; `git diff --check -- term-control-center/server/browserFeed.ts term-control-center/server/frontendBrowserLaunch.ts term-control-center/server/launchPlan.ts term-control-center/tests/browserFeed.test.ts term-control-center/tests/frontendBrowserLaunch.test.ts term-control-center/tests/launchPlan.test.ts` | `ready_for_verifier` |
| 2 | `checkpoint 2 initial noVNC/full-display backend implementation` | `term-control-center/server/browserFeed.ts`, `term-control-center/server/browserCdpProxy.ts`, `term-control-center/server/browserControlState.ts`, `term-control-center/server/browserNovncPage.ts`, `term-control-center/server/browserRuntime.ts`, `term-control-center/server/browserRuntimeSupport.ts`, `term-control-center/server/browserScreencast.ts`, `term-control-center/server/index.ts`, `term-control-center/tests/browserFeed.test.ts`, `term-control-center/tests/browserRuntime.test.ts`, `term-control-center/tests/server.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/browserRuntime.test.ts tests/server.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts`; `git diff --check -- term-control-center/server/browserFeed.ts term-control-center/server/browserCdpProxy.ts term-control-center/server/browserControlState.ts term-control-center/server/browserNovncPage.ts term-control-center/server/browserRuntime.ts term-control-center/server/browserRuntimeSupport.ts term-control-center/server/browserScreencast.ts term-control-center/server/index.ts term-control-center/tests/browserFeed.test.ts term-control-center/tests/browserRuntime.test.ts term-control-center/tests/server.test.ts` | `revision_requested` |
| 3 | `checkpoint 2 revision 2 addressing CHK2-SEC-001 and CHK2-RESOURCE-001 plus partial KISS/fallback follow-up` | `term-control-center/server/browserFeed.ts`, `term-control-center/server/browserCdpProxy.ts`, `term-control-center/server/browserControlState.ts`, `term-control-center/server/browserNovncPage.ts`, `term-control-center/server/browserRuntime.ts`, `term-control-center/server/browserRuntimeSupport.ts`, `term-control-center/server/browserRuntimeSurface.ts`, `term-control-center/server/browserScreencast.ts`, `term-control-center/server/browserStreamBackpressure.ts`, `term-control-center/server/index.ts`, `term-control-center/tests/browserFeed.test.ts`, `term-control-center/tests/browserRuntime.test.ts`, `term-control-center/tests/browserStreamBackpressure.test.ts`, `term-control-center/tests/server.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/browserRuntime.test.ts tests/browserStreamBackpressure.test.ts tests/server.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts`; `git diff --check -- term-control-center/server/browserFeed.ts term-control-center/server/browserCdpProxy.ts term-control-center/server/browserControlState.ts term-control-center/server/browserNovncPage.ts term-control-center/server/browserRuntime.ts term-control-center/server/browserRuntimeSupport.ts term-control-center/server/browserRuntimeSurface.ts term-control-center/server/browserScreencast.ts term-control-center/server/browserStreamBackpressure.ts term-control-center/server/index.ts term-control-center/tests/browserFeed.test.ts term-control-center/tests/browserRuntime.test.ts term-control-center/tests/browserStreamBackpressure.test.ts term-control-center/tests/server.test.ts` | `ready_for_verifier` |
| 4 | `checkpoint 2 revision 3 addressing CHK2-FALLBACK-001 and CHK2-KISS-001` | `term-control-center/server/browserFeed.ts`, `term-control-center/server/browserControlState.ts`, `term-control-center/server/browserNovncPage.ts`, `term-control-center/server/browserRuntime.ts`, `term-control-center/server/browserRuntimeSurface.ts`, `term-control-center/tests/browserRuntime.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/browserRuntime.test.ts tests/browserStreamBackpressure.test.ts tests/server.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts`; `git diff --check -- term-control-center/server/browserFeed.ts term-control-center/server/browserCdpProxy.ts term-control-center/server/browserControlState.ts term-control-center/server/browserNovncPage.ts term-control-center/server/browserRuntime.ts term-control-center/server/browserRuntimeSupport.ts term-control-center/server/browserRuntimeSurface.ts term-control-center/server/browserScreencast.ts term-control-center/server/browserStreamBackpressure.ts term-control-center/server/index.ts term-control-center/tests/browserFeed.test.ts term-control-center/tests/browserRuntime.test.ts term-control-center/tests/browserStreamBackpressure.test.ts term-control-center/tests/server.test.ts` | `approved` |
| 5 | `checkpoint 3 initial viewer UI implementation` | `term-control-center/src/BrowserPane.tsx`, `term-control-center/src/browserPaneState.ts`, `term-control-center/src/App.tsx`, `term-control-center/src/TerminalPane.tsx`, `term-control-center/src/styles.css`, `term-control-center/tests/browserPaneState.test.ts`, `term-control-center/tests/termBasePath.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserPaneState.test.ts tests/termBasePath.test.ts tests/browserFeed.test.ts tests/browserRuntime.test.ts tests/browserStreamBackpressure.test.ts tests/server.test.ts tests/frontendBrowserLaunch.test.ts tests/launchPlan.test.ts`; `git diff --check` | `approved` |
| 6 | `checkpoint 4 initial visible delegate implementation` | `term-control-center/server/launchPlan.ts`, `term-control-center/tests/launchPlan.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchPlan.test.ts`; `git diff --check -- term-control-center/server/launchPlan.ts term-control-center/tests/launchPlan.test.ts`; `git diff --check` | `approved` |
| 7 | `checkpoint 5 initial coms label/deploy hardening` | `scripts/agentops/pi-agent.sh`, `scripts/agentops/patch-pi-coms-local.sh`, `term-control-center/server/launchPlan.ts`, `term-control-center/tests/launchPlan.test.ts`, `term-control-center/tests/agentopsComsLabel.test.ts`, run artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/agentopsComsLabel.test.ts tests/launchPlan.test.ts`; `bash -n scripts/agentops/pi-agent.sh scripts/agentops/patch-pi-coms-local.sh`; `git diff --check -- scripts/agentops/pi-agent.sh scripts/agentops/patch-pi-coms-local.sh term-control-center/server/launchPlan.ts term-control-center/tests/launchPlan.test.ts term-control-center/tests/agentopsComsLabel.test.ts`; `git diff --check` | `approved` |
| 8 | `checkpoint 6 final regression/security validation` | run artifacts only | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `npm --prefix term-control-center run test`; targeted browser-feed/noVNC/CDP/launch/coms tests; implementation launch contract tests; `bash -n scripts/agentops/pi-agent.sh scripts/agentops/patch-pi-coms-local.sh`; static browser exposure/control/capture/coms checks; privacy artifact scan; `git diff --check` | `revision_requested` (`CHK6-SCOPE-001`) |
| 9 | `checkpoint 6 revision 2 addressing CHK6-SCOPE-001` | `dev-plans/prd-backlog.md`, run artifacts | `git diff --name-only origin/main...HEAD -- dev-plans/prd-backlog.md` (no output); `git diff --check` | `approved`; compact verdict also returned `bug_check_status: passed` |
