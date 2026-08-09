# Verifier Checklist

Use this checklist during checkpoint review and final bug-check.

## Scope and source of truth

- The change matches the approved PRD and no forbidden action occurred.
- Reusable standards or skills live in AI Global Tools, not as divergent repo-local copies.
- Stack-specific choices cite fresh Exa or Researcher evidence when required.

## Architecture

- Transport, business logic, data access, side effects, and observability have explicit boundaries.
- Frontend rendering, effects, data fetching, and business rules are separable.
- APIs define request, response, errors, compatibility, pagination/streaming, retries, timeouts, and idempotency where applicable.
- Background jobs define retry, timeout, idempotency, cancellation, and dead-letter behavior where applicable.

## Data, state, and migrations

- State ownership is discoverable and local-first.
- Shared or persisted state has schema, versioning, mutation rules, retention, and migration behavior where applicable.
- Cache invalidation is explicit.
- Migrations are ordered, reviewable, compatible across deploy transitions, and aligned with fixtures.

## Structure and KISS

- Directories are flat, semantic, and justified.
- No speculative layers, dumping grounds, boolean flag explosions, hidden globals, or avoidable nesting.
- Side effects, time, randomness, network, filesystem, environment, and database access are isolated.
- Comments explain why, constraints, or tradeoffs instead of restating code.

## Testing and operations

- Validation covers business rules and IO boundaries at deterministic layers.
- Tests control network, time, randomness, concurrency, and shared state.
- Configuration fails closed and avoids insecure production defaults.
- Observability avoids secrets and raw private data.

## Exceptions and boundaries

- Exceptions are explicit, bounded, justified, mitigated, and reviewed.
- High-risk exceptions have human approval.
- The handoff lists changed files, validation commands/results, skipped checks, known risks, and cleanup notes.
- No PR creation, merge, deployment, production rollout, trading, backtest, or approval is implied.
