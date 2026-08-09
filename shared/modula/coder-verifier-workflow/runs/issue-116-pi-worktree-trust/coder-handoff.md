# Coder handoff — Issue #116 Pi worktree trust

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/116
- PRD status: approved in issue body; CEO approved.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-116`
- Branch: `prd/d1-prd-auto-trust-harness-launched-116`
- PR: https://github.com/hyperbotsx/agentops-harness/pull/155

## Pre-edit status
- `git status --short --branch`: clean (`## prd/d1-prd-auto-trust-harness-launched-116...origin/main`).
- Pre-existing dirty files: none.
- Local Pi trust flag confirmation: `pi --help` lists `--approve, -a` as "Trust project-local files for this run" and `--no-approve, -na` as the inverse.
- Researcher freshness consult: not required by PRD; no external/volatile API surface touched.

## Scope boundaries
Allowed paths from PRD:
- Harness launch planning and session state.
- `scripts/agentops/pi-agent.sh` or equivalent launch wiring.
- Tests for per-run Pi trust, exact cwd, negative trust scope, UI-visible state, and artifact evidence.
- Coder/verifier run artifacts and required validation ledger notes.

Forbidden:
- No broad trust for `/mnt/hyperliquid-data/projects/worktrees`, sibling worktrees, or unrelated temp worktrees.
- No silent fallback to parent-path trust.
- No unrelated launch roles, approval flows, deployments, trading, backtests, PR creation, or merge.

Validation targets:
- Focused TypeScript launch-plan/workspace-trust/pi-agent tests.
- Typecheck/build only if local dependencies are available.
- Later smoke launch evidence after verifier approves command construction and negative trust tests.

Stop condition:
- Stop after final verifier bug-check approval or human escalation; do not create PR.

## Verifier checkpoints
1. Launch command construction before live smoke testing.
2. Negative trust-scope tests for unrelated temp worktree, sibling worktree, and shared parent path.
3. Final live launch evidence and issue-scoped artifact contents.

## Current checkpoint
- Checkpoint 1/2 approved by verifier revision 1.
- Checkpoint 3 approved by verifier revision 1; verifier response also reported final bug-check passed.
- Steward final hygiene review returned clean; no cleanup needed.
- Final verifier closeout after steward approved revision 1 with bug-check passed and zero open findings.
- Checkpoint 3 smoke evidence collected with fake `pi` to prove the real `scripts/agentops/pi-agent.sh` wrapper forwards `--approve`, keeps cwd at `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-116`, and uses issue-scoped `PI_COMS_DIR` without showing a trust prompt.

## Changes made
- Added shared launch trust state types so session group task state can expose Pi trust evidence in UI-visible `/groups` state.
- Updated implementation launch args to pass `--approve` through the `pi-agent.sh` wrapper for every harness-launched implementation pane while preserving exact `command.cwd` as the task worktree.
- Added issue-scoped Pi trust evidence writing to the runtime artifact root as `pi-trust-evidence.json` with issue number, worktree path, mechanism, persisted-trust status, result, timestamp, evidence path, and failure reason when applicable.
- Added fail-closed Pi trust setup handling before persistent Claude/Codex trust or pane launch when evidence writing/scope checks fail.
- Kept existing Claude/Codex trust behavior unchanged and did not add persistent Pi trust decisions.
- Added focused tests for `--approve` args, exact cwd, issue-scoped evidence, UI-visible trust state, no parent/sibling/temp saved trust entries, and fail-closed evidence-write failure.

## Changed files
- `term-control-center/shared/launcher.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/validation-ledger-log.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/review-request-r1-checkpoint-1-2.json`
- `dev-plans/agentops/open-prd-sweep-ledger-2026-06-28.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/pi-agent-approve-smoke.txt`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/review-request-r2-checkpoint-3.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/steward-request-r1-final-hygiene.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/steward-response-r1-final-hygiene.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/review-request-r3-final-after-steward.json`

## Validation
- `cd term-control-center && TMPDIR=$(mktemp -d) env -u TERM_CONTROL_CEO_REVIEW_WORKTREE -u TERM_CONTROL_CEO_REVIEW_REF -u TERM_CONTROL_CEO_REVIEW_ARTIFACT_ROOT -u TERM_CONTROL_BROWSER_USER_DATA_DIR -u TERM_CONTROL_BROWSER_STATE_DIR -u TERM_CONTROL_BROWSER_CDP_PORT -u TERM_CONTROL_BROWSER_CDP_PROXY_PORT -u TERM_CONTROL_BROWSER_VNC_PORT tsx --test tests/launchPlan.test.ts tests/workspaceTrust.test.ts tests/agentopsComsLabel.test.ts`
  - Result: passed, 27 tests.
- `cd term-control-center && npm run typecheck`
  - Result: failed before validating this change because local `term-control-center/node_modules` is absent/incomplete; errors include missing `react`, `react/jsx-runtime`, `@xterm/xterm`, and type declarations.
- `cd term-control-center && tsc -p tsconfig.server.json --noEmit`
  - Result: failed because local `@types/node` is unavailable.
- Wrapper smoke with fake `pi`:
  - `PATH=<fake-pi> PI_AGENT_SKILLS_DIR=<temp-skills> PI_AGENT_CLAUDE_EXTENSION=0 PI_AGENT_PATCH_PI_COMS_LOCAL=0 NVM_DIR=<temp-nvm> scripts/agentops/pi-agent.sh coder --approve --model smoke-model --thinking low 'smoke prompt' > dev-plans/agentops/coder-verifier-workflow/runs/issue-116-pi-worktree-trust/pi-agent-approve-smoke.txt`
  - Result: passed; output records `--approve`, cwd `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-116`, and `PI_COMS_DIR=/tmp/agentops/coms/agentops-prd-116`.
- `git diff --check`
  - Result: passed after final handoff/steward updates.

## Known risks / follow-up
- Full live Term Control server launch smoke could not be run in this worktree because local server-test dependencies such as `ws` are unavailable; wrapper-level smoke evidence is recorded.
- Runtime artifact root is outside the repo worktree; the in-repo handoff records the implementation evidence, while the harness writes per-launch Pi trust evidence at runtime.
- Local typecheck requires installing/restoring `term-control-center` dependencies; focused tests ran through PATH-resolved `tsx`.
