---
name: ai-ci-gate-pack
description: The CI gates human pipelines lack for AI-generated code — code duplication at scale, stale dependencies, incomplete integration into existing systems, and shallow tests with high coverage but low mutation score. Repo-scale, cost-tiered checks run at verification. Use when reviewing a change or configuring CI. Language- and app-type-agnostic.
---

# AI-CI Gate Pack

Traditional CI catches the mistakes humans make — syntax, missing tests, style. AI-generated
code passes all of those and fails differently: the same utility written twelve times, a
dependency two majors stale, an endpoint that never wired into logging, a test suite with 90%
coverage and no bugs caught. These gates target exactly that class.

They are **repo-scale and expensive**, so they are **tiered by cost** and start as warnings.
Local, single-file anti-patterns belong to `machine-lint-pack`; security belongs to
`security-per-pr`; this pack owns only what needs the whole codebase or a test run.

## Cost tiers

Run the cheap gates on every change and reserve the expensive ones for where the risk is, so the
pipeline stays fast:

- **Tier 1** — standard lint/tests + `machine-lint-pack` + `security-per-pr` blocking gates. Every change.
- **Tier 2** — duplication + dependency freshness. When shared/common code or dependencies change.
- **Tier 3** — integration completeness + mutation/test-quality. High-risk changes (new surface, auth, data).

## How to invoke

- Claude Code: `/ai-ci-gate-pack` · Codex: `$ai-ci-gate-pack` · Pi/OpenCode: `/skills` picker.

## The gates

Posture (per the source discipline): **start every gate as a warning, measure its false-positive
rate, then make it blocking.** Nothing here blocks on day one; each graduates on evidence.

### 1. Duplication at scale — Tier 2 · advisory (graduates) · applies always
Flag copy-pasted blocks across the repo — duplicated utilities, retry logic, rate limiters,
clients — not just within the diff. The failure mode is N implementations of one thing, each
passing CI in isolation. Capability: *a cross-file duplication detector* (block threshold ~20+
lines). Evidence: the clone set (all locations) and size. This is the verify-side twin of the
reuse-before-you-write scan — that one searches before writing, this one catches what slipped.

### 2. Dependency freshness — Tier 2 · advisory · applies when dependencies exist
Flag dependencies stale enough to matter — more than one major behind current — and imports on
the project's deprecated-patterns list. Distinct from `machine-lint-pack`'s deprecated-API rule:
that flags a deprecated *call in code*, this flags a *dependency version* the project has outgrown.
Capability: *a dependency-version auditor*. Evidence: package, current vs latest, majors behind.

### 3. Integration completeness — Tier 3 · advisory (graduates) · applies to new surface
Verify new code wires into the systems the codebase already runs on: logging, error tracking,
auth/permission middleware, request/trace context, feature flags, metrics. The failure mode is an
endpoint or service that works in isolation but is invisible to operations. Capability: *static
analysis for expected integration points* — flag a new handler that references no error tracking,
a service that never initializes request context. Evidence: the new surface and the missing wiring.

### 4. Test quality beyond coverage — Tier 3 · advisory · applies when tests are present
Coverage says a line ran, not that a bug would be caught. Measure **mutation score** (do the tests
fail when the code is perturbed?), assertion variety, and the negative/edge-case ratio — AI tests
over-index on the happy path. Shallow, no-run test smells belong to `machine-lint-pack`; this is
the run-required depth. Capability: *a mutation tester* + assertion/negative-ratio metrics.
Evidence: surviving mutants (file/line/operator), and the happy-path skew.

## As the coder (generation overlay)

Before adding a utility, retry, client, or limiter, find the existing one and extend it — a
fourth variant is the default failure. Add dependencies at a current major, and off the project's
deprecated list. Wire every new endpoint/service into logging, error tracking, auth, request
context, and flags as you build it — not later. Write tests that kill mutants: assert on
behaviour, cover the failure and edge paths, not fifteen shapes of the happy case.

## As the verifier (gates)

Run the tier appropriate to the change. Report each gate with evidence and route to the coder;
graduate a gate to blocking once its false-positive rate is known and low. **If a gate is skipped
for cost (tier not run, sampling, top-N truncation), say so** — a silent skip reads as "clean"
when it was "not checked." Dismiss false positives with a reason, restorably.

## Notes

- Language coverage is the adapter's job and is well-served by multi-language tools (see
  `gates.yaml` bindings): duplication and mutation both have polyglot engines, so these gates hold
  for any language or app type.
- Cross-refs, never re-implemented here: `machine-lint-pack` (local lint anti-patterns, shallow
  test smells), `security-per-pr` (security), the Context Brief duplicate & reuse scan (pre-write).
