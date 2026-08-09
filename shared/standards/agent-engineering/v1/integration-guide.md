# Integration Guide

## Canonical loading paths

- Standards pack: `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1/`
- Shared skill: `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/skills/agent-engineering-standards/SKILL.md`
- Optional Pi wrapper: `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/agent-engineering-standards/SKILL.md`

## Future AgentOps sessions

- Researchers load `researcher-instructions.md` before stack-specific recommendations.
- Coders load `coder-rules.md` before implementation or restructuring.
- Verifiers load `verifier-checklist.md` during checkpoint and final review.
- Stewards load `steward-checklist.md` before final bug-check when structure, artifacts, generated files, prompts, or skills changed.
- PRD authors may reference `canonical-standards.md` when writing implementation hygiene requirements.

## Automatic, opt-in, and human-gated behavior

Automatic:

- Agents may reference this pack in handoffs, checklists, and launch context.
- Agents may use the shared skill entrypoint to find the canonical pack.

Opt-in:

- Repositories may add docs, examples, loaders, prompt references, or tests that point to the canonical pack.
- Projects may add drift checks after a separate approved PRD.

Human-gated:

- Making the pack binding for a project.
- Enabling hard-blocking enforcement.
- Changing PRD approval, PR approval, merge, deployment, production, trading, or backtest gates.
- Creating divergent project-only skills.

## Reference pattern

Repo-local references should name the pack, version, canonical path, and skill entrypoint. They should not copy the full standards. If a local copy is unavoidable, it must be generated from the canonical source with drift detection and human approval.
