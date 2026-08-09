# Coder handoff — Issue #231 native Claude coms peer

## Source of truth

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/231
- PRD state: approved (`status:approved`); CEO reviewed 2026-07-14.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-231`
- Branch: `prd/native-claude-coms-peer-231`
- Memory: disabled for `@samfp/pi-memory`; no memory evidence used.

## Pre-edit status and scope

- `git status --short --branch` before editing: clean (`## prd/native-claude-coms-peer-231...origin/main`).
- Pre-existing dirty files: none.
- Context brief: explicit skip. No context-brief artifact was supplied or configured; checkpoint 1 is limited to the verified transport contract and mandatory source research. Repository/PRD/source inspection is recorded below.
- Operator continuation authorization: proceed through the approved #231 checkpoints and ordinary bounded verifier revisions; do not create a PR, merge, deploy, approve, trade, or backtest.

Allowed: runtime-neutral contract documentation, a small native adapter, opt-in native launch wiring, role prompts, focused tests, required run artifacts, and bounded local interop evidence.

Forbidden: changing `pi-coms-local` protocol/framing/registry, breaking Pi/Codex peers, API-key/cloud auth, weakening browser or human-control gates, secrets/transcripts over coms, GitHub mutation, PR creation, merge, deployment, trading, or backtesting.

Validation target: adapter and interop tests, `npm --prefix term-control-center run typecheck`, `npm --prefix term-control-center run test`, `npm --prefix term-control-center run build`, `PYTHONPATH=src python3 -m pytest tests/unit -q`, and `git diff --check`. The active checkpoint uses source-anchor verification plus `git diff --check` because it changes documentation only.

Stop condition: final verifier bug-check approval after the required steward review, or a true human escalation.

## Verifier checkpoints

1. Contract: runtime-neutral wire contract verified against installed `extensions/coms.ts`.
2. Adapter conformance and native↔Pi/Codex interop.
3. Native pane launch with generated strict MCP config, subscription/OAuth preflight, and legacy fallback.
4. Bounded await-loop inbound handling and visible native tool work.
5. Security and authority parity.
6. Steward hygiene review, verifier recheck, and final bug-check.

## Research consulted before implementation

1. `disler/pi-vs-claude-code`, 2026-07-17: its 2026-06 bridge is an unreleased one-shot `claude --print` launcher, not a coms client. Reuse only bounded spawn/cwd/output safeguards if needed; do not copy its hardcoded paths or permissive defaults.
2. Installed `pi-coms-local@0.1.1` `extensions/coms.ts`, 2026-07-17: confirmed registry fields and atomic write, LF-delimited 64 KiB socket framing, prompt/response/ping envelopes, ACK/NACK, name collision behavior, 10s ping, 30s heartbeat, and cleanup.
3. Claude Code CLI/MCP, 2026-07-17: use one generated `--mcp-config` plus `--strict-mcp-config`; require subscription/OAuth preflight; use active-turn bounded polling (maximum 30s) rather than autonomous inbound injection or preview Channels.

## Current checkpoint

Checkpoint 1 revision 2 resolved `V231-C1-001`, `V231-C1-002`, and `V231-C1-004`. Revision 3 is ready for verifier review and makes the final bounded framing correction for `V231-C1-003`.

## Changes made

- Added a runtime-neutral local coms wire contract from the installed `pi-coms-local@0.1.1` reference implementation.
- Recorded exact registry, naming, socket, framing, envelope, ACK/NACK, liveness, cleanup, and compatibility semantics.
- Corrected the reference tool surface to exactly `coms_list`, `coms_send`, `coms_get`, and `coms_await`; `coms_wait` is now explicitly an adapter-only PRD addition.
- Corrected the frame limit to the reference's exact accumulated decoded JavaScript UTF-16 code-unit check, including LF before first-line extraction. The contract now states that no raw-byte limit is conformant without separately negotiated versioning.
- Corrected liveness to distinguish PID-present registry entries, independent ping reachability, active heartbeat timestamp rewrites, and UI stale counters.
- Kept the shared contract runtime-neutral; the Claude-specific bounded-poll/MCP/auth decision remains only in this handoff's dated research evidence.
- Defined the adapter-only `coms_respond` tool without changing the wire protocol.
- Made the existing missing `sender_cwd` enforcement explicit as an AgentOps adapter/workflow security overlay.

## Touched files

- `docs/coms-wire-contract.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/review-request-r1-checkpoint-1.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/review-request-r2-checkpoint-1.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/review-request-r3-checkpoint-1.json`

## Acceptance criteria covered

- AC-1: covered by the new verified wire-contract document.
- AC-9: decision and rationale recorded for bounded await-loop polling.
- AC-2 through AC-8 and AC-10: pending later checkpoints and tests.

## Validation

- `python3` source-anchor check against installed `extensions/coms.ts` for registry, naming, framing, handlers, and heartbeat anchors — passed.
- `git diff --check` plus direct untracked-file whitespace checks — passed after revision 2.

## Findings addressed

- `V231-C1-001`: reference tools enumerated exactly; `coms_wait` is adapter-only.
- `V231-C1-002`: provider/launcher-specific policy removed from the shared contract.
- `V231-C1-003`: reference frame measurement documented as accumulated decoded JavaScript code units including LF before extraction; mandatory raw-byte hardening removed because it would reject reference-accepted multibyte frames.
- `V231-C1-004`: registry PID pruning, ping reachability, active heartbeat `started_at` refresh, and UI staleness documented separately.

