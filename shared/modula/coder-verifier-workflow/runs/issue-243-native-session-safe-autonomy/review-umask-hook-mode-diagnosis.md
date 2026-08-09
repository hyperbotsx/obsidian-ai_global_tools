# Review — Native-Claude Settings Validator: Nominal Fixture Exit-5 Diagnosis (PRD #243)

- **Scope:** read-only diagnostic of the residual settings-validation failure after the realpath/metacharacter corrections landed. Follow-up to `review-native-claude-settings-validation.md`.
- **Date:** 2026-07-18
- **Verdict:** **REVISE** — fixture and artifact provisioning, not the validator. The validator is correct and must stay exactly as written.
- **Files reviewed (working-tree state):**
  - `scripts/agentops/claude-native.sh`
  - `term-control-center/server/nativeClaudeSettings.ts`
  - `term-control-center/tests/nativeClaudeLauncher.test.ts`

## Context

The prior review (H1–H4) identified raw-string path comparison as the primary defect. Those corrections were applied: realpath-based executable/hook identity comparison, canonicalized fixture root, shell-metacharacter rejection, and two-token limit. The nominal valid fixture still exited 5 with the generic rejection at `claude-native.sh:121`:

> "settings must own exactly the compiled PreToolUse hook with no allow rules and no bypass mode"

Negative settings tests passed. No control may be weakened.

## 1. Exact failing predicates

Every predicate of the validator (`claude-native.sh:101-119`) was replayed against a byte-for-byte reconstruction of the nominal fixture on the target host:

| Predicate | Observed | Result |
|---|---|---|
| `ownerOnlyFile(settings, 0o077)` | settings mode 600 (explicit `mode: 0o600` + `chmod`) | pass |
| `ownerDir(dirname(settings))` | mkdtemp root, mode 700 | pass |
| **`ownerOnlyFile(hook, 0o022)`** | **hook mode 664 — group-writable** | **FAIL** |
| **`ownerDir(dirname(hook))`** | **`build/server` dir mode 775 — group-writable** | **FAIL** |
| Metacharacter/quote/newline rejection on command | no match | pass |
| `trim().split(/\s+/)` two-token limit | 2 tokens | pass |
| `realpath(parts[0]) === realpath(process.execPath)` | equal | pass |
| `realpath(parts[1]) === realpath(hook)` | equal | pass |

Root cause: **the host umask is `0002`** (verified: `umask` → `0002`). In `nativeFixture()` (`nativeClaudeLauncher.test.ts`), `writeFile(hook, '')` inherits the umask and produces mode **0664**, and `mkdir(..., { recursive: true })` produces **0775** parents. The validator's `mode & 0o022 === 0` checks then correctly reject the hook file and its parent at `claude-native.sh:107`, the embedded node script exits 1, and the wrapper maps that to exit 5 with the generic message. Only the settings file received mode discipline in the fixture; the hook artifact received none.

This explains the observed test pattern exactly: the nominal fixture fails (it should pass but its artifacts violate the boundary), while negative tests pass (they expect exit 5 and get it — though some for the wrong underlying reason until the fixture is fixed).

The prior review's H1 (raw-string comparison) is genuinely fixed; the realpath'd fixture root agrees with the fake `git`'s `$PWD`. The mode predicates were the *next* gate in line, previously shadowed by H1.

## 2. Production implication (verified, not hypothetical)

The deployed artifact in the worktree had the same defect: `term-control-center/build/server/pretoolHook.js` was **664** in a **775** directory (verified via `stat` before the fix). `tsc` emits build output with umask-inherited modes, so on any umask-`0002` host a real launch would exit 5 identically. The validator is **right** to reject this — a group-writable PreToolUse hook that runs on every tool call is a genuine tamper vector. The correction must make the artifact comply, never relax the check.

## 3. Required correction (validator untouched)

1. **Fixture:** after creating the hook, `chmod` (umask-immune) the hook to `0o644` and its parent to `0o755`.
2. **Provisioning:** normalize the built artifact's modes before launch — at build time (`build:server` post-step) and at settings-generation time (`setupNativeAutonomy`), failing closed on symlink or foreign-owner artifacts, and never requiring the hook to exist at plan time (plans may precede `build:server`; the wrapper remains the fail-closed boundary).

## 4. Tests required

Positive:
- Nominal fixture passes (status 0) with compliant modes — hook `0o644` also pins that the hook mask is `0o022` (group-*read* allowed), not `0o077`.

Negative (one-dimension mutations, expect status 5 + the settings-rejection message):
- Hook file `0o664` → reject (pins today's failure as intended behavior, not a umask accident).
- Hook parent dir `0o775` → reject.
- Restore modes afterward and assert status 0 again, proving the mutation was the sole cause.

## 5. Invariants confirmed preserved

No validator predicate changes, so every control survives verbatim: owner-uid + mode masks (settings `0o077`, hook `0o022`), parent-directory owner/non-writable checks, `lstat`-based symlink rejection, schema checks (empty `allow`, `defaultMode === "default"`, only `PreToolUse`, exactly one `*` matcher, exactly one `command` hook), metacharacter/quote/newline rejection, two-token limit, realpath identity of executable and hook, caller `--settings`/`--setting-sources` rejection, and bypass-mode CLI rejections.

## 6. Residual risk (out of scope, noted for later)

The validator checks only the hook's *immediate* parent. Grandparents (`build`, `term-control-center`, the worktree root) remain 775 on this host, which in principle permits a directory swap by another group member. Exposure is nil here (group = owner's primary group), but extending `ownerDir` up the chain would be an additive tightening if wanted.
