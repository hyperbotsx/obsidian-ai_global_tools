# Canonical Agent Engineering Standards v1

## 1. Philosophy

Complexity is the enemy of reliability. Prefer the lowest viable complexity that is correct, explicit, testable, and easy to delete. Build boring, readable, deterministic systems before clever abstractions. Consolidate before adding layers. Keep names, ownership, boundaries, and flow obvious enough for the next human or agent.

Ponytail-inspired engineering means less code, less hierarchy, fewer hidden paths, and tidier surfaces without sacrificing correctness or safety.

## 2. Universal engineering rules

- Solve the current problem, not speculative future scale.
- Prefer flat structures and explicit data flow over deep indirection.
- Keep side effects named, isolated, and reviewable.
- Fail closed for unsafe, ambiguous, missing, or stale state.
- Make inputs, outputs, errors, retries, timeouts, and ownership visible.
- Use comments only for why, constraints, or non-obvious tradeoffs.
- Do not store secrets, credentials, raw prompts, raw transcripts, private account data, or private operational state in standards artifacts, logs, generated docs, UI state, or tests.
- Do not hardcode temporary product names in reusable rules or integration surfaces; use configured names or generic AgentOps terms.

## 3. Backend architecture

- Transport handlers parse requests, validate inputs, call application/domain logic, and format responses.
- Business and domain logic must not depend directly on HTTP, CLI, framework, database, queue, or scheduler details unless those details are intentionally isolated behind an adapter.
- Data access is separate from business rules.
- Side effects are explicit boundaries such as repository, gateway, notifier, job runner, clock, filesystem, or external client.
- Error paths are deliberate: fail closed, return actionable errors, avoid silent failure, and preserve caller-deterministic behavior.
- Observability belongs at meaningful boundaries and must not leak secrets or raw private data.
- Background jobs and async workflows need named retry, idempotency, timeout, cancellation, and dead-letter behavior where applicable.

## 4. Frontend architecture

- Components have one clear responsibility.
- Separate rendering from business rules and data fetching where practical.
- Prefer predictable, unidirectional data flow.
- Compute derived data explicitly instead of duplicating it across state locations.
- Keep UI state local by default; promote it only when ownership is genuinely shared.
- Global state has a named owner, mutation rules, persistence rules if any, and bounded scope.
- Effects are isolated, dependency-aware, and easy to reason about.
- Compose semantic primitives instead of deeply nested anonymous structures.

## 5. Styling and design-system tokens

- Centralize colors, spacing, typography, radii, elevation, breakpoints, and semantic states as design tokens.
- Prefer flat semantic tokens over deeply nested token hierarchies.
- Do not scatter one-off visual constants across components.
- Layout systems must be deterministic and inspectable.
- Prefer reusable visual primitives over ad hoc styling.
- Add animation, responsive behavior, and visual complexity only when they serve a clear product purpose.
- Treat focus states, contrast, spacing, reduced-motion behavior, and touch targets as functional requirements.

## 6. State management

- Keep state local until multiple owners need it.
- Use immutable transitions and explicit reducers/actions for non-trivial changes.
- Avoid hidden mutation, implicit global singletons, temporal coupling, and untracked event chains.
- Make state ownership discoverable from file or module structure.
- Persisted state needs schema, versioning, retention, migration, and recovery behavior where applicable.
- Cache state needs invalidation semantics and must not become an untracked source of truth.

## 7. Database and schema migrations

- Migrations are version-controlled, ordered, reviewable, and environment-aware.
- Prefer declarative schema changes when the stack supports them.
- Data migrations define rollback/recovery expectations or state why rollback is unsafe.
- Avoid hidden triggers, opaque database logic, and side effects application code cannot reason about.
- Preserve compatibility during deploy transitions where applicable.
- Constraints, indexes, and defaults are intentional; document non-obvious behavior.
- Test fixtures and migrations stay aligned.

