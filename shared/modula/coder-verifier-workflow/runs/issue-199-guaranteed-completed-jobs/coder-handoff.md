# Coder handoff — Issue #199 Guaranteed Completed Jobs Rows After Main Merge

## Source of truth
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/199
- Branch: `prd/guaranteed-completed-jobs-after-merge-199`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-199`
- Status: final verifier bug-check approved

## Pre-edit state
- `git status --short --branch`: clean branch at `prd/guaranteed-completed-jobs-after-merge-199...origin/main`
- Pre-existing dirty files: none
- Memory disabled warning acknowledged; repository/PRD/verifier evidence win.

## Allowed / forbidden scope
- Allowed: `pipeline-diagram/completed_work.py`, `pipeline-diagram/generate.py`, `pipeline-diagram/completed.html`, focused tests/docs/run artifacts for completed-work reconciliation.
- Forbidden: PR creation, merge, deploy, PRD approval, validation signoff, GitHub Project mutation, secrets/raw transcripts/tokens/env dumps, hardcoded one-off PR/project/local paths.
- Stop condition: final verifier bug-check approval after implementation, steward review if structure/artifact placement changes.

## Research consult
- Researcher consulted 2026-07-13 for GitHub PR/linking/Projects v2 freshness.
- Key implications: use merged PR evidence as durable source; Projects v2 is advisory; degrade rather than omit on missing/stale Project metadata, missing linked issue metadata, branch deletion, rate/timeouts/partial API failures; parse closing keywords and use branch fallback when API linked-issue metadata is unavailable.
- Researcher consulted again after repeated `F199-C3-001` redaction misses; applied bounded key-assignment/header/GitHub-token regex approach for refresh-error text.

## Checkpoints
1. Evidence model and registry/reconciliation design.
2. GitHub merged-PR reconciliation and degraded evidence behavior.
3. Completed Jobs generation/rendering.
4. Completion lifecycle integration and idempotency.
5. Validation-state compatibility and duplicate prevention.
6. Final bug-check for silent omissions, stale evidence, duplicate rows, and unsafe persistence.

## Checkpoint 1 design
- Add a completed-work reconciliation layer in `pipeline-diagram/completed_work.py` that combines existing PRD issue/Project rows with recently merged PR evidence from GitHub.
- Merged PR evidence source: `gh pr list --state merged --base main --limit 200 --json number,url,title,body,state,mergedAt,mergeCommit,headRefName,baseRefName` via a `recent_merged_prs` context hook. The explicit 200-row window is a one-refresh-cycle backfill window and avoids relying on gh defaults; tests can inject a smaller fixture list. Use PR body closing keywords and PRD branch/issue-number fallback; retain existing issue timeline linkage for issue-sourced rows.
- Canonical registry key/schema: `repo:<owner/repo>|prd:<issue-number-or-unlinked>|pr:<pr-number>|merge:<merge-sha-or-fingerprint>|branch:<headRefName-or-unknown>|evidence:<source-fingerprint>`. This satisfies the PRD fields: repository, PR number, PRD issue number or explicit unlinked sentinel, merge commit SHA or fallback fingerprint, branch, and source evidence fingerprint.
- Validation-state compatibility: keep the current `validationKey` shape for linked PRD rows (`prd:<issue>|pr:<pr>|merge:<sha-or-fingerprint>`) so existing signed-off records still match. Diagnostics-only changes must not change `validationKey`; only PR/merge evidence changes should. Unlinked warning rows use a separate non-PRD key prefix such as `unlinked-pr:<repo>|pr:<pr>|merge:<sha-or-fingerprint>` and disable/avoid human validation semantics in rendering so they cannot masquerade as completed PRD signoff rows.
- Row identity/deduplication: collapse duplicate sources by the canonical registry key first, then by linked validation tuple for normal rows. Prefer rows with merge commit, PRD linkage, and fewer missing-evidence reasons.
- Evidence fields: keep existing `evidenceFingerprint` and `validationKey`; add safe diagnostics such as `registryKey`, `evidenceStatus`, `missingEvidence`, and `suggestedAction` without secrets or raw transcripts.
- Degraded behavior: if PR merged but Project/issue closeout/merge commit/linkage evidence is missing or stale, emit a row with actionable source notes instead of silently omitting. Missing PRD linkage creates an unlinked merged-PR warning row keyed to the PR rather than pretending validation is complete.
- Durable registry paths: write sanitized generated JSON to `pipeline-diagram/completed-registry.json` and `pipeline-diagram/projects/<project_id>/completed-registry.json` using atomic temp-file replace. Add `completed-registry.json` to `pipeline-diagram/.gitignore`; `projects/` is already ignored. The registry is generated runtime state, not source.
- Sanitized registry fields: only row fields already safe for Completed Jobs display plus diagnostics (`issueNumber`, `title`, URLs, PR number/state/url, merge status/SHA/time, branch, worktree, owner, source state/notes, evidence status, missing evidence, suggested action, fingerprint, validation key, registry key). Never persist secrets, raw transcripts, attach tokens, cookies, raw env dumps, or full API responses.
- Fail-closed refresh control flow: remove the top-level `completed = []` fallback in `generate.py`. If completed refresh raises, load prior registry rows through a `completed_registry_rows()` hook and mark them degraded with a refresh-failure source note before writing `completed-data.js`; if no registry exists, write a single safe degraded refresh-failure row only when PR evidence is unavailable rather than silently emptying prior known rows.
- Backfill/idempotency: merge current rows with prior registry rows on every successful refresh, preserving older merged rows outside the current 200-PR window while replacing matching registry keys with fresher current evidence.
- Rendering: `completed.html` can continue to render existing columns; evidence cell should explicitly surface `missingEvidence` and `suggestedAction`, and unlinked rows should show a warning instead of validation-ready actions.
- Tests: extend `tests/unit/test_completed_work.py` for normal body keyword, stale Project/open issue degraded row, duplicate collapse, missing-link warning row, registry fallback, validation-key stability, and the current `completed = []` refresh-failure regression.

## Design revision findings addressed
- `F199-DESIGN-001`: canonical registry key now includes repo, PRD/unlinked sentinel, PR, merge, branch, and fingerprint; validationKey compatibility and unlinked semantics are explicit.
- `F199-DESIGN-002`: fail-closed `generate.py` control flow, registry fallback, explicit `--limit 200` merged-PR backfill window, and regression test target are specified.
- `F199-DESIGN-003`: registry paths, generated/ignored status, atomic writes, and sanitized field allowlist are specified.

## Checkpoint 2 implementation
- Added merged-PR reconciliation to `pipeline-diagram/completed_work.py` using a `recent_merged_prs` context hook or `gh pr list --state merged --base main --limit 200`.
- Added PRD linkage detection from PR body closing keywords, optional `closingIssuesReferences` payloads when injected/available, and branch fallback for PRD-style or known working branches.
- Added degraded evidence diagnostics (`evidenceStatus`, `missingEvidence`, `suggestedAction`, `registryKey`) and unlinked merged-PR warning rows with `validationDisabled`.
- Added `pipeline-diagram/completed_registry.py` for row dedupe/registry key helpers and `pipeline-diagram/completed_links.py` for linkage parsing so `completed_work.py` stays under 300 lines.
- Extended `tests/unit/test_completed_work.py` for body keyword reconciliation, duplicate collapse, unlinked warning rows, and merged-PR refresh failure degradation.
- Revision fixes for verifier findings:
  - `F199-C2-001`: shadowed issue-only `pr:none` rows are pruned when a linked recent merged-PR row exists for the same PRD.
  - `F199-C2-002`: recent merged-PR API failures no longer make `fetch_completed()` raise; existing rows are marked degraded with a refresh-failure note.
  - `KISS-199-C2-001`: new/changed helper signatures now stay within the <=4 parameter budget; `completed_work.py` is 290 lines.
  - `KISS-199-C2-002`: test helper now accepts a compact options dict and delegates fake gh/recent behavior to small helpers.

## Checkpoint 3 implementation
- Added generated completed-work registry persistence in `pipeline-diagram/generate.py` to root and active project output using sanitized row fields and atomic replace.
- Added completed refresh fallback: fetch errors load prior registry rows as degraded, or emit a safe `refresh-failed` row if no registry exists.
- Added `pipeline-diagram/.gitignore` entry for generated `/completed-registry.json`; `projects/` remains ignored.
- Updated `pipeline-diagram/completed.html` so evidence cells show missing evidence and suggested actions, and `validationDisabled` warning rows show repair guidance instead of validation action buttons.
- Added `tests/unit/test_completed_generate.py` for registry write/sanitization and degraded refresh fallback.
- Added `tests/unit/test_completed_html_static.py` to pin static rendering references for `mergeCommitSha`, missing evidence, suggested action, and disabled validation warnings.
- Revision fixes for verifier findings:
  - `F199-C3-001`: Completed row emission, registry writes, stale registry fallback, and refresh-failure notes now strip/redact nested PR bodies, closing references, attach tokens, cookies, common env-token assignments (quoted, colon, equals), GitHub token prefixes, token-like text, and unknown nested PR fields.
  - `F199-C3-002`: recent merged-PR refresh failures degrade prior registry rows before merge, so stale registry evidence cannot look fresh.
  - `F199-C3-003`: Completed Jobs now renders a short merge commit SHA in the Merge column when available.

## Checkpoint 4/5 implementation notes
- Completion lifecycle integration: existing board/completion refresh path (`refresh_board_async()` -> `pipeline-diagram/generate.py`) now regenerates `completed-data.js` and `completed-registry.json` in the same refresh cycle, so post-merge sync/closeout-triggered refreshes pick up merged PR reconciliation without adding a new action or mutating GitHub.
- Backfill path: `generate.py` calls `fetch_completed()` which includes `gh pr list --state merged --base main --limit 200`, merges prior registry rows, and writes the refreshed registry idempotently.
- Idempotency: `completed_registry.dedupe_rows()` collapses shadowed issue-only rows when linked PR rows exist, prunes stale unlinked warning rows when the same PR/merge becomes linked, and `merge_registry_rows()` replaces matching registry keys instead of appending duplicates.
- Validation-state compatibility: linked PRD rows keep the existing `validationKey` tuple (`prd:<issue>|pr:<pr>|merge:<sha-or-fingerprint>`). Unlinked warning rows use `unlinked-pr:<repo>|pr:<pr>|merge:<sha-or-fingerprint>` plus `validationDisabled` so they cannot masquerade as PRD validation signoff rows.
- Distinct surfaces preserved: Completion Center flow was not repurposed; Completed Jobs remains generated evidence, and validation rows remain local/human-confirmed.

## Steward review
- Steward pre-final hygiene returned `cleanup_recommended` only for ignored caches.
- Cleanup completed: removed `.pytest_cache/`, `pipeline-diagram/__pycache__/`, `tests/unit/__pycache__/`.
- Steward said no recheck needed unless changed-file set/generated artifacts change.

## Final bug-check fixes
- `F199-FBC-001`: unlinked registry rows are now pruned by PR number when a current linked PRD row exists, covering missing merge-SHA/fingerprint mismatch cases.
- `F199-FBC-002`: registry sanitization now iterates only dict rows, ignoring malformed scalar registry entries instead of crashing fallback.
- `F199-FBC-003`: refresh-error redaction now covers prefixed/suffixed token names, API key names, secret names, and password-style env assignments.
- `F199-FBC-004`: stale registry text fields are now redacted during sanitization before fallback rows, JS output, or registry persistence.

## Validation log
- `python3 -m pytest tests/unit/test_completed_work.py tests/unit/test_completed_generate.py tests/unit/test_completed_html_static.py tests/unit/test_pipeline_generate.py -q` — passed (34 tests)
- `python3 -m pytest tests -q` — failed during collection because `agentops_harness` was not on `PYTHONPATH` in this shell.
- `PYTHONPATH=src python3 -m pytest tests -q` — passed (1202 tests, 60 subtests)
- `python3 -m py_compile pipeline-diagram/generate.py pipeline-diagram/completed_work.py pipeline-diagram/completed_registry.py pipeline-diagram/completed_links.py tests/unit/test_completed_work.py tests/unit/test_completed_generate.py tests/unit/test_completed_html_static.py tests/unit/test_pipeline_generate.py` — passed
- `git diff --check` — passed
- AST KISS check for `pipeline-diagram/completed_work.py`, `pipeline-diagram/completed_registry.py`, `pipeline-diagram/completed_links.py`, `tests/unit/test_completed_work.py`, `tests/unit/test_completed_generate.py`, `tests/unit/test_completed_html_static.py` — no functions with >4 parameters or >20 lines

## Changed files
- `pipeline-diagram/completed.html`
- `pipeline-diagram/completed_work.py`
- `pipeline-diagram/completed_registry.py`
- `pipeline-diagram/completed_links.py`
- `pipeline-diagram/generate.py`
- `pipeline-diagram/.gitignore`
- `tests/unit/test_completed_work.py`
- `tests/unit/test_completed_generate.py`
- `tests/unit/test_completed_html_static.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-199-guaranteed-completed-jobs/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-199-guaranteed-completed-jobs/review-request-r1-checkpoint-1-design.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-199-guaranteed-completed-jobs/review-request-r2-checkpoint-1-design-fix.json`
