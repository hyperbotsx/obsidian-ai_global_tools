# Review — Native-Claude Launcher Settings/Hook Validation Failure (PRD #243)

- **Scope:** review-only analysis of the native-Claude launcher test failure. No files edited.
- **Date:** 2026-07-18
- **Files reviewed (current working-tree state):**
  - `scripts/agentops/claude-native.sh`
  - `term-control-center/server/nativeClaudeSettings.ts`
  - `term-control-center/tests/nativeClaudeLauncher.test.ts`

## Problem statement

The wrapper correctly requires exactly one owner-only generated settings file and a single exact `PreToolUse` command hook. The valid test fixture still fails with:

> "settings must own exactly the compiled PreToolUse hook with no allow rules and no bypass mode"

The settings hook command is intended to invoke Node plus:
`<worktree>/term-control-center/build/server/pretoolHook.js`

All of the following must be preserved: owner-only regular settings/hook files; no symlinks or writable parent; no allow rules; default permission mode; exactly one `PreToolUse` matcher `*`; exactly one command hook; no caller-controlled settings/source flags; no shell execution, extra arguments, comments, substitutions, or alternate executable.

Goal: the safest exact command-validation strategy that is robust to Node-executable symlink/path normalization between a TypeScript test runner and the spawned Bash wrapper.

---

## 1. Root-cause hypotheses

The rejection comes from the hook-command check in `claude-native.sh:117`:

```js
parts.length !== 2 || fs.realpathSync(parts[0]) !== fs.realpathSync(process.execPath) || parts[1] !== hook
```

Note the asymmetry: `parts[0]` (the Node executable) is compared with **`realpathSync` on both sides**, but `parts[1]` (the hook path) is compared with **raw string equality** against `hook` (= `$EXPECTED_HOOK` = `$worktree_root/term-control-center/build/server/pretoolHook.js`, where `worktree_root="$(git rev-parse --show-toplevel)"`).

- **H1 — primary: raw-string path comparison is not normalization-safe.** The two sides derive the hook path from different sources:
  - Test side (`settingsFor`, test line 50): `parts[1]` is built from `path.join(root, …)` where `root` comes from `mkdtemp(os.tmpdir()…)` — **not canonicalized**.
  - Wrapper side: `hook` is derived from `git rev-parse --show-toplevel`, and the fake `git` prints `$PWD` (test line 37). Bash initializes `PWD` from `getcwd()`, which **is canonicalized** (symlinks resolved).

  When the temp path contains any symlinked component — macOS `os.tmpdir()` is `/var/…` → `/private/var/…`; a symlinked `TMPDIR`; a bind-mounted state dir — the two strings differ character-for-character while pointing at the same file, and `parts[1] !== hook` is true → reject. The Node-exe check survives the same divergence only because it already uses `realpathSync`. This exactly matches the symptom "robust to symlink/path normalization between a TypeScript test runner and the spawned Bash wrapper."

- **H2 — same flaw, earlier trigger: the coms-MCP check (`claude-native.sh:90`) has the identical raw-string bug** (`server.args[0] !== expected`, and `server.command !== process.execPath` with no realpath). On a symlinked-temp host `assertDirectLaunch` would fail *first* with the "local compiled coms-mcp" message. Whichever the operator sees, the underlying defect is one class: raw-string path/exe equality.

- **H3 — secondary robustness gap: `command.split(" ")`.** The command is validated by splitting on a single space and requiring exactly two tokens. This is fragile (any space in the worktree/control-plane path → `parts.length !== 2`) and semantically wrong: a Claude `type:"command"` hook is executed **through a shell**, so token-splitting neither reflects how the string runs nor blocks shell metacharacters. It is not what fails the valid fixture, but it is the wrong primitive to build the security check on.

- **H4 — production, not just test:** in production `setupNativeAutonomy` builds the hook path from `path.resolve(input.worktree)` (`nativeClaudeSettings.ts:20,22`) while the wrapper independently recomputes it from `git rev-parse`. If `input.worktree` is ever a symlinked/bind-mounted path (this repo lives under `/mnt/hyperliquid-data/…`), the same raw-string mismatch rejects a legitimate launch. This is a real defect, not a test artifact.

