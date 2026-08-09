# Modula coder-verifier(-git) workflow — canonical harvest

Relocated here 2026-07-24 from the agentops-harness PR worktree because git-town's sync-stash repeatedly removed these untracked docs from the branch worktree (see MW-19). This vault is not a git repo, so it is a durable home.

- `modula-workflow-requirements.md` — the MW-1..MW-N harvest table (product requirements distilled from live trio runs). **Canonical.**
- `operating-model.md` — orchestration spec (roles, autonomy/escalation, checkpoint loop, guards, gate-order, landmines).
- `coms-transport.md` — coms house rules (one-outbound-in-flight, reply expiry, peer visibility).
- `runs/` — per-issue run evidence (handoffs, review-request payloads) backing the harvest rows.

Every trio run is dual-purpose: ship the PRD AND harvest workflow rules into `modula-workflow-requirements.md`.
