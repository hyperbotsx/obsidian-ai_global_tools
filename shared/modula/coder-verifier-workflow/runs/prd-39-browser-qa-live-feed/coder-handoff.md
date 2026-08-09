# Coder Handoff — PRD #39 Agent Launch Model Configuration + Browser QA Live Feed

## Source of truth
- PRD issue: https://github.com/hyperbotsx/agentops-harness/issues/39
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Branch: `prd/agent-launch-browser-qa-live-feed-39`

## Pre-edit status
- `git status --short --branch` before editing: clean (`## prd/agent-launch-browser-qa-live-feed-39...origin/main`).
- Pre-existing dirty files: none.

## Scope controls from PRD
- Allowed paths/actions: Term Control Center launch types/schema/profile resolution/UI, Browser QA role launch workflow, Browser QA artifacts/report parsing, local-only live-feed prototype behind feature flag, tests, docs/runbooks.
- Forbidden: public VNC/CDP/browser/terminal exposure; non-localhost browser control ports; default/personal Chrome profile; Browser QA code edits by default; arbitrary browser-provided command execution; secrets/cookies/credentials/private recordings/raw transcripts in committed artifacts; PR creation, merge, deploy, approval, trading/backtesting.
- Required validation: `npm --prefix term-control-center run build`, `npm --prefix term-control-center run test`, Python unit tests for Browser QA planning/report parsing, schema/default tests, Browser QA policy tests, unsafe CDP/VNC rejection tests, four-agent compatibility tests.
- Stop condition: all PRD checkpoints implemented, required validation passes, final verifier bug-check approved; or human escalation.

## Research freshness consult
Mandatory researcher consult completed 2026-06-19. Key guidance recorded:
- Claude Code Chrome is beta; use `claude --chrome` or `/chrome`; requires current Claude Code and Claude in Chrome extension; fail closed if unavailable.
- Claude Code supports explicit `--model` and `--effort`; use explicit launch values and normalize extra-high to `xhigh`.
- CDP screencast remains experimental; use `Page.startScreencast`, `Page.screencastFrame`, and `Page.screencastFrameAck`; fail closed if unsupported.
- noVNC should use WebSocket embedding with local auth/token patterns; prefer path URL over deprecated host/port/encrypt options.
- Chrome 136+ requires a non-default `--user-data-dir` for remote debugging; bind CDP/VNC/WebSocket to `127.0.0.1` only.
- Playwright traces can contain sensitive screenshots/DOM/network data; keep local and bounded.

## Verifier checkpoints
1. Launch config checkpoint — schema, UI defaults, model profiles, thinking/effort normalization.
2. Browser QA workflow checkpoint — handoff prompt, report format, coder fix handoff, verifier evidence path.
3. Claude Code Chrome checkpoint — Browser QA launches through Claude Code/Chrome safely and handles unavailable states.
4. Live feed checkpoint — noVNC/CDP/fallback decision, locality/auth/privacy/feature flags.
5. Responsive workspace checkpoint — five roles usable without forced five-terminal grid.
6. Final regression checkpoint — PRD #24 compatibility, non-frontend skip, command-launch security.

## Checkpoint 1 changes
- Added `browser-qa` as a launchable role in shared launch/protocol/App terminal types and `scripts/agentops/pi-agent.sh`.
- Added `BrowserQaLaunchPolicy` (`auto`, `force_on`, `off`) and optional task fields (`body`, `labels`, `previewUrl`, `browserQaPolicy`) for browser-visible detection.
- Added PRD defaults:
  - Coder: Codex `codex-default`, `high`.
  - Verifier: Codex `codex-default`, `xhigh`.
  - Researcher: Codex `codex-default`, `xhigh`.
  - Steward: Codex `codex-default`, `high`.
  - Browser QA: Claude `pi-claude-opus`, `high`, enabled when selected.
- Normalized `extra high`/`extra-high`/`extra_high` to `xhigh`; `max` is accepted by schema and profiles can allow/reject it safely.
- Browser QA auto policy selects frontend/browser-visible work using title/body/labels/preview/local URL hints, skips explicit non-UI/backend/docs/test/profile-config work, and honors force/off overrides.
- Existing two-role implementation launches still fill researcher/steward and only add Browser QA when policy/hints select it.
- Browser QA provider is fail-closed to Claude only.
- Disabled Browser QA panes (`enabled: false`) are filtered out before launch planning.
- Browser QA launch prompts require Claude Code Chrome integration (`claude --chrome` or `/chrome`) and fail closed when unavailable.
- `scripts/agentops/pi-agent.sh` allowlists `browser-qa`; if no approved global Browser QA skill exists yet, it generates a minimal temp-only Browser QA skill prompt under `/tmp/agentops/pi-generated-skills` rather than creating a project-local skill.
- App workspace pair switcher recognizes Browser QA as a separate role tab/pair without forcing a five-terminal grid.

