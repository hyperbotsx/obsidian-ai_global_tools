# Coder Handoff — PRD #30 Simple Admin Login and Configuration Panel

## Source of truth
- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/30
- Branch: `prd/simple-admin-login-config-panel-30`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Pre-edit state
- `git status --short --branch`: `## prd/simple-admin-login-config-panel-30...origin/main`
- Pre-existing dirty files: none.

## Allowed paths / scope
- Term Control server endpoints, auth/session/config persistence helpers, and tests under `term-control-center/`.
- Static board/admin UI surfaces under `pipeline-diagram/` only as needed for `/admin/` discovery and Create PRD workspace resolution.
- PRD #40 route-policy docs/templates/tests only if needed to keep `/admin/` and `/api/admin/` aligned with `agentops-admin`.
- Run artifacts under this folder.

## Forbidden scope
- No plaintext password storage.
- No unauthenticated admin settings exposure.
- No browser localStorage secrets, GitHub token storage, PR creation, merge, deploy, trading, or backtesting.
- No live Authentik, nginx, firewall, DNS, certificate, Docker, systemd, or identity-provider mutation.
- Do not replace PRD #40 Authentik/WebAuthn hosted perimeter.
- Do not trust direct client-supplied `X-Authentik-*` headers.

## Researcher consult summary
Mandatory freshness consult completed before implementation edits.

- Prefer explicit auth modes: local bootstrap login for loopback/local setup; hosted mode must require Authentik/WebAuthn perimeter and proxy identity only from a trusted reverse-proxy boundary.
- Password hashing: Argon2id is preferred; Node built-in `scrypt` is acceptable fallback when avoiding new native dependencies. Use per-password salts and cost factors appropriate for low-volume admin login.
- Bootstrap: never ship default credentials. Create admin only when no admin exists, through loopback/bootstrap-token style setup or local operator-supplied password. Store only password hash and lock bootstrap after creation.
- Sessions: opaque random server-side session IDs, rotate after login/bootstrap, idle expiry about 30 minutes, absolute expiry 8–12 hours, logout destroys server session and clears cookie.
- Cookies: `HttpOnly`, `SameSite=Strict`, no `Domain`, narrow path. Use `Secure` on HTTPS/hosted; plain HTTP only for loopback local mode.
- CSRF: cookie-auth unsafe methods need CSRF protection and same-origin checks; disable broad CORS.
- Audit: log bootstrap/auth/settings/logout/rejection lifecycle without passwords, cookies, session IDs, CSRF tokens, tokens/JWTs, raw Authentik headers, raw transcripts, or private identity data.
- Proxy boundary: hosted mode may trust `X-Authentik-*` only when request comes from a configured trusted proxy and reverse proxy clears/overwrites inbound identity headers; app must fail closed otherwise.
- Sources cited by Researcher: OWASP Password Storage, Session Management, CSRF Prevention, Logging cheat sheets; NIST SP 800-63-4 (Aug 2025); MDN Set-Cookie (Jun 15 2026); Express behind proxies; Authentik proxy provider docs.

## Implementation summary
- Added local/bootstrap admin auth and session implementation:
  - `term-control-center/server/adminAuth.ts`
  - no default credentials;
  - loopback-only first admin bootstrap in local mode;
  - salted Node `scrypt` password verifier (`N=32768`, `r=8`, `p=1`);
  - server-side sessions with `HttpOnly`, `SameSite=Strict`, optional `Secure`, idle/absolute expiry, logout, and CSRF token checks.
- Added settings persistence and validation:
  - `term-control-center/server/adminConfig.ts`
  - local work path, GitHub repository, worktrees root, worktree naming, PRD authoring workspace, and typed `extra` settings;
  - atomic writes to the Term Control state directory;
  - audit JSONL entries that summarize settings without secrets;
  - repository validation now uses a matching remote parser that supports dotted repo names.
- Added admin routes/UI:
  - `term-control-center/server/adminRoutes.ts`
  - readable static admin assets in `term-control-center/server/adminAssets.ts`
  - `/admin/`, `/api/admin/session`, `/api/admin/bootstrap`, `/api/admin/login`, `/api/admin/logout`, `/api/admin/settings`, `/api/admin/audit`.
- Integrated PRD authoring launches with saved admin config:
  - `term-control-center/server/index.ts`
  - PRD authoring launch context and `/launch` require saved, validated admin configuration;
  - absent or invalid configured authoring workspaces fail closed instead of falling back.
- Added Admin navigation link in `pipeline-diagram/global-nav.js` and `term-control-center/src/App.tsx`.
- Added `docs/admin-configuration.md` with local setup, hosted Authentik/WebAuthn boundary, audit, and authoring workspace behavior.
- Added tests in `term-control-center/tests/admin.test.ts`, updated existing authoring tests to seed validated admin config, and added route-policy assertions in `term-control-center/tests/nginxProxy.test.ts`.