## Skipped checks

- Typecheck, unit tests, build, Python test suite, and interop smoke are deferred: checkpoint 1 changes documentation only; later implementation checkpoints will run them.

## Known risks and cleanup

- Pi's reference transport does not itself validate `sender_cwd`; the documented security overlay must be enforced by the native adapter and existing Pi role/worktree contract without changing Pi protocol behavior.
- The installed reference still uses Pi's `--name`; the native adapter must use a distinct option such as `--cname` to avoid Pi CLI ownership drift.
- No generated output, secrets, raw transcripts, or cleanup candidates were created.
- Bounded standards exception: none.

## Checkpoint 2 implementation

- Added `term-control-center/server/comsAdapter.ts`: a local registry/socket adapter with atomic registry writes, 30-second heartbeats, LF JSON framing, ACK/NACK/ping handling, same-worktree send/receive checks, one outbound request guard, inbound queue, explicit response delivery, cleanup, and stale-socket probing.
- Added `term-control-center/server/comsMcp.ts`: a stdio MCP server exposing `coms_list`, `coms_send`, `coms_get`, `coms_await`, adapter-only `coms_wait`, and `coms_respond`; stdout remains MCP-only.
- Added focused adapter and MCP-stdio tests plus pinned production MCP SDK dependencies.
- Researcher layout consult (2026-07-17): use the existing flat `term-control-center/server` and `tests` layout, not `pi-packages`; use production `@modelcontextprotocol/sdk@1.29.0` with `zod` and a stdio transport.

### Checkpoint 2 validation

- `cd term-control-center && node --import tsx --test tests/comsAdapter.test.ts tests/comsMcp.test.ts` — passed (4 tests).
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build:server` — passed.
- Historical revision-1 receipt: `npm --prefix term-control-center run test` had 575 passes and 20 failures. It is superseded by the revision-3 receipt below; do not interpret its earlier all-`node-pty` classification as current evidence.
- Live Pi→native MCP smoke registered `native-smoke-231` in the current Pi pool and the MCP client received/responded to the request, but Pi `coms_await` timed out three times. The adapter inserted a bounded response delay to avoid Pi's post-ACK pending-registration race, but the response remains unobserved by the Pi sender. This was superseded by checkpoint-2 revision 2 below.

## Checkpoint 2 revisions 2–3 — revision 3 pending verifier review

### Pre-edit status and bounded scope

- `git status --short --branch` before this revision recorded the expected checkpoint-1/2 dirty scope: package manifest/lock changes; the #231 run folder; `docs/coms-wire-contract.md`; adapter/MCP sources; and focused tests. No unrelated product files were edited. The generated `claude-cp2-revision` run subfolder was removed during revision-3 artifact cleanup.
- The canonical issue read was attempted with the required `gh issue view ... --json` command, but GitHub GraphQL rate limiting blocked it. The operator-supplied issue reference, existing approved handoff, and verifier report remain the local source evidence; no GitHub mutation was performed.
- Allowed paths: checkpoint-2 adapter/MCP implementation, focused conformance tests, dependency manifest/lock, and #231 review artifacts. Forbidden paths/actions remain unchanged: Pi protocol implementation, launch/routing/deployment, secrets/transcripts, GitHub mutation, PR, merge, deployment, approval, trading, or backtesting.
- Stop condition: checkpoint 2 is not complete until this revision receives verifier approval. No next checkpoint is started.

### Findings resolved

- `V231-C2-001`: MCP correlation schemas now accept a bounded non-empty protocol string, so Pi ULID `msg_id`s work with `coms_get`, `coms_await`, `coms_wait`, and `coms_respond`; the unsupported response delay was removed. A live Pi → native MCP await/respond → Pi await smoke passed.
- `V231-C2-002`: `send()` reserves its outbound slot and pending reply before its first await and rolls both back on transport failure. Focused tests cover same-tick concurrent rejection and an immediate response.
- `V231-C2-003`: nested sends derive `hops` from the active inbound request, enforce the ceiling, and clear that context after response. Focused tests cover propagation, ceiling rejection, and reset after response.
- `V231-C2-004`: startup resolves live registry collisions to `name2`, `name3`, and so on, and cleanup uses the resolved registry path. Focused coverage verifies collision isolation.
- `V231-C2-005`: `coms_list` mirrors same-pool `project` and `include_explicit`, returns the configured project, and fails closed for a foreign project; targets resolve by same-pool name or session ID. Focused adapter/MCP coverage verifies each behavior.
- `V231-C2-006`: registry reads remove `ESRCH` entries, heartbeat recreates a deleted agents directory behind an error boundary, and heartbeat queue depth counts all unresolved inbound requests. Focused coverage verifies pruning, self-heal, queue depth, and socket cleanup.
- `V231-C2-007`: replaced stale interop evidence with one sanitized current two-direction result and added deterministic framing, guard, lifecycle, MCP, and interop coverage; the full-suite receipt now distinguishes 18 environment-blocked files from two unrelated baseline assertion failures.
- `V231-C2-008`: startup resolves the configured worktree and fails closed when the local cwd is outside it; accepted-inside and rejected-outside startup coverage is focused and deterministic.
- `V231-C2-009`: grouped prompt-envelope options to keep the method parameter count bounded, removed the unused test helper, and kept every changed module below 300 lines.
- `V231-C2-010`: removed the generated `claude-cp2-revision/` delegate/transcript/provider/launch artifacts; only sanitized durable run evidence remains.

### Revision-2 touched files

- `term-control-center/package.json`
- `term-control-center/package-lock.json`
- `term-control-center/server/comsAdapter.ts`
- `term-control-center/server/comsMcp.ts`
- `term-control-center/tests/comsAdapter.test.ts`
- `term-control-center/tests/comsAdapter.conformance.test.ts`
- `term-control-center/tests/comsMcp.test.ts`
- `term-control-center/tests/comsTestFixture.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/interop-smoke-result.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/coder-handoff.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/review-request-r2-checkpoint-2.json`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/review-request-r3-checkpoint-2.json`
- Removed: `dev-plans/agentops/coder-verifier-workflow/runs/issue-231-native-claude-coms/claude-cp2-revision/`

