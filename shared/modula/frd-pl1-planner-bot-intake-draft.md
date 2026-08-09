# FRD: PL1 — Planner Bot + Planning Intake Page (P-4, P-5) — Phase 2 start

> Canonical FRD source: the GitHub issue created from this draft (house labels `type:prd`, `status:draft`).
> Assigned agent: `agent:agentops`. Code home: `hyperbotsx/agentops-harness`.
> Proposed branch: `prd/planner-bot-intake-<issue#>` off `main`; worktree `agentops-prd-<issue#>`.
> Umbrella: #267 Modula Stack Design Rollout — PL1 in `dev-plans/drafts/page-briefs/00-index.md` (Phase 2 start; spine F3+F4→PL1→PL2→PL3).
> Briefs: 02-planner (frozen v1, decisions §9) — P-4 chat/bot scope §2.4–2.7 · P-5 intake §2.6; 03-frd-studio (cohort handoff seam only).
> Dependencies: F3 #277 (notification backbone) + F4 #283 (page-bot substrate) — both merged. Blocks: PL2 (plan engine), PL3 (replan loop); establishes the page-bot pattern E0/PL7/E7/E12 reuse.
> Research-first surfaces: F4 substrate — `term-control-center/server/pageBotPlatform.ts`, `pageBotRuntime.ts`, `pageBotLazyPool.ts`, `pageBotInjection.ts`, `pageBotModelSettings.ts`, `pageBotMemoryRecord.ts`, `conversationStore.ts`, `src/PageBotPanel.tsx` + `pageBotPanelContract.d.ts`, Python `conversation_store.py`/`conversation_lock.py`; planning reuse — server `planningBrief.ts`, `prd_studio_artifacts.py` (17 fields, validation, templates), `lane_plan.py`, `parallel_plan.py`, `planned_worktrees.py`, `laneOrchestrator`/`launchPlan`/`launchGroup`, `github_project.py`; notifications — F3 producer registration; nav — `src/navigation/registry.ts` + `npm run nav:emit` byte-parity pipeline.

- **Status:** draft (CEO review optional gate before implementation)
- **Date:** 2026-07-24
- **Operator decisions inherited:** brief 02 §9 (unprompted proposals YES but that mechanism is PL3; slot capacity is a Setting; Plans sub-tab is PL2 scope; quick jobs foldable) · F4 D1 indefinite retention, D2 per-page/per-project conversations, D3 seeded per-role model defaults, D4 lazy pool.

## 1. Problem

F4 shipped the page-bot substrate — chat persistence, lazy pool, model settings, runtime binding — but zero product bots exist on it. Planning today is manual: board state lives in labels/Project fields, "what should we work on next" happens in the operator's head, and FRD intake is hand-written markdown. Brief 02 (frozen) promises a Planner that proposes plans, executes instruction-bound board ops, and runs one-to-one planning intake — with nothing plugged in. Phase 2 (the product core) cannot start, and every later bot (Lead E0, Reviewer PL7, Review Manager E7, QA Manager E12) waits on PL1 to establish the substrate-integration pattern.

## 2. Goals

**P-4 — Planner bot (first tier-3 page bot):**
- Bind a Planner role onto the F4 substrate: registry entry, role prompt, seeded model default (D3), lazy-pool launch on first chat (D4), per-project persistent conversation (D1/D2).
- Chat rail on the board page + `#plan`, via `PageBotPanel` and the panel contract.
- **Instruction-bound board ops** (whitelist: resume job, queue job, request gate review, rebalance-proposal) — every op receipted; zero unprompted mutations; kanban drag stays a non-interaction.
- **Plan-proposal rendering contract:** the structured chat message (slot lines, team chips, gate notes, Approve/Modify affordances). Approval in PL1 emits a receipt + F3 event; **plan activation (waves populating) is PL2** — the contract ships now so PL2/PL3 plug into it.
- F3 producer registration for planner events (proposal posted, intake decision needed) → Needs-you card + Activity + badge per F3 kinds.

