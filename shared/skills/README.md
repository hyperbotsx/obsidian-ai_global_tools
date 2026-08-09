# Shared skills

This folder holds canonical skills that should be reused across multiple runtimes.

## Pattern

- keep one canonical skill package here
- symlink it into runtime-specific skill folders when appropriate
- include supporting reference files alongside `SKILL.md` when the skill depends on them

## Installed shared skills

- `herdr/` — herdr workspace/tab/pane control skill, with `SOCKET_API.md` reference
- `create-pr/` — push branch + open GitHub PR via `git town propose` with house formatting (Greptile tag, no AI mentions). Symlinked into `claude/skills/create-pr` and `codex/skills/create-pr`.
- `create-branch/` — create a new development branch from the latest `main` via `git town hack`, with clean-tree checks and branch naming guidance. Symlinked into `claude/skills/create-branch` and `codex/skills/create-branch`.
- `fast-lane/` — build one approved FRD slice end-to-end in a single strong-model session; review after, not checkpoints during. Model-tier guidance (Fable 5 / Opus 5 / Codex via Pi) and mandatory tracker row in `docs/fast-lane-pilot.md` (modulastack repo). Symlinked into `claude/`, `pi/`, and `codex/` skills.

### Design doctrine set (write it right the first time)

Distilled decision rules — not book summaries — from *A Philosophy of Software Design*,
*Clean Architecture*, *Fundamentals of Software Architecture*, and *Designing
Data-Intensive Applications*. Applied **during implementation**, not only in review; each
carries a `Verifier gates` section so the checking side reads the same doctrine the coder
built against. All symlinked into `claude/`, `pi/`, and `codex/` skills.

- `design-core/` — always-on core (~60 lines). Mirrored into the worktrees `CLAUDE.md`
  for auto-load and appended to trio panes via `pi-agent.sh`; **update both together.**
- `deep-modules/` — module/interface altitude: deep-vs-shallow, information leakage,
  errors-out-of-existence, split-or-merge.
- `boundaries/` — component altitude: Dependency Rule, where to cut, coupling checks.
- `arch-tradeoffs/` — system altitude: driving characteristics, style selection, ADRs,
  fitness functions.
- `data-design/` — data altitude: write/read/failure/evolution, idempotency, replication,
  schema migration.

**Precedence when doctrines conflict:** house KISS wins, then `design-core`, then the
altitude skills. Two known collisions, already reconciled in the files: *decomposition
granularity* — the KISS size limits are review triggers with an escape hatch, and deep
modules agrees (cohesion beats size numbers), so never split to hit a number; *comments* —
house rules stand (no what-comments, naming first, <5% density), with the single addition
that an **interface contract** comment on a public seam is a permitted why-comment.