### Acceptance coverage and validation

- AC-2/AC-10: registry collision, pruning, heartbeat self-heal/queue depth, explicit discovery, session targeting, cleanup, and framing have deterministic coverage.
- AC-3/AC-5/AC-7: native↔Pi response completion, ULID correlation, cwd guards, one-outbound behavior, and hop limits have deterministic coverage plus live bidirectional scratch-pool evidence.
- `cd term-control-center && node --import tsx --test tests/comsAdapter.test.ts tests/comsAdapter.conformance.test.ts tests/comsMcp.test.ts` — passed, 21 tests.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build:server` — passed.
- Live scratch-pool smoke — passed in both directions; details are sanitized in `interop-smoke-result.json`.
- `npm --prefix term-control-center run test` — 592 passed and 20 failed: 18 files cannot load `node-pty` because dependencies were installed with `--ignore-scripts` and its native binary is absent; two unrelated baseline assertions also fail (`coworker launcher mounts as a distinct floating surface...` and `fix-loop launch wiring carries selected findings...`). No unrelated product code was changed.
- `git diff --check` — passed.

### Skipped checks, risks, cleanup, and standards

- Python tests and client build are outside this server-only checkpoint. Steward review and final bug-check are premature until checkpoint 2 approval.
- The full suite is not passing: 18 failures are environment-blocked by the absent `node-pty` binary and two are unrelated baseline assertion failures. Neither category was suppressed or treated as passing.
- Temporary live-smoke processes closed cleanly; their registry files and sockets were absent after cleanup. No generated runtime files, secrets, prompts, replies, or raw transcripts were retained.
- Context brief: explicit skip remains valid; the operator supplied the issue, handoff, verifier report, contract, standards, and bounded findings.
- Canonical standards: the focused test helper separates local socket/filesystem setup from assertions, all changed code/test modules are below 300 lines, errors fail closed at transport boundaries, and no standards exception is requested.
- Pre-verdict risk: checkpoint 2 awaited independent verifier review; the recorded verdict below resolves this checkpoint.

### Checkpoint-2 revision-3 verdict

- Verifier compact verdict: `approved`, checkpoint `2 - Adapter conformance + interop`, revision `3`, zero open findings, and no bug-check applicable.
- Per the approved-verdict rule, the full verifier report was not read after this response.
- Checkpoint 2 is approved. This operator authorization ends at checkpoint 2; no checkpoint-3 implementation, PR, merge, deployment, approval, trading, or backtest action was started.

## Checkpoint 3 — native Claude pane launch

- Operator continuation authorization: the operator explicitly authorized checkpoint 3 only after checkpoint-2 approval. Do not begin checkpoint 4 before an approved checkpoint-3 verdict.
- Pre-edit status (2026-07-17): `## prd/native-claude-coms-peer-231...origin/main`; preserve the approved checkpoint-1/2 dirty scope: `term-control-center/package.json`, `term-control-center/package-lock.json`, `docs/coms-wire-contract.md`, the #231 run folder, `term-control-center/server/comsAdapter.ts`, `term-control-center/server/comsMcp.ts`, and their focused tests. No unrelated dirty files were present.
- Allowed paths: `term-control-center/server/launchPlan.ts`, `term-control-center/server/launchProfiles.ts`, any small launch-only helper under `term-control-center/server/`, focused `term-control-center/tests/launchPlan.test.ts` and `launchProfiles.test.ts`, `scripts/agentops/` native-Claude launch wrapper, and this run folder's revisioned artifacts/handoff. Existing browser/MCP launch helpers may be reused without changing their security policy.
- Forbidden paths/actions: `pi-coms-local` protocol or extension, unrelated product/UI/routes/navigation/deployment, browser allowlist or human-control gates, shared contract semantics, secrets/transcripts, GitHub mutation, PR, merge, deploy, approval, trade, or backtest.
- Required implementation: a profile-selectable `native-claude` pane runtime that `exec`s Claude Code in the term-control PTY; per-launch generated MCP config containing `coms-mcp` plus existing eligible browser/codebase servers; `--strict-mcp-config`; subscription/OAuth-only preflight that rejects API-key/cloud auth; and unchanged `claude-agent` legacy profiles as the opt-in fallback.
- Validation: focused launch-profile/launch-plan tests; `npm --prefix term-control-center run typecheck`; `npm --prefix term-control-center run build:server`; `npm --prefix term-control-center run test` with failures accurately classified; `git diff --check`; native wrapper shell syntax; and a mocked native-Claude launch/preflight smoke that records no auth token or raw output.
- Verifier acceptance: native-selected profile launches a first-class Claude CLI pane rather than Pi or `claude_agent`; generated config has only expected MCP servers including `coms-mcp` and is passed with strict mode; authenticated subscription/OAuth is required and API/cloud variables fail closed; browser config/gates remain unchanged; legacy `claude-agent` plan is unchanged and selectable; invalid native config fails before spawn.

