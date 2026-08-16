---
name: machine-lint-pack
description: Catch the anti-patterns AI coding agents produce — swallowed errors, type escapes, dead code, leftover variant files, async misuse, deprecated APIs, abstraction bypass, and shallow tests. Deterministic per-file/per-diff lint rules applied while code is written and enforced at verification. Use whenever generating or reviewing code. Language- and app-type-agnostic.
---

# Machine-Lint Pack

Agents produce code that compiles, lints on the defaults, and passes tests — while quietly
tripping a recognizable set of anti-patterns. This pack names them and turns each into a
deterministic rule, so "systematic problems yield to systematic prevention."

One doctrine, two consumers: the *coder* gets it as a generation overlay, the *verifier*
enforces the gate list in `gates.yaml`. Checks are stated as **capability intents**, never a
tool or language, so they hold on any stack.

## Boundary — what this pack owns, and what it defers

This pack owns the **local** anti-patterns — the ones decidable from a single file or the diff.
Two neighbours own the rest; this pack references them and never re-implements them:

- **Security** anti-patterns (secrets, injection, weak auth) → `security-per-pr`.
- **Repo-scale / expensive** gates — code **duplication**, dependency **freshness**,
  integration **completeness**, **mutation**/test-quality-beyond-coverage → `ai-ci-gate-pack`.

The seam is scope and cost: if a rule needs the whole codebase or a test run, it belongs to
`ai-ci-gate-pack`; if it is a security property, it belongs to `security-per-pr`; what is left —
a rule you can decide by reading the change — is here.

## How to invoke

- Claude Code: `/machine-lint-pack` · Codex: `$machine-lint-pack` · Pi/OpenCode: `/skills` picker.

## The rules

Each names **what it flags**, its **severity**, and **when it applies**. Posture: block only the
unambiguous, mechanical classes; start the judgment-tinged ones advisory and graduate them once
their false-positive rate is measured.

### 1. Leftover variant files — BLOCKING · applies always
Flag files whose names mark them as iteration residue: `*_old`, `*_new`, `*_v2`, `*_copy`,
`*_backup`, `* (copy)`, `*.bak`, and near-duplicate siblings of a real module. Rely on git
history, not on a second copy in the tree. Purely name-based, so it is language-agnostic.
Capability: *a filename-residue detector*.

### 2. Swallowed errors — BLOCKING (high-confidence) · applies always
Flag catches that hide failure: empty catch blocks, catch-all handlers that neither handle nor
re-surface, errors logged-and-continued where the caller needed to know. "Don't swallow" means
surface it (to the caller or the operator), never silently drop it. Capability: *an
error-handling lint*.

### 3. Type escapes — ADVISORY (graduates) · applies to typed languages
Flag holes punched in the type system: dynamic/`any` types where a real type is known, unchecked
casts, and blanket type-suppression comments. Capability: *a type-strictness check* (the
language's own strict mode). Does not fire on untyped languages.

### 4. Dead code & over-engineering — ADVISORY · applies always
Flag unused imports, variables, parameters, and unreachable branches, plus abstraction with a
single caller and no second use in sight. Delete unused code; do not comment it out.
Capability: *a dead-code / unused-symbol lint*.

### 5. Async misuse — ADVISORY (graduates) · applies to code using concurrency
Flag blocking calls inside async contexts, unawaited/floating async results, and fire-and-forget
work with no error path. Capability: *an async-correctness lint*. Applies only where the language
and code use async/concurrency.

### 6. Deprecated APIs — ADVISORY · applies when a deprecated-patterns list exists
Flag calls the project or ecosystem has moved past — known-deprecated stdlib/framework APIs, and
anything on the project's maintained deprecated-patterns list. Training data is ~2 years stale, so
this is where an agent reaches by default. Capability: *a deprecated-pattern detector*.

### 7. Abstraction bypass — ADVISORY · applies when the project defines wrappers/banned APIs
Flag use of a raw library or primitive where the project has a wrapper for exactly that concern
(e.g. a raw HTTP client instead of the project's client). Capability: *a banned-API / wrapper
enforcement check* over the project's banned-import list. This is the write-side twin of the
reuse-before-you-write doctrine.

### 8. Shallow tests — ADVISORY · applies when tests are present
Flag test smells decidable without running: assertion-free tests, tests that never use the value
they set up, over-mocking that asserts against the mock instead of behaviour, and copy-pasted
near-identical cases. Depth beyond this — mutation score — is `ai-ci-gate-pack`. Capability:
*a test-smell lint*.

## As the coder (generation overlay)

Surface every error to the caller or operator; never write an empty or catch-all-and-continue
handler. Keep the type system whole — no `any`, no blanket suppressions — where the type is
known. Leave no unused symbol and no variant file behind; git is the history. Await what you
start and give async work an error path. Reach for the project's wrapper before a raw library,
and for the current API before the one in memory. Write tests that assert on behaviour, not on a
mock.

## As the verifier (gates)

Run `gates.yaml`. Block the mechanical classes (variant files, high-confidence swallowed errors);
report the rest with evidence and route to the coder. Dismiss a false positive **with a reason**,
restorably. Graduate an advisory class to blocking once it is reliably precise.

## Notes

- Language coverage is the adapter's job: prefer a multi-language rule engine, fall back to the
  language's native linter per `gates.yaml` bindings. The filename-residue rule needs no tool.
- Do not restate `security-per-pr` or `ai-ci-gate-pack` rules here — reference them.
