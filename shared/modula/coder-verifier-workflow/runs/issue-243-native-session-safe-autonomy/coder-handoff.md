# Coder Handoff — Issue #243

## Current status

`post_pr_kody_verifier_approved` — checkpoints 2, dormant Bubblewrap 2b, checkpoint 3 revision 4, checkpoint 4 revision 7, and post-PR Kody remediation revision 9 are verifier-approved. Revision 9 completed its final bug-check with no open findings. PR #252 remains open; native wiring and autonomous execution remain disabled.

## Post-PR Kody remediation — 2026-07-19

- Kody finding `d2c6d5a895e49ec6` fixed: audit append/rotation now runs under a bounded owner-only exclusive lock, so separate hook/executor processes cannot interleave rotate/append operations. A held-lock regression proves audit state remains unchanged and fails closed.
- Kody finding `9bb14d1106c62f3b` fixed: verification audit writes now pass the trusted `controlRoot`; control-plane tree validation rejects audit files outside that root. A negative regression covers a private but out-of-root audit path.
- Kody finding `66b3ba19e981fec2` is non-actionable: a fresh source-cited Researcher recheck confirms successful exact `LoadState=not-found` from the same systemd v255 user manager is collected-scope proof; `unit_may_gc()` retains units with recursively non-empty cgroups. Existing C4-007 strict query/error validation remains unchanged.
- Validation: focused audit/control/lifecycle suite 39/39; `npm --prefix term-control-center run test:sandbox` passed 26 structural plus 13 live; typecheck, full build, `git diff --check`, and post-suite `agentops-verify-*` scope inventory passed. Full build retained only known non-failing Vite static-script/chunk-size warnings.
- `V243-C4-008` fixed after the revision-8 recheck: trust validation now requires lexical containment within `controlRoot` while traversing through its immediate parent; a regression proves `readPolicy()` rejects a valid policy when that parent later becomes mode `0777`.
- Revision-9 validation: focused audit/control/lifecycle suite 40/40; `npm --prefix term-control-center run test:sandbox` passed 26 structural plus 13 live; typecheck, full build, `git diff --check`, and post-suite scope-residue checks passed. Full build retained only known non-failing Vite static-script/chunk-size warnings.
- Final verifier verdict: approved — post-PR Kody remediation revision 9 completed its final bug-check with no open findings. Next actor: Git Manager may commit and push this bounded correction to PR #252; Kody may then be explicitly rerun. No merge, deployment, activation, permission bypass, or unrelated GitHub mutation is authorized.

## Revision 7 submission — 2026-07-19

- `V243-C4-004` fixed: removed the stale terminal copy-mode session handover from this PRD branch. The separate `fix/tmux-copy-mode-hold` branch retains that work; the cumulative PRD diff has no terminal/tmux artifact. The touched-file inventory no longer lists the net-zero `comsAdapter.ts` path and now matches the retained cumulative diff.
- `V243-C4-006` fixed without behavior change: split control-file trust/write/verification helpers and browser prompt assertions so every changed function/test callback is below the repository limit.
- `V243-C4-007` fixed: collected proof now requires exact `LoadState=not-found`; otherwise cleanup requires an exact loaded, inactive/failed scope with an explicit control-group property and verified drained cgroup. A live regression test injects a status-zero incomplete manager response and proves it disables the session instead of accepting cleanup.
- Validation: focused adapter/native/autonomy suite 32/32; `npm --prefix term-control-center run test:sandbox` passed 25 structural plus 13 live; typecheck, full build, `git diff --check`, and post-suite `agentops-verify-*` scope inventory passed. The full build retained only known non-failing Vite static-script/chunk-size warnings.
- Final verifier verdict: approved — checkpoint 4 revision 7 final safety review and bug-check completed with no open findings. Next actor: human/operator for any separate PR-preparation, push, or PR-creation decision. No push, PR, merge, GitHub mutation, activation, or permission bypass occurred; those remain human-gated.

