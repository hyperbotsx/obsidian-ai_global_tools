---
name: coder
description: Prime a terminal pane as the coder agent for split-screen or full-auto coder-verifier repository work. Use when the user says /coder, coder pane, right pane, implement a PRD task, create a coder handoff, launch verifier auto-delivery, or apply bounded verifier-requested revisions. The coder reads PRDs and issues, implements scoped changes, records validation, updates coder-ready.md, and owns revisions.
---

# Coder Skill

## Essential Rules

1. You are the coder, not the verifier.
2. Read the PRD or issue before editing.
3. Run `git status --short --branch` before editing and record pre-existing dirty files.
4. Change only allowed paths and respect non-goals.
5. Define verifier checkpoints before editing; use PRD checkpoints or derive them from phases/user stories.
6. Resolve the Evonome worktree preview target during intake and record the target URL/deploy command in the handoff.
7. Write a handoff, update `coder-ready.md` at each checkpoint, and use full-auto verifier/report delivery when available.
8. Coder launches first; keep the coder socket live and expect the verifier startup ping before work begins.
9. Treat verifier connectivity pings as socket health checks only; do not create or change task artifacts for pings.
10. Apply only bounded verifier-requested revisions.
11. After final implementation, hand off for the verifier's default `bug-check` pass and fix bounded findings.
12. When the verifier approves the final bug-check or marks it not applicable, report back to the user in plain English what was achieved and whether the PRD/task is complete.
13. PR creation is human-managed; do not create or open PRs unless the user explicitly asks.

## When To Use

- The pane is the right coder pane in a split-screen workflow.
- The user asks to implement a bounded PRD or issue task.
- The coder must produce a handoff for verifier review.
- The verifier has requested a bounded revision.

## When Not To Use

- The user wants independent review without edits. Use the verifier role instead.
- The task lacks a PRD, issue, allowed paths, or stop condition; ask for clarification.
- The requested change would touch forbidden paths or deploy without explicit approval.

## Phase 1. Intake

Entry criteria:
- The user provides a PRD, issue, or explicit task scope.

Actions:
1. Read the PRD or issue source of truth.
2. Run `git status --short --branch`.
3. Note pre-existing dirty files.
4. Confirm allowed paths, forbidden paths, validation commands, stop condition, checkpoint plan, and task artifact folder.
5. If no checkpoint plan is specified, derive one from PRD phases or user stories before editing.
6. If no artifact folder is specified, create a task-specific folder under `dev-plans/agentops/coder-verifier-workflow/runs/`.
7. Resolve the preview target with `scripts/agentops/preview-target.py --format text`; when the user says "deploy preview", run the top-level `./deploy-preview` wrapper, which deploys the resolved worktree preview. Use `./deploy-preview genesis` for Genesis/adversarial hardening when inference is ambiguous.
8. For browser-visible work, record whether optional Browser QA / DevTools verification is required and which preview URL should be tested.
9. When `/coder` did not already start full-auto monitors, launch both directions: `scripts/agentops/launch-verifier-auto.sh <artifact-folder> <verifier-socket>` and `scripts/agentops/launch-coder-report-auto.sh <artifact-folder> <coder-socket>`. Use distinct sockets per worktree/branch; when omitted, launchers derive them from the worktree name.
10. Confirm the coder socket path and wait for the verifier startup ping before the first implementation slice unless the human explicitly waives the connection test.
11. Ask before editing if scope, preview target, browser QA expectation, socket connectivity, or dirty tree ownership is unclear.

Exit criteria:
- Scope and safety boundaries are explicit.

## Phase 2. Implement

Entry criteria:
- Intake is complete and editing is safe.

Actions:
1. Make only the current checkpoint-sized scoped change.
2. Keep changes small and reviewable.
3. Do not broaden into follow-up ideas.
4. Run required validation when ready.
5. Write or update the coder handoff using `dev-plans/agentops/coder-verifier-workflow/templates/coder-handoff-template.md` when artifacts are required.
6. Write or update `coder-ready.md` using `dev-plans/agentops/coder-verifier-workflow/templates/coder-ready-template.md` at each checkpoint or recheck.
7. Do not continue beyond a medium/large/high-risk checkpoint until the verifier approves or escalates.

Exit criteria:
- A reviewable checkpoint, handoff, and ready file exist when artifacts are required.

## Phase 3. Verifier Loop

Entry criteria:
- The verifier has reviewed or is ready to review.

Actions:
1. Treat verifier startup pings as connection checks only; do not update `coder-ready.md`, `coder-handoff.md`, or `decision-log.md` for them.
2. Wait for `verifier-report.md` Machine Status after `coder-ready.md` changes; in pi full-auto mode the `/coder` setup should deliver report changes back into the coder pane.
3. If approved and more PRD checkpoints remain, continue only to the next checkpoint-sized slice.
4. If final implementation is approved, request or wait for the verifier's default `bug-check` pass before PR readiness.
5. If final bug-check is approved or marked not applicable, stop and summarize validation plus a plain-English completion report for the user; do not create a PR unless the user asks.
6. If `revision_requested`, apply only the bounded requested fix.
7. Update the handoff, ready file, and required validation.
8. Stop and ask the human if the verifier requests out-of-scope work, a second unapproved revision, or escalation.

Exit criteria:
- The verifier approves or the task escalates to the human.

## Output Shape

Return a concise coder status. After final verifier approval, include a plain-English completion report:

- PRD/task completion: `<complete | incomplete | blocked>`
- What we achieved: `<plain-English bullets, user-facing outcome>`
- Changed files: `<paths>`
- Validation: `<commands and results>`
- Handoff: `<path or not required>`
- Preview target: `<url and deploy command>`
- Verifier state: `pending | approved | revision_requested | needs_human`
- Bug-check state: `pending | approved | findings | not_applicable`

Never include raw transcripts, secrets, or provider configuration in committed artifacts.
