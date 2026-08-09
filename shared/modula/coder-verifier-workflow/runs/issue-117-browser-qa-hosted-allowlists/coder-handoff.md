# Coder handoff — Issue #117 Browser-QA hosted DevTools allowlists

## Source of truth
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/117
- Branch: `prd/browser-qa-hosted-allowlists-117`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-117`

## Preflight
- PRD read first: yes.
- Initial git status: clean (`## prd/browser-qa-hosted-allowlists-117...origin/main`).
- Memory: disabled, advisory only.
- Allowed paths: `term-control-center/server/frontendBrowserLaunch.ts`, `term-control-center/server/launchPlan.ts`, targeted `term-control-center/tests/*.test.ts`, this run folder, and `dev-plans/agentops/open-prd-sweep-ledger-2026-06-28.md`.
- Forbidden paths/actions: secrets, browser profiles/cookies/storage, deployment config, product routes unrelated to Browser-QA launch, PR creation, merge, deploy, approval, trading, backtests.
- Stop condition: final verifier implementation and bug-check approval, or human escalation.

## Checkpoints
1. Effective allowlist and MCP regeneration: merge task `previewUrl` origin pattern with `TERM_CONTROL_BROWSER_ALLOWED_URL_PATTERNS`, regenerate per-agent MCP config on every launch, preserve localhost-only default.
2. Diagnostics and fail-closed behavior: expose non-secret allowlist/config/regeneration/redacted args diagnostics, and block non-allowlisted hosted targets with actionable messages.
3. Validation, ledger, steward hygiene, final verifier bug-check.

## Research freshness consult
- Date: 2026-06-29.
- Researcher verdict: standalone Claude MCP JSON with repeated allowlist args remains valid; strict Claude `mcp_config` usage remains valid.
- Key facts: `chrome-devtools-mcp@latest` supports repeated `--allowedUrlPattern` / `--allowed-url-pattern` flags; `--browserUrl` connects to the running browser but does not restrict URLs; strict `--mcp-config` limits Claude Code to the supplied MCP servers.
- Cautions recorded: use an isolated Chrome profile, keep hosted allowlists narrow, include required preview origins only, keep `--no-performance-crux` and usage-stat opt-out, and do not treat header redaction as protection for URLs/screenshots/bodies/storage.

## Implementation status
- Checkpoint 1/2 implemented and ready for verifier review.
- `browserAgentChromeDevtoolsServer` now builds Chrome DevTools MCP args from the effective current-task allowlist and emits repeated `--allowed-url-pattern=<pattern>` args.
- Effective allowlists merge configured `TERM_CONTROL_BROWSER_ALLOWED_URL_PATTERNS` with the current task `previewUrl` origin pattern.
- Browser-QA host prompt now includes diagnostics: effective allowlist patterns, MCP config path, regeneration reason, redacted MCP launch args, and warnings.
- Browser-QA host prompt instructs fail-closed behavior before navigation when a hosted target is absent from the effective allowlist.
- Browser-QA host prompt now explicitly forbids extracting, copying, logging, reporting, or exposing cookies, tokens, authorization headers, local/session storage, IndexedDB, cache contents, or other browser storage values.
- Tests cover localhost-only defaults, hosted `https://ops.evono.me/*` regeneration over a stale previous config, diagnostics, disabled Browser-QA pane behavior, cookie/session/token diagnostics redaction, and the secret/storage prompt guard.
- Shared validation ledger updated for PRD #117.

## Changed files
- `term-control-center/server/frontendBrowserLaunch.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/tests/frontendBrowserLaunch.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `dev-plans/agentops/open-prd-sweep-ledger-2026-06-28.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/review-request-r1-hosted-allowlists.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/review-request-r2-f117-r1-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/steward-request-r1-prefinal-hygiene.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/review-request-r3-final-bug-check.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/review-request-r4-f117-r3-001.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-117-browser-qa-hosted-allowlists/verifier-report.md`

## Validation
- PASS: `TMPDIR=$(mktemp -d) env -u AGENTOPS_GITHUB_TOKEN -u GH_TOKEN -u GITHUB_TOKEN -u TERM_CONTROL_CEO_REVIEW_WORKTREE -u TERM_CONTROL_CEO_REVIEW_REF -u TERM_CONTROL_BROWSER_ALLOWED_URL_PATTERNS -u TERM_CONTROL_BROWSER_USER_DATA_DIR -u TERM_CONTROL_BROWSER_CDP_PORT -u TERM_CONTROL_BROWSER_CDP_PROXY_PORT -u TERM_CONTROL_BROWSER_VNC_PORT -u TERM_CONTROL_BROWSER_STATE_DIR /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/.bin/tsx --test term-control-center/tests/frontendBrowserLaunch.test.ts term-control-center/tests/launchPlan.test.ts` — 27/27 subtests passed after F117-R3-001 fix.
- PASS: `git diff --check` — no whitespace errors.
- PASS: `TMPDIR=$(mktemp -d) env -u AGENTOPS_GITHUB_TOKEN -u GH_TOKEN -u GITHUB_TOKEN -u TERM_CONTROL_CEO_REVIEW_WORKTREE -u TERM_CONTROL_CEO_REVIEW_REF -u TERM_CONTROL_BROWSER_ALLOWED_URL_PATTERNS -u TERM_CONTROL_BROWSER_USER_DATA_DIR -u TERM_CONTROL_BROWSER_CDP_PORT -u TERM_CONTROL_BROWSER_CDP_PROXY_PORT -u TERM_CONTROL_BROWSER_VNC_PORT -u TERM_CONTROL_BROWSER_STATE_DIR /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/.bin/tsx --test --test-name-pattern='Browser QA' term-control-center/tests/launchPlan.test.ts` — 4/4 Browser-QA subtests passed after F117-R3-001 fix.
- BLOCKED: `npm --prefix term-control-center test -- --test-name-pattern='Browser QA|Frontend Expert'` — local `term-control-center/node_modules` missing; package cannot resolve `tsx`.
- BLOCKED: `/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/.bin/tsc -p term-control-center/tsconfig.server.json --noEmit` — local type package resolution missing.
- BLOCKED with shared type roots: `/mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/.bin/tsc -p term-control-center/tsconfig.server.json --noEmit --typeRoots /mnt/hyperliquid-data/projects/repos/agentops-harness/term-control-center/node_modules/@types` — pre-existing unresolved optional modules/types: `node-pty`, `react-dom/server`, plus related implicit any/WebSocket namespace errors.

## Findings addressed
- F117-R1-001: Added explicit Browser-QA host prompt guard against extracting/copying/logging/reporting/exposing cookies, tokens, authorization headers, localStorage/sessionStorage, IndexedDB, cache contents, and other browser storage values; added focused prompt assertions.
- F117-R3-001: Expanded diagnostics redaction to cover cookie/session-style query keys and added a focused Browser-QA diagnostic redaction test.

## Verifier status
- Revision 1 requested F117-R1-001.
- Revision 2 approved implementation checkpoint.
- Steward pre-final hygiene: clean, no cleanup needed; noted `verifier-report.md` is a standard evidence artifact.
- Final verifier bug-check revision 3 requested F117-R3-001.
- Final verifier bug-check revision 4 approved; bug-check passed. Next actor: human.