## Revision 6 submission — 2026-07-19 (superseded)

- `V243-C4-005` fixed in two commits: `7cef12b` tracks and clears the pending verify timer and accepts already-collected successful scopes; `e3f94bb` completes the remediation — an inactive scope with no reported control group counts as positively torn down (systemd deactivates a scope only after every process in its cgroup is reaped), and `settleScope` retries briefly for positive proof before strict forced termination. Fail-closed behavior is preserved when proof is genuinely unavailable. New live regression test: `fast successful scopes remain verified and reusable`.
- `V243-C4-003`/`V243-C4-004` evidence remediations landed in `5dd48fc`: the superseded receipt is labeled historical with its schema-conformance assertions removed, the handoff status/supersession conflict is resolved, the r3 handoff records its final nested artifact paths, the activation receipt's wiring statement is corrected, and the touched-file inventory marks `comsAdapter.ts` net-zero.
- Advisory tightening in `5dd48fc`: the default native pane policy now grants only `local_read`/`workspace_edit`/`peer_coms`; `verification_command` requires the explicit activation decision (tested). The one existing host control-plane policy was updated in place to version 2 with the same reduction. The README documents the hook-denial constraint for non-coms tools on native panes.
- Scope restoration: the unrelated terminal copy-mode fix `db69092` is reverted from this branch (`ebc52fe`) and preserved as `cee9e48` on `fix/tmux-copy-mode-hold` off `origin/main` for a separate fix-only PR decision. The cumulative PRD diff contains no terminal/tmux files.
- Validation: focused adapter/native/autonomy suite 48/48; `npm --prefix term-control-center run test:sandbox` passed 25 structural plus 12 live on three consecutive runs (one pre-fix flake of the new fast-exit test was observed and eliminated by `e3f94bb`); typecheck and `git diff --check` passed after every change; no `agentops-verify-*` unit remained.
- Requested next actor: verifier — checkpoint 4 revision 6 final safety review and bug-check. No push, PR, merge, GitHub mutation, activation, or permission bypass occurred; those remain human-gated.

## Post-synchronization validation — 2026-07-18

- Exact change in this validation pass: no product-code change; this handoff records the Git Manager synchronization and fresh validation results.
- Git Manager fetched and strictly fast-forwarded to `origin/main` twice because the remote advanced during finalization; no merge commit or conflict. The branch remains synchronized with `origin/main` (zero behind); local evidence commits remain unpushed and each action is recorded in the Git Manager ledger. The authorized implementation scope retained its content fingerprint through synchronization. Ledger: `/home/hyperbots/.local/state/agentops/term-control-center/git-actions.jsonl`.
- `npm --prefix term-control-center run test:sandbox` — passed: 25 structural and 10 live tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed, including client and server builds. Vite emitted non-failing warnings for two non-module static scripts and a minified chunk above 500 KiB.
- `git diff --check` — passed. `dev-plans/prd-backlog.md` is restored and clean.
- Receipt: `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/sandbox-activation-validation.json`; it remains `validated_dormant`, with `sandbox_enabled: false` and `native_wiring_enabled: false`.
- Required Steward hygiene review — clean: all changed files and run evidence are in approved locations; run artifacts are sanitized and parseable; no generated tracked drift, launcher/config ownership issue, or KISS/file-size issue remains. The `verifier-report.md` length is accepted as run evidence, not product code.
- Native Claude→Codex live validation receipt: `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/native-coms-validation-243.md`. It records a pass in isolated same-worktree pool `agentops-prd-243-native-validation`: native `coms_list` found one live Codex verifier; a bounded synthetic `coms_send` received an ID; short and longer waits returned only non-fatal `timeout`/`pending`; and `coms_get` returned a correlated response whose observed fields matched the request; no adapter-level JSON-Schema validation exists, and the r4 exact four-field payload equality is the sole final payload evidence. It retains no prompts, response payload, tokens, or transcripts. Final verifier review must independently assess the receipt against every PRD criterion, including verifier-side one-response/resumed-availability evidence.
- Skipped: native activation, final verifier safety review, and final bug-check. They are not passed or approved.
- Residual gates: final verifier safety review and bug-check remain required before enabling the bounded autonomous path or preparing a PR. The existing authorization does not permit arbitrary commands, network, credentials, PR/deploy actions, push, PR creation, or permission bypasses.

