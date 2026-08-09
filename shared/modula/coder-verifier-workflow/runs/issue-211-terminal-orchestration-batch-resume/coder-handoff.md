# Coder handoff — Issue #211 terminal orchestration and batch resume

## Source of truth
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/211
- PRD status: approved.
- Context brief: `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-211-70c311424020/artifacts/project-context-brief.md`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-211`
- Branch: `prd/terminal-orchestration-batch-resume-211`
- Operator continuation authorization: implement approved #211 scope and continue through bounded checkpoints, routine revisions, validation, Steward hygiene, and verifier bug-check. Human approval boundaries remain mandatory; no PR, merge, deploy, approval, trading, or backtest authority is granted.
- Exceptional authorization (2026-07-19): implement the bounded authoritative active-project controller correction for escalated `F211-C3-005`: distinct initialization/refresh/stable/selection/failure states, refresh invalidation at every selection start, archived-project rejection, structured refresh failure, exact stale-read tests, and verifier re-review only. No other scope or authority expands.

## Pre-edit status and boundaries
- `git status --short --branch`: clean (`## prd/terminal-orchestration-batch-resume-211...origin/main`).
- Pre-existing dirty files: none.
- Allowed paths: PRD-approved orchestrator modules/routes, narrow `server/index.ts` composition and planner-injection refactor, existing assistant adapters/UI, focused tests, docs, and this run folder.
- Forbidden: product-unrelated surfaces; deployment/identity config; raw transcripts/runtime state/generated output; repo-local skills/standards; any path where model output can mutate terminal/action state without a human-minted approval token.
- Required validation: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run test`; `npm --prefix term-control-center run build`; `PYTHONPATH=src python3 -m pytest tests/unit -q`; `git diff --check`.
- Stop condition: final verifier bug-check approval or a true human escalation.

## Checkpoints
1. Read layer: project-scoped envelope, structured evidence, bounded redacted fenced tails, fingerprints, read-only route/tool.
2. Proposal/approval: durable fail-closed store, transitions/TTL/supersession, human-only token minting, item-set binding, ledger/recovery.
3. Injection: shared adapter, exact live identity/routing/preflights, lock/idempotency/rate limit, echo-before-Enter, planner regression.
4. Delegation: existing completion/Kody/lane entry points and reserved-kind rejection.
5. Assistant/UI: exactly three adapters, hostile-tail policy, proposal card/veto/supersede/outcomes and Active Jobs link.
6. Steward hygiene, verifier recheck, final verifier bug-check, docs/validation.

## Research
- Mandatory pre-implementation researcher consults are complete; their bounded findings are recorded below.
- Consult 1 (2026-07-19): tmux 3.4 supports `set-buffer` then `paste-buffer -p` for bracketed-paste-aware apps; prompt text must not use `send-keys`; the universal Pi/Claude/Codex echo/Enter timing contract is undocumented. Require per-role scratch smoke, bounded capture polling, complete echoed draft confirmed in two samples, then one literal Enter; no Enter on failure. Codex has a current paste-burst timing risk.
- Consult 2 (2026-07-19): Co-Worker is Python deterministic intents plus one-shot Claude/Codex CLI text, not provider tool calling. Use explicit narrow Python-to-Term adapters for exactly three Node-owned tools; do not expose a generic proxy or token minting to Python/model/browser state. Existing coworker surface markers are defense-in-depth, not authority.
- Consult 3 (2026-07-19): `prepare_pr` currently auto-triggers Kody/Kodus by default. The future orchestrator must extract/reuse the completion application service, persist that recorded outcome, and make a following `kody_review` item reuse it to avoid a double trigger. Lane delegation must call `executeLanePlan()` with its bounded existing confirmation/caps.
- Consult 4 (2026-07-19): persisted `groups.json` is recovery seed data, not liveness proof. Post-restart injection must require exact live group/pane/session/supervisor identity, `recoverability === recovered`, fresh exact tmux liveness, current fingerprint, and a new structured awaiting-input signal. Proposal execution recovery must use pre-side-effect ledger attempt records then fail interrupted batches closed.
- Dead-end consult (2026-07-19): after two bounded KISS revisions, researcher directed reuse of the canonical registry/settings parser through a non-mutating snapshot mode, not an orchestrator-local parser. The implementation now makes `readProjectRegistry(store, false)` preserve canonical validation while skipping only legacy migration writes.
- Consult 5 (2026-07-19): for proposal/ledger crash recovery, use a durable same-directory pending transition/WAL before the ledger append and state checkpoint; retain an idempotent event ID, replay pending transitions at startup before ordinary recovery, and never retry an attempt-side effect. Sources: Node v22 `fsyncSync`, Linux `fsync(2)`, and `rename(2)` (all accessed 2026-07-19).
- Checkpoint 3 final-fix consult (2026-07-19): retain a same-action result from immediately before the first possible pane input (`paste-buffer`/PTY write), leave conclusively pre-paste failures retryable, treat every `await` as invalidating state before Enter, and clear only on session lifecycle end. Sources: MDN `await`, tmux(1), Node v22 `crypto.randomUUID` (all accessed 2026-07-19).

## Touched files
- `term-control-center/server/adminProjectSelection.ts`
- `term-control-center/server/adminRoutes.ts`
- `term-control-center/server/adminProjects.ts`
- `term-control-center/server/contextBriefTransition.ts`
- `term-control-center/server/completionRoutes.ts` (checkpoint 4 transport adapter)
- `term-control-center/server/completionPrepareAction.ts` (new; checkpoint 4 application service)
- `term-control-center/server/kodyReview.ts` (checkpoint 4 project-scoped review IDs)
- `term-control-center/server/kodyReviewStore.ts` (checkpoint 4 cross-writer canonical ID migration)
- `term-control-center/server/kodyReviewTrigger.ts` (new; checkpoint 4 shared deduplicated trigger)
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/laneOrchestrator.ts` (checkpoint 4 lane/ad-hoc freshness service)
- `term-control-center/server/laneRequestResolution.ts` (new; checkpoint 4 lane request/fingerprint semantic boundary)
- `term-control-center/server/canonicalPrdApproval.ts` (new; checkpoint 4 read-only canonical ad-hoc approval evidence)
- `term-control-center/server/tmuxSupervisor.ts`
- `term-control-center/server/validationReceipt.ts`
- `term-control-center/shared/blockedPaths.ts`
- `term-control-center/server/projectScope.ts` (new; exceptional checkpoint 3 scope)
- `term-control-center/server/planningBrief.ts`
- `term-control-center/server/orchestrator/machineEvidence.ts` (new)
- `term-control-center/server/orchestrator/orchestratorRoutes.ts` (new)
- `term-control-center/server/orchestrator/proposalStore.ts` (new; checkpoint 2/4 review candidate)
- `term-control-center/server/orchestrator/proposalValidation.ts` (new; checkpoint 4 validation boundary)
- `term-control-center/server/orchestrator/proposalLedger.ts` (new; checkpoint 2 review candidate)
- `term-control-center/server/orchestrator/proposalLock.ts` (new; checkpoint 2 review candidate)
- `term-control-center/server/orchestrator/proposalPersistence.ts` (new; checkpoint 2 review candidate)
- `term-control-center/server/orchestrator/proposalTransitionReducer.ts` (new; checkpoint 2 review candidate)
- `term-control-center/server/orchestrator/paneInjection.ts` (new; checkpoint 3 in progress)
- `term-control-center/server/orchestrator/paneInjectionGuard.ts` (new; checkpoint 3 in progress)
- `term-control-center/server/orchestrator/paneInjectionRunner.ts` (new; checkpoint 3 in progress)
- `term-control-center/server/orchestrator/delegatedActions.ts` (new; checkpoint 4 review candidate)
- `term-control-center/tests/paneInjection.test.ts` (new; checkpoint 3 in progress)
- `term-control-center/tests/delegatedActions.test.ts` (new; checkpoint 4 review candidate)
- `term-control-center/tests/kodyReviewTrigger.test.ts` (new; checkpoint 4 review candidate)
- `term-control-center/tests/laneOrchestrator.test.ts` (new; checkpoint 4 review candidate)
- `src/agentops_harness/kodus_state.py` and `src/agentops_harness/kodus_agent.py` (checkpoint 4 shared Kody state writer)
- `tests/unit/test_kodus_agent.py` (checkpoint 4 Python writer/dedupe coverage)
- `term-control-center/tests/projectScope.test.ts` (new; exceptional checkpoint 3 scope)
- `term-control-center/server/orchestrator/paneInventory.ts` (new)
- `term-control-center/server/orchestrator/paneTail.ts` (new)
- `term-control-center/tests/orchestratorPanes.test.ts` (new)
- `term-control-center/tests/proposalStore.test.ts` (new; checkpoint 2 in progress)
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/coder-handoff.md` (run artifact)

## Current checkpoint
- Checkpoint 2 is verifier-approved at revision 7 with zero findings. Checkpoint 3 is verifier-approved at exceptional revision 7 with zero findings. Checkpoint 4 is verifier-approved at revision 4 with zero open findings; its compact verdict was accepted without reading the approved full report. Required Steward hygiene review is next, then verifier recheck and final bug-check.

## Implementation summary and acceptance coverage
- Checkpoint 1 implementation: registered authenticated read-only `GET /api/orchestrator/panes` through narrow server composition.
- The active-project envelope inventories live group panes, reports cap/omitted count, combines completion/heartbeat/session state structured-first, exposes available completion actions and strict Machine Status evidence, and derives a stable state fingerprint.
- Attention-only tmux tails are typed for capture failures, ANSI-stripped, bounded, redacted, fenced as untrusted content, and hashed. Non-attention panes do not capture tails.
- `captureTmuxTail()` reports failure separately without changing legacy capture behavior. The shared blocked-path module now owns secret redaction for tail use.
- Covered acceptance criteria: partial AC-1 (project scope, structured envelope, attention tails), AC-11 (redaction/bounds/fencing), AC-13 (project isolation), and FR-1 through FR-6 read-side aspects. No approval, mutation, injection, or assistant tool has been introduced.

## Commands/results
- `git rev-parse --show-toplevel && git branch --show-current && git status --short --branch`: correct worktree/branch; clean before edits.
- `gh api repos/hyperbotsx/agentops-harness/issues/211`: canonical approved PRD read successfully.
- All four mandatory pre-implementation researcher consultations completed.
- `npm --prefix term-control-center ci`: passed; installed ignored local validation dependencies, `0 vulnerabilities`.
- `npm --prefix term-control-center run typecheck`: passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/orchestratorPanes.test.ts`: passed, 4 tests.
- `git diff --check`: passed.
- Checkpoint 1 revision 2: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 1 revision 2: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 22 tests.

