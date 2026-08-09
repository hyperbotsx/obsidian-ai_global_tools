# Coder Handoff — PRD #46 Multi-Project Admin Management and Project Switching

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/46
- Branch: `prd/multi-project-admin-management-project-switching-46`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Pre-edit state
- `git status --short --branch`: `## prd/multi-project-admin-management-project-switching-46...origin/main`
- Pre-existing dirty files: none.
- Issue state/labels: open PRD with `status:approved`.
- Implementation preflight: worktree root and remote match `hyperbotsx/agentops-harness`; branch ends in `-46`.

## Allowed paths / scope
- `term-control-center/server/`, `term-control-center/shared/`, `term-control-center/src/`, and `term-control-center/tests/` for project config, admin APIs/UI, active project state, launch/session/completion metadata, and tests.
- `pipeline-diagram/` for board/dropdown/project-aware launch and generator context.
- `docs/` for multi-project setup/security notes.
- `config/templates/secure-access/` only if new hosted routes outside `/admin/` or `/api/admin/` are introduced.
- Run artifacts under this folder.

## Forbidden scope
- No GitHub repository/Project creation, mutation, delete, archive, linking, PR creation, merges, deployment, trading, backtesting, or local sync automation.
- No plaintext credentials, provider tokens, GitHub tokens, cookies, CSRF tokens, raw identity headers, raw transcripts, or secrets in project config/audit/coms.
- Do not weaken PRD #40 hosted Authentik/WebAuthn enforcement or trust direct client-supplied `X-Authentik-*` headers.
- Do not hardcode Project 2, tracker `#862`, field names absent from the selected project, machine-specific defaults, or one repository as the only supported project.

## Required validation
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run test`
- `npm --prefix term-control-center run build`
- `python3 -m py_compile pipeline-diagram/generate.py` if the generator changes.
- `python3 config/templates/secure-access/validate-secure-access-templates.py` if secure-access templates or route inventory change.
- `git diff --check`

## Researcher consult summary
Mandatory freshness consult completed before implementation edits (2026-06-20).
- GitHub Projects v2: use read-only GraphQL/REST metadata discovery; `read:project` is sufficient for queries; validate user/org owner, number, URL, title, closed state, node id, and linked repositories; prefer GraphQL node id over deprecated database id; do not call mutation APIs.
- Term Control Center: add `projectId` as backward-compatible metadata on config, task/launch context, groups, persisted groups, completion/action state, and UI filters; do not embed it in session IDs or attach tokens; legacy groups without `projectId` should load as default/legacy; switching projects must not kill existing groups.
- Route policy: no PRD #40 template/inventory update needed if new admin APIs stay under `/api/admin` and UI under `/admin`; endpoints outside those prefixes require secure-access updates.
- Sources cited by Researcher: GitHub Docs for Projects API/GraphQL ProjectV2, GitHub REST Projects v2 docs, local `docs/runbooks/secure-access-deployment.md`, and local Term Control files.

## Checkpoint plan
1. Existing-plan and migration / project config model: multi-project store, legacy PRD #30 settings migration, stable project IDs, atomic persistence, validation, project-scoped audit summaries, and compatibility projection.
2. Admin CRUD UI/API: list/create/detail/edit/archive/unarchive with disabled invalid states and tests.
3. Security: auth/CSRF/proxy-header spoofing and route-policy alignment for admin additions.
4. Active project API/dropdown: safe metadata endpoint, active selection persistence, top-left dropdown wiring, archived/missing behavior.
5. Launch/session/completion integration: selected project context on `/launch-context`, `/launch`, groups, persisted sessions, completions, fail-closed invalid selected project.
6. Board/pipeline integration and isolation: per-project board/generator data, refresh isolation, notifications/coms/action-center namespace separation.
7. PRD #32/#45/profile integration: selected-project hooks for action config, PRD Studio, CEO/Approval Review metadata resolution without hardcoded Project 2/tracker `#862`.
8. Final bug-check and regression hardening.

## Current checkpoint
- Checkpoint 5 ready for verifier review: board/pipeline project integration, selected-project isolation, and PRD #32/#45/profile integration hooks.

