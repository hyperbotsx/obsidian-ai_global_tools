# Coder Handoff — PRD #47 Feature Validation Ledger

## Source of truth
- PRD issue: https://github.com/hyperbotsx/agentops-harness/issues/47
- Approval verified: PRD status Approved, CEO approved Yes, `status:approved` label present on 2026-06-20.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Branch: `prd/feature-validation-ledger-agent-assisted-acceptance-47`

## Pre-existing dirty state
- Before approval/readiness work: clean branch (`git status --short --branch` showed no dirty files).
- Before implementation checkpoint 1: clean branch after GitHub approval mutations; no repo-local files changed.

## Scope controls
- Allowed after approval: ledger schemas/models/fixtures/parsers/renderers, durable local/state storage, closeout integration, dashboard/manual workflow, Play launch planning, Browser QA hooks, evidence/report capture, redaction/audit helpers, docs/tests.
- Forbidden: PRD approval bypass, other PRD approval, PR creation, merge, deploy, production data mutation, automatic validation-agent launch, autonomous verified status, browser/security bypass, secret/raw transcript/session token storage, hardcoded product names/Project 2/tracker #862/field names/worktree defaults, repo-local canonical PRD copies.
- Stop condition: stop after each verifier checkpoint approval; after all checkpoints, final verifier bug-check approval.

## Verifier checkpoints
1. Ledger model and fixtures — current.
2. Closeout integration.
3. Dashboard/manual workflow.
4. Play button and validation-agent launch.
5. Browser validation hook.
6. Evidence and audit.
7. Wrong-context hardening.
8. Final bug-check.
9. Profile/project checkpoint.
10. Implementation preflight checkpoint.

## Mandatory research completed
- GitHub Projects v2 (researcher, 2026-06-20): use live GraphQL/`gh` state; require `read:project`/`project` scopes as appropriate; fail closed on REDACTED/null/incomplete pagination/rate limits/missing fields; PR merge evidence must use `merged`, `mergedAt`, `mergeCommit`; avoid `fieldValueByName` as authoritative when duplicate names are possible.
- PRD #39 browser runtime (researcher, 2026-06-20): Browser QA is existing CLI/runtime evidence ingestion, dry-run only for runtime launch, Claude Code + Chrome assumptions; no Playwright assumption; browser-required ledger items must fail closed when Chrome/Claude/extension/feed/evidence unavailable.
- Term Control Center launch/session contract (researcher, 2026-06-20): reuse token-guarded `/launch` and session-group primitives; browser should send typed IDs/options only; server owns prompt; new validation role requires central allowlist/tests; Play must not approve, PR, merge, deploy, or mutate GitHub autonomously.

## Checkpoint 1 implementation
Changed files:
- `src/agentops_harness/validation_ledger.py`
- `tests/unit/test_validation_ledger.py`
- `tests/fixtures/feature_validation_ledger.sample.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/prd-47-feature-validation-ledger/coder-handoff.md`

Implemented:
- Ledger constants for validation modes and statuses.
- Dataclasses for ledger item, evidence, status history, validation result, and transition result.
- Required-field validation, project context validation, validation mode/status/area checks, timestamp checks, checklist rule for non-`not_applicable` items.
- Explicit status transition table and audited transition helper.
- Parser from dict payloads with evidence redaction.
- Evidence redaction for bearer auth, Authorization headers, cookies, token/secret/password/credential/API/private/session keys, identity headers, and private local secret paths.
- Safe sample fixtures covering `manual`, `agent_cli`, `agent_browser`, `agent_mixed`, and `not_applicable` modes.
- Unresolved-first ordering helper for later dashboard work.

