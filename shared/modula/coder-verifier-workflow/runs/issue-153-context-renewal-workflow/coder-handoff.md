# Coder Handoff — Issue #153 AgentOps Context Renewal Workflow

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/153
- Branch: `prd/d5-prd-agentops-context-renewal-workflow-153`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-153`
- Project routing: Project 3 (`agentops-dev`); no Project 2 tracker mutation authorized.

## Pre-edit state
- `git status --short --branch`: `## prd/d5-prd-agentops-context-renewal-workflow-153...origin/main`
- Pre-existing dirty files: none.

## Allowed paths / scope
- AgentOps harness scripts, term-control-center orchestration code, tests, docs, workflow artifacts, and future first-party Pi extension/package files required for context renewal.
- Run artifacts under this folder.
- Current checkpoint scope: documentation/design only for policy, status model, feature flags, artifact paths, safe-boundary rules, and activation plan.

## Forbidden scope
- No product application code, deployment mutation, secrets, raw transcripts, PR creation, merge, deploy, approval, trading, backtesting, or GitHub Project mutation.
- No fully automatic pane reset.
- No verifier/researcher/steward reset/resume automation.
- No external context/offload package adoption in MVP.
- No deletion or overwrite of handoffs, verifier reports, or review evidence.

## Researcher consult summary
Mandatory freshness consult completed before implementation edits on 2026-06-29.

- Implement on Pi extension plus AgentOps harness/tmux primitives; do not adopt external offload packages.
- Pi 0.80.2 supports packages/extensions through settings and `-e/--extension`; normal terminal Pi and hyper-pi have separate config roots.
- `scripts/agentops/pi-agent.sh` runs `pi --no-extensions` and explicitly adds `pi-coms-local` and `pi-claude-agent`, so AgentOps panes need explicit renewal extension wiring under the feature flag.
- Pi `ctx.getContextUsage()` returns `{ tokens, contextWindow, percent }` with nullable values after compaction or if unknown.
- Relevant Pi hooks/primitives: `ctx.ui.setStatus/setWidget`, `tool_*`, `agent_end`, `input`, `session_before_compact`, command-context `ctx.waitForIdle()`, `ctx.newSession({ setup, withSession })`, and replacement-session `sendUserMessage()`.
- `pi-coms-local@0.1.1` `coms_list` reports advisory peer fields including `context_used_pct`; queue depth exists in registry but is not exposed by `coms_list`, so do not use it alone for safe-boundary decisions.
- AgentOps tmux primitives include `startLaunchGroup`, exact `killTmuxSession`, and `tmux set-buffer`/`paste-buffer`/`send-keys Enter` injection patterns.
- External `context-mode` and MCP offload packages exist, but PRD scope only allows mentioning them; do not adopt without separate approval.

## Checkpoint plan
1. Policy and global activation design — current checkpoint.
2. Global extension/package foundation.
3. Continuation-pack generator.
4. Safe-boundary and status integration.
5. Coder reset/resume MVP.
6. Documentation and final hardening.

## Implementation summary — checkpoint 1
- Added `docs/agentops-context-renewal.md` documenting:
  - feature flag shape;
  - 70/75/80 threshold defaults;
  - renewal statuses;
  - safe-boundary rules;
  - continuation-pack folder and required file contents;
  - normal terminal Pi, hyper-pi, and AgentOps-launched activation design;
  - usage source precedence and `coms_list` advisory limits;
  - coder-only reset/resume MVP design;
  - unsupported fallback states;
  - smoke-test plan;
  - Project 3 routing and authority boundaries.
- No reset automation or executable behavior was added in checkpoint 1.
- Verifier approved checkpoint 1 revision 1 with no findings.

## Implementation summary — checkpoint 2
- Added first-party Pi package foundation under `pi-packages/agentops-context-renewal/`:
  - `package.json` with Pi package manifest;
  - `lib/policy.ts` for threshold parsing, default states, feature flag checks, and status text;
  - `extensions/context-renewal.ts` to update Pi footer/status on session, turn, agent, input, and compaction events and expose `/context-renewal-status`.
