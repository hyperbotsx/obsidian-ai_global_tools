---
name: agent-engineering-standards
description: Load the Agent Engineering Standards Pack v1 for minimalist architecture, KISS implementation rules, mandatory Exa research before stack-specific structure, verifier/steward checklists, and exception handling.
---

# Agent Engineering Standards

Use this skill before creating or restructuring software, choosing stack-specific layouts, reviewing architecture, or checking file placement hygiene.

Canonical pack:
`/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1/`

## Load by role

- Researcher: read `researcher-instructions.md`.
- Coder: read `coder-rules.md`, then consult `canonical-standards.md` for details.
- Verifier: read `verifier-checklist.md`.
- Steward: read `steward-checklist.md`.
- Any role handling deviations: read `exception-policy.md`.

## Hard rules

- Do not duplicate the full standards into repo-local skills or prompt templates.
- Use Exa or Researcher before stack-specific directory structures, boilerplate, migration layout, test layout, state patterns, design-system layout, external APIs, SDKs, auth, rate limits, or deprecations.
- If Exa evidence is unavailable, stale, undated for volatile surfaces, or conflicting, fail closed and ask the human or Researcher.
- This skill does not authorize PR approval, PR creation, merge, deployment, hard-blocking enforcement, production rollout, trading, or backtesting.