## Validation run
Revision 1:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_validation_ledger.py` — passed, 9 tests.
- `python3 -m py_compile src/agentops_harness/validation_ledger.py tests/unit/test_validation_ledger.py` — passed.
- `git diff --check -- src/agentops_harness/validation_ledger.py tests/unit/test_validation_ledger.py tests/fixtures/feature_validation_ledger.sample.json` — passed.

Revision 2 after verifier findings VL-001, VL-002, VL-003:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_validation_ledger.py` — passed, 11 tests.
- `python3 -m py_compile src/agentops_harness/validation_ledger.py tests/unit/test_validation_ledger.py` — passed.
- `git diff --check -- src/agentops_harness/validation_ledger.py tests/unit/test_validation_ledger.py tests/fixtures/feature_validation_ledger.sample.json` — passed.

## Findings addressed
- VL-001: redacts full Cookie/Set-Cookie header values and all Authorization schemes/values, with regression coverage for multi-cookie and Basic authorization headers.
- VL-002: malformed `source_prd_issue` now coerces to `0` and validation reports the missing required field instead of parser crash.
- VL-003: removed unused terminal-status constant and replaced multi-parameter transition helpers with `LedgerTransitionRequest`/`LedgerHistoryEvent` handoff.

## Checkpoint 2 implementation
Changed files added:
- `src/agentops_harness/validation_ledger_closeout.py`
- `tests/unit/test_validation_ledger_closeout.py`

Implemented:
- Pure closeout-to-ledger proposal helper that takes existing `CloseoutRequest`/`CloseoutLiveState` evidence plus explicit validation claims.
- `LedgerCloseoutContext` and `LedgerCloseoutClaim` to avoid hardcoded project/worktree/repository defaults.
- Fail-closed checks for missing project/owner/worktree context, missing explicit claims, invalid PRD/PR URLs, repository mismatch, unmerged PRs, missing merge commit, and wrong base branch.
- Deterministic project-scoped ledger item IDs.
- Evidence links for canonical PRD issue, merged PR, merge SHA, verifier report, and local sync commit without storing PRD body copies.
- Safe create/append path that blocks duplicate ledger item IDs instead of overwriting existing rows.
- `not_applicable` claim mode records a verified item with warning that explanatory evidence is still required.

Checkpoint 2 validation revision 1:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py` — passed, 18 tests.
- `python3 -m py_compile src/agentops_harness/validation_ledger.py src/agentops_harness/validation_ledger_closeout.py tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py` — passed.
- `git diff --check -- src/agentops_harness/validation_ledger.py src/agentops_harness/validation_ledger_closeout.py tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py tests/fixtures/feature_validation_ledger.sample.json` — passed.

Checkpoint 2 validation revision 2 after verifier findings VL-004, VL-005, VL-006:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py` — passed, 22 tests.
- `python3 -m py_compile src/agentops_harness/validation_ledger.py src/agentops_harness/validation_ledger_closeout.py tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py` — passed.
- `git diff --check -- src/agentops_harness/validation_ledger.py src/agentops_harness/validation_ledger_closeout.py tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py tests/fixtures/feature_validation_ledger.sample.json` — passed.

Checkpoint 2 findings addressed:
- VL-004: `LedgerCloseoutContext` now requires explicit PRD title; proposals preserve it and blank titles fail closed.
- VL-005: closeout proposal validation now reuses existing `prd_closeout` request validation so PRD issue URL, PR URL, and expected repository must match.
- VL-006: closeout proposal validation now reuses verifier/sync request validation and also blocks local sync commits that do not match the merge commit.

## Checkpoint 3 implementation
Changed files added:
- `term-control-center/shared/validationLedger.ts`
- `term-control-center/tests/validationLedger.test.ts`

Implemented:
- Shared dashboard view model for validation ledger tables with required columns: status, feature, PRD, PR, area, validation mode, evidence, age, and actions.
- Loading, empty, error, blocked, stale, and success table states.
- Unresolved-first row ordering and verified/deferred/superseded history separation.
- Item detail projection with checklist, evidence, and status history text.
- Manual status proposal helper for verified/needs-fix/deferred/superseded actions that requires human confirmation and evidence note; it does not mutate state.
- Row actions for Play, manual status actions, defer/supersede, and show evidence with disabled reasons.

