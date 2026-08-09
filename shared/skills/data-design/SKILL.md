---
name: data-design
description: Data and state design per Designing Data-Intensive Applications — apply when adding persistent state, choosing a store or queue, designing a schema or wire format, or reasoning about concurrency, retries, replication, and consistency. Triggers on database choice, schema design, migration, replication, consistency, transaction, idempotency, race condition, queue, event log, caching, partitioning, at-least-once.
---

# Data Design — state, consistency, and failure

State is where systems actually break. Before writing code that persists or shares state,
answer four questions in the FRD, PR, or a decision note:

1. **Write path** — who writes, how often, under what concurrency?
2. **Read path** — who reads, how fresh must it be, how much can it tolerate being stale?
3. **Failure behavior** — what happens on crash mid-write, duplicate delivery, or a
   partition? What does a reader see?
4. **Evolution** — how does this schema change without breaking existing readers/writers?

Unanswered, these become production incidents; answered, they usually simplify the design.

## Correctness under concurrency and retries

- **Assume at-least-once delivery.** Anything retried must be idempotent — key writes on a
  stable id, or make the operation naturally repeatable. "It won't retry" is not a property
  of a distributed system.
- **Read-modify-write across a boundary is a race.** Use a transaction, a compare-and-set,
  an atomic operation, or a single owner. Two processes doing read-then-write on one row
  will interleave eventually.
- **Name the isolation you rely on.** Read committed does not prevent lost updates or
  write skew. If correctness depends on serializability, say so and enforce it.
- **Clocks lie.** Never order events by wall-clock time across machines; use sequence
  numbers, versions, or a logical clock. Do not use timestamps for uniqueness.
- **Every network call has three outcomes**: success, failure, and *unknown*. Design for
  unknown — it is the one that corrupts state.

## Choosing where state lives

| Need | Reach for | Cost |
|---|---|---|
| Durable record of truth | Single-writer relational store | Scale ceiling per node |
| Read-heavy, tolerant of staleness | Replica + explicit staleness budget | Reads can go backwards |
| Append-only history / audit | Event log | Replay and compaction discipline |
| Work handoff between processes | Queue with ack + dead-letter | Duplicates, ordering caveats |
| Fast lookup of derived data | Cache with a stated invalidation rule | Stale reads, thundering herd |
| Local process state | In-memory + a restart story | Lost on crash unless persisted |

Rules of thumb: **one writer per piece of state** wherever possible — it eliminates whole
classes of conflict. Derived data must be reproducible from its source; if it cannot be
rebuilt, it is source data and needs the same durability. Add a store only when an
existing one cannot serve the access pattern — polyglot persistence is an operational tax.

## Replication and consistency (only when distributed)

- **Single-leader** is the default: simple, ordered, one place to write. Followers may lag —
  name the staleness budget, and route reads that cannot tolerate lag to the leader.
- **Multi-leader / leaderless** buys availability and pays in conflict resolution. If you
  choose it, write down the conflict rule (last-write-wins loses data; say so explicitly).
- **Read-your-own-writes** is the guarantee users notice first. Ensure it after any write
  a user can immediately observe.
- Do not claim "eventually consistent" as a shrug. State *how* eventual, and what a reader
  sees in the meantime.

## Schema and format evolution

- **Additive changes only** by default: new fields optional with defaults; never repurpose
  or renumber an existing field.
- **Both directions matter.** New readers must handle old data; old readers must tolerate
  new data (ignore unknown fields).
- **Migrations are two-phase**: expand (write both, read old) → backfill → contract (read
  new, drop old). A single-step rename is a rollback trap.
- Persisted data outlives the code that wrote it. Assume every format you write today will
  be read by software you have not written yet.

## Verifier gates

- New persistent state documents write path, read path, failure behavior, evolution.
- Retryable operations are idempotent, keyed on a stable id.
- No read-modify-write across a boundary without a transaction or CAS.
- No ordering or uniqueness derived from wall-clock time.
- Schema changes are additive, or carry an expand/backfill/contract plan.
- Any tolerated staleness has a stated budget, not an implied one.
