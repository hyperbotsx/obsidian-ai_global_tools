# Trio coms + orchestration loop — reliability audit

Status: v1 · 2026-07-29 · reviewer: distributed-systems audit (operator-requested) · readers: operator + Lead
Scope: stability/reliability only. No architecture changes proposed — the loop works; this hardens it.

Evidence base (all claims grounded here):
- Transport extension: `~/.pi/agent/npm/node_modules/@giovani-junior-dev/pi-coms-local/extensions/coms.ts` (incl. local `handleSteer`)
- Hub coms layer: `term-control-center/server/comsAdapter.ts`, `comsMcp.ts`, `comsTransport.ts`, `comsWire.ts` (worktree agentops-prd-355) + the LIVE build `repos/agentops-harness/term-control-center/build/server/comsAdapter.js`
- Runtime scripts: `~/.local/bin/agentops-steer`, `agentops-trio-{lead,coder,verifier,git}`, `scripts/agentops/pi-agent.sh`, `patch-pi-coms-local.sh`, `watch-verifier-report.py`
- Live state (observed 2026-07-29 ~15:20): `/tmp/agentops/coms/agentops-trio-{e0,pl2,r1}/…`
- Contracts: vault `frd-agent-comms-contract-draft.md` (R1–R9), `frd-agent-wake-renewal-driver-draft.md`, `frd-agent-lifecycle-teardown-invariant.md`, `coder-verifier-workflow/coms-transport.md`
- Run history: `dev-plans/agentops/coder-verifier-workflow/runs/frd-355-lead-runtime/` (CP-3..CP-6 + PR-362 rounds) + a sweep of all sibling run dirs and the MW-N rulebook (`modula-workflow-requirements.md`, `operating-model.md`)

## Verdict

The spine is right and should not change: disk-authoritative artifacts + machine-status JSON as truth, the Lead driving off Monitors, steer as the wake primitive, respond-over-send for the hub. The residual reliability risk concentrates in four places: (1) the TTL fix exists only in one unpushed branch + one build — a rebuild regresses it silently; (2) the steer path is a hand-edit to `node_modules` that nothing protects or logs; (3) lifecycle/teardown hygiene — zombie pools and a duplicate hub are live on this machine right now; (4) Monitor discipline, because Monitors are the Lead's only wake mechanism. Everything below is an incremental change tied to a concrete failure mode.

## What already holds — do not regress

- **Disk-authoritative loop.** Verdict format is contractually pinned as compact JSON (`coms-transport.md:115-134`) and the live `verifier-report.md:3-16` conforms. Dispositions embed a "if you just compacted/renewed" resume block (`lead-cp6-rev8-disposition.md:24-25`) — R8a operationalized.
- **Structural loop-await for the hub.** `comsMcp.ts:8` caps every `coms_await` at 30 s; the Lead physically cannot dead-wait (R3 by construction).
- **At-least-once toward the hub.** An unresponded active inbound is redelivered on every await (`comsAdapter.ts:119`); duplicate inbound msg_ids are rejected (`:183`).
- **Isolation checks on every envelope.** Worktree + pool validation (`comsAdapter.ts:181-182,195,207,226-227`), registry pruning on read (`comsWire.ts:31-37`).
- **The hub transport cannot hang.** 1 s connect/read timeouts (`comsTransport.ts:5,12,44`).
- **Late replies are NOT lost on the pi side.** A response arriving after `coms_await` timed out overwrites the pending result (`coms.ts:683-696`); a coder that keeps polling `coms_get` sees it. R2's real residual windows are narrower: hub expiry amnesia, renewal correlation (below), and behavioral give-up (covered by R3 briefing).
- **The 60-minute expiry + env knob are already live** in the running Lead build (`build/server/comsAdapter.js`: `outboundExpiryMs = 60 * 60_000`, `PI_COMS_OUTBOUND_EXPIRY_MS`). The problem is where that fix lives (QW-1).

---

## Priority 1 — quick wins