Checkpoint 3 validation revision 1:
- `npm --prefix term-control-center run test -- validationLedger.test.ts` — passed; command ran the suite and 207 tests passed, including 7 validation-ledger tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check -- term-control-center/shared/validationLedger.ts term-control-center/tests/validationLedger.test.ts` — passed.

Checkpoint 3 validation revision 2 after verifier findings VL-007, VL-008, VL-009:
- `npm --prefix term-control-center run test -- validationLedger.test.ts` — passed; command ran the suite and 210 tests passed, including 10 validation-ledger tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check -- term-control-center/shared/validationLedger.ts term-control-center/src/ValidationLedgerDashboard.ts term-control-center/tests/validationLedger.test.ts` — passed.

Checkpoint 3 findings addressed:
- VL-007: added filter behavior plus a minimal rendered `ValidationLedgerDashboard` component with search/status/unresolved filters, table, details, action buttons, ARIA labels, and rendering/accessibility tests.
- VL-008: row actions and manual proposals now use the ledger transition map; Play is enabled only for eligible agent modes in `awaiting_validation`/`needs_fix`, and invalid manual transitions are blocked.
- VL-009: replaced the five-parameter manual proposal API with `ManualStatusProposalRequest`.

## Checkpoint 4 implementation
Changed files added:
- `term-control-center/shared/validationLedgerPlay.ts`
- `term-control-center/tests/validationLedgerPlay.test.ts`

Implemented:
- Human-clicked Play dry-run plan builder for one selected validation ledger item.
- Scoped validation prompt containing selected item ID, PRD/PR/merge context, achieved summary, checklist, evidence links, allowed actions, forbidden actions, and expected report path/format.
- Fail-closed checks for missing human click, ineligible validation modes, non-runnable statuses, missing checklist, invalid issue URL, relative worktree path, and missing context fields.
- Secret-like redaction for Play prompt fields.
- Regression proving unrelated ledger item text is not included in the selected item prompt.

Checkpoint 4 validation revision 1:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedgerPlay.test.ts` — passed; command ran the suite and 214 tests passed, including 4 validation-ledger Play tests.
- `git diff --check -- term-control-center/shared/validationLedgerPlay.ts term-control-center/tests/validationLedgerPlay.test.ts` — passed.

Checkpoint 4 validation revision 2 after verifier findings VL-010, VL-011, VL-012:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedgerPlay.test.ts` — passed; command ran the suite and 215 tests passed, including 5 validation-ledger Play tests.
- `git diff --check -- term-control-center/shared/validationLedgerPlay.ts term-control-center/tests/validationLedgerPlay.test.ts` — passed.

Checkpoint 4 validation revision 3 after verifier re-opened VL-010 and VL-011:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedgerPlay.test.ts` — passed; command ran the suite and 215 tests passed, including 5 validation-ledger Play tests.
- `git diff --check -- term-control-center/shared/validationLedgerPlay.ts term-control-center/tests/validationLedgerPlay.test.ts` — passed.

Checkpoint 4 findings addressed:
- VL-010: Play plan now requires strict `https://github.com/<owner>/<repo>/issues/<number>` and `/pull/<number>` URLs, rejects extra path/query/fragment content, verifies issue/PR owner and repo match, and verifies launch `repository` matches the selected item source repository.
- VL-011: Play prompt redaction now covers Authorization values, cookies, token/secret/password/credential/API/private/session-like keys, session IDs, private local paths, and identity headers such as `x-auth-request-user`, `x-forwarded-user`, and `x-identity-*`.
- VL-012: prompt generation was split into smaller helpers and passes KISS function-size review.

## Checkpoint 5 implementation
Changed files updated:
- `term-control-center/shared/validationLedgerPlay.ts`
- `term-control-center/tests/validationLedgerPlay.test.ts`

