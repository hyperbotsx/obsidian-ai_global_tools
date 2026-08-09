# Coder handoff — PRD #58 Unified AgentOps Activity Center and Slack Notification Sink

## Scope source

- Canonical issue: https://github.com/hyperbotsx/agentops-harness/issues/58
- Title: `B2-PRD: Unified AgentOps Activity Center and Slack Notification Sink`
- Branch: `prd/unified-activity-center-slack-notifications-58`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneB`
- Base: `origin/main`

## Pre-edit status

- `git status --short --branch` before edits: clean on `prd/unified-activity-center-slack-notifications-58`.
- Pre-existing dirty files: none.
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/`

## Scope guardrails

### Allowed paths

- `pipeline-diagram/**` for Activity Center UI integration and shared nav wiring
- `term-control-center/shared/**` and `term-control-center/server/**` for completion/session lifecycle and retention updates
- `term-control-center/tests/**` for completion/activity guardrails
- `src/agentops_harness/**` for review-job activity normalization, retention, Slack sink, health, and profile-backed config
- `tests/unit/**` for Python activity/slack/profile coverage
- `profiles/evonome.example.yaml`
- `docs/slack-operator-gateway.md`
- `docs/activity-center.md` if needed
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/**`

### Forbidden paths/actions

- No PR creation, merge, deploy, or approvals.
- No raw transcripts, raw terminal output, raw diffs, secrets, tokens, Slack webhooks, or credentials in repo state, activity records, or Slack payloads.
- Do not rebuild or bypass the existing Slack command-center approval/action path.
- Do not reimplement terminal session recovery/tmux ownership outside the scoped activity/retention adapters.
- Durable review-job execution persistence remains out of scope; only degraded restart surfacing is allowed.

## Validation commands

- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center test`
- `npm --prefix term-control-center run build`
- `PYTHONPATH=src python3 -m pytest tests/unit -q`
- `git diff --check`

## Stop condition

Implement all #58 requirements and acceptance criteria, get verifier approval through the PRD checkpoints plus final bug-check, keep validations green, then pause before any PR action.

## Planned verifier checkpoints

1. Unified activity model as a normalization layer over existing sources.
2. Activity Center UI, grouping, badge count, and next-action copy.
3. Cleanup/retention rules with numeric thresholds and never-prune-evidence guard.
4. Completion/review/session dedupe behavior.
5. Slack sink reuse of gateway policy/health, outbound send safety, fail-closed behavior, dedupe, throttling, and redaction.
6. No duplication/bypass of the existing command-center action path.
7. Cross-surface compatibility with #57 navigation and existing review/completion flows.
8. Tests, docs, and manual-QA evidence.

## Research consult

Required before implementation because the PRD names research-first surfaces.

### Retention / TTL policy

- Completed 2026-06-20 via `researcher`.
- Recommended local-state policy:
  - feed cards: 30 days from creation
  - completion history: 90 days from completion
  - review activity history: 90 days from last review event
  - muted items: until terminal + 30 days, 365-day hard cap, re-confirm at 180 days if still open
- Operational guidance: purge daily plus on app start and workspace/account switch; treat local state as a UX cache, not an audit log; never make it the only historical record.
- Researcher sources: EC GDPR storage limitation guidance, ICO storage limitation guidance, Microsoft Teams activity-feed best practices (2024-11-07), GitHub notification retention change (2026-04-24), GitHub saved notifications docs, Nextcloud activity retention docs, MDN/web.dev storage durability guidance.

### Accessible Activity Center / browser notification patterns

- Completed 2026-06-20 via `researcher`.
- Recommended UI guidance:
  - use a trigger button + accessible drawer/panel/dialog
  - move focus into the drawer only when it opens as an overlay, trap Tab, support Escape, return focus to trigger
  - keep grouped sections filterable; use tabs only for exclusive instant views, otherwise use combinable filters
  - use polite `role="status"` summaries for result-count/new-update announcements; do not make the whole drawer a chatty live region
  - silent polling only; no focus stealing, no auto-scroll, no auto-open; batch arrivals behind a “show new updates” affordance when relevant
  - keep one clear heading/link per card, textual status, timestamp/source, and explicit mute/archive controls
- Researcher sources: WCAG 2.2 status/pause guidance, WAI APG dialog/feed/tabs guidance, WCAG ARIA22/ARIA23/F85 techniques, UK Home Office notification accessibility guidance.

## Coms preflight

- Project/worktree namespace: `agentops-laneB`
- `coms_list` in this pool shows `verifier`, `researcher`, and `steward`.
- Local coder registration file: `/tmp/agentops/coms/agentops-laneB/projects/agentops-laneB/agents/coder.json`
- Outbound review identity assumption: `coder@agentops-laneB`

## Checkpoint 1 — unified activity model as a normalization layer over existing sources

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `src/agentops_harness/activity_center.py`
- `src/agentops_harness/activity_center_models.py`
- `src/agentops_harness/activity_center_completion.py`
- `src/agentops_harness/activity_center_runtime.py`
- `src/agentops_harness/activity_center_sources.py`
- `src/agentops_harness/review_server.py`
- `tests/unit/test_activity_center.py`

### What changed

- Added a new Python activity-summary normalization layer that reads sanitized completion state, persisted terminal groups, live review jobs, optional stall items, and board refresh health into one shared activity-item shape.
- Normalized completion states into `needs_attention`, `running`, `ready`, `done`, and `muted` buckets with dedupe keys based on the existing completion notification family (`project/repository/issue/branch`).
- Normalized review jobs by job kind/PRD/status and terminal sessions by recoverability so stale/unrecoverable sessions surface as attention items while recovering/running sessions remain non-alerting.
- Added optional support for a future stall-item JSON source via `AGENTOPS_ACTIVITY_STALL_JSON` so #65 can emit `possibly_stuck` / `disconnected_or_unknown` items into the same model without changing the Activity Center contract.
- Exposed `GET /activity/summary` from `review_server.py` so later UI work can consume the unified normalized payload.
- Added focused unit coverage for bucket mapping, badge counts, board-error items, optional stall items, and completion dedupe.

### Validation run for this checkpoint

- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/activity_center.py src/agentops_harness/activity_center_models.py src/agentops_harness/activity_center_completion.py src/agentops_harness/activity_center_runtime.py src/agentops_harness/activity_center_sources.py src/agentops_harness/review_server.py` — passed.

### Revision 2 fixes for verifier findings

- `V58-CP1-001`: task-less blocked/error completion items now fall back to `notification.id` and then `groupId` before the generic title fallback, so distinct unresolved completion records stay visible.
- `V58-CP1-002`: top-level summary ordering now keeps bucket priority ascending (`needs_attention` first) while preserving recency ordering inside each bucket.
- Added regressions for both findings in `tests/unit/test_activity_center.py`.

### Revision 2 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/activity_center.py src/agentops_harness/activity_center_models.py src/agentops_harness/activity_center_completion.py src/agentops_harness/activity_center_runtime.py src/agentops_harness/activity_center_sources.py src/agentops_harness/review_server.py` — passed.

### Verifier status for checkpoint 1

- Revision 1: `revision_requested` for `V58-CP1-001` and `V58-CP1-002`.
- Revision 2: `needs_human` with `V58-CP1-001` resolved and `V58-CP1-002` still open.
- Escalated report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`
- Human override: after the escalation, the user explicitly instructed: `please fontinue hbtil full prd is implemented`, so work continued with one more bounded fix attempt on `V58-CP1-002`.

### Revision 3 fix after human override

- `V58-CP1-002`: removed the secondary title-based sort so bucket priority remains ascending while the prior recency sort stays intact within each bucket.
- Added a regression proving two `needs_attention` stall items in the same bucket remain newest-first regardless of title order.

### Revision 3 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/activity_center.py src/agentops_harness/activity_center_models.py src/agentops_harness/activity_center_completion.py src/agentops_harness/activity_center_runtime.py src/agentops_harness/activity_center_sources.py src/agentops_harness/review_server.py` — passed.

### Final verifier result for checkpoint 1

- Revision 3: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 2 — Activity Center UI, grouping, badge count, and next-action copy

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/activity-center.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/board.html`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/wip.html`
- `pipeline-diagram/public/activity-center.js`
- `term-control-center/tests/boardGuardrails.test.ts`

### What changed

- Added a new filterable `Activity Center` panel for Board/Pipeline/WIP that fetches `/api/activity/summary` and renders grouped sections for `Needs attention`, `Running now`, `Ready / next action`, `Done / recent history`, and `Muted / dismissed`.
- Added project/source/severity filters plus search over issue number, title, summary, and next-action copy.
- Wired item clicks back into existing surfaces instead of creating new mutation flows:
  - review items reopen the board review panel
  - completion items reopen the existing term completion action center
  - session items reopen the live term session
  - PR URL items open the existing PR URL in a new tab
- Kept the old `reviews-btn`, `completion-center-btn`, and `term-sessions-btn` elements mounted but hidden so legacy notifier/action hooks stay addressable during migration.
- Bound the unified `needs_attention` count to the nav entry path by adding badges to the desktop `Activity` trigger and the mobile `More` trigger.
- Added session deep-link support on the board (`?session=<groupId>`) plus `window.onOpenLiveSession` so Activity items can reopen live terminal sessions safely.
- Added a guardrail test covering nav integration, `/activity/summary` wiring, live-session deep links, and script load order.

### Validation run for this checkpoint

- `node --check pipeline-diagram/activity-center.js` — passed.
- `node --check pipeline-diagram/global-nav.js` — passed.
- `npm --prefix term-control-center test -- --runInBand boardGuardrails` — passed.

### Revision 2 fixes for verifier findings

- `V58-CP2-001`: isolated the unified Activity badge from the legacy review-job badge selector by switching to a dedicated `.activity-badge` class.
- `V58-CP2-002`: the `Done / recent history` section now renders both `done` and `history` buckets.
- Expanded the guardrail test to assert both fixes.

### Revision 2 validation

- `node --check pipeline-diagram/activity-center.js` — passed.
- `npm --prefix term-control-center test -- --runInBand boardGuardrails` — passed.

### Final verifier result for checkpoint 2

- Revision 2: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 3 — cleanup/retention rules with numeric thresholds and never-prune-evidence guard

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `term-control-center/server/completionRetention.ts`
- `term-control-center/server/completionStore.ts`
- `term-control-center/tests/completion-store.test.ts`
- `src/agentops_harness/activity_center.py`
- `src/agentops_harness/activity_state.py`
- `src/agentops_harness/review_server.py`
- `tests/unit/test_activity_state.py`
- `pipeline-diagram/activity-center.js`
- `pipeline-diagram/activity-center-actions.js`
- `pipeline-diagram/public/activity-center-actions.js`
- `term-control-center/tests/boardGuardrails.test.ts`

### What changed

- Added completion retention thresholds in Term state:
  - `closeout_done` history: keep 90 days, max 200 records
  - muted completion states (`validation_queued`, `dismissed`, `deferred`): keep 30 days, max 200 records
  - synthetic `/tmp/agentops-*` completion artifacts: prune after 24 hours
- Applied completion cleanup both on term-store load/save and when the Activity Center summary reads `completions.json`, so startup and Activity Center open both trigger safe cleanup.
- Added a generic Activity Center state file for review-server-owned local UI state with:
  - archived/muted item snapshots
  - persisted review/degraded history snapshots
  - override retention: 30 days, max 200
  - review history retention: 90 days, max 200
  - degraded board-history retention: 30 days, max 50
- Added `POST /activity/archive` and `POST /activity/unarchive` so ready/error review items and stale session items can be explicitly moved into the muted bucket without touching canonical evidence.
- Wired Activity Center cards to expose human-triggered Archive / Unarchive controls for review items, stale sessions, and degraded board items.
- Added regression coverage for completion pruning, synthetic cleanup, never-prune-evidence, persisted review history, and archive/unarchive round trips.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test -- --runInBand completion-store boardGuardrails` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py tests/unit/test_activity_state.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/activity_center.py src/agentops_harness/activity_state.py src/agentops_harness/review_server.py` — passed.

### Revision 2 fixes for verifier findings

- `V58-CP3-001`: retained review/degraded history now re-enters `/activity/summary` as `history` bucket items whenever no live item supersedes it.
- `V58-CP3-002`: Python cleanup-on-open now fails closed on malformed timestamps instead of raising.
- `V58-CP3-KISS-001`: split activity action/archive logic into `pipeline-diagram/activity-center-actions.js`, returning `pipeline-diagram/activity-center.js` under the file-size cap.
- Expanded Python and guardrail tests to cover retained history visibility, malformed timestamp safety, archive/unarchive wiring, and the new script order.

### Revision 2 validation

- `npm --prefix term-control-center test -- --runInBand boardGuardrails` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py tests/unit/test_activity_state.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/activity_center.py src/agentops_harness/activity_state.py src/agentops_harness/review_server.py` — passed.

### Final verifier result for checkpoint 3

- Revision 2: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 4 — completion/review/session dedupe behavior

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `tests/unit/test_activity_state.py`
- existing completion/activity files from checkpoints 1 and 3 remain the implementation surface under review

### What changed

- Added explicit regression coverage for review-history dedupe by `dedupe_key`, proving the latest retained snapshot wins.
- Added regression coverage that archived session overrides replace live session items instead of producing live+muted duplicates.
- Reused the previously added completion dedupe coverage from checkpoint 1 (`tests/unit/test_activity_center.py` and `term-control-center/tests/completion-store.test.ts`) as the completion side of this checkpoint.

### Validation run for this checkpoint

- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_state.py -q` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_activity_center.py -q` — passed.
- `npm --prefix term-control-center test -- --runInBand completion-store` — passed.

### Final verifier result for checkpoint 4

- Revision 1: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 5 — Slack sink reuse of gateway policy/health, outbound send safety, fail-closed behavior, dedupe, throttling, and redaction

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `src/agentops_harness/slack_activity_sink.py`
- `src/agentops_harness/slack_gateway_health.py`
- `src/agentops_harness/review_server.py`
- `tests/unit/test_slack_activity_sink.py`
- `tests/unit/test_slack_gateway_health.py`

### What changed

- Added a new optional Slack activity sink using Slack Web API `chat.postMessage` (and `conversations.open` for DM user targets) with bot-token auth.
- Reused the existing gateway allowlist/redaction model:
  - sink reads the shared allowed user/channel env lists
  - destination channel ids must be allowlisted
  - destination user ids must be allowlisted before DM open/send
  - outbound message text is sanitized before send
- Added fail-closed sink config via env (disabled by default):
  - `AGENTOPS_SLACK_ACTIVITY_SINK_ENABLED=1`
  - `AGENTOPS_SLACK_ACTIVITY_DEST_CHANNEL_IDS=...`
  - `AGENTOPS_SLACK_ACTIVITY_DEST_USER_IDS=...`
  - `AGENTOPS_SLACK_ACTIVITY_APP_URL=...`
  - `AGENTOPS_SLACK_ACTIVITY_THROTTLE_SECONDS=...`
  - `AGENTOPS_SLACK_ACTIVITY_STATE=...`
- Added per-event dedupe/throttling state with persisted `last_send`, deduped count, dropped count, and degraded reasons.
- Integrated sink dispatch into `review_server.activity_summary()` and a background 30-second loop started only when the sink is enabled.
- Extended `slack_gateway_health.py` to surface sink delivery counters and `last_send` from the persisted sink state file.
- Added unit coverage for fail-closed missing token/config behavior, allowlist-derived config, dedupe/throttle, redaction-before-send, safe button links, and health counter reuse.

### Validation run for this checkpoint

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink.py tests/unit/test_slack_gateway_health.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/slack_activity_sink.py src/agentops_harness/slack_gateway_health.py src/agentops_harness/review_server.py` — passed.

### Revision 2 fixes for verifier findings

- `V58-CP5-001`: serialized sink dispatch per sink-state path with a process-local lock and added a concurrent regression proving only one send occurs.
- `V58-CP5-002`: malformed throttle env now fails closed with a degraded reason instead of raising through `/activity/summary`.
- `V58-CP5-003`: health now reads the sink’s default persisted state path when the explicit sink-state env var is absent.

### Revision 2 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink.py tests/unit/test_slack_gateway_health.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/slack_activity_sink.py src/agentops_harness/slack_gateway_health.py src/agentops_harness/review_server.py` — passed.

### Final verifier result for checkpoint 5

- Revision 2: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 6 — no duplication/bypass of the existing command-center action path

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `tests/unit/test_slack_activity_sink_guardrails.py`

### What changed

- Added a guardrail test proving the sink remains read-only and does not import or call the existing Slack button / command-center action path.
- The guardrail asserts the sink is limited to Slack Web API read-only delivery surfaces (`chat.postMessage` and `conversations.open`) and does not route through PR approvals, completion actions, or other mutating Slack command-center flows.

### Validation run for this checkpoint

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink_guardrails.py -q` — passed.

### Revision 2 fix for verifier finding

- `V58-CP6-001`: strengthened the guardrail from substring checks to an exact allowed-Slack-API-method set assertion (`chat.postMessage` and `conversations.open` only), while also asserting the sink does not import Slack button/command-center modules.

### Revision 2 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink_guardrails.py -q` — passed.

### Final verifier result for checkpoint 6

- Revision 2: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 7 — cross-surface compatibility with #57 navigation and existing review/completion flows

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `pipeline-diagram/agentops-nav.js`
- `term-control-center/src/navigation/navModel.ts`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/admin.test.ts`

### What changed

- Pointed shared Activity cross-links at the stable Activity Center home: `/board.html?activity=1`.
- Reduced Term’s Activity panel links to a single `Activity Center` entry so cross-surface navigation lands on the unified board-side surface instead of the legacy fragmented entry points.
- Updated the static Admin nav Activity link to the same `?activity=1` landing surface.
- Added guardrail coverage for the shared nav query string and Admin link target.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test -- --runInBand boardGuardrails admin` — passed.

### Final verifier result for checkpoint 7

- Revision 1: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Checkpoint 8 — tests, docs, config source, restart degradation, and manual-QA evidence

### Status

Implemented and ready for verifier review.

### Files changed in this checkpoint

- `src/agentops_harness/activity_state.py`
- `src/agentops_harness/review_server.py`
- `src/agentops_harness/slack_activity_sink.py`
- `src/agentops_harness/profile_schema.py`
- `src/agentops_harness/profile_commands.py`
- `profiles/evonome.example.yaml`
- `docs/activity-center.md`
- `docs/slack-operator-gateway.md`
- `tests/unit/test_activity_state.py`
- `tests/unit/test_slack_activity_sink.py`
- `tests/unit/test_slack_gateway_health.py`
- `tests/unit/test_profile_schema.py`
- `tests/unit/test_slack_activity_sink_guardrails.py`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/admin.test.ts`

### What changed

- Added review-server restart degradation support for lost in-memory review jobs by persisting volatile running/rate-limited review snapshots and surfacing a degraded `needs_attention` item after restart until the job is relaunched or archived.
- Added profile-aware Slack sink config resolution while preserving env overrides, including profile-backed `activity_sink` settings and `bot_token_env` as an allowed reference key.
- Rewrote `profiles/evonome.example.yaml` to the current schema and documented `slack.activity_sink` settings.
- Added `docs/activity-center.md` with entry points, source model, retention thresholds, archive behavior, restart degradation behavior, and manual-QA checklist.
- Updated `docs/slack-operator-gateway.md` with Activity sink delivery, env/profile config, and sink safety rules.
- Expanded tests for default sink-state health lookup, profile-backed sink config, restart degradation behavior, and profile-schema acceptance of `bot_token_env`.

### Manual-QA evidence recorded

- Activity Center entry points: Board `/board.html?activity=1`, Term nav `Activity Center`, Admin nav `Activity`.
- Retention expectations documented in `docs/activity-center.md` and backed by completion-store/activity-state tests.
- Restart degradation expectation documented in `docs/activity-center.md` and backed by `test_restart_lost_review_jobs_surface_as_degraded_attention_items`.
- Slack sink health/state expectations documented in `docs/slack-operator-gateway.md` and backed by sink/health tests.

### Validation run for this checkpoint

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test -- --runInBand boardGuardrails admin` — passed.
- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink.py tests/unit/test_slack_gateway_health.py tests/unit/test_slack_activity_sink_guardrails.py tests/unit/test_activity_state.py tests/unit/test_activity_center.py tests/unit/test_profile_schema.py -q` — passed.
- `PYTHONPATH=src python3 - <<'PY' ... validate_profile_document(parse_profile_yaml('profiles/evonome.example.yaml')) ... PY` — passed.
- `python3 -m py_compile src/agentops_harness/slack_activity_sink.py src/agentops_harness/slack_gateway_health.py src/agentops_harness/review_server.py src/agentops_harness/activity_state.py src/agentops_harness/activity_center.py src/agentops_harness/profile_schema.py src/agentops_harness/profile_commands.py` — passed.

### Revision 2 fix for verifier finding

- `V58-CP8-001`: made profile-backed sink destinations robust to inline/empty list literals, removed the broken `destination_user_ids: []` example syntax, updated docs to use block-list/omit semantics only, and added a regression that loads the real `profiles/evonome.example.yaml` through `config_from_profile(...)`.

### Revision 2 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink.py tests/unit/test_slack_gateway_health.py tests/unit/test_profile_schema.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/slack_activity_sink.py src/agentops_harness/profile_schema.py src/agentops_harness/profile_commands.py src/agentops_harness/review_server.py` — passed.

### Final verifier result for checkpoint 8

- Revision 2: `approved`
- Open findings: `0`
- Report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`

## Steward hygiene review

- Steward review result: `clean`
- Summary: file placement, docs, example config, public symlinks, and run-artifact structure all match repo patterns; no cleanup required before final verifier bug-check.

## Final validation before bug-check

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (263 tests).
- `npm --prefix term-control-center run build` — passed.
- Removed `term-control-center/dist/` after the build rerun.
- `PYTHONPATH=src python3 -m pytest tests/unit -q` — passed (753 tests, 42 subtests).
- `git diff --check` — passed.
- `git ls-files --others --exclude-standard` — only the scoped issue-58 run artifacts plus new tracked implementation files listed in this handoff.

## Final bug-check revision 2 fix

- `V58-FINAL-001`: expanded Slack sink resolved-update eligibility so `review` items in the `ready` bucket emit the required `CEO review ready` message, and added a regression proving exactly one sanitized outbound message is sent for a ready review item.

### Final bug-check revision 2 validation

- `PYTHONPATH=src python3 -m pytest tests/unit/test_slack_activity_sink.py -q` — passed.
- `python3 -m py_compile src/agentops_harness/slack_activity_sink.py` — passed.

## Final verifier result

- Final bug-check revision 2: `approved`
- Bug-check status: `passed`
- Open findings: `0`
- Final report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-58-unified-activity-center-slack-notifications/verifier-report.md`
- Status: ready to prepare PR, but paused per instruction before any PR action.
- No PR created. No merge. No deploy.