### Checkpoint-3 revision 1 implementation

- Added the opt-in `native-claude` model-profile runtime. Default Claude profiles remain `claude-agent`, so the existing Pi `claude_agent` delegation path remains the legacy fallback.
- Native profiles launch `scripts/agentops/claude-native.sh` as the pane process. The wrapper performs subscription/OAuth-only preflight, rejects API-key and cloud-provider auth variables, requires one existing strict MCP config with the local `coms-mcp` server, exports the same worktree-local coms identity variables, then `exec`s `claude` directly in the visible term-control PTY.
- Native launch plans generate one MCP config in the task artifact directory. It always includes the compiled local `coms-mcp`; codebase-memory and Chrome DevTools entries are included only under the unchanged existing eligibility rules. Native arguments include `--mcp-config <generated-path>` and `--strict-mcp-config` and do not contain `--approve`, a Pi wrapper, or `claude_agent` delegation.
- Native-only launch avoids Pi trust provisioning; the interactive native Claude pane retains its own visible workspace/permission flow. Mixed launches retain the existing Pi trust evidence for Pi panes.
- Browser environment, allowlist, human-control checks, and Browser QA readiness checks are reused unchanged for native browser roles.

### Checkpoint-3 revision-1 validation

- `bash -n scripts/agentops/claude-native.sh` — passed.
- `cd term-control-center && node --import tsx --test tests/launchProfiles.test.ts tests/launchPlan.test.ts tests/nativeClaudeLauncher.test.ts` — passed, 38 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed; confirmed the generated local MCP target is `term-control-center/build/server/comsMcp.js`.
- `npm --prefix term-control-center run test` — blocked, accurately classified: 597 passed and 20 failed; 18 test files fail to load the absent `node-pty` native binary, and two pre-existing unrelated assertions fail (`coworker launcher mounts as a distinct floating surface and stacks above completion center on mobile`; `fix-loop launch wiring carries selected findings into task details`). The five new focused tests increased the passing count without adding failures.
- `git diff --check` — passed.

### Checkpoint-3 revision-1 files and review state

- Checkpoint-3 implementation: `scripts/agentops/claude-native.sh`, `term-control-center/server/launchPlan.ts`, and `term-control-center/server/launchProfiles.ts`.
- Checkpoint-3 tests: `term-control-center/tests/nativeClaudeLauncher.test.ts`, `term-control-center/tests/launchPlan.test.ts`, and `term-control-center/tests/launchProfiles.test.ts`.
- Durable artifacts: this handoff and `review-request-r1-checkpoint-3.json`. No raw auth output, token, prompt, response, browser storage, or transcript was retained.
- Known risk: the local `coms-mcp` process target is generated from the server build output, so normal native launch requires the existing server build step; the wrapper fails closed before Claude spawn if that target is absent.
- Standards exception: none. The native wrapper is a small explicit process/auth boundary; TypeScript changes remain within existing flat launch modules and all changed implementation modules remain below 300 lines.
- Current status: checkpoint 3 revision 1 is ready for verifier review. Checkpoint 4 has not started.

### Checkpoint-3 revision-2 fixes

- `V231-C3-001`: the native wrapper now fails closed when `claude auth status --text` exits nonzero, even if its output contains a subscription marker; focused wrapper coverage proves the rejected status path.
- `V231-C3-002`: extracted one runtime-neutral browser security prompt applied to both native and delegated browser/frontend Claude roles. It retains the dedicated-session, no-separate-profile, human-control hold, allowlisted local/preview navigation, fail-closed navigation, and browser-storage/token non-exfiltration rules; legacy role-specific Chrome targeting wording remains intact.
- `V231-C3-003`: the wrapper validates the exact generated `coms-mcp` shape: current Node executable, exactly the current worktree's `term-control-center/build/server/comsMcp.js`, and an existing target. Focused tests cover both accepted local and rejected substituted targets.
- `V231-C3-004`: codebase MCP availability is derived from the generated MCP config plus enabled codebase memory rather than the legacy runtime label. Native prompts now advertise installed codebase tools.
- `V231-C3-005` and `V231-C3-006`: moved native launch-plan cases out of the oversized legacy `launchPlan.test.ts` into focused `nativeClaudeLaunchPlan.test.ts`; wrapper setup/assertions are small helpers.
- `V231-C3-007`: grouped the model-profile factory inputs into `ProfileInput`, reducing the changed constructor surface to one parameter.

### Checkpoint-3 revision-2 validation

