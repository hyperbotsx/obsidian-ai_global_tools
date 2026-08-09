# Trio Operating Model — Lead / Coder / Verifier

Status: living · started 2026-07-23 · owner: lead

The orchestration layer above [`coms-transport.md`](./coms-transport.md) (which governs
the wire protocol and isolation). This doc captures **how a trio run is driven** — the
rules a lead follows and a verifier enforces. It is dogfooded on every AgentOps run and
is the **reference spec for the agent workflow Stack Modula will productize**: each rule
here should map onto a platform-enforced behavior in Modula. Frictions and fixes graduate
into [`modula-workflow-requirements.md`](./modula-workflow-requirements.md).

## Roles and authority

- **Lead** — plans, authors/holds the canonical spec, briefs the coder in bounded units,
  receives checkpoint/completion reports, rules on process/scope dispositions, runs the
  final diff review. The lead **never clears a human gate** (PR, merge, deploy, trading,
  confirm-phrase actions) — those stay with the operator.
- **Coder** — implements one checkpoint at a time against the canonical spec; runs house
  gates per commit; loops with the verifier to clean before reporting completion to the lead.
- **Verifier** — reviews each checkpoint against acceptance criteria and guardrails;
  **completeness/acceptance review precedes style**; does not edit coder-owned files.
- Extended roster (per `coms-transport.md`): researcher, steward, git-manager, code-reviewer —
  bidirectional peers, invoked per the mandatory ordering there.

## Autonomy and escalation

The lead runs the checkpoint loop **autonomously** and re-delegates without waiting on the
human. The coder and verifier report to the **lead**, not the human: the coder sends checkpoint
plans, completion reports, and scope escalations; the verifier sends verdicts. The lead acts on
all of them by default — approves/adjusts plans, authorizes the next checkpoint, dispositions
findings, re-delegates bounded work.

The **human (operator) is the escalation point, not the driver.** Escalate to the human ONLY for:

1. **Safety** — data loss, production/live impact, security, secret exposure, or destructive/
   irreversible actions outside the sandbox.
2. **Human gates** — PR-creation approval, merge, deploy, production-readiness, trading, and any
   confirm-phrase action. The lead never clears these (per `coms-transport.md`).
3. **Big / irreversible decisions** — material scope change to an approved FRD (new FRs, dropping
   an acceptance criterion, an architecture pivot), anything that changes what was CEO-approved,
   or cross-project impact.

Everything else — checkpoint plan approval, findings disposition, bounded scope rulings within
the approved FRD, revision loops, re-delegation — the lead decides. The human stays **informed
by default** (visible activity/notifications) and may intervene at any time, but is not required
for the loop to advance. Goal: the lead acts and re-delegates; the human is pulled in for safety
and big calls only.

## The checkpoint loop

1. Lead drains coms, confirms all legs live, briefs the **verifier first** (so it holds the
   guards before work arrives), then briefs the **coder for CP-1 only** (bounded).
2. Coder returns a plan → lead approves/adjusts → coder implements + runs house gates.
3. Coder → verifier handoff per checkpoint; loop until clean (findings resolved).
4. Coder reports checkpoint completion to lead; lead authorizes the next checkpoint.
5. **CP-final (lead):** full diff review, house gates, receipt check, final bug-check.
6. **Operator gates PR and merge.** Never before.

## Briefing pattern (what a good brief contains)

- Pointer to the **canonical spec** (the GitHub issue is source of truth, not a side doc).
- **Bounded scope** — this checkpoint's FRs only; explicit "do not start CP-N+1".
- **Reuse verdicts** — reuse-as-is / extend / replace, from the research sweep.
- **House gates** to run per commit, and the documented baseline failures to expect.
- **Workflow reminder** — loop with verifier, report to lead, no PR.
- End by asking for a plan (files, data model, enforcement approach) before coding.

## Guards

- **Completeness-precedes-style** — the verifier judges whether every FR/AC is actually
  satisfied before commenting on style.
- **Over-minimization is blocking** — dropped fields, skipped requirements, a spec quietly
  narrowed (e.g. a two-key-shape store built project-only) are blocking findings, not nits.
  This is the guard against the F3 `V277-CP1-004` failure mode and is mandatory whenever a
  minimal-code overlay (Ponytail) is active on the coder.
- **A/B capture** — record review rounds + findings per checkpoint against the prior
  baseline so overlay effects are measurable, not asserted.

## Execution continuity and liveness

Agents complete a turn after producing output and then stop. A coder that replies with an
acknowledgment or a status line ("starting now", "recon done, no changes yet") has ENDED its
turn and will sit idle unless re-driven. Rules:

- **Coder execution contract** — every checkpoint brief states: execute the authorized work to
  completion across continuous turns; do NOT end your turn merely to acknowledge or report
  interim status. The coder's next message to the lead must be a genuine `needs_lead` blocker or
  the checkpoint completion report — nothing in between. Baked in at the source: the
  `execution-continuity-v1.md` overlay is applied by the trio wrappers
  (`PI_AGENT_EXECUTION_CONTINUITY=1` → `pi-agent.sh`) to every coder/verifier launch, so agents
  start hardened — the brief and the lead re-drive are complementary layers (prevention + detection).
- **Measure liveness by work, not heartbeat** — the coms heartbeat is a transport timer and
  proves only that the coms server is up, NOT that the agent's loop is active. To tell "working"
  from "stalled", sample real signals: CPU delta over a few seconds, live child processes
  (tsc/node/test), and working-tree changes. Zero CPU + no subprocess + no tree change
  mid-checkpoint = stalled, regardless of a fresh heartbeat.
- **Lead re-drive** — when the poll finds the coder stalled mid-checkpoint (stopped after an ack,
  not blocked on the lead), the lead issues a "continue and execute now" nudge and re-checks by
  work-signal. If repeated nudges produce no work progress, it is a runtime/config issue
  (autonomous-continue not enabled) and the lead escalates to the operator.

## Gate-order discipline

Dependency/launcher PRs merge **before** the dependent run launches (e.g. a launcher
role-gating change must be in main's base before the trio that relies on it starts). Order
is a hard precondition, not a reminder.

## House gates (per commit)

`cd term-control-center && npm test` · `npm run typecheck` · `npm run build` ·
`PYTHONPATH=src python3 -m pytest tests -q` — documented baseline failures excepted.
Registry edits re-emit (`npm run nav:emit`) to keep byte-parity green.

## Landmine catalog (provenance-tagged)

- **Stale-worktree coms config** (prd-283) — a local-scope `coms-mcp` entry pins an absolute
  worktree path; on a new worktree it fails `validateConfig` ("cwd outside worktree") and the
  lead silently never registers. Fix: launch via `agentops-trio-lead`, which re-derives the
  worktree and re-registers every launch. → requirement MW-1.
- **Kody "Review Complete" short-circuit** (#281) — a "complete" posted seconds after a trigger
  is not a real review; a finding landed 4 min later. Anchor the findings window at trigger
  time and wait before declaring clean. → requirement MW-4.
- **GitHub GraphQL rate-limit** — the shared GraphQL pool exhausts; use REST for issue/PR/merge
  operations under load. → requirement MW-5.
- **Lead responsiveness is turn-bound** — a peer's `needs_lead` can sit until the lead is
  nudged; drain inbound at every turn start. → requirement MW-3.

## Per-run retrospective (the fine-tuning loop)

At CP-final of every run, the lead appends a short block to
[`modula-workflow-requirements.md`](./modula-workflow-requirements.md): what we tuned this
run, and what Modula must enforce because of it — each entry tagged with the run that taught it.
