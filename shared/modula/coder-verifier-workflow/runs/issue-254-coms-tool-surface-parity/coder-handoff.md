# Coder Handoff — Issue #254

## Authority and scope

- Canonical task: [Issue #254](https://github.com/hyperbotsx/agentops-harness/issues/254).
- PRD facts: the supplied project context brief, dated 2026-07-19; GitHub retrieval was rate-limited.
- Operator continuation authorization covers ordinary bounded implementation and review revisions only.
- Allowed: direct-Pi launch and wrapper plumbing, reusable bridge code, launch/prompt/bridge tests, maintained integration documentation, this issue-scoped run folder, and the human-authorized baseline test-runner repair in the current worktree.
- Forbidden: adapter, wire, or transport guard changes; installed caches; runtime state; generated MCP configuration; secrets; transcripts; deployment; and unrelated surfaces.
- Stop condition: final verifier bug-check approval. No PR, merge, deploy, GitHub mutation, trading, or backtest authority exists.

## Current checkpoint state

1. Architecture — approved.
2. Launch and prompt — approved.
3. Guard regression — approved; adapter, wire, and transport sources remain unchanged.
4. Literal runtime — approved after the required human trust attestation. The retained receipt records the earlier pre-attestation machine outcome only; do not rerun this checkpoint.
5. Guide and authority — approved at revision 5; final verifier bug-check passed.

## Delivered implementation

- Direct `pi` launches select named mode; delegated `claude-agent` launches select explicit harness-native compatibility; native Claude remains unchanged.
- The local bridge starts one existing `comsMcp` child, requires the literal six-tool inventory, verifies the requested role identity, and forwards tool calls without duplicating adapter or wire behavior.
- Named mode fails closed when prerequisites, connection, inventory, or identity verification fail. It does not silently load the compatibility extension.
- Direct-Pi prompts require pool confirmation, bounded inbound waiting, one `coms_respond` per inbound request, and wait resumption.
- `docs/agentops-coms-integration.md` documents runtime attachment, all six tool semantics, environment forwarding, immutable guards, fail-closed behavior, fallback precedence, and new-CLI wiring.

## Touched files

- `scripts/agentops/pi-agent.sh`
- `term-control-center/extensions/agentopsComsBridge.ts`
- `term-control-center/server/comsLaunchMode.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/delegationPrompts.ts`
- `term-control-center/tests/agentopsComsBridge.test.ts`
- `term-control-center/tests/agentopsComsLabel.test.ts`
- `term-control-center/tests/comsLaunchMode.test.ts`
- `term-control-center/tests/contextRenewal.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/coworkerGuard.test.ts`
- `docs/agentops-coms-integration.md`
- This issue-scoped run folder.

## Review and hygiene

- Steward reviewed placement and artifact hygiene: implementation and tests are under `term-control-center`, the wrapper is under `scripts`, the guide is under `docs`, and artifacts are confined to this run folder.
- No generated MCP configuration, runtime registry/socket data, raw peer content, or secrets are retained.
- The checkpoint-4 human gate is resolved and approved; earlier blocked states are historical only.
- Research confirmed that the pinned Pi version needs an extension for MCP client behavior and that the bridge must reuse the existing MCP server rather than implement another transport. The baseline-repair consult confirmed that fixture wrappers must `exec` their long-running child so PTY shutdown targets the child directly; no production lifecycle change is required.

## Validation

Passed:

- `bash -n scripts/agentops/pi-agent.sh scripts/agentops/claude-native.sh`
- `git diff --check`
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run build` (existing Vite warnings only)
- Focused bridge, mode, wrapper, launch, native, MCP, adapter, conformance, final, and context-renewal tests: 85/85.

Baseline repair outcome:

- Human decision (2026-07-19): reject the Issue #254-only `server.test.ts` timeout exception and authorize a baseline test-runner repair in this worktree.
- Test fixtures now `exec` their long-running child, preventing shell descendants from retaining the PTY after teardown. Test setup disables ambient browser-runtime and pipeline-refresh work that is unrelated to the assertions.
- `server.test.ts` completes 54/54 in 36.9 seconds; `coworkerGuard.test.ts` completes 2/2.
- The serial full suite completes: 867/871 tests pass; the four retained failures are unchanged baseline cases in `coworkerLauncher.test.ts`, `kodyReview.test.ts`, `launchProjectFallback.test.ts`, and `verificationSandbox.test.ts`. No timeout exception remains.
- The sanitized per-file manifest now records 106 completed test files and four baseline failures.

## Revision 2 validation

Passed:

- `git diff --check`
- Shell syntax checks
- Typecheck
- Bridge tests: 7/7, including cleanup-rejection shutdown coverage.

The guide and bridge updates are ready for verifier recheck. The per-file manifest now records command, base, timeout, exit status, counts, and classifications. `server.test.ts` has a separate proposed, unapproved timeout exception requiring human approval; it is not passing evidence.

## Revision 2 changes

- Documented `coms_send` and `coms_get` semantics alongside every other named tool.
- Ensured startup failure calls session shutdown even if child cleanup rejects, while preserving the original startup error.
- Reduced bridge-start parameters to a single focused context object and added cleanup-rejection coverage.
- Rewrote this handoff to remove runtime endpoint/registry detail and transport correlation metadata.

## Revision 5 validation repair

- Checkpoint 5 approved; verifier final bug-check passed.

- Updated stale profile and direct-Pi prompt expectations.
- Isolated server and coworker tests from ambient browser, model, and pipeline-refresh configuration.
- Made fixture wrappers replace themselves with their long-running child.
- Passed `git diff --check`, typecheck, `server.test.ts` (54/54), `coworkerGuard.test.ts` (2/2), and the serial suite (867/871; four documented unchanged baseline failures).

## Post-PR Kody fix

- Replaced bridge-only endpoint construction with one shared platform-aware helper used by the bridge and adapter.
- Added Windows named-pipe and bridge identity coverage.
- Passed typecheck, build, and focused bridge/adapter tests (36/36).
