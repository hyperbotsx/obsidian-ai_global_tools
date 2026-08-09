# Exception Policy

Exceptions are allowed only when the approved PRD or human-reviewed implementation constraints require them.

## Required exception record

Every exception must include:

- Rule being excepted.
- Project constraint requiring the exception.
- Scope and expiration or review date.
- Risks introduced.
- Mitigations preserving readability, testability, determinism, and low cognitive load.
- Owner.
- Validation evidence.
- Human approval when required.

## Human review required

Escalate before proceeding when an exception involves:

- Security controls, secrets, credentials, or private data.
- Data loss, migrations, rollback, retention, or recovery.
- External auth, payment, trading, production systems, or privileged APIs.
- Production rollout, hard-blocking enforcement, deployment, merge, or PR approval.
- Relaxing human gates.

## Fail-closed behavior

If the exception is unclear, unbounded, undocumented, or safety-sensitive without approval, stop and ask the human or verifier. Do not normalize exceptions into new defaults.
