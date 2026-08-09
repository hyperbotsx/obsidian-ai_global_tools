---
name: design-core
description: Always-on design doctrine distilled from A Philosophy of Software Design, Clean Architecture, Fundamentals of Software Architecture, and DDIA — the rules that shape code while it is being written, not fixed in review. Use when implementing anything non-trivial, or when asked for design-core, design doctrine, write-it-right rules.
---

# Design Core — write it right the first time

Portable canonical copy. Once adopted, the worktrees `CLAUDE.md` carries the same section
for auto-loading — **update both together**. Complexity arrives incrementally, through
small "just this once" decisions; these rules are applied while designing and typing,
never as a post-hoc checklist. Depth on demand: `deep-modules` (module/interface design) ·
`boundaries` (component seams) · `arch-tradeoffs` (style selection, ADRs) · `data-design`
(storage/replication/consistency).

## Modules and interfaces

- **Deep over shallow.** A module's value = functionality hidden ÷ interface exposed.
  Before adding a class, function, or config knob ask: does this deepen an interface or
  just add surface?
- **The deep-module test on every change:** did an interface get simpler or wider?
  Wider needs a stated reason.
- **Split only on information-hiding seams.** Never split cohesive logic to satisfy a
  size number — scattering one state machine across files is complexity, not simplicity
  (this is the house KISS escape hatch, applied at write time).
- **Somewhat-general beats special-purpose.** Design the interface for the class of
  problem; implement only today's case.
- **Define errors out of existence.** Prefer semantics where the error case cannot occur
  over throwing and handling. Every exception you don't create is interface you don't have.
- **Pull complexity downward.** The module author absorbs difficulty so every caller
  doesn't; a simple implementation behind a complex interface is backwards.

## Dependencies and boundaries

- **Dependencies point toward stability.** Business logic never imports frameworks,
  IO details, or transport shapes. Details depend on policy, never the reverse.
- **The inner side owns the interface.** Keep external data shapes (API responses, DB
  rows, wire formats) out of core types; translate at the boundary.
- **Defer detail decisions.** Storage, transport, and framework choices sit behind a
  seam until they must be made — a decision not yet taken cannot be wrong.

## Change amplification and trade-offs

- **Name the trade before writing.** What future change does this design make cheap, and
  what does it make expensive? An option without a stated cost is analysis not yet done.
- **N-place changes reveal missing modules.** If one logical change will touch N places,
  stop — that is the design showing you where the module boundary should be.
- **Record the why where the next reader looks** (FRD, PR body, or a one-line decision
  note). The why outlives the how.

## Data

- **State is the hard part.** For any new persistent state, name the write path, the
  read path, and the concurrent/partial-failure behavior before writing code.
- **Schemas evolve additively.** Never break old readers silently.

## Working code is not enough

Tactical "just make it work" is how complexity accumulates. Leave every touched design
slightly better, or state explicitly why not. The review standard is whether the change
left the system easier to change — hold your own diff to it before anyone else does.
