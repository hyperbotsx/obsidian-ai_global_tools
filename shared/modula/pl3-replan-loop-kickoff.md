# Kickoff — PL3: Replan Loop + Unprompted Proposals (fresh-session brief)

Read this first when starting the PL3 session. Workspace is pre-provisioned; **panes are deliberately NOT
pre-launched** (PL1 lesson: pane sessions decay over hours — launch fresh on kickoff day, it takes two minutes).

## GATE — do not start until BOTH are true

1. **PL2 (#293) is merged to main.** PL3's §4.1 is a hole that only PL2's shipped plan object can fill.
2. The operator has said go.

## What this work is

Build the **replan loop (P-3)**: trigger watcher, replan chip, delta proposals against the active plan
version, and **unprompted proposals** with the full F3 fan-out. PL1 taught the Planner to answer;
PL3 teaches it to notice. Operator decision already made (brief 02 §9.1): unprompted proposals are a YES.

## Canonical references

- **FRD (skeleton → expand to spec at kickoff):** GitHub issue **#304**. Vault mirror `frd-pl3-replan-loop-skeleton.md`.
- **Page brief:** `dev-plans/drafts/page-briefs/02-planner.md` §2.5, §3, §5, §9.1.
- **PL1 substrate (merged 37c5d26):** planner rail + plan-proposal rendering contract + Approve/Modify acts
  (`pageBotInjection.ts`, `page-bot-panel.js`, `planner-rail.js`), turn-bound intent protocol
  (`pageBotPlannerProtocol.ts`, `pageBotPlannerHandler.ts`, `plannerIntentStore.ts`), receipts
  (`plannerReceiptStore.ts`), F3 producer (`activity_center_planner.py`, `notification_router.py`).
- **PL2 substrate:** read its merged FRD/PR at kickoff — plan object, version identity, activation seam.
- **Harvest doc (EDIT as rules emerge):** `coder-verifier-workflow/modula-workflow-requirements.md` (next id: check tail, ≥MW-36).

## Workspace (already created, 2026-07-25)

- **Worktree:** `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-304`
- **Branch:** `prd/replan-loop-304` (cut from main @ `dac8333`; git-town parent = main set). Clean tree.
- **PL2 will have advanced main** — syncing is Lead pre-flight step 1, not an error.

## Lead pre-flight (IN ORDER, before briefing any peer)

1. **Sync:** `cd` the worktree; `git fetch origin main && git merge origin/main` (expect PL2's changes; resolve nothing blindly — if conflicts touch planner files, read PL2's diff first).
2. **Fill §4.1 of #304** from PL2's shipped reality: plan-object shape, active-version identity, immutable snapshot fields, "job has started" boundary, receipt/activation seam. Then expand #304 from skeleton to spec.
3. **Settle watcher ownership with #301 (PL6):** both need a "since the active plan version" counter. PL3 landing first ⇒ PL3 owns the watcher and #301 consumes it — record the decision on both issues.
4. **Context Brief (MANDATORY — Phase 0 is binding):** PL3 routes to **run** (`cross-cutting` + `completion-state`, medium+ scope). Produce `project-context-brief.md` + `context-brief-state.json` in the run dir per `context-brief-phase0-workflow.md`, via a read-only gatherer, BEFORE the CP-1 coder directive. Sources must name real files.
5. Only then: launch panes and brief CP-1.

## How to launch (kickoff day — isolated pool, MW-21/22)

`cd /mnt/hyperliquid-data/projects/worktrees/agentops-prd-304` in EVERY pane; prefix EVERY launch with
`PI_AGENT_COMS_PROJECT=agentops-trio-pl3`.

1. **Lead:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl3 agentops-trio-lead`
2. **Coder:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl3 PI_AGENT_PONYTAIL=0 agentops-trio-coder`
3. **Verifier:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl3 agentops-trio-verifier`
4. **Git Manager:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl3 agentops-trio-git`

Lead confirms via `coms_list`: canonical names, no `2`-suffixes (suffix = stale registration; stop and clean).
Optionally start the stall watcher (PR #303): `python3 scripts/agentops/content-filter-watch.py --pool agentops-trio-pl3 --coms-dir /tmp/agentops/coms/agentops-trio-pl3`.

## Checkpoints (provisional — re-cut when §4.1 is filled)

- **CP-1:** trigger watcher + chip state, read-only. No proposals. (Stateful-surface checklist applies: absent ≠ corrupt, fail closed, monotonic counters independent of rollback.)
- **CP-2:** delta proposal + Approve/Modify + receipts. Approval = plan v+1, activates NOTHING.
- **CP-3:** unprompted proposals + full F3 fan-out (pulse, Needs-you, Activity, email) + suppression of declined deltas.

## Gates & landmines (PL1-earned)

- House gates before handoffs: `cd term-control-center && npm test && npm run typecheck && npm run build`; `PYTHONPATH=src python3 -m pytest tests -q`. Known baselines as of 2026-07-25: ~5 node (PI_COMS label, fix-loop source, Browser-QA target, lane-cap wording, issue-243 sandbox fixture), 1 pytest (`test_unlinked_merged_pr…`). Nav registry byte-parity must stay green.
- **Durable artifacts are the handoff contract, not coms** (MW-28): coder-handoff.md / verifier-report.md in the run dir; lead POLLS files; reviewers write findings incrementally. Peer→lead delivery failed one-directionally for hours in PL1 — never let completion depend on a message.
- Ack-then-work is unreliable with turn-based agents: reply-slot expiry ≠ undelivered; check inbound + file mtimes before re-driving (double-execution risk).
- Codex content filter can kill the verifier on security-flavoured review prose (MW-29): phrase directives in neutral correctness language; on a block, lead-verify or reframe — never blind-retry. The #303 watcher classifies this.
- Liveness = file mtimes/CPU/session-log, never status pings (MW-10). Agents wedge into zero-token turns after hours: 2-3 failed re-drives ⇒ ask operator for a pane relaunch (cheap; durable state makes it lossless).
- Fix directives name the bug CLASS and demand an audit of sibling paths (MW-30); whole-diff bug-check before each commit closes what per-finding probes miss.
- git-town eats untracked docs — commit run docs promptly. No hardcoded product names (APP_NAME/config).
- **Forgejo is primary (cutover 2026-07-27):** origin = forge.modulastack.com (ModulaStack/modulastack);
  issues/PRs/reviews live there — do NOT use `gh` for writes (old GitHub repo is archived read-only).
  Reviews: agents post `@kody start-review` directly via the forge API (humans use the
  `@modula start-review` relay); `--force` only to re-run an already-reviewed head. Forge API via
  AGENTOPS_FORGE_FORGEJO_URL/TOKEN.
- Scope fences: plan **activation stays PL2's engine** — PL3 proposes deltas and creates v+1 only. No Studio, no intake changes. `#296` will replace the receipt store's persistence — check its status at kickoff before building on receipt internals.

## Paste-to-start prompt for the fresh Lead session

> You are the Lead for FRD #304 (PL3 — Replan Loop + Unprompted Proposals, P-3). Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-304`, branch `prd/replan-loop-304`. PL2 (#293) has merged — verify that first; if it has not, STOP and tell the operator. Read the kickoff brief `AI_Global_Tools/shared/modula/pl3-replan-loop-kickoff.md`, issue #304, page brief 02 §2.5/§3/§5/§9.1, and PL2's merged FRD + PR. Then run the Lead pre-flight IN ORDER: (1) sync the worktree with origin/main; (2) fill §4.1 of #304 from PL2's shipped plan object and expand the skeleton to a spec; (3) record the watcher-ownership decision on #304 and #301; (4) produce the Project Context Brief per Phase 0 — it routes to RUN — before any coder directive; (5) launch and verify the trio panes (pool agentops-trio-pl3, canonical names). Hub-route all coms through yourself; durable run-dir artifacts are the handoff contract; push/merge stay human-gated. Run the checkpoint loop autonomously, harvest frictions into the vault harvest doc, and ping the operator at CP-final or any human gate.