## Checkpoint 4 revision 2 in progress

- `V243-C4-001` fixed: natural process close now checks for a drained scope and, when descendants remain, terminates and verifies the complete scope before returning. The session remains disabled if that termination or verification fails.
- Added shipped-lifecycle live coverage for detached descendants after both zero and nonzero parent exits. The test-only finite validation IDs and package scripts remain excluded from the production parser/build.
- `V243-C4-002` is addressed pending final verifier recheck: the committed deterministic real-socket test proves the controlled timeout/pending/release lifecycle, and the r4 live receipt proves exactly-one normal Pi correlated response/no reply-via-`coms_send`, exact requested-payload equality, and post-response verifier availability.
- Required dead-end Researcher consult, 2026-07-18: a human foreground turn can prove one bounded native-Claude→Pi/Codex round trip and structural responder behavior, but documented native Claude/Pi behavior cannot deterministically prove a model-requested responder delay. A deterministic delay requires separately reviewed test-only responder/atomic-helper work; no background task, prompt injection, or permission bypass is acceptable. The installed native wrapper also does not pass Claude's history-skip control, so literal no-local-history validation needs separately approved launcher-policy work; human purge is cleanup, not prevention. Sources: Claude CLI/permissions docs and `pi-coms-local`, checked 2026-07-18.
- Deterministic helper: `tests/comsAdapter.final.test.ts` now uses two production `ComsAdapter` instances and real local socket/wire behavior to prove send → short timeout → pending → controlled delayed release → exactly one correlated completion → responder remains listable. It changes no production MCP, adapter, policy, or wire surface. The native wrapper forwards only exact `CLAUDE_CODE_SKIP_PROMPT_HISTORY=1`; the README documents this validation-only history control.
- Native runtime policy correction: exact ToolSearch discovery of the six strict `coms-mcp` methods is classified as `peer_coms` only for the fixed `select:` query and `max_results: 6`; every other ToolSearch shape and all other MCP discovery remain denied. The native standing-peer prompt supplies that exact selection before its first coms call. It also gives the agent the existing launch-supplied context-brief path for direct `Read`, which is already permitted within the trusted artifact root. This fixes the observed C4-002 runtime blocker without broadening Bash, GitHub, WebFetch, strict MCP, worktree, or authority boundaries. Focused hook/launch-plan tests pass.
- Live receipt r3 is retained under `native-coms-r3/`: it proves strict tool discovery, one same-pool verifier, one normal correlated Pi response, no reply-via-`coms_send`, and post-response liveness. It is partial evidence only: its response is schema-nonconformant, so its own `final: passed` label is not a PRD-final claim.
- User-provided commit `b4a97c6` exposed the Pi responder's request-schema metadata and updated the native prompt to require the exact requested JSON object in peer prompt text, because the normal Pi response path does not expose that metadata to its model. The broad `schema_conformant` adapter annotation was removed after final bug-check found it could overclaim unsupported JSON Schema validation; response delivery remains unchanged.
- Live receipt r4 is retained under `native-coms-r4/`: native Claude read the supplied context brief, used only the six strict coms tools, found exactly one same-worktree Codex verifier, sent exactly one request, received one harness-native—not `coms_send`—correlated reply whose exact four-field payload is recorded, and found that verifier live afterward. It pairs with the committed real-socket deterministic test-only responder proof (short timeout → pending → controlled release → one correlated completion → responder listable). Together they address the two distinct C4-002 evidence requirements; final verifier acceptance remains required.
- Revision validation: after removing the unsafe broad schema annotation, the focused adapter/native suite passed 39/39; `npm --prefix term-control-center run test:sandbox` passed, 25 structural plus 11 live tests; typecheck, full build, and `git diff --check` passed. The full build retained only the non-failing Vite static-script/chunk-size warnings. Verifier checkpoint-4 revision 2 independently resolved `V243-C4-001`; C4-002 has r4 evidence and awaits final recheck.

