---
name: arch-tradeoffs
description: Architecture decisions per Fundamentals of Software Architecture — apply when choosing an architecture style, naming the -ilities a feature must hit, weighing options with real trade-offs, or recording a decision. Triggers on architecture decision, ADR, which architecture, trade-off, scalability vs, architecture characteristics, fitness function, style selection, should we use microservices.
---

# Architecture Trade-offs — decide, state the cost, record it

Two laws govern every decision here:

1. **Everything is a trade-off.** An option presented without its cost is analysis not yet
   finished. If you cannot name what an option makes worse, you do not yet understand it.
2. **Why beats how.** The reasoning outlives the implementation; capture it where the next
   reader will look.

There is no best architecture — only the least-bad fit for the characteristics that
actually matter here.

## Step 1 — name the driving characteristics (max 3)

Pick from: availability, performance, scalability, elasticity, reliability, fault
tolerance, security, deployability, testability, modifiability, evolvability, simplicity,
observability, cost. Rules:

- **Three at most.** Everything cannot be primary; a list of eight is a list of zero.
- Derive them from the business driver, not from taste ("must survive a runner going
  offline" → fault tolerance; "operator ships several times a day" → deployability).
- **Make them measurable.** "Fast" is unusable; "p95 under 200 ms with 50 concurrent
  lanes" can be tested. An unmeasurable characteristic cannot be verified or defended.
- Name the ones you are explicitly sacrificing. That sentence is the decision.

## Step 2 — choose the shape

Reach for the simplest structure that satisfies the driving characteristics. In rough
order of cost to operate:

| Shape | Good at | Pays with |
|---|---|---|
| Modular monolith (layered/modular) | Simplicity, testability, cost | Deployability at scale, partial scaling |
| Pipeline | Composability, one-way transforms | Interactivity, cross-cutting state |
| Microkernel / plugin | Extensibility, third-party surface | Contract rigidity, versioning cost |
| Event-driven | Responsiveness, decoupling, bursts | Debuggability, ordering, eventual consistency |
| Service-based (few coarse services) | Deploy independence, moderate scaling | Distributed data, more ops |
| Microservices | Independent deploy/scale/ownership | Operational complexity, distributed failure |

Escalate only when a driving characteristic demands it. Distribution is a cost you pay
forever: every network hop adds latency, partial failure, and debugging surface.

## Step 3 — decide and record (ADR)

Every non-obvious decision gets a short record — an FRD section, PR body, or decision
note. Five parts, a few lines each:

- **Context** — the forces, including the constraint that makes this non-obvious.
- **Decision** — stated in the active voice, one sentence.
- **Alternatives** — what else was viable, and the specific reason it lost. An
  alternatives list with no plausible entry means the analysis was ceremonial.
- **Consequences** — including what got worse. Every real decision has this section.
- **Status** — proposed / accepted / superseded (by which).

Prefer **reversible** decisions taken early and **irreversible** ones taken late.
Identify which kind you are making before you take it; the cost of being wrong differs by
an order of magnitude.

## Step 4 — make it checkable

A characteristic nobody measures decays silently. Where it matters, add a fitness
function — an automated check that fails when the property erodes: a latency budget in a
test, a dependency-direction lint, a bundle-size ceiling, a startup-time assertion, a
chaos/kill test for fault tolerance. One real check beats a paragraph of intent.

## Red flags

- A choice justified by novelty, résumé value, or "it scales" with no measured target.
- Distribution added for modularity — modularity is achievable in one process.
- Characteristics list with more than three primaries, or none.
- "We'll refactor later" applied to an irreversible decision (data model, public
  contract, wire format).
- An option with no stated downside.

## Verifier gates

- Non-obvious structural change carries a decision record with consequences.
- Driving characteristics are named and measurable.
- At least one plausible alternative documented with a concrete losing reason.
- A new distributed boundary names the force requiring it.
- Where feasible, the characteristic has an automated check, not just prose.
