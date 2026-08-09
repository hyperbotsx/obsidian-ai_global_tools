# Lane B Conflict Note — Issue #98 Launch Metadata Auto-fix

## Original stop

Final verifier bug-check found `A98-FINAL-001`: issue #98 includes **One-click launch metadata auto-fix**.

Implementing that item appeared to require overlap with Lane B / forbidden surfaces while Lane B #99 was still active:

- `term-control-center/server/adminRoutes.ts` / active Project field read/write routes
- `term-control-center/server/adminClient.ts` / GitHub Project field mutation client
- `pipeline-diagram/*` / PRD board launch failure UI and launch-data refresh
- potentially launch-context extraction/board regeneration surfaces

Per operator instruction, Lane A stopped before editing those surfaces.

## Resolution after Lane B #99 merge

After PR #124 / issue #99 merged to `origin/main`, Lane A fast-forwarded this branch to latest main and resumed #98.

Final #98 launch metadata implementation:

- touches `pipeline-diagram/board.html` for the required **Auto-fix launch metadata** button;
- adds `term-control-center/server/launchMetadataFix.ts` and a guarded term route in `term-control-center/server/index.ts`;
- reuses Lane B's queued pipeline refresh via `queuePipelineRefresh` without modifying `adminPipeline.ts`;
- does not edit `adminRoutes.ts`, `adminClient.ts`, or `adminPipeline.ts`.

No merge conflicts remained after syncing with latest `origin/main`.