## Final verifier outcome — 2026-07-18 (superseded by checkpoint 4 revision 5)

- Superseded 2026-07-19: the independent checkpoint 4 revision 5 review of `257eadf` returned `revision_requested` with open findings `V243-C4-003`, `V243-C4-004`, and `V243-C4-005`; the statements below are retained as dated history only and PR-material preparation is on hold until revision 6 is approved.
- Checkpoint 4 revision 4 — approved; no open findings; final bug-check completed with no findings. The coder did not read the full approved report.
- Steward final hygiene recheck — clean after C4-003/C4-004 cleanup.
- Final evidence includes the deterministic real-socket delayed responder test and the r4 native Claude→Codex exact-payload/liveness receipt. C4-001 through C4-004 are resolved.
- PR materials may now be prepared locally under the recorded operator authorization. Push and opening a PR remain separately human-gated; no native activation, deployment, GitHub mutation, or permission bypass is authorized.

## Source and authorization

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/243
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-243`
- Branch: `prd/native-session-coms-followup-243`
- Context brief: `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-243-ab5c0e8a0fdc/artifacts/project-context-brief.md`
- The operator authorizes automatic bounded coder/verifier revisions for this PRD run.
- Human/security decisions dated 2026-07-18 approve exact finite environment names, the conservative secret config/data basename taxonomy, the fixed owner-0700 control-plane base, and option B.
- The operator approved one additional fail-closed trusted evidence-root correction after checkpoint 2b revision 4.
- The operator subsequently approved live sandboxed adversarial validation.
- On 2026-07-18, the operator authorized native wiring and autonomous execution only for the immutable sandboxed `typecheck` command, using the validated Bubblewrap/systemd lifecycle and existing policy kill switch. Enabling remains conditional on branch synchronization and final Steward/verifier checks.
- On 2026-07-18, the operator authorized Git Manager to create local checkpoint commits for the complete enumerated PRD #243 scope so the worktree can become clean for required live validation. PR preparation may follow final approval, but push and PR creation remain separately human-gated.
- On 2026-07-18, the operator authorized the bounded C4-002 extension: a deterministic test-only responder-delay/atomic validation helper and documented no-history validation handling when safely supported. Strict local MCP configuration, project-scoped policy, kill switch, and high-impact denials remain unchanged; global/default `--dangerously-skip-permissions` remains prohibited.
- Global permission bypass remains rejected. Arbitrary commands, network, credentials, PR/deploy actions, push, merge, GitHub mutation, secrets/auth changes, destructive filesystem actions, external sends, money-related actions, and scope expansion remain prohibited or human-gated as applicable.

## Checkpoint-2 implementation

- Native Claude launches with one AgentOps-owned settings source and one strict local coms MCP configuration.
- A synchronous `PreToolUse` hook hard-denies always-gated and untrusted execution before policy evaluation.
- Policy is strict, default-deny, worktree/session-bound, re-read per action, atomic, owner-controlled, and preserves revocation. Existing malformed, untrusted, or mismatched state fails launch closed.
- Policy, settings, audit, the native wrapper, and the built enforcement graph are protected from autonomous writes.
- Audit records are enumerated and sanitized, rotate at 256 KiB with one retained file, reject untrusted paths/files, and fail actions closed when persistence fails.
- Reads are worktree/artifact scoped. `.git`, protected roots, broad searches, credential/config files, and escaping symlinks deny.
- The final native child environment is constructed from exact allowed names. Only `LC_ALL` and `LC_CTYPE` locale variables are retained; `LC_SECRET` and unknown locale-like names are removed.
- Delimiter-aware config/data basename denial covers password, passphrase, secret, credential, service account, API key, access key, private key, auth, token, webhook, cookie, JWT, and wallet categories. Ordinary source files such as `auth.ts` remain readable.
- All Bash, including read-only Git, remains denied until a separately approved Bubblewrap executor exists.
- Option B remains a mapping only: native Claude named await/respond corresponds to the Pi-hosted Codex normal-response correlated reply. No coms wire/adapter or legacy delegated-Claude behavior changed.

## Finding disposition

- `V243-C2-001`: resolved — state/build/wrapper enforcement paths are protected.
- `V243-C2-002`: resolved — all host Bash/Git/npm/node/build/test execution is denied; no sandbox is active.
- `V243-C2-003`: resolved in revision 6 — both TypeScript and shell use exact locale names; TypeScript and wrapper tests deny `LC_SECRET`/`LC_FAKE` and retain `LC_ALL`/`LC_CTYPE`.
- `V243-C2-004`: resolved in revision 6 — the approved config/data basename categories are implemented and tested, including `passwords.txt`, `passphrase.json`, `api-key.json`, `access-key.csv`, and `webhook-url.txt`; `auth.ts` remains readable.
- `V243-C2-005`: resolved — control state uses a fixed owner-0700 base with base-to-leaf owner/mode/symlink validation.
- `V243-C2-006`: resolved — invalid repeated setup fails closed and revocation persists.
- `V243-C2-007`: resolved — exact nested settings schema rejects async/extra fields.
- `V243-C2-008`: resolved — `installed-claude-settings-canary.json` records a passed sanitized Claude Code 2.1.195 differential canary.
- `V243-C2-009`: addressed by this singular revision-6 handoff.
- `V243-C2-010`: resolved — `launchPlan.ts` is 296 lines and changed code remains within KISS limits.
- `V243-C2-011`: resolved for this review — approved run evidence is retained, `.ralph/` is absent, and generated backlog drift is restored before verifier requests.

## Touched files

### Implementation and tests

- `scripts/agentops/claude-native.sh`
- `term-control-center/package.json`
- `term-control-center/README.md`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/autonomyAudit.ts`
- `term-control-center/server/autonomyControlPlane.ts`
- `term-control-center/server/autonomyGates.ts`
- `term-control-center/server/autonomyPaths.ts`
- `term-control-center/server/autonomyPolicy.ts`
- `term-control-center/server/comsWire.ts`
- `term-control-center/server/delegationPrompts.ts`
- `term-control-center/server/nativeClaudeSettings.ts`
- `term-control-center/server/verificationSandbox.ts`
- `term-control-center/server/verificationExecutor.ts`
- `term-control-center/server/verificationRuntime.ts`
- `term-control-center/server/verificationScopeLifecycle.ts`
- `term-control-center/tsconfig.server.build.json`
- `term-control-center/server/pretoolHook.ts`
- `term-control-center/tests/autonomyControlPlane.test.ts`
- `term-control-center/tests/autonomyHook.test.ts`
- `term-control-center/tests/comsAdapter.final.test.ts`
- `term-control-center/tests/nativeClaudeLaunchPlan.test.ts`
- `term-control-center/tests/nativeClaudeLauncher.test.ts`
- `term-control-center/tests/verificationSandbox.test.ts`
- `term-control-center/tests/live/verificationExecutor.live.test.ts`
- `term-control-center/tests/support/verificationValidationHarness.ts`
- `term-control-center/tests/fixtures/verificationSandboxAdversary.mjs`
- `term-control-center/tests/fixtures/verificationSandboxNaturalExit.mjs`
- `term-control-center/tests/fixtures/verificationSandboxOom.mjs`
- `term-control-center/tests/fixtures/verificationSandboxOutput.mjs`
- `term-control-center/tests/fixtures/verificationSandboxTimeout.mjs`