### QW-1 · Land the expiry fix on main before anything rebuilds
- **Failure mode.** The dominant historical stall (5-min reply amnesia + completed-reply deletion; contract R2/R5) is fixed only in the unpushed branch `fix/coms-reply-handle-expiry` on the canonical checkout and in its Jul-28 build. Every other source of truth still ships the bug: this worktree has `outboundExpiryMs = 5 * 60_000` (`comsAdapter.ts:12`), `fromEnv()` does not wire `outboundExpiryMs`/`inboundLimit` (`:44-50`), and the same constant re-arms after a reply lands (`:200`) so a completed answer is deleted on the same clock. Any rebuild from main silently reverts the Lead to the old behavior — the worst kind of regression: no error, just 2026-07-26-style stalls returning.
- **Change.** PR + merge the branch now; add a unit test pinning `fromEnv` env wiring; return the canonical serving checkout to main and rebuild. Update the stale "5-minute TTL" references (`frd-355-expanded.md` §5R.3) after landing.
- **Risk/effort.** None/S. **Layer:** app (`comsAdapter.ts`).

### QW-2 · Teardown discipline: zombie pools and duplicate hubs (live today)
- **Failure mode.** Observed now: pool `agentops-trio-pl2` (run finished 2026-07-27) still has **five live agents heartbeating**, including **two live lead comsMcp processes** (pids 906092 + 2997578; `lead.json` + `lead2.json`). Name reservation silently suffixes on collision (`comsAdapter.ts:213-220`; `coms.ts:331-340`), so a relaunched hub becomes `lead2` while every briefed agent still targets `lead` → messages and steers route to the stale hub. Also: 3 dead socket files linger in e0's socket dir (no GC on crash — `coms.ts:1602-1606` cleans only on clean shutdown), and a SIGKILL between name-reserve and registry write leaves an empty `<role>.json` that `comsWire.ts:40-45` skips but never deletes — permanent name shadowing. This is the CLI-side instance of the fail-closed teardown invariant (`frd-agent-lifecycle-teardown-invariant.md`).
- **Change.** (a) `agentops-trio-down <pool>`: SIGTERM every registered pid, wait, remove the pool dir (incl. sockets + invalid/empty registry files); add to the Lead's closeout checklist. (b) Launch-side guard in the wrappers: if `<role>.json` in the target pool has a live pid, refuse with a clear message instead of silently becoming `role2`.
- **Risk/effort.** Low/S (~30 lines total). **Layer:** runtime scripts (wrappers + new script).

### QW-3 · Protect the steer capability from silent loss; give it an audit trail
- **Failure mode.** `handleSteer` — the trio's only programmatic wake path (R4) — exists solely as a hand-edit inside `node_modules` (`coms.ts:663-681`, dispatch `:775-776`). `patch-pi-coms-local.sh` patches **only the model label** (`:34-77`). Any `npm` reinstall/update, cache refresh, version bump past the `@0.1.1` pin (`pi-agent.sh:185`), or new machine silently deletes steer; the loop then reverts to manual pane pokes with no error anywhere. (Verified today: the per-session tmp copies do carry the patch — but that guarantee is accidental.) Separately, steer leaves no trace: `handlePrompt` logs `inbound_prompt` (`coms.ts:651-658`) but `handleSteer` logs nothing, so a lost steer cannot be diagnosed after the fact.
- **Change.** Extend `patch-pi-coms-local.sh` to assert `handleSteer` is present in every candidate copy and **fail the launch loudly** if missing (~5 lines); add a `pi.appendEntry("coms-log", {event:"steer", …})` line to the handler. Full fix is vendoring (L-1).
- **Risk/effort.** None/S. **Layer:** runtime scripts.

