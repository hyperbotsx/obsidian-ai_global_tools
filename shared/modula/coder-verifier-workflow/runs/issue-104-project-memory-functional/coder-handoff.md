# Coder Handoff — Issue #104 Project Memory Functional Layer

## Source of truth
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/104
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-104`
- Branch: `prd/a2-prd-make-the-project-memory-104`

## Scope controls
- Allowed: existing project memory substrate/admin/launch/completion surfaces, tests, docs/runbook, coder-verifier run artifacts.
- Forbidden: live `ops.evono.me` config mutation, deployment, PR creation, merge, raw transcripts/secrets/provider caches/memory store contents, project-local skills, cross-project memory sharing, cloud sync, per-turn injection, trading/backtests.
- Validation: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; targeted Node tests for memory/launch; `PYTHONPATH=src python3 -m pytest tests/unit` where environment allows.
- Stop condition: verifier implementation approval, steward hygiene approval because docs/run artifacts changed, then final verifier bug-check approval; otherwise human escalation.

## Verifier checkpoints
1. Provider/doctor: package presence gate plus write/read/isolation round-trip and missing-provider remedy.
2. Capture: explicit remember + workflow verifier/closeout capture, redaction, provenance, disabled-project no-write.
3. Recall: bounded project-scoped advisory recall in launch context/env/prompt.
4. Provider reconciliation: codebase-memory-mcp as always-on codebase layer; one learned provider only; default pi-persistent-intelligence; legacy codebase provider migrated.
5. Isolation/safety: #48 path/flag guards preserved; no cross-project recall, cloud sync, or per-turn injection.
6. Live readiness: runbook and validation evidence; no live enablement.
7. Regression/security: admin/launch behavior remains intact; final bug-check pending.

## Pre-existing worktree state
- `git status --short --branch` before edits: clean (`## prd/a2-prd-make-the-project-memory-104...origin/main`).
- Memory warning from launch context: memory disabled for `@samfp/pi-memory` at `/home/hyperbots/.config/agentops-harness/projects/agentops-harness/memory`.

## Research consult
- Mandatory freshness consult completed with researcher on 2026-06-29.
- Recommendation: default learned provider `pi-persistent-intelligence@0.11.2`; codebase layer `codebase-memory-mcp@0.8.1`; mark providers unavailable/warning until doctor verifies pinned package presence; never run both learned-memory providers.
- Key source refs returned: unpkg package metadata for `@samfp/pi-memory@1.5.0`, `pi-persistent-intelligence@0.11.2`, `codebase-memory-mcp@0.8.1`; provider docs/GitHub; pi-total-recall Node 24 warning.

## Implementation summary
- Reconciled provider model: `MemoryProvider` now represents exactly one learned provider, defaulting to `pi-persistent-intelligence`; `codebase-memory-mcp` is an always-on codebase layer rather than a competing provider option.
- `runMemoryDoctor` validates roots/flags, writes and reads a redacted project checkpoint at the configured root, checks an isolated second root, probes pinned learned + codebase package presence, returns `ok` only when all pass, and returns a clear install warning otherwise.
- Added explicit memory capture helpers and Admin `POST /api/admin/projects/:id/memory/remember` for operator “remember this”.
- Added workflow capture at completion verifier-decision events and successful PRD closeout, using provenance-tagged redacted entries and silently skipping disabled memory.
- Added bounded launch recall (`launchMemoryRecall`) into resolved launch task memory; launch prompts now include advisory recalled snippets and codebase MCP wiring is driven by the codebase layer.
- Admin UI no longer offers `codebase-memory-mcp` as a learned provider option and labels the codebase layer as paired behavior.
- Updated docs plus added live-enablement/rollback runbook; no live config was changed.

## Changed files
- `docs/agentops-project-memory.md`
- `docs/agentops-project-memory-live-enablement.md`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/adminMemoryClient.ts`
- `term-control-center/server/adminProjectMemory.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/completionCloseoutRoutes.ts`
- `term-control-center/server/completionRoutes.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/projectMemory.ts`
- `term-control-center/server/projectMemoryProvider.ts`
- `term-control-center/server/projectMemoryProviderSmoke.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/projectMemoryProvider.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-104-project-memory-functional/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-104-project-memory-functional/validation-ledger-log.md`

## Validation log
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts`
- PARTIAL/known environment failures: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts tests/launchPlan.test.ts` passed all project memory tests and memory-related launch tests, but failed existing environment-sensitive launch assertions for PRD review auth and browser profile path.
- PARTIAL/known environment failures: `PYTHONPATH=src python3 -m pytest tests/unit` passed 952/956, with failures in agent GitHub config env expectations and AF_UNIX socket path length due this runtime path; unrelated to changed memory files.
- FAIL/setup: `python -m pytest tests/unit` because `python` command is unavailable; reran with `python3` and `PYTHONPATH=src` above.

## Revision 2 fixes for verifier findings
- F104-R1-001: Launch config now carries provider-specific env (`PI_MEMORY_ROOT` for pi-persistent-intelligence), and package probing now requires an exact pinned package version through Node package metadata or exact `pi list` source instead of name-only matching.
- F104-R1-002: Shared capture/remember/workflow write path now validates the persisted project memory config and duplicate roots before writing; added regression coverage for corrupted persisted roots.
- F104-R1-003: Split provider/package logic into `term-control-center/server/projectMemoryProvider.ts`, removed the unused codebase settings export, and replaced widened closeout positional args with a context object.

## Revision 2 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts`

