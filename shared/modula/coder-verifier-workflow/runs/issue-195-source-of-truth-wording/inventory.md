# Issue #195 stale wording inventory

## Source
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/195
- Inventory command: `rg -n "Project 2|projects/2|#862|SoldierOne|source[- ]of[- ]truth|source of truth|canonical PRD|Project 3|agentops-dev|tracker" README.md docs profiles pipeline-diagram src tests term-control-center`

## Active AgentOps Harness guidance needing copy cleanup
- `README.md`: Source-of-truth section still says GitHub Project 2; examples still use tracker #862.
- `docs/architecture.md`: authority model still says GitHub Project 2.
- `docs/skills.md`: compatibility-wrapper source-of-truth sentence still says Project 2.
- `docs/ai-maestro-readonly-integration.md`: Project 2 source-of-truth, bridge, and memory wording.
- `docs/ai-maestro-runbook.md`: Project 2 source-of-truth wording.
- `docs/human-confirmed-action-assistant.md`: legacy SoldierOne PRD link, Project 2 source-of-truth / metadata, and sample command.
- `docs/slack-operator-gateway.md`: legacy SoldierOne PRD link, Project 2 source-of-truth / rollback wording, and sample command.
- `pipeline-diagram/README.md`: active board/operator documentation still describes Project 2, tracker #862, and seven tracker issues as the single source of truth.

## Active source/help/policy strings needing wording cleanup
- `src/agentops_harness/ai_maestro_bridge.py`: bridge source-of-truth string says Project 2 via #924.
- `src/agentops_harness/ai_maestro_plan.py`: gate text says duplicate Project 2 logic.
- `src/agentops_harness/daily_report.py`: status-source label says GitHub Project 2.
- `src/agentops_harness/slack_gateway.py`: status source says GitHub Project 2 via #924.
- `src/agentops_harness/slack_prd_github_creation.py`: rollback and partial-failure copy says Project 2.
- `src/agentops_harness/action_assistant.py`: action labels say Project 2 metadata.
- `src/agentops_harness/control_tower_cli.py`: markdown headings / health labels say Project 2.
- `src/agentops_harness/control_tower.py`: limit warning says Project 2 items.
- `src/agentops_harness/lead_dev_memory.py`: authority caveat says Project 2.
- `src/agentops_harness/lead_dev_inbox.py`: source string says Project 2.
- `src/agentops_harness/ai_maestro_coordination.py`: forbidden-action copy says Project 2 mutation.
- `src/agentops_harness/review_server.py`: degraded GraphQL fallback copy says live Project 2 field data.

## Likely tests to update with active copy changes
- `tests/unit/test_slack_prd_github_creation.py`
- `tests/unit/test_slack_gateway_policy.py`
- `tests/unit/test_action_assistant.py`
- `tests/unit/test_action_assistant_cli.py`
- `tests/unit/test_control_tower.py` / control tower view tests if asserting headings.
- `tests/unit/test_daily_report.py`, `tests/unit/test_lead_dev_operations.py`, or other focused tests if source labels/caveats are asserted.
- `term-control-center/tests/launchPlan.test.ts` if launch prompt guard wording changes.

## Context to leave alone or allowlist
- `dev-plans/agentops/coder-verifier-workflow/runs/**`: historical run/evidence artifacts; read-only except this issue's run folder.
- `tests/fixtures/trajectory/**`: fixture artifacts used to test trajectory evaluation, not active guidance.
- Existing test fixtures using `SoldierOne`, Project 2, or #862 as inert sample data may remain if not asserting active AgentOps Harness source-of-truth guidance.
- `src/agentops_harness/cli_runtime.py` has a historical provenance comment; not operator-facing source-of-truth guidance.
- `src/agentops_harness/ceo_review_evonome_apply.py` has `LEGACY_REPO_CHECKOUT`; not part of Project source-of-truth wording unless verifier requests follow-up.
- Term Control tests using `SoldierOne`/Project 2 as generic sample payloads can remain if active launch prompts continue warning against hardcoding them.

## Guardrail direction
Add a lightweight repo test that scans active docs/source surfaces for stale Project 2 / `projects/2` / tracker #862 / `SoldierOne` wording, with explicit allowlists for historical evidence, fixtures, test sample data, and legacy compatibility identifiers. The guardrail should fail on active operator guidance but not rewrite history.
