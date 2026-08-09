# Buzz relay study → Modula Relay v2 plan

Status: v1 · 2026-07-30 · owner: Erik + Lead · type: investigation + decision plan (no code changed)
Sources: `block/buzz` @ HEAD (cloned read-only 2026-07-30: ARCHITECTURE.md, NOSTR.md, VISION_AGENT/MESH, `crates/buzz-acp/*`, `crates/buzz-core/src/kind.rs`, `docs/nips/NIP-AM|AO`, `docs/welcome-kickoff-silent-failures.md`, `perf/RELAY_BUS_SCALING.md`) · forge #363 (Term-1) + #364 (Term-2) · `coms-reliability-audit-2026-07-29.md` · `frd-agent-comms-contract-draft.md` (R1–R9) · `frd-agent-wake-renewal-driver-draft.md`.
Feeds: the comms-contract FRD (R1–R9 → "Modula Relay v2"), MW-26 activity-ledger FRD, Z4 runner split.

## 1. What Buzz actually is, relay-wise

Buzz (Block, Apache-2.0, Rust) is a self-hosted team-chat platform where humans and AI agents are
protocol-equal clients of one **relay** — a standalone Axum WebSocket server speaking Nostr NIP-01.
The relay is the single source of truth; there is no peer-to-peer path at all.

**Core mechanics (verified in source):**
- **Universal signed event.** Every action is `{id, pubkey, kind, tags, content, sig}` — chat (kind 9),
  reactions, workflow steps, job lifecycle, presence. `kind` is the only dispatch switch; new feature =
  new kind, zero breakage. Events are Schnorr-signed by the author (human or agent keypair).
- **Connection lifecycle.** WS connect → NIP-42 challenge → signed auth → subscriptions (`REQ` +
  filters). Writes are acked (`OK`), reads replay history first (`EOSE` marks the live boundary).
  Slow-client grace, heartbeat ping, connection/handler semaphores.
- **Event pipeline.** auth → pubkey match → verify sig → channel membership → **Postgres insert
  (idempotent, ON CONFLICT DO NOTHING)** → Redis publish → in-process fan-out (3-tier subscription
  index) → search-index/audit/workflow triggers (fire-and-forget). Ephemeral kinds (20000–29999:
  presence, typing, observer frames) skip storage.
- **Loss-resistance is total.** The store is authoritative; clients track per-channel `last_seen` and
  resubscribe with `since = min(last_seen, dropped_floor) − skew` (`buzz-acp/src/relay.rs`) — even
  events dropped by *local* backpressure are re-replayed. Harness startup replays the whole unprocessed
  @mention backlog.
- **Access control** = channel membership, checked before subscription registration (no race window);
  tenancy = host-resolved community; audit = hash-chained append-only log.

## 2. How GPT↔Claude conversations work (buzz-acp)

This is the piece Erik asked about. Model heterogeneity is solved by **three stacked open protocols**,
not by a custom bridge:

```
Nostr relay (transport+persistence)  ──WS──  buzz-acp harness (per agent identity)
                                              └─ stdio ACP/JSON-RPC ──  agent runtime
                                                 (goose | codex via codex-acp | claude via claude-agent-acp)
                                                     └─ stdio MCP ── tools
```

- **Identity:** each agent has its own Nostr keypair; a GPT agent and a Claude agent are just two
  relay members. They talk by posting kind-9 messages @mentioning each other (`#p` tag) in a shared
  channel. Nothing anywhere knows "GPT is talking to Claude" — the relay routes pubkeys and kinds.
- **Wake = delivery.** The harness (not the model) owns the subscription. @mention events queue
  **per channel**; when a channel has pending events and no prompt in flight, the harness drains up to
  50 into ONE batched `session/prompt`. Per-channel serialization, cross-channel parallelism (pool of
  1–32 subprocesses, claim/return, crash-respawn, lazy start).
- **Steer = cancel + merge.** A message landing mid-turn cancels the ACP turn and re-prompts with the
  cancelled batch merged in, framed either "continue, incorporate this" (`Steer`) or "supersede"
  (`Interrupt`) (`queue.rs::CancelReason`). Owner side-channel: `!cancel`, `!rotate` (fresh session).
