# FRD Tasks-1 — Portable task ledger (a to-do that outlives compaction, in any CLI)

Status: draft v1 · 2026-07-30 · owner: Erik + Lead · CEO review: **pending**
Canonical FRD source (once approved): a forge issue on `ModulaStack/modulastack`.
Vault working draft: `AI_Global_Tools/shared/modula/frd-portable-task-ledger-draft.md`.
Harvest: surfaced 2026-07-30 — the FRD-363 Lead (Claude Code) was asked to keep a to-do list
that survives auto-compaction; the operator wants that as a standing, cross-harness capability.

Related: FRD Teams-1 (agent roles & team templates — its Lead role **mandates** this ledger) ·
frd-agent-activity-ledger-draft (MW-26 — turn-event ledger / auto-re-drive: **different artifact**,
see §3) · #153 context-renewal workflow · the coder/verifier `coder-handoff.md` run-dir convention.

---

## 1. Problem

Claude Code's built-in to-do list keeps a long implementation focused across context-window
compaction — the operator saw its value driving FRD-363 and wants it on **every** FRD. But it has
three limits that matter for us:

1. **Harness-locked.** It is a Claude Code feature. Our coder, verifier, and git-manager run on
   pi/codex and have no equivalent; a future Lead might be codex, not Claude. The plan-of-record
   cannot live inside one harness's private tool.
2. **Session-locked.** It does not reliably survive a full session restart or hand-off to another
   agent — only in-session compaction.
3. **Not shared.** Because it is per-harness, an improvement to "how we track tasks" cannot
   propagate to the whole fleet.

We want **one** tool, backed by a durable artifact, that any CLI reads and writes — and that
Claude Code agents use **instead of** their native to-do, so the capability is uniform and
centrally improvable.

## 2. Grounded facts (verified 2026-07-30 on `main`; read-only)

| # | Fact | Evidence |
|---|------|----------|
| GF-1 | Native to-do is Claude-only and in-context; pi/codex agents have no durable task list. | Claude Code `TodoWrite`; `pi-agent.sh` roles have no todo mechanism |
| GF-2 | A per-run durable-artifact convention already exists and is machine-consumed — the natural home for a ledger file. | `dev-plans/agentops/coder-verifier-workflow/runs/issue-<N>/` holds `coder-handoff.md`, `verifier-report.md`, `verdicts.jsonl`; app reads them (`term-control-center/server/preparePr.ts:205`, `heartbeatSweep.ts:204`, `launchRemediation.ts:18`) |
| GF-3 | All roles already load a shared MCP (coms) — a candidate uniform interface. | `comsMcp.ts`/`build/server/comsMcp.js`; roles use `coms_list/send/get/await/wait/respond` |
| GF-4 | Verdicts are already validated + append-archived per run — precedent for a small durable, tool-backed ledger. | `scripts/agentops/agentops-verdict.py` (`verdicts.jsonl`, flock, idempotent) |
| GF-5 | The Lead is the natural owner (it decomposes the FRD and receives verifier verdicts / coder completions), and today it is a raw Claude with no standing task discipline. | `agentops-trio-lead` = `exec claude …`; [[trio-lead-hub-reporting-protocol]] |

## 3. Goals / Non-goals

**Goals**
- G-1 A **durable task ledger** artifact per FRD/run, the single source of truth for the task
  list and each task's status — survives compaction, session restart, and agent hand-off.
- G-2 **One uniform interface** to it, usable by every harness: an **MCP tool** (Claude Code +
  any MCP CLI) and a **CLI** (pi/codex/shell), both reading/writing the same store.