## Changed files for checkpoint 1
- `scripts/agentops/pi-agent.sh`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/protocol.ts`
- `term-control-center/server/launchProfiles.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/src/TerminalPane.tsx`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/server.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/prd-39-browser-qa-live-feed/coder-handoff.md`

## Validation run for checkpoint 1
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launcher.test.ts tests/launchProfiles.test.ts tests/launchPlan.test.ts tests/server.test.ts` — passed (46 tests).
- `timeout 5s scripts/agentops/pi-agent.sh browser-qa --version` — passed (`0.79.3`).

## Revision 2 fixes for verifier findings
- `PRD39-C1-001`: added Browser QA to the safe wrapper allowlist, generated a temp-only Browser QA skill fallback, and added regression coverage that Browser QA launch plans use the wrapper role and Chrome requirement.
- `PRD39-C1-002`: filtered `enabled: false` panes before launch planning and added regression coverage proving disabled Browser QA does not launch.
- `PRD39-C1-003`: restored unrelated concurrent files/untracked symlink and updated the handoff file list/status to match the current worktree. Later steward cleanup removed temporary unrelated-state evidence files from the run folder.

## Checkpoint 2 changes
- Browser QA prompt now includes an explicit stop condition, `browser-qa-report.md` artifact expectation, fail-closed conditions, and bounded coder-fix detail requirements for blocking/major findings.
- Browser QA report artifact writing now also creates `browser-qa-verifier-evidence.md` so verifier has a durable evidence path before frontend-visible approval.
- Browser QA status JSON now exposes `browser_qa_verifier_evidence_path`.
- Added verifier evidence rendering that states Browser QA is non-authoritative and that verifier approval remains required.
- Existing fix handoff behavior remains scoped to blocking/major findings only.

## Additional changed files for checkpoint 2
- `src/agentops_harness/browser_qa.py`
- `src/agentops_harness/browser_qa_report.py`
- `tests/unit/test_browser_qa.py`
- `tests/unit/test_browser_qa_report.py`

## Validation run for checkpoint 2
- `PYTHONPATH=src python3 -m pytest tests/unit/test_browser_qa.py tests/unit/test_browser_qa_report.py` — passed (30 tests).

## Revision 2 fixes for checkpoint 2 verifier findings
- `PRD39-C2-001`: Browser QA prompt extraction now includes exact checks from acceptance criteria section numbered lists, checklist bullets, and regular bullets; added regression coverage for numbered/checklist criteria.

## Checkpoint 3 changes
- Browser QA runtime launch config now carries/validates effort (`high` default, `extra_high` normalized to `xhigh`, unknown values rejected).
- Browser QA launch config now requires Chrome integration evidence: `--chrome` in command/args or an explicit safe Chrome path override.
- Browser QA launch config now fails closed for declared unavailable states: `claude_code_available: false`, `chrome_available: false`, or `chrome_extension_ready: false`.
- Browser QA launch config rejects unsafe Claude command strings that are not a direct `claude` path.
- Tests cover missing Chrome integration, unavailable extension state, unsafe command/invalid effort, and existing dangerous-flag/code-edit safeguards.

## Additional changed files for checkpoint 3
- `src/agentops_harness/browser_qa_runtime.py`
- `tests/unit/test_browser_qa.py`

## Validation run for checkpoint 3
- `PYTHONPATH=src python3 -m pytest tests/unit/test_browser_qa.py tests/unit/test_browser_qa_runtime.py tests/unit/test_browser_qa_report.py` — passed (36 tests).

## Revision 2 fixes for checkpoint 3 verifier findings
- `PRD39-C3-001`: Browser QA runtime now rejects non-`claude_code` runtimes; added regression coverage for `runtime: codex`.
- `PRD39-C3-002`: removed broad alternate-path bypasses by requiring command `claude`, rejecting arbitrary `/tmp/.../claude`, and validating `safe_chrome_path` against a constrained absolute Chrome-binary shape; added malformed path/missing `--chrome` coverage.
- `PRD39-C3-003`: split Browser QA runtime tests into `tests/unit/test_browser_qa_runtime.py`; touched test files are now below 300 lines.

## Human continuation approval after checkpoint 3 escalation
- Human approved continuing after verifier `needs_human` escalation.

## Revision 3 fixes for checkpoint 3 verifier finding
- `PRD39-C3-002`: replaced regex-based Chrome path acceptance with an explicit trusted Chrome binary allowlist; `/tmp/Google Chrome` now fails closed. Added regression coverage for `/tmp/Google Chrome` rejection and `/usr/bin/google-chrome` acceptance.
- Validation: `PYTHONPATH=src python3 -m pytest tests/unit/test_browser_qa.py tests/unit/test_browser_qa_runtime.py tests/unit/test_browser_qa_report.py` — passed (38 tests).

## Checkpoint 4 changes
- Added Browser QA feed decision/config module with default fallback-only disabled mode.
- Added authenticated `/browser-feed` Term Control endpoint protected by the existing local term token guard.
- Added feature flag controls: `TERM_CONTROL_BROWSER_FEED_ENABLED=1`, `TERM_CONTROL_BROWSER_FEED_MODE=cdp|novnc|fallback`.
- CDP mode fails closed unless Term Control host and CDP host are localhost and a non-default dedicated Chrome user-data-dir is configured; CDP mode marks frame ack handling required.
- noVNC mode fails closed unless VNC host is localhost and view-only mode is preserved.
- Fallback evidence links are exposed only as sanitized links and secret-looking paths are omitted.
- Live feed config never enables raw recording and reports authenticated/view-only/dedicated-profile boundaries.

## Additional changed files for checkpoint 4
- `term-control-center/server/browserFeed.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/browserFeed.test.ts`

## Validation run for checkpoint 4
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/browserFeed.test.ts tests/server.test.ts` — passed (33 tests).