- **Failure containment:** per-channel in-flight deadline (turn cap + 100 s) auto-expires stuck
  channels; failed batches retry 10× (5 s→300 s backoff) then dead-letter loudly. Turn liveness =
  **stdout activity** (idle timeout 620 s resets on any output; hard cap 2 h) — work signals, not
  heartbeats (our MW-10 lesson, independently converged).
- **Heartbeat driver:** optional idle-agent prompt ("check feed for pending mentions/actions"),
  lower priority than real events, skipped when busy, one in flight globally.
- **Author gates:** owner-only / allowlist / anyone / nobody, checked before anything reaches the
  model; same-owner sibling agents admitted via owner attestation (NIP-OA).
- **Outbound is agentic:** the agent replies by calling the Buzz CLI itself (signed with its key) —
  the harness relays inbound only. Replies/threading guided by a `[Context]` block carrying channel
  UUID + pre-resolved reply anchor.

**Agent-protocol suite (their custom NIPs — the formalized version of what our FRDs are groping toward):**
- **NIP-AM (kind 44200, durable):** one encrypted per-turn usage event — input/output tokens, cost,
  `contextLimit`/`used`, session/turn ids, `deltaReliable`, stop reason. Published by a Drop-guard so
  it fires even on panic/cancel. == our missing context-percent feed (F-27/FR-29) + usage accounting.
- **NIP-AO (kind 24200, ephemeral):** encrypted raw ACP activity frames agent→owner, relay MUST NOT
  persist. == our MW-26 turn-event ledger, as a live stream.
- **NIP-AE engrams:** agent memory as encrypted replaceable events, fetched at session birth (memory
  layer parallel). Plus personas, teams, managed-agent kinds; job lifecycle kinds 43001–43006
  (request/accepted/progress/result/cancel/error); workflow approval request/grant/deny kinds.
- **Ops postmortems worth stealing:** `welcome-kickoff-silent-failures.md` documents their A→B→A agent
  ack-loop (21+ "parked, won't reply again" messages). Fix: publish-only-if-the-turn-produced-
  something, humans always get replies, **no bare acknowledgements** (named offenders), callback-
  mention only on completed work; circuit breaker = consecutive agent-authored reply budget (high N,
  human message resets) — deliberately NOT yet shipped because a low cap manufactures silent drops.

## 3. Ours today (grounded in the 07-29 audit + #363 facts)

One paragraph, since the audit is the canonical map: Modula Relay (post-rename) is an **RPC hub
inside the Lead's session** — comsMcp + in-memory `pending/inbound/queue` maps that die with the Lead;
peers attach via a hand-patched npm extension over per-session unix sockets; request/reply correlated
by msg_id with outbound slots, TTL expiry, 30 s bounded awaits, redelivery-until-respond; steer is a
separate socket path; renewal breaks reply correlation permanently (L-3); durable truth lives in a
parallel hand-rolled layer of run-dir markdown + `verdicts.jsonl` + Monitors/greps; context %
hardcoded 0. The `coms/reliability-hardening` branch (QW-1..11, L-2/5/6, relay_* rename, contract
0.3.0) patches the sharpest edges **within** this architecture.

Two additions from the 2026-07-30 code re-verification (subagent sweep of the canonical checkout,
branch `fix/coms-reply-handle-expiry` @ `338ce07`, cross-checked against `build/`):
- **The wake asymmetry is worse than "Lead not steerable": native-Claude clients have no push path at
  all.** For Pi/Codex an inbound `prompt` triggers a turn (`coms.ts:628-640`); for the native adapter
  an inbound lands only while the agent is blocked inside a 30 s `coms_await` — otherwise it sits in
  the in-memory queue undrained, and a steer envelope is nacked "malformed" by `parseEnvelope`
  (adapter has zero steer support). `agentops-steer` therefore wakes Pi/Codex panes only. Relay v2's
  "wake = delivery" must explicitly cover native-Claude clients, i.e. the Lead itself.