## Checkpoint 1 revision 2
- Addressed `F211-C1-001`: the shared redaction boundary covers attach/session token forms; adversarial tail tests prove raw values are absent.
- Addressed `F211-C1-002`: tail clipping retains the newest whole UTF-8 characters and proves post-cap byte size.
- Addressed `F211-C1-003`: inventory determines the capped pane identities before building/capturing, and reads validated runtime tail line/byte limits.
- Addressed `F211-C1-004`: orchestrator uses a non-mutating active-project snapshot; legacy-state regression test proves no migration write.
- Addressed `F211-C1-005` and `F211-C1-KISS-001`: one semantic evidence reader selects newest valid project-bound verifier report by mtime; the receipt parser is directly reused and redundant/nested code removed.

## Checkpoint 1 revision 3
- Addressed remaining `F211-C1-004`: the authenticated route test now owns a temporary legacy-only state directory, asserts its active project ID, and compares all state file names/content/sizes/mtimes before and after GET. Production snapshot ownership moved to the orchestrator boundary so `adminProjects.ts` remains below the file-size limit.
- Addressed `F211-C1-KISS-002`: `adminProjects.ts` is 296 lines; `buildPane()` now delegates task/completion summaries and is below the function-size limit.
- Revision 3 validation: `npm --prefix term-control-center run typecheck` passed; focused orchestrator/receipt/heartbeat suite passed (22); `git diff --check` passed.

## Checkpoint 1 approval
- Verifier approved checkpoint 1 revision 4 with zero open findings. Full report intentionally not read after the approved compact verdict.

## Checkpoint 1 revision 4
- Addressed `F211-C1-006`: removed the divergent project snapshot parser. `readProjectRegistrySnapshot()` reuses canonical strict registry/settings parsing and performs legacy conversion in non-persisting mode; malformed/versionless/unsafe registry state fails closed. Focused regression covers unsafe versionless state.
- Re-addressed `F211-C1-KISS-002`: `buildPane()` now delegates state construction and response rendering to semantic helpers; `adminProjects.ts` is 299 lines and the inventory functions remain below the limit.
- Revision 4 validation: `npm --prefix term-control-center run typecheck` passed; focused orchestrator/receipt/heartbeat suite passed (23); `git diff --check` passed.

