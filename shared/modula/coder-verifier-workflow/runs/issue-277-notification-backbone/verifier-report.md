# Verifier Report — Issue #277 Notification Backbone

## Review metadata

- Decision: `revision_requested`
- Checkpoint: CP-3 final bug-check
- Revision: 5
- Revision reviewed: `2eb40e952db4be2fcdf8819707a659c01ed7e907`
- Revision-5 baseline: `eaf88769e38b7b597d171a3fff4d9f61b7c5b53b`
- Cumulative CP-3 baseline: `0f14332affe9f1ddee979b74444c9b5053664f60`
- Branch/worktree: `prd/notification-backbone-277` at `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-277`
- Source of truth: approved GitHub issue #277 and its CP-3/final bug-check requirements
- Continuation authorization: active; bounded implementation/test/KISS/audit fixes may continue, but no PR, merge, deploy, approval, GitHub mutation, trading, or backtest is authorized
- Review boundary: bounded recheck of `V277-CP3-BUG-001` through `V277-CP3-BUG-003`, their requested regressions, revision-5 audit scope, and explicit KISS gates

## Recheck summary

All three runtime mechanisms are repaired:

- heartbeat publication failures no longer reject the fire-and-forget scheduler, and later sweeps continue with production console observability;
- normalized `config.stateDir` now reaches the publisher;
- the canonical review-server launcher creates/reuses a private activity token.

The recheck is not yet approvable because revision 5 adds no regression tests for the three reproduced bugs despite each finding's explicit test request. The existing nine heartbeat tests are unchanged success-path tests. The durable cumulative handoff also omits the two new revision-5 product paths.

## Finding status

### V277-CP3-BUG-001 — Runtime fixed; failure/recovery regression still missing

- Status: open, bounded test completion required
- Runtime verification:
  - `startHeartbeatSweep()` catches sweep rejection before scheduling the next timer.
  - Production supplies `onError: error => console.error(...)`.
  - Independent invalid-state-dir probe survived, observed seven bounded error callbacks across later intervals, and exited 0.
- Missing requested evidence: no test injects a publisher/write failure and proves that the scheduler remains alive, invokes observability, and performs a later successful sweep.
- Existing coverage: `heartbeatSweep.test.ts` and `activityStatePublisher.test.ts` remain unchanged and cover success paths only.
- Requested bounded action: add the failure-then-recovery scheduler regression requested in the original finding. Prefer deterministic dependency/error injection over spawning a crashing process.
- Decision impact: the high-severity crash fix has no automated regression lock.

### V277-CP3-BUG-002 — Runtime fixed; explicit-state-dir regression still missing

- Status: open, bounded test completion required
- Runtime verification:
  - `config.stateDir` now flows through `startServerMonitors()` and `SweepOptions` to `publishHeartbeatActivity()`.
  - Independent isolated-HOME probe wrote `activity-stalls.json` only under the supplied custom state directory.
- Missing requested evidence: no test creates a term server/publisher with explicit `stateDir` while the environment is absent/different and asserts option precedence plus absence from the fallback path.
- Existing publisher test still sets `TERM_CONTROL_STATE_DIR` and calls `publishHeartbeatActivity()` without the new explicit argument, so it cannot catch the original split-brain bug.
- Requested bounded action: add the explicit-option precedence/isolation regression requested in the original finding.
- Decision impact: the high-severity wrong-state-root fix has no automated regression lock.

### V277-CP3-BUG-003 — Runtime fixed; launcher token lifecycle regression/documentation still missing

- Status: open, bounded test/documentation completion required
- Runtime verification:
  - `run-review-server.sh` now creates the review-server state directory with mode `0700`, creates/reuses `activity-api-token` with mode `0600`, and exports it unless an external token is already configured.
  - Generation failures stop the launcher under `set -euo pipefail` rather than starting with an empty token.
- Missing requested evidence:
  - no isolated launcher test proves first-run creation, reuse across restart, permissions, and external-token precedence;
  - the deployment runbook does not document the token file/lifecycle or recovery/rotation behavior requested by the original finding.