- **A second bespoke in-house relay already exists**: PRD Studio's host-mediated page-bot path
  (`server/pageBotInjection.ts` over a persistent `ConversationStore`; surfaces planner/author/
  ceo-reviewer/…/lead) — and it already has the two properties Relay v2 wants (durable store,
  idempotent delivery via content-hash deliveryIds with a pending→delivered state machine). Relay v2
  should absorb this seam or share its store, not become a third relay.

## 4. The comparison that matters

The deep difference is not Nostr, WebSockets, or Rust. It is:

> **Ours is transient point-to-point RPC with in-memory state; Buzz is a durable append-only event
> log with subscriptions.** Sends are appends, replies are events, "waiting" is a cursor, and restart
> = re-read. Most of our contract R1–R9 exists to patch failure modes that the log model makes
> *unrepresentable*.

| Contract req | Our mechanism (patched) | Buzz mechanism (structural) |
|---|---|---|
| R1 durable inbound | 32-slot in-memory queue, redeliver-on-await | Postgres log + since-replay + startup backlog |
| R2 no reply-loss | 60 m TTL + overwrite-pending + procedural care | reply is an event in the log; late = still there |
| R3 loop-await | 30 s capped awaits, re-await briefing | subscription; nothing to loop over |
| R5 no send-lock | per-recipient slots + `relay_cancel` | no slots; fire-and-ack append |
| R6 dual report | briefing rule ("both-and"), repeatedly violated | channel broadcast: hub sees everything by subscription |
| R7 disk truth | markdown artifacts + jsonl + atomic-rename conventions | the log IS the durable truth, queryable |
| R7a inbox alarm | queue_depth monitor w/ phantom-depth caveats | push delivery + `needs_action` feed + heartbeat prompt |
| R4 wake | steer socket (hand-patch) + Monitors + pokes | **wake = delivery**: harness starts a turn per batch; steer = cancel+merge |
| R8/R8a renewal | per-CLI extension + Lead ritual; correlation lost on renewal | harness-side sessions + `!rotate`; identity=keypair so renewal is invisible to the wire; NIP-AM usage stream |
| — | context % hardcoded 0 | per-turn metric event, crash-proof publisher |

**Efficiency, honestly:** at 4-agent pool scale, their throughput engineering (3-tier fan-out index,
partitioned Postgres, community-scoped Redis topics with a measured 64× ingress reduction) is
irrelevant to us — raw transport was never our bottleneck. The efficiency that DOES transfer is
**agent-turn economics and operator time**: batch-drain (N queued messages = 1 prompt, not N turns),
push instead of poll loops, no redelivery spam, heartbeat-skipped-when-busy, "silence is success"
norms killing ack storms, and zero lost-message stalls (the 2026-07-26-class incidents that cost us
hours). Their model is *better*, not faster — better because whole failure classes are structurally
absent, and because one uniform surface carries messages, telemetry, presence, jobs, and audit.

