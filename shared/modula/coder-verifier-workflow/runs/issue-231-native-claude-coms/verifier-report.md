# Verifier Report — PR #241 Post-PR Kodus Revision 2

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "PR #241 - Kodus revision 2",
  "revision_reviewed": 2,
  "open_findings": 2,
  "finding_ids": [
    "V241-K2-005",
    "V241-K2-006"
  ],
  "bug_check_status": "revision_required",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/verifier-report.md"
}
```

## Decision

Post-PR Kodus revision 2 needs two bounded fixes. Inbound capacity/deduplication, bounded transport extraction, and logger routing pass review. However, endpoint-pool validation remains bypassable through a path-traversing `session_id`, and the new outbound lifecycle timer starts before transport acknowledgement, allowing a supported short expiry to remove correlation state before `send()` returns.

Reviewed revision: committed PR head `7511b5aa6b4eb9bbd66f13a3b5e66d95528d118f` plus dirty bounded-revision fingerprint `abdf80c7767a274ffe8e372ba0d57fafdef0a2e8cf78e0b108375d7e30cdf58c` before this report update.

## Open findings

### V241-K2-005 — Session-ID traversal still escapes the configured endpoint pool

- Severity: high.
- Confidence: confirmed by deterministic scratch repro.
- Location: `term-control-center/server/comsAdapter.ts:202-204`; `term-control-center/server/comsWire.ts:54,60`.
- Trigger: a syntactically accepted registry entry or inbound prompt uses a `session_id` such as `../../../escape` and sets `endpoint` to the normalized result of the adapter's own `endpointFor(comsDir, session_id)` calculation.
- Failure mechanism: registry/envelope parsing validates `session_id` only as a non-empty string. `sameComsEndpoint` then derives the expected path with `path.join`; traversal components are normalized, so the equality check accepts a socket outside `$PI_COMS_DIR/sockets/` and can escape `$PI_COMS_DIR` entirely.
- Impact: the Kodus transport-boundary bypass remains exploitable for outbound sends and inbound prompt identities. The repro placed a socket outside the configured coms root; `coms_send` reached it and an inbound prompt from it received ACK.
- Requested bounded action: require protocol-safe session IDs on registry and envelope reads and make endpoint validation independently prove that the normalized endpoint remains inside the configured sockets directory before exact comparison. Add outbound and inbound traversal-session regressions.
- Decision impact: blocks the endpoint-pool security fix.

### V241-K2-006 — Outbound lifecycle expiry can fire before delivery is acknowledged

- Severity: medium.
- Confidence: confirmed by deterministic delayed-ACK repro.
- Location: `term-control-center/server/comsAdapter.ts:84-98,213-223`.
- Trigger: the supported `outboundExpiryMs` is shorter than a peer's ACK delay while still within the transport deadline.
- Failure mechanism: `armExpiry` runs before target resolution and `sendEnvelope`. The expiry can remove pending state and clear `outboundId`; the later valid ACK then lets `send()` return a message ID that already reports `unknown msg_id`.
- Impact: callers can receive success-shaped send completion with no retrievable correlation, and the expiry window does not represent the requested post-ACK response lifecycle.
- Requested bounded action: begin terminal response expiry only after prompt ACK succeeds, while preserving pending registration before transport for the immediate-response race. If a response completes before expiry is armed, do not arm it. Add a delayed-ACK regression proving `send()` returns a pending ID and expiry starts after ACK.
- Decision impact: blocks lifecycle-expiry correctness.

## Resolved portions

- Inbound unresolved work is bounded by a validated positive limit and counts active plus queued requests.
- Duplicate unresolved inbound message IDs are rejected before ACK.
- Ordinary off-pool endpoint values are rejected for target send, liveness ping, and inbound prompt sender identity.
- Unanswered post-ACK requests have a terminal default lifecycle and release the outbound slot.
- Diagnostics route through the local logger abstraction without prompt, peer, token, or raw error content.
- Transport helpers are correctly extracted and retain the established frame/connection deadlines.

## Independent validation

| Check | Result |
|---|---|
| Focused adapter/MCP suite | Pass, 28/28 |
| `npm --prefix term-control-center run typecheck` | Pass |
| `npm --prefix term-control-center run build:server` | Pass |
| `git diff --check` plus bounded trailing-whitespace scan | Pass |
| Session traversal endpoint probe | Fail closed: **no**; outbound accepted and inbound ACKed outside the coms root |
| Delayed-ACK/short-expiry probe | Fail closed: **no**; `send()` returned an already-unknown message ID |
| Full suite | Not represented as passing; status remains the documented prior harness timeout |

## KISS review

- File size: pass; `comsAdapter.ts` is 288 lines, `comsTransport.ts` is 23 lines, and `logger.ts` is 4 lines.
- Function size: pass in the bounded diff.
- Nesting depth: pass.
- Parameter count: pass.
- Comments: pass; no new comments.
- Dead code: pass.

## Scope and authority review

- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-231`.
- Branch: `prd/native-claude-coms-peer-231`, tracking the same-named remote at committed head `7511b5aa6b4eb9bbd66f13a3b5e66d95528d118f`.
- Native wrapper and role/security prompt hashes are unchanged; no authority or permission behavior changed.
- PR/Kodus state was read only. No commit, push, re-review trigger, merge, GitHub mutation, deployment, approval, trading, or backtest action occurred during verification.