- Checkpoint 2 foundation: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts`: passed, 3 tests.
- Checkpoint 2 revision 1: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 1: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 30 tests.
- Checkpoint 2 revision 1: `git diff --check`: passed.
- Checkpoint 2 revision 2: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 2: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 33 tests.
- Checkpoint 2 revision 2: `git diff --check`: passed.
- Checkpoint 2 revision 3: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 3: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 34 tests.
- Checkpoint 2 revision 3: `git diff --check`: passed.
- Checkpoint 2 revision 4: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 4: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 34 tests.
- Checkpoint 2 revision 4: `git diff --check`: passed.
- Checkpoint 2 revision 5: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 5: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 34 tests.
- Checkpoint 2 revision 5: `git diff --check`: passed.
- Checkpoint 2 revision 6: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 6: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 34 tests.
- Checkpoint 2 revision 6: `git diff --check`: passed.
- Checkpoint 2 revision 7: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 2 revision 7: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/proposalStore.test.ts tests/orchestratorPanes.test.ts tests/validationReceipt.test.ts tests/heartbeatClassifier.test.ts`: passed, 34 tests.
- Checkpoint 2 revision 7: `git diff --check`: passed.
- Checkpoint 3 foundation: `npm --prefix term-control-center run typecheck`: passed.
- Checkpoint 3 foundation: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/paneInjection.test.ts`: passed, 10 tests.

## Checkpoint 2 revision 1
- The private `orchestrator-proposals.json` store now has strict versioned parsing, private-mode atomic writes, active-project-scoped lookups/mutations, 30-minute configurable TTL expiry, supersession, exact selection hashes, constant-time token comparison, and a serialized interprocess mutation lock.
- Only `ui` and `exact_phrase` approval surfaces are representable. The store has no assistant-facing route and returns a plaintext token only from its Node-owned approval operation; token storage is salted digest only. Human UI/phrase wiring remains the approved Checkpoint 5 surface work.
- `orchestrator-actions.jsonl` is append-only/private/rotated and records sanitized proposal, approval, consumption, pre-side-effect item attempts, results, supersession, recovery, and approval invalidation events. It retains only a bounded, redacted prompt excerpt, never a token digest/salt or raw terminal tail.
- Execution state persists per-item results. On store restart, approved tokens are invalidated; interrupted batches become failed with recorded partial results and no item auto-resumes.
- Focused tests cover reserved kinds, sensitive/oversize prompt rejection, project isolation, selection-bound single-use tokens, supersession, attempt-before-result ledger ordering, restart recovery, expiry, corruption, and lock contention.
- Checkpoint 3 owns live awaiting-input/role/recoverability checks and immediate fingerprint revalidation; this store preserves the required target/fingerprint and fails closed on malformed values.

## Checkpoint 2 revision 2
- Addressed `F211-C2-001`: payload validation now rejects secret-like field names and values recursively before persistence; ledger key summaries enforce the same policy and strict ledger readback rejects malformed/sensitive records.
- Addressed `F211-C2-002`: private-store initialization creates a dedicated marker; a missing initialized file fails closed. Persisted proposals now strictly validate unique item IDs, item/result ownership, result schema, approval schema, token expiry binding, and proposal/result lifecycle consistency.
- Addressed `F211-C2-003`: one proposal lock now serializes state and ledger writes; stale locks are never unlinked and instead visibly block mutation. The ledger is appended before each state save, so an append failure leaves no committed transition; focused fault injection proves this ordering.
- Addressed `F211-C2-004`: approval audit rows retain the exact approved item IDs and sanitized summaries. `readProposalLedger()` provides bounded validated filtering by proposal, group, and PRD issue.
- Addressed `F211-C2-KISS-001`: semantic request/event objects reduce every checkpoint helper to four parameters or fewer; strict lifecycle validation is expanded into named guards while `proposalStore.ts` remains under the 300-line limit.

## Checkpoint 2 revision 3
- Re-addressed `F211-C2-002`: store creation is now an explicit initialization operation only. Normal opening fails closed for missing state authority, and initialization refuses prior ledger/pending evidence. The persisted file, proposal, item, approval, result, supersession, and chronology schemas reject unexpected or inconsistent data.
- Addressed `F211-C2-003`: `proposalPersistence.ts` owns an atomic private pending-transition journal. Every event has an idempotent ID; startup reconciles the pending journal before normal recovery, writes missing ledger records once, applies the intended state checkpoint, then removes the journal. The focused recovery test simulates a ledgered completed result with a missing state checkpoint and proves it remains executed after restart.
- Re-addressed `F211-C2-004`: every ledger row now includes sanitized proposal scope identity, so proposal/group/issue filtering returns all lifecycle rows. Readback includes the bounded retained `.1` ledger. Event-specific parser requirements reject incomplete approval records.

## Checkpoint 2 revision 4
- Final bounded fix for `F211-C2-002`: explicit initialization recognizes both active and retained ledger authority. The pending journal has an exact schema, a transaction/state checkpoint binding, nonempty index-bound unique event IDs, and canonical item/result/event-state validation before it can write a ledger row.
- Final bounded fix for `F211-C2-004`: creation rows retain sanitized all-item summaries; approval-bound lifecycle rows retain exact selected identity. The parser now requires result status, reason code, and before fingerprint for attempt/result/recovery rows and enforces complete approval bindings for applicable events.

## Checkpoint 2 escalation — verifier revision 4
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- `F211-C2-002` remains after three bounded fixes and focused research: the pending journal validates individual event shape but does not prove its event set reduces to the persisted after-state. Verifier requires a transaction-level canonical reducer/equality check before any replay write.
- `F211-C2-004` remains after three bounded fixes and focused research: ledger parsing checks fields but accepts impossible semantics such as an `attempted` event with final `ok/delivered` outcome. Verifier requires a discriminated event-union validator that rejects inapplicable/impossible fields and status/reason pairs.
- Human authorization received: one exceptional bounded fix for the two stable findings; no other authority expanded.

## Checkpoint 2 exceptional revision 5
- `F211-C2-002` partially addressed: ghost proposals are rejected and item/result equality is checked, but verifier found pending event labels are not reduced through canonical transition semantics before comparison to the after-state.
- `F211-C2-004` partially addressed: impossible attempt/recovery outcome pairs are rejected, but verifier found no-action variants still accept inapplicable item-set fields.

## Checkpoint 2 escalation — verifier revision 5
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- The human-authorized exceptional revision is exhausted. `F211-C2-002` requires a typed canonical transition reducer against a bound before-state/revision, then exact comparison of its computed after-state before replay. `F211-C2-004` requires exact allowed-key sets for each audit event variant, including no-action variants.
- Human authorization received: one additional bounded fix for the two contracts; no other authority expanded.

## Checkpoint 2 exceptional revision 6
- `F211-C2-002` partially addressed: the transition reducer rejects ghost/mislabeled events and requires exact computed after-state equality, but verifier found replay does not compare `pending.before` to the current persisted checkpoint before replacement.
- Addressed `F211-C2-004`: no-action event variants now reject item-set evidence; creation retains item evidence under its dedicated contract while approval-bound variants retain it only with complete approval binding.

## Checkpoint 2 escalation — verifier revision 6
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- `F211-C2-002` remains: recovery must read the current state under the existing lock and accept it only if it exactly equals `pending.before` (apply) or `pending.state` (idempotent cleanup). Any third state must degrade without ledger/state mutation.
- Human authorization received: one final bounded fix for WAL-current-state binding; no other authority expanded.

## Checkpoint 2 exceptional revision 7
- Re-addressed `F211-C2-002`: reconciliation now reads the current checkpoint under the proposal lock. It applies a pending transition only when current state exactly equals `pending.before`, removes the journal idempotently when current state equals `pending.state`, and fails closed on any third state before any ledger or state write.

## Checkpoint 3 revision 1
- `injectPanePrompt()` now resolves its group and session only from live maps, requires exact pane/session/profile identity, an exact project and PRD-or-draft binding, `recoverability === recovered`, live transport, structured awaiting-input proof, and a bounded Node-side authority shape before any terminal write.
- The shared guard serializes a pane, binds deduplication to an explicit idempotency key, defaults to the binding one-minute per-pane rate limit, and consumes an idempotency key before an uncertain Enter failure so a retry cannot double-send.
- Supervised delivery uses a per-request named tmux buffer, bracketed paste with deletion, two changed-tail echo samples, then one literal Enter. Capture failures, failed liveness, paste failures, echo failures, and Enter failures are distinct fail-closed reasons. The tmux pane target is exact-session syntax (`=session:`); the scratch smoke exposed that bare `=session` is not accepted for `capture-pane`/`send-keys` on tmux 3.4.
- Fresh PTY sessions are explicitly `recovered`; planner/context-brief human-recovery callers now use the shared injection path and preserve the legacy draft binding as `legacy-default` project scope.
- Focused tests cover strict identity, unrecovered/dead/role/project/PRD/awaiting/authority rejection, named buffers, echo/capture/Enter failures, same-pane serialization, idempotency, one-minute rate limiting, and the planner PTY regression.
- Disposable tmux smoke completed on 2026-07-19: Pi 0.80.6, Claude Code 2.1.195, and Codex CLI 0.144.6 each echoed a bracketed-pasted multiline-safe draft in two samples before one literal Enter and returned the expected harmless acknowledgement. No captures/transcripts were persisted.
- Revision 1 validation: `npm --prefix term-control-center run typecheck` passed; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/paneInjection.test.ts` passed (15); targeted `tests/server.test.ts` planner-recovery tests passed (4); `git diff --check` passed.

## Checkpoint 3 revision 2
- Addressed `F211-C3-001`: the guard reserves an explicit key before the queued work begins and retains the exact promise/outcome without a time-based replay path. Echo/capture and Enter failures replay their original failed result with no further paste, PTY write, or Enter; one-minute limiting remains separate for different keys.
- Addressed `F211-C3-002`: echo confirmation now requires the normalized prompt occurrence count to increase over the pre-paste baseline in two samples. A pre-existing exact draft plus unrelated redraw cannot authorize Enter.
- Addressed `F211-C3-003`: active project scope is a server-owned callback read from the current project registry inside the pane lock. The live group and requested target must both match that scope.
- Addressed `F211-C3-004`: removed the caller-asserted awaiting-input shape and the future approved-item authority seam. Only role-bound human recovery remains; it must revalidate the relevant structured recovery gate immediately before delivery. Future C4 execution must introduce a consumed, item-bound capability and its structured live-state proof before reopening that path.
- Addressed `F211-C3-005`: project read, live group/session resolution, every preflight, and rate check now occur in the per-session serialized work body immediately before delivery.
- Addressed `F211-C3-006`: all supplied issue and draft bindings must match; a missing binding or either conflict fails closed.
- Addressed `F211-C3-KISS-001`: delivery/echo use semantic context objects, the recovery call uses one object, and the guard factory delegates its narrow API construction; changed functions are within the configured line/parameter limits.
- Revision 2 validation: `npm --prefix term-control-center run typecheck` passed; `tests/paneInjection.test.ts` passed (13); targeted planner-recovery server tests plus `contextBrief.test.ts` passed (5); `git diff --check` passed.

## Checkpoint 3 revision 3
- Re-addressed `F211-C3-001`: only terminal-attempt outcomes enter the same-action cache. A server-generated action ID is used for each explicit recovery request; a validated `x-idempotency-key` lets one client action retry with the same key. Preflight failures are not cached, later actions get new IDs, and guarded records are cleared when context/draft recovery groups retire.
- Addressed `F211-C3-004`: `authority` is runtime-validated as an exact two-field `human_recovery` discriminated variant before role/action matching; forged approved-item-shaped objects fail closed.
- Re-addressed `F211-C3-005`: after awaiting the recovery gate, the adapter rereads active project scope and resolves live map identity before a synchronous final preflight, so neither stale map objects nor the old project snapshot survive the await.
- Addressed `F211-C3-007`: PTY exceptions produce `write_failed`; runner exceptions produce `delivery_failed`; both are cached only after a terminal attempt as structured results.
- Addressed `F211-C3-KISS-002`: removed the unused delivery guard field.
- Addressed `F211-C3-HANDOFF-001`: touched paths/current revision are corrected and `contextBrief.test.ts` is run separately rather than counted through the name filter.
- Revision 3 validation: `npm --prefix term-control-center run typecheck` passed; `tests/paneInjection.test.ts` passed (19); targeted planner-recovery server tests passed (4); `tests/contextBrief.test.ts` passed (6); `git diff --check` passed.

