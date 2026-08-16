# STRIDE threat model — high-risk change walkthrough

Loaded on demand when `security-per-pr` reaches a high-risk surface. Read-only analysis: it
produces a threat table, never a code edit. Run it isolated (Claude `context: fork`, read-only
tools) or inline where the harness has no fork — the output is identical.

## When it triggers

Any of: authentication/session, authorization model, payments/billing, a data model or migration,
a new external endpoint/surface, cryptography, file upload, deserialization of untrusted input.

## The six categories

Walk each against the change. For each, ask the question and, if a threat exists, record whether a
mitigation is already present.

| Category | Ask | Typical mitigation |
|----------|-----|--------------------|
| **S**poofing | Can an actor pretend to be someone/something else? | Authentication, signature/verification, mutual TLS |
| **T**ampering | Can data or code be modified in transit or at rest? | Integrity checks, signing, parameterized writes, access control |
| **R**epudiation | Can an actor deny an action with no trace? | Audit log, receipts, append-only records |
| **I**nformation disclosure | Can data leak to someone who should not see it? | Authorization, encryption, error-leakage control, least privilege |
| **D**enial of service | Can an actor exhaust or wedge the system? | Rate limits, quotas, timeouts, bounded work, backpressure |
| **E**levation of privilege | Can an actor gain rights they should not have? | Object-level authorization, deny-by-default, input validation at the boundary |

## Output — the threat table

Produce one row per identified threat:

```
| threat | category | affected asset | mitigation present? | action |
|--------|----------|----------------|---------------------|--------|
| ...    | S/T/R/I/D/E | ...         | yes / no / partial  | route-to-coder / accept / needs-decision |
```

- **mitigation present? = no** on a plausible, reachable threat → route to the coder with the
  affected asset and the expected mitigation.
- **partial** → name what is missing.
- Threats with an operator/business trade-off (accept the risk vs. mitigate) are `needs-decision`,
  surfaced to the human — never silently accepted by the model.

## Relationship to the seven checks

The seven `gates.yaml` checks are the always-on floor; STRIDE is the risk-triggered ceiling. A
STRIDE finding that maps to one of the seven (e.g. Information disclosure → error-leakage) routes
through that gate; findings with no gate (e.g. a missing rate limit → DoS) route to the coder
directly with the threat-table row as evidence.
