# Coder Handoff — Issue #160 Memory Admin UX

## Source of truth
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/160
- Branch: `prd/memory-admin-ux-project-memory-160`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-160`

## Preflight
- PRD read first from GitHub issue #160.
- Pre-edit status: `## prd/memory-admin-ux-project-memory-160...origin/main`; no dirty files.
- Dependencies rechecked: #104 closed with `status:approved`; #48 closed with `status:approved`.
- Issue #160 state rechecked: open; labels `type:prd`, `agent:agentops`, `status:approved`; Project item `agentops-dev` status `In progress`.
- Research-first surfaces: none in PRD; no researcher consult needed for checkpoint 1.

## Scope controls
- Allowed paths: Admin Memory UI/client code, narrow server memory endpoint behavior, focused tests, run artifacts.
- Forbidden paths/actions: no live memory enablement, deployment, PR creation, merge, issue/Project/tracker mutation, raw transcript/secret display, provider upgrade, cross-project/global recall, per-turn injection, product routes/navigation redesign.
- Validation commands: `npm --prefix term-control-center run typecheck`; targeted Node tests for changed memory/admin behavior.
- Stop condition: verifier approves checkpoint 1, then proceed to checkpoint 2.

## Verifier checkpoints
1. Remember control checkpoint: UI + endpoint behavior, redaction, disabled-project no-write.
2. Recall preview checkpoint.
3. Readiness panel checkpoint.
4. Security/privacy checkpoint.
5. Regression/safety + steward + final bug-check.

## Checkpoint 1 — Remember control
### Changed files
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/server/adminCss.ts`
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminProjects.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/projectMemoryAdminUx.test.ts`

### Implementation notes
- Added compact Admin Memory `Remember this` textarea with `maxlength="4000"`, operator warning text, and `Remember` action.
- Wired client-side remember action to existing project-scoped `/memory/remember` endpoint.
- Manual remember now trims text, rejects empty input, rejects content over 4000 chars, and rejects raw transcript/terminal-log markers before any write.
- Successful manual remember returns source/provenance, redacted text, redaction flag, and stored length.
- Existing capture path still reuses project validation, duplicate-root guard, enabled-state guard, and `redactMemoryText` before persistence.

### Validation
- `npm --prefix term-control-center ci` — passed (installed missing local deps; `node_modules/` untracked ignored).
- `npm --prefix term-control-center run typecheck` — passed (r1 and r2).
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='admin static assets|admin memory API|project memory|operator remember|capture writes' tests/admin.test.ts tests/projectMemory.test.ts` — passed, 7/7 (r1).
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='admin static assets|admin memory API|operator remember|capture writes' tests/admin.test.ts tests/projectMemory.test.ts` — passed, 4/4 (r2).
- Initial untargeted `npm --prefix term-control-center test -- --runInBand` failed before dependency install because `tsx` was missing.
- A broader `npm --prefix term-control-center test -- tests/projectMemory.test.ts tests/admin.test.ts` was mis-invoked; package script ignored file args, ran broad suite, timed out with unrelated pre-existing environment-sensitive failures in browser/PRD-review tests. Relevant memory tests in that run passed.

## Revision 2 — F160-C1-001
- Manual remember now requires selected project memory to be enabled and `health.status === "ok"` before writing.
- Warning, error, disabled, missing, or otherwise unverified health states fail before persistence with actionable doctor/provider guidance.
- Existing non-manual capture helpers are unchanged for completion workflows; the readiness gate is applied only by manual remember.
- Tests now prove no-doctor/provider-warning remember attempts create zero entries, and verified/ok enabled memory still writes redacted provenance-tagged entries.

## Revision 3 — F160-C1-002
- Admin memory create/update paths now strip client-supplied `health`, so API callers cannot mark memory provider-ready by posting `health.status: "ok"`.
- Memory reset now leaves health at `warning` with a doctor-before-remembering note instead of setting provider-ready `ok`.
- Manual remember still permits trusted persisted `ok` health; tests set trusted fixture state directly outside the admin settings API to prove the positive path.
- r3 validation repeated: typecheck passed; targeted admin/project memory tests passed 4/4.