## Revision 2 fixes for verifier findings
- `V30-R1-001`: PRD authoring launch/context now require saved validated admin settings. Added tests for absent settings and invalid saved settings proving fail-closed behavior.
- `V30-R1-002`: GitHub remote slug parser now accepts dotted repo names consistently with the settings validator. Added dotted repo regression test.
- `V30-R1-003`: Admin UI assets moved from one-line embedded strings into readable static asset routes; route plumbing now uses a `RouteContext` object instead of widened `registerRoutes`/`launchHandler` signatures.

## Changed files
- `pipeline-diagram/global-nav.js`
- `term-control-center/server/index.ts`
- `term-control-center/server/adminAssets.ts`
- `term-control-center/server/adminAuth.ts`
- `term-control-center/server/adminConfig.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/nginxProxy.test.ts`
- `term-control-center/tests/server.test.ts`
- `docs/admin-configuration.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-30-simple-admin-login-config-panel/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-30-simple-admin-login-config-panel/review-request-r1.json`

## Acceptance/checkpoint mapping
1. Auth/session: implemented bootstrap, login, logout, cookie sessions, CSRF enforcement, no plaintext password storage tests.
2. Settings persistence: implemented atomic local config save/reload with last updated time and audit events.
3. Validation: implemented path, repo, branch/ref, git root, repository match, current branch validation, absent-settings fail-closed, and dotted repo regression coverage.
4. Admin UI: implemented `/admin/` page with login/bootstrap, save, reset, logout, effective settings, and recent audit display.
5. PRD #40 alignment: hosted mode disables local login, requires trusted proxy address plus `agentops-admin`, route-policy tests assert `/admin/` and `/api/admin/` map to `agentops-admin`, direct `X-Authentik-*` spoofing fails closed.
6. Guardrails: no GitHub mutation, PR, merge, deploy, trading, backtest, or live infrastructure mutation added.

## Validation results
- `cd term-control-center && npm run typecheck`: passed.
- `cd term-control-center && npm test`: passed, 141 tests.
- `cd term-control-center && HOME=$(mktemp -d) node --import tsx --test --test-concurrency=1 tests/admin.test.ts`: passed, 9 tests.
- `cd pipeline-diagram && AGENTOPS_ADMIN_SETTINGS_FILE=/home/hyperbots/.local/state/agentops/term-control-center/admin-settings.json python3 generate.py`: passed, wrote 8 open PRDs / 0 in-progress; Project fields skipped during current GitHub API rate limit.
- `cd /mnt/hyperliquid-data/projects/repos/agentops-harness/pipeline-diagram && AGENTOPS_ADMIN_SETTINGS_FILE=/home/hyperbots/.local/state/agentops/term-control-center/admin-settings.json python3 generate.py`: passed, wrote 8 open PRDs / 0 in-progress; Project fields skipped during current GitHub API rate limit.
- `python3 config/templates/secure-access/validate-secure-access-templates.py`: passed.
- `git diff --check`: passed.

## Verifier checkpoints
1. Auth/session checkpoint: local bootstrap/login/logout/session enforcement, no plaintext password storage, session cookie defaults, CSRF/origin checks.
2. Settings persistence checkpoint: local work path, GitHub repo, worktree root, naming convention, default PRD authoring workspace, atomic save/reload, audit events.
3. Validation checkpoint: invalid paths/repos/branch-refs/authoring workspaces fail clearly and do not persist.
4. Admin UI checkpoint: usable login/admin panel with save/cancel/logout and current-setting display.
5. PRD #40 alignment checkpoint: `/admin/` and `/api/admin/` align with `agentops-admin`; local login is not hosted perimeter; proxy identity headers are fail-closed unless trusted boundary is configured.
6. Guardrail checkpoint: no GitHub mutation/PR/merge/deploy/trading/backtest authority; no secret leakage; no live infrastructure mutation.
7. Final bug-check: verifier regression review after implementation approval.

## Steward hygiene review
- Steward review completed after revision 2 verifier implementation approval.
- Decision: `clean`.
- Scope checked: server implementation files, UI/navigation files, tests, docs, and issue-specific run artifacts.
- Cleanup needed: none.

## Follow-up: first-class GitHub Project config
- Operator identified GitHub Project URL/number as fundamental project configuration for the PRDs shown on board/pipeline.
- Added `githubProjectUrl` and `githubProjectNumber` as first-class admin settings with URL/number matching validation.
- Admin UI now renders dedicated GitHub Project URL and number fields instead of relying on `extra` JSON.
- PRD authoring `/launch-context` and launched authoring task now carry configured `projectUrl`.
- Board Create PRD flow now preserves `context.projectUrl` from admin launch context.
- Existing saved settings without the new fields migrate to default Project 3 values or an existing `extra.githubProjectUrl` value, then persist first-class fields on next save.
- Tests now cover project field validation, persistence, launch task propagation, and board Create PRD project URL propagation.

