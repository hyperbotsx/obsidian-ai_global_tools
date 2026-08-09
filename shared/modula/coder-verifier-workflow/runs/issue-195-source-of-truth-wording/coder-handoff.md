# Coder handoff — Issue #195 Project 3 source-of-truth wording cleanup

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/195
- PRD status: approved; CEO approved by human in issue comment.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-195`
- Branch: `prd/project-3-source-of-truth-wording-cleanup-195`

## Pre-edit status
- `git status --short --branch`: clean (`## prd/project-3-source-of-truth-wording-cleanup-195...origin/main`).
- Pre-existing dirty files: none.
- Research-first surfaces: none in PRD; no researcher consult required yet.
- Memory: disabled per launch context; not used.

## Scope boundaries
Allowed paths from PRD:
- Active documentation, examples, README text, operator-facing copy.
- Source constants/help strings when wording/policy display only.
- Tests/static checks for stale source-of-truth wording.
- Profile examples where they represent AgentOps Harness current defaults.
- This run artifact folder.

Forbidden:
- No historical run/evidence rewrite outside this issue run folder.
- No machine-local profile edits outside repository.
- No GitHub Project configuration/data mutation.
- No PRD approval semantics changes.
- No PR creation, branch creation, merge, deploy, agent launch, production operation, trading, or backtest.
- No hardcoded Project 3 assumptions in generic code paths; use active Project/profile-derived wording where generic.