Implemented:
- Browser validation access contract for `agent_browser` and `agent_mixed` Play plans.
- Fail-closed checks when browser-required ledger items lack configured PRD #39 browser access, have blocked/unavailable access, missing target URL, missing journey, missing expected visible state, or browser runtime warnings.
- Scoped browser prompt section that routes ready browser-required items through PRD #39 browser/web-access capability for only the selected ledger item.
- Browser prompt support for target URL/path, journey steps, expected visible state, safe setup notes, and evidence links.
- Regression coverage for missing/unavailable browser access and ready browser route prompts.

Checkpoint 5 validation revision 1:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedgerPlay.test.ts` — passed; command ran the suite and 217 tests passed, including 7 validation-ledger Play tests.
- `git diff --check -- term-control-center/shared/validationLedgerPlay.ts term-control-center/tests/validationLedgerPlay.test.ts` — passed.

Checkpoint 5 validation revision 2 after verifier finding VL-013:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedgerPlay.test.ts` — passed; command ran the suite and 218 tests passed, including 8 validation-ledger Play tests.
- `git diff --check -- term-control-center/shared/validationLedgerPlay.ts term-control-center/tests/validationLedgerPlay.test.ts` — passed.

Checkpoint 5 findings addressed:
- VL-013: Browser access context no longer broadens `agent_cli` Play prompts; browser routing is emitted only for `agent_browser` and `agent_mixed` ledger items, with regression coverage.

## Checkpoint 6 implementation
Changed files updated:
- `term-control-center/shared/validationLedger.ts`
- `term-control-center/tests/validationLedger.test.ts`

Implemented:
- Validation report proposal helper that links a structured report as `validation_report` evidence without mutating ledger state.
- Report recommendations require human confirmation before any status change, including `verified` recommendations.
- Report proposal audit events include timestamp, actor, target status, summary, and report path for status history review.
- Fail-closed checks for missing report path, missing summary, missing actor, disallowed recommendation target, and invalid status transition.
- Stronger dashboard/manual/report proposal redaction for Authorization, cookies, token/secret/password/credential/API/private/session-like keys, identity headers, and private local paths.

Checkpoint 6 validation revision 1:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedger.test.ts` — passed; command ran the suite and 220 tests passed, including 12 validation-ledger tests.
- `git diff --check -- term-control-center/shared/validationLedger.ts term-control-center/tests/validationLedger.test.ts` — passed.

## Checkpoint 7 implementation
Changed files updated:
- `term-control-center/shared/validationLedger.ts`
- `term-control-center/tests/validationLedger.test.ts`

Implemented:
- Ledger context preflight helper for validation-time safety checks.
- Duplicate ledger item ID detection.
- Fail-closed checks for missing PRD source, missing/invalid PR source, wrong project, wrong PRD, wrong PR, wrong repository, stale merge SHA evidence, and unavailable browser runtime for browser-required items.
- Regression coverage for the wrong-context and stale-evidence cases in one bounded preflight.

Checkpoint 7 validation revision 1:
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test -- validationLedger.test.ts` — passed; command ran the suite and 221 tests passed, including 13 validation-ledger tests.
- `git diff --check -- term-control-center/shared/validationLedger.ts term-control-center/tests/validationLedger.test.ts` — passed.

## Checkpoint 9 implementation
Changed files updated:
- `tests/unit/test_ceo_review_answers.py`

Implemented:
- Regression coverage proving CEO Review approval packages derive Project metadata from live Project field names.
- Coverage for Project 3-style fields including `PRD Review Status`, `Working Branch`, and `Worktree Path` without emitting legacy Project 2 or tracker `#862` defaults.

Checkpoint 9 validation revision 1:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed, 29 tests.
- `python3 -m py_compile src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.
- `git diff --check -- src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.

## Checkpoint 10 implementation
Changed files updated:
- `src/agentops_harness/prd_preflight.py`
- `src/agentops_harness/cli.py`
- `tests/unit/test_prd_preflight.py`

