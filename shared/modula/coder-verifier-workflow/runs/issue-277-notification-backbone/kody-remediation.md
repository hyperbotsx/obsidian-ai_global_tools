# Kodus remediation — PR #278

## Scope

Addressed active Kodus findings from the 2026-07-23 review:

- `r3639525922`: retain pre-attachment badge bindings; prune nodes only after they were connected and later detached.
- `r3639526241`: persist the first degraded-review snapshot and timestamp across activity-summary calls and review-server restarts until a live review replaces it.
- `r3639526617`: treat only a missing heartbeat timestamp file as empty history; propagate read and JSON errors.

## Changed files

- `pipeline-diagram/activity-center.js`
- `src/agentops_harness/activity_state.py`
- `term-control-center/server/activityStatePublisher.ts`
- `tests/unit/test_activity_state.py`
- `term-control-center/tests/activityCenter.test.ts`
- `term-control-center/tests/activityStatePublisher.test.ts`

## Validation

- Focused Python: `13 passed`.
- Focused TypeScript: `44 passed`.
- Typecheck and build: passed.
- Full Python: `1317 passed, 60 subtests passed`; one known baseline failure in `test_unlinked_merged_pr_emits_warning_row`.
- Full Node: `1115 passed, 5 known baseline failures`; none in changed paths.
- `git diff --check`: passed.

## Revision 2 — verifier findings addressed

- `V278-KODY-001`: live review records now replace only matching degraded records; a persisted two-review regression proves an unrelated degraded review remains visible with its original timestamp.
- `V278-KODY-002`: added an executable VM lifecycle regression for pre-attachment retention and post-attachment detachment pruning.
- `V278-KODY-003`: added a deterministic `EISDIR` regression alongside corrupt-JSON coverage; only `ENOENT` remains the empty-history path.

### Revision 2 validation

- Focused Python: `14 passed`.
- Focused TypeScript/nav: `42 passed`.
- `cd term-control-center && npm run typecheck`: passed.
- `cd term-control-center && npm run build`: passed.
- Full Python: `1318 passed, 60 subtests passed`; the known baseline `test_unlinked_merged_pr_emits_warning_row` failed.
- Full Node: `1117 passed, 5 known baseline failures`; none are in changed paths.
- `git diff --check`: passed.

## Revision 3 — verifier finding addressed

- `V278-KODY-001`: on a new server epoch, prior volatile reviews are converted to stable degraded snapshots before current live reviews are merged. The first new-epoch summary can therefore replace a matching review while retaining every unmatched lost review.
- The two-review regression now covers that first-summary ordering, persistence/reload, retained sibling visibility, and its stable degradation timestamp.

### Revision 3 validation

- Focused Python: `14 passed`.
- Focused TypeScript/nav: `42 passed`.
- `cd term-control-center && npm run typecheck`: passed.
- `git diff --check`: passed.

## Revision 4 — final verifier finding addressed

- `V278-KODY-001`: volatile state now identifies every current review before retaining degraded records. A current ready/error review clears its matching stale/degraded snapshot; only active review records and unmatched degraded records remain volatile.
- The state-machine regression covers prior running A/B, new-epoch running A plus degraded B, ready A with B retained, persistence/reload, and the next restart surfacing only B with its preserved timestamp.

## Approval

- Verifier approved revision 4 with `bug_check_status: clean` and zero open findings.

## Kodus round 3 — lead-authorized remediation

Lead accepted `r3639809169`, `r3639809468`, `r3639809770`, and `r3639810111` under active continuation authorization. The prior dismissal of the activity-user identity finding is superseded: activity user identity now derives only from the trusted `X-Authentik-Username` request header, with `DEFAULT_USER_ID` as the loopback fallback. Request body `user_id` and the Activity summary query parameter are ignored.

- Badge registrations now receive a mount-frame connection check, removing entries that never attach while retaining later-detachment pruning.
- Review activity timestamps now use the immutable job `created`/`updated` epochs.
- Notification routing loads a user's muted kinds once per publish batch.
- Activity writes and summary reads use the forwarded identity; body-controlled state keys cannot grow the user store.

### Kodus round 3 validation

- Focused Python: `44 passed`.
- Focused TypeScript/nav: `43 passed`.
- `cd term-control-center && npm run typecheck` and `npm run build`: passed.
- Full Python: `1320 passed, 60 subtests passed`; the known `test_unlinked_merged_pr_emits_warning_row` baseline failure remains.
- Full Node: `1118 passed, 5 known baseline failures`; none are in changed paths.
- `git diff --check`: passed.

### Kodus round 3 revision 2

- `V278-KODY-R3-001`: the header-derived summary user now flows into `build_activity_summary()` and its one-load router batch; the supplied user's mute snapshot governs delivery.
- `V278-KODY-R3-002`: removed a redundant blank line so `activity-center.js` remains below the 300-line KISS gate.
- Focused Python: `45 passed`; focused TypeScript/nav: `43 passed`; typecheck and diff check passed.

### Kodus round 3 revision 3

- `V278-KODY-R3-003`: restored `build_activity_summary()` to 10 lines and four formal parameters by reusing its keyword-options seam for `user_id` and extracting a three-parameter source collector. The forwarded identity still reaches the one-load delivery batch.
- Focused Python: `45 passed`; AST measurement: builder 10 lines/4 parameters, source collector 11 lines/3 parameters; board file remains 299 lines.
- Verifier approved revision 3 with `bug_check_status: clean` and zero open findings.