- `bash -n scripts/agentops/claude-native.sh` — passed.
- `cd term-control-center && node --import tsx --test tests/frontendBrowserLaunch.test.ts tests/launchProfiles.test.ts tests/launchPlan.test.ts tests/nativeClaudeLaunchPlan.test.ts tests/nativeClaudeLauncher.test.ts` — passed, 42 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed.
- `npm --prefix term-control-center run test` — blocked, 597 passed and 20 failures: 18 absent-`node-pty` native-binary file-load failures plus the two unchanged unrelated baseline assertions (`coworker launcher mounts as a distinct floating surface and stacks above completion center on mobile`; `fix-loop launch wiring carries selected findings into task details`). The 20 failures are unchanged from the approved checkpoint-2 baseline; checkpoint-3 focused cases pass.
- `git diff --check` — passed.

### Checkpoint-3 revision-2 files and status

- Added `term-control-center/server/delegationPrompts.ts` and `term-control-center/tests/nativeClaudeLaunchPlan.test.ts` to the allowed checkpoint-3 scope; the former is the narrow shared launch-prompt boundary required to preserve existing browser gates for native panes, and the latter keeps native tests out of the oversized baseline module.
- Revisioned artifacts: `review-request-r1-checkpoint-3.json` remains immutable; `review-request-r2-checkpoint-3.json` records this bounded recheck. No raw auth status output, secrets, prompts, browser data, or transcripts were retained.
- Standards exception: none. Changed source and focused test modules remain below 300 lines; native-only generated config and auth failures remain fail closed.
- Checkpoint-3 revision-2 compact verifier verdict: `approved`; zero open findings; bug-check not applicable. Per the approved-verdict rule, the full verifier report was not read after this response.
- Current status: checkpoint 3 is approved. The operator authorized checkpoint 3 only; checkpoint 4 has not started.

## Checkpoint 4 — inbound await-loop and transparency

- Operator continuation authorization: the operator explicitly authorized checkpoint 4 only after checkpoint-3 approval. Do not begin checkpoint 5 before an approved checkpoint-4 verdict.
- Pre-edit status (2026-07-17): checkpoint-1/2/3 dirty scope remains exactly as recorded above, with the additional approved launch-prompt source and focused native launch tests. No unrelated dirty files were introduced.
- Allowed paths: `term-control-center/server/delegationPrompts.ts`, `term-control-center/server/launchPlan.ts`, focused native launch/prompt tests under `term-control-center/tests/`, and this run folder's revisioned artifacts/handoff.
- Forbidden paths/actions: Pi protocol/adapter behavior, browser allowlist or human-control gates, role authority/human gates, unrelated product/UI/routes/deployment, secrets/transcripts, GitHub mutation, PR, merge, deployment, approval, trading, or backtesting.
- Required implementation: chosen active-turn await-loop for native Claude peers, an explicit bounded startup task in the visible native pane, `coms_list → coms_await(timeout_ms: 30000) → native handling → coms_respond(msg_id)` behavior, clear non-fatal timeout/resume semantics, and no prompt-injection or auto-closing delegate mechanism.
- Validation: focused native launch/prompt tests, `npm --prefix term-control-center run typecheck`, `npm --prefix term-control-center run build:server`, full suite with classified blockers, and `git diff --check`.
- Verifier acceptance: native launch includes an initial standing-peer task and no nested Pi/tmux delegate; prompt requires same-pool discovery and 30-second bounded inbound await, explicit same-message response, no ping-pong response send, timeout resume, visible native tool work, preserved role/browser/human-control constraints, and a recorded await-loop-vs-injection decision.

### Checkpoint-4 revision-1 implementation

- Chosen inbound mechanism: active-turn native Claude await-loop, not #211 prompt injection. Rationale: the MCP adapter already supplies bounded inbound `coms_await` and explicit `coms_respond`; a 30-second timeout keeps the visible native Claude pane in control, avoids an unbounded autonomous/background loop, and preserves direct operator visibility of every native tool action.
- Native plans now set the Claude session display name to the role and pass an explicit initial standing-peer user task after the system prompt, so a first-class pane begins the peer workflow rather than merely opening at an empty prompt.
- The native-only system prompt directs `coms_list`, `coms_await` with `timeout_ms` 30000, non-fatal timeout/re-wait behavior, native visible handling, and exactly one `coms_respond` tied to the inbound `msg_id`. It forbids `coms_send` as a reply, prompt injection, background loops, cross-worktree handling, and authority expansion.
- Existing runtime-neutral browser safety and generic role/human-gate prompts remain composed into native prompts unchanged.

### Checkpoint-4 revision-1 validation

- `cd term-control-center && node --import tsx --test tests/nativeClaudeLaunchPlan.test.ts tests/launchPlan.test.ts tests/frontendBrowserLaunch.test.ts` — passed, 33 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed.
- `npm --prefix term-control-center run test` — blocked, 597 passed and the unchanged 20 failures (18 absent-`node-pty` load failures plus two unrelated baseline assertions).
- `git diff --check` — passed.

### Checkpoint-4 revision-1 files and status