## Checkpoint 3 revision 4
- Final bounded fixes for `F211-C3-001` and `F211-C3-005` follow the recorded consult: tmux liveness, baseline capture, and buffer setup are retryable pre-paste checks; the action becomes stable only immediately before `paste-buffer` or a PTY write. Pre-paste failures therefore do not consume rate limit or poison the same action key.
- The common `disposeSession()` lifecycle clears the shared injection guard, covering group kills, dead/retired groups, manual termination, and server shutdown; existing selected group-retirement cleanup remains harmless.
- Current state is coherently rechecked after the recovery/project awaits, and again after echo polling immediately before Enter. The bounded double-read rejects a changed project or recovery gate; live map identity is re-resolved synchronously after the final await.
- Revision 4 validation: `npm --prefix term-control-center run typecheck` passed; `tests/paneInjection.test.ts` passed (21); targeted planner-recovery server tests passed (4); `tests/contextBrief.test.ts` passed (6); `git diff --check` passed.

## Checkpoint 3 escalation — verifier revision 4
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- `F211-C3-005` remained after three bounded fixes and the focused researcher consult. The human authorized one exceptional architecture-level fix limited to a coherent versioned server-owned project/eligibility snapshot.

## Checkpoint 3 exceptional revision 5
- `server/projectScope.ts` owns an in-process active-project version. The only active-project selection mutation advances that version after its durable registry write; injection snapshots carry both project ID and version.
- Recovery eligibility is now synchronous at the terminal boundary: context recovery reuses synchronous `readyContextBrief`, planner recovery uses synchronous `planningBriefRecoveryRequired`. The adapter awaits only the project snapshot, then synchronously verifies its version, recovery eligibility, live maps, role/PRD, and project binding immediately before paste and again immediately before Enter.
- Adversarial regression covers a project-scope version invalidated during the final lookup; existing post-echo project/map removal coverage proves no Enter.
- Exceptional revision 5 validation: `npm --prefix term-control-center run typecheck` passed; combined `tests/paneInjection.test.ts tests/admin.test.ts` passed (48); targeted planner-recovery server tests passed (4); `tests/contextBrief.test.ts` passed (6); `git diff --check` passed.

## Checkpoint 3 escalation — exceptional revision 5
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- The exceptional version-only snapshot was insufficient: a stale registry read could be paired with the current version after active-project selection changes. The human then authorized the bounded authoritative controller revision below.

## Checkpoint 3 exceptional revision 6
- `ProjectScopeController` is the sole process-local authority for active project ID, epoch, and transition state. It starts fail-closed; `refreshProjectScope()` captures the controller epoch before a registry read and discards that read if selection started or completed while it was pending.
- `selectActiveProject()` enters transition before any registry/validation/persistence await, preventing injections; it publishes only after the durable write completes, and reconciles the durable active ID on failure while remaining fail-closed if reconciliation fails. Concurrent selection is rejected.
- Recovery refresh occurs before injection; the terminal path reads only the controller snapshot synchronously. The adapter verifies controller ID+epoch synchronously before paste and before Enter, eliminating stale registry-read minting from the terminal critical path.
- Added controller lifecycle and exact stale-read-after-selection-start regressions; exceptional revision 6 validation: typecheck passed; `tests/paneInjection.test.ts tests/projectScope.test.ts tests/admin.test.ts` passed (50); targeted planner-recovery server tests passed (4); `tests/contextBrief.test.ts` passed (6); `git diff --check` passed.

## Checkpoint 3 escalation — exceptional revision 6
- Compact verdict: `needs_human`; report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/verifier-report.md`.
- The controller's `transitioning` boolean conflates initialization and active selection: a stale initialization refresh can publish while a selection is in progress. The exceptional change also regressed archived-project rejection and lets refresh errors escape the structured injection boundary.
- The human authorized the bounded controller correction below.

## Checkpoint 3 exceptional revision 7
- The controller now has distinct `uninitialized`, `refreshing`, `stable`, `selecting`, and `failed` states. Refresh increments a token before its reader await; selection increments/enters `selecting` before every await. A refresh can publish only its matching `refreshing` token, so it cannot leak an initialization read through a selection transition.
- Concurrent selection rejects for every `selecting` state. Archived targets fail before validation/persistence. Refresh errors return `false`, leave scope unavailable, and therefore reach the adapter as structured `stale_state` rather than escaping the recovery helper.
- Added uninitialized stale-refresh/selection, concurrent-selection, and stable lifecycle regressions. Exceptional revision 7 validation: typecheck passed; `tests/paneInjection.test.ts tests/projectScope.test.ts tests/admin.test.ts` passed (51); targeted planner-recovery server tests passed (4); `tests/contextBrief.test.ts` passed (6); `git diff --check` passed.

## Checkpoint 3 approval
- Verifier approved exceptional revision 7 with zero open findings. The compact verdict was accepted without re-reading the full approved report.

## Skipped checks
- Full Term suite/build and Python unit suite remain pending for later checkpoints. A pre-fix full `server.test.ts` run exposed the planner-recovery gaps corrected above and one unrelated profile-default environment drift; focused recovery coverage passes after the bounded fix.

## Known risks / cleanup / standards exception
- General orchestrator execution has not yet been wired. Checkpoint 4 must introduce a consumed, item-bound approval capability, current fingerprint revalidation, and a structured awaiting-input producer before it can call the injection adapter.
- The current injection path is restricted to explicit human recovery routes with server-owned active-project and artifact-gate callbacks; it creates no assistant/tool/write route.
- Local `term-control-center/node_modules` was installed for validation and is ignored. No runtime state, captures, transcripts, or generated output were created. No standards exception.

## Checkpoint 4 revision 1
- `proposalStore` now rejects every completion sub-action except `prepare_pr`; `kody_review` accepts no model payload; `launch_lanes` accepts only structured lane selection. Launch targets must be an exact server-checked project ID. The ledger validator accepts this project-only target without leaking it into group/issue filters.
- `executeDelegatedProposal()` consumes the existing human-minted, proposal/item-set-bound token once, refreshes authoritative active-project scope, records each attempt before delegation, rechecks pane/project fingerprints, and persists sanitized per-item outcomes. It dispatches only `prepare_pr`, Kody review, and lane launches; `inject_prompt` remains unavailable to this delegation slice until its approved executor is composed in checkpoint 5.
- `prepareCompletionAction()` extracts the existing completion-route preflight/state-transition service. Delegated preparation calls it with `kodusReview: false`, preserving existing Prepare PR preflights while assigning the following explicit `kody_review` item sole trigger ownership.
- `triggerKodyReview()` is the shared Kody application service used by the existing Kody route and the orchestrator. It records/reuses the project-scoped PR request before any second trigger. Lane execution receives a server-owned existing confirmation and active project ID, then invokes unmodified `executeLanePlan()` so caps, queues, reuse, provisioning, and lane validation remain authoritative.
- Focused tests prove all three item kinds delegate once; Kody requests deduplicate; stale state produces an item result without side effects; reserved completion sub-actions and command-shaped lane payloads are rejected. No `git`/`gh` command string is accepted or injected by the orchestrator.
- Revision 1 validation: `npm --prefix term-control-center run typecheck` passed; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/delegatedActions.test.ts tests/kodyReviewTrigger.test.ts tests/proposalStore.test.ts tests/completedKodusReview.test.ts tests/completion-server.test.ts` passed (29); `git diff --check` passed.

