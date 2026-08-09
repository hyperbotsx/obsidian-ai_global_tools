# Coder Rules

Load these rules before creating or restructuring code.

1. Implement the smallest correct change for the approved scope.
2. Research first with Exa or Researcher before stack-specific layouts, boilerplate, test/migration layouts, state patterns, design-system structure, external APIs, SDKs, auth, rate limits, or deprecations.
3. Keep transport, business logic, data access, and side effects separated.
4. Keep frontend rendering, data fetching, business rules, and effects easy to identify.
5. Keep state local by default; promote it only with named ownership and mutation rules.
6. Use centralized, semantic design tokens for reusable styling decisions.
7. Prefer flat semantic directories; do not create dumping grounds or speculative layers.
8. Make errors, retries, timeouts, idempotency, and observability explicit at boundaries.
9. Validate configuration at boot and fail closed when required values are missing.
10. Write deterministic tests at the lowest useful layer and document validation commands in the handoff.
11. Isolate time, randomness, network, filesystem, environment, and database access.
12. Never store secrets, raw prompts, raw transcripts, credentials, or private account data in code, artifacts, logs, UI state, or tests.
13. Document exceptions with constraint, scope, risk, mitigation, owner, review date, and human approval when required.
14. Do not create PRs, merge, deploy, roll out hard-blocking enforcement, trade, backtest, or bypass human gates.

If a rule conflicts with a project PRD, stop and ask for clarification unless the PRD explicitly approves a bounded exception.
