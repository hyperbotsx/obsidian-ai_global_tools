# Security Design Review — PRD #243 Local Verification Sandbox

- **Scope:** read-only security design review of the proposed project-scoped local verification sandbox for AgentOps Harness PRD #243.
- **Canonical PRD:** https://github.com/hyperbotsx/agentops-harness/issues/243
- **Reviewer role:** security reviewer (review-only; no code edited, no PR/merge/deploy/GitHub mutation, no secret access).
- **Date:** 2026-07-18
- **Host verified:** Ubuntu 24.04.3 LTS, kernel 6.8.0-90 (live checks run on this machine).

---

## Decision: REVISE

The operator decision — a project-scoped local sandbox as the *only* future autonomous path for build/test, with direct Bash/npm/node/network/Docker/credential/control-plane denied — is the correct resolution of the open Critical finding V243-C2-002, and Bubblewrap is the right mechanism for this host. But the design is not yet activatable:

1. It must be built on top of the still-open checkpoint-2 control-plane findings (V243-C2-001/005/006/007).
2. The current `autonomyGates.ts` still auto-allows unsandboxed `npm`/`node`/`git` verification commands, which directly contradicts the operator decision and must be removed before any sandbox lands.

Findings and exact constraints are below. The sandbox claims were live-verified on this host rather than relying on documentation alone.

---

## Host facts (verified 2026-07-18 on this machine)

- Ubuntu 24.04.3 LTS, kernel 6.8.0-90. **`bwrap` 0.9.0 installed** at `/usr/bin/bwrap`; `systemd-run` (systemd 255) and `unshare` present. **`firejail`, `docker`, `podman`, `nsjail` are NOT installed.**
- Unprivileged user namespaces work: `bwrap --unshare-all` runs as uid 1000 with `pid1=bwrap`; `kernel.apparmor_restrict_unprivileged_userns` reads `0` (unrestricted) on this box.
- **Network isolation confirmed:** under `--unshare-all` with no `--share-net`, an in-sandbox Node `connect(443, 1.1.1.1)` returns `ENETUNREACH`. No loopback bridge, no DNS path.
- **Minimal profile works:** with `--clearenv`, `HOME=/tmp`, no `/home`/`/root` bind, node 22 and git 2.43 available, worktree writable, `~/.ssh` and `~/.config/gh` not present in the namespace.
- **Git-worktree dependency (important boundary fact):** the worktree `.git` is a pointer to `/mnt/hyperliquid-data/projects/repos/agentops-harness/.git/worktrees/agentops-prd-243`. `git status` inside the sandbox only succeeds if the **common gitdir** (`…/repos/agentops-harness/.git`) is bound. Read-only bind is sufficient for status/diff/log. This means the sandbox boundary is not the worktree alone.

---

## 1. Smallest safe mechanism: Bubblewrap (`bwrap`)

Recommended over the alternatives for this host:

- **Docker/Podman — reject.** Neither is installed; adding a container runtime + daemon/rootless plumbing is a large new dependency and, for Docker, a root daemon and socket that themselves become an escape surface. Contradicts "installed, stable, minimal-dependency."
- **firejail — reject.** Not installed; it is setuid-root (larger trusted surface with a history of privilege-escalation CVEs). Bubblewrap is explicitly designed as a smaller unprivileged alternative.
- **systemd sandboxing (`systemd-run --user` with `PrivateNetwork`, `ProtectHome`, etc.) — viable fallback but not first choice.** It properties-map well but ties each verification run to a transient unit and the user-manager lifecycle; harder to make per-command ephemeral and to bind a precise filesystem view than bwrap.
- **Bubblewrap — select.** Already installed (0.9.0), unprivileged (relies on user namespaces, no setuid on modern kernels), single static binary, purpose-built to construct a minimal bind-mount + namespace sandbox and exit. It is the sandbox Flatpak uses in production. Live-verified above to deliver filesystem, network, PID, IPC, and user isolation on this exact host.

Sources: Bubblewrap project README and man page, `github.com/containers/bubblewrap` (matches installed 0.9.0), verified against the live binary 2026-07-18. Ubuntu 24.04 unprivileged-userns AppArmor restriction background: Ubuntu 24.04 release notes / `kernel.apparmor_restrict_unprivileged_userns` (observed value `0` here).

**Constraint:** the design must detect the userns/AppArmor state at launch, because a hardened host that sets `apparmor_restrict_unprivileged_userns=1` will break bwrap unless an AppArmor profile is installed; that must fail closed (deny verification), not fall back to unsandboxed exec.