### QW-4 · Monitor discipline: treat Monitors as the production alarm system they are
- **Failure mode.** The Lead has **no in-band wake**: the wire accepts only `prompt|response|ping` toward the hub (`comsWire.ts:16-23,49` — the Lead is not steerable), and an inbound to the passive comsMcp only queues. Monitors are therefore the loop's wake mechanism — and they have sharp edges: non-persistent monitors die at ≤1 h; persistent ones die with the session (a Lead restart silently disarms *everything*); over-chatty monitors are auto-stopped; a success-only grep is silent through a crash. Any of these = "event with no watcher" = stalled loop. The operator confirms grep/path fragility already bit one run.
- **Corroboration from run history.** No file in any run dir records monitor patterns or watched paths — the liveness approach exists only at design level (`operating-model.md:92-96`; MW-10 re-drive recipe, `modula-workflow-requirements.md:26,43-52`). MW-10 exists because *"a fresh heartbeat was mistaken for an active agent (twice)"* — heartbeat-based watching false-negatives on a dead agent loop (live instance: `runs/post-r1-parity/lead-independent-evidence.md:88-91`, CPU flat, `queue_depth: 0`, assignment open). A prior monitor also died on its first downstream failure (issue-277: heartbeat sweep scheduler rejected by a single publish error).
- **Change.** Runbook + convention, no code: (1) every loop watcher is `persistent: true`; (2) every filter matches failure signatures, not just the success marker; (3) liveness checks sample **work signals** (CPU delta, live subprocesses, tree changes), never the coms heartbeat (MW-10); (4) on arming, append the monitor's command + purpose to `<run-dir>/monitors.md`; (5) the Lead's restart/renewal ritual starts by re-arming from that manifest; (6) each watcher emits a periodic heartbeat line so "no events" is distinguishable from "watcher dead".
- **Risk/effort.** None/S. **Layer:** Lead runbook + run-dir convention (this is R7a/R8a + MW-10 operationalized).

### QW-5 · One machine-status extractor; retire the drifted validators
- **Failure mode.** Three format authorities disagree today: the contract pins compact JSON incl. `needs_lead` (`coms-transport.md:119-133`); the live report conforms (`verifier-report.md:3-16`); but `watch-verifier-report.py:18-37` validates a **bullet-line Title-Case format** without `needs_lead`, and `shared/completion.ts` lacks `needs_lead` entirely (`frd-355-expanded.md` §2). Lead monitors meanwhile use ad-hoc greps. Format drift + hand-rolled greps = false-positive/negative watchers — the exact class that already bit.
- **Change.** A ~40-line `agentops-verdict <verifier-report.md>` script: extract the fenced JSON block, validate enums (reuse the value sets from `watch-verifier-report.py`), print normalized fields, exit non-zero with a reason on malformed/missing. Lead monitors and dispositions call it instead of grepping; the contract doc names it as the reference parser.
- **Risk/effort.** Low/S. **Layer:** runtime scripts + contract doc.

### QW-6 · Add a cancel primitive for the single outbound slot (R5) — and it must not require the msg_id
- **Failure mode.** The single in-flight-send rule is contractual (`coms-transport.md:103`) and stays. But the slot is freed only by a reply (`comsAdapter.ts:201`), expiry (`:242-251`), or send-throw (`:96`) — there is **no cancel tool** (`comsMcp.ts:24-31`). This already produced a documented hour-long wedge: `runs/post-r1-parity/lead-independent-evidence.md:93-98` — raising the TTL to 60 min *"fixed the lost-reply failure but lengthened the wedge: one stalled peer now locks the lead out of the entire pool for up to an hour, with no way to clear it — the msg_id died with the prior session's context, so coms_get cannot reach it."* That last clause is the design constraint: after a Lead renewal the msg_id is gone, so a `{msg_id}`-only cancel cannot clear the slot.
- **Change.** Expose `adapter.forgetPending()` as `coms_cancel {msg_id?}` — with no argument it clears the current outbound slot (there is exactly one: `outboundId`). ~12 lines adapter + mcp; bump `COMS_MCP_CONTRACT_VERSION`. Renewal checklist: on peer renewal, cancel and re-dispatch (see L-3).
- **Risk/effort.** None/S. **Layer:** app (`comsAdapter.ts`/`comsMcp.ts`).

### QW-7 · Steer confirmation + idempotency convention
- **Failure mode.** A steer ack means only "the injection API didn't throw" (`coms.ts:672-680`) — not that a work-turn ran. Silent-loss windows: steer lands as the target renews (socket acks, session dies before the turn); steer lands mid-turn and derails in-flight work; a retried steer double-fires (no dedupe — each envelope is its own injected turn). `agentops-steer` resolves the registry endpoint with **no staleness check** (`agentops-steer:28-37`), so it happily steers a stale-but-alive predecessor session.
- **Change.** Convention + 3 lines of code: every steer prompt carries a revision token and instructs the agent to update the corresponding disk artifact (handoff/report) — the Lead's existing Monitor is the delivery confirmation; re-steer only after N minutes of no disk evidence, with the **same** token so a duplicate self-identifies as stale ("if rev-N already handled, ignore"). In `agentops-steer`: warn when registry `heartbeat_at` is older than ~90 s or `session_id` doesn't match the socket filename.
- **Risk/effort.** None/S. **Layer:** steer CLI + Lead runbook.