---

## 2. Minimal secure validation algorithm

Keep every invariant; replace string-equality and space-splitting with metacharacter-rejection + file-identity comparison. In the wrapper's `node -e` validator:

1. **File/mode/owner checks (unchanged, already correct):** settings and hook are owner-uid regular files, non-symlink, `mode & 0o077 === 0` (settings) / `mode & 0o022 === 0` (hook), and the hook's parent dir is owner-only, non-symlink, `mode & 0o022 === 0`. Extend the same owner-only, non-symlink, non-group/other-writable check to the settings file's **parent directory** (currently only the hook dir is checked).
2. **Structural checks (unchanged):** `permissions.allow` is an empty array; `permissions.defaultMode === 'default'`; the only key under `hooks` is `PreToolUse`; `PreToolUse` has exactly one entry; `matcher === '*'`; that entry's `hooks` array has exactly one element with `type === 'command'`.
3. **Command safety — reject before parsing:** reject the command string if it contains any shell metacharacter or control character: any of `` ; | & $ ` ( ) < > { } [ ] * ? ! # ' " \ `` , or whitespace other than the single separating run, or a newline/CR. This kills comments, substitutions, redirection, chaining, globbing, and quoting in one step.
4. **Tokenize safely:** trim, then split on `/\s+/`; require exactly two tokens. (After step 3 the only permitted whitespace is the separator, so two tokens ⇒ `node hook` and nothing else — no extra args.)
5. **Compare by file identity, not string:** accept only if `realpathSync(token0)` equals `realpathSync(process.execPath)` **and** `realpathSync(token1)` equals `realpathSync(expected_hook)` (equivalently, compare `statSync(...).dev`+`.ino` inode identity). This is the normalization-safe fix: both sides resolve symlinks, so `/var` vs `/private/var`, bind mounts, and `git rev-parse` vs `path.resolve(worktree)` all collapse to the same real inode.
6. **Generation-side guard (`nativeClaudeSettings.ts`):** in `assertHookPath`, additionally reject a resolved node execPath or hook path that contains whitespace or any of the step-3 metacharacters, and `realpathSync` the worktree before building `hookPath`. This makes generation fail closed on a hostile/space-containing path instead of emitting a command the validator must special-case, and guarantees the generated string always tokenizes to two parts.
7. **Apply the same realpath/inode fix to the coms-MCP check (H2)** so both trusted-path comparisons are normalization-safe and consistent.

This preserves: owner-only regular files, no symlink/writable parent, no allow rules, default mode, exactly one `*` matcher, exactly one command hook, no caller settings/source flags (already handled at `claude-native.sh:71-74`), and no shell/args/comments/substitution/alternate exe.

---

## 3. Exact test-fixture strategy

Make the fixture honest about canonicalization and identity so it exercises the real contract rather than an accidental string match:

- **Canonicalize the temp root once:** `const root = await fs.realpath(await mkdtemp(path.join(os.tmpdir(), 'agentops-native-claude-')))`. Every derived path (mcp server, hook, settings, `cwd`) then equals what Bash's `getcwd()`-derived `$PWD` / `git rev-parse` produces, so the fixture passes on macOS/symlinked-`TMPDIR`/bind-mount hosts too. This single change also fixes the H2 coms-MCP path.
- **Derive the hook path in settings from the same canonical root** already used to lay down the file (test lines 33, 50), so the settings command references the exact on-disk hook inode.
- **Keep the Node token as a real, resolvable executable** but rely on identity, not string: `process.execPath` (or the existing `execFileSync('node', ['-p','process.execPath'])`) is fine because validation realpaths both sides. Do **not** hardcode a `node` string.
- **Assert the positive path explicitly:** add a `assertValidSettingsPasses(fixture)` that runs with a good token and asserts `status === 0` and stdout contains `--settings\n<settings>` — so a regression in the validator is caught directly, not only via the negative cases.
- Leave the fake `git` emitting `$PWD`; with a realpath'd root it now agrees with the fixture-constructed paths by construction.

---

## 4. Negative tests to add

Each builds a settings file that differs in exactly one dimension and asserts `status === 5` with the settings-rejection message (or the specific message where noted):

- **Comment:** command `"<node> <hook> # rm -rf"` → metacharacter (`#`) reject.
- **Extra args:** `"<node> --inspect-brk <hook>"` and `"<node> <hook> --foo"` → token-count reject.
- **Alternate executable:** `"/usr/bin/env <hook>"` and a second real node binary path → `realpath(token0) !== realpath(execPath)` reject.
- **Command substitution:** `"<node> $(echo <hook>)"` and backtick form → metacharacter reject.
- **Shell chaining/redirect/pipe:** `"<node> <hook>; curl x"`, `"… && …"`, `"… | sh"`, `"… > /tmp/x"` → metacharacter reject.
- **Symlinked settings file:** replace `settings.json` with a symlink to a valid file → `isSymbolicLink` reject.
- **Symlinked hook file and symlinked hook parent dir:** → reject (and, once step 5 lands, a `token1` that symlinks to the real hook should still resolve — add one case proving realpath equivalence *is* accepted, to lock in intended behavior).
- **Loose modes:** settings `0o640` (group-readable) → reject; hook `0o664` (group-writable) → reject; hook parent dir `0o775` → reject; **settings parent dir `0o777`/`0o770`** → reject (covers the added parent-dir check).
- **Extra hooks:** two entries in `PreToolUse`; two elements in the inner `hooks`; a second matcher; a non-`PreToolUse` key (e.g. `PostToolUse`) present → each rejects.
- **Bypass / non-default mode:** `defaultMode: "bypassPermissions"` and `defaultMode: "acceptEdits"` → mode reject. (Distinct from the existing CLI-flag bypass tests, which stay.)
- **Allow rules present:** keep the existing `['Bash(rm:*)']` case; add a non-empty `deny` or stray `additionalDirectories` case if you choose to tighten step 2 to reject unknown permissive keys.