## Checkpoint 4 revision 2
- Addressed `F211-C4-001` and `F211-C4-002`: preconditions are async and fail with the schema-defined `stale_state`; every delegated promise is awaited inside the item boundary, so a rejection records one sanitized failed result and later approved items continue deterministically.
- Addressed `F211-C4-003` and `F211-C4-004`: Kody trigger input is one named request object. Both the existing route and delegator use it; the route derives the active project only from the server-owned scope. Kody store IDs include project identity. A replay is discriminated: recorded requested/in-progress work may reuse, while failed/indeterminate records produce `blocked`, never a synthetic successful review.
- Addressed `F211-C4-005` and `F211-C4-006`: `launchStateFingerprint()` binds active-project scope version, selected lane/ad-hoc PRD, resolved lane-plan path, and lane-plan content. `launch_lanes` rechecks it immediately before delegation. The existing lane orchestrator now accepts exactly one synthetic ad-hoc PRD lane and feeds it through the same cap, queue, reuse, provisioning, confirmation, and launch loop.
- Addressed `F211-C4-007`: proposal target schemas are exact by item kind; pane actions cannot carry a conflicting project ID, while launches carry only project ID.
- Addressed `F211-C4-KISS-001`: moved semantic proposal validation into `proposalValidation.ts` (`proposalStore.ts` now 257 lines), changed Kody trigger to a request object, and extracted the Prepare PR application service into `completionPrepareAction.ts`; `completionRoutes.ts` is now a transport adapter for that service.
- Revision 2 validation: `npm --prefix term-control-center run typecheck` passed; `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/laneOrchestrator.test.ts tests/delegatedActions.test.ts tests/kodyReviewTrigger.test.ts tests/proposalStore.test.ts tests/completion-server.test.ts tests/completedKodusReview.test.ts` passed (33); `git diff --check` passed.

## Checkpoint 4 revision 3
- Pre-edit status for this continuation contained the approved checkpoints 1–3 and checkpoint 4 revision 2 dirty implementation/artifact files; no unrelated files were introduced by revision 3.
- Addressed `F211-C4-003`: TypeScript and Python now share `kody:<projectId>:<owner>:<repo>:<pr>` identity. Both writers locate project-matching target-only legacy records, rekey on upsert, and the Python requester reuses existing shared state before posting. Cross-writer coverage writes a legacy Python record and proves TypeScript sees one canonical record; Python coverage proves the reverse requester dedupes project-scoped state.
- Addressed `F211-C4-004`: a queued/pre-trigger record is now `blocked`, never a successful reuse or automatic retrigger. Terminal-negative records remain blocked; relayed running review state remains reusable. The queued crash-window regression proves zero trigger calls.
- Addressed `F211-C4-005`: `ProjectScopeController.selectionVersion` changes only when the observed active project changes, while ordinary refresh bookkeeping remains separate. Launch fingerprints use this selection generation plus resolved plan/ad-hoc content. Delegation passes the expected fingerprint and current-scope callback to `executeLanePlan()`, which re-resolves/rechecks before provisioning and again before queue/launch mutation. Focused tests cover unchanged refresh, changed plan/selection, and a post-await selection race.
- Addressed `F211-C4-006`: one ad-hoc item now requires the server-owned canonical issue reader to confirm an open issue with `status:approved` and `CEO approved: Yes` before any worktree provisioning. Batch confirmation remains launch confirmation only. Execution tests prove unapproved rejection before provisioning and approved ad-hoc cap, queue, and reuse behavior.
- Addressed `F211-C4-KISS-001`: lane parsing/resolution/fingerprinting/ad-hoc shaping moved to `laneRequestResolution.ts`; `laneOrchestrator.ts` is 161 lines. The Prepare worker takes one `PrepareJob` object rather than five parameters.
- Revision 3 validation: `npm --prefix term-control-center run typecheck` passed. Focused TypeScript suite passed (74): `tests/kodyReviewTrigger.test.ts tests/laneOrchestrator.test.ts tests/delegatedActions.test.ts tests/proposalStore.test.ts tests/completion-server.test.ts tests/completedKodusReview.test.ts tests/kodyReviewSync.test.ts tests/projectScope.test.ts tests/paneInjection.test.ts`. `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py -q` passed (10). `git diff --check` passed.
- Known unrelated baseline: a broader run that included `tests/kodyReview.test.ts` had one pre-existing static assertion failure in “fix-loop launch wiring carries selected findings into task details,” expecting a `launchGroup.ts` string no longer present; no revision-3 Kody/lane test failed. It is outside these five bounded findings and was not changed.

## Checkpoint 4 revision 4
- Addressed remaining `F211-C4-003`: each writer derives the canonical ID at upsert, collects every matching canonical and same-project target-only record, deterministically selects the canonical/current prior for revision continuity, and removes every duplicate. Cross-writer coverage seeds persisted coexisting legacy/canonical rows, then proves both Python and TypeScript upserts retain exactly one canonical row.
- Addressed remaining `F211-C4-005`: queue processing now has one mutable `QueueProcessor` whose refreshed global running count flows from each pending batch to the next. The two-batch execution regression queues two approved ad-hoc lanes, releases one global slot, and proves exactly one lane starts.
- Addressed remaining `F211-C4-006`: canonical evidence now requires all four facts: open state, `type:prd`, `status:approved`, and `CEO approved: Yes`. Focused parser coverage rejects each missing/invalid fact.
- Addressed remaining `F211-C4-KISS-001`: semantic `LaneBatch`, `LaneLaunchJob`, `SelectedGroups`, and `QueueProcessor` objects keep lane helper parameter counts at four or fewer. The readable lane orchestrator is 219 lines; request resolution is 120 and Prepare remains 59.
- Revision 4 validation: `npm --prefix term-control-center run typecheck` passed. Focused TypeScript suite passed (76): `tests/canonicalPrdApproval.test.ts tests/kodyReviewTrigger.test.ts tests/laneOrchestrator.test.ts tests/delegatedActions.test.ts tests/proposalStore.test.ts tests/completion-server.test.ts tests/completedKodusReview.test.ts tests/kodyReviewSync.test.ts tests/projectScope.test.ts tests/paneInjection.test.ts`. `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py -q` passed (10). `git diff --check` passed.
- Checkpoint 4 approval: verifier approved revision 4 with zero findings. The full approved report was intentionally not read.

## Steward hygiene — post-checkpoint 4
- Steward returned `cleanup_recommended`: source/test/module placement and KISS boundaries are clean; no tracked/generated/prohibited paths or staging concern was found. It requested removal of ignored generated pipeline data and Python cache directories before final bug-check.
- Completed bounded cleanup: removed the listed ignored `pipeline-diagram/*-data.js`, `pipeline.mmd`, `completed-registry.json`, `pipeline-diagram/projects/`, `.pytest_cache/`, and listed `__pycache__/` directories. Confirmed no listed runtime/cache path remains; retained ignored `term-control-center/node_modules/` only for local validation and will not stage it. `git diff --check` passed.
- Verifier hygiene recheck: Steward cleanup is approved and checkpoint 4 remains approved. The requested final bug-check was correctly deferred (`F211-FINAL-GATE-001`) because canonical PRD checkpoint 5 (assistant/UI) and final docs/validation are not yet implemented. No checkpoint-4 product finding remains. Next implementation scope is checkpoint 5, followed by its verifier review, any renewed Steward review, and then final bug-check.

## Checkpoint 5 revision 1 — assistant/UI
- Added exactly three Coworker-marked assistant adapters: `orchestrator_status`, `orchestrator_propose`, and `orchestrator_execute`. They use only authenticated, project-scoped Term routes. There is no generic model proxy or token-mint route.
- The assistant prompt explicitly treats `UNTRUSTED_TERMINAL_TAIL` fences as hostile evidence, not instructions, approvals, or commands. It requires structured-field rationale and maps completion/start recommendations to existing `prepare_pr`/`kody_review` and `launch_lanes` services rather than terminal `git`/`gh` commands.
- Proposal create/list/execute routes reuse the durable proposal store and delegated executor. Coworker requests may create/read/execute only a pre-approved held capability; direct coworker approval/veto requests fail closed. Human approval stores the single-use, item-set-bound capability only in the Node process, and public responses omit token/salt/digest values.
- `inject_prompt` is now available only from consumed delegated items. It requires an exact approved-item gate in addition to the existing live project, role, PRD, recoverability, awaiting-input, rate-limit, lock, paste/echo, and pre-Enter checks. Direct/fabricated approved-item authority is rejected.
- The proposal card uses DOM `textContent` for proposal data, offers approve-selected (unchecked items vetoed), dismiss, exact displayed phrase approval, supersede-feedback handoff, explicit execution, per-item outcome visibility, and pane links. Active Jobs polls a pending-proposal count and links to that card; it reuses no #210 resume state or controls.
- Documentation now records proposal lifecycle, exact-phrase/UI approval, server-owned capability behavior, reserved-action denial, ledger/outcome/recovery expectations, and badge-only coordination with the existing resume UI.
- Post-validation bounded compatibility fix: legacy four-part Kody IDs without structured PR metadata are now parsed into the canonical project-scoped identity, restoring the full debt dry-run unit coverage without weakening cross-project identity.