Validation targets from PRD:
- `PYTHONPATH=src python3 -m pytest -q`
- `npm --prefix term-control-center run test`
- `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
- Manual review for changed docs/UI/help strings and no external profile/historical artifact mutation.

Stop condition
- Stop after final verifier bug-check approval or human escalation; do not create PR.

## Verifier checkpoints
1. Inventory checkpoint — stale wording inventory separates active guidance from historical evidence.
2. Copy checkpoint — active docs/examples/UI/help strings use Project 3 or profile-derived wording appropriately.
3. Guardrail checkpoint — static checks prevent regressions without failing on historical artifacts.
4. Scope checkpoint — no behavior migration, external profile mutation, Project config mutation, branch, PR, merge, deploy, or agent launch occurred.
5. KISS checkpoint — changes remain small, reviewable, and limited to wording/config hygiene.

## Current checkpoint
- Checkpoint 1 inventory approved by verifier revision 1.
- Checkpoint 2 copy cleanup implemented. Active docs/source/help strings now say Project 3 (`agentops-dev`) where AgentOps-specific and active Project/configured status where generic.
- Checkpoint 2 approved by verifier revision 2.
- Checkpoint 3 approved by verifier revision 2.
- Full validation attempted; failures are recorded below.
- Checkpoints 4/5 approved by verifier revision 2.
- Steward hygiene review completed: `clean`; no cleanup needed.
- Final bug-check revision 1 found `F195-BUG-R1-001`; bounded fix applied.
- Final verifier bug-check revision 2 approved with zero open findings.

## Changes made
### Checkpoint 1
- Created issue run folder and inventory/handoff artifacts.

### Checkpoint 2
- Updated README, architecture, skills, AI Maestro, Slack gateway, human-confirmed action, operations, context-renewal, and pipeline diagram docs away from stale Project 2/SoldierOne/#862 source-of-truth wording.
- Updated active source/help strings to use active Project/configured status wording instead of Project 2/#924 hardcoding.
- Updated Slack PRD draft text to avoid unconditional tracker fields unless the active profile requires one.
- Left the pre-existing CEO-review legacy checkout fallback behavior unchanged; final guardrail explicitly allowlists that compatibility context instead of hiding or migrating it.
- Updated focused Python and Term Control tests for revised copy.
- Fixed `F195-CP2-R1-001` by replacing fabricated AgentOps Harness PRD links for legacy design docs with non-URL legacy design references.
- Fixed `F195-CP2-R1-002` by rendering Slack draft tracker metadata from the active profile when present and generic no-tracker wording only when absent.

### Checkpoint 3
- Added `tests/unit/test_source_of_truth_wording_guardrail.py`, a lightweight static guardrail scanning active README/docs/profiles/pipeline-diagram/src/Term Control server/UI/shared surfaces for stale Project 2, projects/2, legacy product-name, and tracker #862 wording.
- Kept historical run artifacts and inert test fixtures outside the active-surface scan boundary.
- Fixed `F195-CP3-R1-001` by adding `.html`, `term-control-center/src`, `term-control-center/shared`, `term-control-center/index.html`, and `term-control-center/README.md` to the active scan.
- Fixed `F195-CP3-R1-002` by constructing stale terms in the guardrail test without literal rg matches, so the PRD validation scan remains reproducible.
- Fixed `F195-CP45-R1-001` by restoring the legacy checkout fallback behavior in `ceo_review_evonome_apply.py`.
- Fixed `F195-BUG-R1-001` by making the pre-existing legacy checkout fallback transparent as an explicit guardrail allowlist entry instead of hiding it with split string literals.

## Changed files
- `README.md`
- `docs/agentops-context-renewal.md`
- `docs/ai-maestro-readonly-integration.md`
- `docs/ai-maestro-runbook.md`
- `docs/architecture.md`
- `docs/human-confirmed-action-assistant.md`
- `docs/operations.md`
- `docs/skills.md`
- `docs/slack-operator-gateway.md`
- `pipeline-diagram/README.md`
- `src/agentops_harness/action_assistant.py`
- `src/agentops_harness/ai_maestro_bridge.py`
- `src/agentops_harness/ai_maestro_coordination.py`
- `src/agentops_harness/ai_maestro_plan.py`
- `src/agentops_harness/cli.py`
- `src/agentops_harness/cli_runtime.py`
- `src/agentops_harness/control_tower.py`
- `src/agentops_harness/control_tower_cli.py`
- `src/agentops_harness/daily_report.py`
- `src/agentops_harness/lead_dev_inbox.py`
- `src/agentops_harness/lead_dev_memory.py`
- `src/agentops_harness/review_server.py`
- `src/agentops_harness/slack_gateway.py`
- `src/agentops_harness/slack_gateway_health.py`
- `src/agentops_harness/slack_prd_drafts.py`
- `src/agentops_harness/slack_prd_github_creation.py`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `tests/unit/test_action_proposals.py`
- `tests/unit/test_ceo_review_answers.py`
- `tests/unit/test_ceo_review_evonome_apply.py`
- `tests/unit/test_lead_dev_confirmation.py`
- `tests/unit/test_slack_gateway_policy.py`
- `tests/unit/test_slack_prd_github_creation.py`
- `tests/unit/test_source_of_truth_wording_guardrail.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-195-source-of-truth-wording/*`

## Validation
- Inventory commands run:
  - `rg -n "Project 2|projects/2|#862|SoldierOne" README.md docs profiles pipeline-diagram src tests`
  - `rg -n "Project 2|projects/2|SoldierOne|#862|source of truth|source-of-truth" term-control-center src tests docs README.md profiles pipeline-diagram --glob '!**/*.log'`
- Focused Python validation after checkpoint 2:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_slack_prd_github_creation.py tests/unit/test_slack_gateway_policy.py tests/unit/test_action_assistant.py tests/unit/test_action_proposals.py tests/unit/test_lead_dev_confirmation.py tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_control_tower.py tests/unit/test_daily_report.py tests/unit/test_lead_dev_operations.py tests/unit/test_slack_gateway.py tests/unit/test_slack_gateway_health.py`
  - Result: `196 passed, 11 subtests passed in 0.98s`.
- Focused Term Control validation for touched launch prompt assertion:
  - `cd term-control-center && TMPDIR=$(mktemp -d) tsx --test --test-name-pattern "PRD review launch prompt drives CEO review engine" tests/launchPlan.test.ts`
  - Result: passed (`1` test).
- Broader Term Control launchPlan test attempt:
  - `cd term-control-center && TMPDIR=$(mktemp -d) tsx --test tests/launchPlan.test.ts`
  - Result: failed in unrelated environment/config assertions: missing expected auth/runtime exception, browser profile suffix, and hosted allowlist expectation; touched PRD review prompt test passed.
- Stale wording scan after checkpoint 2:
  - `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
  - Result: no matches (`rg` exit 1).