- Requested bounded action: add an isolated startup-wrapper regression and a concise deployment note for token location, permissions, stable reuse, external override, and safe rotation. Do not expose or commit token contents.
- Decision impact: the default-deployment fix is not durably verified or operator-documented.

### V277-CP3-BUG-004 — Revision-5 paths are absent from the cumulative handoff

- Status: open, blocking audit-artifact finding
- Evidence:
  - Revision 5 changes `pipeline-diagram/deploy/run-review-server.sh` and `term-control-center/server/serverMonitors.ts`.
  - Neither path appears in the handoff's cumulative CP-3 inventory.
  - The handoff also has no revision-5 finding/validation section recording the new behavior, unchanged-test limitation, or exact recheck command.
- Requested bounded action: add both paths to their existing inventory categories and append a concise revision-5 bug-fix/validation record. Any new test/runbook paths added for the three open findings must also be covered by the cumulative inventory.
- Decision impact: the durable audit record no longer matches the cumulative delivered checkpoint.

### V277-CP3-BUG-005 — State propagation raises the monitor entry point to six parameters

- Status: open, blocking KISS finding
- Evidence: `startServerMonitors(groups, sessions, completions, stateDir, store, projects)` in `term-control-center/server/serverMonitors.ts:10` now takes six parameters; revision 5 added `stateDir` to an already oversized five-parameter integration signature.
- Requested bounded action: group the optional monitor configuration/dependencies into one small typed context/options object so the entry point returns within the 3–4 parameter gate. Do not add a speculative class or inheritance layer.
- Decision impact: the runtime fix works, but the revision violates the repository's explicit parameter-count gate.

## Silent/edge recheck

| Risk | Result |
| --- | --- |
| Publisher error crashes process | Runtime resolved; missing automated failure/recovery coverage. |
| Publisher writes wrong state root | Runtime resolved; missing option-precedence/isolation coverage. |
| Default launcher has no activity token | Runtime resolved; missing launcher regression and lifecycle documentation. |
| Error observability falsely reports success | Pass: production logs an explicit publication failure and the direct `sweep()` API still rejects to callers. |
| Persistent filesystem failure stops later scheduling | Pass in independent probe; scheduler continued across repeated failures. |
| Missing token provisioning starts server anyway | Pass by inspection: shell strict mode stops on provisioning/read/chmod failure. |

## Explicit KISS review

- File size: pass (`heartbeatSweep.ts` 263 lines; publisher 30; monitor 31; launcher 31).
- Function size: pass; revised functions remain below 20 lines.
- Nesting: pass.
- Parameter count: fail; revision 5 expands `startServerMonitors` to six parameters (`V277-CP3-BUG-005`).
- Comments: no redundant comments were added.
- Dead code: none found in revision 5.

## Validation evidence

- Independent `cd term-control-center && npm run typecheck` — pass.
- Independent unchanged heartbeat publisher/sweep suite — `9 passed`.
- Independent failure-containment probe — survived repeated publication errors, later schedules ran, exit 0.
- Independent explicit-state-dir probe — activity file appeared only under the configured custom state directory.
- Independent revision/worktree `git diff --check` — pass.
- Inventory comparison — the two new revision-5 product paths are absent from the durable cumulative list.
- No researcher consult was needed; remaining items are deterministic regression, audit, and KISS checks.

## Prior status

- CP-1 and CP-2 remain approved.
- CP-3 revision 4 checkpoint review remains approved.
- Final bug-check findings `V277-CP3-BUG-001` through `V277-CP3-BUG-003` have correct runtime fixes in revision 5 but remain open until their requested regressions/documentation land. `V277-CP3-BUG-004` records the new audit mismatch, and `V277-CP3-BUG-005` records the revision-5 KISS regression.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "CP-3 final bug-check",
  "revision_reviewed": 5,
  "revision_sha": "2eb40e952db4be2fcdf8819707a659c01ed7e907",
  "open_findings": 5,
  "finding_ids": [
    "V277-CP3-BUG-001",
    "V277-CP3-BUG-002",
    "V277-CP3-BUG-003",
    "V277-CP3-BUG-004",
    "V277-CP3-BUG-005"
  ],
  "bug_check_status": "findings",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-277-notification-backbone/verifier-report.md"
}
```
