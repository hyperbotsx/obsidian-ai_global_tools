# FRD draft: Agent Activity Ledger + Continuation Supervisor (MW-26 + MW-27)

> Draft for the Modula agent-workflow engine. Harvested from live trio/quartet runs; queued by operator
> decision 2026-07-24 ("write MW-26 up as a proper FRD after R1 lands"). R1 (#294) merged 2026-07-26.
> Source requirements: `coder-verifier-workflow/modula-workflow-requirements.md` MW-26, MW-27, and the
> interacting MW-9 / MW-10 / MW-24 / MW-28.

- **Status:** draft (not CEO-reviewed)
- **Date:** 2026-07-26

## 1. Problem

Multi-agent runs stall constantly, and the orchestrator cannot tell the difference between an agent that
is working, one that has stopped, one that is blocked inside a tool call, and one whose memory has been
erased by compaction. Today a human lead diagnoses this by hand — sampling `/proc` CPU deltas, listing
child processes, and reading working-tree changes — which is minutes-latency, inference-based, and
demonstrably wrong at the moments it matters most.

Measured cost on two runs:

- **prd-294**: three separate stalls, one burning ~25 minutes; a coder wedged **14.3 hours** inside a
  single tool call at 0.00 CPU; a second wedge of 51 minutes; a compaction that silently ended a task.
  The operator noticed the idle trio before the lead's own polling concluded — twice.
- **prd-283**: the same stall pattern recurred **3× within one checkpoint**, and a fresh coms heartbeat
  was mistaken for a live agent twice.

The failure is not that agents stall. Turn-based runtimes stall by design. The failure is that stalling
is **undetectable, unattributable, and unrecoverable** without a human.

## 2. Goals

1. **Make agent state observable in seconds, deterministically** — not inferred from CPU in minutes.
2. **Distinguish four states that currently look identical from outside**: WORKING, IDLE-DONE,
   IDLE-STALLED, BLOCKED-IN-TOOL.
3. **Auto-recover the two recoverable ones** — re-drive the stalled, kill-and-report the wedged.
4. **Survive context loss** — an agent that compacts must resume from durable state, not from guesswork.
5. **Never destroy a healthy agent** on a bad diagnosis.

## 3. Non-goals

- Not a replacement for the verifier or any review gate.
- Not a scheduler; it observes and re-drives, it does not decide what work happens.
- No changes to model selection, role prompts, or checkpoint structure.

## 4. Design

### 4.1 Per-agent activity ledger

Each agent's runtime wrapper writes its **own** append-only ring file (tmpfs, last few minutes,
~2k lines). Per-agent files, never a shared log — no locking, no write contention.

Events, emitted **by the harness**, not by the agent:

| Event | Meaning |
|---|---|
| `turn_start` / `turn_end` | turn boundaries — the load-bearing signal |
| `tool_call_start` / `tool_call_end` | with tool name and elapsed |
| `in_turn` tick (~2s) | only while a turn is genuinely executing |
| `context_compacted` | compaction/clear/renewal occurred |
| `assignment_open` / `assignment_closed` | directive dispatched / completion reported |

**Why harness-emitted turn events rather than a heartbeat:** a timer-based heartbeat — even a 2-second
one — measures the transport. It stays fresh while the agent's loop is stopped. That is MW-10's
false-alive, just faster. Turn boundaries are events the runtime observes exactly.

### 4.2 Derived states

- **WORKING** — tick < 4s old.
- **IDLE-DONE** — `turn_end`, no open assignment. Correct and ignorable.
- **IDLE-STALLED** — `turn_end` **+ open assignment** → auto re-drive.
- **BLOCKED-IN-TOOL** — `tool_call_start` with no matching end past a bound → kill the call, return an
  error result, surface to the lead.

The join with assignment state is what makes this actionable. "Idle" alone is meaningless — an agent
that finished its work *should* be idle.

### 4.3 Bounded tool execution

Sane default timeouts, explicitly short, per call. A 120,000-second default is not a timeout. Past the
bound: auto-kill, return an error, log it. Role prompts must additionally teach the two traps that cost
prd-294 ~17 hours: never run a server in the foreground, and never pipe a possibly-non-terminating
command through `tee` (the pipe cannot close while any writer holds it open).

### 4.4 Compaction survival

1. **Durable per-agent state file**, run-scoped, written **continuously** — not at checkpoint end —
   holding: current checkpoint, active directive, acceptance criteria, files touched, last completed
   step, single next step.
2. On any context event, the agent's **first action** is to re-read that file plus the canonical spec
   paths.
3. Re-drives after compaction must **RE-ANCHOR, not nudge**: carry the durable-state path and the spec
   paths. A bare "continue" makes an agent that has lost its brief resume from confident guesswork,
   which is worse than a visible halt.
4. **Preempt at a safe boundary** — compact at a threshold the orchestrator picks, between work units
   rather than mid-edit, so state is written first. Same threshold-and-offer mechanic as the
   operator-facing renewal chip, applied to agents.

### 4.5 Acknowledgement as a transport primitive (MW-24)

Free the sender's outbound slot **on delivery**, not on the recipient's reply, and immediately re-drive
the recipient with the directive body. Receipt and execution must not share a turn. Instructing agents
to "ack then work" asks them to do something the runtime forbids — on prd-294 all three roles acked and
went idle, and the one that instead worked without acking held the lead's single outbound slot for its
full expiry, blocking dispatch to a healthy peer.

## 5. Acceptance

- Stall detection latency ≤ 3s from `turn_end`, versus minutes today.
- A wedged tool call is reported as BLOCKED-IN-TOOL, never as a dead agent, and is auto-killed at its
  bound. Replay of the prd-294 14.3-hour wedge must surface within its timeout.
- An agent that compacts mid-task resumes from its state file without human re-briefing.
- IDLE-STALLED auto-re-drives; escalates to the human only after N consecutive re-drives with no
  progress.
- Operator UI shows WORKING / IDLE-DONE / IDLE-STALLED / BLOCKED-IN-TOOL as distinct states
  (extends MW-6).
- No healthy agent is ever recommended for restart on the basis of process-level signals alone.

## 6. Risks

- **Ledger volume** is negligible (3 agents ≈ 1.5 writes/s on tmpfs), but a runaway `in_turn` emitter
  must not fill the ring — cap and truncate on write.
- **Auto-re-drive loops**: a re-drive that itself stalls must not recurse; bound consecutive re-drives
  and escalate.
- **Harness coupling**: turn events require runtime cooperation. If a runtime cannot emit them, that
  agent degrades to today's inference-based detection — which must be labelled as degraded, not
  silently trusted.

## 7. Evidence

Every claim above traces to a logged run. prd-294 (#294): three stalls, a 51,322-second wedge, a
3,112-second wedge, one compaction stall, and a lead that hand-sampled `/proc` throughout. prd-283:
three stalls in one checkpoint, two heartbeat false-alives, MW-12's silent one-way coms loss across
context renewal. Full detail in `modula-workflow-requirements.md` MW-9, MW-10, MW-12, MW-24, MW-26,
MW-27, MW-28.
