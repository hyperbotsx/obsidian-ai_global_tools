---
name: boundaries
description: Component seams and dependency direction per Clean Architecture — apply when adding a component, service, or layer; when deciding what depends on what; when framework/DB/transport details are about to leak into core logic; or when a change is rippling across modules. Triggers on boundaries, dependency direction, layering, coupling, where does this belong, circular dependency, dependency inversion, component design.
---

# Boundaries — dependency direction and where to cut

Design decisions that must not leak are the reason components exist. A boundary is worth
drawing where **change arrives at different rates or for different reasons** on each side.
Everything here is applied at design time; a boundary retrofitted after the ripple has
already spread costs an order of magnitude more.

## The Dependency Rule

Source dependencies point **inward**, toward policy and stability, never outward toward
detail. Concretely, for any import you are about to write:

- Does policy (business rules, orchestration logic, domain state) now know about a
  detail (framework, DB driver, HTTP shape, CLI runtime, file layout)? If yes, invert it.
- **Invert via an interface owned by the inner side.** The core declares what it needs;
  the outer layer implements it. An interface owned by the outer layer is not inversion,
  just indirection.
- The dirtiest component is the entry point (main/bootstrap/wiring). It knows everyone;
  no one knows it. If wiring knowledge is spreading beyond it, pull it back.

## What counts as a detail

Database, ORM, web framework, message transport, file format, CLI/agent runtime, cloud
service, UI toolkit. All are **plugins to the policy**, not foundations of it. Test: could
this be replaced by a different vendor without editing domain logic? If not, the boundary
is missing or pointed the wrong way.

- Keep external shapes (API payloads, DB rows, wire envelopes) out of core types.
  Translate at the edge, in one place, in both directions.
- A domain type carrying a vendor field name is a boundary breach already in progress.

## Where to cut

Cut where change rate or change reason differs:

- Different **actors** ask for changes → different components (one component, one reason
  to change).
- Different **release/deploy cadence** → boundary.
- Different **volatility** → boundary; stable things must not depend on volatile things.
- Same reason, same cadence, same actor → **do not cut.** Premature boundaries buy
  indirection and pay in navigation cost.

Boundary strength is a spectrum — pick the cheapest that holds: a module and interface, a
package, a process, a service. Start at the left; move right only when a concrete force
(deploy independence, scaling, team ownership, failure isolation) demands it. A network
call between two things that always change together is a distributed monolith.

## Component coupling checks

- **No cycles.** If A → B → C → A, break it by inverting one edge or extracting the shared
  reason into a fourth component. Cycles make every release a joint release.
- **Depend toward stability.** A component with many dependents must change reluctantly;
  if it changes often, its dependents pay every time. Stable + volatile in one component
  is a split waiting to happen.
- **Abstract as you stabilize.** The more depended-upon a component is, the more its
  surface should be interfaces rather than concretions.
- **Release together, live together.** Things released as a unit, reused as a unit, and
  changed for one reason belong in one component.

## Red flags

| Red flag | What it means | Move |
|---|---|---|
| Core imports framework/driver | Dependency Rule inverted | Declare the port in core; implement outside |
| One logical change touches N components | Boundary in the wrong place | Redraw around the change, not the nouns |
| Import cycle | Components are one component | Invert an edge or extract the shared reason |
| Vendor names in domain types | Detail leaked inward | Translate at the edge |
| Every feature edits the same "shared/utils" | Missing cohesion, not shared code | Split by reason to change |
| New service for code that always co-changes | Distributed monolith | Keep it in-process until a force demands otherwise |

## Verifier gates

- No new import from a policy module to a framework/driver/transport module.
- New interfaces are declared by the consumer (inner) side, not the implementer.
- No new import cycles between components.
- External payload shapes do not appear in domain types or function signatures.
- A new process/service boundary names the force requiring it (deploy, scale, ownership,
  isolation) — "cleanliness" is not a force.