---

## 5. Verdict — REVISE

The structure of the check is right and most of it (owner-only files, non-symlink, mode masks, no-allow, default-mode, single `*` matcher, single command hook, caller-flag rejection) is correct and should stay. Two defects block it and one must be hardened:

- Fix the **raw-string hook path comparison** (and the twin coms-MCP comparison) to **realpath/inode identity** — this is what fails the valid fixture and would also reject legitimate symlinked-worktree launches in production (H1/H2/H4).
- Replace **`split(" ")` + string equality** with **metacharacter-rejection then two-token identity comparison**, and add the **generation-side whitespace/metacharacter guard** (H3, step 6).
- Make the **fixture realpath its temp root** and add an explicit positive-pass assertion (§3).

With the §2 algorithm and §3 fixture change, re-review is not required for these specific corrections provided the §4 negative tests plus a positive-pass test all run green; the security invariants are unchanged and only the comparison primitive and path-normalization handling move from fragile to robust.

---

## Appendix — line references

- `claude-native.sh:14` — `worktree_root="$(git rev-parse --show-toplevel)"` (canonicalized via getcwd in the fixture's fake git).
- `claude-native.sh:71-74` — caller-supplied `--settings`/`--setting-sources` rejection (correct; keep).
- `claude-native.sh:90` — coms-MCP raw-string comparison (H2 — apply the same realpath fix).
- `claude-native.sh:100-121` — settings/hook validator; line 117 is the failing hook check.
- `nativeClaudeSettings.ts:20,22` — `path.resolve(input.worktree)` + `path.join(worktree, HOOK_RELATIVE)` (H4 source-of-truth divergence).
- `nativeClaudeSettings.ts:43` — generated command `` `${fs.realpathSync(process.execPath)} ${hookPath}` `` (add whitespace/metachar guard on `hookPath`).
- `nativeClaudeSettings.ts:48-50` — `assertHookPath` (extend per §2 step 6).
- `nativeClaudeLauncher.test.ts:33,50` — fixture hook path + settings command construction (realpath the root per §3).
- `nativeClaudeLauncher.test.ts:37` — fake `git` prints `$PWD`.
