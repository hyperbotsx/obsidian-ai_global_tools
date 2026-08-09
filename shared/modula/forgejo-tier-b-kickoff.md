# Kickoff — Forgejo Tier-B: Git-Forge Adapter + Git Manager (fresh-session brief)

Read this first when starting a fresh session on this work. Everything below is prepared and ready.

## What this work is
Build a **git-forge adapter** (one interface: issues, PRs, boards, completion-detection) with a **GitHub backend now + a Forgejo backend next**, owned by the **Git Manager agent** — Tier B of the git-host migration. First win: route Modula's own dogfooding board/issue ops to the running Forgejo pilot to escape the GitHub GraphQL rate-limit bottleneck. **Staged, adapter-first — NOT a big-bang cutover** (forbidden mid-wave by #262).

## Canonical references
- **FRD (canonical spec):** GitHub issue **#286** — "Git-Forge Adapter (Forgejo-ready) + Git Manager VCS Ownership — Tier B".
- **Roadmap:** `AI_Global_Tools/shared/modula/git-host-migration-roadmap.md` (3 tiers, adapter table, risks).
- **Companion PRDs:** #251 (Git Manager default pane) · #213 (git lifecycle autonomy) · #214 (API budget/token — Tier A relief, fast-track separately) · #262 (rebrand, Phase 4) · #264 (Kodus reliability).
- **Strategy memory:** `forgejo-migration-strategy`. **Harvest doc (EDIT THIS as rules emerge):** `AI_Global_Tools/shared/modula/coder-verifier-workflow/modula-workflow-requirements.md` (MW-1..MW-20).
- **Forgejo pilot (already running):** `forgejo-test`, Forgejo 15.0.5, `http://localhost:3300`, user **ModulaStack** (ID 3).

## Workspace (already created)
- **Worktree:** `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-286`
- **Branch:** `prd/forge-adapter-git-manager-286` (off `main` @ `deee943`, F4 merged; git-town parent = `main` already set)
- Clean tree, ready to implement.

## How to launch the session (from the -286 worktree)
`cd /mnt/hyperliquid-data/projects/worktrees/agentops-prd-286` in EVERY pane before launching (coms binds to the active worktree at launch — MW-1).

1. **Lead** (Claude — you): `agentops-trio-lead` (re-registers coms for this worktree per launch).
2. **Coder:** `PI_AGENT_PONYTAIL=0 agentops-trio-coder` — **Ponytail OFF** (over-minimizes on architectural work; F5-prep decision).
3. **Verifier:** `agentops-trio-verifier`.
4. **Git Manager (NEW — first dogfood):** `agentops-trio-git`.

Confirm all four see each other: lead runs `coms_list` → expect coder, verifier, git-manager all `alive:true` in pool `agentops-trio`.

## Roles this run (MW-19 dogfood)
- **Coder** edits files only and emits **commit-intents** to the git-manager (ready paths + conventional message) — coder does NOT run git directly.
- **Git Manager** owns ALL VCS: stage+commit (from coder intents), branch, rebase, stash/recovery, PR-prep, and the forge ops as the adapter lands. **Push / merge / force-push / history-rewrite / cross-worktree stay human/lead-gated.** Day-one it's semi-manual (lead routes intents) until the wiring lands — that semi-manual phase IS the harvest.
- **Verifier** reviews per checkpoint + a final bug-check; enforces the over-minimization/completeness guards.
- **Lead (you)** runs the checkpoint loop autonomously; escalate to human only for safety, human gates (push/merge/PR), or big/irreversible decisions.

## Checkpoints (from FRD #286)
- **CP-1:** adapter interface + GitHub backend (parity wrapper) + config selector. No behavior change.
- **CP-2:** Forgejo backend for issues + comments + labels; validate against the pilot.
- **CP-3:** boards/status + completion-detection; route Modula dogfooding board ops to Forgejo; Kody/Kodus review-trigger via Forgejo webhook.

## Gates & landmines
- House gates before any push: `cd term-control-center && npm test && npm run typecheck && npm run build` ; `PYTHONPATH=src python3 -m pytest tests -q` (baselines: 1 known pytest fail `test_unlinked_merged_pr…`, ~4-5 node flakies).
- **git-town eats untracked dev-plans docs** — keep harvest/planning docs in the VAULT, not the worktree (see MW-19). Set `--head-sha` explicitly on Kody triggers. REST-first over GraphQL (rate limit; MW-5).
- **Liveness** = file mtimes / CPU, NOT coms heartbeat (MW-10); re-drive stalled agents with action directives, never status pings (a ping ends their turn — MW-9). Relaunch on hard-stall (~1.5h / many rounds — MW-17).
- **Harvest every friction** into the vault harvest doc — this run is the first Git Manager dogfood, so Git-Manager behavior/tuning is prime harvest material.

## Paste-to-start prompt for the fresh lead session
> You are the Lead for FRD #286 (Git-Forge Adapter + Git Manager, Tier B of the Forgejo git-host migration). Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-286`, branch `prd/forge-adapter-git-manager-286`. Read the kickoff brief `AI_Global_Tools/shared/modula/forgejo-tier-b-kickoff.md`, the FRD (issue #286), and the roadmap. Confirm coder+verifier+git-manager are alive via coms_list, then brief CP-1 (adapter interface + GitHub parity backend + config selector). Coder emits commit-intents to the git-manager (coder does no git); git-manager owns VCS; push/merge stay human-gated. Ponytail OFF. Run the checkpoint loop autonomously, harvest workflow frictions into the vault harvest doc, and ping me at CP-final / any human gate.
