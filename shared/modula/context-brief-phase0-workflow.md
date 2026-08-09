# Context Brief — Phase 0 workflow (Lead-owned, manual gate)

Status: active from 2026-07-25 · owner: Lead · applies to every FRD run in the trio workflow
Purpose: get the pre-implementation Project Context Brief into our hand-launched runs *now*, using the
same artifacts, schema and routing rules the app already enforces, so Phase 2 (routing trio launches
through `/launch`) is a migration rather than a rewrite.

## Why

The app hard-gates coder launches on a brief (`contextBriefLaunch()` rejects a coder pane without brief
metadata). Our trio launches panes directly through `agentops-trio-*` wrappers and tmux, so the gate never
runs. Evidence that this costs us: in the #288 PL1 run the "no TS→Activity receipt bridge exists" fact
surfaced **mid-implementation** as a `needs_lead` blocker. That belongs in the brief's reusable-modules
section, before the coder starts.

## Roles

- **Lead owns the gate and the route decision.** It does not matter who types the brief; the Lead is
  accountable for it existing, being sourced, and being cited.
- **Production is delegated to a read-only gatherer** (subagents in Phase 0, the `context-brief` pane once
  we route through the launcher). Deliberate: the Lead's own assumptions must not *become* the brief — the
  whole value is separating sourced facts from assumptions.

## Granularity

**One brief per FRD**, plus a short **delta note per checkpoint**. A full high-effort brief three times per
FRD is waste; a checkpoint that opens new surfaces gets a delta appended, not a new document.

## Routing (apply the app's rules by hand)

Declare `scope` and `surfaces` per FRD, then:

| Condition | Decision |
|---|---|
| policy `required` (operator asked) | **run**, reason `operator_required`, override true |
| policy `skip` (operator asked) | **skip**, reason must be non-empty, override true |
| any high-risk surface | **run**, reason `high_risk_surface` |
| scope `medium` / `large` / `xl` | **run**, reason `declared_scope` |
| scope `tiny` / `small` / `docs-only` / `one-file-fix` | **skip**, reason `declared_small_scope` |
| neither declared | **needs_operator_decision** — do not brief the coder until resolved |

High-risk surfaces (verbatim from `contextBrief.ts`): `cross-cutting`, `frontend-backend-contract`,
`shared-schema`, `launch-flow`, `completion-state`, `agent-prompts`, `memory`, `github-integration`,
`browser-qa`.

Note for our own runs: page-bot work touches `agent-prompts` and usually `cross-cutting`, so it routes to
**run** every time. PL1 would have been gated.

## Artifacts

Written to the run directory `dev-plans/agentops/coder-verifier-workflow/runs/issue-<n>-<slug>/`, so they
are committed with the run and survive worktree loss.

**1. `project-context-brief.md`** — sections exactly as the app's brief agent produces them:

```
# Project Context Brief — FRD #<n>
## Sourced facts: binding scope
## Affected surfaces and likely files
## Existing patterns to follow and duplicate-code traps
## Architecture and state constraints
## Security and human gates
## Suggested validation and verifier focus
## Steward risks
## Assumptions / questions for the PRD Author and Researcher
## Sources
```

Rules: link to files rather than paste them; target roughly 150–250 lines because it gets re-read;
every claim in the sourced sections carries a `path:line` or URL in `## Sources`; assumptions live only in
the assumptions section, never mixed into sourced facts.

**2. `context-brief-state.json`** — the app's schema verbatim, so the Phase 2 gate accepts it unchanged:

```json
{
  "status": "ready",
  "decision": { "decision": "run", "reason": "high_risk_surface", "operatorOverride": false },
  "reason": "high_risk_surface",
  "operatorOverride": false
}
```

`status` is one of `pending` · `ready` · `skipped` · `degraded`. The app's readiness check requires
`status: ready`, an exact match between the top-level `reason`/`operatorOverride` and the nested decision,
and the presence of a `## Sources` heading — so mirror it precisely.

## Lead gate checklist (before any coder directive)

1. Route decision recorded, with scope and surfaces named.
2. Both artifacts exist; state is `ready` and internally consistent.
3. `## Sources` **names real files, modules or URLs** — a brief citing nothing is worse than none. The app
   only checks the heading exists; we check the content.
4. Affected-surfaces section names the actual files the checkpoint will touch.
5. Reusable-modules / duplicate-trap section answers "what already exists that this must not rebuild?" —
   the question that cost us CP-2.
6. If proceeding without a brief: record `status: degraded` with a **non-empty reason**, exactly as the
   app's `continue_without_brief` path requires. Never skip silently.

## Directive template additions

Coder directive gains:

```
CONTEXT BRIEF (read before editing): <run-dir>/project-context-brief.md
Route: run · reason <reason>. Your ACK must name the brief path back to me.
Re-read rule: after ANY compaction, history clear, pane relaunch, or re-drive, your FIRST action is to
re-read that brief and the FRD before continuing.
```

**Every re-drive repeats the brief path.** This is the manual form of the re-read guarantee that #255 is
adding to the product; our own run — six wedges and relaunches, each losing in-context state — is the
evidence for why it is not optional.

Verifier directive gains: the brief path plus the instruction to treat the brief's "suggested validation
and verifier focus" section as a starting point, and to flag where implementation diverged from it.

## Exit to Phase 1 / Phase 2

- **Phase 1:** `agentops-trio-coder` refuses to launch without a readable brief for the run unless
  `CONTEXT_BRIEF_SKIP_REASON` is set, which is recorded into the state file. Roughly twenty lines of shell.
- **Phase 2:** launch the trio through `/launch` with `task.contextBrief` metadata and continue via
  `POST /groups/:id/context-brief/continue`, inheriting retry, degraded-with-reason and auditability. Because
  Phase 0 uses the same artifact names, paths and schema, nothing has to be rewritten to get there.
