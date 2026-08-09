# Kickoff — PL2: Delegation Plan Engine + Plans Tab (fresh-session brief)

Read this first when starting a fresh session on this work. Everything below is prepared and ready.

## What this work is
Build the **delegation plan engine (P-2)**: versioned immutable plan snapshots, validation (dependency cycles, slot capacity, gate consistency), atomic activation into waves, receipts, and the **Plans sub-tab** (version list + delta view + approval receipts). PL2 of Phase 2 (spine PL1→PL2→PL3). PL1's Planner renders proposals and takes Approve chat acts; PL2 is the engine those acts drive.

## Canonical references
- **FRD (canonical spec):** GitHub issue **#293**. Vault copy: `frd-pl2-delegation-plan-engine-draft.md`.
- **Page brief:** `dev-plans/drafts/page-briefs/02-planner.md` (frozen v1) — §2.4, §3, §5, §9 decisions (§9.2 slot capacity is a Setting; §9.3 Plans tab v1; §9.4 quick jobs foldable).
- **Merged substrate:** F3 #277 (notifications), F4 #283 (page-bot platform), **#286 forge adapter** (board status ops via `forge.boards`, dogfood lane default-off).
- **Harvest doc (EDIT as rules emerge):** `coder-verifier-workflow/modula-workflow-requirements.md` (MW-1..MW-23; MW-23 review-loop split is IN FORCE).

## Workspace (already created)
- **Worktree:** `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-293`
- **Branch:** `prd/delegation-plan-engine-293` (off main @ `a287780`, includes #291 adapter + #290; git-town parent = main set). Clean tree.

## How to launch (CRITICAL: isolated pool + Opus 5 lead)
`cd /mnt/hyperliquid-data/projects/worktrees/agentops-prd-293` in EVERY pane; prefix EVERY launch with `PI_AGENT_COMS_PROJECT=agentops-trio-pl2`.

1. **Lead** (Claude — **Opus 5 trial**, operator decision): `PI_AGENT_COMS_PROJECT=agentops-trio-pl2 agentops-trio-lead`, then immediately run `/model` in the session and select **Opus 5**. A/B vs the Fable-led #286 run — harvest triage quality, MW-20 judgment, session coherence, token spend.
2. **Coder:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl2 PI_AGENT_PONYTAIL=0 agentops-trio-coder` (Ponytail OFF — architectural, MW-18)
3. **Verifier:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl2 agentops-trio-verifier`
4. **Git Manager:** `PI_AGENT_COMS_PROJECT=agentops-trio-pl2 agentops-trio-git`

Lead preflight via `coms_list`: coder, verifier, git-manager alive with CANONICAL names (any `2`-suffix = stale registration squatting the pool — stop and clean before briefing; MW-21/MW-22).

## Roles (MW-19 + MW-23, both proven in #286)
- Coder edits files only; commit-intents to lead {paths, conventional message, rationale}; ZERO git.
- Git Manager owns ALL VCS + the full mechanical tail of advisory-review loops (commit → security sweep → push → review-session refresh → Kody re-trigger with fresh head SHA). Push/merge/force-push/rewrite/cross-worktree = human/lead-gated.
- Verifier reviews per checkpoint + final whole-branch bug-check; joins advisory-loop fixes ONLY for critical/high or contract-touching findings (MW-23).
- Lead hub-routes all coms, ratifies/adjusts every reviewer finding before delegation (never blind-forward), owns MW-20 convergence stop, escalates to human only for safety/gates/irreversibles.

## Checkpoints (FRD #293 §5)
- **CP-1:** plan object + versioned store (immutable snapshots) + validation engine (cycles, capacity, gate consistency) + slot-capacity setting plumbing. Pure backend + mocked tests.
- **CP-2:** atomic validate-then-activate → wave population via existing lane orchestration; receipts to Activity (F3 producer) + audit; thin CLI/route as production consumer (MW-13 — no unmounted engine).
- **CP-3 (GATED on PL1 #288 merged):** Plans sub-tab on the existing board page + wire PL1's Approve/Modify chat act to the engine. If PL1 hasn't landed, PAUSE at CP-2 boundary — never build against an unmerged contract.

## PL1 coordination (it runs in parallel)
CP-1/CP-2 touch lane/plan backend modules PL1 doesn't modify — parallel-safe. The plan-proposal message schema is PL1's artifact: CONSUME verbatim; schema changes are lead↔lead cross-lane negotiation, never a local fork. Check PL1 (#288) state before briefing CP-3.

## Gates & landmines
- House gates: `cd term-control-center && npm test && npm run typecheck && npm run build`; `PYTHONPATH=src python3 -m pytest tests -q` (known baseline fail `test_unlinked_merged_pr…`, ~4-5 node flakies; forge live smokes visibly skip without env). Nav changes keep `npm run nav:emit` byte-parity green.
- Coms: single outbound slot per sender + ~5-min expiry — every directive demands ack-then-work; long results arrive as NEW messages to lead (MW-9/MW-14). Liveness = file mtimes/CPU, never pings (MW-10). Relaunch on hard-stall ~1.5h (MW-17).
- git-town eats untracked docs — planning docs live in the VAULT; commit run docs promptly.
- REST-first for gh (GraphQL pool exhausts — MW-5). No hardcoded product names. No Co-Authored-By/Claude mentions in commits.
- No partial application anywhere in this FRD's domain — validation/activation failures leave prior state untouched.
- Harvest every friction; this run additionally harvests the Opus-5-as-lead A/B evidence.

## Paste-to-start prompt for the fresh lead session
> You are the Lead for FRD #293 (PL2 — Delegation Plan Engine + Plans Tab, P-2). Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-293`, branch `prd/delegation-plan-engine-293`. Read the kickoff brief `AI_Global_Tools/shared/modula/pl2-delegation-engine-kickoff.md`, FRD issue #293, and page brief `dev-plans/drafts/page-briefs/02-planner.md` (§2.4/§3/§5/§9). Confirm coder+verifier+git-manager alive with CANONICAL names via coms_list (pool `agentops-trio-pl2`; any suffix = stale squatter, clean first). Brief CP-1 plan-first (versioned plan object + store + validation engine + slot-capacity plumbing; pure backend; coder proposes store-home D-PL2-1 before building). Coder emits commit-intents (zero git); git-manager owns VCS + advisory-loop mechanics (MW-23); verifier joins fix loops only for critical/contract findings; push/merge human-gated. Ponytail OFF. Hub-route all coms; ack-then-work on every directive; MW-20 convergence stop on any review loop. CP-3 is GATED on PL1 (#288) merging — pause at CP-2 if it hasn't. Run the checkpoint loop autonomously, harvest frictions (plus Opus-5-lead A/B observations) into the vault harvest doc, and ping the operator at CP-final or any human gate.
