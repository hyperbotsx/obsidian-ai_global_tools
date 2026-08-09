# Steward response — checkpoint 4

Decision: `cleanup_recommended`

## Placement and boundaries

- Orchestrator state, inventory, tail, injection, delegation, persistence, locking, and route composition are correctly placed under `term-control-center/server/orchestrator/`.
- Narrow application adapters remain under `term-control-center/server/`; focused TypeScript tests remain under `term-control-center/tests/`.
- Python Kody state/agent changes are under `src/agentops_harness/`, with coverage under `tests/unit/`.
- Checkpoint and review evidence is appropriately contained in the Issue #211 `dev-plans/.../runs/` folder.
- No repo-local skills/standards, deployment configuration, or unrelated product surface was introduced.

## KISS and generated-output review

- New orchestrator modules are semantic and bounded; the largest are `proposalStore.ts` (257 lines), `paneInjection.ts` (198), and `proposalLedger.ts` (149).
- `server/index.ts` grew only by narrow registration/recovery wiring (1,212 -> 1,238 lines); no orchestration state machine was absorbed there.
- `adminProjects.ts` remains under the 300-line project limit (299); `paneInjection.test.ts` is also 299.
- `git diff --check` passes. No prohibited generated/runtime path is tracked or included in the untracked changed-file set.

## Cleanup required before final bug-check

Validation left ignored generated/cache output in the worktree:

- `pipeline-diagram/board-data.js`
- `pipeline-diagram/completed-data.js`
- `pipeline-diagram/completed-registry.json`
- `pipeline-diagram/matrix-data.js`
- `pipeline-diagram/pipeline-data.js`
- `pipeline-diagram/pipeline.mmd`
- `pipeline-diagram/wip-data.js`
- `pipeline-diagram/projects/`
- `.pytest_cache/`, `pipeline-diagram/__pycache__/`, `src/agentops_harness/__pycache__/`, and `tests/unit/__pycache__/`

These are ignored, but include generated project/runtime data and should be removed before final verifier bug-check. `term-control-center/node_modules/` is an ignored validation dependency and may be retained for reruns, but must not be staged.

Stop condition: clean the listed generated/cache paths, confirm `git status --short --ignored` contains no stale runtime output, then request verifier recheck before final bug-check.
