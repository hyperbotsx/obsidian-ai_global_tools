# Domain Overlays

Apply every overlay that matches the profile labels or PRD content. Keep overlays as prompts for PRD content, not automatic approval.

## Frontend

Add requirements for:

- User/operator journeys and visible UX states.
- Loading, empty, error, disabled, and success states.
- Accessibility basics for keyboard, labels, contrast, and focus.
- Preview URL or local path from the active profile.
- Browser/manual verification expectations.
- No unrelated design rewrites or navigation changes.

## Backend/API

Add requirements for:

- API contract, request/response shape, and error semantics.
- Data model, schema, migration, and backward compatibility impact.
- Authorization, authentication, and security checks.
- Failure behavior and observability.
- Unit/integration tests for the contract.

## Data

Add requirements for:

- Data provenance and provider-neutral handling.
- Import/export behavior and file or schema contracts.
- Stale data handling, reproducibility, retries, and idempotency.
- Downstream consumers and compatibility gates.
- Validation fixtures for representative data states.

## Training/Model

Add requirements for:

- Training inputs, outputs, artifacts, and handoff points.
- Reproducibility controls and metrics/evaluation expectations.
- Human approval gates before production or trading use.
- No automatic production, paper trading, live trading, or capital-allocation approval.

## Trading/Backtest

Add requirements for:

- Explicit non-approval for live trading and paper trading.
- Risk controls, data contract dependencies, and validation gates.
- Backtest reproducibility and input versioning.
- Human approval boundaries for any execution beyond analysis.

## Admin/Orchestration

Add requirements for:

- Authority boundaries and human confirmation gates.
- Audit records, drift checks, and fail-closed behavior.
- Operator channel controls for Slack, chat, dashboards, or automation.
- Source-of-truth hierarchy across GitHub, project profiles, artifacts, and memory.
- No autonomous approval, PR creation, merging, deployment, or agent launch unless separately approved.
