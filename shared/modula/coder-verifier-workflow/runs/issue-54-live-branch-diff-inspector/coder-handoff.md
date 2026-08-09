# Coder Handoff — Issue #54 Live Branch Diff Inspector

## Scope

Allowed paths:

- `term-control-center/`
- `pipeline-diagram/` (completion action center and hosted `/term/groups/:id/diff` proxy integration)
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-54-live-branch-diff-inspector/`

Forbidden paths/actions:

- No PR creation, commits, merges, deployments, approvals, staging, or git mutation from the diff inspector.
- No network git operations (`fetch`/`pull`).
- No raw diff/file-content persistence.
- No sensitive path content exposure.

Pre-existing dirty files before editing: none (`git status --short --branch` was clean on `prd/live-branch-diff-inspector-54`).

## PRD / Issue

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/54
- Branch: `prd/live-branch-diff-inspector-54`
- Current checkpoint: Final bug-check — approved

## Research Summary

Researcher consult completed 2026-06-20. Recommendation: keep a lightweight custom renderer; do not add `@git-diff-view/react` because measured gzip size is ~330 KB. `@codemirror/merge` is ~87 KB gzip but unnecessary editor machinery for this read-only inspector. Git approach should use local refs only, argv-spawned `git`, `--no-optional-locks`, `--no-ext-diff`, `--no-textconv`, `--no-color`, `--numstat -z`, stable status output, and rename detection. Implemented server helpers follow that direction with no new runtime dependency.

## Changed Files

- `term-control-center/shared/blockedPaths.ts`: shared blocked path policy extracted from Prepare PR.
- `term-control-center/shared/diff.ts`: shared diff response/data types.
- `term-control-center/server/diffConfig.ts`: env-overridable diff limits.
- `term-control-center/server/diffFailure.ts`: safe diff error mapping.
- `term-control-center/server/diffPaths.ts`: root-contained path normalization.
- `term-control-center/server/diffParsers.ts`: Git status/numstat/patch parsers.
- `term-control-center/server/gitDiffReader.ts`: read-only local Git diff model and patch selection.
- `term-control-center/server/diffState.ts`: group authorization wrapper for diff reads.
- `term-control-center/server/index.ts`: token-guarded `GET /groups/:id/diff` route.
- `term-control-center/server/preparePr.ts`: now reuses shared blocked path policy.
- `term-control-center/src/DiffInspector.tsx`: read-only docked diff inspector UI, polling/backoff, file rail, side-by-side/unified rendering, and defined states.
- `term-control-center/src/diffPolling.ts`: recurring polling/backoff/visibility pause helper extracted for regression coverage.
- `term-control-center/src/App.tsx`: Diff toggle, docked `allotment` pane integration, launch group resolution hooks.
- `term-control-center/src/styles.css`: terminal-matched diff inspector chrome, file rail, split/unified patch rendering, and responsive styles.
- `term-control-center/tests/termBasePath.test.ts`: static UI integration coverage for diff dock, polling, states, responsive mode, and token API path.
- `term-control-center/tests/diffPolling.test.ts`: recurring polling, hidden-tab pause/resume, and error-backoff regression coverage.
- `term-control-center/tests/diffState.test.ts`: parser, route guard, path safety, blocked path, limit, metadata-overflow, summary-only, union coverage, local main fallback, rename, delete, and binary coverage.
- `pipeline-diagram/board.html`: Review diff completion/action-center affordance before Prepare PR; term iframe payload now includes group id/mode and `focus: 'diff'` opens the inspector.
- `pipeline-diagram/deploy/ops.evono.me.nginx`: token-guarded hosted proxy for `/term/groups/:id/diff` without duplicate Basic Auth prompts.
- `term-control-center/tests/boardGuardrails.test.ts`: static coverage for Review diff before Prepare PR and group id/mode payload.
- `term-control-center/tests/nginxProxy.test.ts`: static coverage for hosted diff API proxy auth policy.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-54-live-branch-diff-inspector/coder-handoff.md`: this handoff.

## Implementation Notes