- Touched checkpoint-4 source: `term-control-center/server/delegationPrompts.ts` and `term-control-center/server/launchPlan.ts`.
- Touched checkpoint-4 test: `term-control-center/tests/nativeClaudeLaunchPlan.test.ts`.
- Durable artifact: `review-request-r1-checkpoint-4.json`; no raw prompt, auth status, response, browser data, or transcript was retained.
- Standards exception: none. The selected loop is bounded at the native MCP boundary; no background worker, injection path, new transport API, or authority change was added.
- Current status: checkpoint 4 revision 1 is ready for verifier review. Checkpoint 5 has not started.

### Checkpoint-4 revision-1 verifier findings and human escalation

- `V231-C4-001`: pending bounded fix. The native prompt must explicitly resume `coms_await` after every completed response, not only after a timeout.
- `V231-C4-002`: pending bounded fix. The native prompt must map adapter/MCP inbound `request.msgId` to the `coms_respond` input field `msg_id` explicitly.
- Applied both prompt fixes and added focused assertions for the mapping and post-response re-wait behavior. Post-fix focused validation passed (33 tests), typecheck/build passed, `git diff --check` passed, and full suite remains 597 passed with the same 20 classified baseline failures.
- `V231-C4-003`: blocked on real native CLI runtime evidence. Two sanitized real subscription-native scratch runs (interactive direct session and `--print`) registered the MCP peer but returned no peer response; no output/transcript was read or retained. Per the dead-end rule, a focused Researcher consult was requested after the second failed response.
- Researcher consult, 2026-07-17: official Claude Code headless/MCP/CLI guidance recommends one bounded `claude -p --output-format stream-json --verbose --no-session-persistence` run with exact MCP tool allowlisting, filtering output in memory to tool-use booleans only; no deterministic MCP-client subcommand exists. Sources: https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/mcp, https://code.claude.com/docs/en/cli-reference.
- The recommended bounded headless diagnostic was run with the real native wrapper, strict generated config, exact coms tool allowlist, and in-memory-only stream filtering. The real CLI registered as a live peer, then exited before a sender could deliver the first request; no raw stream output, auth output, prompt, response, browser data, or transcript was retained. This is inconclusive per the researcher guidance and does not prove an adapter failure.
- **needs_human:** the real native Claude foreground pane must be opened by a human and, if Claude presents workspace/MCP trust or approval UI, the human must make that decision. Then manually observe one bounded `coms_list → coms_await → coms_respond` exchange and a second request after the response. Provide only a sanitized receipt (registered/timeout/first-response/second-response/cleanup booleans; no prompts, outputs, tokens, or transcript). This workflow may not auto-accept trust, use permission bypass, inject a prompt, or retain raw terminal output.
- Checkpoint 5 has not started.

### Checkpoint-4 revision-2 human receipt

- Pre-validation status (2026-07-17): the approved checkpoint-1/2/3 dirty scope remains unchanged; no unrelated files were introduced.
- The operator supplied a sanitized, human-visible native-pane receipt confirming: peer registration; one bounded timeout followed by re-wait; a first request response; a second request response after re-wait; visible native pane tool activity; cleanup; and that the operator made any workspace/MCP trust decision themselves.
- No prompt, response content, terminal output, correlation ID, auth detail, token, browser data, screenshot, or transcript was requested, received, or retained.
- The native CLI automation prohibition remains in force. Focused validation completed and checkpoint-4 revision-2 verifier review is next; checkpoint 5 remains unstarted and requires separate explicit operator authorization after checkpoint-4 approval.

### Checkpoint-4 revision-2 validation

- `cd term-control-center && node --import tsx --test tests/nativeClaudeLaunchPlan.test.ts tests/launchPlan.test.ts tests/frontendBrowserLaunch.test.ts` — passed (33 tests).
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed.
- `npm --prefix term-control-center run test` — blocked, accurately classified: 597 passed and 20 failed. Eighteen files fail at load time because the local `node-pty` native binary (`pty.node`) is absent; two unrelated baseline assertions fail (`coworker launcher mounts as a distinct floating surface and stacks above completion center on mobile`; `fix-loop launch wiring carries selected findings into task details`). The focused checkpoint-4 tests pass; no failure is represented as passing.
- `git diff --check` plus direct untracked-file trailing-whitespace check — passed.
- Revision-2 review scope is limited to `V231-C4-001`, `V231-C4-002`, and `V231-C4-003`: the first two were already bounded prompt/test fixes in the preserved checkpoint-4 scope; the third is discharged only by the sanitized human receipt above. No implementation change, native CLI retry, or checkpoint-5 work occurred for this revision.

### Checkpoint-4 revision-3 — V231-C4-004

- Replaced the two alternation-based prompt assertions in `term-control-center/tests/nativeClaudeLaunchPlan.test.ts` with independent assertions for same-pool discovery, bounded inbound await, timeout re-wait, `request.msgId` to `coms_respond.msg_id` mapping, exactly-once response, post-response re-wait, no `coms_send` reply, and no background-loop/prompt-injection path.
- No source prompt, runtime smoke, native CLI, security/authority behavior, or checkpoint-5 code changed.
- Re-ran the checkpoint-4 validation set: focused tests passed (33); typecheck passed; server build passed; full suite remains accurately blocked at 597 pass / 20 failures (18 absent-`node-pty` native-binary file-load failures plus the same two unrelated baseline assertions); `git diff --check` plus untracked trailing-whitespace check passed.
- `review-request-r3-checkpoint-4.json` is the immutable bounded recheck artifact.
- Checkpoint-4 revision-3 compact verifier verdict: `approved`, zero open findings, bug-check not applicable. Per the approved-verdict rule, the full report was not read after this response.
- The operator then explicitly authorized continued work after asking how much remains. This authorizes checkpoint 5 and the required steward/final-review workflow only; it does not authorize a PR, merge, deployment, GitHub mutation, approval, trading, backtesting, secret retention, or trust bypass.

