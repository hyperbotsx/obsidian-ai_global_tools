# Coder Handoff — Issue 138 Browser QA completion action

## Task
- GitHub issue / PRD: https://github.com/hyperbotsx/agentops-harness/issues/138
- Branch: `prd/on-demand-browser-qa-completion-action-138`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`
- PRD status: Approved; CEO approved in issue comment.

## Pre-edit status
- `git status --short --branch`: `## prd/on-demand-browser-qa-completion-action-138...origin/prd/on-demand-browser-qa-completion-action-138 [ahead 1]`
- Pre-existing dirty files: none.

## Scope controls
- Allowed paths: completion action state/routes/UI, existing Browser QA route integration, freshness UI guard, completion/activity state, launch-time Browser QA diagnostics, launch/preflight hygiene, focused tests/docs if required.
- Forbidden: PR creation, merge, deploy, approval, trading, backtest, duplicate Browser QA launcher, broad #113 validation table, raw transcripts/secrets.
- Research-first surfaces: none in PRD.
- Stop condition: final verifier bug-check approval or human escalation.

## Verifier checkpoints covered
1. Browser QA action surface, failed-fetch route/auth/base-path, route reuse/idempotency, focus/failure handling.
2. PR-created/merge refresh visibility and safe generated-view reload deferral.
3. Post-merge closeout/activity state removal or pending closeout/teardown copy.
4. Launch-time Browser QA force_on diagnostics/retry cleanliness and launch hygiene around self-generated `uv.lock`.
5. Guardrails and final validation/bug-check.

## Implementation summary
- Added explicit hosted nginx proxy coverage for `POST /term/groups/:id/browser-qa`, preserving Authentik identity headers and routing to the existing Term Control route.
- Hardened Browser QA open failures in the Term UI: network/proxy fetch failures now show bounded actionable copy instead of raw `Failed to fetch`.
- Kept route reuse/idempotency through the existing server path; no second Browser QA launcher was added.
- Browser runtime startup failures now clean partial managed runtime processes and classify VNC/display/Chrome/CDP failures with retry and explicit `auto/off` fallback guidance.
- Completion action PR/merge responses now push returned pipeline refresh status into the board status line and the shared freshness indicator through an existing freshness module hook.
- Freshness reloads are deferred while terminal modals, completion center, dialogs, or focused form inputs are active; the control changes to `Reload when safe` and performs the deferred reload only when not busy.
- Completion notifications now show explicit `needs closeout` after merge/sync and `needs teardown` after closeout; fully torn-down sessions no longer produce active completion notifications, and teardown records are retained as history.
- Launch hygiene revision for F138-R1-001: removed unsafe `uv.lock` deletion. Arbitrary untracked `uv.lock` now remains in place and blocks launch like any real dirty file. The AgentOps GitHub preflight command in `scripts/agentops/pi-agent.sh` now runs from a temporary isolated cwd so it cannot generate lockfiles in the target implementation worktree.
- Steward cleanup HYG-138-001 completed: removed ignored generated Python artifacts `pipeline-diagram/__pycache__/`, `src/agentops_harness/__pycache__/`, and `src/agentops_harness.egg-info/`.

## Changed files
- `scripts/agentops/pi-agent.sh`
- `pipeline-diagram/board.html`
- `pipeline-diagram/deploy/ops.evono.me.nginx`
- `pipeline-diagram/freshness.js`
- `term-control-center/server/browserRuntime.ts`
- `term-control-center/server/completionRetention.ts`
- `term-control-center/server/implementationWorktreeSync.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/shared/completion.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/browserRuntime.test.ts`
- `term-control-center/tests/completion.test.ts`
- `term-control-center/tests/implementationWorktreeSync.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/nginxProxy.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/review-request-r1-implementation.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/review-request-r2-f138-r1-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/review-request-r3-final-bug-check.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/steward-request-r1.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-138-browser-qa-completion-action/verifier-report.md`

## Validation
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion.test.ts tests/implementationWorktreeSync.test.ts tests/launchPlan.test.ts tests/browserRuntime.test.ts tests/nginxProxy.test.ts tests/termBasePath.test.ts tests/boardGuardrails.test.ts tests/admin.test.ts` — pass (128 tests).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/admin.test.ts tests/boardGuardrails.test.ts && npm run typecheck` — pass.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/implementationWorktreeSync.test.ts tests/launchPlan.test.ts tests/launcher.test.ts && npm run typecheck` — pass (F138-R1-001 revision validation).
- `git diff --check && cd term-control-center && npm run typecheck` — pass.
- `node --check pipeline-diagram/freshness.js` — pass.
- Verifier R1 also ran `git diff --check && node --check pipeline-diagram/freshness.js` — pass.
- Note: an earlier overly broad `npm test -- --test-name-pattern ...` invocation timed out after running unrelated full-suite tests and hit pre-existing/flaky server tmux/planner tests; targeted tests above passed.

## Reviews / findings
- Verifier R1: `revision_requested`, finding `F138-R1-001`.
- Verifier R2: `approved`, open findings 0.
- Steward R1: requested HYG-138-001 and HYG-138-002. Both addressed.
- Verifier R3 final bug-check: `approved`, `bug_check_status: passed`, open findings 0.

## Findings addressed
- `F138-R1-001`: Fixed by removing blind `uv.lock` cleanup, adding tests that arbitrary untracked `uv.lock` is preserved and blocks launch, and isolating AgentOps GitHub preflight cwd to avoid target-worktree lockfile generation.
- `HYG-138-001`: Removed ignored Python artifacts.
- `HYG-138-002`: Updated this handoff to include R2/steward/verifier report artifacts.

## Known risks / notes
- Manual browser QA steps remain unrun in this headless coding pass.
- Final verifier bug-check approved; next actor is human.
