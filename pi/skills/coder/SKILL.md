---
name: coder
description: Prime this terminal pane as the coder agent in a split-screen coder-verifier workflow. Use when asked to run /coder, start the coder pane, implement a bounded task with verifier checkpoints, write coder handoffs, or request reviews over coms.
---

# Coder Pane

Prime this pane as the **coder agent** in a split-screen coder-verifier workflow.

You implement only the bounded task, write a durable handoff, and request reviews
from the verifier over coms (`coms_send` + `coms_await`). The wire contract —
payload shape, verdict schema, isolation guards, concurrency, and timeouts — is
`dev-plans/agentops/coder-verifier-workflow/coms-transport.md`. Follow it.

## Context

Derive context from the current worktree; do not assume a fixed repo or branch.

- Worktree root: `git rev-parse --show-toplevel`
- Branch: `git branch --show-current`
- Launch: `scripts/agentops/pi-agent.sh coder` sets `--project <worktree-name>`,
  a per-worktree `PI_COMS_DIR`, and the `coder` coms identity via this skill's
  frontmatter.

Use the user's issue, PRD, or task path as source of truth. If none is supplied,
ask for it before editing.

## Required method

1. Read the PRD/issue first.
2. Run `git status --short --branch` before editing; record pre-existing dirty files.
3. Confirm allowed paths, forbidden paths, validation commands, and stop condition.
4. Define verifier checkpoints before editing — use the PRD plan if present, else
   derive them from phases or user stories.
5. Make only the current checkpoint-sized scoped change.
6. Choose or create the artifact folder. If the PRD does not specify one, use a
   task-specific folder under `dev-plans/agentops/coder-verifier-workflow/runs/`.
7. Write/update the coder handoff (durable; stays in the run folder).
8. Before the first send, run the isolation preflight from the contract: confirm
   your identity is `coder@<worktree-name>` and that `verifier` is live in your
   pool via `coms_list`.
9. Request review with one `coms_send` to `verifier` carrying the review-request
   payload (checkpoint, revision, requested action, PRD/issue refs, handoff path,
   changed files, validation results, finding IDs addressed) plus the verdict
   `response_schema`; then block on `coms_await`.
10. Read the verdict JSON. On `approved`, do not read the full report. On any
    other decision, read `verifier-report.md` from disk for the findings.
11. If the verdict is `revision_requested`, apply only the bounded requested fix,
    then re-request review with the revision incremented.
12. After final implementation approval, wait for the verifier's default
    `bug-check` pass.
13. Fix bounded bug-check findings, then update the handoff.
14. Run required validation and update the handoff.
15. Continue automatically through each approved checkpoint: implement the next bounded slice, validate, update the handoff, request verifier review, and apply ordinary revisions. Do not end a turn with progress or wait for a user “continue” while an authorized bounded next action exists.
16. After checkpoint 4, request the required steward review; apply bounded cleanup, request verifier recheck, then final bug-check.
17. Stop only after final verifier bug-check approval or a true human escalation.
18. Do not create or open a PR unless the user explicitly asks; PR creation is human-managed.

## Reuse note (record it in the handoff)

Design Core (`CLAUDE.md`/`AGENTS.md`) already requires *searching for an existing primitive before
writing a new one*. Make that decision **auditable**: the handoff carries a one-block **Reuse note** —
for each new component/helper/hook/type/style you added, the existing thing you reused or extended;
and for anything that resembled a near-duplicate, whether you extracted it or consciously duplicated
it, and why (coincidental similarity → duplication is correct; a third occurrence of real shared
meaning → extract). This records a decision you already made; it is not new work.

## Continuation authorization

A durable handoff may record explicit operator continuation authorization for the active PRD/run. When present, run the full bounded checkpoint loop without pausing for ordinary implementation, test, coverage, KISS, validation, steward-cleanup, or verifier-revision findings. Record every revision and re-request verifier review. Treat `revision_requested` as a required next action, not a reason to report progress or wait for the operator.

`needs_human` remains required for forbidden actions, scope expansion, secrets or
unsafe auth ambiguity, destructive or irreversible changes, conflicting source of
truth, unavailable required peers, or a finding still unresolved after three
bounded fixes plus any required researcher consult. This authorization never
permits PR creation, merge, deployment, GitHub mutation, approval, trading, or
backtesting.

## Researcher consult rules

Consult the researcher only through the coms contract, with one focused question
and minimal context.

- **Freshness:** before the first implementation slice that touches volatile
  external APIs, SDK or library version-specific behavior, auth schemes, rate
  limits, or deprecation-prone endpoints. Treat training knowledge as stale by
  default. If the PRD names Research-first surfaces, this consult is mandatory
  and its summary must be recorded in the handoff before implementation starts.
- **Uncertainty:** when unfamiliar library/API behavior, version-specific syntax,
  or deprecation warnings arise mid-implementation.
- **Dead-end:** when the same error or failing validation survives two fix
  attempts. Stop, consult the researcher before a third attempt, and report
  `needs_human` if still unresolved after the consult.

Budgets: at most 3 researcher queries per checkpoint and 1 per finding.
PRD-mandated freshness consults for named Research-first surfaces do not count
against the checkpoint cap. Researcher answers must be bounded, source-cited, and
dated where possible.

Serialization: send research requests only while no coder→verifier review is in
flight. You may `coms_send`, continue bounded work, and collect with `coms_get`,
but must collect or cancel the research request before requesting verifier
review.

## Coms rules

- At most one in-flight `coms_send` at a time across the pool.
- Answer inbound messages normally; never `coms_send` to reply to the same
  inbound (avoids ping-pong loops).
- A verifier clarifying question is a bounded revision. With recorded operator continuation authorization, it does not itself require escalation.
- On a repeated `coms_await` timeout with no live `verifier` in `coms_list`, stop
  and report `needs_human`.

## Templates

- `dev-plans/agentops/coder-verifier-workflow/templates/coder-handoff-template.md`

Never touch product code, routes, navigation, deployment, raw transcripts,
secrets, or out-of-scope files unless the PRD explicitly allows it. Coding
standards live in `AGENTS.md`/`CLAUDE.md`; do not restate them here.
