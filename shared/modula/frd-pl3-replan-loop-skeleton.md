# FRD (skeleton) — PL3: Replan Loop + Unprompted Proposals (P-3)

Status: **skeleton, not a spec** · 2026-07-25 · author: lead (Fable 5)
**Blocked by #293 (PL2).** Do not expand into a spec until PL2 lands — §4.1 is deliberately a hole, because
PL2 owns the plan object this feature diffs against. Filling it now would be guessing.
Brief anchors: 02-planner §2.5 (replan flow) · §3 (replan chip) · §5 (trigger watcher) · §9.1 (unprompted proposals).

## 1. Problem

PL1 shipped a Planner that only speaks when spoken to, and PL2 gives plans a versioned object with waves and
activation. Neither notices when the world moves. FRDs land, gates resolve, waves drain — and the active plan
silently becomes the wrong plan. Today the only path back is the operator remembering to ask.

## 2. Goals

- **Replan trigger watcher** — count FRDs created/approved since the active plan version; expose chip state;
  hand the Planner the delta set.
- **Replan chip** in the board toolbar: `⟳ Replan? · 2 FRDs since last plan`, amber/mono, matching the renew chip.
- **Delta proposals** — the Planner diffs new/changed FRDs against the current plan and proposes adjustments
  *as a delta* ("insert #260 into slot 2 after #212; push #256 to Wave B"), through the PL1 proposal contract.
- **Unprompted proposals** (brief 02 §9.1 — operator already decided yes) with the full F3 fan-out: chat
  unread pulse, Needs-you card, Activity entry, email per user notification settings.
- **Never interrupt running work.** A mid-wave replan re-orders only what has not started.

## 3. Non-goals

- Does not create or author FRDs, and does not approve them.
- Does not activate waves — activation remains PL2.
- Proposals never self-approve. They wait, indefinitely, without nagging.

## 4. Design

### 4.1 Plan-object interface — **HOLE, owned by PL2**

Everything below needs answers PL2 will produce. Do not invent them:

- the shape of the versioned plan object (waves, slot assignments, per-FRD team, gates, rationale);
- how "active plan version" is identified, and how v+1 snapshots are created;
- which fields are immutable in an approved snapshot, so a delta knows what it may legally touch;
- how "job has started" is determined, since that is the boundary a mid-wave replan must not cross;
- the receipt/activation seam a delta approval writes into.

When PL2 lands, fill this section from its actual output and *then* expand the rest.

### 4.2 Trigger set (single watcher, shared)

One watcher, consumed by several features — **do not build a second one**:

- N FRDs created or approved since the active plan version;
- a wave drains;
- a gate resolution unblocks queued work.

**#301 (PL6, Plan Reconciliation) consumes this same watcher** for its threshold trigger. Whichever of PL3
and PL6 is built first owns the watcher and exposes it; the other consumes it. Two counters that disagree
about "since the active plan" would be worse than none.

### 4.3 Proposal surface

Reuses the PL1 plan-proposal rendering contract and its Approve/Modify chat acts, rendering a **delta** rather
than a whole plan. Approval creates plan v+1 with receipts; activation stays PL2's call.

### 4.4 Unprompted-proposal notification path

The distinguishing feature versus PL1: the Planner may now speak first. Every unprompted proposal must be
surfaced through all four channels (chat pulse, Needs-you card, Activity entry, email per settings) — a
proposal the operator never sees is worse than no proposal, because the plan silently ages while looking healthy.
Suppression matters: a declined delta must not be re-raised unchanged on the next trigger.

## 5. Phasing (provisional)

- **CP-1** — trigger watcher + chip state, read-only. No proposals.
- **CP-2** — delta proposal + Approve/Modify + receipts (needs §4.1 filled).
- **CP-3** — unprompted proposals + F3 fan-out + suppression.

## 6. Acceptance (provisional)

- A landed FRD raises the chip within the trigger window.
- A delta proposal names concrete slot/wave moves, never a whole-plan rewrite.
- Approving a delta creates plan v+1 and activates nothing.
- A mid-wave replan provably does not touch already-started jobs.
- An unprompted proposal appears in all four notification channels.
- A declined delta is not re-raised unchanged.

## 7. Notes for whoever picks this up

- **Context Brief applies.** This touches `cross-cutting` and `completion-state` surfaces and is medium+
  scope, so it routes to **run** — produce the brief before briefing a coder (see
  `context-brief-phase0-workflow.md`).
- The PL1 run's lesson about stateful surfaces applies to the watcher: distinguish absent from corrupt state,
  fail closed on corrupt, and make counters monotonic independent of rollback.