---

## 2. Exact sandbox boundary

| Aspect | Required setting |
|---|---|
| Worktree mount | `--bind <worktree> <worktree>` read-write (build/test must write `node_modules/.cache`, test output). This is the only rw bind on real data. |
| `.git` | Common gitdir `…/repos/agentops-harness/.git` bound **read-only**; worktree-private gitdir (`…/.git/worktrees/agentops-prd-<n>`) read-only if commands tolerate it, else a `tmpfs`-backed copy of just `index`/`HEAD`. Never rw-bind the common gitdir — it holds `config` (→ `core.hooksPath`, aliases) and `hooks/`, an execution vector. |
| AgentOps runtime/control-plane | **Not mounted at all.** Policy, settings, audit, hook executable, and the compiled `term-control-center/build/**` import graph must be outside every sandbox bind (see V243-C2-001). The sandbox runs *approved verification commands*; it never needs to see its own enforcement plane. |
| Artifact/handoff writes | **Not writable from inside the sandbox.** Handoff/artifact writes are `workspace_edit`/`artifact` tool calls gated by the hook on the host side, not sandboxed subprocess writes. Sandbox stdout is captured to a bounded buffer by the launcher, not written to the artifact root by the child. |
| Network | `--unshare-net` with **no** `--share-net` (verified `ENETUNREACH`). No bridge, no slirp. |
| DNS | None. Do not bind `/etc/resolv.conf`; with no net-namespace bridge it is moot, but omit it to avoid leaking resolver config. |
| Unix sockets | None bound. No `SSH_AUTH_SOCK`, no `/run/user/<uid>/**`, no X11/Wayland, no coms sockets. Verification commands have no reason to reach any socket. |
| Docker/container sockets | Never bound. `/var/run/docker.sock` absent (Docker not installed); assert its absence and refuse to bind any `docker.sock`/`containerd.sock` if one appears. |
| `/proc`, `/sys`, devices | `--proc /proc` (namespaced), **no `/sys`**, `--dev /dev` (minimal `--dev` gives null/zero/random/tty only, not host devices). Confirmed pid1=bwrap, so `/proc` shows only in-namespace PIDs. |
| Temp dirs | `--tmpfs /tmp` and set `TMPDIR=/tmp`; size-cap via the resource limits below. No host temp bind. |
| Environment | `--clearenv`, then inject only: `PATH` (node+git bin dirs), `HOME=/tmp`, `CI=1`, `NODE_ENV=test`, and worktree path. **No inherited `process.env`.** This is the fix vector for V243-C2-003 — do the stripping by constructing the child env explicitly, not by unsetting a denylist. |
| Credentials / SSH / GitHub / cloud / package tokens | None present in the namespace. No `~/.ssh`, `~/.config/gh`, `~/.npmrc`, `~/.aws`, `~/.config/gcloud`, no `*_TOKEN`/`*_KEY` env. |
| User/group identity | Run as the same unprivileged uid (1000), `--unshare-user` maps it; do **not** map to root inside (avoids `--cap-add`-style expectations). No new privileges: bwrap sets `PR_SET_NO_NEW_PRIVS` by default. |
| CPU / mem / procs / disk / timeout / output | Wrap the bwrap invocation in a resource-limited launcher: wall-clock timeout (default 300 s, the observed coder command budget), `RLIMIT_NPROC` (e.g. 512), `RLIMIT_AS`/cgroup memory cap (e.g. 2–4 GiB), `RLIMIT_FSIZE` and tmpfs size cap (e.g. 1 GiB), and a captured-output byte cap (e.g. 1 MiB, then kill + `deny_output_limit`). Enforce timeout by killing the whole process group/namespace (bwrap `--die-with-parent` + a `SIGKILL` on the launcher's timeout). |

---

## 3. Initial allowed build/test commands (finite, anchored)

Route only these through the sandbox; everything else denied. Anchored, post-metacharacter-rejection, arguments must resolve inside the worktree:

- `npm --prefix <worktree> run typecheck`
- `npm --prefix <worktree> run build:server`
- `npm --prefix <worktree> run build`
- `npm --prefix <worktree> run lint`
- `npm --prefix <worktree> test` and `npm --prefix <worktree> run test`
- `npx tsc -p <worktree-path> --noEmit` / `tsc --noEmit`
- `node --import tsx --test <worktree-test-paths>`
- `npx eslint <worktree-paths>` / `npx vitest run <worktree-paths>` (only if the repo uses them; otherwise omit)
- Read-only git (also runnable un-sandboxed since they only read the ro gitdir): `git status`, `git diff`, `git log`, `git show`, `git rev-parse`, `git branch --show-current`, `git merge-base`, `git ls-files`, `git describe`, `git shortlog`
- Trivial: `pwd`, `true`, `node -v`, `npm -v`, `git --version`, `tsc --version`

**Must stay denied (never sandboxed-auto-allowed):** `npm install`/`ci`/`add`/`publish`/`exec`/`dlx` (network + lifecycle scripts), any `pip`/`cargo`/`go`/`gem`/`brew`/`apt`, `git push`/`fetch`/`pull`/`remote`/`commit`/`config`/`checkout`/`reset`/`clean`/`worktree`/`apply`, all `gh`, `curl`/`wget`/`nc`/`ssh`/`scp`/`rsync`, `docker`/`podman`/`kubectl`/cloud CLIs, `rm`/`mv`/`chmod`/`ln`/`dd`, `sudo`/`su`, and any command with shell metacharacters or env-assignment prefixes.

The current `autonomyGates.ts:80` already gates package-manager `install|add|publish|...` as `scope_expansion` — good — but `autonomyGates.ts:84-89` auto-allows `npm run`/`npm test`/`node --import tsx --test` **without any sandbox**. Under the operator decision that is now a defect (see F1).

---

## 4. May the sandbox run package scripts / `node --test` against agent-modified code?

**Yes — but only inside the sandbox, and only with the containment proof below.**

Running agent-written JavaScript is the entire risk (V243-C2-002: a malicious `package.json` `test` script or test file is arbitrary code with user authority). The sandbox neutralizes the *impact* that the PreToolUse hook cannot — because the hook gates the top-level tool call, not subprocesses (confirmed by the checkpoint-2 researcher note and the Anthropic hooks docs: PreToolUse fires per tool call, not per subprocess). Required containment proof before this may be enabled:

1. In-sandbox network egress is impossible (verified `ENETUNREACH`; test T-net below must pass from *inside a package script*, not just a shell).
2. No credential/secret/socket is present in the namespace (env constructed allowlist-only; T-secret below).
3. No write reaches the control-plane, the common gitdir, or outside the worktree (T-escape, T-git).
4. Subprocess spawning stays within the namespace and the `RLIMIT_NPROC`/timeout/output caps (T-fork, T-resource).
5. The sandbox cannot be induced to run a *different* command than the classified one (the classified argv is passed as exec args, never via `sh -c`; T-meta).

If any of those cannot be proven for a given command, that command stays human-gated. Absent the sandbox, `npm`/`node`/build/test **must remain human-gated** — which is exactly the operator decision, and the code must be brought into line with it.

---

## 5. Hook → sandbox invocation without direct Bash/npm/node bypass

- The PreToolUse hook classifies the `Bash` command. If it matches the §3 allowlist, the hook does **not** allow the raw command. It returns `allow` only for a canonical, re-serialized argv, and the **only executor** is an AgentOps-owned `run-verification` launcher that itself constructs the `bwrap` invocation. The agent never receives permission to run `npm`/`node`/`git` directly against the host.
- Cleanest implementation: expose verification as a dedicated **MCP tool** (e.g. `mcp__autonomy__run_verification` with a typed `{command_id, args}` enum), so the agent cannot express an arbitrary string at all — the classifier maps an enum to a fixed argv. If verification stays on the `Bash` tool, the hook must reject anything that is not a byte-exact match to a generated allowlist entry and hand the matched entry (not the agent's string) to the launcher.
- The launcher must ignore `process.env` for the child (§2) and must be on the protected control-plane root (§6), not in the worktree, so agent edits cannot alter how the sandbox is built. This is the structural fix for "unsandboxed npm/node bypass": there is no code path from an agent tool call to an unsandboxed interpreter.

---

## 6. Keeping launcher / policy / hook / import graph / settings / audit / credentials outside autonomous write authority

This is the still-open **V243-C2-001 (Critical)** and it is a precondition, not a new item:

- Move the policy, generated settings, audit log, the compiled hook, and its entire import graph (`build/server/pretoolHook.js` + `autonomyGates/autonomyPaths/autonomyPolicy/autonomyAudit`) into an **owner-only control-plane root outside every artifact/worktree bind** — today they live under `<artifactRoot>/autonomy` (`launchPlan.ts`) which `autonomyPaths.ts` treats as writable. The sandbox §2 already excludes them from binds; the *host-side* path classifier must also deny `workspace_edit`/`local_read` against that root.
- The hook currently imports from the **writable worktree** compiled output (`nativeClaudeSettings.ts` executes `<worktree>/term-control-center/build/server/pretoolHook.js`). An agent `workspace_edit` to `term-control-center/server/*.ts` plus an allowed build would rewrite the enforcement code. The hook binary and its imports must be **snapshotted to the control-plane root** at launch and executed from there; the worktree copy must never be the enforcement path. Add an integrity check (compare to a launch-time hash) and fail closed on mismatch.
- Wrapper hardening already partly present in the working tree: `claude-native.sh` now rejects caller `--settings`/`--setting-sources` and injects `--setting-sources ''` — good. But **V243-C2-007** remains: it accepts any hook command that merely `includes(expected_hook)`, so `true # <hook>` passes. Require exact schema/matcher/quoted-command validation and owner-only regular-file checks on the settings file and hook.
- Credentials: **V243-C2-003** — `claude-native.sh` unsets only a fixed denylist while the PTY inherits full `process.env`. Switch the native launch to an allowlist-constructed environment (subscription-preflight material only, dropped after preflight). The sandbox child env is already allowlist-only per §2.

---

## 7. Fail-closed behavior

| Condition | Required behavior |
|---|---|
| Sandbox binary missing / `bwrap` not executable | Deny verification (`deny_sandbox_unavailable`); never fall back to unsandboxed exec. |
| Unprivileged userns unavailable (`apparmor_restrict_unprivileged_userns=1`, no profile) | Deny at launch preflight; verification class disabled for the session. |
| Sandbox startup failure (bind error, namespace error) | Deny that command; do not retry outside the sandbox. |
| Command timeout | Kill process group + namespace, deny (`deny_timeout`), audit. |
| Output-limit breach | Kill, deny (`deny_output_limit`), audit; discard captured output beyond the cap. |
| Policy revoked / missing / malformed | Deny (already: `deny_policy_revoked/missing/malformed`); revocation must survive relaunch (V243-C2-006). |
| Audit-write failure | Deny the action (already implemented: `pretoolHook.ts:14-16` → `deny_audit_write_failed`). Keep it. |

Add the four sandbox reason codes (`deny_sandbox_unavailable`, `deny_sandbox_start`, `deny_timeout`, `deny_output_limit`) to the enumerated `REASON_CODES` list.

---

## 8. Sanitized audit fields and bounded retention

The current `autonomyAudit.ts` shape is correct and already compliant: `ts`, `action_class`, `decision`, `reason`, `policy_version`, `session`, `worktree`, `owner_uid` — **no prompts, tool arguments, command strings, outputs, transcripts, tokens, or secrets.**

For sandbox events add only enumerated fields: `command_id` (the allowlist entry id, *not* the raw command), `exit_class` (`ok`/`timeout`/`output_limit`/`nonzero`), and `duration_bucket`. Do **not** log argv, stdout, or stderr.

Retention: 256 KiB rotation with one retained `.1` file is bounded and adequate for v1 (`AUDIT_ROTATION_BYTES` already set); keep the rotation marker record. No unsanitized field may be added — enforce via the `sanitize()` allowlist, which currently reconstructs the record field-by-field (keep that pattern so a future field addition can't silently leak).

---

## 9. Minimum adversarial negative tests before activation

All must pass, and the code-execution ones (T-net/secret/git/escape/fork) must be driven **from inside a package `test` script**, not just a shell, since that is the real threat:

- **T-net** — package script attempts TCP/UDP/DNS egress → `ENETUNREACH`/failure; no data leaves.
- **T-secret** — script reads `~/.ssh`, `~/.config/gh`, `~/.npmrc`, `/proc/1/environ`, `$GH_TOKEN` → all absent/empty.
- **T-git** — script writes `.git/hooks/pre-commit`, `.git/config` (`core.hooksPath`), common gitdir → denied (ro bind); a later git command executes no injected hook.
- **T-controlplane** — script/edit targets policy, settings, audit, hook, or `build/server/*` enforcement files → denied by path classifier and not present in sandbox.
- **T-docker** — script attempts to reach `/var/run/docker.sock` or any container socket → absent; bind refused.
- **T-escape** — path/symlink escape: symlinked worktree entry pointing outside, `../` traversal, symlinked policy dir (V243-C2-005) → all denied; write lands nowhere outside the rw worktree bind.
- **T-meta** — `npm test && git push`, `npm test; gh …`, backticks, `$(...)`, pipe-to-`sh`, `git -c core.hooksPath=…`, `npm --prefix /etc …`, newline-embedded → all denied before exec.
- **T-fork** — package script fork-bomb / spawns 10k procs → `RLIMIT_NPROC`/timeout kills it, deny recorded.
- **T-resource** — memory balloon and disk fill → cgroup/`RLIMIT` caps hold; deny.
- **T-revoke** — command N allowed, revoke, command N+1 denied same session, survives relaunch (V243-C2-006).
- **T-coms** — inbound coms request instructing a gated action → receiver hook denies (proves peer-induced actions are gated).
- **T-hookfail** — hook binary removed/crashing → tool not auto-approved (zero allow rules + `defaultMode: default` degrade to human prompt, never allow).
- **T-canary** — installed-Claude 2.1.195 settings isolation: repo/user `settings.json` allow-rule/hook is **not** honored under `--setting-sources ''` (V243-C2-008, still open; may be a recorded human-operated local check).

---

## 10. Separate PRD/security approval, or #243 follow-up?

**Implementable as a bounded #243 follow-up — but it requires its own explicit security sign-off and its own activation gate before it is switched on.**

Rationale: #243's approved scope already includes a project-scoped safe-autonomy path and a security-reviewed verification-command decision, and the operator has now chosen "sandbox is the only path," so this is within the PRD's intent rather than new product scope. However, a filesystem/namespace sandbox that executes agent-modified code is a materially larger blast radius than the pure-policy hook, so treat it as a distinct checkpoint (call it checkpoint 2b/3): it cannot ride the existing checkpoint-2 approval, must land only after V243-C2-001/003/005/006/007 are fixed, and must pass §9 in a human-operated run before the delayed-response live validation.

If the sandbox design grows to need a container runtime, a privileged helper, or any network egress, escalate to a separate PRD — those exceed #243's blast radius.

---

## Findings

| ID | Severity | Exploit / failure path | Bounded remediation |
|---|---|---|---|
| **F1** | **Critical** | `autonomyGates.ts:84-89` auto-allows `npm run`/`npm test`/`node --import tsx --test` **unsandboxed today**, contradicting the operator decision and re-opening V243-C2-002 (agent-written test script runs with user authority, network + credentials). | Remove `verification_command` from host auto-allow; route the allowlist exclusively through the bwrap launcher (§5). Until the sandbox lands, verification stays human-gated. |
| **F2** | **Critical (precondition)** | V243-C2-001 unfixed: policy/settings/audit/hook + import graph are under the writable artifact/worktree root; agent edit + build rewrites enforcement. | Owner-only control-plane root outside all binds; snapshot + hash-verify the hook and imports; deny classifier on that root (§6). |
| **F3** | **High** | Env inheritance (V243-C2-003): PTY inherits full `process.env`; denylist unset misses arbitrary `*_SECRET`. Sandbox child must not inherit it either. | Allowlist-constructed env for both native launch and sandbox child; `--clearenv` + explicit injects (§2). |
| **F4** | **High** | Common gitdir must be exposed for git to work in a worktree; a rw bind exposes `config`/`hooks` as an execution vector. | Bind common gitdir **read-only**; never rw; T-git must show no hook injection survives. |
| **F5** | **High** | Host hardening drift: a future `apparmor_restrict_unprivileged_userns=1` breaks bwrap; naive fallback would run unsandboxed. | Launch preflight probes userns; on failure **deny verification**, never fall back. |
| **F6** | **Medium** | Settings/hook validation still substring-based (V243-C2-007); revocation reset + role-as-session (V243-C2-006). | Exact schema/command validation, owner-only file checks; bind policy to real pane/session id, preserve revoked across relaunch. |
| **F7** | **Medium** | Output/resource caps unspecified; a test can exhaust memory/disk or flood stdout into audit/artifacts. | Wall-clock 300 s, `RLIMIT_NPROC`/mem/`FSIZE`/tmpfs caps, 1 MiB output cap → kill + deny (§2, §7). |
| **F8** | **Low** | Missing enumerated reason codes for sandbox failures ⇒ deny paths not auditable by code. | Add `deny_sandbox_unavailable`/`deny_sandbox_start`/`deny_timeout`/`deny_output_limit` to `REASON_CODES`. |

---

## Exact implementation constraints (summary)

1. Executor is an AgentOps-owned launcher on the control-plane root; the only path to `npm`/`node`/`git` is through `bwrap`. No agent tool call reaches an unsandboxed interpreter.
2. `bwrap --unshare-all` (net, pid, ipc, uts, user, cgroup) with **no `--share-net`**; `--die-with-parent`; `--clearenv` + explicit env allowlist; `--proc /proc`, `--dev /dev`, `--tmpfs /tmp`; no `/sys`, no sockets.
3. Binds: worktree rw (only rw real-data bind); common gitdir ro; node+git toolchain ro; nothing else. Control-plane, artifacts, secrets, home never bound.
4. Resource caps: 300 s wall-clock, `RLIMIT_NPROC`, memory cap, `RLIMIT_FSIZE`, tmpfs size cap, 1 MiB output cap; timeout kills the process group/namespace.
5. Preflight: probe unprivileged userns; deny verification if unavailable. Never fall back to unsandboxed exec.
6. Control plane (policy/settings/audit/hook/import graph) owner-only, outside every read/write root, snapshot + hash-verified.
7. Enumerated audit only; 256 KiB rotation with one retained prior file; no argv/stdout/stderr/secret stored.
8. Fix V243-C2-001/003/005/006/007 as preconditions; pass §9 in a human-operated run before live validation.

---

## Initial command allowlist (activation baseline)

See §3. Finite and anchored; arguments must resolve inside the worktree; commands with shell metacharacters or env-assignment prefixes are denied before matching. Everything not listed is denied.

---

## Required tests

See §9 (T-net, T-secret, T-git, T-controlplane, T-docker, T-escape, T-meta, T-fork, T-resource, T-revoke, T-coms, T-hookfail, T-canary). Code-execution tests must run from inside a package `test` script.

---

## Residual risks (record, do not silently accept)

- **In-sandbox correctness of agent code is not vouched for** — the sandbox contains impact, it does not validate that tests are meaningful; a hostile test that merely *passes* is possible. Acceptable: the gate is safety, not trust.
- **Kernel/bwrap 0-day** — namespace escape via a kernel or bwrap bug remains theoretically possible; mitigated by no-network, no-secrets, unprivileged uid, `no_new_privs`. Track bwrap/kernel CVEs.
- **Build cache poisoning** — a run may write `node_modules/.cache` the next run reads; contained to the worktree, but note it. Consider a tmpfs cache per run if it matters.
- **Common-gitdir read exposure** — the whole main repo history/config is readable (ro) inside the sandbox. Contained (already the agent's own repo), but it is broader than the worktree.

---

## Dated sources

- Bubblewrap README + man page, `github.com/containers/bubblewrap` — cross-checked against installed `bwrap 0.9.0`; behavior live-verified 2026-07-18.
- Anthropic Claude Code — PreToolUse hooks: https://docs.anthropic.com/en/docs/claude-code/hooks#pretooluse (per-tool-call, not per-subprocess; deny/exit-2 semantics) — cited by checkpoint-2 researcher 2026-07-18.
- Anthropic Claude Code — settings & `--setting-sources`: https://docs.anthropic.com/en/docs/claude-code/settings — 2026-07-18; installed Claude 2.1.195 (canary still required per V243-C2-008).
- Ubuntu 24.04 unprivileged user-namespace AppArmor restriction (`kernel.apparmor_restrict_unprivileged_userns`) — Ubuntu 24.04 release notes; observed value `0` on this host 2026-07-18.
- Git worktree layout (`.git` gitdir pointer / `commondir`) — `git-worktree` docs; verified against this worktree 2026-07-18.
- Checkpoint-2 verifier report `verifier-report.md` (V243-C2-001…010, `revision_requested`) and the working-tree modules `autonomyGates.ts`, `pretoolHook.ts`, `autonomyPolicy.ts`, `autonomyAudit.ts`, `claude-native.sh` diff — read 2026-07-18.

---

## Net

Adopt Bubblewrap with the §2 boundary, §3 allowlist, and §5 hook-to-launcher routing; block activation on F1–F6 and the §9 tests; keep it a bounded #243 follow-up with its own security sign-off and human-operated validation before the live delayed-response run.