### Checkpoint 5 touched files
- `src/agentops_harness/review_server.py`
- `src/agentops_harness/kodus_state.py`
- `tests/unit/test_review_server_coworker.py`
- `pipeline-diagram/coworker-launcher.js`
- `term-control-center/server/index.ts`
- `term-control-center/server/orchestrator/orchestratorRoutes.ts`
- `term-control-center/server/orchestrator/orchestratorProposalService.ts`
- `term-control-center/server/orchestrator/proposalStore.ts`
- `term-control-center/server/orchestrator/delegatedActions.ts`
- `term-control-center/server/orchestrator/paneInjection.ts`
- `term-control-center/src/JobSidebar.tsx`
- `term-control-center/src/JobSidebar.css`
- `term-control-center/tests/orchestratorCheckpoint5.test.ts`
- `term-control-center/tests/coworkerLauncher.test.ts`
- `term-control-center/tests/terminalJobSidebar.test.ts`
- `term-control-center/tests/paneInjection.test.ts`
- `docs/agentops-terminal-sessions.md`
- `term-control-center/README.md`

### Checkpoint 5 validation
- `npm --prefix term-control-center run typecheck`: passed.
- Focused TypeScript suite (`orchestratorCheckpoint5`, `coworkerLauncher`, `terminalJobSidebar`, `delegatedActions`, `paneInjection`, `proposalStore`): passed, 66 tests.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_debt.py tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q`: passed, 103 tests.
- `npm --prefix term-control-center run build`: passed (existing Vite non-module script notices and chunk-size warning only).
- `PYTHONPATH=src python3 -m pytest tests/unit -q`: 1258 passed; one pre-existing unrelated failure remains in `test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`. Current production code intentionally filters `issueNumber == 'unlinked'`, contrary to that stale assertion; no #211 path was changed.
- `npm --prefix term-control-center run test`: did not complete before the 600-second timeout. The isolated `tests/server.test.ts` reproduces the known unrelated profile-default environment drift at `recovers tmux launch groups after service restart` (`codex-default` expected vs configured `codex-gpt-5-6-luna`) and then remains live after the failed test. Checkpoint 5 focused and build validation pass.
- `git diff --check`: passed.
- Removed test-created build/dist, Python caches, and ignored pipeline generated output. Ignored `term-control-center/node_modules/` remains local validation-only and unstaged.

### Next gate
- Checkpoint 5 requires verifier review. If approved, request Steward hygiene because assistant topology, UI, docs, and run artifacts changed; then request the final verifier bug-check only after Steward recheck and the documented validation exceptions are accepted.

## Checkpoint 5 revision 2 — bounded verifier fixes
- Addressed `F211-C5-001`: route and executor share the live heartbeat map, and the production integration test is enabled. It reads a `waiting_on_human` heartbeat fingerprint through `/api/orchestrator/panes`, creates/approves/executes through the authenticated production routes, and proves no false `stale_state` result. Execution also reads the non-mutating project-registry snapshot.
- Addressed `F211-C5-002`: `src/agentops_harness/orchestrator_adapters.py` owns the deterministic one-shot directive dispatcher. Only `status`, `propose`, and `execute` are dispatchable; there is no generic proxy/tool loop. The chat path catches a blocked adapter request and records a safe assistant reply. Coworker status/propose/execute tests cover pane status, `prepare_pr`, `kody_review`, and lane recommendations. Lane proposal fingerprints are derived server-side from the selected lane context before persistence, rather than minted by the model.
- Addressed `F211-C5-003`: proposal creation runs the semantic server-owned preflight against the authoritative envelope after project-scope refresh. It rejects absent, role/PRD-mismatched, stale, and moving/non-awaiting injection targets before the durable store writes.
- Addressed `F211-C5-004`: the approved-item recovery gate binds the exact proposal fingerprint and runs after pane-lock acquisition and again immediately before Enter. A deterministic echo-phase drift test proves paste has no Enter after fingerprint change.
- Addressed `F211-C5-005`: proposal validation rejects raw `git`/`gh` terms anywhere in an injection prompt, shell chaining/substitution, redirection, and command pipes. Tests retain conversational recovery prompts and the structured `prepare_pr` plus `kody_review` alternative.
- Addressed `F211-C5-006` and `F211-C5-007`: the extracted proposal-card module renders the full copyable exact phrase, strict phrase matcher, bounded role/PRD/group identity, supported `board.html?session=` pane link, and retained approved/vetoed selection/outcome state. DOM behavior tests cover these contracts.
- Addressed `F211-C5-KISS-001`: assistant adapters and proposal-card rendering moved from oversized integration files to semantic modules. `server/index.ts` remains composition; no generic assistant proxy was added. `delegatedActions.ts` is 179 lines, routes 131, preflight 27, proposal service 58. `review_server.py` and the launcher retain their established legacy size but the new concerns are thin wiring only.

### Revision 2 validation
- `npm --prefix term-control-center run typecheck`: passed.
- Focused TypeScript suite: 97 passed (`canonicalPrdApproval`, `coworkerLauncher`, `coworkerProposals`, `delegatedActions`, `kodyReviewTrigger`, `laneOrchestrator`, `orchestratorCheckpoint5`, `paneInjection`, `projectScope`, `proposalPreflight`, `proposalStore`, `terminalJobSidebar`).
- Focused Python suite: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_debt.py tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` passed, 105 tests.
- `npm --prefix term-control-center run build`: passed; only existing Vite non-module-script and chunk-size warnings.
- `PYTHONPATH=src python3 -m pytest tests/unit -q`: 1260 passed plus the documented unrelated stale `test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row` failure.
- `npm --prefix term-control-center run test`: rerun was bounded at 620 seconds and timed out without a checkpoint-5 assertion failure, retaining the documented unrelated full-suite/profile-default live-process limitation.
- `git diff --check`: passed.
- Cleanup: removed generated Term `build/` and `dist/`, Python caches, and generated pipeline data; ignored `term-control-center/node_modules/` remains unstaged for local validation.

### Revision 2 next gate
- Request verifier re-review for checkpoint 5 only. Do not request final bug-check until checkpoint 5 is approved, a Steward hygiene review is completed, and verifier rechecks that cleanup.

## Checkpoint 5 revision 3 — bounded status-to-proposal and KISS fixes
- Addressed remaining `F211-C5-002`: `orchestrator_status` now appends a bounded `pane-status-v1` JSON evidence block to the ordinary assistant reply/transcript. It contains only validated `groupId`, `sessionId`, `role`, `issueNumber`, `stateFingerprint`, and classification status for at most 20 panes. It explicitly excludes terminal tails, titles/prompts, tokens, sockets, and arbitrary envelope fields, labels the evidence read-only/non-authorizing, and leaves server proposal preflight authoritative. No generic proxy, provider-native tool loop, or extra inference pass was added.
- The one-shot integration test now derives its second-turn `completion_action`/`kody_review` target and fingerprint by parsing the exact prior model-visible `pane-status-v1` evidence rather than pre-seeding those values. Its lane item remains server-fingerprinted; all dispatches remain limited to status/propose/execute.
- Addressed remaining `F211-C5-KISS-001`: `proposeItems()` now accepts one semantic `ProposalCreateRequest` object rather than five parameters. The Python adapter `approve()` has four meaningful parameters; its unused project argument was removed. New semantic modules remain small.
- Focused dead-end researcher consult (2026-07-19) completed before this third bounded C5-002 fix. It recommended exactly this capped, server-authored, non-tail evidence block in the existing transcript rather than a second inference or generic tool loop; sources are `orchestrator_adapters.py`, `review_server.py`, the system policy, and the prior focused test, recorded in the researcher response for this run.