## Revision 2 fixes for checkpoint 4 verifier finding
- `PRD39-C4-001`: live feed summary no longer reports CDP/noVNC as ready while endpoints are unimplemented; live modes fall back with `live_feed_endpoint_unimplemented`.
- Added guarded fail-closed `/browser-feed/cdp-screencast` and `/browser-feed/novnc` routes that require the term token and return 501 until real feed transport exists.
- Added regression coverage proving unauthenticated live feed path access is rejected and enabled-but-unimplemented live modes do not report ready.

## Checkpoint 5 changes
- Browser QA remains a separate workspace focus pair/tab (`Browser QA`) instead of adding a forced five-terminal grid.
- Hidden sessions remain mounted and live through the existing focused pane stack (`hidden={!visible.has(...)}`) rather than being killed.
- Phone/focus mode keeps one visible pane at a time via existing role switcher and full-screen pane switching.
- Added regression coverage that Browser QA is exposed as a separate focus pair and no five-grid layout is introduced.

## Additional changed files for checkpoint 5
- `term-control-center/tests/termBasePath.test.ts`

## Validation run for checkpoint 5
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/termBasePath.test.ts` — passed (16 tests).

## Checkpoint 6 changes
- Board launch UI now exposes Browser QA model/effort controls and launch policy (`auto`, `force_on`, `off`) alongside coder/verifier/researcher/steward.
- Board defaults now align with PRD #39: researcher `xhigh`, steward `high`, Browser QA Claude profile `pi-claude-opus` with `high` effort.
- Implementation launch payload now includes Browser QA only when policy/auto detection selects it; backend/docs/test/profile-config-only hints skip Browser QA unless forced.
- Board guardrail text updated to reflect implementation roles plus evidence-only Browser QA.
- Term Control README documents per-role defaults, Browser QA policy, and fallback-only live feed behavior.
- Regression validation confirms existing four-agent compatibility, non-frontend skip behavior, launch security, and responsive Browser QA role visibility.

## Additional changed files for checkpoint 6
- `pipeline-diagram/board.html`
- `term-control-center/README.md`
- `term-control-center/tests/boardGuardrails.test.ts`

## Validation run for checkpoint 6
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launcher.test.ts tests/launchPlan.test.ts tests/browserFeed.test.ts tests/boardGuardrails.test.ts tests/termBasePath.test.ts tests/server.test.ts` — passed (84 tests).
- `PYTHONPATH=src python3 -m pytest tests/unit/test_browser_qa.py tests/unit/test_browser_qa_runtime.py tests/unit/test_browser_qa_report.py` — passed (38 tests).

## Steward hygiene review
- Steward verdict: `cleanup_recommended` for two temporary unrelated-state files in the run folder; implementation file placement was clean.
- Cleanup completed: removed `unrelated-concurrent-diff.patch` and `unrelated-concurrent-untracked.txt` from the run folder.

## Final validation
- `npm --prefix term-control-center run build` — passed (existing Vite warnings about non-module `term-config.js` and chunk size only).
- `npm --prefix term-control-center run test` — passed (168 tests).
- `PYTHONPATH=src python3 -m pytest tests/unit/test_browser_qa.py tests/unit/test_browser_qa_runtime.py tests/unit/test_browser_qa_report.py` — passed (38 tests).
- `git diff --check` — passed.

## Final bug-check revision 2 fix
- `BUGCHECK-39-001`: Board Browser QA auto-selection now treats any non-empty preview/local URL as Browser QA-worthy unless explicit skip hints or policy `off` apply; `force_on` still includes Browser QA. Added board regression coverage for `Boolean(task.previewUrl)` selection.
- Validation: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts` — passed (21 tests).
- Validation: `git diff --check` — passed.

## Open items before final bug-check
- Request verifier final bug-check recheck.