- G-3 **Claude Code uses our ledger, not native TodoWrite**, so improvements propagate fleet-wide
  (the operator's explicit ask).
- G-4 The **Lead role owns it**: on FRD kickoff, decompose the FRD into ordered tasks; on every
  turn (and after compaction) re-read it; update as verifier verdicts and coder completions
  arrive; drive the loop from it.
- G-5 Optional **read surface** in the Terminal (render a run's ledger) — reuse, not required.

**Non-goals**
- Not the turn-event **activity ledger** / auto-re-drive (MW-26): that answers "did an agent take
  a turn; re-drive if stalled." This answers "what work remains to finish the FRD." Different
  artifacts; may share the run dir.
- Not a project-management board (that is the app's board/ledger); this is the agent-facing
  working plan for one run.
- Not the coms transport.

## 4. Functional requirements

- **FR-1 — Ledger store.** A durable file per run under the existing run dir
  (`…/coder-verifier-workflow/runs/issue-<N>/task-ledger.json`), holding an ordered task list:
  `{ id, title, status: pending|in_progress|done|blocked, owner_role, checkpoint?, note?,
  updated_at }` plus FRD/issue ref. Atomic writes + a lock, mirroring `agentops-verdict.py`.
- **FR-2 — MCP interface.** Ledger tools (`task_list`, `task_add`, `task_update`, `task_get`)
  on a shared MCP so Claude Code and any MCP CLI use them natively. Host = extend `coms-mcp` or a
  sibling `task-mcp` (OD-1).
- **FR-3 — CLI interface.** `agentops-todo <list|add|update|get>` over the same store, for
  pi/codex panes and scripting. MCP and CLI are two faces of one file → one source of truth.
- **FR-4 — Claude Code adopts ours.** The lead/role prompts direct Claude Code agents to use the
  ledger tool and **not** native `TodoWrite`; a fleet update to the ledger reaches every agent.
- **FR-5 — Lead ownership + loop.** The Lead role prompt (Teams-1 FR-2) mandates: decompose the
  FRD into the ledger at kickoff; re-read at each turn start (compaction-safe); mark tasks
  in_progress/done as work is delegated and verdicts return; never lose the plan-of-record.
- **FR-6 — Compaction/renewal safety.** Because the store is on disk and re-read each turn, the
  plan survives compaction and restart without depending on any harness re-surfacing it. Where a
  harness *can* re-inject (Claude Code), mirror the ledger in on-turn context.
- **FR-7 — Project/run isolation.** Ledger is scoped to the run/worktree
  ([[agentops-strict-project-isolation]]); no cross-run leakage.

## 5. Checkpoints

- **CP-1 — Store + CLI.** FR-1, FR-3, FR-7. `agentops-todo` + the run-dir `task-ledger.json`.
  Immediately usable by pi/codex and scripts; independent of any app change.
- **CP-2 — MCP tool.** FR-2. Same store exposed as MCP tools; wired into the shared coms/MCP the
  agents already load.
- **CP-3 — Role adoption.** FR-4, FR-5, FR-6. Lead + worker role prompts use the ledger (Claude
  Code uses ours over native). Dogfood on a live FRD run.
- **CP-4 — Terminal read surface (optional).** Render a run's ledger in the workspace/active-jobs
  view (prototype pass if it becomes a first-class surface).

## 6. Sequencing / dependencies

- **Reuses** the `coder-verifier-workflow/runs/` convention and the `agentops-verdict.py`
  durable-write pattern — no new storage subsystem.
- **Pairs with Teams-1**: Teams-1 FR-2 (the Lead role) references this ledger as a required
  behavior; CP-1/CP-2 here can land **before or in parallel** with Teams-1 CP-1 (both are
  vault/scripts + a small MCP, independent of #363 app files).
- Distinct from the MW-26 activity ledger (§3) but should share the run dir so one place holds all
  per-run artifacts.

## 7. Open decisions (operator)

- **OD-1** MCP host: extend `coms-mcp` (one server the agents already load) vs a new `task-mcp`.
- **OD-2** Store format: JSON (tool-friendly) with an optional rendered `task-ledger.md` mirror
  for humans, or Markdown-as-source.
- **OD-3** Granularity: one FRD-level ledger, or nested per-checkpoint sub-lists.
- **OD-4** Do we hard-suppress Claude Code's native `TodoWrite`, or just instruct against it?
- **OD-5** Who may write: Lead-only, or each role updates its own task's status.