### Revision 3 validation
- `npm --prefix term-control-center run typecheck`: passed.
- Focused TypeScript suite (`orchestratorCheckpoint5`, `delegatedActions`, `proposalPreflight`, `paneInjection`, `coworkerProposals`, `coworkerLauncher`): 52 passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q`: 90 passed.
- `git diff --check`: passed.
- No generated build/cache/pipeline artifact was introduced by this revision.

### Revision 3 next gate
- Request verifier re-review for checkpoint 5 only. Do not request Steward or final bug-check until checkpoint 5 is approved.

## Checkpoint 5 approval
- Verifier approved checkpoint 5 revision 3 with zero open findings. The compact approved verdict was accepted without reading the full report.
- Required next gate: Steward hygiene review for the assistant/UI/docs topology and run artifacts, followed by verifier cleanup recheck. Final bug-check remains deferred.

## Steward hygiene — post-checkpoint 5
- Steward returned `clean`: assistant adapters, Term services, proposal-card UI, tests, docs, and run artifacts are correctly placed; no duplicate resume UI, deployment change, repo-local skill, oversized new semantic module, generated/runtime/cache artifact, or staging concern was found. `term-control-center/node_modules/` remains ignored and unstaged.
- Steward report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-211-terminal-orchestration-batch-resume/steward-response-checkpoint-5.md`.
- Required next gate: request verifier cleanup recheck. Final bug-check remains deferred until that recheck is approved.
- Verifier approved the Steward hygiene recheck with zero findings and marked the run ready for the final bug-check.

## Final bug-check revision 1 — bounded fixes for F211-FINAL-001..008
Verifier report `revision_requested` (8 findings). All fixes preserve human-only approval and keep raw shell injection non-proposable; no PR/merge/deploy performed.

- `F211-FINAL-001` (self-echo invalidates the approved fingerprint): decomposed the pane fingerprint. `paneInventory.ts` exports `coreStateFingerprint()` (classification + machine-status, excluding the attention tail). `paneInjection.ts` threads a `postEchoGate` used for the pre-Enter recheck (falling back to `recoveryGate` for human recovery). `delegatedActions.ts` captures the approved core fingerprint at the full-match pre-paste gate (`approveInjection`) and, pre-Enter, requires the same core fingerprint and an injectable classification (`reinjectable`) — tolerating the orchestrator's own tail echo while still blocking any independent classification/machine-status change. Integrated test in `delegatedActions.test.ts` builds a real envelope fingerprint with a fake tmux runner: one normal echo reaches one Enter; an independent classification change still blocks Enter.
- `F211-FINAL-002` (PTY newline without echo verification): `writePty` now writes the draft only, confirms the complete echo with the shared bounded policy (`echoConfirmed` generalized to a `poll` source reading the session output buffer), re-runs the current-authority `currentLivePane` recheck, then submits exactly one newline; unconfirmed echo fails closed with no newline. Pre-write capture stays retryable outside the idempotency guard. `paneInjection.test.ts` covers split draft/newline, fail-closed on no echo, and authority recheck before the newline.
- `F211-FINAL-003` (raw shell reachable via `inject_prompt`): `proposalValidation.commandShapedPrompt()` replaced the narrow denylist with a conversational-prompt contract rejecting `;`/`|`/`&&`/`||`, newlines, `$()`/`${}`/backticks, redirection, leading path executables, leading known executables, and any executable-plus-flag shape, while keeping ordinary recovery prompts. Adversarial cases (semicolons, `python3 -c`, unlisted pipe targets, leading `./script`, embedded newline) added to `delegatedActions.test.ts`.
- `F211-FINAL-004` (concurrent Python Kody double-trigger): `kodus_state.py` adds `reserve_session()`/`release_session()` that atomically claim the canonical project/PR identity under the shared cross-language lock before any external trigger, and makes the lock bounded-blocking so a loser waits and reuses instead of failing. `kodus_agent.request_review()` reserves first; only the reservation owner posts/relays, all other writers return reused/blocked, and a relay failure rolls the reservation back. New Python/Python concurrency and reserve-before-side-effect tests in `test_kodus_agent.py`.
- `F211-FINAL-005` (orphaned approval capability): `orchestratorProposalService.executeApprovedProposal()` no longer deletes the hold before the operation; it deletes only after a successful consume and, on a pre-consume failure, restores the hold when the durable proposal is still `approved`. `proposalPersistence.reconcileProposalTransition()` rolls back (discards) a replayed pending transition that mints an approval capability, so a WAL fault that never returned the plaintext token cannot reconcile into usable `approved`. Fault tests added in `delegatedActions.test.ts` (transient pre-consume scope failure preserves capability) and `proposalStore.test.ts` (approval WAL fault rolls back to proposed and stays re-approvable).
- `F211-FINAL-006` (premature supersede retirement): `coworker-launcher.js` `supersedeProposal()` no longer vetoes the original; it only seeds the feedback input, leaving the original `proposed` for the single atomic supersession at replacement creation. UI behavior test in `coworkerLauncher.test.ts` and a store test in `proposalStore.test.ts` (failed replacement leaves the original proposed; later linked replacement supersedes).
- `F211-FINAL-007` (grounded status omitted): `orchestrator_adapters.py` `proposal_row()` extends the bounded server-authored evidence whitelist with completion status/availableActions and machine-status decision/checkpoint/next-actor/bug-check-status (tails/titles/tokens still excluded). `test_review_server_coworker.py` now derives the Prepare PR/Kody recommendation and target from the prior `pane-status-v1` transcript evidence.
- `F211-FINAL-008` (runtime store degradation hangs the request): `orchestratorRoutes.ts` route handlers are now dispatched through a bounded rejection handler that returns the structured `orchestrator_degraded` (503) response instead of leaking an unhandled rejection. Live HTTP test in `orchestratorCheckpoint5.test.ts` holds the proposal-store lock after startup and asserts the degraded response.

### Final bug-check revision 1 touched files
- `term-control-center/server/orchestrator/paneInventory.ts`, `paneInjection.ts`, `delegatedActions.ts`, `proposalValidation.ts`, `orchestratorProposalService.ts`, `proposalPersistence.ts`, `orchestratorRoutes.ts`
- `src/agentops_harness/kodus_state.py`, `kodus_agent.py`, `orchestrator_adapters.py`
- `pipeline-diagram/coworker-launcher.js`
- Tests: `term-control-center/tests/paneInjection.test.ts`, `delegatedActions.test.ts`, `proposalStore.test.ts`, `coworkerLauncher.test.ts`, `orchestratorCheckpoint5.test.ts`, `tests/unit/test_kodus_agent.py`, `tests/unit/test_review_server_coworker.py`

