# Coder Handoff

## Task

- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/72`
- PRD: `hyperbotsx/agentops-harness#72`
- Branch: `prd/ai-co-worker-chat-surface-floating-launcher-72`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneD`

## Scope

Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/`
Verifier socket: `local coms pool`
Preview target: `pipeline-diagram/board.html`
Preview URL: `board service on :8801`
Preview deploy command: `not applicable`
Browser QA / DevTools required: `no`
Browser QA target URL/path: `not applicable`

Allowed paths:

- `pipeline-diagram/board.html`
- `pipeline-diagram/README.md`
- `pipeline-diagram/completion-center.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/agentops-nav.js`
- `pipeline-diagram/coworker-launcher.js`
- `src/agentops_harness/**`
- `term-control-center/server/**`
- `term-control-center/shared/**`
- `term-control-center/tests/**`
- `tests/unit/**`
- `term-control-center/README.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/**`

Explicit non-goals:

- No PR creation, merge, deploy, or approval behavior except deny guards/tests
- No new external provider or egress path
- No cross-origin browser chat transport redesign
- No second status store outside existing board / `/groups` surfaces
- No unrelated navigation or completion-center feature work beyond de-confliction hooks

## Dirty Tree Before Editing

- none

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Floating launcher/chat shell on board with desktop/mobile de-confliction vs `#completion-center-btn` | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 2 | Same-origin chat wiring over existing Python rails; no new egress | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 3 | Grounding injection: product PRD, advisory memory, portfolio/board state, `plan-order.json` | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 4 | Explicit-only planner/orchestrator actions and running-state reporting; model text cannot dispatch | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 5 | Code-enforced authority allowlist + denylist with 403 coverage across Python + TCC | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 6 | Privacy/redaction coverage | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| 7 | Docs + final validation | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |
| Final bug-check | `after full implementation` | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md` |

## Validation Plan

- Per checkpoint: targeted tests for touched Python/TS surfaces plus `git diff --check`
- Final:
  - `npm --prefix term-control-center run typecheck`
  - `npm --prefix term-control-center run test`
  - `npm --prefix term-control-center run build`
  - `PYTHONPATH=src python3 -m pytest tests/unit -q`
  - `git diff --check`

## Stop Condition

- Stop after final verifier bug-check approval, updated handoff, and passing validation.
- Pause for human review before any PR creation/merge/deploy/approval action.

## Validation

- `npm --prefix term-control-center run typecheck`: `pass`
- `npm --prefix term-control-center run test`: `pass`
- `npm --prefix term-control-center run build`: `pass`
- `PYTHONPATH=src python3 -m pytest tests/unit -q`: `pass` (`761 passed, 42 subtests passed`)
- `git diff --check`: `pass`

## Research Summary

Mandatory research-first consult completed before implementation (`researcher`, 2026-06-21).

- Keep transcripts server-side; persist only an opaque conversation id client-side, and prefer `sessionStorage` unless cross-restart reopen is required.
- Same-origin POST actions still need CSRF-style defenses when browser cookies authenticate requests; CORS alone is insufficient.
- Treat model output as advisory text only; explicit UI actions must map to fixed server-owned action ids with allowlisted params and confirmation.
- Do not let Python forward arbitrary model-generated method/URL/body to Node; map fixed action ids to fixed server-side calls and re-authorize in Node.
- Keep backend tokens server-side when bridging services; if a bearer token is used, scope/rotate it and add replay-resistant request handling.

Sources cited by researcher:

- OWASP Session Management Cheat Sheet
- MDN Secure cookie configuration (2026-02-11)
- MDN Web Storage API (2025-02-22)
- OWASP CSRF Prevention Cheat Sheet
- MDN CSRF (2026-06-08)
- MDN CORS (2025-11-30)
- OWASP AI Agent Security Cheat Sheet
- OWASP MCP Security Cheat Sheet
- RFC 9700 (2025-01)
- OWASP API5:2023 Broken Function Level Authorization
- OWASP LLM Prompt Injection Prevention Cheat Sheet

## Known Gaps

- Skill-referenced template `dev-plans/agentops/coder-verifier-workflow/templates/coder-handoff-template.md` is absent in this worktree; this handoff follows the established run-folder format used by issues #70 and #71.

## Steward Review

- Decision: `cleanup_recommended`
- Outcome: implementation/tests/docs placement is clean; no misplaced outputs or transcript artifacts were found.
- Cleanup applied: `git add -N dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher` so the durable run-folder audit trail is intentionally visible in the tracked diff surface before final bug-check.
- Optional note from steward left unchanged: `coworker-launcher.js?v=issue-72-cp1` cache-bust token could be normalized later, but no cleanup recheck was required because no board/test content changed after the steward consult.

## Isolation Preflight

- Sender identity: `coder@agentops-laneD` (coder pane in the `agentops-laneD` coms pool)
- `coms_list` before outbound requests: `researcher`, `steward`, and `verifier` live in the local pool
- Sender cwd for peer requests: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneD`