## 8. API contracts and integrations

- Define request, response, error, pagination, streaming, and compatibility semantics explicitly.
- Use strict schemas, typed IDLs, or equivalent contracts where practical.
- Breaking changes need versioning or a migration path.
- Integration boundaries need timeouts, retry rules, idempotency expectations, cancellation behavior, and failure handling.
- Error responses should be stable enough for callers to handle deterministically.
- External APIs, SDKs, auth schemes, rate limits, and deprecations require fresh research before implementation.

## 9. Testing and quality assurance

- Pure functions and business rules get focused unit tests.
- IO boundaries get integration tests, contract tests, or explicit manual validation when automation is not practical.
- End-to-end tests cover critical user or operator flows but must not be the only validation layer.
- Tests are deterministic: control network, time, randomness, concurrency, and shared state.
- Fixtures are explicit, minimal, and representative.
- Flaky tests are fixed or quarantined with a tracked explanation; they are not normalized.
- Handoffs list validation commands, results, skipped checks, and reasons.

## 10. Configuration and secrets

- Validate runtime configuration at boot with a schema or equivalent checks.
- Missing required configuration fails closed.
- Defaults must be safe for local development and must not accidentally enable insecure production behavior.
- Environment-specific behavior is named, reviewable, and testable.
- Tokens, service accounts, webhooks, and API clients use least privilege.
- Never commit, log, prompt-embed, artifact-write, or UI-expose secrets or raw private data.

## 11. Directory layout

- Prefer flat semantic directories over deep nesting.
- Directories represent stable concepts such as domain, feature, adapter, test, schema, migration, or shared primitive.
- Avoid generic dumping grounds such as `utils`, `helpers`, `misc`, or `common` unless tightly scoped locally.
- Separate source, tests, docs, generated files, runtime artifacts, schemas, migrations, and fixtures.
- File names explain ownership and purpose.
- New directories require a current reason, not speculative future scale.

## 12. Function and module design

- Functions do one thing at one level of abstraction.
- Inputs and outputs are explicit.
- Prefer pure functions where possible.
- Isolate time, randomness, filesystem, network, environment, and database access behind named boundaries.
- Avoid boolean flag explosions, deeply nested conditionals, hidden global dependencies, and broad public APIs.
- Modules expose narrow public APIs and hide internal details.

## 13. Immutability and data flow

- Prefer immutable data transformations by default.
- Mutations have clear ownership and limited scope.
- Shared mutable state requires justification and tests around ordering, concurrency, and failure behavior.
- Data transformations are traceable from input to output.
- Avoid hidden observers, implicit event chains, and silent mutation across unrelated modules.

## 14. Mandatory Exa research directive

Before generating directory structures, boilerplate code, framework paradigms, test layout, migration layout, state-management patterns, or design-system layout for a concrete project, downstream agents must use Exa search to research current industry consensus, official/versioned guidance, and modern minimalist patterns for the selected stack.

Agents must cite or summarize the evidence used for stack-specific structure decisions. If Exa is unavailable, blocked, stale, undated for a volatile surface, or conflicting, fail closed and ask the human or Researcher. Fresh research informs stack application; it does not override this pack's minimalist standards.

## 15. Exceptions

Exceptions are explicit, documented, bounded, and justified by a concrete project constraint. They must preserve readability, testability, deterministic behavior, and low cognitive load where possible. Exceptions involving security, secrets, data loss, migrations, external auth, production behavior, or human approval boundaries require human review.

## 16. Agent workflow boundaries

Researchers provide source-cited context and do not edit. Coders implement only approved scope and write handoffs. Verifiers review checkpoints and bug-checks without replacing human approval. Stewards review placement, artifacts, cleanup, and source-of-truth drift. This pack never authorizes PR creation, merging, deployment, hard-blocking enforcement, production rollout, trading, paper trading, live trading, backtests, or bypassing human gates.
