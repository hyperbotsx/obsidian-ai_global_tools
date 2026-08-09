# Modula Agent-Comms Contract — requirements (harvest)

Status: draft v1 · 2026-07-28 · owner: Erik + Lead
Source: hard-won on the **E0 #355** trio run. The trio (Lead / Coder / Verifier / Git-Manager) **is** Modula's reference workflow, so these are **product requirements for Modula's agent-to-agent comms layer** — not one-off fixes for one session. Every future trio/agent-team session must inherit them.

Related: `frd-agent-activity-ledger-draft.md`, `frd-review-fix-controller-draft.md`, E0 Lead runtime FRD (#355).

## Guiding principle

**Every blocking wait must have a guaranteed answerer.** No agent ever blocks on a party that might not reply. Map every `await` to someone who always answers (the hub, or a responder contractually required to reply), or make the wait loop until answered.

## Requirements

- **R1 — Durable inbound queue, drain at own pace.** Inbound requests queue durably; a busy recipient drains them when free. A late pickup must **never lose** the message. (Failure seen: the Lead was mid-writing while a coder request sat unqueued/unpicked; only luck + loop-await saved it.)
- **R2 — No reply-loss on timeout.** A reply to a wait that already timed out must **not be silently discarded** — it lands in the recipient's queue, or waits loop until answered. (Failure seen: `coms_respond` to a timed-out `coms_await` vanished; the coder reported "reply timed out, blocked" and the Lead's carefully-written answer was lost.)
- **R3 — Loop-await.** A requester re-awaits across timeouts; **one timeout ≠ blocked**. Never conclude "failed" after a single expiry.
- **R4 — Wake idle agents programmatically.** Idle turn-bound agents must be wakeable by prompt/socket injection that **starts a new turn** — not only by a human poke. (Failure seen: a `coms_send` to a fully-idle codex agent queued unheard; only a manual pane poke or the inert pi-coms-local socket could wake it.)
- **R5 — No orphaned-send channel-lock.** An unanswered outbound must not permanently block the sender's ability to send. Provide cancel, or auto-expire that frees the channel. (Failure seen: a superseded outbound held the Lead's single send-slot until TTL.)
- **R6 — Dual reporting through the hub.** Review verdicts go to **both** the requester (coder — to unblock its wait) **and** the Lead (visibility) — never one *instead of* the other. (Failure seen: verifier set `next_actor:coder` and reported only to disk → Lead blind; then "report to Lead instead of coder" → coder's wait dead-ended. Both-and is the fix.)
- **R7 — Disk-authoritative status.** Durable, machine-readable status artifacts (handoff + verifier-report machine-status block) are the source of truth; the hub drives off them (watchers/Monitors), not fragile in-band replies.
- **R7a — Active inbox drain (the hub must be alerted to pending inbound).** A hub that only drains its inbox when it happens to act will leave peers blocked (seen repeatedly: a coder escalation queued unheard while the Lead was watching disk or reporting). The coms registry exposes `queue_depth` per agent on disk (`.../agents/<name>.json`) — the hub runs a persistent Monitor on its own `queue_depth` and drains+responds the instant it goes above 0. Inbound-draining must be an automatic, monitored signal, exactly like checkpoint outcomes — not a thing the hub remembers to do.
- **R8 — Context-renewal, full loop, CLI-AGNOSTIC.** Agents detect their budget (thresholds ~70% prepare / 75% renewal / 80% hard-stop), **auto-write a continuation summary before hard-stop**, and **auto-continue in a fresh session** (detect → summarize → relaunch → resume from the summary). No silent death at the window limit. (Failure seen: the coder ran silent to its window and froze mid-checkpoint; the pi `AGENTOPS_CONTEXT_RENEWAL` extension supplies only the detect+signal half — Modula must supply relaunch+resume automatically.) **Modula is CLI-modular** (Claude CLI, opencode, roo, codex/pi …), so renewal must live at the **orchestration/runner layer**, not a per-CLI extension: a per-CLI adapter for the usage/detect signal + one common summarize→relaunch→resume driver. Note the per-CLI reality: Claude Code auto-compacts natively (the Lead relies on this); codex/pi hit a hard window; opencode/roo TBD (research — see the CLI-agnostic-renewal task). Continuity survives renewal because state is disk-authoritative (R7): FRD, verifier-report, task list, memory — not just in-context.
- **R8a — Auto-compaction is the worst-case fallback and MUST resume, not dead-end.** If the summarize→relaunch renewal (R8) does not fire, in-session auto-compaction (pi/Claude free context without a new session) is a valid last resort — but the agent, and anyone waiting on it, must not freeze after compacting. Detect the sharp same-session context drop and steer-resume the compacted agent; compaction preserves the summarized task, so it continues in place. (Failure seen: the verifier auto-compacted mid-review and stopped; the coder got no response and dead-ended. Renewal is the clean path; compaction+resume is the guaranteed floor.)
- **R9 — Hub drives via respond + disk, minimizing held sends.** The Lead orchestrates through `coms_respond` (needs no send-slot) and disk watchers; its single send-slot must never be the workflow bottleneck.

## Component mapping

- **Comms layer** (comsAdapter / comsWire): R1, R2, R3, R5, R9.
- **Lead runtime** (E0 / #355): R6, R7, R9 — Lead as always-present hub.
- **Renewal**: R8 — `pi-packages/agentops-context-renewal` (detect) + a relaunch/resume driver (to build).
- **Wake**: R4 — pi-coms-local socket injection + `scripts/agentops/watch-*.py` auto-drivers (present but were inert; must be live by default).

## Acceptance (behavioral)

A team of turn-bound agents runs a multi-checkpoint job **with zero manual pokes and zero lost messages**: agents that fill their window renew themselves and resume; idle agents are woken programmatically; every escalation is answered; verdicts reach both the coder and the Lead; no wait ever dead-ends.
