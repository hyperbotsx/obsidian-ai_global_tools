---
name: acceptance-specs
description: Contract-derived acceptance specifications written by an independent verifier before implementation — when they pay, how to write them, and what they provably do not catch. Use when planning a slice, setting up a verifier lane, or deciding whether a feature wants Gherkin. Triggers on acceptance tests, ATDD, BDD, Gherkin, specification by example, verifier lane, write the tests first, independent tests.
---

# Acceptance specs

An independent verifier writes the acceptance tests from the contract, before the
implementer starts. The implementer cannot edit them.

The mechanism is not "tests first". It is **independence**. A builder's tests encode the
builder's blind spots: they assert what the builder thought to check, which is a subset of
what the builder thought about. Classic TDD does not fix this — the same mind writes both
sides. Separating the author is what makes the tests capable of failing for reasons the
implementer did not anticipate.

Evidence this is written from: modula-runner CP-2 (pty host, 2026-08-09). A 166-test suite
written by the implementer passed *with* an output-loss bug present — the exit path discarded
a command's final output. The tests asserted that the exit waited and that no errors appeared;
they never asserted the output arrived. An independent reviewer found it in minutes.

## Decide first: does this slice want acceptance specs?

Write them where the contract's promises are observable from outside. Skip them where the
risk is internal.

| Slice shape | Acceptance specs | Why |
|---|---|---|
| Protocol / wire contract | Yes, high value | Obligations are literally written down |
| Business rules, pricing, eligibility | Yes, high value | Examples *are* the specification |
| Lifecycle and state machines | Yes | Illegal transitions are contract-level |
| Infrastructure adapters (pty, tmux, sockets, git) | Partly | Only the promised surface; the quirks are not in any contract |
| Resource, concurrency, scale behaviour | No | Not expressible as a scenario — see the coverage table |

**Test at the level where the promise lives.** The standard BDD advice — test the domain
layer, decouple from infrastructure, keep suites in milliseconds — is right for business logic
and wrong for adapters. In CP-2 the valuable tests drove *real* tmux and *real* ptys; a
domain-layer-only spec would have missed tmux's pane-target form, its output coalescing for a
paused client, and the status line consuming a terminal row. Fast, mocked specs would have been
green and useless.

## Independence rules

The verifier:

- **reads** the FRD / PRD acceptance criteria, the wire schema, the seam or contract docs, and
  the *published interface* (exported types and signatures);
- **does not read** implementation bodies, implementation diffs, or the implementer's own tests;
- **runs a different model** from the implementer where the harness allows it. Diff-blindness is
  the mechanism; model diversity is a reinforcement, not a substitute.

If the verifier reads the implementation, it will ratify it. That is the failure mode this
whole practice exists to prevent.

## Interface-first handshake

Acceptance tests that fail to *compile* are noise, not signal, and they take the quality gate
away from the entire lane. So:

1. Implementer publishes the **interface only** — types, signatures, new protocol shapes,
   throwing stubs. One commit, announced.
2. Verifier writes tests against that surface. They compile and fail at **runtime**. That is
   the correct starting state.
3. Implementer implements until they pass.

If the interface cannot express a contract obligation, that gap is itself a finding, and it is
cheaper to fix in the interface than after implementation.

## Writing the specs

- **Ubiquitous language.** Define domain terms strictly and use them exactly. Agents hallucinate
  logic when terminology is loose. "Blocks execution when volatility is below the dead-zone
  threshold" beats "doesn't trade when the market is flat".
- **Declarative, not imperative.** State the obligation and its observable outcome, not the
  click-path or the call sequence. Imperative scenarios test the implementation's shape and
  break on every refactor.
- **One test per obligation, named after the obligation.** `pauses a job targeting an offline
  runner instead of queueing it silently`, not `presenceTracker sets offline flag`.
- **Cite the source.** Every test carries a comment referencing the FRD line or schema statement
  it enforces. If you cannot cite the obligation, do not assert it.
- **Assert what is promised, not what happens to be true.** This is where independent verifiers
  most often go wrong, and each mistake costs a debug cycle to unmask, because a red test could
  mean either side is wrong. Real examples from CP-2, all initially asserted and all wrong:
  a terminal byte stream is not exactly-once (multiplexers repaint); output missed while a
  viewer's flow window was closed is recoverable by replay, not from the live stream; timing
  bounds are contract only where the contract names them.
  **When unsure whether a behaviour is a promise or an artifact, file it as a question, not an
  assertion.**

## Gherkin: when it earns its keep

Given/When/Then forces preconditions, action, and observable outcome to be named separately,
which is exactly where under-specification hides. It is also well represented in model training
data, so agents parse and generate it reliably.

It costs a glue layer. Gherkin plus step definitions is two artifacts where a well-named test is
one, and that glue is where BDD adoptions usually die.

Use it when specs are read by people who do not read code, or when the feature files serve as
context anchors that reload a system's intent into an agent cheaply. Skip it when the loop is
agent-to-agent and an expressive test name carries the same information. Decide deliberately;
do not adopt it by default.

## Ownership and disputes

- The implementer **may not edit the acceptance directory** — not to relax an assertion, not to
  fix a flake, not for style. Tests that can be edited by the party they constrain are not
  constraints.
- A red test admits exactly two responses: fix the code, or file a written dispute stating what
  the contract says and why the assertion does not follow.
- The question under dispute is always **"is this assertion implied by the contract?"** — never
  "is this code good?". That question is decidable; the other one is an argument.
- If the contract is genuinely ambiguous, the fix is a contract amendment and the test follows
  the amendment.

## What specs catch, and what they do not

Measured against CP-2's 67 review findings (63 fixed, 4 routed as design boundaries). Roughly
half were contract-observable; the rest required reading code.

**Contract-derived acceptance specs would have caught:** output loss at exit · end-of-stream
overtaking an undrained tail · a lifecycle message dropped behind buffered input · a command
unkillable before initialization · metadata a peer's validator rejects · replay ordering ·
exit-code propagation · provisioning refusals and reuse rules.

**Only code review caught:** session environment leaking into a shared server process ·
per-session polling that scaled to 20N subprocesses per second · an operational failure read as
"resource absent" · kills reported as confirmed without verification · an unbounded capture
buffer · synchronous calls blocking a shared event loop · config injection through a predictable
temp path · a two-phase recovery invariant violated by a later patch.

The second list is resource, concurrency, security and failure-mode properties. No scenario
expresses "subprocess count stays constant as sessions grow". **Acceptance specs shrink review
rounds; they do not retire the reviewer.** Plan for both, and expect the reviewer's findings to
shift toward design and security as the specs absorb the correctness defects.

## Definition of done for the verifier

- Every in-scope requirement has at least one test that would fail if the obligation were unmet.
- The acceptance suite compiles; every failure is a runtime failure naming the obligation.
- A written summary of: obligations covered, obligations that could not be expressed and why,
  and contract gaps or ambiguities found while reading.

That last list is usually the most valuable artifact. The defects that survive an implementer's
own suite are precisely the ones it never thought to assert.

## Sources

Gojko Adzic, *Specification by Example* (process, living documentation, "the examples are the
specification") · John Ferguson Smart with Jan Molak, *BDD in Action, 2nd ed.* (discovery
through automation, separating business-readable specs from glue) · Kamil Nicieja, *Writing
Great Specifications* (Gherkin craft, declarative over imperative, stripping incidental detail).
The independence rule and the coverage table above are not from these books — they come from
measuring an agentic lane.
