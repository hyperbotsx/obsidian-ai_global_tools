# Fixes Applied — Umask-Inherited Hook Modes (PRD #243)

- **Date:** 2026-07-18
- **Applied by:** external diagnostic session (coder on PRD #242 worktree), at the operator's direction, directly in this worktree (`agentops-prd-243`).
- **Companion diagnosis:** `review-umask-hook-mode-diagnosis.md` (same folder).
- **Status:** uncommitted working-tree changes, left for the #243 coder to review, absorb into the branch, and commit. **No validator predicate in `claude-native.sh` was modified.**

## Why

The nominal launcher-test fixture exited 5 because this host's umask is `0002`: the fixture's `writeFile`/`mkdir` produced a group-writable hook (0664) in group-writable parents (0775), which the validator's `mode & 0o022` checks correctly reject. The deployed `build/server/pretoolHook.js` had the same modes, so real launches would fail identically. The boundary is right; the artifacts were wrong.

## Changed files (4)

### 1. `term-control-center/server/nativeClaudeSettings.ts`

Added `normalizeHookArtifact(hookPath, ownerUid)`, called from `setupNativeAutonomy()` right after `ownerUid` is computed:

- If the hook does not exist → **return silently**. This is deliberate: launch plans can be built before `build:server` has run in the worktree (the launch-plan tests do exactly this), and the wrapper remains the fail-closed boundary at launch time. Do not "fix" this into a hard requirement.
- If the hook or its parent is a symlink, not a regular file/dir, or not owned by the current uid → **throw** (`untrusted PreToolUse hook artifact/directory`).
- Otherwise `chmodSync` parent to `0o755` and hook to `0o644`.

### 2. `term-control-center/package.json`

`build:server` now hardens its own output so fresh builds comply regardless of host umask:

```
"build:server": "tsc -p tsconfig.server.json && chmod 755 build/server && chmod 644 build/server/*.js"
```

`build/server` is flat (no subdirectories), so the glob covers everything. This also puts `comsMcp.js` at 644, which the wrapper doesn't mode-check today but plausibly will.

### 3. `term-control-center/tests/nativeClaudeLauncher.test.ts`

- `nativeFixture()`: after creating the hook, added umask-immune chmods —
  `await chmod(path.dirname(hook), 0o755); await chmod(hook, 0o644)`
  This is the one-line root-cause fix that turns the nominal fixture green.
- Added `assertGroupWritableHookFailure(fixture)` to the "enforces AgentOps-owned settings" test. It pins the previously-accidental behavior as intended: hook at `0o664` → exit 5; hook parent at `0o775` → exit 5 (both matching `/no allow rules and no bypass mode/`); modes restored between mutations; final run asserts status 0 to prove the mutation was the sole cause.

### 4. `term-control-center/tests/nativeClaudeLaunchPlan.test.ts`

- Imports extended to `chmod, mkdir, mkdtemp, readFile, stat, writeFile`.
- New test **"native Claude plan normalizes umask-loosened hook artifact modes"**: creates the hook at 664/775 inside the fixture worktree, commits it (`buildCoderVerifierLaunchPlan` asserts a clean worktree — an uncommitted hook file fails with "Worktree has uncommitted changes"), builds the plan, then asserts the hook ends at `0o644` and its dir at `0o755`. This exercises the real `launchPlan.ts → autonomyPaneEnv → setupNativeAutonomy` path.

## Verification run (this worktree, 2026-07-18)

- `tests/nativeClaudeLauncher.test.ts` + `tests/nativeClaudeLaunchPlan.test.ts` + `tests/autonomyHook.test.ts`: **23/23 pass**.
- `npm run typecheck`: clean (both tsconfigs).
- `npm run build:server`: succeeded; on-disk `build/server` now 755, `pretoolHook.js` and `comsMcp.js` now 644 (previously 664/775).
- `tests/launchPlan.test.ts` + `tests/launcher.test.ts`: 56/58 — the 2 failures are **pre-existing on base commit `2e80015`** (verified by running the identical tests in a pristine detached-HEAD checkout, since removed): model-label assertions expecting `'Claude Opus 4.8'` but getting `'Claude Opus (delegated)'` in "Claude provider launch delegates through claude_agent…" and "Frontend Expert delegates Claude into a visible autoclosing tmux pane". Unrelated to this fix; not addressed.

## Invariants — nothing weakened

Owner-uid + mode masks (settings `0o077`, hook `0o022`), parent-dir checks, `lstat` symlink rejection, schema checks (empty `allow`, default mode, single `*` PreToolUse matcher, single command hook), metacharacter/quote rejection, two-token limit, realpath identity for executable and hook, caller `--settings`/`--setting-sources` rejection, and bypass-mode rejections are all untouched. The changes only make fixtures and real artifacts comply with the existing boundary — and tighten the deployed state by removing group-write from the hook.

## Notes for the #243 coder

- These are working-tree edits sitting alongside your in-flight changes; review and fold them into your branch/commits as you see fit.
- Keep the "missing hook → skip" behavior in `normalizeHookArtifact`; making it throw breaks the launch-plan tests and the plan-before-build flow.
- Optional follow-up (additive tightening, not required): extend the wrapper's `ownerDir` check up the parent chain (`build`, worktree root are still 775 on this host); see the residual-risk note in the companion diagnosis.
