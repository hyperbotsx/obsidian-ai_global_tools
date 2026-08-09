# FRD — Agent Turn Protocol (page-bot envelope, end-of-turn marker, provenance)

**Status:** draft v1 · 2026-08-08 · author: fast-lane session (FRD #391 CP-1) · **awaiting CEO review**
Canonical source once filed: the forge issue. This vault copy is the working draft.
Origin: the requirement set was *empirically generated* by the 11 Kody review rounds + two
adversarial audits on PR #448 (CP-1 residency) — every "Problem" item below is a shipped
finding or a documented residual, not speculation. Receipts:
`qa-receipts/frd-391/cp1-security-audit.md`, PR #448 review dispositions rounds 1–11.

## Intent

Every chat agent surface in Modula (Lead dock, Planner, CEO review, Frontend Expert,
future per-page agents) is a page bot: a child process speaking newline-delimited text
over stdio to a runtime that attributes, persists, and routes its output. Today each
surface speaks an ad-hoc dialect (`lead-message`/`lead-disposition`, planner protocol
lines, free text). This FRD defines ONE turn protocol they all speak, so that
attribution, authority, and trust are properties of the platform — designed once, tested
once — instead of being re-derived (and re-broken) per surface.

## Problem — each item is a paid-for finding from PR #448

- **P-1 No end-of-turn marker.** Output cannot be deterministically attributed to the
  turn that produced it. Consequences shipped as findings: free-text reply
  misattribution across channels, delayed operator replies nearly exposed to pool peers,
  fragile first-line-reply heuristics, kill-on-timeout as the only stale-output defense.
- **P-2 No per-turn provenance.** Authority receipts (`lead-disposition`) are attributed
  by a mutable last-write origin. The confused-deputy forgery residual (Kody rounds
  7/9/10/11, five revisions) is open precisely until output carries the turn it belongs to.
- **P-3 No possession-proof identity.** Wire `sender_name`/`sender_session` are
  self-declared; registry lookup proves existence, not possession (Kody 2399/2407, four
  revisions). Verdict routing in #391 CP-2 must not trust either.
- **P-4 Line framing is the only structure.** Oversized/fragmented lines required three
  rounds of parser hardening (buffer preservation, cap, discard-to-newline) because a
  reply is just "a line" with no length-declared envelope.
- **P-5 Dock turns have no completion signal at all** (the #367 H5 gap): the operator
  channel cannot know when a turn ended, receipts cannot be awaited, and the send queue
  releases on stdin write.
- **P-6 The planner already grew its own protocol** (`pageBotPlannerProtocol`,
  authorization-bound-to-current-turn comment in `pageBotRuntime.ts:23`) — evidence this
  need recurs per surface and should be platform-level.

## Goal

A single versioned turn protocol for all page-bot roles:

1. **Turn envelope.** The runtime delivers each turn as a kind-tagged JSON line carrying a
   runtime-issued `turn_id` (unguessable), `origin` (`operator` | `coms` | `system`),
   and the payload (message, instructing ref, sender identity as verified by the runtime).
2. **Output envelope.** The child emits kind-tagged JSON lines each echoing the
   `turn_id` it answers; the runtime rejects/quarantines output whose `turn_id` is not
   the currently-open turn of that channel.
3. **End-of-turn marker.** The child terminates every turn with an explicit
   `turn-end` line; the runtime uses it to settle waits (coms replies, dock receipts),
   release the per-role send queue (fixes P-5), and close the attribution window.
4. **Authority binding.** Receipts (`lead-disposition` and successors) are valid only
   when their `turn_id` names an `operator`-origin turn — closing P-2 deterministically
   and retiring the outstanding-refs heuristic shipped in CP-1.
5. **Session credential.** Runtime-issued per-session secret delivered out-of-band of the
   registry (env at spawn for children; handshake for pool peers), attached to
   cross-agent payloads so verdict/handoff trust keys on possession (closes P-3 to the
   extent the per-user boundary allows; explicitly NOT cross-user security).
6. **Compatibility.** Protocol version negotiated at spawn (env flag); legacy free-text
   children remain supported per role until migrated, with today's CP-1 quarantine
   heuristics as the documented fallback.

## Failure-mode contract (per fast-lane convergence rule 1)

| Surface | Failure | Behaviour |
|---|---|---|
| turn_id | child echoes stale/foreign id | output quarantined to plain history, surfaced once per turn |
| turn-end | never arrives | existing reply-window timeout applies; child restarted only if no newer turn (write-seq rule) |
| envelope | unparsable/oversized line | discard-to-newline (CP-1 rule), counts against the turn, never settles a wait |
| credential | missing/wrong on cross-agent payload | payload handled as unverified sender (CP-1 labeling), never as the claimed identity |
| version | child predates protocol | role-gated legacy mode; no mixed-mode within one child |
| queue | turn-end lost + timeout | queue releases on timeout with surfaced warning; no permanent wedge |

## Acceptance criteria

1. A turn's output is attributable to that turn by `turn_id` alone, for dock and coms
   channels, under interleaving (pinned with the CP-1 interleave tests ported to the
   protocol).
2. A receipt persists only for an operator-origin `turn_id`; the CP-1 forgery corpus
   (coms-induced, replayed, invented-ref, timed-into-dock-window) all quarantine — with
   the outstanding-refs heuristic deleted, not layered on.
3. Dock sends resolve on `turn-end` (not stdin write); the dock UI can render turn
   completion (H5 closed).
4. A verdict envelope carrying a valid session credential routes as its sender; one with
   a missing/invalid credential is labeled unverified (consumed by #391 CP-2).
5. Planner protocol expressed as protocol kinds on the same envelope (P-6 unified) with
   its existing authorization semantics preserved (its current tests keep passing).
6. Legacy children keep working role-by-role until migrated; enabling the protocol for a
   role is a config/env decision, not a code fork.

## Verifier checkpoints

- CP-A envelope + turn_id round-trip (dock, coms) with interleave pins.
- CP-B end-of-turn settle: queue release, coms reply settle, timeout fallback.
- CP-C authority binding: full CP-1 forgery corpus green without the refs heuristic.
- CP-D credentialed sender: CP-2 verdict flow consumes it end-to-end.
- CP-E planner unification: planner suite green on the shared envelope.
- CP-F legacy fallback: unmigrated role behaves exactly as CP-1-current (pinned).

## Implementation home

- Fence: `term-control-center/server/pageBotRuntime.ts`, `pageBotPlannerProtocol.ts`
  (absorbed), a new `server/agentTurnProtocol.ts`, `leadRuntime.ts`/`leadResidency.ts`
  (first consumer), `rolePrompts.ts`/`qualityLoopPrompt.ts` (child-side contract),
  `scripts/agentops/pi-agent.sh` (env plumbing), tests.
- **Sequencing with #391:** this FRD is CP-2's dependency. Same lane, same single-owner
  files — NOT a parallel lane. Order: CEO review → implement E1 (envelope/turn-end,
  lead-first) → #391 CP-2 consumes it → planner unification (E2) may trail CP-2.
- The five CP-1 carried requirements in the #391 task ledger (end-of-turn marker, signed
  provenance, receipt tags, anti-induction child prompt, coms→dock history) are THIS
  FRD's E1 scope; CP-2 keeps only verdict/handoff semantics.

## Out of scope

Cross-user security (the per-user `0o700` boundary stands), Relay v2 transport rewrite
(this rides the existing wire contract), wake semantics (#391 CP-4), tmux pane agents'
prompt-level protocol (they already follow `delegationPrompts`; converging them onto
these envelopes is a follow-up once page bots are proven).
