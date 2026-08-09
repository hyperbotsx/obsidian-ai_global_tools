# #391 standing-peer — handoff from the #355 audit + E0 base

Purpose: carry everything the #355/E0 work + the coms-reliability audit learned about **standing presence (FR-3 / AC-5 / CP-6 dogfood)** into #391, which now OWNS that scope. Companion to `frd-lead-as-standing-peer-draft.md`. Written 2026-08-01.

> **Read `frd-391-delta-notes-2026-08-08.md` alongside this file.** Three commits landed in #391's
> territory after this handoff was written (`7ece01f`, `0a988c3`, `cce7c7a`) — they fix a socket-path
> bug that sat directly on the standing peer's path, add mandatory socket-safety helpers any new
> registration path must use, and change `leadRuntime.ts`'s dependency shape (so the `leadRuntime.ts`
> line numbers below are stale). That note also carries 2026-08-08 dogfood evidence.

## The cut line
#355 shipped everything EXCEPT FR-3. FR-3 (standing presence), AC-5 (peer message answered without the dock open), and the CP-6 end-to-end dogfood are **carved to #391** and were deliberately NOT built in E0. #391 is the single owner of `leadRuntime.ts` and `comsAdapter.ts` going forward — coordinate any #363/#366/#367 follow-up that would touch either.

## The seam, in current-main code terms
The Lead is a **spoke presented as a hub**: it can reach the team, but the team cannot discover or address it.
- `leadRuntime.ts:30` — the Lead already computes its job pool: `pool = implementationComs(target.task.worktreePath, target.jobId)`.
- `leadRuntime.ts:32,42` — but it only registers a **page-bot surface** (`createPageBotSurfaceRegistry([defaultPageBotSurface('lead','lead')], poolName)`), and sends outbound via page-bot delivery (`:96`, `:212` `runtime.send(...)`).
- It never binds a live **ComsAdapter registry entry + socket** as a peer named `lead` in that pool. So `coms_list`/`relay_roster` from a coder/verifier does not show `lead`, and `relay_dispatch → lead` finds no live entry. Confirmed by the operator's 2026-07-31 dogfood (the pool registers `coder/researcher/steward/verifier`, no standing `lead`).
- `implementationComs`/`controlPlaneComs` are defined in `draftComs.ts:17,21`; how turn-bound peers join the pool: `comsLaunchMode.ts` / `launchPlan.ts` (`PI_COMS_NAME`) — mirror this for a **standing** (not turn-bound) Lead.

**The build, in one line:** give the Lead runtime a standing `ComsAdapter` bound into `implementationComs(wt, jobId)` as name `lead`, drained for the job's lifetime — the transport already supports it; the change lives in `leadRuntime.ts`, not the transport.

## What E0 already landed that #391 stands on (do not rebuild)
- `lead` is a launchable role; job-scoped Lead runtime, dock bound to the live job conversation, per-job history (`conversationStore` scope:`job`), `stateDirFor` seam, disposition receipts, `archiveJob` at closeout. (PR #362, on main.)
- The Lead already knows its job pool path and persists replies to the job key — it just isn't a discoverable peer.

## What the coms-reliability work (PR #365, on main, contract 0.3.2) already gives you
These are exactly the "hub behaviours" #391's goal enumerates — already shipped, lean on them:
- **Per-recipient outbound slots** (L-6): one wedged peer no longer locks the Lead out of the pool.
- **`relay_cancel`** (QW-6): frees a send slot after a peer renewal loses the msg_id — needed for a standing hub that outlives many peer sessions.
- **Inbound self-heal** (QW-10) + **relay_await inbound drain** semantics: the durable-inbox primitive for R1/R7a.
- **Verdict tooling** (`agentops-verdict.py`) + **pool doctor/teardown** (`agentops-trio-doctor.py`/`-down.py`) + **registry implementation stamp** (L-5) + **steer wake** endpoint (QW-3) — discovery, liveness, terminal-verdict routing, idle wake.

## Design rulings already made — #391 inherits, need not re-litigate
From FRD #355 §5R.3 / §7:
- **Wake sources:** (a) a job-pool inbound addressed to `lead`; (b) a dock message. Both wake the Lead.
- **Checkpoint/completion transitions arrive as coms reports** from coder/verifier/git-manager — NOT a separate SessionGroupStatus/completion-bus subscription (explicitly rejected as redundant coupling; additive seam only if dogfood shows silent transitions).
- **Standing presence** exists to close the turn-bound gap where peer requests expire against the coms TTL — the Lead maintains presence for the job's lifetime and drains without a human opening the dock.

## Requirements the standing Lead must satisfy (audit harvest — `frd-agent-comms-contract-draft.md`)
R1 durable inbound · R2 no reply-loss on timeout · R3 loop-await · R4 wake idle programmatically · R5 no orphaned-send lock (done: per-recipient + cancel) · R6 dual reporting through the hub · R7/R7a disk-authoritative + **active inbox drain monitored on `queue_depth`** · R9 respond-over-send so the single send-slot is never the bottleneck.


## Dogfood evidence added 2026-08-08 (Opus 5 Lead, FRD #363 trio run)

Posted in full to issue #391. Summary, because it sharpens four checkpoints:

- **CP-4.** A reply carrying the *complete* assignment still did not schedule a work-turn — the coder
  consumed 20k tokens answering and went idle. Delivering content and scheduling a turn are two
  operations; today only the out-of-band steer does the second.
- **CP-4.** The steer path has **no integrity guarantee**: a shell-quoted payload had backticks
  evaluated, a word was silently stripped, and `agentops-steer` still reported success. A first-class
  wake needs a structured payload and verifiable delivery, not an interpolated command line.
- **CP-3.** `relay_cancel` exists and works — **R5 below is correct, do not reopen it.** The gap is
  discoverability: it is the one verb with no `coms_` alias, so the Lead that needed it never found it
  and routed around the block for a whole run. `autonomyGates.ts:31` already carries a comment saying
  exactly this. Fix = add the alias, or name the remedy in the error text.
- **CP-5.** Registry slots leak across relaunches — this Lead registered as `lead3` with two dead
  predecessors still listed. Teardown must reclaim the canonical name, not increment past it.
- **CP-1.** Residency is runtime-asymmetric: pi panes auto-bind and poll; the Claude verifier registered
  but would not await until a human pasted a standby line. State which runtimes CP-1 covers.

**Correction to an earlier read of mine:** the outbound slot is per-**recipient**
(`comsAdapter.ts:103`), not global. R5's "done" marking is accurate.

## Pointers
- Audit: `shared/modula/coms-reliability-audit-2026-07-29.md`
- Contract: `shared/modula/frd-agent-comms-contract-draft.md`
- Wake/renewal: `shared/modula/frd-agent-wake-renewal-driver-draft.md`
- Runbook: `shared/modula/coder-verifier-workflow/coms-reliability-runbook.md` (monitor/steer/queue/renewal/restart conventions)
- FR-3/AC-5 source text: issue #355 FRD §5R.3, §6 table, §7 FR-3.