- Copy revision 2 focused validation:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_slack_gateway_policy.py tests/unit/test_slack_prd_github_creation.py`
  - Result: `67 passed in 0.16s`.
  - `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
  - Result: no matches (`rg` exit 1).
- Guardrail focused validation:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_source_of_truth_wording_guardrail.py`
  - Revision 1 result: `1 passed in 0.03s`.
  - Revision 2 result after active UI boundary expansion: `1 passed in 0.05s`.
  - `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
  - Result after revision 2: no matches (`rg` exit 1).
- Scope/KISS revision 2 focused validation:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_ceo_review_evonome_apply.py tests/unit/test_source_of_truth_wording_guardrail.py`
  - Result: `7 passed in 0.15s`.
  - `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
  - Result before final bug-check fix: no matches (`rg` exit 1).
  - `git diff --check`
  - Result: passed.
- Final bug-check revision 2 focused validation:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider tests/unit/test_source_of_truth_wording_guardrail.py tests/unit/test_ceo_review_evonome_apply.py`
  - Result: `7 passed in 0.15s`.
  - `rg -n "Project 2|projects/2|SoldierOne|#862" README.md docs profiles pipeline-diagram src tests`
  - Result: one explicit allowlisted legacy compatibility context: `src/agentops_harness/ceo_review_evonome_apply.py:155` (`LEGACY_REPO_CHECKOUT` fallback).
  - `git diff --check`
  - Result: passed.
- Full PRD validation attempts:
  - `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q -p no:cacheprovider`
  - Result: `1174 passed, 60 subtests passed, 7 failed`; failures are unrelated environment/state issues in activity center live Kody state, dedicated gh env expectations under harness-provided env, and AF_UNIX temp path length.
  - `npm --prefix term-control-center run test`
  - Result: failed because worktree-local `term-control-center/node_modules` lacks package `tsx`; focused PATH-resolved `tsx` test above passed.
  - `git diff --check`
  - Result: passed.
- Cleanup:
  - Removed generated `src/agentops_harness/__pycache__/` and `tests/unit/__pycache__/` after validation.

## Revision 1 verifier findings addressed
- `F195-CP3-R1-001`: expanded guardrail active-surface boundary to include `.html` and active Term Control UI/shared roots.
- `F195-BUG-R1-001`: restored transparent literal legacy fallback and added an explicit guardrail allowlist entry for that one pre-existing compatibility path; final rg evidence now reports this allowlisted context.
- `F195-CP45-R1-001`: removed the runtime fallback behavior migration and restored the legacy fallback behavior.
- `F195-CP3-R1-002`: removed literal stale terms from the guardrail test source while preserving runtime checks, and refreshed validation evidence.
- `F195-CP2-R1-001`: removed fabricated current-repo PRD URLs from legacy design docs; no stale product/repo string reintroduced.
- `F195-CP2-R1-002`: Slack draft tracker line now uses configured `tracker_issue` when present and generic no-tracker wording when absent; focused test added for tracker `#58`.

## Steward review
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-195-source-of-truth-wording/steward-response-r1.md`: clean.
- No cleanup needed; pre-existing historical log under issue #154 left untouched.

## Risks / notes
- Several docs are legacy PRD-specific designs but still active docs in this repository; cleanup updates authority wording without rewriting historical run artifacts.
- Term Control tests still contain inert legacy sample payloads outside the PRD final `rg` scope; active launch prompt copy was updated.
- Steward response recorded at `dev-plans/agentops/coder-verifier-workflow/runs/issue-195-source-of-truth-wording/steward-response-r1.md`; final verifier bug-check revision 2 approved.
- One final `rg` match remains by design: the pre-existing `LEGACY_REPO_CHECKOUT` compatibility fallback in `src/agentops_harness/ceo_review_evonome_apply.py`; it is allowlisted by the guardrail and should be a separate follow-up if behavior migration is desired.
- Final cache check found no `__pycache__` or `.pytest_cache` paths after cleanup.
- No external profile, GitHub Project data, PR, branch, merge, deploy, trading, or backtest action was run.
- Stop condition met: final verifier bug-check approved; no PR created.
