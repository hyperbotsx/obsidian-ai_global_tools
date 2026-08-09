# Context Brief — PRD #242 Native Claude ↔ Codex Coms Runtime Validation

> **Supersession note (2026-07-19):** this brief describes the ORIGINAL literal transport
> contract as written at run start (2026-07-17). The canonical PRD was amended on 2026-07-19
> (operator-authorized; issue section "CEO review amendment (transport contract)"): FR-4/FR-7/
> AC-3 now accept the verifier runtime's supported same-pool inbound and reply paths (harness-
> native where the coms-MCP inbound `coms_await`/`coms_respond` surface is not exposed).
> References below to receiving via `coms_await` / answering via `coms_respond` are the
> pre-amendment wording, retained unedited as the historical record.

## Canonical scope
- PRD (source of truth): https://github.com/hyperbotsx/agentops-harness/issues/242
- Branch: `prd/native-claude-codex-coms-validation-242`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-242`
- Base: `main` at `2e80015` (PR #241 / PRD #231 merged native coms runtime).

## Nature of this PRD
Runtime-validation only. No product-code changes are expected (PRD §11). The single
allowed write is a sanitized evidence receipt in this run-artifact folder.

## Roles in this isolated per-worktree pool
- `coder` — this pane, native Claude Code runtime (initiator of the bounded review request).
- `verifier` — Codex CLI runtime (`gpt-5.6-sol`); receives via `coms_await`, answers once via `coms_respond`.
- `researcher`, `steward` — optional; unused unless a failure requires bounded consultation (PRD FR-1).

## What I will do (approved scope)
1. `coms_list` and confirm only same-pool peers before sending (FR-2).
2. Send the verifier ONE bounded review request with a `conversation_id` and small JSON
   response schema (FR-3).
3. Prove the FR-6 non-fatal short wait: `coms_await` with a deliberately short timeout →
   observe `timeout` while the verifier runs its turn → retrieve the later valid response via
   a second `coms_await`/`coms_get` for the same correlation id (FR-5, FR-6).
4. Confirm exactly one `coms_respond` answer; neither peer uses `coms_send` to answer (FR-7).
5. Write only sanitized outcomes, message ids, tool statuses, peer identities, timestamps,
   validation commands, and result classification (FR-8).
6. Request the verifier's checkpoint classification (`passed`/`failed`/`needs_human`) of the
   sanitized receipt (AC-6).

## Hard boundaries (PRD §7 forbidden)
- No source/deploy/route/config edits; no service restart; no PR/merge/deploy/GitHub mutation.
- No auth bypass, API-key auth, browser/session-storage exposure, or transcript retention.
- No off-pool contact, socket probes, or worktree/endpoint guard weakening.

## Stop condition (FR-9)
Any failed same-pool check, native-Claude auth problem, missing MCP tool, bad correlation, or
unexpected tool result → stop and classify `needs_human`; do not patch code in this PRD.

## FR-0 / AC-0 note
`native-claude` runtime is already supported in `term-control-center/server/launchProfiles.ts`
(merged via PR #241). Exposing it in `TERM_CONTROL_MODEL_PROFILES` is a human-gated operator
config action (PRD §6 "separate human authorization"), not a coder source change. Evidence that
it succeeded is this pane running as the native-Claude `coder` alongside the Codex `verifier`
with no nested-Claude delegate fallback.

## Transport semantics (from source, read-only)
`term-control-center/server/comsAdapter.ts` + `comsMcp.ts`:
- `coms_send` returns `{msg_id}` immediately; the reply arrives asynchronously (one outbound in flight).
- `coms_await(msg_id, timeout_ms)` → `{status:'complete'|'timeout'|'error', ...}`; on timeout the
  pending reply stays live, so a later await/get for the same `msg_id` still completes.
- `coms_get(msg_id)` polls; `coms_respond(msg_id, response)` is the only way to answer an inbound.