**What Buzz does NOT give us** (and where we're ahead): checkpoint discipline, review-fix convergence
control, launch gating, worktree/session supervision — their workflow engine's approval gates are
literally unfinished (WF-08: suspended runs marked Failed). Their scope is chat-with-agents; ours is
a delivery control plane. We are not behind as a product; we are behind on the transport layer only.

## 5. Decision

**D-A. Do not adopt buzz-relay/Nostr itself.** Postgres+Redis+Rust relay, keypair crypto envelope,
community tenancy — wrong weight and wrong trust domain for ephemeral single-machine trio pools
(KISS: "standard libraries before exotic dependencies"). Revisit the crypto/auth layer only when a
wire crosses machines (Z4).

**D-B. Adopt the architecture pattern into Modula Relay v2** — the comms-contract FRD (R1–R9) gets
written as an event-log relay, not as further RPC patching:

1. **Re-home the relay out of the model session.** One single-writer relay process per machine
   (module in the Term server, launchable standalone for app-less pools; behind the Z4 seam like
   SessionSupervisor). The Lead becomes a client like everyone else. What dies with the Lead today
   (queues, pending, Monitors) survives.
2. **Event-log semantics on disk.** Append-only per-pool JSONL (house pattern: `verdicts.jsonl`,
   atomic rename) + per-agent cursors. `relay_dispatch` = append; `relay_reply` = append referencing
   msg_id; `relay_await` = cursor tail. Restart/renewal = resume cursor keyed on **role identity, not
   session id** — kills R2 residuals, L-3 renewal-correlation loss, QW-10's invisible-inbound class,
   and the R7 duplication (artifacts stay, but stop being the only durable channel).
3. **Delivery driver with buzz-acp semantics** (this absorbs the wake driver draft): per-recipient
   one-in-flight; drain-all-pending into one batched work-turn; mid-turn arrivals steer (cancel+merge
   framing, or followUp for codex/pi equivalents); in-flight deadline + bounded retries + loud
   dead-letter; idle heartbeat tick for the hub's own inbox (R7a structural). Turn-liveness from work
   signals (stdout/CPU), never coms heartbeats (MW-10 — Buzz independently agrees).
4. **Turn telemetry as events on the same log** (NIP-AM-shaped): every turn end appends
   `{role, session_id, turn_seq, context_used_pct, tokens_in/out, stop_reason, ts}`. FR-29's gauge
   feed, the renewal watcher, MW-26's ledger, and future usage accounting all read this one stream.
5. **Comms norms + circuit breaker.** Port the Buzz base-prompt rules into trio briefings/rolePrompts
   (publish only when the turn produced something worth knowing; a human question always gets an
   answer; **no bare acknowledgements**; callback-mention = completed work only). Add the reply-budget
   breaker in the delivery driver (N≈8 consecutive agent-authored turns in a thread → drop trigger +
   tracing line; human message resets).
6. **Defer to Z4:** transport auth (token/keypair — NIP-42/98 as reference) when control plane and
   runner split across machines; and an **ACP evaluation** for the runner⇄agent seam — codex-acp and
   claude-agent-acp exist today, and ACP would give spawn-verify (initialize/session-new as the
   registration deadline), steer (turn cancel), stop reasons, and usage streaming as protocol reads
   instead of tmux scraping — collapsing R8's per-CLI adapter matrix. Big move; prototype first.

## 6. Sequencing (respects approved FRDs; no scope disturbance)

0. **Now:** land `coms/reliability-hardening` and `fix/coms-reply-handle-expiry` on main. Status
   check 2026-07-30: the 60-min TTL + env wiring is committed (`f94405b`) and live in the prod build,
   but the canonical checkout sits on the fix branch — a rebuild from main still regresses it; the
   0.3.0 hardening work (per-recipient slots, `relay_cancel`, self-heal, rename) is separately
   unmerged. Apply the staged runtime rollout at the next clean pool boundary.
1. **Term-1 #363 / Term-2 #364 proceed unchanged.** One cheap forward-compat action inside Term-1:
   implement FR-29's "server-readable artifact" as the per-turn JSONL telemetry event of D-B.4 (same
   fields), so Relay v2 later changes the carrier, not the schema — and FR-28's single steer surface
   choice (in-repo verifier-socket path, vendored) is the same surface D-B.3 will drive.
2. **Post Term-1 CP-7:** write the comms-contract FRD as **"Modula Relay v2 (event-log core)"** —
   phases: (P1) re-home state to the relay process, wire-compatible, same MCP tools; (P2) event-log
   semantics + cursors; (P3) delivery driver + steer unification + breaker; (P4) telemetry stream +
   retire hardcoded context 0. Fold in the deferred rename phases 2–3 and L-1 vendoring at the same
   boundary. Trio dogfoods it (fake-pi-agent E2E from Term-1 FR-30 is the harness).
3. **MW-26 ledger FRD** consumes the same log (its "harness-emitted turn events" = D-B.4 stream +
   NIP-AO-style frames if we want live tailing in Term).
4. **Z4:** auth + ACP prototype per D-B.6.

## 7. Skip list (explicit)

Redis/Postgres infra; Nostr wire format + signatures (until Z4); communities/multi-tenant host
resolution (we have project pools + `stateDirFor`); huddles/media/mesh/social; their YAML workflow
engine (ours is the product); their unfinished approval gates. Keep watching: NIP-AE engrams (memory
layer #104 parallel), push-lease gateway (mobile notifications, far future).