## Implementation summary — checkpoint 1
- Added `term-control-center/server/adminProjects.ts` with a versioned multi-project registry at `admin-projects.json`.
- Added stable URL/path-safe project IDs with reserved-name rejection and uniqueness checks.
- Migrates existing PRD #30 `admin-settings.json` into a default active project without deleting the legacy settings file.
- Keeps a backward-compatible active settings projection in `admin-settings.json` after saves so existing generator/refresh paths keep working during the transition.
- Active PRD authoring config now resolves through the project registry, validates before launch, and still fails closed for missing/invalid saved settings.
- Project-scoped audit summaries include `projectId`, safe settings metadata, validation status, and no passwords/session data.

## Implementation summary — checkpoint 2
- Added authenticated project CRUD endpoints under `/api/admin/projects` for list, detail, create, update, archive, and unarchive.
- Added project list/detail/create/edit/archive controls to the existing `/admin/` page without adding routes outside `/admin` or `/api/admin`.
- Project create/update reuses the existing settings validation path and rejects duplicate/reserved IDs, unsafe IDs, invalid paths/repos/projects/refs, and wrong remotes before persistence.
- Archive/unarchive emits project-scoped audit events; archiving the active project is blocked until active switching lands so archived projects cannot remain active/selectable.
- Existing `/api/admin/settings` compatibility remains for active settings reads while the admin UI now saves via project-specific CRUD.