### Approved run evidence

- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/fixes-applied-umask-hook-modes.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/installed-claude-settings-canary.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/review-native-claude-settings-validation.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/review-umask-hook-mode-diagnosis.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/security-review-sandbox.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/sandbox-activation-validation.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/native-coms-validation-243.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/native-coms-r3/{coder-handoff-r3.md,validation-receipt-r3.json}`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/native-coms-r4/coder-handoff.md`

## Revision-6 validation

- `bash -n scripts/agentops/claude-native.sh` — passed.
- `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/autonomyControlPlane.test.ts tests/nativeClaudeLauncher.test.ts tests/nativeClaudeLaunchPlan.test.ts` — 31/31 passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed.
- `git diff --check` — passed.
- `wc -l term-control-center/server/launchPlan.ts` — 296 lines.
- Installed-Claude settings-isolation canary — passed on Claude Code 2.1.195; no bypass mode or raw debug/prompt/response evidence retained.
- Full suite/app build — deferred to the later full-validation checkpoint.

## Current risks and cleanup deviation

- Bubblewrap containment is validated locally, but no native tool/launcher/MCP wiring is active and autonomous verification execution is not enabled.
- Strict MCP isolation remains mandatory because settings-source isolation does not exclude user MCP configuration.
- Legacy delegated-Claude `bypassPermissions` remains an explicit out-of-scope residual risk and is unchanged.
- The branch is zero behind `origin/main`; local evidence commits remain unpushed and the latest clean-tree validation was run on that synchronized base.
- `dev-plans/prd-backlog.md` is restored and clean; no generated backlog drift remains.
- `.ralph/` is absent. No task-generated temporary artifacts are retained outside the approved run directory.
- No secrets, raw prompts, responses, transcripts, tokens, or private account data are retained.
- Standards exception: none.