- Wired `scripts/agentops/pi-agent.sh` to append the renewal package when `AGENTOPS_CONTEXT_RENEWAL` is truthy, while preserving existing `pi --no-extensions`, role identity, project name, `PI_COMS_DIR`, pi-coms-local, and pi-claude-agent behavior.
- Added safe fallback behavior: if the feature flag is enabled but the package path is missing, `pi-agent.sh` exits before launching the pane.
- Added `scripts/agentops/context-renewal-preflight.py` plus `src/agentops_harness/context_renewal_preflight.py` to report terminal Pi, hyper-pi, and AgentOps wrapper entry-point status without mutating settings or resetting panes.
- Added targeted tests for threshold transitions, env threshold normalization, wrapper feature-flag loading/fail-closed behavior, and preflight active/unsupported/blocked states.
- Updated `docs/agentops-context-renewal.md` with implemented flags, package path, wrapper fail-closed behavior, and preflight command.
- Revision 3 fixes:
  - `F153-R2-001`: preflight now derives the effective package path from `PI_AGENT_CONTEXT_RENEWAL_EXTENSION`, matching `pi-agent.sh`, and reports `blocked` when that override is missing.
  - `F153-R2-002`: wrapper tests now use shared setup helpers so checkpoint test callbacks stay within KISS function-size boundaries.
- No continuation-pack generator, safe-boundary reset, or pane reset automation was added in checkpoint 2.
- Verifier approved checkpoint 2 revision 3 with no open findings.

## Implementation summary — checkpoint 3
- Added dry-run continuation-pack generator:
  - `src/agentops_harness/context_renewal_pack.py` renders `STATE.md` and `CONTINUATION_PROMPT.md` from current repo/run state and explicit checkpoint inputs.
  - `scripts/agentops/context-renewal-pack.py` exposes the generator as a dry-run CLI with required PRD, artifact folder, checkpoint, revision, and next-action inputs.
- Generated continuation-pack evidence at `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T145002Z/`.
- Revision 5 fixes:
  - `F153-R4-001`: regenerated pack at `continuation/20260629T145747Z/` with addressed verifier findings, full validation history, run-artifact allowed path, pending re-review state, and PRD safety boundaries.
  - `F153-R4-002`: generator now runs `git status --short --branch --untracked-files=all` so changed files are captured at file granularity.
- Added tests for required continuation sections, changed-file capture, prompt Project 3 routing, and redaction of token/password-style sensitive values.
- Updated `docs/agentops-context-renewal.md` with the dry-run pack command.
- No safe-boundary reset, pane kill, prompt injection, or automatic reset behavior was added in checkpoint 3.
- Verifier approved checkpoint 3 revision 5 with no open findings.

## Implementation summary — checkpoint 4
- Added safe-boundary checker:
  - `src/agentops_harness/context_renewal_boundary.py` evaluates coms/tool/edit/git/artifact state and fails closed when any state is unknown or unsafe.
  - `scripts/agentops/context-renewal-boundary.py` exposes read-only JSON/markdown status for operator-visible boundary checks.
- Boundary checker reports `blocked` for unknown default state, `safe-boundary` only when all required no-in-flight/no-active/no-partial-edit/captured-state/continuation-pack-completed inputs are provided, and `reset_allowed` only when safe plus operator confirmation is present.
- Revision 7 fix: `F153-R6-001` added explicit continuation-pack-completed state to boundary module, CLI, docs, and tests so reset cannot be allowed without pack completion evidence.
- Added tests for unknown-state blocking, safe boundary without reset permission, and operator-confirmed reset allowance.
- Updated docs with boundary command and explicit operator-confirmation requirement.
- No pane reset, kill, tmux injection, `ctx.newSession`, or reset/resume automation was added in checkpoint 4.
- Verifier approved checkpoint 4 revision 7 with no open findings.

## Implementation summary — checkpoint 5
- Added coder-only manual resume MVP:
  - `src/agentops_harness/context_renewal_resume.py` builds a manual coder resume plan only when `STATE.md`, `CONTINUATION_PROMPT.md`, and a safe boundary report with `reset_allowed: true` exist.
  - `scripts/agentops/context-renewal-resume.py` prints the continuation prompt for manual paste; it does not kill panes, inject text, call tmux, or reset sessions.
- Added tests proving resume is blocked without safe boundary, blocked when prompt is missing, and manual prompt is printed only when boundary allows.
- Wrote safe-boundary evidence and a manual resume plan under this run folder, with latest prompt-printing evidence in `manual-resume-plan-r8-latest.md` using continuation pack `20260629T150817Z`.
- Updated docs with the manual resume command and explicit no-injection/no-reset MVP behavior.
- Verifier approved checkpoint 5 revision 8 with no open findings.

## Implementation summary — checkpoint 6 / final hardening
- Updated docs to explicitly keep verifier/researcher/steward renewal as future-only behavior requiring separate approval and the same boundary gates.
- Addressed final bug-check findings:
  - `F153-FBC-001`: continuation-pack generation now fails closed on git capture errors and writes no pack on failure.
  - `F153-FBC-002`: redaction now covers spaced key/value forms and Authorization bearer tokens.