## Changed files
- `term-control-center/server/adminProjects.ts`
- `term-control-center/server/adminProjectSelection.ts`
- `term-control-center/server/adminConfig.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/adminAssets.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/completionStore.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/completion.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/admin.test.ts`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/board.html`
- `pipeline-diagram/generate.py`
- `pipeline-diagram/review-notify.js`
- `pipeline-diagram/public/projects`
- `docs/agentops-multi-project-admin.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-46-multi-project-admin-switching/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-46-multi-project-admin-switching/review-request-r1-project-config-migration.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-46-multi-project-admin-switching/review-request-r2-admin-crud.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-46-multi-project-admin-switching/review-request-r3-admin-crud-fixes.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-46-multi-project-admin-switching/review-request-r4-active-project-dropdown.json`

## Acceptance/checkpoint mapping
- Existing single-project settings migrate to a default active project: covered by `legacy admin settings migrate into a default project without losing settings`.
- Stable project ID model: default ID derives from repository slug (`agentops-harness` in tests), validates URL/path-safe syntax, reserved names, and uniqueness on registry load.
- Atomic persistence: project registry and compatibility settings projection use temp-file-plus-rename writes.
- Validation/fail-closed behavior: saves validate; migrated legacy settings carry validation status; PRD authoring launch validates active settings before use.
- Audit privacy: migration/update audit entries include `projectId` and safe metadata, with regression checks excluding passwords/session-cookie names.
- Admin CRUD: covered by `admin project CRUD creates edits archives and unarchives project records` for authenticated create/list/detail-style persistence through list, edit, duplicate/invalid rejection, archive/unarchive, active archive refusal, and audit privacy.
- Admin UI: `/admin/` now renders project list and project form controls; API tests cover server behavior and existing admin HTML smoke checks remain passing.
- Security/route alignment: all new endpoints are under `/api/admin` and use `requireAdmin`; mutations use `requireCsrf`.

## Revision 3 fixes for checkpoint 2 findings
- `CP2-001`: Project summaries and `/api/admin/projects` responses now include `updatedAt`; admin rows render `Updated <timestamp>`; CRUD test asserts `updatedAt` is present for all listed projects.
- `CP2-002`: Active-project archive buttons are disabled in the admin UI with `Switch before archive`/title text while the backend continues to reject active archive attempts.
- `CP2-003`: Removed the now-unused `saveMessage()` helper after the admin UI save path moved to project CRUD.

## Implementation summary — checkpoint 3
- Added safe active-project selection APIs under `/api/admin/project-selection`.
- Safe selection metadata includes only `projectId`, display name, repository, GitHub Project URL/number, and updated time; local paths/worktree roots stay out of the dropdown payload.
- Active project selection validates the target project, rejects archived/invalid projects, writes the active compatibility settings projection, and emits project-scoped selected/rejected audit events.
- Wired the static board/pipeline/WIP global nav and Term React top nav to render an active-project dropdown for authenticated admins when multiple valid unarchived projects exist.
- Switching the dropdown calls the CSRF-protected selection API and reloads the current page so subsequent launch/context requests resolve through the selected project.

## Revision 5 fix for checkpoint 3 finding
- `CP3-001`: Split active-project selection helpers into `term-control-center/server/adminProjectSelection.ts`; `adminProjects.ts` is now 279 lines and the new selection module is 43 lines, with behavior unchanged.

## Implementation summary — checkpoint 4
- Added optional `projectId` to launch task context and completion signal types.
- `/launch-context` and PRD authoring/planning launches now include the active project ID resolved from server-side project config.
- Launched groups persist/carry `task.projectId`; task context files now include Project ID.
- Reusable group matching and completion identity/notification keys include `projectId` with `legacy-default` fallback for existing sessions/states.
- Completion event reconciliation includes `projectId` so spoofed or wrong-project completion events fail closed.
- Board launch payload now preserves chip `projectId` and avoids hardcoded repository/Project fallback when chip metadata is absent.

## Revision 7 fix for checkpoint 4 finding
- `CP4-001`: Synthetic completed group IDs and approved-report discovery now include `projectId || legacy-default`; report discovery requires matching report project metadata and legacy reports only match legacy tasks.
- Added regression coverage proving two tasks with the same issue/repo/worktree/branch but different `projectId` get different synthetic completion IDs and legacy reports do not complete non-legacy project tasks.

## Implementation summary — checkpoint 5
- Board generator now reads `AGENTOPS_PROJECT_ID`, embeds `projectId`/Project URL in board, pipeline, and WIP data, and writes active compatibility files plus project-scoped copies under `pipeline-diagram/projects/<projectId>/`.
- Active project selection refreshes pipeline data for only the selected project and passes `AGENTOPS_PROJECT_ID`; the public static root exposes the project-scoped output directory via `pipeline-diagram/public/projects`.
- Board chips include `projectId`; PRD Studio draft context carries selected `projectId`; live session lists, running-chip marking, and completion notification polling filter by the active project while keeping other-project terminal groups alive.
- Completion notifications/action-result records now carry `projectId`; notification de-duplication includes project identity for completion and action-result keys.
- Added `docs/agentops-multi-project-admin.md` documenting migration, switching, scoped board outputs, PRD #32 action-configuration handoff via project-scoped completion/action state, PRD #45 selected-project PRD Studio context, and security boundaries.
- Removed Project 2/tracker-specific generated issue text from the generator's push body; CEO/Approval review mutation code already resolves profile project owner/number and live Project fields.

## Revision 9 fix for checkpoint 5 finding
- `CP5-001`: Active project selection from `/api/admin/project-selection` is now authoritative for board session and completion filters once loaded; generated `PIPELINE_PROJECT_ID` is only the bootstrap fallback.
- `global-nav.js` dispatches an `agentops-active-project` event after reading active selection; board handlers re-render live sessions and re-poll completions without requiring pipeline refresh success.
- Added a static regression test covering stale generated project IDs versus authoritative active selection for sessions and completions.

## Validation results
- `npm --prefix term-control-center run typecheck`: passed.
- `cd term-control-center && HOME=$(mktemp -d) node --import tsx --test --test-concurrency=1 tests/admin.test.ts`: passed, 14 tests.
- `node --check pipeline-diagram/global-nav.js`: passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion-server.test.ts`: passed, 8 tests.
- `npm --prefix term-control-center test`: passed, 200 tests.
- `npm --prefix term-control-center run build`: passed.
- `python3 -m py_compile pipeline-diagram/generate.py`: passed.
- `node --check pipeline-diagram/global-nav.js`: passed.
- `node --check pipeline-diagram/review-notify.js`: passed.
- `git diff --check`: passed.

## Verifier status
- Checkpoint 1 approved by verifier at revision 1 (`bug_check_status: not_applicable`).
- Checkpoint 2 revision 2 requested fixes: `CP2-001`, `CP2-002`, `CP2-003`.
- Checkpoint 2 approved by verifier at revision 3 (`bug_check_status: not_applicable`).
- Checkpoint 3 revision 4 requested fix: `CP3-001`.
- Checkpoint 3 approved by verifier at revision 5 (`bug_check_status: not_applicable`).
- Checkpoint 4 revision 6 requested fix: `CP4-001`.
- Checkpoint 4 approved by verifier at revision 7 (`bug_check_status: not_applicable`).
- Checkpoint 5 revision 8 requested fix: `CP5-001`.
- Checkpoint 5 approved by verifier at revision 9 (`bug_check_status: not_applicable`).
- Steward pre-final hygiene review approved with no findings.
- Final verifier bug-check approved at revision 10 (`bug_check_status: passed`).
