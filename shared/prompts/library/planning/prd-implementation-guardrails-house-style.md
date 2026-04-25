# PRD implementation guardrails — house style snippet

Use this snippet selectively during PRD review when the implementation is likely to touch shared UI, internal naming, CSS/layout patterns, or canonical contracts.

## Implementation Guardrails
- Use institutional / neutral internal naming in code.
- Extend shared components before creating forks.
- Prefer shared design tokens and existing UI primitives over one-off styling.
- Keep one canonical contract per concept; do not create parallel models.
- Follow KISS: small focused functions and components, low nesting, precise names.

## When to inject this into a PRD
Inject this section when the PRD is implementation-heavy and likely to cause:
- naming drift
- duplicated components
- ad hoc CSS/layout work
- parallel schemas or contracts

Do not inject it into every PRD by default. Skip it for research-only, prioritization-only, or governance-only artifacts unless implementation drift is still a real risk.
