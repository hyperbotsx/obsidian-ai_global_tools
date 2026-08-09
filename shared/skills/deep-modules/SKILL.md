---
name: deep-modules
description: Module and interface design per A Philosophy of Software Design — apply while creating or reshaping a module, class, API, service surface, or config knob; when deciding whether to split or inline; when a diff widens an interface; or when running a deep-modules review. Triggers on new module, API design, interface design, deep modules, split this file, extract a helper, add a config option, interface review.
---

# Deep Modules — interface design that hides complexity

The unit of design is the interface, not the file. A module (function, class, service,
config surface) is **deep** when a small interface hides substantial functionality, and
**shallow** when its interface is large relative to what it does. Shallow modules add
complexity instead of hiding it: every caller pays the interface cost forever. Apply this
at write time — the cheapest moment to fix an interface is before it has callers.

## The core test

Before and after any change that touches a public surface, answer:

1. **Did an interface get simpler or wider?** Wider requires a stated reason in the PR.
2. **What does the caller no longer need to know?** If the answer is "nothing", the
   module is packaging, not abstraction.
3. **Interface = everything a caller must know** — signatures, ordering constraints,
   error cases, performance cliffs, side effects. Undocumented obligations are still
   interface, just hidden interface.

## Red flags → fixes

| Red flag | Symptom | Fix |
|---|---|---|
| Shallow module | Interface restates implementation; wrapper adds a name, not a secret | Inline it, or deepen it by absorbing caller-side logic |
| Classitis / helper sprawl | Many one-call helpers whose names restate their bodies | Inline; split only where a secret (design decision) can be hidden |
| Information leakage | One design decision (format, protocol, layout) known by ≥2 modules | Move the decision into one module; others call, never assume |
| Temporal decomposition | Structure mirrors execution order (`readFile`, `processFile`, `writeFile` sharing format knowledge) | Structure around knowledge: one module owns the format end-to-end |
| Pass-through method | Method forwards to another with the same signature | Delete a layer, or make the layer add real behavior |
| Pass-through variable | Argument threaded through N functions that only relay it | Carry in context owned by the module chain, or restructure |
| Conjoined methods | Understanding A requires reading B | Merge, or redraw the boundary so each stands alone |
| Config-knob export | Hard decision punted to the caller as an option | Decide. Compute a sensible default; expose a knob only for genuine caller-varying policy |
| Special-general mixture | General operation with special-case parameters for one caller | Keep the operation general; the caller adapts at its own edge |

## Interface design rules

- **Make the common case trivial.** The 90% call should need no options, no setup
  ceremony, no cleanup obligations. Complexity belongs to the rare case.
- **Somewhat-general-purpose.** Design the interface for the class of problem, implement
  today's case. Test: would a plausible second caller use it unchanged? Special-purpose
  interfaces multiply; general ones deepen.
- **Define errors out of existence.** Redefine semantics so the error case is a no-op or
  a normal result (delete-nonexistent succeeds; out-of-range selects nothing). Exceptions
  that remain are genuinely exceptional — crash-worthy or caller-decidable, nothing between.
- **Pull complexity downward.** When difficulty must exist, put it inside the module —
  the author pays once, callers pay never. An interface exporting its implementation's
  awkwardness (retry loops, ordering rules, cleanup protocols) is upside down.
- **Different layer, different abstraction.** Adjacent layers exposing the same
  vocabulary means one of them isn't earning its keep.

## Split or merge

Split when two **independent secrets** live in one place — each new module hides a
decision the other never needs. Merge (or never split) when:

- the pieces share information (a format, a protocol, an invariant),
- they are always read together to be understood,
- the split would create pass-throughs or a conjoined pair,
- the only motive is a size number — the house KISS limits are review triggers with an
  escape hatch, not decomposition commands. Say "exceeds default, cohesive because X,
  seam when Y" in the PR and keep the module whole.

## Comments are part of the interface (house reconciliation)

House rules stand: no what-comments, naming first, <5% density. Within that, the
**interface contract comment is a permitted why-comment** on public seams: what the
caller must know that the signature cannot say — units, ordering, error semantics,
performance cliffs, invariants. If naming cannot carry it, a two-line contract at the
declaration beats every caller rediscovering it. Never narrate implementation.

## Verifier gates (same doctrine, checked)

- Any widened public interface has a stated reason in the PR.
- No new wrapper whose body is one call with the same signature (pass-through).
- No design decision (format/protocol/layout) asserted in two modules.
- New options/knobs: show the caller that varies; otherwise a computed default.
- Split files: each side names the secret it hides; no conjoined reading order.
- Error paths: list the error cases the design removed vs merely handles.
