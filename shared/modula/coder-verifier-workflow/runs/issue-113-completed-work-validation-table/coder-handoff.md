# Coder Handoff — Issue #113 Completed-Work Validation Table

## Scope
Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/113
Branch: `prd/c2-prd-completed-work-validation-table-113`
Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-113`

## Pre-existing dirty files
None. `git status --short --branch` was clean before edits.

## Allowed / forbidden paths
Allowed: `pipeline-diagram/`, `term-control-center/server/`, `term-control-center/src/navigation/`, `term-control-center/tests/`, run artifacts under this folder.
Forbidden: product routes outside AgentOps UI, deployment mutation, PR creation, merge, deploy, secrets, raw transcripts.

## Checkpoints
1. Completed-work source aggregation + static page/navigation/deploy wiring.
2. Local validation state persistence/keying and needs-recheck behavior.
3. Browser-QA per-row wiring through existing `/term/groups/:id/browser-qa` guard path.
4. Steward structure check before final verifier bug-check because static assets/run artifacts changed.

## Research freshness consult
2026-06-29 researcher guidance: use authenticated `gh api graphql`/`gh` for Project v2, issues, PR fields; trust issue `state`, `closed_at`, labels; PR `mergedAt`, `mergeCommit`; do not fabricate Done state, linked PRs, merge SHAs, or Project membership when fields are absent, inaccessible, or ambiguous. Implemented generator emits `unknown`/source notes for missing PR/merge evidence.

## Implementation notes
- Added `pipeline-diagram/completed.html` with client-side filtering, queue filters, local validation mark-off, same-PRD historical needs-recheck detection, and Browser-QA launch buttons.
- Added generated `completed-data.js` support via extracted `pipeline-diagram/completed_work.py`; source notes fail closed for missing implementation PRs, unavailable merge commits, and Project/issue conflicts.
- Added Term Control Center `validation-state.json` store and `/completed-validation-state` GET/PUT routes for local persisted validation records.
- Added `/completed-work/browser-qa` to launch a Browser-QA-only bounded session from safe row branch/worktree evidence when no matching implementation group exists; existing groups still reuse `/groups/:id/browser-qa`.
- Added completed page to shared nav and deploy/smoke asset lists; added public symlinks.

## Revision 2 fixes
- Addressed F113-R1-001: historical same-PRD signed-off records with changed key/fingerprint now surface as `needs-recheck`.
- Addressed F113-R1-002 partially: row Browser-QA can launch a bounded Browser-QA-only session from row evidence when no live implementation group exists, while still failing closed if branch/worktree evidence is missing.
- Addressed F113-R1-003: completed-work aggregation moved out of `generate.py` into focused `completed_work.py`; added Python behavioral tests.

## Revision 3 fixes
- Addressed remaining F113-R1-002 partially: Browser-QA launch now records `pending-browser-qa-report` advisory proposal state/rationale instead of treating a Term group as evidence.
- Addressed F113-R2-001: completed-work Browser-QA launch calls `startLaunchGroup(..., { skipFreshness: true })` so it does not run implementation worktree sync/push before evidence-only QA.
- Addressed F113-R2-002: validation records no longer persist Term group URLs with attach tokens; store sanitization strips any `attachToken` evidence link.

## Revision 4 fixes
- Added `/completed-work/browser-qa-report` report discovery route that scans safe row worktree evidence for `browser-qa-report*.md` artifacts.
- Added row-visible `Refresh QA report` and automatic pending-report polling; when a report is found, the row stores a sanitized relative report path plus advisory `pass`/`fail`/`inconclusive` proposal rationale.
- Added `completedBrowserQaReport` tests for pass/fail/pending discovery.

## Revision 5 fixes
- Addressed F113-R4-001: `/completed-work/browser-qa` now requires the row's own `worktree` evidence and no longer falls back to the Term server worktree.
- Added `completedBrowserQa` tests for missing-worktree fail-closed behavior and Browser-QA-only launch construction.

## Final bug-check fixes
- Addressed F113-FBC-001: report evidence now opens through a token-guarded `/completed-work/browser-qa-report-file` route via transient `termFetch`, not as an unserved static relative link.
- Addressed F113-FBC-002: Browser-QA launch records `launchedAt`; report discovery ignores reports older than that launch baseline to avoid stale prior-run evidence.

## Validation log
- PASS: `npm --prefix term-control-center ci` (installed local dependencies required by existing typecheck/test scripts).
- PASS: `npm --prefix term-control-center run typecheck`.
- PASS: `cd term-control-center && node --import tsx --test tests/completedValidationStore.test.ts tests/completedStatic.test.ts tests/completedBrowserQa.test.ts tests/completedBrowserQaReport.test.ts tests/launchProjectFallback.test.ts` (17 tests after final bug-check fixes).
- PASS: `python3 -m py_compile pipeline-diagram/generate.py pipeline-diagram/completed_work.py pipeline-diagram/deploy/sync-public-assets.py pipeline-diagram/deploy/asset-smoke-check.py`.
- PASS: `python3 tests/unit/test_completed_work.py`.
- PASS after generated data refresh: `python3 pipeline-diagram/deploy/sync-public-assets.py --root pipeline-diagram --check`.
- PASS earlier: `cd pipeline-diagram && python3 generate.py` produced completed-data.js with 51 completed rows (ignored generated output).
- BLOCKED on rerun by GitHub API rate limit: `cd pipeline-diagram && python3 generate.py` now fails at `gh issue list` with `GraphQL: API rate limit already exceeded`; generated local data from the earlier pass remains present for asset checks.
- PASS: `npm --prefix term-control-center run build`.
- PARTIAL/ENV: `npm --prefix term-control-center run test` progressed through broad suite but timed out at 300s; failures were pre-existing/environment-sensitive launch/runtime expectations (review runtime auth, browser profile path, server launch fixture assumptions) outside this scope. Targeted new tests passed.

## Steward review
- Steward returned `cleanup_recommended` before final bug-check.
- Coder removed `pipeline-diagram/__pycache__` and `pipeline-diagram/deploy/__pycache__`.
- Steward response saved at `dev-plans/agentops/coder-verifier-workflow/runs/issue-113-completed-work-validation-table/steward-response-r1.md`.

## Final verifier status
- Final bug-check approved at revision 7.
- Verifier verdict: `approved`, `bug_check_status: passed`, open findings: 0.
- Report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-113-completed-work-validation-table/verifier-report.md`.