## Bubblewrap implementation checkpoint — revision 5

- The future autonomous runtime boundary exposes only non-emitting `typecheck` and `test`. Three separate fixed validation-only IDs exercise containment, output-limit, and timeout behavior; unknown/non-string values, including `build` and `build-server`, return `deny_sandbox_start`.
- Root resolution derives linked-worktree private/common Git metadata from the trusted worktree gitfile, rejects symlinked/malformed/unrelated roots, and mounts the Git file, private/common Git directories, supplied enforcement paths, and durable run evidence read-only inside the writable worktree bind.
- Production preflight requires a root-owned executable `/usr/bin/bwrap`, strict readable user-namespace sysctls, a bounded strict-userns no-op probe, and a supported owner-controlled Node runtime. Unknown/read/probe errors normalize to `deny_sandbox_unavailable`.
- The active Node 22 prefix is mounted read-only at `/opt/agentops/node22`; exact child environment is `PATH`, `HOME`, `TMPDIR`, `CI`, `NODE_ENV`, and `AGENTOPS_WORKTREE` only.
- Namespace planning uses `--unshare-user --unshare-all --clearenv`, no shared network, no resolver/home/run/sysfs/socket bind, namespaced proc/dev/tmp, and only the worktree as a writable real-data bind.
- `term-control-center/server/verificationSandbox.ts` is 187 lines with small named validation, preflight, Git, evidence, environment, and mount helpers. The test file is 128 lines.
- `V243-C2B-001`: resolved after explicit human approval — `build` and `build-server` IDs remain removed; the `.git` pointer, wrapper, complete current `build/server` enforcement root, and every run-evidence directory matching the trusted `agentops-prd-<issue>` worktree are derived internally as mandatory read-only mounts. There is no caller-selected evidence-root input. Missing, wrong-issue, file, and unrelated evidence candidates fail closed. External owner-private runtime snapshot/wiring remains an activation prerequisite and is not claimed.
- `V243-C2B-002`: trusted linked-worktree/Git relationship validation and negative fixtures added.
- `V243-C2B-003`: injectable fail-closed host adapter and bounded production no-op probe added; unavailable/restricted/read/probe negatives pass.
- `V243-C2B-004`: exact denial and exact post-`--` argv tests added for every command ID.
- `V243-C2B-005`: active supported Node 22 toolchain is selected and mounted at a neutral path; nonexistent `lint` ID removed.
- `V243-C2B-006`: `TMPDIR` and worktree environment restored; exact environment parity is tested.
- `V243-C2B-007`: addressed by this current revision-5 handoff.
- `V243-C2B-008`: compressed implementation replaced with readable single-purpose helpers.
- Direct host Bash—including npm/node/Git—remains hard denied. No native MCP/launcher/hook wiring or sandboxed package-script execution was added.
- Validation: `npm --prefix term-control-center run typecheck` passed; focused autonomy/sandbox tests passed 25/25; `npm --prefix term-control-center run build:server` passed on the human-operated host validation path; production no-op bwrap preflight/plan construction passed; `git diff --check` passed.
- `dev-plans/prd-backlog.md` is generated runtime drift and is restored immediately before the verifier request.

