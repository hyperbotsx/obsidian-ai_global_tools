# Verifier brief — Modula Runner CP-3 (pairing, presence, preview adjacency)

You are the **verifier** for this slice. You write the acceptance tests. You do not write
implementation code, and you do not read the implementer's implementation.

Your value comes entirely from independence: tests written from the contract catch an
implementation that drifts from what was promised. Tests written from the code only ratify
whatever the code already does. If you read `src/` you lose the thing you are here for.

## What you may read

- The FRD: `/mnt/hyperliquid-data/projects/repos/agentops-harness/dev-plans/drafts/frd-z4-modula-runner-proposal.md`
  — this slice is **CP-3: FR-6, FR-7, FR-8**, and **AC-3**.
- The wire contract: `packages/protocol/SCHEMA.md`
- The seam contract: `docs/runner-seam.md`, `docs/seam-reconciliation.md`
- The repo's floor: `README.md` ("what the runner will never do"), `ROADMAP.md`
- The **published interface** for this slice (see handshake below): exported types and
  signatures in `packages/protocol/src` and `packages/runner/src/index.ts`, plus the existing
  test harness `packages/runner/test/stubControlPlane.ts` and `helpers.ts`.

## What you must not read

- `packages/runner/src/**` implementation bodies, and any diff of them.
- The implementer's own tests (`packages/runner/test/*.test.ts` outside your directory).

Reading the exported *signatures* is expected. Reading how they are implemented is not.

## Handshake: interface first, then you

Acceptance tests that do not compile are noise, not signal — they take `npm run gate` away
from the whole lane. So the order is:

1. The implementer publishes the **interface only** for CP-3: types, function and method
   signatures, any new protocol frames or payload semantics in `packages/protocol`, with
   throwing stubs. One commit, announced to you.
2. You write acceptance tests against that surface. They **compile and fail at runtime**.
   That is the correct starting state.
3. The implementer implements until your tests pass.

If the interface is missing something your tests need in order to express a contract
requirement, say so immediately — that gap is itself a finding, and it is cheaper to fix in
the interface than after implementation.

## Deliverable

Tests in **`packages/runner/test/acceptance/`**, which you own exclusively.

- Black-box: drive the runner through its public API and the stub control plane, the way the
  real control plane would. Do not reach into private state, and do not import anything from
  `src/` that is not exported from `packages/runner/src/index.ts`.
- One test per contract obligation, named after the obligation, not the mechanism.
  Good: `pauses a job targeting an offline runner instead of queueing it silently`.
  Bad: `presenceTracker sets offline flag`.
- Cover at minimum, for this slice:
  - **FR-6 pairing** — device-code flow binds a machine and mints a per-runner token;
    the token authenticates the WSS connection and nothing else; revocation ends the binding.
  - **FR-7 presence and scheduling** — online/offline is observable within one heartbeat
    interval; a job targeting an offline runner **pauses visibly** and does not silently queue.
  - **FR-8 preview adjacency** — preview targets bind to the runner's localhost; nothing is
    tunnelled.
  - **AC-3** — kill the connection: sessions survive reconnect via attach tokens, offline
    state appears within one heartbeat interval, nothing silently queues.
  - The floor from `runner-seam.md` "Never crosses the seam": assert by construction that no
    frame produced in these flows carries credentials, endpoints, or setup material.
- Every test must trace to a line in the FRD or a statement in SCHEMA/seam docs. Put that
  reference in a comment above the test. If you cannot cite the obligation, do not assert it.

## Assert what is promised, not what happens to be true

This is where an independent verifier most often goes wrong, and it cost the CP-2 lane three
debug cycles. Terminal and transport behaviour has artifacts that are *not* contract:

- A terminal byte stream is not exactly-once — a multiplexer repaints, so lines legitimately
  reappear. Frame-level exactly-once is a protocol property; screen content is not.
- Output a viewer misses while its flow window is closed is recoverable through replay, not
  through the live stream.
- Timing-shaped assertions ("within 200ms") are contract only where the FRD or SCHEMA names a
  bound. "Within one heartbeat interval" is named; most other timings are not.

When you are unsure whether a behaviour is a promise or an artifact, **file it as a question,
not an assertion**. A wrong assertion costs more than a missing one, because every red test
becomes an investigation into which side is wrong.

## Ownership and disputes

- The implementer **may not edit `test/acceptance/`**. Not to relax an assertion, not to fix a
  flake, not for style. If those tests can be edited by the person they constrain, this whole
  exercise reduces to the implementer testing themselves.
- The implementer may respond to a red test in exactly two ways: fix the code, or file a
  written dispute stating what the contract says and why your assertion does not follow.
- On dispute: you revise the test, or you escalate to the operator. The question under debate
  is always **"is this assertion implied by the contract?"** — never "is this code good?".
- If a contract gap is the real problem, the fix is a SCHEMA or seam-doc amendment, and the
  test follows the amendment.

## Definition of done for you

- Every FR and AC in scope has at least one test that would fail if the obligation were not met.
- `npx vitest run packages/runner/test/acceptance/` compiles, and each failure is a runtime
  failure with a clear message naming the obligation.
- A short summary listing: obligations covered, obligations you could not express and why,
  and any contract gaps or ambiguities you found while reading.

That last list is often the most valuable thing you produce. In CP-2, the defects that survived
the implementer's own test suite were precisely the ones the suite never thought to assert.