## Checkpoint 2 — Recall preview
### Changed files added for checkpoint 2
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/projectMemoryAdminUx.test.ts`

### Implementation notes
- Added authenticated project-scoped `GET /api/admin/projects/:id/memory/preview` endpoint.
- Preview validates project memory path/isolation and duplicate roots before reading.
- Disabled projects fail closed with `memory is disabled for this project` and do not write.
- Preview returns `{ projectId, advisory, precedence, recall }` with explicit advisory precedence text.
- UI adds `Preview launch recall` action and visible advisory copy; client renders bounded JSON preview in the existing memory output panel.
- Tests cover project-scoped preview, advisory metadata, disabled preview rejection, and no cross-project recall leakage.

### Validation
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='admin static assets|admin memory API|operator remember|capture writes' tests/admin.test.ts tests/projectMemory.test.ts` — passed, 4/4.

## Revision 5 — F160-C2-001
- Recall preview now uses `launchMemoryConfig` launch eligibility before returning recall.
- Enabled memory with `health.status === "error"` or launch-disabled health returns an explicit unavailable preview with `recall: []` and warnings instead of stale launch-ineligible recall.
- Enabled warning/ok states still preview bounded project-scoped recall, matching current launch behavior.
- Tests now cover warning-state preview availability and error-health preview no-recall behavior.
- r5 validation repeated: typecheck passed; targeted admin/project memory tests passed 4/4.

## Checkpoint 3 — Readiness panel
### Changed files added for checkpoint 3
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/server/adminCss.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/projectMemoryAdminUx.test.ts`

### Implementation notes
- Added authenticated `GET /api/admin/projects/:id/memory/readiness` endpoint.
- Readiness validates memory path/isolation and duplicate roots, then returns a compact checklist for enabled state, learned provider, codebase layer, doctor, isolation, recall preview, and live human gate.
- Doctor status is not ready when unknown/stale/non-ok; isolation is unavailable unless a fresh ok doctor/isolation timestamp exists.
- Recall preview readiness uses launch eligibility and shows unavailable with warnings when not launch-eligible.
- UI adds `Refresh readiness`, renders the checklist, links `docs/agentops-project-memory-live-enablement.md`, and labels live enablement as requiring separate human confirmation.
- Non-ready/unavailable/human-required rows render with non-green status styling.

### Validation
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='admin static assets|admin memory API|operator remember|capture writes' tests/admin.test.ts tests/projectMemory.test.ts` — passed, 4/4.

## Revision 7 — F160-C3-001
- Isolation readiness now validates `isolationTestAt` freshness before marking the row ready.
- Missing, invalid, or stale isolation evidence renders `unavailable` with rerun doctor/isolation guidance.
- Tests now prove stale isolation evidence is not ready and fresh ok isolation evidence is ready.
- r7 validation repeated: typecheck passed; targeted admin/project memory tests passed 4/4.

## Revision 8 — F160-C3-002
- Moved expanded operator remember / recall preview / readiness coverage into focused `term-control-center/tests/projectMemoryAdminUx.test.ts`.
- Reduced `term-control-center/tests/projectMemory.test.ts` to 229 lines; new focused test file is 154 lines.
- Split the new Admin UX test into smaller callbacks for remember, preview, readiness, and disabled/invalid states.
- r8/r9 validation repeated: typecheck passed; targeted admin/project memory tests passed 7/7 with the new test file included.

## Checkpoint 4 — Security/privacy
### Changed files added for checkpoint 4
- `term-control-center/server/projectMemory.ts`
- `term-control-center/tests/projectMemoryAdminUx.test.ts`

### Implementation notes
- Extended memory redaction to cover bearer/basic auth strings, modern GitHub PATs, AWS access keys, AWS env names, and quoted key/value secrets in addition to existing GitHub/OpenAI-style tokens, key/value secrets, and private keys.
- Existing manual remember validation rejects raw transcript and terminal-log markers before persistence.
- Preview/readiness endpoints return bounded summaries and do not expose raw provider cache contents or memory-store file browsing.
- Tests now verify bearer/basic credential redaction, modern GitHub PAT redaction, AWS env/key redaction, quoted password redaction, existing token redaction, oversized rejection, raw transcript rejection, disabled no-write, preview scoping, and launch-ineligible no-recall behavior.