### Final bug-check revision 2 validation
- Passed 2026-07-21: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/paneInjection.test.ts tests/delegatedActions.test.ts tests/proposalStore.test.ts tests/coworkerLauncher.test.ts tests/coworkerProposals.test.ts tests/orchestratorCheckpoint5.test.ts` — 66 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 102 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after build validation. The existing Vite non-module-script and chunk-size warnings did not fail the build.
- Documented unrelated baseline exceptions are unchanged: the stale `test_completed_work.py::test_unlinked_merged_pr_emits_warning_row` assertion and the Term full-suite profile-default/live-process timeout.

### Final bug-check revision 2 next gate
- Final bug-check revision 2 returned `revision_requested` with F211-FINAL-001, F211-FINAL-003, F211-FINAL-004, F211-FINAL-005, and F211-FINAL-KISS-001. The full report is in `verifier-report.md`.

### Final bug-check revision 3 — bounded fixes
- `F211-FINAL-001`: post-echo authorization now compares the approved core state and tail, allowing only the exact approved draft echo; a same-classification unrelated tail mutation blocks Enter. `injectPrompt` was also split into a one-job-argument helper plus focused builders, resolving `F211-FINAL-KISS-001`.
- `F211-FINAL-003`: proposal validation now rejects generic bare command-line prompts using a positive conversational-prompt boundary. Tests cover `cat /etc/passwd`, `touch /tmp/pwned`, `whoami`, `ls /tmp`, and `cp source target`.
- `F211-FINAL-004`: Node and Python Kody writers use an atomic shared-file-lock reservation with owner nonces and conditional finalization/release. Mixed-writer regression coverage verifies only one first side effect.
- `F211-FINAL-005`: pending approval-capability transactions now roll back whether their before or after state was persisted, preventing an approval with no returned plaintext capability. The applied-state cleanup-fault regression is covered.

### Final bug-check revision 3 validation
- Passed 2026-07-21: focused TypeScript suite across injection, delegated actions, proposal store, Kody trigger/sync, coworker, and checkpoint routes — 85 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 102 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after validation. Existing Vite script/chunk warnings remain non-fatal.
- No Steward re-review is required: these are narrow in-place corrections and test additions with no material topology or artifact-placement change.

### Final bug-check revision 3 next gate
- Final bug-check revision 3 returned `revision_requested` with F211-FINAL-001, F211-FINAL-003, F211-FINAL-004, and F211-FINAL-KISS-002. F211-FINAL-005 and F211-FINAL-KISS-001 are closed.

### Final bug-check revision 4 — bounded fixes
- `F211-FINAL-001`: expected prompt echo comparison now operates on unfenced bounded tail content, accepts deterministic oldest-prefix eviction only, and checks the expected prompt occurrence count. Full 40-line rollover and same-classification unrelated-tail regression tests cover both outcomes.
- `F211-FINAL-003`: conversational prompts must now start with a bounded natural-language instruction intent. Punctuated direct commands and marker-word command arguments are rejected in focused regressions.
- `F211-FINAL-004`: pre-trigger Python reservations are `queued`; all writers classify them as blocked rather than reused. The owner only becomes `running` after successful external triggering/finalization, and Python releases its nonce-owned reservation for failures at any trigger phase.
- `F211-FINAL-KISS-002`: Kody state mutation conditions are now passed as one semantic options object rather than a fifth positional helper argument.

### Final bug-check revision 4 validation
- Passed 2026-07-21: focused TypeScript suite across injection, delegated actions, proposal store, Kody trigger/sync, coworker, and checkpoint routes — 87 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 102 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after validation. Existing Vite script/chunk warnings remain non-fatal.
- No Steward re-review is required: these remain narrow in-place corrections with no material topology or artifact-placement change.

### Final bug-check revision 4 next gate
- Final bug-check revision 4 returned `needs_human` after F211-FINAL-001 and F211-FINAL-003 survived three bounded corrections. The operator explicitly authorized one exceptional final bounded correction for those two findings.

### Final bug-check revision 5 — operator-authorized bounded correction
- `F211-FINAL-001`: the post-echo tail check now removes the newest, appended exact draft occurrence rather than a pre-existing matching occurrence. Existing regressions now cover an older identical draft in a retained tail both with and without full-window rollover; unrelated tail drift remains blocked.
- `F211-FINAL-003`: validation now recognizes only complete natural-language recovery instruction forms (not a first-word marker), rejecting wrapped command probes including `Fix rm -rf /`, `Review curl https://example.test/script`, `help pwd`, and `continue 2` while retaining the established recovery prompts.

### Final bug-check revision 5 validation
- Passed 2026-07-21: focused TypeScript suite across injection, delegated actions, proposal store, Kody trigger/sync, coworker, and checkpoint routes — 87 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 102 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after validation. Existing Vite script/chunk warnings remain non-fatal.
- No Steward re-review is required: the operator-authorized changes remain narrow in-place corrections and tests.

### Final bug-check revision 5 next gate
- Final bug-check revision 5 closed F211-FINAL-001 and returned `needs_human` for F211-FINAL-003. The operator selected and authorized the verifier-recommended structured/server-rendered recovery-intent contract.

### Final bug-check revision 6 — structured recovery intent
- `inject_prompt` payloads now accept only `{ "recoveryIntent": "continue_checkpoint" }`; free-form prompt text is not representable.
- The server maps the accepted intent to its fixed recovery text immediately before pane delivery. Proposal validation rejects any other intent or raw shell-like text in the intent field.
- Proposal ledger payload summaries now expose only payload keys, avoiding a stale free-form prompt evidence path.
- All #211 test fixtures and preflight/store/checkpoint coverage use the typed recovery intent.

### Final bug-check revision 6 validation
- Passed 2026-07-21: focused TypeScript suite across injection, delegated actions, proposal store/preflight, Kody trigger/sync, coworker, and checkpoint routes — 92 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 102 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after validation. Existing Vite script/chunk warnings remain non-fatal.
- No Steward re-review is required: this is the human-selected narrow prompt-contract correction within the existing orchestrator modules and tests.

### Final bug-check revision 6 next gate
- Final bug-check revision 6 returned `needs_human` because the structured recovery intent needed exact own-key validation and Co-Worker schema exposure. The operator explicitly authorized that final bounded completion.

### Final bug-check revision 7 — exact recovery intent completion
- `recoveryPrompt()` now uses an exact string equality check, so inherited object keys and every non-`continue_checkpoint` value fail proposal validation before persistence.
- The Co-Worker system policy now states the exact `inject_prompt` payload shape and the server-rendered prompt boundary.
- Added an assistant status-to-proposal integration test that derives the target/fingerprint from bounded status evidence and emits only `{ "recoveryIntent": "continue_checkpoint" }`.
- Focused validation rejects the verifier’s inherited-key probes (`toString`, `constructor`, `valueOf`, `__proto__`) and raw prompt strings.

### Final bug-check revision 7 validation
- Passed 2026-07-21: focused TypeScript suite across injection, delegated actions, proposal store/preflight, Kody trigger/sync, coworker, and checkpoint routes — 92 passed, 0 failed.
- Passed 2026-07-21: `PYTHONPATH=src python3 -m pytest tests/unit/test_kodus_agent.py tests/unit/test_review_server_coworker.py -q` — 103 passed.
- Passed 2026-07-21: `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build`; `git diff --check`.
- Removed generated `term-control-center/dist` and `term-control-center/build` after validation. Existing Vite script/chunk warnings remain non-fatal.
- No Steward re-review is required: this is the exact human-authorized schema/policy/test completion within existing modules.

### Final bug-check approval
- Verifier approved final post-context bug-check revision 7 on 2026-07-21: `open_findings: 0`, `bug_check_status: passed`.
- Final evidence is the compact approved verifier verdict; the full report was intentionally not read after approval.

### PR #270 Kody findings — bounded remediation
- Kody reported five medium findings on PR #270. This slice addresses: Co-Worker graceful degradation for `URLError`; async, 15-second-bounded canonical PRD `gh` reads; strict requested-project lookup; per-project lane-plan default/marker validation; duplicate-lane and configured-slot rejection.
- `laneRequestResolution.ts` retains legacy root-plan behavior only while no saved multi-project configuration exists; saved configurations fail closed for absent/archived project IDs and use a project-scoped plan.
- Validation passed: focused TypeScript 72/72, focused Python 106/106, typecheck/build/diff check passed. Generated build artifacts were removed; Vite script/chunk notices remain non-fatal.

### Kody remediation verifier gate
- Verifier revision 1 closed three Kody findings and returned F270-KODY-001 / F270-KODY-003: catch `OSError` transport failures, and derive/strictly bind the unsaved default project identity.

### Kody remediation revision 2
- Co-Worker degradation now catches `OSError` (including established-connection `TimeoutError`) and the focused regression asserts the stored safe reply.
- Unsaved project configuration now derives the canonical default registry identity; only that ID, omitted ID, or `legacy-default` is accepted. Arbitrary IDs fail before binding the default repository/settings. Legacy root plan compatibility remains only for this derived default path.
- Validation: focused TypeScript 74 passed with one documented unrelated Browser-QA environment preflight failure; targeted lane/project identity assertions passed. Focused Python 106 passed; typecheck/build/diff check passed. Generated build artifacts were removed.

### Kody remediation revision 2 next gate
- Verifier revision 2 approved F270-KODY-003 and returned only F270-KODY-001 because the source/test still caught `URLError` rather than `OSError`.

### Kody remediation revision 3
- `coworker_orchestrator_response()` now catches `OSError`, covering `URLError`, `TimeoutError`, and other bounded urllib/socket transport failures.
- The focused timeout regression asserts both the returned safe reply and the appended assistant message in the active Co-Worker session.
- Passed: focused Co-Worker Python suite 94/94, TypeScript typecheck, and diff check. The launch-project identity assertion continues to pass; its unrelated Browser-QA environment preflight remains a documented baseline failure.

### Kody remediation approval
- Verifier approved PR #270 Kody remediation revision 3 with zero open findings.
- The compact approved verdict was accepted without reading a full report.
- Before re-triggering Kody, local configuration was checked: the local Kody fix-loop launch plan explicitly uses Codex for coder/verifier panes; the external Kody trigger itself is a GitHub comment/webhook integration and exposes no local Claude model setting.
- Commit and push the approved remediation to PR #270, then request the advisory Kody re-review.
