# Agent Engineering Standards Pack v1

Agent Engineering Standards Pack v1 is the shared standards source for AgentOps-launched researchers, coders, verifiers, and stewards.

## Source of truth

The canonical source is this folder:

`/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1/`

Repository docs, prompt templates, role skills, and launch notes may reference this folder, but they must not copy or fork the full standards.

## Quick start

- Researchers: read `researcher-instructions.md` before answering stack-specific structure, boilerplate, testing, migration, state, or design-system questions.
- Coders: read `coder-rules.md` before creating or restructuring code.
- Verifiers: use `verifier-checklist.md` during checkpoint and final review.
- Stewards: use `steward-checklist.md` before final bug-check when file placement, artifacts, generated output, or source-of-truth layout changed.
- Everyone: use `exception-policy.md` before accepting deviations.

## File map

- `manifest.json` — version, inventory, ownership, consumers, and update metadata.
- `canonical-standards.md` — full human-readable standards.
- `researcher-instructions.md` — Exa research workflow and fail-closed rules.
- `coder-rules.md` — concise implementation rules.
- `verifier-checklist.md` — review checklist.
- `steward-checklist.md` — structure and hygiene checklist.
- `exception-policy.md` — bounded exception process.
- `integration-guide.md` — future AgentOps session loading plan.
- `update-process.md` — versioning and review process.
- `validation-checklist.md` — completeness and readiness checks.

## Non-authority

This pack does not approve PRDs, PRs, merges, deployments, production rollout, hard-blocking enforcement, trading, paper trading, live trading, or backtests. Human gates still apply.
