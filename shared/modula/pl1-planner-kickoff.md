# Kickoff — PL1: Planner Bot + Planning Intake (fresh-session brief)

Read this first when starting a fresh session on this work. Everything below is prepared and ready.

## What this work is
Build the **Planner page bot (P-4)** — the FIRST tier-3 product bot on the F4 page-bot substrate — and the **planning intake page (P-5)**: chat rail on the board page, instruction-bound board ops, the plan-proposal rendering contract, and the 17-field intake UI with decision cards. Phase 2 start of the Modula Stack Design Rollout (spine: F3+F4→PL1→PL2→PL3). PL1 establishes the substrate-integration pattern every later bot (E0/PL7/E7/E12) reuses.

## Canonical references
- **FRD (canonical spec):** GitHub issue **#288** — "PL1 — Planner Bot + Planning Intake Page (P-4, P-5)". Draft state; vault copy `frd-pl1-planner-bot-intake-draft.md`.
- **Page brief:** `dev-plans/drafts/page-briefs/02-planner.md` (frozen v1; §9 operator decisions) + 03 (Studio handoff seam only).
- **F4 substrate (merged deee943):** `pageBotPlatform.ts`, `pageBotRuntime.ts`, `pageBotLazyPool.ts`, `pageBotInjection.ts`, `pageBotModelSettings.ts`, `pageBotMemoryRecord.ts`, `conversationStore.ts` (+ py `conversation_store.py`/`conversation_lock.py`), `PageBotPanel.tsx` + contract. F4 decisions: D1 indefinite retention, D2 per-page/project conversations, D3 seeded per-role model defaults, D4 lazy pool.
- **Harvest doc (EDIT as rules emerge):** `AI_Global_Tools/shared/modula/coder-verifier-workflow/modula-workflow-requirements.md` (MW-1..MW-22).

## Workspace (already created)
- **Worktree:** `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-288`
- **Branch:** `prd/planner-bot-intake-288` (off main @ `92c5dbf`; git-town parent = main set). Clean tree.

## How to launch (CRITICAL: isolated coms pool — MW-21/MW-22)
`cd /mnt/hyperliquid-data/projects/worktrees/agentops-prd-288` in EVERY pane, and prefix EVERY launch with `PI_AGENT_COMS_PROJECT=agentops-trio-pl1` (wrappers honor the override as of 2026-07-24). This keeps the run's pool fully separate from the live #286 pool — same-name collisions produced the zombie/suffix dispatch breakage documented in MW-21/MW-22.

1. **Lead** (Claude): `PI_AGENT_COMS_PROJECT=agentops-trio-pl1 agentops-trio-lead`
2. **Coder:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl1 PI_AGENT_PONYTAIL=0 agentops-trio-coder` (Ponytail OFF — architectural, MW-18)
3. **Verifier:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl1 agentops-trio-verifier`
4. **Git Manager:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl1 agentops-trio-git`

Lead confirms via `coms_list`: coder, verifier, git-manager all alive with CANONICAL names (no `2` suffixes — a suffix means a stale registration; stop and clean before briefing).

## Roles (MW-19)
Coder edits files only, emits commit-intents to lead (paths + conventional message + rationale); Git Manager owns ALL VCS (push/merge/force-push/rewrite/cross-worktree human-gated); verifier reviews per checkpoint; lead routes everything (hub-routing — do NOT rely on agent↔agent direct dispatch) and runs the loop autonomously.

## Checkpoints (FRD #288 §5)
- **CP-1:** Planner role bound to substrate; chat rail on board page; persistence + lazy pool + model settings proven. No board ops.
- **CP-2:** instruction-bound board ops (whitelist: resume, queue, gate-review request, rebalance-proposal) + receipts; plan-proposal rendering contract + Approve/Modify chat acts; F3 producer registration.
- **CP-3:** `#plan` intake page: 17-field UI + decision cards + per-draft session store + cohort arm-state + Studio handoff stub.

## Operator decisions in force
- D-PL1-1: mount on the EXISTING board page (R2 reskins later) — lead recommendation, operator may override.
- D-PL1-2: Codebase Expert inline consult DEFERRED to fast-follow — lead recommendation, operator may override.
- Brief 02 §9: unprompted proposals exist but their trigger mechanism is PL3 — in PL1 the Planner only speaks when spoken to. Plan APPROVAL renders + receipts + F3 event; ACTIVATION is PL2 (bound the verifier to this line, MW-16).

## Gates & landmines
- House gates before handoffs: `cd term-control-center && npm test && npm run typecheck && npm run build`; `PYTHONPATH=src python3 -m pytest tests -q` (1 known baseline fail `test_unlinked_merged_pr…`, ~4-5 node flakies). Nav registry changes MUST keep `npm run nav:emit` byte-parity test green.
- Coms protocol: single outbound slot per sender + ~5-min expiry — directives must demand ack-then-work; long results arrive as NEW messages to lead, never as held replies (MW-9/MW-14).
- Liveness = file mtimes/CPU, never status pings (MW-10); re-drive with action directives; relaunch on hard-stall ~1.5h (MW-17).
- git-town eats untracked docs — keep planning docs in the VAULT; commit run docs promptly.
- REST-first for any gh calls (GraphQL pool exhausts — MW-5); no product names hardcoded (APP_NAME/config pattern).
- Harvest every friction into the harvest doc — PL1 is the first product bot on F4; substrate gaps are prime material.

## Paste-to-start prompt for the fresh lead session
> You are the Lead for FRD #288 (PL1 — Planner Bot + Planning Intake, P-4/P-5, Phase 2 start). Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-288`, branch `prd/planner-bot-intake-288`. Read the kickoff brief `AI_Global_Tools/shared/modula/pl1-planner-kickoff.md`, FRD issue #288, page brief `dev-plans/drafts/page-briefs/02-planner.md`, and the F4 substrate surfaces listed in the kickoff. Confirm coder+verifier+git-manager are alive with CANONICAL names via coms_list (pool `agentops-trio-pl1`; any `2`-suffix = stale registration, stop and clean first). Then brief CP-1 (Planner role binding + chat rail + persistence/lazy-pool/model-settings; no board ops). Coder emits commit-intents to you (coder does no git); git-manager owns VCS; push/merge stay human-gated. Ponytail OFF. Hub-route all coms through yourself; demand ack-then-work on every directive (5-min expiry). Run the checkpoint loop autonomously, harvest frictions into the vault harvest doc, and ping the operator at CP-final or any human gate. Scope discipline: plan approval renders/receipts only — activation is PL2; intake hands off to a Studio STUB — Studio is PL4.