**P-5 — Planning intake page (`#plan`):**
- 17-field planning-brief UI backed by existing `planningBrief.ts` + `prd_studio_artifacts.py` (reuse, not rebuild) with field-level write receipts.
- One-to-one intake conversation with the Planner (drafts fields at tier 2; flags operator decisions, never resolves them) with decision cards.
- Intake session store: persistent per draft (D2 keying).
- **"Start authoring cohort" arm-state** when required fields + decisions complete — hands off to Studio (brief 03) as a stubbed seam; Studio itself is PL4.

## 3. Non-goals (deferred, bounded per MW-16)

- Delegation plan **engine** — versioned plan object, validation, activation, waves (PL2).
- Replan loop, replan chip, **unprompted** proposals + their trigger watcher (PL3). PL1's Planner only speaks when spoken to.
- Board reskin — kanban/matrix/timeline/plans tabs (R2/P-1); PL1 mounts on the existing board serving.
- Studio pages, authoring cohort runtime (PL4/PL5).
- Email/SMTP delivery (F3 D2: interface only).

## 4. Design

- Planner = pageBotPlatform role registration + `rolePrompts` addition; model default seeded in `pageBotModelSettings` (D3).
- Conversations through `conversationStore` (TS) / `conversation_store.py` (Python parity), per-project keying (D2), indefinite retention (D1), `conversation_lock` semantics respected.
- Board-op tool surface: a small, whitelisted op set wired to existing lane orchestration (`laneOrchestrator`, `launchPlan`, `planned_worktrees`) — instruction-bound, receipted to Activity + audit.
- Plan-proposal message schema defined once (shared contract for PL2/PL3), rendered structured in the chat rail with Approve/Modify as chat acts (no confirm phrase; receipts written).
- Intake route `#plan`: brief store reuse; decision cards; arm-state validation = required fields + all decision cards resolved.
- Nav entries via `registry.ts` + `nav:emit` (byte-parity test must stay green).
- Consult hook (brief 02 §6: intake may pull Codebase Expert tier-1 inline) — **open decision D-PL1-2 below**.

## 5. Phasing (checkpoints)

- **CP-1:** Planner role bound to substrate; chat rail live on board page; persistence + lazy pool + model settings proven (restart survives, first-message launch). No board ops.
- **CP-2:** instruction-bound board ops + receipts; plan-proposal rendering contract + Approve/Modify chat acts; F3 producer registration (Needs-you/Activity entries fire).
- **CP-3:** `#plan` intake page: 17-field UI + decision cards + per-draft session store + cohort arm-state + Studio handoff stub.

## 6. Acceptance

- Planner chat on the board page: lazy-launched, per-project persistent, survives server restart, model configurable in settings.
- Board ops execute only on explicit instruction; each writes a receipt; audit shows zero unprompted mutations.
- A plan proposal renders as the structured message; Approve emits receipt + F3 event; activation explicitly deferred (assert the PL2 seam exists and is documented).
- Intake completes end-to-end to arm-state with field receipts; decision cards resolvable only by the operator.
- Nav registry byte-parity + house gates green (node test/typecheck/build; pytest with known baseline).
- A short page-bot integration recipe doc exists (the pattern E0 and later bots follow).

## 7. Risks / open decisions

- **D-PL1-1 — hosting surface:** mount the chat rail on the existing board page now (recommended; R2 reskins later) vs wait for R2. Recommended: existing page.
- **D-PL1-2 — Codebase Expert consult:** tier-1 consult runtime doesn't exist yet as a page bot; recommend deferring inline consults to a fast-follow unless trivially cheap via existing coms.
- **Tier-3 permission envelope:** the op whitelist is the security boundary — review it explicitly at CP-2.
- **Boundary discipline:** approval-without-activation will tempt over-scope into PL2 (MW-16); the verifier brief must bound CP-2 to the rendering/receipt contract.

## 8. Dogfood setup (parallel run)

Quartet (lead + coder + verifier + git-manager) in a NEW worktree with an **isolated coms pool**: launch every pane with `PI_AGENT_COMS_PROJECT=agentops-trio-pl1` (wrapper env override) so this run cannot collide with the live #286 pool (MW-21/MW-22). Ponytail OFF (architectural work, MW-18). Coder emits commit-intents; git-manager owns VCS; push/merge human-gated. Harvest frictions into `modula-workflow-requirements.md`.
