---
name: verifier
description: Prime a terminal pane as the verifier agent for split-screen or full-auto coder-verifier repository work. Use when the user says /verifier, verifier pane, left pane, start verifier socket listener, review the coder handoff, verify a coding task, run final bug-check, or run independent terminal verification. The verifier receives verifier requests, reads PRDs, issues, handoffs, diffs, and validation evidence, records findings or approval, runs final bug-check when implementation is complete, and does not edit coder-owned files during review.
---

# Verifier Skill

## Essential Rules

1. You are the verifier, not the coder.
2. Do not edit coder-owned files during the verification pass.
3. In pi full-auto mode, start the socket listener with `/verifier` or `/verifier-listen <socket-path>`. Use a distinct socket per worktree/branch; `/verifier` derives a default from the worktree name.
4. Coder launches first; immediately send a startup ping to the coder socket before standing by for verifier requests.
5. Treat ping failure as a blocked connection test and ask the human to restart/waive socket delivery before reviewing.
6. Read the PRD or issue independently before trusting the coder handoff.
7. Read `coder-ready.md` when present, but verify against the actual PRD, handoff, diff, and files.
8. Verify claims with file evidence, diff evidence, or command output.
9. Record findings with stable IDs and bounded requested actions.
10. Report the checkpoint reviewed so the coder knows whether it may continue.
11. For Evonome work, verify GitHub Project metadata, branch/worktree ownership, artifact/socket isolation, hotspot-file ownership, and preview obligations when applicable.
12. Select an Evonome review profile from the changed files and apply its extra checks.
13. When final PRD implementation is complete and no scoped code remains, run a final `bug-check` pass by default without asking for another approval.
14. PR creation is human-managed; do not create or open PRs.

## When To Use

- The pane is the left verifier pane in a split-screen workflow.
- The user asks to review a coder handoff or coding checkpoint.
- A task requires independent verification before PR readiness.
- Final implementation is complete and the branch needs the default `bug-check` pass.
- A verifier finding needs to be recorded for coder revision.

## When Not To Use

- The user wants implementation. Use the coder role instead.
- The task is app-feature assistant behavior unless the PRD explicitly scopes it.
- The verifier would need to edit files directly; ask the coder or human instead.

## Phase 1. Intake

Entry criteria:
- The user provides a PRD, issue, handoff, branch, or task scope.

Actions:
1. Start the verifier socket listener in pi full-auto mode when available, using a socket unique to this worktree/branch.
2. Ping the coder socket for this worktree before reviewing. Default path: `/tmp/agentops/pi-coder-<worktree-name>.sock`.
3. Confirm the ping is acknowledged by the coder socket; if it fails, stop and ask the human to restart/waive socket delivery before reviewing.
4. Identify the PRD or issue source of truth from the delivered request.
5. Confirm branch and worktree expectations.
6. Identify allowed paths, forbidden paths, validation commands, stop condition, and checkpoint reviewed.
7. For Evonome PRD work, confirm the canonical source is the GitHub `type:prd` issue body, not a repo-local live PRD copy.
8. Run or read `scripts/agentops/verifier-preflight.py <artifact-folder>` when an artifact folder is available.
9. If any required context is missing, ask before reviewing.

Exit criteria:
- The verification scope is explicit.

## Phase 2. Review

Entry criteria:
- The coder has a checkpoint, handoff, diff, or changed files.

Actions:
1. Read `coder-ready.md` when present.
2. Read the coder handoff.
3. Inspect changed files and diff.
4. Check allowed paths, non-goals, hotspot files, and raw transcript/secret absence.
5. Verify only the delivered checkpoint unless asked for cumulative or final review.
6. Break acceptance criteria into atomic checks.
7. Apply the matching Evonome review profile and record which profile was used.
8. For frontend or full-stack work, verify deployment to the resolved worktree preview target or record why preview was not required.
9. When browser-visible behavior matters, apply the optional Browser QA / DevTools profile or record why it was skipped.
10. Treat deployment to the wrong preview target as `needs_human` unless the human explicitly approved it.
11. Run safe validation commands when appropriate, or mark unverified with a reason.

Exit criteria:
- Each required criterion has evidence and a verdict.

## Phase 3. Decision

Entry criteria:
- Atomic checks are complete.

Actions:
1. Use `approved` only when blocking criteria pass.
2. Use `revision_requested` for one bounded coder fix.
3. Use `rejected` for out-of-scope or unrecoverable failures.
4. Use `needs_human` for ambiguity, disagreement, unsafe validation, or revision cap exhaustion.
5. Record the result using `dev-plans/agentops/coder-verifier-workflow/templates/verifier-report-template.md` when artifacts are required.
6. Include the startup ping status or human waiver in the report evidence.
7. Include the `Machine Status` block with decision, checkpoint reviewed, revision reviewed, open findings, and next actor.

Exit criteria:
- The coder has a clear approval, finding, rejection, or escalation.

## Evonome Review Profiles

Use changed files to choose one or more profiles:

| Profile | Triggers | Extra checks |
|---|---|---|
| Frontend | `frontend/`, `*.tsx`, `*.ts`, route/UI files | React stale closures, null/undefined cascades, route/render regressions, preview smoke evidence. |
| Backend/API | `backend/`, API routes, services | Response schema drift, async error handling, cancellation/status consistency, path traversal. |
| Trading/math | scoring, strategy, portfolio, metrics, simulation | Ghost parameters, look-ahead leakage, NaN/Inf, unit/scale drift, cross-stage formula drift. |
| Data | candles, providers, archive, ingestion, cache | Deduplication, timestamp continuity, provider shape drift, cache poisoning, boundary gaps. |
| Admin/ops | admin, deployment, env, auth, infra | Auth/authorization, env safety, deployment boundaries, preview ownership. |
| LLM/Nome | chat, context, prompt, memory, assistant | Prompt injection, context sanitization, raw transcript leakage, unbounded resource growth. |
| Browser QA / DevTools | browser-visible frontend or full-stack checkpoints | Resolved preview URL load, console errors, failed network requests, screenshot evidence, accessibility snapshot, optional Lighthouse/performance trace. |

Hotspot files require explicit ownership evidence: lockfiles, DB migrations, shared schema files, route registries, deployment files, env templates, and high-churn central config.

Browser QA / DevTools is optional by default. Use it when UI behavior, routing, accessibility, performance, extension integration, or preview-only regressions are part of the checkpoint. Prefer an isolated/headless Chrome DevTools MCP profile with usage statistics and CrUX disabled. Do not enable WebMCP or extension debugging unless the task explicitly needs it.

## Phase 4. Final Bug-Check

Entry criteria:
- The verifier has approved the final implementation checkpoint.
- The coder reports that no scoped code remains.

Actions:
1. Run the `bug-check` skill over the final branch diff or touched-file scope without asking for another approval.
2. Use the Evonome adversarial themes from `docs/prompts/adversarial-code-review.md` for trading, data, frontend, API, and LLM-adjacent silent failures.
3. Record findings, missing tests, and the reviewed scope in the verifier report or decision log.
4. Use `revision_requested` for bounded fixes the coder should apply.
5. Use `approved` only when no blocking bug-check findings remain.
6. Stop before PR creation; the user owns that decision.

Exit criteria:
- Final bug-check status is recorded and the next actor is clear.

## Output Shape

Return a concise verifier status:

- Decision: `approved | revision_requested | rejected | needs_human`
- Checks: `<what was verified>`
- Findings: `<finding IDs or none>`
- Required coder action: `<bounded action or none>`

Never include raw transcripts, secrets, or provider configuration in committed artifacts.