## Post-checkpoint-4 Steward review

- Required Steward review returned `clean`: approved #231 files are correctly placed, run artifacts are revisioned and sanitized, expected ignored build/dependency artifacts are not retained scope, and no checkpoint-5 implementation artifact or cleanup action was found.
- No Steward cleanup or verifier recheck is required from this review. It does not replace the required checkpoint-5 verifier review or final verifier bug-check.

## Checkpoint 5 — security and authority parity

- Operator continuation authorization is active for this checkpoint after checkpoint-4 approval.
- Allowed scope: focused tests and the minimal existing adapter/native-launch/prompt source necessary to prove or repair same-worktree send/receive scoping, one-outbound/no-ping-pong behavior, browser allowlist/human-control preservation, role/human gate preservation, and no-secrets/transcript handling. Run artifacts remain allowed.
- Forbidden: Pi protocol changes, browser allowlist/human-control weakening, trust bypass, unrelated product/UI/routes/deployment, retained secrets/prompts/transcripts, GitHub mutation, PR, merge, deployment, approval, trading, or backtesting.
- Required validation: focused security/authority tests, typecheck, server build, full suite with exact classification, and `git diff --check`.
- Stop condition: checkpoint-5 verifier approval, then required final verifier bug-check approval. No PR action.

### Checkpoint-5 implementation and validation