- Endpoint: `GET /groups/:id/diff?path=<relative-path>`.
- Unknown group returns `unknown_group`; inactive/non-implementation groups return `inactive_group`.
- Worktree and branch are re-verified with `rev-parse --show-toplevel` and `branch --show-current` before diff reads.
- Base comparison uses local `origin/main`, falling back to local `main`, then `merge-base <base> HEAD`.
- Working-tree coverage includes staged, unstaged, and untracked files.
- Per-path precedence: working-tree status wins; paths that also have committed changes are reported as `source: combined` and selected patches are rendered from merge-base to working tree.
- Sensitive paths are surfaced as redacted entries (`blocked: true`, `note: content withheld`) with no hunks.
- Binary and over-limit selected files return metadata only.
- Git commands use `execFile` argv and include `--no-optional-locks`; no `fetch`/`pull` commands are used.
- Checkpoint 2 adds regression coverage for local `main` fallback, committed renames, working deletes, untracked binary files, staged/unstaged/untracked union, and combined precedence for a path in both committed and working changes.
- Checkpoint 3 adds an in-cockpit `Diff` toggle, an `allotment`-docked inspector pane, live polling with error backoff and visibility pause, manual refresh, file rail keyboard navigation, side-by-side patch rows, responsive unified mode, and visible loading/empty/error/blocked/binary/too-large/no-active-session/missing-worktree/git-lock states.
- Checkpoint 4 adds `Review diff` before Prepare PR in the completion action center. It only reopens/focuses the read-only term diff inspector and does not mutate completion state, git state, or action gates.
- Checkpoint 5 visual notes: diff chrome uses `--ao-*` tokens, Berkeley Mono via existing font variables, square corners via `--ao-radius`, diff additions/deletions via `color-mix()` from `--ao-success`/`--ao-danger`, and compact toolbar/file rail density matching `TerminalPane`.

## Env Vars Documented So Far

- `TERM_CONTROL_DIFF_MAX_FILES` (default `300`)
- `TERM_CONTROL_DIFF_MAX_TOTAL_PATCH_BYTES` (default `2097152`)
- `TERM_CONTROL_DIFF_MAX_FILE_PATCH_BYTES` (default `262144`)
- `TERM_CONTROL_DIFF_POLL_INTERVAL_MS` (default `4000`)
- `TERM_CONTROL_GIT_PATH` (existing-style override for Git binary; default `git`)

## Findings Addressed

- `V54-CP1-001`: `files[]` now stays summary-only; selected hunks are only under `selectedFile`. Regression added.
- `V54-CP1-002`: metadata command max-buffer overflow now fails closed as `git_error`; selected patch overflow can still degrade to metadata-only `tooLarge`. Regression added with an injected runner.
- `V54-CP1-003`: new diff reader helper signatures were refactored behind small context objects to stay within the KISS parameter limit.
- `V54-CP3-001`: `DiffInspector` state/loading/polling logic was split into a small model hook and helpers; polling delay, scheduling, visibility binding, and visibility refresh are separated.
- `V54-FBC-001`: polling is now recurring via `startDiffPolling`; regression tests prove two consecutive visible refreshes and hidden-tab pause/resume.

## Validation

- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffPolling.test.ts tests/termBasePath.test.ts tests/diffState.test.ts` — passed (31/31).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/boardGuardrails.test.ts tests/nginxProxy.test.ts tests/termBasePath.test.ts tests/diffState.test.ts` — passed (56/56 before final bug-check fix).
- `npm --prefix term-control-center run build` — passed with existing Vite non-module/chunk-size warnings.
- `npm --prefix term-control-center test` — passed (254/254).
- Steward cleanup: removed ignored generated `term-control-center/build/`, `term-control-center/dist/`, and `pipeline-diagram/__pycache__/` after validation.

## Bundle / Dependency Notes

- No new runtime diff-rendering dependency was added; renderer is custom React/CSS.
- Latest build client JS gzip measurement: Vite reports `152.02 kB` for `dist/assets/index-BmGeLqPo.js` (ignored build artifact removed after validation).
- Runtime diff-rendering dependency delta: `+0 KB gzip`.

## Next Checkpoints

1. Server API safety — approved by verifier revision 2.
2. Git coverage — approved by verifier revision 3.
3. UI/UX — approved by verifier revision 5.
4. Prepare PR integration — approved by verifier revision 6.
5. Visual QA checklist — approved by verifier revision 7.
6. Final bug-check — approved by verifier revision 9 (`bug_check_status: passed`).