## Checkpoint 3 revision-1 history — superseded

Revision 1 added the initial unwired executor and two live tests. The verifier found its public/test command separation, audit enumeration, process-group cleanup, disk containment, launch-time revocation, and KISS evidence insufficient. The current revision-2 section below replaces those mechanisms and claims. Native wiring and autonomous execution remained disabled throughout.

## Revision-4 researcher consult

A required dead-end consult on 2026-07-18 recommends one shipped internal lifecycle engine plus an excluded test-only finite case adapter. The engine may accept a generic prepared job but must expose no validation IDs, mutable caller options, policy, or audit authority; native input still reaches it only through the finite production parser. Disabled state must be checked before allow audit and again before spawn. For OOM, trusted evidence is the known unique scope reporting `Result=oom-kill`, inactive/failed state, verified `OOMPolicy=kill`, and empty/missing previously captured cgroup. Sources: systemd.scope(5), systemd resource-control documentation, Linux cgroup-v2 documentation, and Node 22 test-runner documentation, checked 2026-07-18.

## Checkpoint 3 — revision 4 current state

- Revision 2 initially retained `typecheck` and `test`; revision 3 narrows production `verificationPlan()` and `runVerification()` to the only demonstrated immutable command ID, `typecheck`. The actual production entrypoint completes live under the fixed 300-second limit. Validation IDs, mutable validation limits, and plan transformation now exist only in `tests/support/verificationValidationHarness.ts`, are runtime-enumerated, and are excluded from the production server build by `tsconfig.server.build.json`. The default test glob also excludes `tests/live/verificationExecutor.live.test.ts`.
- Command ID validation occurs before any audit write. Audit `command_id` is typed and runtime-filtered to the finite production/test enum; invalid production requests produce `deny_sandbox_start` without creating an audit record.
- The executor creates a UUID-named trusted `systemd-run --user --scope` with `KillMode=control-group`, `SendSIGKILL=yes`, `TimeoutStopSec=1s`, `RuntimeMaxSec`, `TasksMax`, `MemoryHigh`, `MemoryMax`, `MemorySwapMax=0`, `OOMPolicy=kill`, and `Delegate=no`. Systemd calls are status-aware. Forced cleanup requires successful kill and stop plus a positively known inactive/failed, empty/missing cgroup; a previously observed collected unit is distinguished from manager failure. Natural success and nonzero exits also require final drainage. Any unverifiable cleanup disables that session, and the live manager-failure test proves the next same-session request denies.
- Bubblewrap mounts the worktree read-only and creates a sized `/tmp` tmpfs (1 GiB production; a fixed 16 MiB test harness cap). `RLIMIT_FSIZE` remains only a supplement. The adversarial package fixture now proves many-file ENOSPC under the sized tmpfs.
- Policy is re-read after plan/preflight and immediately before authorization audit/spawn. The live suite injects revocation in that window and proves no allow audit/launch.
- The single shipped lifecycle is `verificationScopeLifecycle.ts`. Production `verificationRuntime.ts` supplies only the immutable production plan/limits; excluded test support supplies only frozen, runtime-enumerated validation cases. Timeout, output, OOM, successful exit, and manager failure now execute the exact same shipped lifecycle—no duplicate executor remains.
- Disabled session state is checked before any allow audit and again inside the lifecycle immediately before spawn. The manager-failure test proves the next same-session request creates no allow audit and never calls `spawn`.
- Production authorization/completion audit-failure tests include a long invalid ID and prove subsequent fail-closed behavior. The OOM fixture must yield trusted systemd `Result=oom-kill`, inactive/failed state, verified `OOMPolicy=kill`, and a drained known cgroup; ordinary nonzero failure cannot satisfy the claim.
- Native launcher, hook, MCP, coms transport, runtime wiring, and direct host Bash denials are unchanged. The executor/test harness remain imported only by their live test.