## Revision 3 fixes after human selected strict provider wiring
- Human selected verifier option 1: require stricter provider runtime wiring before approval.
- F104-R1-001 follow-up: launch args now explicitly add `-e npm:<selected-learned-provider>@<pinned-version>` only when memory health is `ok`, so panes using `pi --no-extensions` still load the selected learned provider.
- F104-R1-001 follow-up: doctor now gates `ok` on exact package presence plus a selected-provider runtime probe through explicit Pi extension loading; if the selected learned provider does not load, doctor remains `warning`.
- Added launch test coverage for explicit learned-provider extension args and provider env.

## Revision 3 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts`
- PARTIAL/known environment failures: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts tests/launchPlan.test.ts` passed memory-related launch tests including explicit provider extension loading, but still failed the same unrelated PRD review auth and browser profile path assertions.

## Revision 4 fixes for verifier findings
- F104-R1-001 follow-up: replaced the ineffective `--version` runtime probe with `pi --no-extensions -e <spec> --list-models __agentops_memory_probe_no_match__`, which fails for bogus extension specs and loads explicit extensions without invoking a model prompt.
- F104-R1-001 follow-up: added regression coverage proving a bogus extension spec fails the default runtime probe.
- F104-R3-002: replaced the five-parameter `runMemoryDoctor` signature with a `MemoryDoctorOptions` object for probe injection.

## Revision 4 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts`

## Revision 5 fixes for verifier finding F104-R1-001
- Added provider-native smoke for `pi-persistent-intelligence`: writes and reads a project-scoped provider-format record under `memory/projects/<project>.jsonl`, and checks an isolated second provider root for no leakage.
- Doctor `ok` now requires exact package presence, explicit Pi extension load, provider-native write/read/isolation smoke, and the existing harness round-trip.
- If the selected provider lacks a verifiable provider-native smoke path, doctor stays `warning` instead of claiming `ok`.

## Revision 5 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts`

## Revision 6 fixes for verifier finding F104-R5-004
- Split provider-focused tests into `term-control-center/tests/projectMemoryProvider.test.ts`; `projectMemory.test.ts` is now 253 lines.
- Split the provider smoke record builder helpers so the new provider smoke functions stay under the function-size limit.

## Revision 6 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/projectMemory.test.ts tests/projectMemoryProvider.test.ts`

## Revision 7 final bug-check fix
- F104-FBC-001: enabled-memory workflow capture failures are now surfaced as non-blocking `validationErrors` on completion-event and closeout response state instead of being silently swallowed.
- Disabled/no project memory remains a no-op.
- Added completion route coverage for verifier-decision and closeout capture failure observability with invalid persisted memory roots.

## Revision 7 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion-routes.test.ts tests/projectMemory.test.ts tests/projectMemoryProvider.test.ts`

## Revision 8 final bug-check fix
- F104-FBC-002: rejected completion events now skip automatic memory capture when reconciliation fails, preventing rejected/mismatched payloads from writing advisory memory.
- Added completion route coverage proving a rejected mismatched project event returns 400 and writes no memory for the payload project.

## Revision 8 validation
- PASS: `npm --prefix term-control-center run typecheck`
- PASS: `npm --prefix term-control-center run build`
- PASS: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completion-routes.test.ts tests/projectMemory.test.ts tests/projectMemoryProvider.test.ts`

## Steward hygiene review
- Steward decision: clean.
- Changed implementation/tests/docs are in appropriate locations.
- Run artifacts are scoped under the issue run folder.
- No raw transcripts, provider caches, memory store contents, generated DB/jsonl outputs, or secret-like changed paths found.
- Ignored build/cache artifacts are not part of the diff and need no cleanup.
- Revision 7 steward recheck after final bug-check fix: clean; no cleanup required.
- Revision 8 final steward recheck after F104-FBC-002 fix: clean; no cleanup required.

## Final verifier status
- Revision 9 verdict: approved.
- Final bug-check status: passed.
- Open findings: 0.
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-104-project-memory-functional/verifier-report.md`.

## Risks / manual QA
- Doctor package probing checks exact Node package metadata or exact `pi list` source; live/staging provider installation should still be verified during manual enablement.
- The doctor writes a provenance `doctor` checkpoint into the selected memory root as evidence of the configured-root round-trip.
- Manual local/staging verification still needed for real installed Pi provider runtime, launch recall display, Admin remember endpoint, and A/B project isolation before any live enablement.