### Validation
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='remember requires|remember redacts|admin static assets|admin memory API|recall preview|readiness|disabled and invalid|capture writes' tests/admin.test.ts tests/projectMemory.test.ts tests/projectMemoryAdminUx.test.ts` — passed, 8/8.
- `wc -l term-control-center/tests/projectMemory.test.ts term-control-center/tests/projectMemoryAdminUx.test.ts` — 229 and 168 lines.

## Revision 11 — F160-C4-001
- Expanded redaction for the exact credential forms identified by verifier: standalone bearer/basic credentials, `Authorization: Basic`, `github_pat_...`, `AWS_ACCESS_KEY_ID=AKIA...`, and quoted password values with spaces.
- Added focused remember/export/preview test coverage proving those raw forms are not returned.
- r11 validation repeated: typecheck passed; targeted admin/project memory tests passed 8/8.

## Checkpoint 5 — Regression/safety implementation review
### Changed files in full implementation
- `term-control-center/server/adminCss.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminProjects.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/projectMemory.ts`
- `term-control-center/tests/admin.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/projectMemoryAdminUx.test.ts`
- Run artifacts under `dev-plans/agentops/coder-verifier-workflow/runs/issue-160-memory-admin-ux/`

### Regression/safety notes
- Existing Save, Doctor, Isolation, Export, and Reset memory controls remain present and bound.
- Manual remember, preview, and readiness remain project-scoped via `/api/admin/projects/:id/memory/...` routes.
- No PRD labels, Project fields, tracker state, issue closeout, live enablement config, deployment, PR creation, merge, provider package versions, cross-project recall, cloud sync, or per-turn injection were mutated.
- Reset now clears memory but leaves readiness non-ready until doctor verification, preserving rollback safety.

### Final validation so far
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; Vite emitted pre-existing bundle-size/style warnings only.
- `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='remember requires|remember redacts|admin static assets|admin memory API|recall preview|readiness|disabled and invalid|capture writes' tests/admin.test.ts tests/projectMemory.test.ts tests/projectMemoryAdminUx.test.ts` — passed, 8/8.
- `wc -l term-control-center/tests/projectMemory.test.ts term-control-center/tests/projectMemoryAdminUx.test.ts` — 229 and 168 lines.

## Steward / checkpoint 5 status
- Steward pre-final hygiene: clean (`dev-plans/agentops/coder-verifier-workflow/runs/issue-160-memory-admin-ux/steward-response-r1-prefinal-hygiene.md`).
- Verifier checkpoint 5 implementation review: approved at revision 12.

## Final bug-check revision — F160-FBC-001
- Manual remember readiness now rejects stale, missing, or invalid doctor `checkedAt` via the same freshness helper used by readiness display.
- Added focused regression coverage proving stale persisted `ok` health rejects manual remember before any write.
- Final validation repeated after the fix:
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed; Vite emitted existing non-blocking warnings only.
  - `cd term-control-center && env -u TERM_CONTROL_ADMIN_AUTH_MODE -u TERM_CONTROL_ADMIN_TRUSTED_PROXY_ADDRESSES node --import tsx --test --test-concurrency=1 --test-name-pattern='remember requires|remember redacts|admin static assets|admin memory API|recall preview|readiness|disabled and invalid|capture writes' tests/admin.test.ts tests/projectMemory.test.ts tests/projectMemoryAdminUx.test.ts` — passed, 8/8.
  - `wc -l term-control-center/tests/projectMemory.test.ts term-control-center/tests/projectMemoryAdminUx.test.ts` — 229 and 170 lines.

## Final verifier status
- Final bug-check fix review approved at revision 14.
- Final `bug_check_status`: `passed`.
- No open verifier findings.

## Known risks / next work
- Human-managed PR/merge/closeout remains pending; no PR was created.
- Admin test suite is sensitive to hosted-auth environment variables; targeted validation explicitly unsets them.