### Checkpoint 3 revision-4 finding disposition

- `V243-C3-001`: production retains only live-proven `typecheck`; validation authority is test-only and absent from the clean production server build.
- `V243-C3-002`: authorization and completion audit failures, subsequent fail-closed behavior, and long invalid IDs are covered.
- `V243-C3-003`: disabled sessions now produce deny-only audit/no spawn; timeout/output/manager/success cleanup all run through the single shipped lifecycle.
- `V243-C3-004`: OOM now runs through that same shipped lifecycle and requires systemd `Result=oom-kill`, verified OOM policy/inactive state, and known-cgroup sibling drainage.
- `V243-C3-005` and `V243-C3-006`: remain resolved without regression.

### Checkpoint 3 revision-4 validation

- `npm --prefix term-control-center run test:sandbox` — passed in revision 4: 25 structural and 10 live tests, including the live production `typecheck` entrypoint and exact shared-lifecycle timeout/output/OOM cases.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed on the human-authorized local validation host.
- `git diff --check` — passed.
- AST KISS check — all C3 functions remain under 20 lines with at most four parameters; all C3 files remain under 300 lines.
- `systemctl --user list-units 'agentops-verify-*' --all` — empty after the suite.
- `build:server` uses `tsconfig.server.build.json`; its clean output excludes `build/tests` and every validation harness. The default test glob excludes `tests/live/verificationExecutor.live.test.ts`. A prior revision-2 full default-suite invocation exceeded 600 seconds; the unsafe/unvalidated public `test` ID has therefore been removed rather than claiming it fits the immutable 300-second production limit.
- New/updated C3 surfaces: `verificationSandbox.ts`, `verificationExecutor.ts`, `verificationRuntime.ts`, `verificationScopeLifecycle.ts`, `autonomyAudit.ts`, `package.json`, `tsconfig.server.build.json`, `verificationSandbox.test.ts`, `autonomyHook.test.ts`, `tests/support/verificationValidationHarness.ts`, `tests/live/verificationExecutor.live.test.ts`, and the four verification sandbox fixtures.

### Checkpoint 3 revision-4 residual risks

- This is human-authorized local validation evidence, not activation authority. The executor remains dormant/unwired and no agent-facing tool/launcher/MCP/runtime path reaches it.
- The in-memory session disable flag is a fail-closed session guard after cleanup verification failure; future activation still requires verifier approval and a separate human decision.
- `dev-plans/prd-backlog.md` remains generated timestamp drift and must be restored immediately before the verifier request.

## Next actor

Checkpoint 3 revision 4 is approved with no open findings. The next action that could activate or wire autonomous verification is a true human/security gate and is not authorized here. Native wiring and autonomous verification remain forbidden.

## Immutable checkpoint-1 history

Checkpoint 1 selected option B from fresh official Claude/Pi/Codex evidence and stopped `needs_human`. The operator and security reviewer then approved the bounded policy decisions on 2026-07-18, authorizing checkpoint-2 implementation without expanding PR/merge/deploy/GitHub/secrets/money authority. Legacy delegated-Claude bypass remained out of scope.
