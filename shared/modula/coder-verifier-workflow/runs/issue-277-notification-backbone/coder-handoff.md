# Coder handoff — Issue #277 Notification Backbone

## Source and authorization

- Canonical source: GitHub issue #277.
- Planning brief: `dev-plans/drafts/frd-f3-notification-backbone-planning-brief.md`.
- Branch: `prd/notification-backbone-277`.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-277`.
- Lead authorized the full CP-1 → CP-3 verifier loop on 2026-07-23. No PR, merge, deploy, or GitHub mutation is authorized.
- Lead attested on 2026-07-23 that `agentops-trio` is the operator-configured same-worktree pool for this run: it contains exactly lead, coder, and verifier, all rooted at this worktree. Treat `coder@agentops-trio` as the authorized local identity for this run.

## Pre-edit status

- `git status --short --branch`: clean on `prd/notification-backbone-277`.
- Pre-existing dirty files: none.
- Research-first surfaces read: Python activity core/models/state/sources, TS activity notification stack, Slack activity-delivery trio, and badge registry/emit/activity-center path.

## Scope boundaries

- Current checkpoint: CP-1 only — FR-1/FR-2 event contract, taxonomy, Python router recording/delivery skeleton, source mapping, and unit tests.
- Forbidden in CP-1: TS producer changes, endpoint/UI/badge changes, Slack deletion/config edits, mutes/unread persistence, PR actions, and deployments.
- Full gates per commit: `cd term-control-center && npm test`, `npm run typecheck`, `npm run build`, and `PYTHONPATH=src python3 -m pytest tests -q`.

## CP-1 implementation

- Added the single Python `NotificationEvent` contract and exact seven-kind taxonomy in `src/agentops_harness/notification_router.py`.
- Added a central eight-source mapping and `docs/notification-backbone.md` mapping table.
- Routed the Python activity summary adapters through the router. Existing source fields remain intact while every returned item carries `kind` and `needs_human`.
- Router validates kind before append-only in-memory recording and invokes the unread/badge seam plus reserved email/chat channel bindings. No outbound email/chat behavior exists.
- Native line review removed unused stamping code, tightened taxonomy type declarations, preserved job refs, and replaced fragile positional additive state-field reconstruction with named arguments.
- Extended `ActivityItem` additively with `kind`, `provenance`, `needs_human`, and `deep_link`; state round trips preserve those fields.
- Added focused router, source-adapter, summary, and state-round-trip coverage.

### Revision 2 — verifier findings addressed

- `V277-CP1-001`: changed the additive needs-human field to tri-state during source adaptation, preserving an explicit value while deriving legacy items from the attention bucket. State reconstruction now applies the same fallback for records without the additive field.
- `V277-CP1-002`: made `NotificationKind` the sole taxonomy declaration; the runtime tuple and source mapping derive from that enum.

### Lead disposition — scope boundary

> `e5b5574`, `c334acd`, and `d77f6a2` (docs/product-prd.md, dev-plans/drafts/agentic-model-fusion-brief.md, dev-plans/drafts/agent-role-registry-brief.md) are LEAD-AUTHORED, OPERATOR-DIRECTED documentation commits — Erik requested each in-session, and they ride this branch deliberately to land with the F3 squash. They are authorized branch content, owned by lead, and permanently OUTSIDE the CP scope boundary: exclude them from checkpoint file boundaries and reviews, and do not modify them. Any future lead-authored `docs(...)` commit on this branch follows the same rule.

### Revision 3 — verifier findings addressed

- `V277-CP1-003`: extracted small review construction and metadata helpers, leaving `review_item()` below the function-size gate.
- `V277-CP1-004`: restored `job_id` from the real review-job source into metadata and added an adapter regression that verifies the emitted job ref.
- `V277-CP1-005`: resolved by the lead disposition above; lead documentation commits are excluded from CP-1 review scope.

## Files changed

- `docs/notification-backbone.md`
- `src/agentops_harness/activity_center.py`
- `src/agentops_harness/activity_center_models.py`
- `src/agentops_harness/activity_center_runtime.py`
- `src/agentops_harness/activity_state.py`
- `src/agentops_harness/notification_router.py`
- `tests/unit/test_activity_state.py`
- `tests/unit/test_notification_router.py`

## Validation

- Focused: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests/unit/test_notification_router.py tests/unit/test_activity_center.py tests/unit/test_activity_state.py -q` — passed (`31 passed`).
- Full Python: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — expected pre-existing failure only: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`; `1311 passed, 60 subtests passed`.
- `cd term-control-center && npm test` — blocked before execution: this worktree has no local `tsx` dependency (`ERR_MODULE_NOT_FOUND`; all 144 test files fail to load), not the stated six known failures.
- `cd term-control-center && npm run typecheck` and `npm run build` — blocked before compilation: local `tsc` is absent (`sh: tsc: not found`).
- `git diff --check` — passed.

## Commit

- `feat(notifications): add typed activity router`

## Verifier preflight

- `PI_COMS_DIR` identifies this operator-configured pool as `agentops-trio`.
- Lead attested that the pool is isolated to this worktree and contains exactly lead, coder, and verifier; `verifier` is live locally.
- Lead disposition closes `V277-CP1-005`: lead-authored operator-directed documentation commits are authorized branch content but permanently outside CP-1 review scope.
- CP-1 revision 3 was approved by verifier with zero open findings. CP-2 is the active checkpoint.

## Verifier request

- Checkpoint: CP-1 (FR-1/FR-2).
- Revision: 3 approved.
- Requested review: contract fields/taxonomy, unknown-kind rejection, unconditional recording before channel calls, existing-source mapping, legacy activity compatibility, test coverage, and CP-1 scope containment.
- Finding IDs addressed: `V277-CP1-001`, `V277-CP1-002`, `V277-CP1-003`, `V277-CP1-004`, `V277-CP1-005`.

## CP-2 implementation — pending verifier review

- Resumed with the CP-2 worktree changes already present: `src/agentops_harness/activity_user_state.py`, `src/agentops_harness/review_server.py`, and `tests/unit/test_activity_user_state.py`. The verifier-owned `verifier-report.md` was pre-existing dirty content and remains untouched.
- Added atomic, mode-0600 per-user state at `activity-users.json`: `seen_at` cursors and sorted per-kind mutes survive restart under the existing review-server state directory.
- `/activity/summary?user_id=` returns the user-scoped unread needs-human count. Non-human and per-item archived records do not contribute; kind-muted records remain in the feed and preserve the needs-attention badge while contributing zero unread.
- Added token-gated `POST /activity/seen` and `POST /activity/mutes`, guarded by a constant-time comparison of `AGENTOPS_ACTIVITY_API_TOKEN` with `x-activity-token`. Mute requests require a valid taxonomy kind and a JSON boolean. Browser preflight permits the token header.
- Preserved the existing per-item `/activity/archive` and `/activity/unarchive` routes and their state semantics.
- Added endpoint coverage in `tests/unit/test_review_server_activity.py`: token rejection/acceptance, invalid kind and malformed boolean rejection, per-user persistence, seen cursor clearing, muted-but-recorded unread suppression, archive/unarchive preservation, and CORS token preflight.

### Revision 2 — verifier findings addressed

- `V277-CP2-001`: the central router now records unconditionally, then checks the selected user's persisted per-kind mute before delivering to any channel. Regression coverage proves muted events record without delivery and unmuting restores delivery.
- `V277-CP2-002`: unread ordering now parses timezone-aware instants rather than comparing ISO strings; mixed precision, equivalent-zone, and malformed legacy timestamp regressions cover safe behavior.
- `V277-CP2-003`: `update_user_state()` serializes complete load-transform-save transactions for the threaded review server. The synchronized endpoint regression preserves concurrent seen and mute updates for distinct users; its instrumented lock requires both state I/O operations to run inside the serialized transaction.
- `V277-CP2-004`: the HTTP test request helper now accepts four parameters.

### Revision 3 — verifier findings addressed

- `V277-CP2-003`: made the concurrent endpoint test deterministic about the critical transaction: an instrumented lock plus state-I/O wrappers require both load and save to execute while the lock is held; concurrent requests must retain both user updates.
- `V277-CP2-005`: extracted small concurrency and instrumentation helpers so all test functions remain under 20 lines.
- `V277-CP2-006`: updated the durable allowed-path record to include the verifier-requested, canonical FR-6 router repair under the active continuation authorization.

### CP-2 scope

- Allowed paths: `src/agentops_harness/activity_user_state.py`, `src/agentops_harness/notification_router.py`, `src/agentops_harness/review_server.py`, and focused unit tests. The router repair is the verifier-requested, canonical FR-6 delivery enforcement; the active continuation authorization covers this bounded revision.
- Forbidden until CP-3: TS/UI/navigation or badge work, producer unification, Slack deletion/config edits, PR actions, and deployments.
- Stop condition: verifier approval for CP-2 or a true scope/auth/safety conflict. CP-3 remains out of scope for this review.

### CP-2 validation

- Focused revision 2: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests/unit/test_activity_user_state.py tests/unit/test_review_server_activity.py tests/unit/test_notification_router.py -q` — passed (`27 passed`).
- Full Python revision 2: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — expected pre-existing failure only: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`; `1325 passed, 60 subtests passed`.
- `cd term-control-center && npm test` — blocked before execution: local `tsx` is absent; all 144 test files fail to load with `ERR_MODULE_NOT_FOUND`.
- `cd term-control-center && npm run typecheck` and `npm run build` — blocked before compilation: local `tsc` is absent (`sh: 1: tsc: not found`).
- `git diff --check` — passed.

### CP-2 approval

- Verifier approved CP-2 revision 3 at `0f14332` with zero open findings. Addressed findings: `V277-CP2-001` through `V277-CP2-006`.
- The verifier verdict reported `bug_check_status: not_applicable`; no CP-2 bug-check remains pending.
- CP-3 UI/badges, producer unification, and Slack activity-delivery deletion remained untouched at CP-2 close.

## CP-3 active — FR-3/FR-5/FR-9

- Lead authorized CP-3 on 2026-07-23 after confirming local Node dependencies and a clean TypeScript typecheck.
- Allowed paths: Python activity/router/review-server and Slack activity-delivery retirement, registry-backed SPA and vanilla drawer badge code, term notification adapters, focused tests/guardrails, generated nav registry after `npm run nav:emit`, and `qa-receipts/f3/` only.
- Forbidden: new navigation slots, unrelated Slack gateway/PRD/command-center changes, PR actions, deployment, and destructive changes outside the three named Slack activity-delivery modules/config keys.
- CP-3 slices: one-store feed protocol and both drawer renderers; retire the term ad-hoc kind rank through backbone adapters; delete the Slack activity-delivery trio/config keys; then add FR-9 guardrails and browser receipts. Stop after CP-3 verifier approval or a true scope/auth/safety conflict.

## CP-3 implementation — pending verifier review

- Retired the term-only heartbeat attention combiner and its acknowledge/snooze endpoints. Heartbeat attention remains published atomically to `activity-stalls.json`; the Python activity core consumes that persisted seam.
- Replaced the legacy `/completion-notifications` endpoint with token-gated `/completion-updates`. It reads durable `completions.json` records for the existing completion UI only; completion updates no longer combine a second heartbeat notification path.
- Updated board notifier, board callbacks, both nginx proxy configurations, and focused term tests to use the new update projection. Completion actions remain available; the removed heartbeat action path is now represented by the shared Activity surface.
- Tightened the persisted-state guardrail: it proves the legacy combiner files are absent, completion updates read the durable completion store, and heartbeat publication targets `activity-stalls.json`.
- The registry was unchanged, so `npm run nav:emit` was not required; registry byte-parity remains covered by the term suite.

### CP-3 validation

- Focused TypeScript: `cd term-control-center && npm run typecheck` — passed.
- Focused TypeScript tests: completion route/server, activity-state, nginx, review notifier, and board guardrails — passed (`92 passed`).
- Focused Python: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests/unit/test_notification_backbone_guardrails.py tests/unit/test_notification_router.py tests/unit/test_review_server_activity.py -q` — passed (`26 passed`).
- Build: `cd term-control-center && npm run build` — passed.
- Full Python: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — `1312 passed, 60 subtests passed`; sole known pre-existing failure: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`.
- Full Node: `cd term-control-center && npm test` — `1111 passed, 5 pre-existing failures`, none in CP-3 paths: `pi-agent wrapper preserves PI_COMS_MODEL_LABEL`, `fix-loop launch wiring carries selected findings`, Browser-QA pane add, lane outside configured slots assertion, and verification-sandbox protected-run-artifact assertion.
- `git diff --check` — passed.

### Browser QA

- Isolated preview ports: term `3132`, SPA `3133`, board `3134`, CDP `9333`; ports `3032`/`3033` were untouched.
- Shared persisted `completions.json` fixture verified badge-on; empty persisted records verified badge-off. Captured both vanilla board and SPA drawer on dark desktop and light 390px.
- Receipts: `qa-receipts/f3/f3-board-dark-1440-badge-on.png`, `qa-receipts/f3/f3-spa-dark-1440-badge-on.png`, `qa-receipts/f3/f3-board-light-390-badge-off.png`, `qa-receipts/f3/f3-spa-light-390-badge-off.png`.

### CP-3 review boundary

- Review this CP-3 implementation and its focused tests/receipts only. Preserve the verifier-owned `verifier-report.md`; exclude all lead-authored documentation commits under the standing disposition.

### Revision 2 — verifier findings addressed

- `V277-CP3-001`: removed the obsolete sink polling loop and its deleted Slack configuration startup branch; an executable `main()` smoke now proves the review server has no unresolved sink name.
- `V277-CP3-002`: added the same-origin activity-token bootstrap endpoint, cached its token only in the browser runtime, and serialize `markSeen()` before the Activity refresh. Browser smoke against the real token-gated endpoint observed `activity-unread` transition from 1 to 0.
- `V277-CP3-003`: deleted unreachable completion-center inline heartbeat actions, callbacks, renderer, and CSS while preserving the separate board completion action center.
- `V277-CP3-004`: both drawer clients now clear feeds on transport, HTTP, JSON, malformed-summary, zero, and absent-feed outcomes.
- `V277-CP3-005`: corrected the cumulative inventory to include `completion-center.js` and classify the Slack gateway document as the reviewed CP-3 retirement.
- `V277-CP3-006`: extracted token-aware seen transport into the existing activity-actions module; `activity-center.js` is now 293 lines.

### Cumulative CP-3 inventory

- Python/core: `src/agentops_harness/activity_center.py`, `src/agentops_harness/profile_commands.py`, `src/agentops_harness/review_server.py`, `src/agentops_harness/slack_activity_delivery.py` (deleted), `src/agentops_harness/slack_activity_messages.py` (deleted), `src/agentops_harness/slack_activity_sink.py` (deleted), `src/agentops_harness/slack_gateway_health.py`; `tests/unit/test_notification_backbone_guardrails.py`, `tests/unit/test_profile_schema.py`, `tests/unit/test_review_server_activity.py`, `tests/unit/test_review_server_launcher.py`, `tests/unit/test_slack_activity_sink.py` (deleted), `tests/unit/test_slack_activity_sink_guardrails.py` (deleted), `tests/unit/test_slack_gateway_health.py`.
- Term/SPA: `term-control-center/server/activityNotifications.ts` (deleted), `activityStatePublisher.ts`, `completionRoutes.ts`, `heartbeatAttention.ts` (deleted), `heartbeatSweep.ts`, `index.ts`, `serverMonitors.ts`; `term-control-center/shared/completion.ts`; `term-control-center/src/navDrawer.css`, `src/navigation/NavDrawer.tsx`, `src/navigation/activityFeeds.ts`; `term-control-center/tests/activityServer.test.ts`, `activityStatePublisher.test.ts`, `boardGuardrails.test.ts`, `completion-route-action-config.test.ts`, `completion-routes.test.ts`, `completion-server.test.ts`, `heartbeatAttention.test.ts` (deleted), `heartbeatSweep.test.ts`, `nginxProxy.test.ts`, `reviewNotify.test.ts`.
- Board/proxy/receipts: `pipeline-diagram/activity-center.js`, `activity-center-actions.js`, `agentops-shell.js`, `board.html`, `completion-center.js`, `deploy/activity-token.sh`, `deploy/ops.evono.me.nginx`, `deploy/REVIEW-SETUP.md`, `deploy/run-review-server.sh`, `global-nav.js`, `public/board-light.html`, `review-notify.js`; `config/templates/secure-access/nginx-agentops-authentik-forward-auth.template.conf`; all four `qa-receipts/f3/*.png` files.
- Run artifacts: this handoff and every `review-request-r*-cp3.json` revision artifact. `docs/slack-operator-gateway.md` and `profiles/evonome.example.yaml` are reviewed CP-3 Slack activity-delivery documentation/config retirements. Only the standing lead-authored documentation commits listed in the lead disposition are excluded.

### Exact CP-3 commands

- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/activityServer.test.ts tests/activityStatePublisher.test.ts tests/boardGuardrails.test.ts tests/completion-route-action-config.test.ts tests/completion-routes.test.ts tests/completion-server.test.ts tests/navRegistry.test.ts tests/nginxProxy.test.ts tests/reviewNotify.test.ts` — passed (`105 passed`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests/unit/test_notification_backbone_guardrails.py tests/unit/test_notification_router.py tests/unit/test_review_server_activity.py tests/unit/test_profile_schema.py -q` — passed (`39 passed`).
- `cd term-control-center && npm run build` — passed; known Vite chunk-size/non-module script warnings only.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — `1312 passed, 60 subtests`; only `test_unlinked_merged_pr_emits_warning_row` is the known baseline failure.
- `cd term-control-center && npm test` — `1111 passed, 5 known baseline failures`: PI_COMS model label, fix-loop selected findings, Browser-QA pane add, lane configured-slot assertion, and verification-sandbox protected artifact assertion.
- `git diff --check` — passed.

### Revision 6 — final bug-check findings addressed (lead, operator-directed)

Operator instructed the lead to implement the revision-5 follow-ups and run the final bug-check directly instead of a verifier recheck round. Commits: `3b07482` (BUG-005), `f9aebe5` + `344222c` (BUG-001), `6fc68bd` (BUG-002), `be560ff` (BUG-003), this handoff update (BUG-004).

- `V277-CP3-BUG-001`: `heartbeatSweep.test.ts` adds a scheduler regression that injects a deterministic publish failure (state root pointing at a regular file), asserts ≥2 `onError` reports across intervals (scheduler survived and kept sweeping), then repoints the state dir and asserts a later sweep publishes successfully.
- `V277-CP3-BUG-002`: `activityStatePublisher.test.ts` adds an explicit-`stateDir` regression — env `TERM_CONTROL_STATE_DIR` points elsewhere; records land only under the explicit directory and the fallback path stays clean.
- `V277-CP3-BUG-003`: token provisioning extracted unchanged into `pipeline-diagram/deploy/activity-token.sh` (sourced by the launcher; assignment now precedes `export` so a failed read stops strict mode). `tests/unit/test_review_server_launcher.py` proves first-run creation with `0700`/`0600` modes, stable reuse across runs, and external-token precedence without touching state. `REVIEW-SETUP.md` gains the token location/lifecycle/rotation note; token values never printed or committed.
- `V277-CP3-BUG-004`: revision-5 paths (`run-review-server.sh`, `serverMonitors.ts`) and all revision-6 paths added to the cumulative inventory above; this section is the revision record.
- `V277-CP3-BUG-005`: `startServerMonitors` now takes one typed `ServerMonitorOptions` object (was six parameters); sole caller `server/index.ts` updated; no class added.

### Final bug-check (lead, Fable 5 — per operator instruction replacing the verifier recheck)

- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm test` — `1114 passed, 4 failures`, all from the documented baseline list (PI_COMS model-label baseline test passed this run); none in notification, heartbeat, or monitor paths.
- `cd term-control-center && npm run build` — passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — `1317 passed, 60 subtests`; only the known `test_unlinked_merged_pr_emits_warning_row` baseline failure.
- Focused suites: `heartbeatSweep` 9/9 · `activityStatePublisher` 2/2 · `test_review_server_launcher.py` 3/3 · `bash -n` launcher clean.
- KISS on revision-6 surfaces: files ≤ 49 lines added, all touched functions under the 20-line gate (recovery test refactored under it), one comment ("why" class), no dead code.
- `qa-receipts/f3/` all four receipts present. Verdict: all five findings closed with their requested evidence; no new findings. Independence caveat recorded: implementer and final-checker are the same agent for revision 6, by explicit operator instruction.