- Reran targeted Python and TypeScript validation for context-renewal code.
- Final verifier bug-check approved at revision 10 with `bug_check_status: passed` and no open findings.
- Steward review completed before final verifier bug-check.
- Steward decision: `cleanup_recommended`; placement was clean, no restructuring requested.
- Cleanup performed: removed generated `.pytest_cache/` and Python `__pycache__/` directories from scripts, src, tests, and pipeline-diagram paths.
- Unrelated `dev-plans/agentops/coder-verifier-workflow/runs/issue-154/oracle/0001-loop-plan-attempt-1.log` is tracked and was left untouched.

## Changed files
- `docs/agentops-context-renewal.md`
- `pi-packages/agentops-context-renewal/package.json`
- `pi-packages/agentops-context-renewal/lib/policy.ts`
- `pi-packages/agentops-context-renewal/extensions/context-renewal.ts`
- `scripts/agentops/pi-agent.sh`
- `scripts/agentops/context-renewal-boundary.py`
- `scripts/agentops/context-renewal-pack.py`
- `scripts/agentops/context-renewal-preflight.py`
- `scripts/agentops/context-renewal-resume.py`
- `src/agentops_harness/context_renewal_boundary.py`
- `src/agentops_harness/context_renewal_pack.py`
- `src/agentops_harness/context_renewal_preflight.py`
- `src/agentops_harness/context_renewal_resume.py`
- `term-control-center/tests/contextRenewal.test.ts`
- `tests/unit/test_context_renewal_boundary.py`
- `tests/unit/test_context_renewal_pack.py`
- `tests/unit/test_context_renewal_preflight.py`
- `tests/unit/test_context_renewal_resume.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T144809Z/STATE.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T144809Z/CONTINUATION_PROMPT.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T145002Z/STATE.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T145002Z/CONTINUATION_PROMPT.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T145747Z/STATE.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T145747Z/CONTINUATION_PROMPT.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r1-policy-global-activation-design.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r2-global-extension-foundation.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r3-global-extension-foundation-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r4-continuation-pack-generator.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r5-continuation-pack-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r6-safe-boundary-status.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/review-request-r7-safe-boundary-fix.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/safe-boundary-r8.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/manual-resume-plan-r8.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T150817Z/STATE.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/continuation/20260629T150817Z/CONTINUATION_PROMPT.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/safe-boundary-r8-latest.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow/manual-resume-plan-r8-latest.md`