Implemented:
- Implementation preflight checks for canonical issue approved status and required `status:approved` label when explicitly required.
- Repository alignment checks between current repository and expected repository.
- Strict branch suffix check requiring the implementation branch to end in the PRD issue number when explicitly required.
- CLI flags for approved-issue, repository, issue-label, issue-status, and branch-suffix preflight inputs.
- Regression coverage for blocked and passing implementation preflight cases.

Checkpoint 10 validation revision 1:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed, 29 tests.
- `python3 -m py_compile src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.
- `git diff --check -- src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.

Checkpoint 10 validation revision 2 after verifier finding VL-014:
- `PYTHONPATH=src python3 -m pytest tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed, 29 tests.
- `python3 -m py_compile src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.
- `git diff --check -- src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed.

Checkpoint 10 findings addressed:
- VL-014: refactored `tests/unit/test_prd_preflight.py` helper to a small default `PreflightInput` builder with `dataclasses.replace`, removing the long parameter list while preserving existing pass/block coverage.

## Steward hygiene review
- Steward review returned `cleanup_recommended` for one stale generated artifact outside the PRD #47 change set: `pipeline-diagram/__pycache__/generate.cpython-312.pyc`.
- Cleanup applied: removed the stale `.pyc` file and empty `pipeline-diagram/__pycache__` directory if present.
- Post-cleanup `git status --short --branch` shows only expected PRD #47 source/test/run-artifact changes.

## Full validation run after checkpoint approvals
- `PYTHONPATH=src python3 -m pytest tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review_answers.py` — passed, 51 tests before final bug-check fixes; passed, 54 tests after final bug-check fixes and VL-018 cleanup.
- `python3 -m py_compile src/agentops_harness/validation_ledger.py src/agentops_harness/validation_ledger_closeout.py src/agentops_harness/prd_preflight.py src/agentops_harness/cli.py tests/unit/test_validation_ledger.py tests/unit/test_validation_ledger_closeout.py` — passed after final bug-check fixes and VL-018 cleanup.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run test` — passed, 221 tests before final bug-check fixes; targeted rerun after final bug-check fixes ran the suite and passed 222 tests.
- `npm --prefix term-control-center run build` — passed before and after final bug-check fixes; Vite emitted the existing non-blocking large chunk and non-module `term-config.js` bundling warnings.
- `git diff --check` — passed before and after steward cleanup/final bug-check fixes.

## Final bug-check fixes
- VL-015: closeout proposal creation now blocks duplicate ledger item IDs within a proposal batch as well as duplicates against existing items; regression coverage added.
- VL-016: blank-only checklist entries are filtered/blocked, and non-`not_applicable` ledger items require at least one meaningful checklist entry; regression coverage added in model and closeout tests.
- VL-017: Play `reportDir` private local paths now fail closed and report paths/prompts redact private path segments; regression coverage added for ready/blocked paths.
- VL-018: refactored touched Python test helpers/fixtures to stay within KISS limits by using a compact `CloseoutRequest` default builder with `dataclasses.replace` and moving the secret JSON payload into a fixture constant.

## Known notes / risks
- Checkpoint 1 intentionally does not wire CLI, storage, closeout, UI, Play, Browser QA runtime, or GitHub collection yet.
- Checkpoint 2 adds a pure proposal/create helper but does not yet add durable storage, CLI, live GitHub GraphQL collection, or PRD closeout route wiring.
- Checkpoint 3 adds the shared dashboard/manual workflow view model and rendered dashboard component, but not a server route or durable store yet.
- Checkpoint 4 prepares a dry-run Play plan and scoped prompt only; it does not start a terminal pane/session yet.
- Checkpoint 5 keeps browser validation in the Play dry-run plan; it routes configured browser-required items through the PRD #39 browser-access scope and blocks when access is missing, blocked, unsafe, or incomplete.
- `python3 -m pytest ...` without `PYTHONPATH=src` fails in this checkout because the package is not installed in the active environment; validation used the repo-local source path.
