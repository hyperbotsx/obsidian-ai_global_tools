---
name: security-per-pr
description: Embed application security into every change — the security doctrine Modula applies while code is written and again when it is reviewed. Use whenever generating, modifying, or reviewing code that handles input, credentials, data, dependencies, or network surface. Covers secrets, dependency vulnerabilities, injection, auth/authz, error leakage, transport/headers, and exposed routes. Language- and app-type-agnostic.
---

# Security-Per-PR

AI-generated code is functional-but-exploitable by default: it optimizes for the stated goal,
not for the security permit nobody asked for. This skill makes security a standing property of
every change instead of a review-time afterthought.

It is **one doctrine with two consumers**: the *coder* receives it as a generation overlay
("write it secure the first time"), and the *verifier* enforces it as gates (`gates.yaml`
beside this file). They cannot diverge because they ship together.

Every check is stated as a **capability intent** ("a secrets scanner"), never as a specific
tool or language — so it holds for any stack and any app type. Concrete tool bindings and
per-harness invocation live in the adapter layer, not here. Scans run where the code already
is (locally / runner-side); source never leaves the machine to be scanned.

## How to invoke

- Claude Code: `/security-per-pr`
- Codex: `$security-per-pr`
- Pi / OpenCode: `/skills` picker, or it activates from the description above

## The applicability rule (read first)

Not every app is a web app. A check fires only where its **`applies_when`** predicate holds, so
a CLI, a library, a data pipeline, or an embedded target is never nagged about HTTP headers it
does not have. Three checks are near-universal (secrets, dependencies, injection); the rest are
conditional on the surface actually present in the change. When the surface is ambiguous, ask —
do not assume a surface is absent, and do not assume it is web.

## The seven checks

Each check names **what to verify**, **when it applies**, its **severity**, and the **evidence**
a finding must cite. Severity posture: block only what is unambiguous; start the judgment-heavy
checks advisory and let them graduate once their false-positive rate is measured.

### 1. Exposed secrets — BLOCKING · applies always
Verify no credential is committed: API keys, tokens, passwords, private keys, connection
strings — in source, config, or fixtures — and not reachable in prior history of the change.
Capability: *a secrets scanner* (with git-history awareness). Evidence: file + line (or the
introducing commit), and the detector/rule that matched.

### 2. Dependency vulnerabilities — BLOCKING (high + critical) · applies when dependencies change or exist
Verify no added or present dependency carries a known high/critical vulnerability. Capability:
*a dependency-vulnerability auditor* over the ecosystem's lockfile/manifest. Evidence: package,
version, advisory id (CVE/GHSA), severity. Lower severities are advisory.

### 3. Injection — BLOCKING (high-confidence) · applies always
Verify untrusted input cannot reach an interpreter: SQL/NoSQL, OS command, template, LDAP,
path, and cross-site scripting sinks. Prefer parameterization and safe APIs over escaping.
Capability: *a SAST scanner with taint/dataflow rules* (OWASP rulesets). High-confidence,
reachable findings block; single-file heuristic hits are advisory. Evidence: source → sink path.

### 4. Authentication / authorization bypass — ADVISORY (graduates) · applies to request-handling surfaces
Verify every protected operation actually checks identity and permission: unauthenticated
requests are rejected (401/403), and one user cannot act on another's resource (no missing
object-level authorization). Capability: *route/handler inventory* + judgment; a dynamic probe
where a running surface exists. Evidence: the endpoint/handler and the missing check.

### 5. Error-message leakage — ADVISORY (graduates) · applies to service surfaces
Verify errors returned to callers do not leak stack traces, file paths, SQL, or internal
identifiers; detail goes to logs, not responses. Capability: *SAST* + judgment. Evidence: the
handler/response path and the leaked class of detail.

### 6. Transport & security headers — ADVISORY · applies to web surfaces only
Verify HTTPS is enforced and the baseline response headers are present: HSTS,
Content-Security-Policy, X-Content-Type-Options, X-Frame-Options (or framework equivalents).
Capability: *header/config check*. Evidence: the surface and the missing header. Does not fire
on non-web apps.

### 7. Exposed admin / debug routes — ADVISORY · applies to web surfaces only
Verify no administrative, debug, or introspection surface is unintentionally public:
`/admin`, `/debug`, `/.env`, `/api/docs`, framework debug consoles, verbose error modes.
Capability: *route-exposure / config check* + judgment. Evidence: the path and its auth state.

## As the coder (generation overlay)

Before and while you write:

- Treat every external value — request field, header, filename, env, third-party response — as
  untrusted until validated at the boundary; keep the untrusted shape out of core types.
- Reach for parameterized queries and framework-safe rendering; never build an interpreted
  string by concatenation.
- Take secrets from configuration/secret stores; never inline them, never log them, never put a
  real one in a fixture.
- Add or update a dependency at a version free of known high/critical advisories; prefer the
  maintained, current major.
- Put an authorization check at every new protected operation, object-level included.
- Return errors that say *what the caller may know*; send the diagnostic detail to logs.
- On a web surface, wire the baseline headers and keep debug/introspection surfaces behind auth
  or off in production.

## As the verifier (gates)

Run the gate list in `gates.yaml`. Block on the unambiguous classes (secrets, high/critical
dependency advisories, high-confidence reachable injection). Report the advisory classes with
their evidence and route them to the coder; track their false-positive rate, and graduate a
class to blocking once it is reliably precise. A false positive is dismissed **with a reason**
and is restorable — never silently dropped.

## Threat modeling on high-risk changes (STRIDE)

Where a change touches a **high-risk surface** — authentication, authorization, payments, data models,
a new external endpoint, cryptography, file upload, or deserialization — the seven checks are not
enough; the change also gets a STRIDE threat model. Walk the six categories — Spoofing, Tampering,
Repudiation, Information disclosure, Denial of service, Elevation of privilege — against the change,
and produce a **threat table** (threat · category · affected asset · mitigation present? · action).
It produces analysis, never a code edit. Full walkthrough: `references/stride.md`.

Runs isolated where the harness supports a read-only sub-context (Claude `context: fork`), and
**inline as a SKILL.md step where it does not** (Pi and others). The isolation is a preference, not
a correctness dependency — the threat table is identical either way.

## Notes

- **Language/app-type coverage** is the adapter's job: each capability binds to a multi-language
  tool where one exists, so this doctrine is authored once and holds everywhere. The default
  bindings and an alternate single-binary engine are declared in `gates.yaml`.
- STRIDE composes with `vision-keeper`'s fork-optional/inline-fallback pattern — both are read-only
  analyses that degrade gracefully across harnesses.
