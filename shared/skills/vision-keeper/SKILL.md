---
name: vision-keeper
description: Prevent architecture/vision drift in long agent sessions — a read-only audit that re-reads the live specification (PRD, FRD, ADRs) before major decisions and returns ALIGNED, CONTRADICTS (with citations), or AMBIGUOUS. Use before adding a component or service, changing a dependency, making a structural choice, or touching a load-bearing subsystem. Language- and app-type-agnostic.
---

# Vision-Keeper

Over a long session an agent loses sight of the architecture — context compaction, recency bias,
firefighting — and proposes changes that are technically sound but strategically misaligned. This
skill keeps the plan's load-bearing commitments in view and checks decisions against them before
they ship, not after.

It never writes code. Its only output is a **verdict**.

## When it runs

Before a **major** decision — not every edit:

- adding a component, service, module, or layer
- changing or adding a dependency
- a structural choice with real trade-offs (storage, transport, boundary, data model)
- touching a subsystem the project marks load-bearing (paths listed in `audit.yaml`)

Cheap keystone decisions get a fresh look at the spec; routine edits do not pay the cost.

## How it reads

On **every** invocation it re-reads the **live** specification — the master PRD, the relevant
FRD, and the ADR directory — never a remembered version. The guardrail reflects current intent,
so when intent evolves the spec updates first; the audit is never patched with exceptions.

## The verdict

- **ALIGNED** — the decision is consistent with the spec. Proceed.
- **CONTRADICTS** — the decision reverses a stated Goal / Non-Goal / commitment. Cite the exact
  spec line. This is a stop-and-reconcile, not a soft note.
- **AMBIGUOUS** — the spec is silent or unclear. This is productive, not a dead end: it becomes an
  **ADR or amendment proposal** (through the project's §3 amendment pipeline) so the decision is
  recorded and the spec is sharper next time. AMBIGUOUS never silently resolves itself.

## Read-only, and how it runs across harnesses

The audit uses read tools only — Read / Grep / Glob — and **cannot write**. It runs as an isolated
read-only pass so its context is just the spec and the decision under review.

- Where the harness supports an isolated read-only sub-context (Claude `context: fork` with
  read-only tools), run it there.
- Where it does not (Pi and others), run the **same audit inline** as a bounded read-only step.

The isolation is a performance/hygiene preference, never a correctness dependency — the verdict is
identical either way. (Same fork-optional/inline-fallback rule as the STRIDE step.)

## Load-bearing commitments

A companion to the verdict: keep 3–8 load-bearing commitments — the ones whose reversal would
change the project — visible across the session. Reversing one is the definition of a CONTRADICTS.
These are the spec's commitments specifically; the general doctrine re-injection is
`enforcement-hooks#reinject-doctrine`.

## As the operator / lead

Invoke before the keystone decisions above, or list their triggers in project config so the engine
raises the audit automatically. Treat CONTRADICTS as a gate to reconcile and AMBIGUOUS as a prompt
to write the missing ADR — the point is to make marginal-alignment arguable *before* it ships.

## Notes

- Integrates with the product's own machinery: §3 amendment proposals (AMBIGUOUS → proposal), §6
  PRD/plan reconciliation, and the §7 Context Brief (which already re-reads cited design anchors at
  launch). Vision-Keeper is the *decision-time* check between those launch-time and merge-time ones.
- It audits intent-alignment, not code quality — that is `machine-lint-pack` / `ai-ci-gate-pack` /
  `security-per-pr`.
