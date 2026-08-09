# Agent Wake + Renewal Auto-Resume Driver — build spec (harvest)

Status: draft v1 · 2026-07-28 · owner: Erik + Lead
Source: deep investigation during E0 #355 CP-3 (9 revisions, a manual poke/renewal per chunk). This is the permanent fix for the process pain. Implements R4 (wake) + R8 (renewal) of `frd-agent-comms-contract-draft.md`. Ties to task #3 (CLI-agnostic renewal) and the Z4 runner split.

## The problem
Turn-bound codex agents (coder/verifier) needed a manual pane poke to (a) wake from idle and (b) actually WORK (not just ack), and a manual re-brief on every context renewal. Across CP-3 this was the dominant cost — the engineering converged fine; the process didn't.

## Mechanism findings (verified in `@giovani-junior-dev/pi-coms-local/extensions/coms.ts`)
- Each session listens on a unix socket at `$PI_COMS_DIR/sockets/<sessionId>.sock` (for the trio: `/tmp/agentops/coms/<pool>/sockets/<sessionId>.sock`). Sockets DO exist per live session.
- Inbound delivery: a `PromptEnvelope` → `handlePrompt()` → `pi.sendMessage({content: "[from <sender> @ <cwd>]\n\n<prompt>"}, {deliverAs:"followUp", triggerTurn:true})`. So an inbound coms message **does** trigger a turn — but framed as a **peer message**.
- **`coms_send` already uses exactly this path.** There is no separate, unused "steer" socket to exploit.
- **The real gap:** peer-framed `followUp` → agents tend to ACK; direct user input (`deliverAs:"steer"`, what a pane poke effectively is) → agents WORK. The current socket only exposes `followUp`.
- Why the existing auto-drivers are inert: `scripts/agentops/watch-*.py` target `/tmp/agentops/pi-<role>-<worktree>.sock` with `{message,deliverAs}` — WRONG path AND wrong format for the current extension (which wants a full `PromptEnvelope` at the per-session path). Both must be updated.

## Design
**Part A — wake-into-work (steer endpoint):** add a `steer` handling path to `pi-coms-local` (or find pi's user-injection API) that calls `pi.sendMessage(<prompt>, {deliverAs:"steer", triggerTurn:true})` — i.e. deliver an injected prompt as a direct USER instruction, not a peer message. Expose it via the per-session socket (new envelope `type:"steer"`) so a lead-side helper `agentops-steer <sessionId> <prompt>` can wake an idle agent into a real work-turn. Blast radius: shared extension — must be tested; keep the peer-`followUp` path unchanged for normal coms.
**Part B — auto-resume:** a watcher (server/runner-side) keyed on the context-renewal signal (`AGENTOPS_CONTEXT_RENEWAL` state → `renewal-needed`/`hard-stop`) or the continuation file: on renewal, (1) the spent agent has already written its continuation (detect+summarize is done), (2) the driver launches the fresh session **seeded** with "read <continuation> + resume" — via the wrapper's initial prompt or a `steer` to the fresh session's socket. No manual re-brief.
**Part C — auto-compaction fallback (worst-case, self-healing):** pi ALSO auto-compacts near ~100% (frees context in-session) but leaves the agent STOPPED, so anyone waiting on it dead-ends. Detect a sharp SAME-SESSION context drop (registry `context_used_pct` fell hard, `session_id` unchanged) → `steer`-resume the agent; compaction preserves the summarized task, so it continues where it left off — no continuation file needed. Net: renewal (summarize→fresh→seed) is the clean path; auto-compaction (compact→steer-resume) is the guaranteed fallback.
**CLI-agnostic — per-CLI adapters on TWO axes (task #3):** (a) DETECT how-full — pi: `AGENTOPS_CONTEXT_RENEWAL` / registry `context_used_pct`; Claude Code: native; opencode/roo: TBD. (b) CLEAR/RENEW ACTION, DIFFERENT per CLI — pi: `/new`+`/reload` (execution-window hard-stop) or auto-compact (context window); Claude Code: native compaction / a different new-chat command; opencode/roo: own. The runner must issue the CLI-specific clear/new command PROGRAMMATICALLY via the pane host (tmux `send-keys` / herdr pane API) — that issuance is the ONE piece not yet built. Note pi has TWO limits: context window (auto-compacts, no `/new`) vs execution window (hard-stops, needs `/new`).

**Status (E0 #355, validated live):** Part A (steer wake-into-work) DONE + proven on git-manager/coder. Part B detect + steer-seed and Part C detect + steer-resume DONE on the Lead side (renewal + compaction both observed live). Only the runner-side programmatic `/new`+`/reload` issuance remains.

## Recommendation
Build + TEST as a focused effort — a flaky wake driver is worse than a manual poke. Validate Part A empirically (steer a live idle session → confirm a real work-turn) before wiring Part B. Start with the pi-coms-local steer endpoint (bounded, testable), then the renewal watcher.
