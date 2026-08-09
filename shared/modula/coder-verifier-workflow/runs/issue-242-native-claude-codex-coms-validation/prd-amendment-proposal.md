# PRD #242 Amendment Proposal — Transport Contract Wording (Option B)

> **Status: APPLIED 2026-07-19.** Prepared by the #242 coder at operator direction
> (2026-07-18, operator selected Option B now / Option A as follow-up PRD), then applied to
> issue #242 on 2026-07-19 under explicit operator authorization (via `gh api PATCH`); see the
> issue's "CEO review amendment (transport contract)" section. This file is retained as the
> historical record of the proposed wording.

## Why

Verifier checkpoint 2 (see `verifier-report.md`) confirms the functional transport lifecycle
passes: same-pool discovery on both sides, bounded schema'd request, deliberate 250ms
`coms_await` → `timeout`, later correlated single completion (`msg_id`
`3a25afbb-2b6f-4d34-9b88-09f9a8ab2106`), exactly one response, no `coms_send` used to answer,
sanitized evidence only. The sole failures are literal tool-path requirements that the deployed
product does not provide to non-native panes by design (`launchPlan.ts` attaches coms-MCP only
to `native-claude` profiles): the Codex verifier has no inbound-await surface (its `coms_await`
is the outbound-correlation form requiring `msg_id`) and no `coms_respond` tool. The wording
encoded a wrong assumption about the architecture; the invariants that matter — per-worktree
isolation, single correlated response, no-`coms_send`-answer, sanitized records — all held.

Tool-surface parity remains desirable and is routed separately per PRD §11 as a follow-up PRD
(Option A, from `dev-plans/drafts/prd242-coms-tool-surface-followup-proposal.md`), sequenced
after PRD #243 merges because it touches `launchPlan.ts` where #243 has in-flight changes.

## Proposed wording changes (ready to paste)

### FR-4 (§5 item 4) — replace with:

> 4. The Codex verifier must receive the request through its runtime's supported same-pool
> inbound path — the coms-MCP inbound `coms_await` where that surface is exposed, otherwise the
> harness-native inbound listener — validate the request is in scope, then send exactly one
> response through its runtime's supported reply path (`coms_respond` where exposed, otherwise
> the harness-native single-reply path). The response must reach the coder as one validated
> same-pool envelope correlated by `msg_id`.

### FR-7 (§5 item 7) — append one clarifying sentence:

> The verifier's "one response" may be delivered via its runtime's native reply path where
> `coms_respond` is not exposed; the prohibition is on answering via `coms_send`, not on the
> reply tool's name.

### AC-3 (§8 item 3) — replace with:

> 3. The Claude→Codex request is received through the verifier runtime's supported same-pool
> inbound path and answered exactly once through its supported reply path, with the coder
> retrieving one validated response correlated by `msg_id`; `coms_send` is not used to answer.
> Where the verifier runtime exposes the coms-MCP inbound `coms_await`/`coms_respond` tools,
> those must be used.

### Suggested amendment record (for the CEO amendment section):

> - Revision judgment: the amendment aligns the transport contract with the deployed #241
>   architecture, in which the named coms-MCP tools attach only to native-Claude panes and
>   non-native peers participate through their harness-native coms path. All isolation,
>   single-response, no-send-answer, and sanitization invariants are unchanged. Literal tool
>   parity is deliberately deferred to a separate follow-up PRD rather than widened here.

## After the amendment lands

1. Coder notifies the verifier over coms that the canonical contract changed.
2. Verifier re-reviews checkpoint 2 + final checkpoint against the amended wording using the
   existing sanitized evidence (`validation-receipt.json`, including `re_validation_fr6`); no
   new live transport run is expected to be required.
3. Only a verifier `passed` classification supports marking #242 complete (AC-6).
