# Coder handoff — Issue #179 Observable Kody Review Sessions

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/179
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-179`
- Branch: `prd/observable-kody-review-sessions-179`
- PRD status: GitHub issue labels include `status:approved`; human instructed coder to start now.

## Pre-edit status
- `git status --short --branch`: `## prd/observable-kody-review-sessions-179...origin/main`
- Pre-existing dirty files: none.
- Memory disabled per launch instruction; memory not used.

## Research-first consult
Completed with `researcher` on 2026-06-30 before adapter work.

Summary: implement GitHub artifact ingestion as the stable default; treat private Kodus/Kody API as optional, version-gated, schema-validated, timeout-bounded, and fail-closed. Kody supports manual `@kody start-review`, uses GitHub webhooks for issue comments / PR reviews / PR review comments / PRs / pushes, and emits inline comments plus optional PR-level summaries and reactions. Public Kodus API stability is unclear: OpenAPI docs endpoint returned 404, and deployment-local OpenAPI is disabled by default in `.env.schema`.

Sources cited by researcher:
- https://docs.kodus.io/how_to_use/en/code_review/flow
- https://docs.kodus.io/how_to_deploy/en/platforms/github/github_webhook
- https://docs.github.com/en/rest/pulls/reviews?apiVersion=2022-11-28
- https://docs.github.com/en/rest/pulls/comments?apiVersion=2022-11-28
- https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28
- https://docs.github.com/en/rest/reactions/reactions?apiVersion=2022-11-28
- https://github.com/kodustech/kodus-ai/blob/main/.env.schema

## Scope boundaries
Allowed:
- Kody review state/types/routes and UI controls.
- Activity Center `kody_review` source mapping.
- GitHub comment/review artifact adapter boundaries.
- Bounded fix-loop launch plumbing with explicit operator action.
- Docs/tests for privacy, state, finding import, and Activity Center behavior.

Forbidden:
- PR creation, merge, deployment, branch protection/required-check changes, auto-approval/request-changes, automatic debt issues, secrets/raw prompts/raw transcripts/raw terminal logs/plaintext attach tokens/env dumps, product-code edits by Kody Coordinator.

Stop condition:
- Stop after verifier checkpoint approval for this slice, then continue next bounded slice or fix verifier findings.

## Verifier checkpoints
1. Kody state, GitHub artifact import, Completed row controls, Activity Center visibility, privacy-safe persistence, and explicit fix-loop launch plumbing. Current checkpoint.
2. Follow-up hardening for live review-session attach/re-review loop details and any verifier findings.
3. Steward structure/hygiene review before final bug-check because new modules/docs/artifacts were added.
4. Final verifier bug-check.

## Verifier checkpoint status
- Checkpoint 1 revision 1: revision requested (F179-R1-001 through F179-R1-005).
- Checkpoint 1 revision 2: revision requested (F179-R2-001).
- Checkpoint 1 revision 3: approved with zero open findings.
- Final bug-check revision 4: revision requested (F179-R4-001 through F179-R4-004).
- Final bug-check fix review revision 5: revision requested (F179-R5-001, F179-R5-002).
- Final bug-check fix review revision 6: approved; bug-check passed with zero open findings.
- Post-approval hardening checkpoint started after human asked to continue one more bounded pass before PR.

## Current checkpoint implementation
- Added private term-control Kody review state store in `term-control-center/server/kodyReview.ts`.
- Added session statuses, finding classification/status vocabulary, normalized/deduped GitHub artifact import, selected actionable finding filtering, loop brake count, and webhook signature validation helper.
- Added term routes:
  - `GET /kody-review/sessions`
  - `POST /completed-work/kody-review`
  - compatibility `POST /completed-work/kodus-review`
  - `POST /kody-review/import`
  - `POST /kody-review/fix-loop`
  - `POST /kody-review/dismiss`
  - `POST /kody-review/needs-human`
- Completed page now loads Kody session state, highlights active Kody rows, shows state labels, imports findings, launches explicit actionable fix loop, dismisses/needs-human sessions, and opens attached group or latest artifact link from the Kody control.
- Activity Center now exposes `source="kody_review"` with PRD bucket mapping required by the PRD.
- Added privacy/retention docs in `docs/kody-review-sessions.md`.

## Changed files
- `pipeline-diagram/completed.html`
- `src/agentops_harness/activity_center.py`
- `src/agentops_harness/activity_center_sources.py`
- `src/agentops_harness/activity_center_kody.py`
- `term-control-center/server/index.ts`
- `term-control-center/server/kodyReview.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/tests/completedStatic.test.ts`
- `term-control-center/tests/kodyReview.test.ts`
- `tests/unit/test_activity_center.py`
- `docs/kody-review-sessions.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-179-observable-kody/coder-handoff.md`