## Revision 5 fix for verifier finding
- `V30-R4-001`: removed Basic Auth `/admin/` and `/api/admin/` proxy locations from `pipeline-diagram/deploy/ops.evono.me.nginx` so the installable hosted nginx template does not expose admin routes outside PRD #40 `agentops-admin` policy.
- Added regression test proving the Basic Auth nginx template does not contain admin proxy locations and kept route-policy assertions proving `/admin/` and `/api/admin/` belong to `agentops-admin`.

## Follow-up: path browse buttons
- Operator requested Browse buttons for every admin path field.
- Added authenticated directory browser endpoint `GET /api/admin/browse?path=...`.
- Directory browser returns directory names/paths only, not file contents, and requires an authenticated admin session.
- Added Browse buttons for `localWorkPath`, `worktreesRoot`, PRD authoring `repoPath`, and optional `worktreePath`.
- Added modal folder picker UI with Up, Select current, and Cancel controls.
- Added tests for authenticated browsing, directory-only listing, and Browse button rendering.

## Follow-up: board/pipeline project wiring and GitHub Project dropdown
- Researcher refreshed GitHub Projects guidance: Projects v2 are owner-scoped, not strictly repo-scoped; use read-only `gh api graphql` / `gh project list` style access, `read:project` for read-only project queries, and validate URL/number without mutations.
- Added authenticated `GET /api/admin/github-projects?repository=owner/repo` endpoint using read-only GraphQL through `gh api graphql`.
- GitHub Project dropdown now loads owner Projects for the selected repository, sorting Projects linked to the repo first; manual URL/number entry remains available for projects outside the dropdown.
- `pipeline-diagram/generate.py` now reads admin settings from `AGENTOPS_ADMIN_SETTINGS_FILE` or the default Term Control state path, then uses configured `githubRepository`, `githubProjectUrl`, and `githubProjectNumber` for PRD issue fetches, Project item fields, and generated board/pipeline data.
- Admin settings save includes an optional local pipeline refresh hook (`TERM_CONTROL_PIPELINE_REFRESH=1`) so served board/pipeline data can be regenerated from the saved config without GitHub mutation.
- Tests cover the GitHub Project dropdown endpoint with a fake `gh`, linked-project sorting, generator default/configured settings loading, and existing project launch propagation.
- Addressed verifier finding `V30-R8-001` by removing the hardcoded legacy product repository fallback from `pipeline-diagram/generate.py`; generator defaults now use AgentOps config with environment override support.
- Addressed verifier finding `V30-R9-001` by removing the forbidden product-name regression-test literal while keeping generator default/configured settings coverage.

## Current implementation status
- Revision 2 approved by verifier with `bug_check_status: passed`.
- Steward hygiene review clean.
- Revision 3 final verifier confirmation approved with `bug_check_status: passed_confirmed`.
- Follow-up GitHub Project config revision 5 approved by verifier with `bug_check_status: passed`.
- Path browse button follow-up revision 6 approved by verifier with `bug_check_status: passed`.
- Steward recheck after browse follow-up: `clean`.
- Revision 7 final verifier confirmation approved with `bug_check_status: passed_confirmed`.
- Board/pipeline project wiring and GitHub Project dropdown follow-up approved by verifier at revision 10.
- Final verifier bug-check confirmed at revision 11 with `bug_check_status: passed_confirmed`.
- Post-approval hosted-generation bug fixed: `generate.py` no longer tries hardcoded tracker issue bodies before checking lane membership, supports dynamic `agent:*` lanes such as `agent:agentops`, and treats missing legacy tracker bodies as non-blocking.
- Addressed verifier finding `V30-R12-001`: `classify(prds, {})` now uses the explicitly supplied empty field map instead of calling live `gh project item-list`; clean-`HOME` admin test passes.
- Dynamic generator crash fix approved by verifier at revision 13.
- Final verifier bug-check confirmed at revision 14 with `bug_check_status: passed_confirmed`.
- Live deploy attempt hit GitHub Project GraphQL rate limit for `gh project item-list`; bounded fix applied so project fields are best-effort and generator still emits board/pipeline data from configured repo issues.
- Confirmed the user's hosted-generation command now succeeds with saved admin settings: `Wrote pipeline.mmd, pipeline-data.js, board-data.js, wip-data.js (8 open PRDs, 0 in progress)` even while Project fields are skipped due rate limit.
- Copied updated pipeline generator/static outputs to live nginx root `/mnt/hyperliquid-data/projects/repos/agentops-harness/pipeline-diagram` and regenerated there successfully.
- Rebuilt and restarted Term Control Center on `127.0.0.1:3032`; admin HTML shows GitHub Project dropdown/load controls.
- Open findings: none.
- Finding IDs addressed: `V30-R1-001`, `V30-R1-002`, `V30-R1-003`, `V30-R4-001`.
