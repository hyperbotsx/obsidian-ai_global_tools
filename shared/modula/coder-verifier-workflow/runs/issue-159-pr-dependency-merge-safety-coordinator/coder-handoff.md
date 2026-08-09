# Coder Handoff

- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/159`
- PRD: `GitHub issue #159 - D7-PRD: PR Dependency and Merge Safety Coordinator`
- Branch: `prd/pr-dependency-merge-safety-coordinator-159`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-159`
- Agent label: `agent:agentops`
- Checkpoint: `Checkpoint 5 - Final integration and bug-check checkpoint`
- Worktree/branch preflight passed: `yes`

## Scope and constraints

Allowed paths for the current checkpoint:

- `src/agentops_harness/pr_coordination.py`
- `src/agentops_harness/pr_coordination_analysis.py`
- `src/agentops_harness/cli.py`
- `tests/fixtures/pr_coordination_*.json`
- `tests/unit/test_pr_coordination.py`
- `tests/unit/test_cli.py`
- `docs/pr-coordination.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/**`

Forbidden/out-of-scope paths remain GitHub mutation sinks, deployment scripts, product routes/navigation, raw transcripts, secrets, AI Global Tools skill files, branch/PR mutation, Project mutation, PR creation, merge, deployment, backtests, paper/live trading, and non-AgentOps repositories.

Pre-existing dirty files before editing: none (`git status --short --branch` showed a clean branch tracking `origin/main`).

## Verifier checkpoints

1. Contract and fixture checkpoint — status model, high-risk surface categories, fixture scenarios, and docs exist; all behavior is read-only.
2. PR/read model checkpoint — CLI can normalize PR/branch/check/review/linked-issue data from fixtures and live read adapters without mutation.
3. Overlap and staleness checkpoint — exact overlap, high-risk surface overlap, behind-main, and validation-stale detection work with deterministic evidence.
4. Merge-order and visibility checkpoint — merge-order recommendation and optional Activity Center/co-worker read-only summaries are clear and non-authoritative.
5. Final integration and bug-check checkpoint — validation passes, handoff lists touched files and known risks, Steward review runs if structure/artifacts changed, and verifier final bug-check approves.

## Research freshness consult

Mandatory PRD research consult completed before implementation. Researcher summary, accessed 2026-06-29:

- Use read-only `gh pr view --json` for PR fields such as `mergeable`, `mergeStateStatus`, `reviewDecision`, `reviews`, `latestReviews`, `statusCheckRollup`, `closingIssuesReferences`, `projectItems`, refs/OIDs, changed files, commits, and timestamps.
- Use GraphQL query fields for PullRequest readiness, status rollups, closing issues, project items, files, commits, base/head OIDs.
- Use REST/`gh api` GET fallbacks for PR details/reviews/files, commit status/check-runs, and compare data (`ahead_by`, `behind_by`, files).
- Use `gh project field-list`/`item-list` and read-only Project v2 APIs where project metadata is needed.
- Caveats: `mergeable`/merge state can be null or unknown while GitHub computes; checks/reviews are eventually consistent and must be bound to `headRefOid`; private repos/projects require read auth; coordinator must use only GET, GraphQL queries, and non-mutating `gh` commands.

## Checkpoint 1 changes

Implemented the read-only contract and fixture foundation:

- Added `src/agentops_harness/pr_coordination.py` with required status contract, read-only notice, high-risk shared-surface categories, fixture dataclasses, fixture loader, and surface detection helpers.
- Added `tests/fixtures/pr_coordination_overlap_stale.json` modeling PR #156 merged while PR #157 remains open, overlapping CLI/schema/test surfaces with stale validation.
- Added `tests/unit/test_pr_coordination.py` covering required statuses, read-only notice, high-risk category detection, fixture modeling, and same-surface overlap where filenames differ.
- Added `docs/pr-coordination.md` documenting read-only authority, #103 relationship, status contract, high-risk surfaces, operator workflow, and fixture intent.

No CLI command, live GitHub adapter, GitHub mutation, Project mutation, push/rebase/merge, Activity Center integration, or co-worker authority was introduced in checkpoint 1.

Checkpoint 1 verifier verdict: approved, revision 1, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened.

## Checkpoint 2 changes

Implemented read-only PR/read normalization and CLI rendering:

- Expanded `src/agentops_harness/pr_coordination.py` with `CoordinationReport`, live read adapters, `gh pr list`, `gh pr view --json`, and `gh api repos/{repo}/compare/{base}...{head}` readers.
- Added normalization for branch/base, ahead/behind counts, mergeability/merge state, review decision, status check rollup state, closing issue references, labels, Project item names/IDs, changed files, and update time.
- Added `agentops-harness pr-coordination --format json|markdown`, plus `--repo`, `--fixture`, and `--limit` options.
- Kept the command fail-closed/read-only: live read failures return `needs_human`-style read errors and nonzero exit, while fixtures render without network.
- Extended tests for fixture report fields, mocked live `gh` read command usage, and CLI JSON/markdown fixture rendering.
- Updated `docs/pr-coordination.md` with command examples.

No GitHub mutation commands, Project mutation, push/rebase/merge, comments, labels, Activity Center integration, or co-worker authority were introduced in checkpoint 2.

## Validation run

Checkpoint 1:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py -q` — passed (`4 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).

Checkpoint 2:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`59 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format json` — passed; live read returned repository `hyperbotsx/agentops-harness`, `0` open PRs, `0` read errors.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format markdown` — passed; rendered `# PR coordination` markdown.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).

Checkpoint 2 revision 1 verifier verdict: revision requested with finding `F159-R2-001`.

Checkpoint 2 revision 2 fix:

- Addressed `F159-R2-001` by removing unsupported current-`gh` field `closingIssuesReferences` from `GH_PR_FIELDS`, using supported `body` plus branch suffix fallback for linked PRD issue detection, and keeping optional parser support if fixture/GraphQL payloads provide `closingIssuesReferences` later.
- Added regression coverage that `GH_PR_FIELDS` excludes `closingIssuesReferences` and includes `body`.

Checkpoint 2 revision 2 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`60 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format json` — passed (`0` read errors).
- `gh pr view 158 --repo hyperbotsx/agentops-harness --json number,body,projectItems,statusCheckRollup,headRefName` — passed, proving the replacement field list subset is supported by installed `gh`.

Checkpoint 2 revision 2 verifier verdict: revision requested with finding `F159-R3-001`.

Checkpoint 2 revision 3 fix:

- Addressed `F159-R3-001` by normalizing current `gh` list-shaped `statusCheckRollup` payloads.
- Pending/queued/in-progress/expected states now produce `checks_pending`; failure/error/cancelled/timed-out/action-required states produce `blocked`; all-success/neutral/skipped states do not block.
- Added regression tests for list-shaped pending and failing status check rollups, and switched the mocked live adapter payload to the list shape.

Checkpoint 2 revision 3 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`61 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 - <<'PY' ... check_state({'statusCheckRollup':[{'state':'SUCCESS'},{'state':'PENDING'}]}) ... PY` — passed (`PENDING`).
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.

Checkpoint 2 verifier verdict after revision 4: approved, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Checkpoint 3 changes

Implemented deterministic overlap and staleness analysis:

- Added `src/agentops_harness/pr_coordination_analysis.py` for exact-file overlap, high-risk shared-surface overlap, behind-base status, dependency validation staleness, blockers, evidence, recommended action, and next actor.
- Extended PR coordination JSON with `blockers`, `overlap_evidence`, `recommended_action`, and `next_actor` while preserving read-only behavior.
- Fixture mode now analyzes merged dependency PR #156 and open PR #157 so PR #157 is flagged `needs_update_from_main`, `conflict_risk`, and `validation_stale` with exact CLI-file evidence and high-risk schema/CLI surface evidence.
- Live mode now analyzes `behind_by > 0` compare results as `needs_update_from_main` in addition to merge-state derived statuses.
- Updated tests to prove the fixture flags exact overlap, high-risk surface overlap, validation staleness, and behind-main classification.
- Updated docs to describe deterministic evidence.

No GitHub mutation commands, Project mutation, push/rebase/merge, comments, labels, Activity Center integration, or co-worker authority were introduced in checkpoint 3.

Checkpoint 3 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`62 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed; PR #157 statuses were `needs_update_from_main`, `conflict_risk`, `validation_stale` with exact-file and high-risk-surface evidence.
- File length audit: `src/agentops_harness/pr_coordination.py` is 288 lines and `src/agentops_harness/pr_coordination_analysis.py` is 114 lines; changed helpers remain under 20 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.

Checkpoint 3 revision 1 verifier verdict: revision requested with findings `F159-R5-001` and `F159-R5-002`.

Checkpoint 3 revision 2 fixes:

- Addressed `F159-R5-001` by marking behind-base PRs with validation evidence as `validation_stale` and adding a deterministic current base/main blocker when freshness cannot be proven after `behind_by > 0`.
- Addressed `F159-R5-002` by introducing `AnalysisState`, reducing analysis helper parameters to the project limit, reducing `surface_message` parameters, and splitting the live-read test runner helper so test functions remain under 20 lines.
- Added regression coverage for `behind_by > 0` plus validation evidence without a merged dependency.

Checkpoint 3 revision 2 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`63 passed, 7 subtests passed`).
- KISS audit over `src/agentops_harness/pr_coordination_analysis.py` and `tests/unit/test_pr_coordination.py` — passed; no changed helper exceeds 4 parameters or 20 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.

Checkpoint 3 verifier verdict after revision 6: approved, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Checkpoint 4 changes

Implemented deterministic merge-order and read-only visibility summary:

- Added report-level `merge_order` guidance to JSON and markdown output.
- Added deterministic sorting that keeps merge-ready/foundation-style PRs before PRs needing review/check completion, with stale/blocked/overlapping PRs behind update/revalidation guidance.
- Added per-PR merge-order lines that explain each PR's action and statuses without granting merge/approval authority.
- Treat fixture merged dependency PR #156 as already landed so PR #157 remains the open stale/overlap subject.
- Updated docs to state that merge-order lines are operator/co-worker visibility summaries only and not approval, merge authority, or verifier evidence.
- Added tests for deterministic non-authoritative merge-order guidance.

No Activity Center integration, GitHub mutation, Project mutation, push/rebase/merge, comments, labels, or co-worker command authority was introduced in checkpoint 4.

Checkpoint 4 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`64 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed; `merge_order` lists PR #156 as already landed before PR #157 update/revalidation guidance.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format markdown` — passed; markdown includes `## Merge order guidance`.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.

Checkpoint 4 verifier verdict: approved, revision 7, 0 open findings. Compact verdict only was read per workflow; full verifier report was not opened.

## Final integration validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`64 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format json` — passed; live read returned repository `hyperbotsx/agentops-harness`, `0` open PRs, `0` read errors.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format markdown` — passed; rendered markdown summary.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed; JSON includes read-only notice, merge order, validation stale, overlap evidence, recommended action, and next actor.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format markdown` — passed; rendered merge-order guidance.
- KISS audit over `src/agentops_harness/pr_coordination.py`, `src/agentops_harness/pr_coordination_analysis.py`, and `tests/unit/test_pr_coordination.py` — passed; no changed helper exceeds 4 parameters or 20 lines; files remain under 300 lines.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.

## Steward review

Steward review before final bug-check returned `cleanup_recommended`:

- Placement was clean for code, tests, fixtures, docs, and run artifacts.
- No raw transcripts/log dumps found in the run directory.
- Recommended cleanup was ignored cache removal: `.pytest_cache`, `src/agentops_harness/__pycache__`, and `tests/unit/__pycache__`.

Cleanup completed:

- `rm -rf .pytest_cache src/agentops_harness/__pycache__ tests/unit/__pycache__` — completed.

Final validation after Steward cleanup:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`64 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format json` — passed; live read returned repository `hyperbotsx/agentops-harness`, `0` open PRs, `0` read errors.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --format markdown` — passed.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed; first merge-order line was `PR #156: merged dependency already landed (merge_ready)`.
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format markdown` — passed.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.
- Ignored cache cleanup was rerun after validation.

Final bug-check revision 1 verifier verdict: revision requested with finding `F159-R8-001`.

Final bug-check revision 2 fix:

- Addressed `F159-R8-001` by preferring the PR branch suffix issue before fallback body issue parsing, avoiding dependency references such as `#103` being mistaken for the canonical PRD issue when the branch ends in `-159`.
- Added regression coverage for a body that mentions dependencies before `#159` and expects `linked_prd_issue == 159`.

Final bug-check revision 2 validation:

- `PYTHONPATH=src python3 -m pytest tests/unit/test_pr_coordination.py tests/unit/test_cli.py -q` — passed (`65 passed, 7 subtests passed`).
- `PYTHONPATH=src python3 - <<'PY' ... linked_issue({'headRefName':'prd/pr-dependency-merge-safety-coordinator-159','body':'Depends on #103 and #154. Implements #159.'}) ... PY` — passed (`159`).
- `PYTHONPATH=src python3 -m agentops_harness.cli pr-coordination --fixture tests/fixtures/pr_coordination_overlap_stale.json --format json` — passed.
- `PYTHONPATH=src python3 -m agentops_harness.cli handoff-metadata-check --artifact dev-plans/agentops/coder-verifier-workflow/runs/issue-159-pr-dependency-merge-safety-coordinator/coder-handoff.md --format json` — passed (`status: passed`).
- `git diff --check` — passed.
- Ignored cache cleanup was rerun after validation.

Final bug-check revision 2 verifier verdict: approved, revision 10, 0 open findings, bug-check passed. Compact verdict only was read per workflow; full verifier report was not opened after approval.

## Known risks / next work

- No known blocking risks remain.
- Human-managed next steps only: review, commit/PR creation if desired. No PR was created by coder.
