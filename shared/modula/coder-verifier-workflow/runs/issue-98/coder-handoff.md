# Coder Handoff — Issue #98

## Scope
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/98
- Branch: `feat/prd-studio-planner-gate-recovery-98`
- Initial base synced to `origin/main` before coding (`3d16f13`).
- After Lane B #99 merged, fetched and fast-forwarded to latest `origin/main` (`de79ed1`), then restored #98 WIP.
- Pre-existing dirty files before coding: none.

## Checkpoints
1. Gate flexibility for `agent_routing` / `per_agent_prompts` — approved by verifier revision 2.
2. Planner prompt/schema field shapes — approved by verifier revision 1.
3. Recovery route/UI for Fix with planner & Execute — approved by verifier revision 2.
4. Failure paths for unavailable planner, timeout, unchanged brief, still-invalid brief — approved by verifier revision 2.
5. Launch metadata auto-fix and final validation — implemented after Lane B #99 landed; pending final verifier review.

## Changed files
- `pipeline-diagram/board.html`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchMetadataFix.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/planningBrief.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/launchMetadataFix.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/planningBrief.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-98/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-98/lane-b-conflict-note.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-98/verifier-report.md`

## Implementation summary
- Gate now accepts non-empty string, object, or array for `agent_routing` and `per_agent_prompts`; missing/empty values still fail.
- Planner launch instructions now enumerate `planning-brief.v1` fields and explicit required shapes.
- Added `POST /groups/:id/fix-and-execute-authoring` for PRD-planning groups.
- Recovery route sends exact gate feedback to the live planner pane, waits for planner-authored brief changes, revalidates, returns changed-field before/after summary, and launches downstream authoring only after valid recovery.
- Recovery failure paths stop safely for missing confirmation, unavailable planner, unchanged/timeout, and still-invalid recovered briefs.
- Added Term UI action `Fix with planner & Execute`, including before/after success notice and remaining gate feedback on failures.
- Added `POST /prds/:issueNumber/fix-launch-metadata` for one-click launch metadata repair.
- Launch metadata repair reads the canonical issue body, active Project item, and Project field metadata; prefers body labels `Proposed working branch`, `Worktree`, and `Base branch`; otherwise derives an issue-numbered safe branch and deterministic worktree path from active project settings.
- Launch metadata repair writes `Working Branch`, `Worktree Path`, and `Base Branch` when the field exists, read-backs `Working Branch` / `Worktree Path`, queues a board regeneration refresh, and never launches agents.
- Launch metadata read-back now matches real `gh project item-list` keys that preserve spaces after lowercasing the first character, with camelCase fallback for compatibility.
- Board launch setup now shows **Auto-fix launch metadata** only for missing launch-context `Working Branch` / `Worktree Path`, updates the in-memory launch context after success, and re-enables launch without requiring manual GitHub field surgery.

## Validation run
- `cd term-control-center && npm ci` — passed, installed local test dependencies.
- `cd term-control-center && npm test -- tests/planningBrief.test.ts tests/launchPlan.test.ts` — passed (438 tests; npm script ran the full suite despite file arguments).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/server.test.ts --test-name-pattern='fix-and-execute|PRD planning execute fails closed|frontend PRD planning execute'` — passed (45 tests; Node invocation still ran the full server test file).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/termBasePath.test.ts tests/planningBrief.test.ts tests/launchPlan.test.ts` — passed (50 tests).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed (2 tests).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts` — passed (32 tests).
- `cd term-control-center && npm run typecheck` — passed.
- Steward hygiene review before launch metadata work — clean; no cleanup needed.
- `cd term-control-center && npm run typecheck && npm test && npm run build` — passed. Full test suite: 447/447 passed. Build completed with existing Vite warnings about non-module scripts and chunk size.
- Steward hygiene review after launch metadata work — placement clean; removed ignored `term-control-center/build/` and `term-control-center/dist/`; accounted for `verifier-report.md` in changed files.
- Addressed verifier finding `A98-FINAL-002` by aligning Project item field-key read-back with real `gh project item-list` output and updating launch metadata tests to use `working Branch` / `worktree Path` / `base Branch` keys.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/launchMetadataFix.test.ts` — passed (2 tests) after `A98-FINAL-002` fix.
- `cd term-control-center && npm run typecheck && npm test && npm run build` — passed again. Full test suite: 447/447 passed. Build completed with existing Vite warnings about non-module scripts and chunk size.

## Unresolved risks
- Board-level launch metadata repair touches `pipeline-diagram/board.html` after Lane B #99 landed. This was necessary to complete canonical issue #98 item 4.
- No manual browser/GitHub Project live mutation smoke test was run; automated tests cover the derivation/write/read-back behavior with faked `gh` responses and static board wiring.

## Lane B overlap/conflict notes
- Initial conflict note was written before Lane B #99 landed: `dev-plans/agentops/coder-verifier-workflow/runs/issue-98/lane-b-conflict-note.md`.
- After #99 merged and local main was updated, #98 was fast-forwarded to `origin/main`; no merge conflicts remained.
- Final implementation touches `pipeline-diagram/board.html` but does not edit `term-control-center/server/adminPipeline.ts`, `term-control-center/server/adminRoutes.ts`, or `term-control-center/server/adminClient.ts`.
