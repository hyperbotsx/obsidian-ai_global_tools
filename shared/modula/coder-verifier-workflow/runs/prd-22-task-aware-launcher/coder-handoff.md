# Coder Handoff

## Task

- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/22
- PRD: GitHub issue #22 body
- Branch: `feat/task-aware-split-session-launcher-22`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Scope

Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher`
Verifier socket: not used; pi-coms-local
Preview target: not applicable for current checkpoint
Preview URL: not applicable
Preview deploy command: not applicable
Browser QA / DevTools required: optional for later UI checkpoints
Browser QA target URL/path: local term-control-center / board modal after UI wiring

Allowed paths:

- `term-control-center/**`
- `pipeline-diagram/board.html`
- `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/**`

Explicit non-goals:

- Researcher UI
- Test Author/tester launch
- PR creation, merge, deployment, PRD approval, production readiness, backtests, paper/live trading
- Public terminal exposure or remote multi-user access
- Replacing GitHub issue/Project source of truth
- Designing a new task router
- Raw Claude/Codex CLI launch or parallel coder/verifier workflow

## Dirty Tree Before Editing

- None (`git status --short --branch` clean before implementation)

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Dependency and contract gate: task context input contract + safe pi profile registry shape | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |
| 2 | Pre-start UI: Now-chip launcher modal consumes task context and shows pi model profile/effort controls | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |
| 3 | Launch profile resolution: resolve role + provider/profile + effort into wrapper launch plan without raw shell injection | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |
| 4 | Dual session launch: verifier-left/coder-right grouped terminal sessions with context parity | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` (manual verifier JSON pasted by human after coms formatting failure) |
| 5 | Lifecycle, status, failure cleanup, and reconnect safety | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` (report updated despite malformed coms reply) |
| 6 | Guardrails and validation | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |
| Final bug-check | after full implementation | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |
| Post-final live proxy base | `/term/` proxy deploy prep found absolute Vite asset paths | approved | `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/verifier-report.md` |

## Changed Files

- `term-control-center/shared/launcher.ts`: task context, pane config, role/provider/effort, and session-group status contract validators
- `term-control-center/server/launchProfiles.ts`: safe pi model profile registry shape and pane launch-plan resolver
- `term-control-center/server/launchPlan.ts`: resolves validated requests into wrapper command plans using `pi-agent.sh <role> --model <model> --thinking <effort>` and shared context prompt injection
- `term-control-center/tests/launcher.test.ts`: validation coverage for required context, safe values, and verifier-left/coder-right ordering
- `term-control-center/tests/launchProfiles.test.ts`: safe profile resolution coverage
- `term-control-center/tests/boardGuardrails.test.ts`: static guardrail coverage for board launcher UI/payload
- `pipeline-diagram/generate.py`: emits Project 2 worktree/branch/owner/status metadata into board chips for launch context
- `pipeline-diagram/board.html`: disables launch when required context is missing, updates modal to pi model profiles, posts canonical task context, and displays safe launch-plan summaries
- `term-control-center/server/index.ts`: adds token-protected launch profile and launch endpoints with route/lifecycle integration; supports configured public WebSocket origins for `/term/` proxy hosting
- `term-control-center/server/launchGroup.ts`: starts paired PTY sessions, writes shared task context prompts, tracks session groups, supports group summaries and group cleanup
- `term-control-center/src/App.tsx`: accepts launched session group URL payloads and attaches verifier/coder panes without relaunching
- `term-control-center/src/TerminalPane.tsx`: warns before terminating paired coder/verifier panes; resolves WebSocket URLs under the `/term/` proxy base path; uses the default xterm renderer instead of WebGL for remote browser compatibility
- `term-control-center/index.html`: uses relative `./term-config.js` so the app can run under `/term/`
- `term-control-center/vite.config.ts`: sets relative build base so compiled JS/CSS load under `/term/`
- `term-control-center/tests/termBasePath.test.ts`: covers `/term/` proxy asset and WebSocket URL behavior
- `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/coder-handoff.md`: durable handoff artifact
- `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/coms-reliability-note.md`: follow-up note for malformed verifier coms responses

## Validation

- `git status --short --branch`: pass before editing
- `coms_list(project="agentops-term")`: pass; live verifier found
- `coms_send` connectivity ping: pass after retry without schema (`ACK verifier agentops-term`)
- `npm --prefix term-control-center run typecheck`: pass
- `npm --prefix term-control-center run test`: pass (27 tests)
- Post-final proxy-base validation: `npm --prefix term-control-center run test`: pass (29 tests)
- Post-final WebSocket proxy-origin validation: `npm --prefix term-control-center run test`: pass (30 tests)
- Post-final terminal renderer validation: `npm --prefix term-control-center run test`: pass (31 tests)
- Post-final resize message validation: `npm --prefix term-control-center run test`: pass (32 tests)
- `python3 -m py_compile pipeline-diagram/generate.py`: pass
- `node --check /tmp/board-inline-check.js`: pass
- `wc -l term-control-center/server/index.ts term-control-center/server/launchGroup.ts term-control-center/src/App.tsx term-control-center/src/TerminalPane.tsx`: pass (all under 300)
- `npm --prefix term-control-center run build`: pass (Vite chunk-size warning only)
- Post-final proxy-base validation: `npm --prefix term-control-center run build`: pass (Vite chunk-size warning only); rebuilt `dist/index.html` now references `./assets/...`
- Post-final WebSocket proxy-origin validation: `npm --prefix term-control-center run build`: pass (Vite chunk-size warning only)
- Post-final terminal renderer validation: `npm --prefix term-control-center run build`: pass (Vite chunk-size warning only); new client bundle `assets/index-C6X2RTii.js`
- Post-final resize message validation: `npm --prefix term-control-center run build`: pass (Vite chunk-size warning only); new client bundle `assets/index-CgKSZUc6.js`
- Restarted live local term-control service with `TERM_CONTROL_ALLOWED_ORIGINS=https://ops.evono.me`; node PID `4090973`; direct WebSocket with `Origin: https://ops.evono.me` opens successfully.
- `npm --prefix term-control-center audit --audit-level=moderate`: pass
- `git diff --check`: pass

## Assumptions

- Section 21 supersedes earlier Claude/Codex profile wording: UI labels should map to safe pi model profiles, not direct CLIs.
- Project 3 status can remain `Todo` until an operator or separate process marks implementation in progress.
- The current implementation already contains a PRD #21 terminal substrate and a placeholder board modal/launch button.

## Known Gaps

- `dev-plans/agentops/coder-verifier-workflow/coms-transport.md` is not present in this repo; transport contract was read from the merged SoldierOne worktree path referenced by PRD #22.
- Coder/verifier coms verdict capture is unreliable in this run; durable note: `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/coms-reliability-note.md`.
- Live nginx config still needs the `/term/` proxy installed and reloaded with sudo; `/etc/nginx/sites-available/ops.evono.me` is readable and does not yet contain `location /term/`.
- Local term-control service is running at `127.0.0.1:3032` with node PID `4090973`; `/tmp/ops-term-control-center.pid` points at this node PID.

## Verifier Pairing

- Required: yes
- Reason: PRD #22 explicitly requires coder/verifier checkpoint review and final bug-check.
- Coder ready file: not used; coms_send review request will reference this handoff
- Verifier report: pending

## Coder Decision

`approved_post_final_proxy_base_fix_nginx_reload_needs_sudo`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1 | initial setup + checkpoint 1 | `term-control-center/shared/launcher.ts`, `term-control-center/server/launchProfiles.ts`, `term-control-center/tests/launcher.test.ts`, `term-control-center/tests/launchProfiles.test.ts`, handoff | typecheck pass; tests pass; verifier approved after JSON retry | `approved` |
| 2 | checkpoint 2 pre-start UI | `pipeline-diagram/generate.py`, `pipeline-diagram/board.html`, handoff | typecheck pass; tests pass; py_compile pass; verifier approved after manual recovery | `approved` |
| 3 | checkpoint 3 launch profile resolution | `term-control-center/server/index.ts`, `term-control-center/server/launchPlan.ts`, `term-control-center/tests/server.test.ts`, `pipeline-diagram/board.html`, handoff | typecheck pass; tests pass; py_compile pass; node --check pass; addressed CV22-CP3-001 and CV22-CP3-002; verifier approved revision 2 | `approved` |
| 4 | checkpoint 4 dual session launch | `term-control-center/server/index.ts`, `term-control-center/server/launchGroup.ts`, `term-control-center/server/launchPlan.ts`, `term-control-center/src/App.tsx`, `term-control-center/tests/server.test.ts`, `pipeline-diagram/board.html`, handoff | typecheck pass; tests pass; py_compile pass; node --check pass; addressed CV22-CP4-001 and CV22-CP4-002; human pasted verifier approval JSON after coms formatting failure | `approved` |
| 5 | checkpoint 5 lifecycle/status/reconnect | `term-control-center/server/index.ts`, `term-control-center/server/launchGroup.ts`, `term-control-center/tests/server.test.ts`, handoff | typecheck pass; tests pass; py_compile pass; node --check pass; wc pass | `revision_requested` |
| 6 | checkpoint 5 revision fixes | `pipeline-diagram/board.html`, `term-control-center/src/TerminalPane.tsx`, `dev-plans/agentops/coder-verifier-workflow/runs/prd-22-task-aware-launcher/coms-reliability-note.md`, handoff | typecheck pass; tests pass; py_compile pass; node --check pass; wc pass; addressed CV22-CP5-001 and CV22-CP5-002; report approved despite malformed coms reply | `approved` |
| 7 | checkpoint 6 guardrails and validation | `pipeline-diagram/board.html`, `term-control-center/tests/boardGuardrails.test.ts`, handoff | typecheck pass; tests pass; py_compile pass; node --check pass; wc pass; verifier approved | `approved` |
| 8 | final validation | all changed files | build pass; audit pass; diff check pass | `ready_for_final_bug_check` |
| 9 | final bug-check request | all changed files | final bug-check report updated; bug-check passed; open findings 0 | `approved` |
| 10 | post-final live `/term/` proxy asset-base fix | `term-control-center/vite.config.ts`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass; build pass; local service serves `./assets/...`; verifier approved bounded fix and bug-check passed | `approved` |
| 11 | post-final WebSocket proxy-origin fix | `term-control-center/server/index.ts`, `term-control-center/tests/server.test.ts`, handoff | tests pass; build pass; live service restarted with `TERM_CONTROL_ALLOWED_ORIGINS=https://ops.evono.me`; direct proxied-origin WS opens; verifier approved bounded fix and bug-check passed | `approved` |
| 12 | post-final black terminal renderer fix | `term-control-center/src/TerminalPane.tsx`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass; build pass; backend output buffer confirmed; client bundle no longer imports WebGL addon; verifier approved bounded fix and bug-check passed | `approved` |
| 13 | post-final invalid resize message fix | `term-control-center/src/TerminalPane.tsx`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass; build pass; client clamps terminal dimensions before INIT/RESIZE; live static checkout copied; verifier approved bounded fix and bug-check passed | `approved` |
| 14 | post-final malformed WebSocket frame tolerance + autoscroll | `term-control-center/server/index.ts`, `term-control-center/src/TerminalPane.tsx`, `term-control-center/tests/server.test.ts`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass (34); build pass; service restarted with PID `4168313`; new sessions required; verifier approved bounded fix and bug-check passed | `approved` |
| 15 | post-final viewport fit fix | `term-control-center/src/styles.css`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass (35); build pass; app shell uses full `100vw`/`100dvh`, body overflow hidden, no `1180px` width cap; live static checkout copied; verifier approved bounded fix and bug-check passed | `approved` |
| 16 | post-final viewport height containment fix | `term-control-center/src/App.tsx`, `term-control-center/src/styles.css`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass (35); build pass; Allotment wrapped in constrained `terminal-grid`; split view fills remaining height; xterm viewport scroll enabled; live static checkout copied; verifier approved bounded fix and bug-check passed | `approved` |
| 17 | post-final terminal content containment fix | `term-control-center/src/App.tsx`, `term-control-center/src/styles.css`, `term-control-center/tests/termBasePath.test.ts`, handoff | revision 1 requested CV22-PF17-001; revision 2 keeps Allotment pane inline heights intact, adds orientation classes, caps content without `height:100% !important` on `.split-view-view`; tests pass (35); build pass; live static checkout copied; verifier approved bounded fix and bug-check passed | `approved` |
| 18 | post-final embedded fullscreen terminal modal + autostart | `pipeline-diagram/board.html`, `term-control-center/server/launchGroup.ts`, `term-control-center/tests/boardGuardrails.test.ts`, `term-control-center/tests/server.test.ts`, handoff | tests pass (37); build pass; board embeds `/term/?group=...` in fullscreen modal iframe; launch group writes role-specific startup prompt; service restarted with PID `80628`; verifier approved bounded fix and bug-check passed | `approved` |
| 19 | post-final delayed enter autostart submit | `term-control-center/server/launchGroup.ts`, `term-control-center/tests/server.test.ts`, handoff | tests pass (37); build pass; autostart prompt is written then Enter is sent after 1500ms; service restarted with PID `93591` | `ready_for_review` |
| 20 | post-final direct Claude/Codex CLI launch | `term-control-center/server/launchPlan.ts`, `term-control-center/server/launchProfiles.ts`, `term-control-center/tests/server.test.ts`, handoff | tests pass (37); build pass; launch plans use `/home/hyperbots/.local/bin/claude` or `/home/hyperbots/.local/bin/codex` instead of pi/OpenRouter; service restarted with PID `128149` | `ready_for_review` |
| 21 | post-final mobile pane switcher | `term-control-center/src/App.tsx`, `term-control-center/src/styles.css`, `term-control-center/tests/termBasePath.test.ts`, handoff | tests pass (38); build pass; mobile media query enables focus mode and shows pane-switcher buttons so one pane fills the viewport at a time; live static checkout copied | `ready_for_review` |
| 22 | post-final mobile duplicate Basic Auth prompt fix | `pipeline-diagram/deploy/ops.evono.me.nginx`, `term-control-center/tests/nginxProxy.test.ts`, handoff | tests pass (39); git diff check pass; nginx `/term/ws` location disables Basic Auth and stays before `/term/`; live checkout deploy config copied; requires sudo nginx install/reload | `ready_for_review` |
