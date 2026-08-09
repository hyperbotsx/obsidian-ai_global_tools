# Domain Overlays

Apply every overlay that matches the profile labels or PRD content. Keep overlays as prompts for PRD content, not automatic approval.

## Research-first surfaces

Populate the optional PRD field when implementation depends on volatile external
surfaces such as third-party APIs, SDK versions, auth schemes, rate limits,
provider docs, browser/runtime behavior, or deprecation-prone endpoints. Name the
surface and the pre-implementation question the coder must ask the researcher.
Use `none` when no mandatory freshness consult is needed.

## Frontend

Add requirements for:

- User/operator journeys and visible UX states.
- Loading, empty, error, disabled, and success states.
- Accessibility basics for keyboard, labels, contrast, and focus.
- Preview URL or local path from the active profile.
- Browser/manual verification expectations.
- Research-first surfaces for browser/runtime APIs, vendor SDKs, or UI libraries with version-sensitive behavior.
- No unrelated design rewrites or navigation changes.

## Backend/API

Add requirements for:

- API contract, request/response shape, and error semantics.
- Data model, schema, migration, and backward compatibility impact.
- Authorization, authentication, and security checks.
- Failure behavior and observability.
- Research-first surfaces for third-party APIs, SDKs, auth schemes, rate limits, or deprecations.
- Unit/integration tests for the contract.

## Data

Add requirements for:

- Data provenance and provider-neutral handling.
- Import/export behavior and file or schema contracts.
- Stale data handling, reproducibility, retries, and idempotency.
- Downstream consumers and compatibility gates.
- Research-first surfaces for provider docs, datafeed capabilities, schemas, rate limits, or deprecations.
- Validation fixtures for representative data states.

## Training/Model

Add requirements for:

- Training inputs, outputs, artifacts, and handoff points.
- Reproducibility controls and metrics/evaluation expectations.
- Human approval gates before production or trading use.
- Research-first surfaces for framework, model, artifact, or runtime version changes.
- No automatic production, paper trading, live trading, or capital-allocation approval.

## Trading/Backtest

Add requirements for:

- Explicit non-approval for live trading and paper trading.
- Risk controls, data contract dependencies, and validation gates.
- Backtest reproducibility and input versioning.
- Research-first surfaces for exchange/provider APIs, market data contracts, SDKs, auth, rate limits, or deprecations.
- Human approval boundaries for any execution beyond analysis.

## Admin/Orchestration

Add requirements for:

- Authority boundaries and human confirmation gates.
- Audit records, drift checks, and fail-closed behavior.
- Operator channel controls for Slack, chat, dashboards, or automation.
- Source-of-truth hierarchy across GitHub, project profiles, artifacts, and memory.
- Research-first surfaces for external automation APIs, GitHub behavior, MCP/pi extensions, or deployment tooling.
- No autonomous approval, PR creation, merging, deployment, or agent launch unless separately approved.
