# Prompt for the prototype agent — Context Brief settings in the admin area

Hand this over as-is. It is self-contained.

---

Add a **Context Brief** settings panel to the admin area of the prototype.

## What the feature is

Before an implementation agent (the coder) starts work on an FRD, a separate **read-only** agent produces a
*Project Context Brief*: binding scope, affected surfaces and likely files, existing patterns and
duplicate-code traps, architecture and state constraints, security and human gates, suggested validation,
steward risks, assumptions, and a Sources section separating sourced facts from assumptions. The coder
launch is **gated** on that brief existing and passing a readiness check. It exists to stop agents
rebuilding things that already exist and to stop them discovering blocking facts mid-implementation.

## Where it goes

Admin area → **Project settings**, in the **agent behaviour** group, as a sibling of the existing
**Page-bot models** and **Memory** panels. It belongs there because it is per-project agent-behaviour
policy, not a global system toggle, and because it needs the same health affordance the Memory panel has.

Two levels, shown in this order:

1. **Organisation default** (top of the panel, one line) — the policy new projects inherit.
2. **This project** — the effective policy, with an "inherits organisation default" state that the user can
   override. Make inheritance visible: an overridden project should read clearly as overridden, not just
   as a different value.

## The control: three-way policy, not an on/off switch

Render as a segmented control with three options and a one-line consequence under each:

| Option | Meaning |
|---|---|
| **Auto** *(default)* | Brief runs when the work is risky or large; skipped for small, low-risk work |
| **Always** | Every implementation launch gets a brief |
| **Off** | No brief; requires a reason, and the reason is recorded |

**Auto** must be visibly the default and visibly the recommendation. Under Auto, show the routing rules
read-only so the user can see *why* a brief will or will not run:

- runs when any high-risk surface is touched — `cross-cutting`, `frontend-backend-contract`,
  `shared-schema`, `launch-flow`, `completion-state`, `agent-prompts`, `memory`, `github-integration`,
  `browser-qa`
- runs when declared scope is medium, large or XL
- skips when declared scope is tiny, small, docs-only or a one-file fix
- **asks** when neither scope nor surfaces have been declared — this state blocks the launch rather than
  silently skipping, and the UI should say so plainly

Selecting **Off** opens a required one-line reason field. Do not allow Off to be saved with an empty
reason, and show the stored reason afterwards next to the setting so a disabled gate is never invisible.

## Cost line

Briefs consume model capacity, so put a plain-language cost note in the panel: a brief is one extra
read-only agent run per FRD, and Auto is recommended because it spends that only on risky or large work.
If the prototype already renders per-profile model selection, allow the brief to be pointed at a **cheaper
or local model** than the implementation agent — the brief is read-only summarisation and is a good fit for
a low-cost profile. Show it as a profile picker labelled for the brief specifically.

## Health / last-run state

Mirror the pattern the Memory panel already uses. Show, for this project:

- the last brief: FRD reference, when, and its state — `ready` · `skipped` · `degraded` · `pending`
- for `skipped` or `degraded`, the recorded reason, presented as an audit fact rather than a warning toast
- a **Sources check** indicator: whether the last brief actually cited files, not just that it had a
  Sources heading (a brief citing nothing is worse than none)

Use dots plus text for these states, never colour alone.

## Rules to respect

- Brand and product name come from config — **never hardcode a product name**.
- Reuse the existing admin panel construction, section headers and form controls; introduce no new visual
  vocabulary beyond the segmented policy control.
- Per-project settings, with a visible organisation default and a visible override state.
- Nothing here may read as automatic or silent: a disabled gate always shows its reason.

## What not to build

No brief authoring or editing UI — the brief is produced by an agent and read by the coder. No approval
flow. No global kill switch outside the organisation default. Do not surface the brief document itself in
admin; that belongs with the run artifacts, not settings.
