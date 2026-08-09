# FRD draft — Lead as a standing peer in the job coms pool

Status: draft, operator-directed, 2026-07-31. Not part of PR #375 (FRD Term-1 #363).
Origin: operator decision during the Term-1 AC-1 dogfood.
Filed as forge issue #391 (type:prd + status:review-needed), 2026-08-01 — canonical target for CEO
review + implementation; folds in fresh evidence from the Term-1 #363 CP-5 run. This vault file is the
working copy.

## Operator statement of intent

> The way the application should be working is the way how we work here. The Lead Developer should be
> part of the pool and conversations go back and forth between the user, me, and the Lead Developer.
> And the Lead Developer coordinates work with the Coder, receives things from the Verifier, sends
> things to the Verifier, like we've been working here.

This is not an analogy. The Lead/Coder/Verifier/Git-Manager loop we run by hand **is** Modula's
reference workflow, and this run executed it end to end. The product does not yet express it.

## What holds today

`leadRuntime.ts:30` builds the Lead with `implementationComs(task.worktreePath, jobId)` — the same
implementation coms pool as the panes — and passes `poolName` into `createPageBotSurfaceRegistry`.
Pool scoping is already designed in and correct.

## What does not hold

The Lead is a **page bot**: a child process spawned per turn to answer the operator, which exits
afterwards. Observed live on the dogfood instance:

- the pool registry contains only `coder.json`, `researcher.json`, `steward.json`, `verifier.json`
- no `lead.json` between turns, and no lead process resident
- a `lead.json` appears transiently *while a reply is being generated*, then goes

Consequence: **traffic is one-way.** The Lead can reach the team; the team cannot address the Lead.
Panes cannot `coms_list` it or `coms_send` to it. It is a spoke presented as a hub.

## Required behaviour

1. The Lead is a **standing registered peer** in the job's implementation pool for the life of the
   job — discoverable via `coms_list`, addressable via `coms_send`, holding a live endpoint.
2. **Bidirectional operator channel.** The operator's messages reach the Lead and the Lead's replies
   reach the operator, as today, without the Lead ceasing to be a peer between turns.
3. **Team → Lead delivery.** Verifier verdicts and coder handoffs reach the Lead as inbound coms, not
   only as files the Lead must be told to read.
4. **Lead → team dispatch.** The Lead addresses named peers directly.

## What we learned running this manually — these are requirements, not anecdotes

Every workaround this run needed is a gap the product must close:

- **Outbound TTL.** Coms messages expired (~5 min) before a busy agent read them, so acknowledgements
  were silently lost. A hub whose dispatches evaporate is not a hub. Delivery must be durable for the
  life of the job, or expiry must be surfaced to the sender.
- **Single outbound slot.** The Lead could not fan out to several peers at once. Hub dispatch is
  inherently one-to-many.
- **Bounded inbound queue.** `inbound capacity reached` was returned repeatedly; agents were told not
  to retry in a loop. Back-pressure must be explicit and recoverable, not a dropped message.
- **Idle agents need a wake.** A queued message is not a work-turn. We needed `agentops-steer` to
  drive idle agents into real turns. The product needs a first-class equivalent.
- **Durable briefs beat chat.** Every instruction that mattered was written to disk and referenced,
  because context is lost to compaction and messages to TTL. Job-scoped durable artifacts are part of
  the protocol, not a workaround.
- **Reporting must not dead-end.** A verifier that reports `next_actor: coder` strands the Lead. The
  hub must be the default recipient of terminal verdicts.

## Lifecycle consequences the operator should weigh

Making the Lead standing changes its cost and failure modes, and these are the real work:

- a long-lived process per job — context growth, renewal, and compaction now matter for the Lead too
  (see the open finding that renewal is enabled yet agents still auto-compact mid-task)
- crash recovery: a dead Lead must be detectable and restorable without losing the conversation, which
  already persists in `lead-history`
- teardown: the Lead must deregister cleanly when the job ends, or pools accumulate stale peers
- cost: a resident model process per active job, not per turn

## Explicitly out of scope here

PR #375 (Term-1) ships launch reliability, session lifecycle, forge and multi-project. This FRD is
separate and must not be folded into it.