## Post-PR origin/main refresh
- After PR #157 opened, `origin/main` advanced with PR #156 (closed-loop runner foundation).
- Coder fetched and merged latest `origin/main` into this branch with no conflicts.
- Validation after refresh:
  - PASS: `npm --prefix term-control-center run typecheck`
  - PASS: `cd term-control-center && node --import tsx --test tests/completedValidationStore.test.ts tests/completedStatic.test.ts tests/completedBrowserQa.test.ts tests/completedBrowserQaReport.test.ts tests/launchProjectFallback.test.ts` (17 tests)
  - PASS: `python3 tests/unit/test_completed_work.py`
  - PASS: `npm --prefix term-control-center run build`
  - PASS: `python3 pipeline-diagram/deploy/sync-public-assets.py --root pipeline-diagram --check`
  - PASS: `git diff --check`
  - PASS: `cd pipeline-diagram && python3 generate.py` (8 open PRDs, 0 in progress, 54 completed)

## Open questions / risks
- Final merge readiness now depends on post-refresh verifier bug-check approval and PR checks.

## Post-refresh R8 bug-check fixes
- Addressed F113-R8-001: `/completed-work/browser-qa` and `/groups/:id/browser-qa` now return server-issued `launchedAt`; the UI persists that value instead of browser client time for report freshness checks.
- Addressed F113-R8-002: Browser-QA reports containing `major` findings now produce advisory `fail`; tests cover blocking/major/minor/note classifications.
- Validation after fixes:
  - PASS: `npm --prefix term-control-center run typecheck`
  - PASS: `cd term-control-center && node --import tsx --test tests/completedValidationStore.test.ts tests/completedStatic.test.ts tests/completedBrowserQa.test.ts tests/completedBrowserQaReport.test.ts tests/launchProjectFallback.test.ts` (18 tests)
  - PASS: `python3 tests/unit/test_completed_work.py`
  - PASS: `npm --prefix term-control-center run build`
  - PASS: `python3 pipeline-diagram/deploy/sync-public-assets.py --root pipeline-diagram --check`
  - PASS: `git diff --check`

## Post-refresh verifier recheck
- Verifier approved post-origin/main refresh bug-check at revision 9.
- Verdict: `approved`, `bug_check_status: passed`, open findings: 0.