### QW-8 · Wrapper env hardening: shared pool default + git-manager renewal parity
- **Failure mode (a).** All four wrappers default `PI_AGENT_COMS_PROJECT` to the literal `agentops-trio` (`agentops-trio-coder:3`, `-verifier:3`, `-git:5`, `-lead:7`). Two concurrent runs that forget the env share one pool: cross-run sends, steers, and name collisions (the strict-isolation break documented on PL2; `~/.claude.json` still carries an old shared-pool registration). `pi-agent.sh:164` already defaults to the worktree name — the wrappers override the safer default.
- **Failure mode (b).** `agentops-trio-coder:4` and `-verifier:4` set `AGENTOPS_CONTEXT_RENEWAL=1`; `agentops-trio-git` does **not** — the equally turn-bound git-manager can run silent to its execution window mid-rebase/PR round and freeze with no prepare/renewal signal (exactly the R8 failure the other two are protected against).
- **Change.** One line each: default the pool to `agentops-trio-$(basename "$(git rev-parse --show-toplevel)")` (or refuse to launch when unset), and add `AGENTOPS_CONTEXT_RENEWAL=1` to the git wrapper.
- **Risk/effort.** None/S. **Layer:** wrappers.

### QW-9 · queue_depth signal hygiene (phantom depth is real, observed now)
- **Failure mode.** On the pi side, an inbound is cleared only when a turn-end answers the **newest** unfulfilled entry (`coms.ts:1502,1566-1567`); older/superseded entries linger forever. Observed now: the idle e0 verifier reports `queue_depth: 1`. The R7a drain-monitor ("alert when >0") then either cries wolf forever or trains the Lead to ignore it — alarm fatigue that masks a real escalation. Also, a dead comsMcp freezes its registry file, so a depth-watcher without a freshness check false-negatives indefinitely (heartbeat cadence 30 s: `comsAdapter.ts:63,236-239`).
- **Corroboration.** The pull-only inbox has already cost real latency: *"Five stale git-manager reports were also sitting unread in the inbound queue… all historical, drained and answered at the start of this pass"* (`runs/post-r1-parity/lead-independent-evidence.md:101-103`).
- **Change.** Interim (runbook): drain-monitors alert on **increase**, not on >0, and always check `heartbeat_at` freshness alongside. Code (with L-1): at `agent_end`, respond `{error:"superseded"}` to unfulfilled inbounds older than the answered one — unblocks their senders and zeroes the counter (~10 lines).
- **Risk/effort.** Low/S. **Layer:** runbook now; extension later.

