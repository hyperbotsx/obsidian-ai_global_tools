# Kickoff — R1: Workspace Reskin (fresh-session brief)

Read this first when starting a fresh session on this work. Everything below is prepared and ready.

## What this work is
**W-1: reskin the workspace page onto F1 tokens + F2 shell** — design-only, strangler-fig (presentation replaced, behavior preserved): pane grid, mode tabs, sidebar job cards/gauges/renew chip, jobs-mode switch, context menu, the three modals, both diff views — plus the **Lead panel dock** and ephemeral consult-pane surfacing (E0 prep; masterplan delta), and **removal of the BrowserPane tab** (brief 01 §9.4). Phase 1 reskin: needs only F1+F2 (merged). R1 unblocks E0, the masterplan's highest-priority addition.

## Canonical references
- **FRD (canonical spec):** GitHub issue **#294**. Vault copy: `frd-r1-workspace-reskin-draft.md`.
- **Page brief:** `dev-plans/drafts/page-briefs/01-workspace.md` (draft v1 — §9 decisions settled; where brief and FRD disagree, the FRD cut wins; flag ambiguity to lead).
- **Prototype (visual source of truth):** `dev-plans/drafts/modula-stack-design-prototype.html` — `#coder` `#research` `#git` `#diff` `#diffsplit` + renew/new-job/add-agent/remove-job modals.
- **Design principles:** max terminal real estate; consistent menu; Term blue palette via F1 tokens; color by text+dots on dense cards; brand from config, never hardcoded.
- **Harvest doc:** `coder-verifier-workflow/modula-workflow-requirements.md` (MW-1..MW-23 in force).

## Workspace (already created)
- **Worktree:** `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-294`
- **Branch:** `prd/workspace-reskin-294` (off main @ `a287780`; git-town parent = main set). Clean tree.

## How to launch (CRITICAL: isolated pool)
`cd /mnt/hyperliquid-data/projects/worktrees/agentops-prd-294` in EVERY pane; prefix EVERY launch with `PI_AGENT_COMS_PROJECT=agentops-trio-r1`.

1. **Lead:** `PI_AGENT_COMS_PROJECT=agentops-trio-r1 agentops-trio-lead` — then `/model` (Opus 5 recommended; operator's call).
2. **Coder:** `PI_AGENT_COMS_PROJECT=agentops-trio-r1 PI_AGENT_PONYTAIL=0 agentops-trio-coder` (operator may choose Ponytail dynamic per MW-18 — reskin CPs are largely mechanical; verifier watches over-minimization either way).
3. **Verifier:** `PI_AGENT_COMS_PROJECT=agentops-trio-r1 agentops-trio-verifier`
4. **Git Manager:** `PI_AGENT_COMS_PROJECT=agentops-trio-r1 agentops-trio-git`

Lead preflight via `coms_list`: coder/verifier/git-manager alive with CANONICAL names (any suffix = stale squatter — stop and clean; MW-21/22).

## Roles (MW-19 + MW-23)
Coder edits files only, commit-intents to lead, ZERO git. Git Manager owns all VCS + advisory-loop mechanics (commit→sweep→push→session-refresh→Kody re-trigger); push/merge human-gated. Verifier per checkpoint + final bug-check; joins advisory fix loops only for critical/contract findings. Lead hub-routes, ratifies every finding before delegation, owns MW-20 stop.

## Checkpoints (FRD #294 §5)
- **CP-1:** page frame onto tokens+shell (mode tabs, pane grid, topbar/job-switcher). ZERO functional regression.
- **CP-2:** sidebar (cards/gauges/waves/folders/renew chip/context menu/jobs-mode) + the three modals.
- **CP-3:** diff views + Lead dock (layout stub, collapsed default — D-R1-1) + consult-pane surfacing + BrowserPane tab removal + prototype polish pass.

## Parallel lanes — hard boundaries (PL1 #288 and PL2 #293 run concurrently)
- R1 touches WORKSPACE page surfaces only. Board/#plan/planner chat = PL1's; plan engine backend = PL2's. Never edit them.
- Nav `registry.ts`: append-only entries, keep `npm run nav:emit` byte-parity green, rebase-before-propose.
- F2 shell components are consumed, not modified; a needed shell change = lead↔lead cross-lane negotiation.

## Gates & landmines
- House gates: `cd term-control-center && npm test && npm run typecheck && npm run build` (known ~4-5 flakies); pytest only if python touched (baseline fail `test_unlinked_merged_pr…`; forge live smokes skip without env).
- Reskin review discipline: verification = exercising the regression flows (brief §2: enter job, mode tabs, prompt, reorder, sidebar modes, context menu, both diff modes) + prototype side-by-side — not line-by-line diff semantics. Wide-but-shallow diffs are expected; verifier bounds to scope (MW-16).
- Coms: single outbound slot + ~5-min expiry → ack-then-work on every directive; results as NEW messages to lead (MW-9/14). Liveness by mtimes/CPU (MW-10). Relaunch on hard-stall ~1.5h (MW-17).
- git-town eats untracked docs — planning docs in the VAULT; commit run docs promptly. REST-first for gh (MW-5). No product names hardcoded; no Co-Authored-By/Claude mentions.
- CDP/browser plumbing must remain untouched when the BrowserPane tab is removed (grep-verify; it becomes the QA live-view engine).

## Paste-to-start prompt for the fresh lead session
> You are the Lead for FRD #294 (R1 — Workspace Reskin onto Tokens + Shell, W-1). Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-294`, branch `prd/workspace-reskin-294`. Read the kickoff brief `AI_Global_Tools/shared/modula/r1-workspace-reskin-kickoff.md`, FRD issue #294, page brief `dev-plans/drafts/page-briefs/01-workspace.md`, and open the prototype `dev-plans/drafts/modula-stack-design-prototype.html` (visual source of truth). Confirm coder+verifier+git-manager alive with CANONICAL names via coms_list (pool `agentops-trio-r1`; any suffix = stale squatter, clean first). Brief CP-1 plan-first (page frame onto F1 tokens + F2 shell; zero functional regression; coder lists the components it will touch before building). Design-only discipline: presentation replaced, behavior preserved; no board/planner/plan-engine surfaces (PL1/PL2 lanes own those); F2 shell consumed not modified; nav registry append-only with byte-parity green. Coder emits commit-intents (zero git); git-manager owns VCS + advisory-loop mechanics (MW-23); verifier bounds reviews to regression flows + prototype parity (MW-16) and joins fix loops only for critical/contract findings; push/merge human-gated. Hub-route all coms; ack-then-work; MW-20 stop on any review loop. Run the checkpoint loop autonomously, harvest frictions into the vault harvest doc, and ping the operator at CP-final or any human gate.