## Checkpoint Progress

### Checkpoint 1 — Floating launcher shell

- Added a dedicated floating `AI Co-Worker` launcher in the board surface via a new module.
- Positioned the launcher bottom-right on desktop and stacked it above the mobile full-width completion-center control.
- Isolated the launcher coverage in a dedicated focused test file.
- Addressed verifier feedback by moving coworker assertions into a standalone test file and marking new files intent-to-add so they appear in tracked diff output.
- Verifier status: `approved` at revision 3.

### Checkpoint 2 — Same-origin chat wiring

- Replaced the placeholder panel body with a working server-held chat transcript UI.
- Wired the board launcher to same-origin Python endpoints for chat send, restore, and clear.
- Persisted only the opaque session id in `sessionStorage`; transcript content stays server-side.
- Reused the existing Python `call_cli` rail for replies with provider selection limited to Claude or Codex.
- Kept planner/running/execute action buttons disabled for later checkpoints so model text still cannot dispatch actions in this slice.
- Addressed verifier feedback by isolating coworker session ids from PRD/discuss sessions and adding foreign-session regression coverage.
- Verifier status: `approved` at revision 5.

### Checkpoint 3 — Grounding injection

- Added prompt assembly for product PRD reference (#69), advisory memory reference (#48), current board portfolio state, and `plan-order.json` summary.
- Frontend now sends the current `window.PIPELINE_BOARD` snapshot with each chat turn so the Python chat prompt can stay grounded in the visible board state.
- Added focused unit coverage that inspects the assembled coworker system prompt for all required grounding sources.
- Addressed verifier feedback by reading the real dict-shaped `plan-order.json` format emitted by `write_plan_order(...)` and updating the unit test to exercise that authoritative shape.
- Verifier status: `approved` at revision 7.

### Checkpoint 4 — Explicit-only planner / running-state / execute actions

- Enabled fixed action buttons in the coworker surface for `Plan portfolio`, `What is running?`, and `Execute plan`.
- Planner action now uses the existing sequencing planner rail, applies the returned plan outputs, and triggers board refresh through the existing Python service.
- Running-state action summarizes live term `/groups` state plus board `now/next` items through fixed same-origin routes.
- Execute action requires the exact phrase `execute this plan` in the UI and again server-side before the Python service proxies the fixed `/launch` request to Term Control.
- All action buttons call fixed coworker endpoints; model chat text still remains advisory and is never parsed into executable actions.
- Verifier status: `approved` at revision 8.

### Checkpoint 5 — Authority allowlist + denylist

- Added a coworker-surface allowlist in the Python board service so only `/coworker/*` routes are reachable when the request identifies itself as the coworker surface.
- Added a Term Control allowlist middleware so `x-agentops-surface: coworker` requests may only reach `GET /groups` and lane-execution `POST /launch`; completion actions now fail closed with `403`.
- Launcher requests now label themselves with `x-agentops-surface: coworker`, so the server-side deny guards can distinguish coworker traffic from the rest of the board.
- Added focused Python and TCC tests covering `403` denial for approve / prepare PR / merge-main paths while preserving allowed coworker execution surfaces.
- Verifier status: `approved` at revision 9.

### Checkpoint 6 — Privacy / redaction

- Reused `validation_ledger.redact_evidence` and wrapped it with coworker-specific terminal-block stripping before any coworker transcript text is stored.
- Coworker chat now redacts fake secret-like values and replaces fenced raw terminal blocks with `[redacted terminal block]` before both prompt assembly and session storage.
- Added focused unit coverage proving a fake secret plus raw terminal block never survives into stored coworker messages.
- Verifier status: `approved` at revision 10.

### Checkpoint 7 — Docs + final validation

- Documented the board-mounted AI Co-Worker surface, same-origin rails, explicit action boundaries, deny guards, and redaction behavior in `pipeline-diagram/README.md`.
- Documented the Term Control coworker allowlist contract for `x-agentops-surface: coworker` traffic in `term-control-center/README.md`.
- Ran the full required validation suite for the issue: typecheck, test, build, full Python unit tests, and `git diff --check`.

### Final bug-check follow-up

- Fixed a privacy bypass where board-derived coworker grounding could store or forward raw secret-like values / terminal blocks.
- Fixed the launcher clear flow so failed server clears preserve the current session and show an error instead of falsely claiming success.
- Re-ran the full required validation suite after the bug-check fixes.

## Changed Files

- `pipeline-diagram/board.html`: loads the coworker launcher on the board surface
- `pipeline-diagram/coworker-launcher.js`: floating launcher, same-origin chat UI, explicit fixed actions, surface marker, and clear-flow bug fix
- `pipeline-diagram/README.md`: coworker surface documentation
- `src/agentops_harness/review_server.py`: coworker chat/actions, grounding, allowlist/denylist, and redaction fixes
- `term-control-center/server/index.ts`: coworker allowlist middleware for Term Control routes
- `term-control-center/tests/coworkerGuard.test.ts`: TCC allowlist/403 regression coverage
- `term-control-center/tests/coworkerLauncher.test.ts`: launcher endpoint/header/clear-flow regression coverage
- `term-control-center/README.md`: Term Control coworker contract documentation
- `tests/unit/test_review_server_coworker.py`: coworker route, grounding, action, allowlist, and redaction regression coverage
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/**`: durable handoff, review requests, and verifier report for the checkpoint/bog-check audit trail

## Verifier Pairing

- Required: `yes`
- Reason: `PRD mandates verifier checkpoints and final bug-check`
- Coder ready file: `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md`
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/verifier-report.md`

## Coder Decision

`ready_for_human`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1 | `initial setup` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `not run` | `in_progress` |
| 2 | `checkpoint 1 floating launcher shell` | `pipeline-diagram/coworker-launcher.js`, `pipeline-diagram/board.html`, `term-control-center/tests/boardGuardrails.test.ts`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `cd term-control-center && node --import tsx --test tests/boardGuardrails.test.ts`; `git diff --check -- pipeline-diagram/board.html pipeline-diagram/coworker-launcher.js term-control-center/tests/boardGuardrails.test.ts` | `revision_requested` |
| 3 | `CP1-TRACK-001,CP1-KISS-001` | `pipeline-diagram/coworker-launcher.js`, `pipeline-diagram/board.html`, `term-control-center/tests/coworkerLauncher.test.ts`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `git add -N pipeline-diagram/coworker-launcher.js term-control-center/tests/coworkerLauncher.test.ts`; `node --check pipeline-diagram/coworker-launcher.js`; `cd term-control-center && node --import tsx --test tests/boardGuardrails.test.ts tests/coworkerLauncher.test.ts`; `git diff --check -- pipeline-diagram/board.html pipeline-diagram/coworker-launcher.js term-control-center/tests/boardGuardrails.test.ts term-control-center/tests/coworkerLauncher.test.ts` | `approved` |
| 4 | `checkpoint 2 same-origin chat wiring` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/tests/coworkerLauncher.test.ts`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `git add -N tests/unit/test_review_server_coworker.py`; `node --check pipeline-diagram/coworker-launcher.js`; `cd term-control-center && node --import tsx --test tests/coworkerLauncher.test.ts`; `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- pipeline-diagram/coworker-launcher.js src/agentops_harness/review_server.py term-control-center/tests/coworkerLauncher.test.ts tests/unit/test_review_server_coworker.py` | `revision_requested` |
| 5 | `CP2-SESSION-001` | `src/agentops_harness/review_server.py`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- src/agentops_harness/review_server.py tests/unit/test_review_server_coworker.py` | `approved` |
| 6 | `checkpoint 3 grounding injection` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/tests/coworkerLauncher.test.ts`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `node --check pipeline-diagram/coworker-launcher.js`; `cd term-control-center && node --import tsx --test tests/coworkerLauncher.test.ts`; `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- pipeline-diagram/coworker-launcher.js src/agentops_harness/review_server.py term-control-center/tests/coworkerLauncher.test.ts tests/unit/test_review_server_coworker.py` | `revision_requested` |
| 7 | `CP3-PLAN-001` | `src/agentops_harness/review_server.py`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- src/agentops_harness/review_server.py tests/unit/test_review_server_coworker.py` | `approved` |
| 8 | `checkpoint 4 explicit fixed actions` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/tests/coworkerLauncher.test.ts`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `node --check pipeline-diagram/coworker-launcher.js`; `cd term-control-center && node --import tsx --test tests/coworkerLauncher.test.ts`; `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- pipeline-diagram/coworker-launcher.js src/agentops_harness/review_server.py term-control-center/tests/coworkerLauncher.test.ts tests/unit/test_review_server_coworker.py` | `approved` |
| 9 | `checkpoint 5 authority allowlist + denylist` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/server/index.ts`, `term-control-center/tests/coworkerLauncher.test.ts`, `term-control-center/tests/coworkerGuard.test.ts`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `node --check pipeline-diagram/coworker-launcher.js`; `cd term-control-center && node --import tsx --test tests/coworkerLauncher.test.ts tests/coworkerGuard.test.ts`; `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- pipeline-diagram/coworker-launcher.js src/agentops_harness/review_server.py term-control-center/server/index.ts term-control-center/tests/coworkerLauncher.test.ts term-control-center/tests/coworkerGuard.test.ts tests/unit/test_review_server_coworker.py` | `approved` |
| 10 | `checkpoint 6 privacy redaction` | `src/agentops_harness/review_server.py`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`; `git diff --check -- src/agentops_harness/review_server.py tests/unit/test_review_server_coworker.py` | `approved` |
| 11 | `checkpoint 7 docs and final validation` | `pipeline-diagram/README.md`, `term-control-center/README.md`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run test`; `npm --prefix term-control-center run build`; `PYTHONPATH=src python3 -m pytest tests/unit -q`; `git diff --check` | `approved` |
| 12 | `final bug-check` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/tests/coworkerLauncher.test.ts`, `tests/unit/test_review_server_coworker.py`, run-folder audit artifacts | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run test`; `npm --prefix term-control-center run build`; `PYTHONPATH=src python3 -m pytest tests/unit -q`; `git diff --check` | `revision_requested` |
| 13 | `BUG72-PRIV-001,BUG72-CLEAR-002` | `pipeline-diagram/coworker-launcher.js`, `src/agentops_harness/review_server.py`, `term-control-center/tests/coworkerLauncher.test.ts`, `tests/unit/test_review_server_coworker.py`, `dev-plans/agentops/coder-verifier-workflow/runs/issue-72-ai-coworker-chat-surface-floating-launcher/coder-handoff.md` | `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run test`; `npm --prefix term-control-center run build`; `PYTHONPATH=src python3 -m pytest tests/unit -q`; `git diff --check` | `approved` |
