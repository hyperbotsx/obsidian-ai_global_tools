# Coder Handoff — Issue #209 Browser QA delegate diagnostics

## Scope
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/209
- Branch: `prd/browser-qa-delegate-completion-diagnostics-209`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-209`
- Pre-existing dirty files before editing: none (`git status --short --branch` was clean on this branch)

## Allowed / forbidden / stop condition
- Allowed: Browser QA wrapper/preflight/lifecycle code, redacted result artifacts/status reason codes, tests, fixtures, docs.
- Forbidden: product app code, weakened allowlists/MCP sandboxing, unmanaged Chrome profiles, browser storage/secrets, PR/merge/deploy/approval/trading/backtest actions.
- Stop condition for this checkpoint: verifier approval of preflight taxonomy/validation plus initial lifecycle artifact classification, or bounded revision request.

## Researcher consult
Mandatory PRD research-first consult completed 2026-07-13 via coms.
Key findings recorded:
- `pi-claude-agent` tmux backend waits on `done.json`; timeout returns an error with artifact/capture paths, while `SessionEnd` only writes `session-end.json`.
- Stop hook writes `final.md` and `done.json`; artifacts are local debugging output, not sanitized logs.
- Chrome DevTools MCP allowlist should be treated as defense-in-depth; local Chrome observed below docs' stated Chrome 149 requirement, so harness preflight must be primary.
- Existing AgentOps Browser QA only checked `task.previewUrl`; GitHub-only/no-preview targets were not classified fail-closed.

## Checkpoints
1. Preflight design and reason-code taxonomy — implemented.
2. URL/allowlist/auth/MCP validation behavior — implemented with tests.
3. Delegate lifecycle monitoring and artifact writing — initial monitor implemented with tests for closed/timeout.
4. Browser control-state wait/fail-closed behavior — initial wait-state classification implemented with tests.
5. Test coverage and docs — initial docs/tests added.
6. Final bug-check pending after implementation approval and steward hygiene.

## Changed files
- `term-control-center/server/browserQaLifecycle.ts` — new Browser QA preflight/result/lifecycle helper.
- `term-control-center/server/frontendBrowserLaunch.ts` — exports browser launch plan for harness-owned validation.
- `term-control-center/server/launchPlan.ts` — runs Browser QA preflight for context-backed launches and exports artifact env to the Browser QA pane.
- `term-control-center/server/serverMonitors.ts` — starts Browser QA lifecycle monitor with existing server monitors.
- `term-control-center/tests/browserQaLifecycle.test.ts` — regression tests for missing target, allowlist mismatch, auth marker, redaction, MCP config, report-ready success, stale report retry safety, browser-qa-session baseline preference, closed delegate, timeout, and human-control wait.
- `term-control-center/README.md` — documents infrastructure failure reason codes vs product QA report failures.

## Revision fixes
- Addressed `V209-001`: result/diagnostic artifacts and Browser QA diagnostic env now redact secret-like URL values before persistence; added regression coverage for synthetic `token`, `cookie`, `authorization`, and `session_id` values.
- Addressed `V209-002`: preflight now requires an explicit auth marker from the constructed launch env instead of inferring `preflight_pending` from Browser QA pane presence; added a real-shaped missing-auth regression while preserving `interactive_auth_detected` pass behavior.
- Addressed `V209-003`: report-ready detection now uses the newest launch/session creation baseline so stale matching reports are ignored even when Browser QA starts after the parent group; added stale/fresh retry coverage.
- Addressed `V209-004`: `report_ready` result artifacts now include structured `artifacts.browserQaReport` and omit unwritten failure report paths.
- Addressed `BC209-001`: Browser QA launch warnings are redacted before diagnostic/artifact persistence or env propagation; added malformed preview target regression coverage.

## Validation
- PASS: `NODE_PATH=/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules node --import /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/tsx/dist/loader.mjs --test --test-concurrency=1 term-control-center/tests/browserQaLifecycle.test.ts term-control-center/tests/launchPlan.test.ts term-control-center/tests/completedBrowserQaReport.test.ts` (44/44 tests passed; rerun after `BC209-001` fix)
- PASS: `git diff --check` (rerun after steward)
- BLOCKED/PRE-EXISTING: `cd term-control-center && /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/.bin/tsc -p tsconfig.server.json --noEmit --typeRoots /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/@types` remains blocked by existing missing optional modules/types: `node-pty`, `react-dom/server`, plus existing implicit any errors in `index.ts`/`launchGroup.ts` from unresolved `node-pty` (rerun after `BC209-001` fix).
- BLOCKED/PRE-EXISTING: `npm --prefix term-control-center test -- --test-name-pattern='Browser QA|browser qa|Browser-QA'` cannot start in this worktree because local `term-control-center/node_modules` is absent (`ERR_MODULE_NOT_FOUND: tsx`). Used the repo-installed shared `tsx` path above.

## Steward
- PASS: Steward hygiene review returned `clean`; response saved at `dev-plans/agentops/coder-verifier-workflow/runs/issue-209-browser-qa-delegate-diagnostics/steward-response-r1-final-hygiene.md`.
- PASS: Steward recheck after `BC209-001` fix returned `clean`; response saved at `dev-plans/agentops/coder-verifier-workflow/runs/issue-209-browser-qa-delegate-diagnostics/steward-response-r2-bugfix-hygiene.md`.

## Final verifier status
- Final verifier bug-check fix review approved revision 7 with `bug_check_status: completed_clean`.
- Final report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-209-browser-qa-delegate-diagnostics/verifier-report.md`.

## Notes / risks for verifier
- Preflight is enforced when `buildCoderVerifierLaunchPlan` has a real context path (the actual launch path writes `/tmp/agentops/term-context/<group>/task-context.md`). Existing unit tests that build plans without context remain non-mutating.
- Diagnostics artifacts are redacted; raw effective allowlist is kept in memory only for matching and stripped before writing.
- Lifecycle monitor classifies report-ready success plus outer Browser QA pane closure/timeout/human-control state. It does not read raw tmux captures or browser storage.
- Browser actions are conservatively recorded as `false` for infrastructure failures.