## Validation
Passed:
- `npm ci` in `term-control-center` installed locked dependencies.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/kodyReview.test.ts tests/completedKodusReview.test.ts tests/completedStatic.test.ts` — 18 tests passed after final bug-check fixes.
- `PYTHONPATH=src pytest tests/unit/test_activity_center.py -q` — 10 passed.
- `cd term-control-center && npx tsc --noEmit --module NodeNext --moduleResolution NodeNext --target ES2022 --skipLibCheck --esModuleInterop server/kodyReview.ts server/completedKodusReview.ts` — passed.
- `python3` AST KISS check for `src/agentops_harness/activity_center_kody.py` — passed, no functions over 20 lines.
- `git diff --check` — passed.

## Revision 2 fixes for verifier findings
- F179-R1-001: Kody importer now accepts Kody/Kodus-authored artifacts only and explicitly ignores `@kody start-review`; regression covered in `kodyReview.test.ts`.
- F179-R1-002: Fix-loop launch task now carries privacy-safe selected-finding repair context in task details; `launchPlan.ts` includes task details in coder/verifier prompts; static regression checks wiring.
- F179-R1-003: Trigger failures now update any persisted session to `needs_human` with redacted failure reason and failed webhook health.
- F179-R1-004: Finding fingerprints no longer include transient artifact URLs; regression import includes same finding with different URLs and dedupes.
- F179-R1-005: Split Activity Center Kody item construction into smaller helpers and ran AST KISS check.
- F179-R2-001: Removed existing implementation group reuse from Kody fix-loop launch. Each explicit Kody fix loop now starts a Kody-specific coder/verifier group with selected-finding repair context in task details so reused generic groups cannot miss scope.

## Final bug-check fixes
- F179-R4-001: Re-imported selected/fixed findings now become `survived_re_review`; repeated survivors at loop count >= 2 move the session to `needs_human` with a brake reason.
- F179-R4-002: `/kody-review/fix-loop` now catches launch/scope failures, updates the session to `needs_human` when possible, and returns bounded JSON.
- F179-R4-003: Completed row Kody control now resolves live `/groups` details before opening a stored `groupId`, avoiding empty-pane attach URLs.
- F179-R4-004: Kody artifact attribution now uses a strict bot login allowlist (`KODY_BOT_LOGINS` override or known defaults) instead of spoofable substring matching.
- F179-R5-001: `survived_re_review` actionable findings are selectable for a human-continued fix attempt until the loop brake is reached; Completed row enablement matches.
- F179-R5-002: Stored Kody group opening now requires at least one pane with both `sessionId` and `attachToken`; otherwise the UI shows the stale/unavailable message and does not open a broken attach URL.

## Post-approval hardening pass
- Added `Kody details` Completed-row action for structured session metadata: PR URL, branch, requester, status, created/updated time, gateway/webhook health, latest artifact, and finding summary.
- Updated docs to describe the Kody details view.
- Validation after hardening: targeted Kody term-control tests still pass (18), Activity Center pytest still passes (10), and `git diff --check` remains clean.

## Steward hygiene review
- Steward pre-final review returned `cleanup_recommended` for one stale doc wording issue.
- Cleanup applied: `docs/kody-review-sessions.md` now says fix loops launch a Kody-specific coder/verifier implementation group, matching the verifier-approved no-reuse behavior.
- Steward reported placement clean for new Activity Center module, term-control server/test module, docs, and run artifact folder.

Known validation blockers / pre-existing environment failures:
- `cd term-control-center && npm run typecheck` fails on pre-existing TypeScript project issues before this slice is typechecked fully, notably `tests/contextRenewal.test.ts` importing `../../pi-packages/.../policy.ts` outside `rootDir` and without `allowImportingTsExtensions`.
- `cd term-control-center && npx tsc --noEmit ... server/index.ts` still reports existing broad strict-union errors in unrelated server modules; no new Kody-specific errors were shown before those existing errors.
- An attempted broad `npm test -- --test-name-pattern=...` did not filter as expected and timed out after running many unrelated tests; failures were in unrelated launch/project-action/server tests.

## Risks / notes for verifier
- The first slice creates structured session state and opens an attached coder/verifier group for fix loops. The initial Kody review trigger itself does not launch a dedicated terminal pane; the UI opens the latest GitHub artifact until a fix-loop group exists.
- Private gateway support remains bounded to the existing webhook relay path; no private API client was added because researcher found public Kodus API stability unclear.
- No PR, merge, deployment, branch protection, required-check, approval, request-changes, or debt issue automation was added.