## Validation results
- `git diff --check`: passed.
- `cd term-control-center && node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 tests/contextRenewal.test.ts`: passed, 5 tests after revision 3.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_context_renewal_preflight.py`: passed, 5 tests after revision 3.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_context_renewal_pack.py tests/unit/test_context_renewal_resume.py tests/unit/test_context_renewal_boundary.py tests/unit/test_context_renewal_preflight.py`: passed, 18 tests after final bug-check fixes.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_context_renewal_resume.py tests/unit/test_context_renewal_boundary.py tests/unit/test_context_renewal_pack.py tests/unit/test_context_renewal_preflight.py`: passed, 16 tests before final bug-check fixes.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_context_renewal_boundary.py tests/unit/test_context_renewal_pack.py tests/unit/test_context_renewal_preflight.py`: passed, 13 tests after revision 7.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_context_renewal_pack.py tests/unit/test_context_renewal_preflight.py`: passed, 9 tests after revision 5.
- `python3 -m py_compile scripts/agentops/context-renewal-resume.py src/agentops_harness/context_renewal_resume.py scripts/agentops/context-renewal-boundary.py src/agentops_harness/context_renewal_boundary.py scripts/agentops/context-renewal-pack.py src/agentops_harness/context_renewal_pack.py scripts/agentops/context-renewal-preflight.py src/agentops_harness/context_renewal_preflight.py`: passed.
- `scripts/agentops/context-renewal-pack.py --issue-url https://github.com/hyperbotsx/agentops-harness/issues/153 --artifact-folder dev-plans/agentops/coder-verifier-workflow/runs/issue-153-context-renewal-workflow --checkpoint '3 - Continuation-pack generator' --revision 5 --stop-reason 'checkpoint dry run after verifier findings' --next-action 'request verifier checkpoint 3 re-review' ...`: passed; wrote `continuation/20260629T145747Z/STATE.md` and `CONTINUATION_PROMPT.md`.
- `scripts/agentops/context-renewal-boundary.py --format json`: passed command execution with exit 2 blocked status for unknown state.
- `scripts/agentops/context-renewal-boundary.py --no-coms-in-flight --no-active-command --no-partial-edit --git-status-captured --artifact-state-captured --operator-confirmed --format json`: passed command execution with `blocked` because continuation pack completion was not provided.
- `scripts/agentops/context-renewal-boundary.py --no-coms-in-flight --no-active-command --no-partial-edit --git-status-captured --artifact-state-captured --continuation-pack-completed --operator-confirmed --format json`: passed with `reset_allowed: true`.
- `scripts/agentops/context-renewal-resume.py --state .../STATE.md --prompt .../CONTINUATION_PROMPT.md --boundary-json .../safe-boundary-r8.json --format markdown`: passed; wrote manual-ready plan to `manual-resume-plan-r8.md`.
- Regenerated latest checkpoint 5 continuation pack `20260629T150817Z`, boundary JSON, and `manual-resume-plan-r8-latest.md`: passed.
- `scripts/agentops/context-renewal-preflight.py --format json | python3 -m json.tool`: passed; reports terminal Pi/hyper-pi unsupported because local settings do not reference the package and AgentOps wrapper normal because flag is disabled.
- `AGENTOPS_CONTEXT_RENEWAL=1 scripts/agentops/context-renewal-preflight.py --format json | python3 -m json.tool`: passed; reports AgentOps wrapper active and terminal Pi/hyper-pi unsupported.
- `AGENTOPS_CONTEXT_RENEWAL=1 PI_AGENT_CONTEXT_RENEWAL_EXTENSION=/tmp/agentops-missing-renewal scripts/agentops/context-renewal-preflight.py --format json | python3 -m json.tool`: passed; reports all entry points blocked on the missing effective package path.
- `cd term-control-center && npm test -- --test-name-pattern "context renewal"`: failed before tests because this worktree lacks local `term-control-center/node_modules`; Node could not resolve `tsx`.
- `cd term-control-center && npm run typecheck`: failed because this worktree lacks local TypeScript/React/xterm dependencies in `node_modules`; errors are dependency-resolution/ambient type failures unrelated to checkpoint files.
- Earlier checkpoint 1 full-suite attempts:
  - `python -m pytest tests`: failed because `python` is not installed in this environment.
  - `python3 -m pytest tests`: failed during collection with `ModuleNotFoundError: No module named 'agentops_harness'` because `PYTHONPATH=src` was not set.
  - `PYTHONPATH=src python3 -m pytest tests`: ran 1011 tests; 1007 passed, 4 failed. Failures appear unrelated/environmental and are listed below:
    - `tests/unit/test_agent_github_health.py::test_agent_github_check_rejects_config_dir_without_agent_token` expected fail but got pass.
    - `tests/unit/test_ai_maestro_handoff_emit.py::HandoffEmitTests::test_emit_sends_to_unix_socket_when_available` failed with `OSError: AF_UNIX path too long` under the current long temp runtime path.
    - `tests/unit/test_github_cli_env.py::test_agent_gh_env_uses_dedicated_config_and_strips_ambient_tokens` expected `/tmp/agentops-gh`, got `/home/hyperbots/.config/agentops-harness/gh-agent`.
    - `tests/unit/test_github_cli_env.py::test_agent_gh_env_can_inject_dedicated_token` expected `/tmp/agentops-gh`, got `/home/hyperbots/.config/agentops-harness/gh-agent`.

## Acceptance/checkpoint mapping
- Thresholds and state model: documented in `docs/agentops-context-renewal.md` and implemented in `pi-packages/agentops-context-renewal/lib/policy.ts`.
- Safe-boundary rules: documented and read-only boundary checker implemented with fail-closed unknown-state behavior.
- Artifact paths/templates: continuation pack folder and required `STATE.md` / `CONTINUATION_PROMPT.md` contents documented and dry-run generator implemented.
- Feature flags: documented and partially implemented for extension loading and thresholds.
- Global Pi activation: terminal Pi, hyper-pi, and `pi-agent.sh --no-extensions` behavior documented; AgentOps wrapper wiring implemented behind `AGENTOPS_CONTEXT_RENEWAL`; terminal Pi/hyper-pi preflight reports unsupported until their settings reference the package.
- Project 3 routing: recorded in this handoff and design doc authority section.
- Reset automation: fully automatic reset not implemented; manual coder resume plan prints the continuation prompt only after safe-boundary and operator-confirmation evidence.

## Open risks / next exact action
- Next checkpoint should complete documentation/final hardening, then request Steward review before final bug-check because package/scripts/run artifacts were added.
- Manual resume exists as a prompt-printing fallback only; no automated pane reset/injection behavior exists yet.
- Full suite currently has pre-existing/environmental failures listed above; rerun with a shorter temp path, local node install, and review GitHub env precedence if full-suite green is required.