### QW-10 · Adapter inbound self-heal
- **Failure mode.** A request that enters `inbound` but falls out of the deliverable set (any future edit or missed edge in the waiter handoff, `comsAdapter.ts:121-128,186-189`) is invisible forever, yet still counts against the 32-slot capacity (`:184` → hard `inbound capacity reached` lockout for all senders) and inflates `queue_depth` (`:234`). (Note: I verified the waiter handoff itself is safe under Node's event ordering — this is defense-in-depth for a state that has no recovery path if ever reached.)
- **Change.** In `awaitInbound`, when the queue is empty and there is no `activeInbound` but `inbound.size > 0`, re-enqueue unresponded entries (~4 lines; consistent with the existing redeliver-until-respond semantics).
- **Risk/effort.** Low/S. **Layer:** app (`comsAdapter.ts`).

### QW-11 · Append-only verdict archive + artifact naming convention
- **Failure mode.** `verifier-report.md` is a single **mutable** file overwritten every round — historical verdicts survive only as quotes inside Lead dispositions, and the frd-355 timeline cannot be replayed from artifacts alone (CP-3 even has filename/mtime disorder: `coder-handoff-rev7.md` predates `rev6`, and the internal revision counter reached 9 while file suffixes stopped at 7). A mutable watched file is also the mtime-vs-content race surface: a monitor can fire on a half-written report and act on a mixed old/new read.
- **Change.** Two conventions + ~5 lines: (1) the verifier writes the report to a temp file and renames into place (atomic — same pattern the registry already uses); (2) on each verdict, append the machine-status JSON as one line to `<run-dir>/verdicts.jsonl` (or copy to `verifier-report-<cp>-rev<N>.md`). The Lead's extractor (QW-5) can enforce both. Filename convention: `<artifact>-<cp>-rev<N>.md`, counter owned by the Lead's disposition.
- **Risk/effort.** None/S. **Layer:** verifier briefing + run-dir convention.

---

## Priority 2 — worth doing later

### L-1 · Vendor the patched pi-coms-local extension
The extension is load-bearing (steer, renewal signals ride on it) but lives as a hand-edited npm package. Vendor it (repo or vault, loaded by path, pinned + integrity-checked at launch) and carry the small fixes in one place: steer audit log (QW-3), superseded-inbound sweep (QW-9), send timeouts (L-2), reply attribution (L-4). Effort M; do at a clean run boundary — a flaky transport change mid-run is worse than the status quo.

### L-2 · Symmetric transport timeouts
The pi-side `sendEnvelope` has **no** connect/read timeout (`coms.ts:460-489`) — a wedged receiver event-loop hangs the sender's `coms_send` tool call indefinitely (the hub side has 1 s: `comsTransport.ts:5`). Add ~5 s timeouts in the vendored extension. Inverse nuance: the hub's 1 s ack-read can time out against a busy-but-delivered peer; the caller's retry is a **new** msg_id → duplicate delivery. When touching this, widen the hub ack window to 3–5 s and brief: "send error ≠ not delivered; check before re-sending."

### L-3 · Make renewal-correlation loss visible
Strict response validation (`comsAdapter.ts:195` — reply must come from the original session/endpoint) means a peer that renews mid-request **can never deliver its reply in-band**: the new session's response is nacked; the pi side then drops it permanently (`coms.ts:1554-1567`) or, worse, the orphan path acks (`coms.ts:697-704`) so the Lead's `coms_respond` to a renewed coder reports success while nobody ever reads it. Disk covers the content; the fix is procedural: the Lead's renewal-seed checklist cancels pending sends to the old session (QW-6) and re-dispatches to the new one.

### L-4 · Fix reply attribution at agent_end (vendored fork)
Any turn end — including steer-driven work turns — answers the **newest** unfulfilled inbound with that turn's final text (`coms.ts:1501-1519`): misattributed replies, LIFO starvation of older senders, and the phantom depth of QW-9. Track which inbound triggered the turn (`currentInbound`, `coms.ts:624`) and answer *that* one; skip reply-capture entirely for steer-triggered turns. Disk remains the real channel regardless.

### L-5 · Contract-version doctor
Three coexisting stacks interoperate on an implicit wire contract (patched extension 0.1.1, canonical build, worktree builds); the registry `version: 1` field is written but never read. Stamp implementation + semver into registry entries; add `agentops-trio-doctor <pool>`: per-agent liveness (pid), socket connectivity, heartbeat age, queue_depth, session/socket match, contract version — essentially today's ad-hoc audit as a 40-line preflight. Fold in socket-file GC (3 stale socks in e0 now).

### L-6 · Per-recipient outbound slots (MW-14)
The workflow rulebook already records the cross-recipient cost of the single global slot: MW-14 — *"couldn't re-drive an idle verifier because a prior coder directive was still pending… until its ~5-min expiry"* (`modula-workflow-requirements.md:30`). QW-6's cancel closes the acute wedge; the structural follow-up is one in-flight send **per recipient** (a `Map<peer, msgId>` replacing `outboundId`, `comsAdapter.ts:32,84`) — keeps the contract's bounded-request intent per peer while removing the innocent-bystander lock. Medium effort, app layer; do after cancel has proven insufficient, not before (KISS).

### L-7 · Retire or repoint the watch-*.py drivers
They still target the pre-steer socket path and payload format (`watch-verifier-report.py:48-50,176-184` — `/tmp/agentops/pi-<role>-*.sock`, `{message,deliverAs}`), which no longer exists; the wake-driver doc already flagged this. Either shell out to `agentops-steer` or delete them; their machine-status validation logic moves into QW-5's extractor either way. Dead-but-plausible automation is a trap for the next person.

---

## Hub (Lead) single-point-of-failure posture

What dies with the Lead session: the comsMcp process and its **in-memory** `pending`/`inbound`/`queue` maps (R1 durability is per-process, not disk), plus **every armed Monitor**. What survives: all run-dir artifacts, peer sessions, peer registry entries. Peers already survive hub absence by briefing (R3 loop-await + disk writes). The gap is the **restart ritual**, which should be a pinned checklist in the run dir, not memory:

1. Read latest `verifier-report.md` (machine status), latest `lead-*-disposition.md`, latest `coder-handoff*.md` — that triple is the loop state.
2. Drain inbound: `coms_await` (no msg_id) in a loop until two consecutive timeouts.
3. Re-arm Monitors from `monitors.md` (QW-4).
4. Cancel/re-dispatch any sends recorded as in-flight (QW-6, L-3).

Note: peers cannot see Lead context fullness — the adapter hardcodes `context_used_pct: 0` (`comsAdapter.ts:208,255`); `heartbeat_at` is the only external Lead-liveness signal. Fine while Claude self-compacts (R8a native), but doctor/monitors should watch heartbeat age, and both heartbeat paths clobber `started_at` with now() (`coms.ts:925`; `comsAdapter.ts:255`) — renewal detection must stay keyed on `session_id` change only.

---

## Rename proposal — "Modula Relay" (operator request)

Goal: the tool surface should read as Modula's own protocol, not the package that inspired it. Recommended protocol name: **Modula Relay** (the hub literally relays); MCP server `modula-relay` (tools then surface as `mcp__modula-relay__relay_*`).

| Today | Proposed | Notes |
|---|---|---|
| `coms_list` | `relay_roster` | who is live in the pool |
| `coms_send` | `relay_dispatch` | one bounded request ("dispatch" matches Lead vocabulary) |
| `coms_get` | `relay_poll` | non-blocking reply check |
| `coms_await` | `relay_await` | bounded wait (reply or inbox) |
| `coms_wait` (alias) | — | retire |
| `coms_respond` | `relay_reply` | answer an inbound |
| *(new, QW-6)* | `relay_cancel` | free the outbound slot |
| steer envelope / `agentops-steer` | `relay_wake` / CLI `modula-wake` | wake an idle agent into a work-turn |
| server `coms-mcp` | `modula-relay` | `COMS_MCP_SERVER_NAME` in `shared/comsContract.ts` is the single seam |
| wire types `prompt/response/ping/steer` | `request/reply/pulse/wake` | phase 3 only (interop) |
| `PI_COMS_*` / `PI_AGENT_COMS_*` env | `MODULA_RELAY_*` | phase 3, dual-read fallback |

Alternates considered: `mux_*` ("Modula Mux" — hub-flavored, but implies multiplexing the single-slot design deliberately rejects), `loom_*`/`weave_*` (brandable, opaque). `relay_*` is honest and self-describing — recommended.

Side benefit of owning the naming: today "R6"/"R8a" protocol rules (comms contract) collide with "R8"-style revision-round labels in run artifacts (`F148-R8-001`, `review-request-r8-*.json`) — the run-history sweep hit this ambiguity directly. When the rename lands, move the contract rules to an `MR-n` ("Modula Relay") numbering and leave `R<n>` to mean revision rounds only.

Migration (keep interop in mind — three stacks share the wire):
1. **Phase 1 (cheap, now):** rename tools + server in `comsMcp.ts:25-30` with old names kept as hidden aliases for one run (the codebase already uses the alias pattern via `coms_wait`); bump `COMS_MCP_CONTRACT_VERSION`.
2. **Phase 2:** sweep prompt/briefing surfaces: `rolePrompts.ts:145`, `delegationPrompts.ts`, `autonomyGates.ts`, `extensions/agentopsComsBridge.ts`, vault briefings/kickoffs + `coms-transport.md`; then drop aliases.
3. **Phase 3 (at the L-1 vendoring boundary):** wire envelope types, env vars (dual-read), pool base dir (`/tmp/agentops/coms` → `/tmp/agentops/relay`), and pi-extension tool names — all in the vendored fork, both sides updated at a fresh pool so mixed-version pools never exist.

---

## Run-history evidence (sweep of all run dirs, 2026-07-29)

The frd-355 run dir itself is clean of live coms stalls — the loop converged on verifier findings (~8 CP-6 rounds on one lifecycle-bug family), held by **operator-set** convergence gates (`lead-cp6-rev6-disposition.md:6`, `rev8:18-19`), which are a manual backstop today (the review-fix-controller draft is the automated successor; out of scope here). The incidents that ground this audit's priorities:

- **The wedge + false-liveness incident** (`runs/post-r1-parity/lead-independent-evidence.md`): `:88-91` verifier went idle with an assignment open while its heartbeat stayed fresh (MW-26 IDLE-STALLED; drives QW-4/QW-7); `:93-98` the 60-min TTL turned the single-slot lock into an hour-long pool-wide lockout with the msg_id lost to a prior session (drives QW-6's no-arg cancel); `:101-103` five stale reports sat unread in the pull-only inbox (drives QW-9).
- **In-flight message drop on lifecycle eviction** (issue-288/pl1): a child evicted mid-`process.send()` dropped the message; fixed by arming eviction only in `finally` after the send settles — same fail-closed-teardown class as QW-2.
- **Monitor died on first failure** (issue-277): one publish error killed the heartbeat-sweep scheduler — QW-4 rule 2's precedent.
- **Renewal recovery worked via disk, not coms** (frd-355): dispositions carry resume blocks; one renewal round silently skipped its verifier request (`coder-continuation-rev4.md:1` — *"No verifier request sent for rev-4"*) — exactly the class QW-7's disk-ack convention catches.
- **Adjacent system, same patterns** (forge review stack, issue-264/101): crashed Kodus workers strand rows that silently swallow re-triggers, recovery is manual SQL; queue timeout had to be raised 30 s → 600 s+. Out of this audit's layers, but the stall-threshold prior art (25-min frozen-`updatedAt`) is reusable for trio-doctor heuristics.

## Implementation status (2026-07-29, branch `coms/reliability-hardening`)

Implemented and tested (isolated worktree + isolated pool; live trio untouched):
- **App layer (committed):** QW-1 (60m + env wiring + pin test), QW-6 `relay_cancel` (bare/target/msg_id),
  L-6 per-recipient slots, QW-10 inbound self-heal, L-2 hub ack window 3s, L-5 registry stamp,
  **rename phase 1** (relay_roster/dispatch/poll/await/reply/cancel + legacy coms_* aliases, server
  `modula-relay`, contract 0.3.0 — operator approved relay_*), QW-5/QW-11 `agentops-verdict.py`
  (+`verdicts.jsonl` archive), QW-2 `agentops-trio-down.py` + L-5 `agentops-trio-doctor.py`,
  QW-3 steer assert in patch script + pi-agent hard-fail, L-7 stale watchers deleted,
  runbook (QW-4, QW-7, QW-9-interim, L-3, restart ritual, QW-11 conventions).
- **Runtime rollout package (staged, NOT live):** extension copy (QW-3 steer log, QW-9 supersede
  sweep, L-4 steer-turn reply suppression, L-2 5s send deadline, L-5 stamp), steer CLI staleness
  warnings (QW-7), wrappers (QW-8 pool defaults, QW-8b git renewal, QW-2 launch guard). Package +
  diffs + harnesses: repo `dev-plans/agentops/coms-reliability-rollout/` (mirrored in
  `/tmp/agentops/coms-reliability/rollout/`); apply per its rollout-note when no trio is mid-loop.
- **Deferred:** rename phases 2–3 (prompt sweep, wire/env names) and L-1 vendoring — at a clean boundary.

## Acceptance for the hardening batch

- A rebuild from main yields a comsAdapter with 60-min default expiry + `PI_COMS_OUTBOUND_EXPIRY_MS` honored (test-pinned).
- `agentops-trio-down` leaves zero live pids, zero socket files, zero registry files for the pool; launch guard refuses a second live `lead`.
- A pristine reinstall of pi-coms-local makes the next trio launch **fail loudly** (steer assert), not silently lose wake.
- `agentops-verdict` accepts the live report format, rejects the legacy bullet format with a reason, and knows `needs_lead`.
- Next run dir contains `monitors.md`; a mid-run Lead restart is recovered via the four-step ritual with no operator poke.
- A wedged peer no longer blocks hub sends: `relay_cancel`/`coms_cancel` frees the slot immediately.