- Kept the existing adapter same-worktree guards and one-outbound/no-ping-pong behavior unchanged; their deterministic conformance coverage remains part of this checkpoint.
- Added explicit native-peer prompt protection against sending secrets, credentials, tokens, browser storage, or raw transcripts over coms.
- Replaced the remaining loose native-browser security assertion with atomic checks for human-control hold, allowlisted local/preview navigation with fail-closed outside targets, browser-storage non-exfiltration, untrusted page content, Browser QA role/human gates, and no-secrets-over-coms.
- Added native wrapper coverage proving `--dangerously-skip-permissions` fails closed before Claude launch.
- `cd term-control-center && node --import tsx --test tests/comsAdapter.test.ts tests/comsAdapter.conformance.test.ts tests/nativeClaudeLaunchPlan.test.ts tests/nativeClaudeLauncher.test.ts tests/browserQaLifecycle.test.ts` — passed (35 tests).
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build:server` — passed.
- `npm --prefix term-control-center run test` — blocked, accurately classified: 597 passed and 20 failed. Eighteen files fail at load time because the local `node-pty` native binary (`pty.node`) is absent; two unrelated baseline assertions fail (`coworker launcher mounts as a distinct floating surface and stacks above completion center on mobile`; `fix-loop launch wiring carries selected findings into task details`). The focused checkpoint-5 suite passes; no failure is represented as passing.
- `git diff --check` plus direct untracked-file trailing-whitespace check — passed.
- `review-request-r1-checkpoint-5.json` is the immutable checkpoint review artifact. No raw transcript, prompt, response, auth output, token, browser data, or workspace/MCP trust action was retained or automated.

### Checkpoint-5 revision-2 — V231-C5-001

- The native wrapper now rejects `--permission-mode bypassPermissions` and `--permission-mode=bypassPermissions` before Claude launch, alongside the two pre-existing dangerous-skip flags. It leaves safe permission modes unchanged.
- Focused wrapper coverage independently checks rejection of all four bypass spellings and confirms a safe `--permission-mode plan` argument still reaches the native CLI invocation.
- `bash -n scripts/agentops/claude-native.sh` plus the 35-test focused security/authority suite — passed.
- Typecheck and server build — passed. Full suite remains accurately blocked at 597 pass / 20 failures (18 absent-`node-pty` native-binary file-load failures plus the same two unrelated baseline assertions). `git diff --check` plus untracked trailing-whitespace check — passed.
- `review-request-r2-checkpoint-5.json` is the immutable bounded recheck artifact.
- Checkpoint-5 revision-2 compact verifier verdict: `approved`, zero open findings, bug-check not applicable. Per the approved-verdict rule, the full report was not read after this response.
- All implementation checkpoints are approved. The required final verifier bug-check is next; no PR action is authorized.
- Final bug-check request attempt 1 received a non-JSON transport response, so no machine verdict could be recorded and no verifier report update was produced. No implementation, validation, or authority action occurred.

## Final bug-check revision 1 findings and revision 2 fixes

- `V231-FINAL-001`: extracted registry parsing into `term-control-center/server/comsWire.ts`; it validates required registry fields, safe registry names, and name-to-enumerated-filename correspondence before discovery. Dead-record pruning deletes only the enumerated in-directory registry file.
- `V231-FINAL-002`: added type-specific wire-envelope validation and exact ACK/PONG correlation/type checks before a send, response, or ping is considered delivered. Invalid acknowledgements now fail the call and retain inbound work when appropriate.
- `V231-FINAL-003`: startup now rolls back its bound server/socket on registry-write failure; adapter-owned inbound sockets are tracked and destroyed during close; peer connection/read paths use a bounded timeout; MCP startup closes the adapter if stdio connection setup fails.
- `V231-FINAL-004`: `term-control-center/README.md` now documents native-runtime opt-in, server-build and subscription/OAuth prerequisites, generated strict MCP config, standing-peer tools, the wire-contract link, and the unchanged legacy fallback.
- Added deterministic regression coverage in `term-control-center/tests/comsAdapter.final.test.ts` for traversal-safe registry handling, malformed typed envelopes, wrong acknowledgement IDs/types and outbound-slot recovery, post-bind startup rollback, bounded idle shutdown, and blackhole-peer liveness. Native launch tests also assert the durable README guidance.
- Validation: `bash -n` plus the focused adapter/MCP/native/browser suite passed (43 tests); typecheck, server build, and full client/server build passed (only existing Vite asset/chunk-size warnings); full Node suite is accurately blocked at 602 pass / 20 failures (18 absent-`node-pty` native-binary file-load failures plus the same two unrelated baseline assertions); `git diff --check` plus untracked trailing-whitespace check passed.
- `final-bug-check-request-r2.json` is the immutable final recheck artifact. No PR, merge, deployment, GitHub mutation, approval, trading, backtest, secret retention, transcript retention, or workspace/MCP trust bypass occurred.
- Final bug-check revision-2 compact verifier verdict: `approved`, zero open findings, `bug_check_status: passed`. Per the approved-verdict rule, the full report was not read after this response.

## Final status

- Checkpoints 1 through 5 are verifier-approved; the required Steward review is clean; final verifier bug-check passed.
- Post-final human authorization created and pushed commit `b117eef` and opened PR #241; advisory Kodus review was triggered. No merge or deployment occurred.

## Post-PR Kodus revision

- Kodus found `V241-K-001`: an outbound `coms_await` timeout discarded late peer replies and released the single-outbound slot before a peer response arrived.
- Kodus found `V241-K-002`: inbound socket reads had no deadline, permitting an idle local client to retain a descriptor until shutdown.
- `awaitReply` now returns timeout without discarding pending outbound correlation state; a late valid response completes `coms_get` and releases the outbound slot only on receipt.
- Inbound frame reads now use the existing bounded transport deadline and fail closed with a NACK.
- Added deterministic late-reply regression coverage. Focused adapter/MCP suite passed (26 tests); typecheck and server build passed. A full-suite run exceeded its 600-second harness timeout after `node-pty` was rebuilt for the separate local smoke; it is not represented as passing. `git diff --check` passed.
- Operator authorization covers commit, push, Kodus re-trigger, merge after a clean Kodus result, local-main refresh, and local deployment. No permission/trust bypass is authorized.

## Post-PR Kodus revision 2

- Kodus review of `7511b5a` completed with three distinct fixes requested: constrain registry and inbound prompt endpoints to the configured session-derived socket pool, bound/deduplicate unresolved inbound prompts, and add lifecycle expiry for unanswered outbound requests while retaining short-timeout late replies. It also requested logger-based heartbeat/MCP diagnostics; its duplicate logging comment is covered by the same change.
- The adapter now rejects off-pool endpoints for target send, liveness ping, and inbound prompt sender identities; it has a default 32-request unresolved inbound bound, duplicate message-ID rejection, and a default five-minute terminal outbound expiry that releases the outbound slot. Short `coms_await` timeouts still retain late responses until that lifecycle expiry.
- Diagnostics use the new local `server/logger.ts` abstraction without logging peer data or errors. `server/comsTransport.ts` holds bounded connection/frame helpers so the adapter remains below the project file-size limit.
- Regression coverage proves endpoint rejection, duplicate/capacity rejection, late-response retention, and terminal outbound-slot release. The focused adapter/MCP suite passed (28 tests); typecheck and server build passed; `git diff --check` passed. Full-suite status is unchanged from the prior documented harness limitation and is not represented as passing.
- Independent verifier revision-2 review requested two further bounded corrections: safe session identifiers plus endpoint-root proof to prevent traversal, and lifecycle expiry arming only after prompt ACK while preserving the immediate-response race registration.
- Session IDs now use the protocol-safe segment grammar in registry/envelope parsing, and endpoint validation independently requires the derived POSIX path to remain inside the configured sockets directory. New regressions prove traversal registry entries cannot be targeted and traversal inbound identities receive NACKs.
- Pending outbound correlation is still registered before delivery, but its expiry is armed only after ACK succeeds and only if no immediate response has completed it. A delayed-ACK regression proves the returned ID is pending before the post-ACK expiry runs.
- The Kodus logging finding `r3606062919` replaced the console-backed shim with the project-local diagnostics-channel logging facility (`getLogger('coms')`), which emits only level/scope/event records and no peer/error/prompt data.
- Focused adapter/MCP suite passed (29 tests); typecheck, server build, and `git diff --check` passed. Full-suite status is unchanged from the prior documented harness limitation and is not represented as passing.
- Next: independent verifier recheck, then commit/push and force Kodus re-review. No merge occurs until a clean completed Kodus review.
