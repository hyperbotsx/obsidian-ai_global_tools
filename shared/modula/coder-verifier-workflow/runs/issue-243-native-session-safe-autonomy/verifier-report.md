# Verifier Report — Issue #243

## Review history

### Revision 1 — Checkpoint 1: research and contract decision

- Reviewed revision: `2e80015f72b3fa5abeebd6967715674997afe540` plus the untracked checkpoint handoff.
- Scope: decision/research evidence only; no implementation reviewed.
- Verdict: `needs_human`.
- Rationale: the delivered decision is coherent and preserves the required boundaries, but canonical PRD #243 expressly requires security review and explicit human approval before any autonomy implementation. This is a true human gate, not a coder revision finding.

## Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical task, worktree, branch, and Project ID agree | Pass | Issue #243; `prd/native-session-coms-followup-243`; worktree root; `AGENTOPS_PROJECT_ID=agentops-harness` |
| Canonical PRD independently retrieved | Pass | REST-backed `gh api repos/hyperbotsx/agentops-harness/issues/243` succeeded; the coder's GraphQL `gh issue view` failure does not prevent independent verification |
| Global permission bypass rejected | Pass | PRD non-goals/forbidden actions; handoff scope controls; native wrapper rejects bypass flags |
| Option B is explicit and minimal | Pass with recorded qualifier | Native Claude has named MCP reply tools; the installed Pi extension auto-emits the correlated response from the normal assistant turn. “Codex” here means the AgentOps Codex pane launched through Pi, not arbitrary stock Codex CLI |
| Legacy delegated-Claude bypass path is bounded | Pass | Handoff marks it separate/out of scope; `delegationPrompts.ts` confirms it remains distinct from `claude-native.sh` |
| Same-pool/worktree and wire safeguards remain required | Pass | No code changed; handoff defers conformance proof to the post-approval contract checkpoint |
| Safe-autonomy implementation authority exists | Blocked | The PRD and context brief require security review and explicit human approval before policy/launcher implementation |
| Research is current enough for this decision | Pass with recorded qualifier | Researcher recheck dated 2026-07-18; installed Claude Code is 2.1.195, so settings/worktree resolution is version-sensitive and is not a durable kill-switch contract |
| KISS review | Pass / code not applicable | The only coder artifact is a 59-line handoff. No functions, parameters, nesting, comments, or dead code were introduced; file-size and artifact clarity are within limits |

## Research relied upon

A bounded Researcher validation was performed while the coder was awaiting review. Summary only:

- The installed native MCP exposes explicit inbound await/respond tools, while `pi-coms-local@0.1.1` exposes its existing tool set and emits the inbound correlated response when the assistant turn ends. This supports option B without adding another Pi tool surface.
- The mapping applies to AgentOps Codex panes launched through `pi-agent.sh`; it is not a claim about arbitrary stock Codex CLI sessions.
- Claude permission/settings hot reload does not prove cancellation of already-running effects. Installed Claude Code 2.1.195 also differs from newer documented worktree settings resolution, reinforcing the need for an AgentOps-owned per-worktree policy checked immediately before each action.
- Native launcher bypass rejection and legacy delegated `bypassPermissions` are separate paths.
- Option B still requires post-approval negative conformance tests before it can be called security-validated.

Sources checked or cited on 2026-07-18:

- <https://docs.anthropic.com/en/docs/claude-code/settings>
- <https://docs.anthropic.com/en/docs/claude-code/hooks#pretooluse>
- <https://developers.openai.com/codex/guides/agents-sdk>
- <https://developers.openai.com/codex/mcp>
- <https://github.com/giovani-junior-dev/pi-coms-local>
- Local installed adapter, MCP, launcher, delegation prompt, and Pi extension sources.

## Findings

No coder-remediable findings are open for checkpoint 1.

The blocking condition is the PRD-mandated security/human approval. That approval must define the permitted routine-action taxonomy, per-worktree kill-switch location and revocation semantics, sanitized audit fields/retention, always-gate enforcement, and the bounded option-B mapping before checkpoint 2 begins.

## Validation Receipt

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 1 — research and contract decision
- **Decision:** needs_human
- **Final review:** no
- **Acceptance criteria reviewed:** fresh Claude/Pi/Codex research; explicit rejection of global skip-permissions; minimal native↔harness-native contract selection; same-pool/worktree preservation; deterministic delayed-reply design retained for later validation; legacy delegated bypass path explicitly excluded; required security/human gate honored.
- **Reviewed files/surfaces:** checkpoint handoff; canonical issue #243; project context brief; `docs/coms-wire-contract.md`; `scripts/agentops/claude-native.sh`; `term-control-center/server/comsMcp.ts`; `term-control-center/server/delegationPrompts.ts`; installed `pi-coms-local` response handler; Agent Engineering Standards Pack v1 verifier and exception guidance.
- **Commands/results:**
  - `git status --short --branch` — expected untracked checkpoint run directory only.
  - `git rev-parse HEAD` and `git merge-base HEAD origin/main` — both `2e80015f72b3fa5abeebd6967715674997afe540`.
  - `gh api repos/hyperbotsx/agentops-harness/issues/243 --jq ...` — passed; canonical title/state retrieved.
  - `claude --version` — `2.1.195`.
  - `git diff --check` — passed for tracked changes; no tracked implementation diff exists.
  - handoff trailing-whitespace check — passed.
  - source inspection of named MCP tools, Pi automatic response handler, native bypass rejection, and legacy delegation mode — passed.
- **Skipped checks/reasons:** typecheck, build, unit/conformance tests, live delayed-reply smoke, Steward final review, and bug-check were not run because no implementation exists and the mandatory approval gate has not been satisfied.
- **Edge cases:** arbitrary stock Codex must not be conflated with AgentOps Codex-through-Pi; settings resolution varies by Claude version; hot reload cannot be treated as in-flight cancellation; option B needs negative isolation/framing/duplicate/hop tests; late reply and deliberately delayed responder behavior remain unproven at this checkpoint.
- **Regression risks:** implementing before approval; treating repository settings as the kill switch; silently expanding option B beyond AgentOps panes; claiming wire equivalence proves security overlay equivalence; accidentally changing the separate legacy bypass path.
- **Relevant canonical standards checklist summary:** the decision favors the smallest existing integration, explicit runtime boundaries, fail-closed configuration, fresh evidence for volatile tooling, deterministic later tests, secret-free observability, and a bounded human-reviewed security exception process. No standards source was copied or forked.
- **Findings:** none coder-remediable; one mandatory human/security gate remains.
- **Required follow-up:** security reviewer and human operator must explicitly approve the bounded autonomy design and option-B implementation scope. The approval record must define routine actions, kill switch/revocation, audit rules, always-gates, and legacy-path exclusion.
- **Next actor:** human/security reviewer.
- **Forbidden-action confirmation:** no PR creation, GitHub mutation, push, merge, deployment, approval, trading, backtest, secret access, permission bypass, or coder-owned-file edit by the verifier occurred.
- **Checkpoint compliance/deviation:** checkpoint 1 correctly stops before implementation and complies with the PRD's authority boundary. The role skill's referenced repository report template is absent on the baseline branch; this report follows the transport contract and operator-required receipt fields directly, with no scope or safety deviation.

## Checkpoint 2 review — revision 1

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the checkpoint-2 working tree.
- **Scope:** project-scoped autonomy policy, native launcher/settings enforcement, audit, path/Bash/MCP classification, and focused tests only.
- **Verdict:** `revision_requested`.
- **Authorization evidence:** the durable handoff records operator policy decisions and security approval dated 2026-07-18. Review is limited to that approved scope; the approval does not override canonical always-gate requirements.

### Atomic acceptance checks

| Check | Result | Evidence |
| --- | --- | --- |
| Missing/malformed/revoked policy denies | Pass in focused unit path | `readPolicy()` and focused negative tests |
| Always-gate classifications deny before policy read | Pass for directly classified top-level tools | `autonomyGates.ts`; focused tests |
| Policy cannot encode always-gate classes | Pass | strict Zod enum and negative test |
| Policy state is private, trusted, atomic, and symlink-safe | Fail | V243-C2-005 |
| Revocation survives setup/relaunch and is session-bound | Fail | V243-C2-006 |
| Enforcement/settings/audit are outside autonomous write authority | Fail | V243-C2-001 |
| Verification commands cannot transitively bypass gates | Fail | V243-C2-002 |
| Secret/credential access remains gated | Fail | V243-C2-003 and V243-C2-004 |
| Caller settings and settings-derived bypass are rejected exactly | Fail | V243-C2-007 |
| Audit fields are sanitized and rotation is bounded | Partial | Record shape/rotation tests pass, but the audit file is autonomously writable under V243-C2-001 |
| Literal `coms-mcp` method classification | Pass | exact prefix/method set and focused tests |
| `.git`, root escape, and escaping symlink edits deny | Pass for tested inputs | path classifier and focused tests |
| Legacy delegated bypass remains unchanged/out of scope | Pass | no legacy delegation diff |
| Installed-Claude settings-isolation canary exists | Fail | V243-C2-008 |
| Handoff evidence is current and unambiguous | Fail | V243-C2-009 |
| KISS limits are met | Fail | V243-C2-010; other changed files/functions/parameters/nesting/comments/dead-code checks pass |

### Research relied upon

A bounded Researcher validation was performed on 2026-07-18 against installed Claude Code 2.1.195 and current Anthropic hook/settings guidance. Summary only:

- A matching `PreToolUse` command hook is invoked for each Claude tool call, but Claude provides no hashing or immutability guarantee for the hook executable or its policy inputs.
- Current documentation does not establish hot reload for a file supplied through CLI `--settings`; revocation therefore must come from the independently re-read policy input.
- `PreToolUse` gates the top-level Bash tool call, not subprocesses. Unsandboxed npm/node commands can execute workspace-controlled code with user authority and cannot preserve an unbypassable deploy/push/external-send/secrets boundary.
- The safe boundary must keep hook/control-plane files outside autonomous write authority and keep executable verification commands gated until a separately approved no-network/no-credentials sandbox exists.

Sources: <https://docs.anthropic.com/en/docs/claude-code/hooks#pretooluse> and <https://docs.anthropic.com/en/docs/claude-code/settings>.

### Open findings

#### V243-C2-001 — Critical — Autonomy can overwrite its own control plane

- **Evidence:** `launchPlan.ts:162-166` places policy/settings/audit under `<artifactRoot>/autonomy`; `autonomyPaths.ts:38-39` allows writes anywhere under the artifact root; `nativeClaudeSettings.ts:19-26` executes the hook and imports from the writable worktree. Independent evaluation returned `allow_workspace_edit` for the live policy file, generated settings file, and compiled `pretoolHook.js`. The audit log is in the same writable state directory.
- **Affected paths:** `term-control-center/server/{nativeClaudeSettings,autonomyPaths,pretoolHook,launchPlan}.ts` and compiled enforcement modules.
- **Bounded action:** move/snapshot the hook, imported enforcement modules, policy, settings, and audit into an owner-only control-plane root outside every autonomous read/write artifact root, or add an independently enforced protected-root boundary that covers the entire executable/import graph and state directory. Add negative tests for Write/Edit/MultiEdit/NotebookEdit against policy, settings, audit, hook, and imported enforcement modules.
- **Decision impact:** the always-gate and audit boundaries are currently self-modifiable; checkpoint cannot pass.

#### V243-C2-002 — Critical — Unsandboxed verification commands bypass always-gates

- **Evidence:** `autonomyGates.ts:84-89` auto-allows `npm run`, `npm test`, and arbitrary workspace test paths through `node --import tsx --test`. Those commands execute agent-writable package scripts/JavaScript and unrestricted child processes; the hook does not inspect subprocesses. The broad git pattern also permits path/output options without root validation.
- **Affected path:** `term-control-center/server/autonomyGates.ts` and its tests.
- **Bounded action:** remove npm/node/build/test execution from auto-allow and keep it human-gated until a separately approved OS/container sandbox denies network, credentials, sensitive sockets, and control-plane paths. Narrow any retained read-only git forms to explicit safe arguments and worktree-contained paths. Add adversarial package-script, arbitrary test-file, `--prefix` escape, git outside-read, and git output-path tests.
- **Decision impact:** direct always-gates pass, but transitively equivalent actions remain possible. If unsandboxed test/build autonomy remains a requirement, escalate for PRD/security re-decision rather than accepting it as residual risk.

#### V243-C2-003 — High — Arbitrary inherited credentials reach the native session

- **Evidence:** PTY/tmux launch merges full `process.env`; `claude-native.sh:106-108` unsets only a fixed list. A verifier fixture with dummy `SOME_SERVICE_SECRET` reached the final fake Claude process (`SECRET_PRESENT=yes`), despite `isCredentialKey()` classifying that name as sensitive.
- **Affected paths:** `scripts/agentops/claude-native.sh`, `term-control-center/server/nativeClaudeSettings.ts`, and native launcher tests.
- **Bounded action:** apply the credential-name policy to the actual inherited environment immediately before `exec`, preserving only the subscription preflight material until preflight completes, then remove it too. Add an end-to-end wrapper test with arbitrary `_SECRET`, `_TOKEN`, `_PASSWORD`, private-key, auth-socket, and known provider names.
- **Decision impact:** the secrets always-gate and R5 credential-stripping condition are not met.

#### V243-C2-004 — High — Auto-read can access credential files

- **Evidence:** `autonomyGates.ts:24,42-44` makes Read/Grep/Glob/NotebookRead/LS candidates based only on root containment. Nothing rejects `.env`, credential/key files, auth config, or a broad Grep rooted above such files. Root containment is not a secret boundary.
- **Affected paths:** `term-control-center/server/autonomyGates.ts`, `term-control-center/server/autonomyPaths.ts`, and focused tests.
- **Bounded action:** define and test a conservative secret-path/content-scope deny before policy evaluation. Keep broad directory Grep/Glob/read operations human-gated when their result set cannot exclude sensitive files deterministically.
- **Decision impact:** acceptance criterion 6 and the non-negotiable secrets gate are not proved.

#### V243-C2-005 — High — Policy creation is non-atomic and writes through untrusted paths

- **Evidence:** `autonomyPolicy.ts:31-43` validates only the file and immediate parent when reading; `:75-89` calls `mkdirSync`/`writeFileSync` directly before trust validation. There is no atomic temporary file/rename or full ancestor check. A verifier fixture using a symlinked state directory wrote the policy into the symlink target before later returning `deny_policy_untrusted`.
- **Affected paths:** `term-control-center/server/autonomyPolicy.ts`, `term-control-center/server/nativeClaudeSettings.ts`, and tests.
- **Bounded action:** validate the full control-plane ancestry and ownership/modes before any write, reject symlinks, and create policy/settings atomically with private temporary files plus rename and final verification. Add world-writable ancestor, symlinked directory/file, existing-loose-file, interrupted-write, and mode tests.
- **Decision impact:** explicit security condition F2 is not implemented.

#### V243-C2-006 — High — Setup clears revocation and uses role as session identity

- **Evidence:** `nativeClaudeSettings.ts:21-26` always rewrites a fresh `revoked:false` policy and binds `session` to `input.role`. A verifier fixture revoked the policy, invoked setup again, and observed `revokedAfterRepeatedSetup:false`. A role such as `coder` is not a unique launch session.
- **Affected paths:** `term-control-center/server/nativeClaudeSettings.ts`, `term-control-center/server/autonomyPolicy.ts`, `term-control-center/server/launchPlan.ts`, and tests.
- **Bounded action:** bind policy to the real pane/session identifier, preserve an existing revoked state across plan regeneration/restart, and require an explicit operator-controlled re-enable operation. Test repeated plan resolution, restart, duplicate roles, and stale-session policy reuse.
- **Decision impact:** kill-switch persistence and per-session isolation are not met.

#### V243-C2-007 — High — Launcher accepts a non-hook command containing the expected path

- **Evidence:** `claude-native.sh:101` accepts any hook command whose string merely `includes(expected_hook)`. A generated settings fixture using `true # <expected-hook>` passed validation and launched Claude without invoking the hook. The wrapper also does not verify settings-file ownership/mode/symlink status.
- **Affected paths:** `scripts/agentops/claude-native.sh` and `term-control-center/tests/nativeClaudeLauncher.test.ts`.
- **Bounded action:** validate the exact settings schema, matcher, hook type, and exact safely quoted command; require one intended command and no competing permission/hook entries. Verify the settings file and hook executable/import graph are trusted owner-only regular files. Add substring/comment, extra-hook, alternate-mode, symlink, and loose-permission negatives.
- **Decision impact:** F1/R6 settings-derived bypass protection is bypassable.

#### V243-C2-008 — Medium — Required installed-Claude settings canary is absent

- **Evidence:** `nativeClaudeLauncher.test.ts:36-38,61-65` replaces Claude with a fake executable and asserts only forwarded arguments. It does not demonstrate that installed Claude 2.1.195 isolates user/project/local settings under `--setting-sources ''`, although the handoff claims R1-R7 addressed.
- **Affected paths:** native launcher validation evidence and `term-control-center/tests/nativeClaudeLauncher.test.ts`.
- **Bounded action:** add or record a sanitized, version-pinned installed-Claude canary that proves excluded setting sources cannot add an allow rule/hook. If automation would require an external model call, record it as a bounded human-operated local validation rather than treating the fake as proof.
- **Decision impact:** R2 remains an evidence gap and fails closed.

#### V243-C2-009 — Medium — Durable handoff is internally stale

- **Evidence:** the handoff still says implementation is blocked/pending approval, only research artifacts are allowed, no policy changes should exist, no tracked diff exists, and checkpoint 2's next action is to implement. Later sections say approval was granted and checkpoint 2 is already implemented. The touched implementation and current git status contradict the earlier/final status text.
- **Affected path:** `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/coder-handoff.md`.
- **Bounded action:** update status, authorization, scope, validation, risk, and next-action sections into one current record; retain checkpoint-1 history explicitly without presenting it as current state.
- **Decision impact:** operator-required evidence is ambiguous and cannot support approval.

#### V243-C2-010 — Medium — Changed file exceeds the repository KISS limit

- **Evidence:** `term-control-center/server/launchPlan.ts` is 306 lines after the change; baseline was 291. The repository limit is under 300 lines. Other changed files are under 300; changed functions remain under 20 lines with bounded parameters/nesting; no redundant comments or dead code were found.
- **Affected path:** `term-control-center/server/launchPlan.ts`.
- **Bounded action:** extract the cohesive native-autonomy environment/setup composition into the existing autonomy module or otherwise reduce `launchPlan.ts` below the limit without adding speculative layers.
- **Decision impact:** mandatory explicit KISS review fails.

## Validation Receipt — Checkpoint 2

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement
- **Decision:** revision_requested
- **Final review:** no
- **Acceptance criteria reviewed:** project/session scoping; missing/invalid/revoked default deny; kill switch; non-representable always-gates; launcher settings isolation; path/Bash/MCP classification; sanitized bounded audit; credential removal; F1-F5; R1-R7; focused validation; KISS.
- **Reviewed files/surfaces:** all eleven implementation/test/doc paths in the coder request; checkpoint handoff; canonical PRD/context brief; tmux/PTY environment merge; installed Claude 2.1.195 hook/settings behavior; current Agent Engineering Standards verifier/exception guidance.
- **Commands/results:**
  - `git status --short --branch`, `git diff --stat`, `git diff --name-status`, `git diff --check` — scope enumerated; tracked diff check passed; new files remain untracked.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `cd term-control-center && node --import tsx --test tests/nativeClaudeLaunchPlan.test.ts tests/nativeClaudeLauncher.test.ts tests/autonomyHook.test.ts` — 22 passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `claude --help` / `claude --version` — installed 2.1.195 exposes the relevant settings/source/mode flags.
  - Adversarial local fixtures — reproduced control-plane self-write allowances, symlink-following policy creation, revocation reset, arbitrary inherited-secret propagation, and substring settings validation bypass.
- **Skipped checks/reasons:** full suite was not rerun after the coder's 300-second timeout because focused review already found blocking security defects; full app build, checkpoint-3 coms conformance, live delayed-response smoke, Steward final review, and final bug-check are not applicable until checkpoint 2 passes.
- **Edge cases:** state-dir/file symlinks and loose ancestors; repeated plan generation/restart; duplicate role sessions; broad Grep over secret files; arbitrary npm scripts/test files; git output/outside paths; inherited unknown credential names; settings command comments/substrings; concurrent audit rotation; missing policy/audit writes.
- **Regression risks:** self-modified enforcement, silent kill-switch re-enable, credential disclosure, subprocess external sends/deploy/destruction, secret-file reads, untrusted settings substitution, broken audit evidence, and launcher complexity drift.
- **Relevant canonical standards checklist summary:** the implementation has useful narrow modules and deterministic focused tests, but it currently violates fail-closed control-plane ownership, secret isolation, explicit side-effect boundaries, deterministic trust/atomicity, and repository KISS limits. Security exceptions must be explicit, bounded, and human-reviewed; an unsandboxed subprocess exception cannot silently override the PRD's always-gate floor.
- **Findings:** V243-C2-001 through V243-C2-010 are open.
- **Required follow-up:** coder applies bounded fixes within the authorized scope. Keep verification execution gated unless a separately approved sandbox resolves V243-C2-002. Re-run focused negatives, typecheck, server build, diff checks, and refresh the durable handoff before re-requesting checkpoint 2.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, trade, or backtest; accessed no real secret; edited no coder-owned file; and used only dummy `/tmp` fixtures for adversarial validation.
- **Checkpoint compliance/deviation:** implementation stayed within the listed repository surfaces and did not change legacy delegation or coms transport, but checkpoint 2 materially deviates from approved F1/F2/R2/R5/R6 and the canonical always-gate/secret boundaries. No exception record authorizes those deviations.

## Checkpoint 2 re-review — revision 2

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the current working tree.
- **Verdict:** `revision_requested`.
- **Summary:** revision 2 materially improves control-state placement, top-level npm/node denial, path classification, atomic file replacement, settings command identity, and KISS placement. Focused validation passes. Several original security findings are only partially closed, the human-operated installed-Claude canary is still absent, and new repository-hygiene drift is present.

### Finding disposition

| Finding | Status at revision 2 | Evidence / remaining action |
| --- | --- | --- |
| V243-C2-001 | Open, partially remediated | Policy/settings/audit moved outside artifact root and `build/**` is protected, but the directly executed launcher remains auto-writable |
| V243-C2-002 | Open, partially remediated | npm/node/build/test now deny; raw host Git profiles can still execute inherited helpers and mutate optional metadata |
| V243-C2-003 | Open, partially remediated | uppercase credential families are removed; lowercase/mixed-case credential names still survive the shell scrub |
| V243-C2-004 | Open, partially remediated | broad read tools and several common secret names deny; common credential/config paths remain readable |
| V243-C2-005 | Open, partially remediated | temp+fsync+rename exists; trust stops at the control root and audit append does not enforce the same tree/file trust |
| V243-C2-006 | Open, partially remediated | trusted exact-session revocation persists; malformed/untrusted/mismatched state is silently replaced unrevoked |
| V243-C2-007 | Open, partially remediated | substring bypass is fixed; unknown hook fields such as `async:true` are accepted |
| V243-C2-008 | Open | installed-Claude settings-isolation canary remains explicitly human-operated and has no receipt |
| V243-C2-009 | Open | current handoff still contains contradictory historical status, scope, validation, risk, and next-action text |
| V243-C2-010 | Resolved | `launchPlan.ts` is 296 lines; other explicit KISS checks pass |
| V243-C2-011 | New, open | unrelated backlog/runtime and `.ralph` artifacts plus omitted changed paths violate scope/hygiene evidence |

### Revision-2 evidence for open findings

#### V243-C2-001 — Critical — Launcher remains within autonomous write authority

The protected-root test now correctly denies policy, settings, audit, and `term-control-center/build/**`. The same live evaluator returns `allow_workspace_edit` for `scripts/agentops/claude-native.sh`, which is executed directly on the next native launch and can remove every guard without a build. Protect the native launcher and any other directly executed enforcement entrypoint, or execute an owner-only snapshot outside autonomous roots. Add the direct-wrapper negative test.

#### V243-C2-002 — Critical — “Read-only” host Git is still executable authority

The npm/node patterns now hard-deny, resolving the original direct interpreter path. However, `VERIFICATION_COMMANDS` auto-allows bare `git diff`, `git show --stat`, `git status`, `git log`, and `git branch`. A local fixture proved that inherited `GIT_EXTERNAL_DIFF` makes the allowed literal `git diff` execute an arbitrary program. Current Git guidance also documents optional index refresh, fsmonitor, external diff/textconv, and shell-interpreted pager surfaces.

Keep all host Git human-gated, or route only fixed argv profiles through an AgentOps-owned executor with an allowlist-constructed environment, pinned Git binary, no pager, no optional locks, system/global config disabled, fsmonitor/hooks disabled, and external diff/textconv disabled. The strongest boundary remains read-only `.git` mounting. Add negative helper/pager/config/fsmonitor and metadata-write tests.

Research sources checked 2026-07-18: Git `status` background refresh, fsmonitor/hook, diff options/config, pager config, and Git environment/option documentation at <https://git-scm.com/docs/>. No raw research transcript was retained.

#### V243-C2-003 — High — Shell credential scrub differs from the tested policy

`isCredentialKey()` is case-insensitive, but the Bash `case` patterns are case-sensitive. A native-wrapper fixture with dummy lowercase `some_service_secret` still reached the final fake Claude process (`SECRET_PRESENT=yes`). Align the actual wrapper behavior with the case-insensitive policy or, preferably, construct an explicit child-environment allowlist after subscription preflight. Add end-to-end lower/mixed-case tests rather than testing only the TypeScript helper.

#### V243-C2-004 — High — Secret-path deny remains incomplete

Broad Grep/Glob/LS now deny and exact Read/NotebookRead require a path, which is a meaningful improvement. Independent checks still classify `.envrc`, `token.json`, `.cargo/credentials.toml`, `.config/gh/hosts.yml`, and `terraform.tfvars` as non-secret. Expand the conservative deny and keep ambiguous config/dotfile reads human-gated. Add these and equivalent provider/package-manager credential cases to focused tests.

#### V243-C2-005 — High — Control-plane ancestry and audit trust remain incomplete

`writeControlFile()` now uses a private temp file, fsync, rename, chmod, and post-check. But `assertTrustedTree()` stops at `controlRoot`, and `ensureControlDir()` never validates the parent ancestry. A fixture placed the control root below a mode-0777 parent and setup succeeded. This does not meet the approved no-world-writable/symlink-ancestor condition. In addition, `appendAudit()` still uses unchecked `mkdirSync`/`statSync`/`appendFileSync`, so an existing audit symlink or loose file is not rejected under the same trust contract.

Validate from the leaf through a fixed trusted owner root (or `/` with the approved mode rules), reject unsafe ancestors before creating anything, and apply no-symlink/owner/mode checks to audit append/rotation. Add world-writable-parent, symlinked-ancestor, audit-symlink, and loose-audit tests.

#### V243-C2-006 — High — Invalid state silently re-enables policy on setup

Exact trusted matching-session `revoked:true` now survives setup. However, `existingRevoked()` maps every missing, malformed, untrusted, owner/session-mismatched policy to `false`, then `writePolicy()` replaces it with a valid unrevoked policy. A fixture corrupted the policy, repeated setup, and observed a valid `revoked:false` replacement. Create only on a proven first-run absence; if a file exists but is malformed, untrusted, or mismatched, fail launch closed. Preserve the stable collision-resistant session binding and add repeated-setup tests for every invalid-state class.

#### V243-C2-007 — High — Settings validation is not strict at nested schema boundaries

The exact two-token realpath command check rejects the prior substring/comment attack. The validator still ignores unknown fields inside the command hook and other nested objects. A settings fixture with the correct command plus `"async":true` passed and launched the fake Claude; an async pre-tool hook cannot provide the required synchronous decision boundary. Compare against an exact allowlisted schema (including allowed keys at every level) and add async, extra-field, extra-top-level, extra-permission, symlink, and mode negatives.

#### V243-C2-008 — Medium — Installed-Claude canary still needs a human receipt

The fake launcher tests prove argument injection only. The coder explicitly records that the installed-Claude 2.1.195 `--setting-sources ''` isolation canary remains human-operated and absent. This checkpoint cannot be approved until a sanitized receipt proves user/project/local allow rules and hooks are excluded, or the security reviewer explicitly revises that requirement.

#### V243-C2-009 — Medium — Handoff remains ambiguous

The new opening status is current, but later unscoped sections still state “pending approval,” “only research artifacts allowed,” “no tracked diff exists,” “18 passed,” “make no policy changes,” and “apply remaining revisions.” The current tree has tracked implementation diffs, 23 focused passing tests, and this revision already applies changes. Move checkpoint-1 text under a clearly labeled immutable history section and make current touched paths, validation, risks, open findings, and next actor singular and accurate.

#### V243-C2-011 — Medium — Unapproved/generated repository drift is not reconciled

The working tree contains `.ralph/` run-state files and an unrelated timestamp update in `dev-plans/prd-backlog.md`, contrary to the PRD's approved artifact-placement boundary and Steward readiness. Relevant changes to `term-control-center/package.json`, `tests/nativeClaudeLaunchPlan.test.ts`, `autonomyControlPlane.ts`, and additional run review files are also omitted from the handoff touched-file inventory. Remove generated/unrelated drift or move necessary evidence into the co-located approved run directory, then list every retained changed path and rationale. The package/test changes must be explicitly justified as checkpoint-2 enforcement scope.

### KISS recheck

V243-C2-010 is closed. `launchPlan.ts` is 296 lines; every new implementation/test file is under 300. Changed functions remain within the under-20-line rule, nesting is bounded, parameters are grouped or within limits, comments explain an external umask constraint, and no commented-out/dead code was found.

## Validation Receipt — Checkpoint 2 Revision 2

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement, revision 2
- **Decision:** revision_requested
- **Final review:** no
- **Acceptance criteria reviewed:** default deny/revocation, always-gate ordering, owner-only atomic state, protected enforcement, secret access, inherited environment, strict native settings, read-only command classification, sanitized audit, F1-F5, R1-R7, KISS, and durable evidence.
- **Reviewed files/surfaces:** the full current diff and untracked source/test/run scope, including newly added `autonomyControlPlane.ts`, package/build script, native launch-plan tests, sandbox/security review artifacts, PTY/tmux inherited environment, installed Claude 2.1.195, and Git 2.43 command behavior.
- **Commands/results:**
  - `npm --prefix term-control-center run typecheck` — passed.
  - `cd term-control-center && node --import tsx --test tests/nativeClaudeLaunchPlan.test.ts tests/nativeClaudeLauncher.test.ts tests/autonomyHook.test.ts` — 23/23 passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Adversarial dummy `/tmp` fixtures — protected current policy/settings/hook passed; direct launcher write was allowed; malformed policy reset to unrevoked; world-writable control ancestor accepted; lowercase credential survived; async hook settings launched; common secret paths were not classified secret; inherited `GIT_EXTERNAL_DIFF` executed under bare `git diff`.
- **Skipped checks/reasons:** installed-Claude settings-isolation canary is pending human operation; full suite/full app build were not needed to establish the remaining bounded defects; sandbox implementation/activation, checkpoint-3 conformance, live delayed-response smoke, Steward final review, and final bug-check remain gated.
- **Edge cases:** duplicate/colliding logical sessions; malformed or loose state on relaunch; world-writable and symlinked ancestors; audit symlink/rotation; lower/mixed-case credentials; async/extra settings fields; Git helper/pager/fsmonitor/config environment; secret-like config files; direct launcher self-edit; generated artifact placement.
- **Regression risks:** next-launch guard removal, silent kill-switch reset, external helper execution, credential/secret disclosure, audit redirection, settings hook becoming non-blocking, stale handoff authority, and unreviewed repo drift.
- **Relevant canonical standards checklist summary:** modularity and KISS improved, but fail-closed control ownership, environment isolation, trusted filesystem ancestry, exact schema validation, deterministic evidence, and artifact hygiene are still incomplete. The standards require these security deviations to remain blocked rather than normalized as residual risk.
- **Findings:** V243-C2-001 through V243-C2-009 remain open; V243-C2-010 is resolved; V243-C2-011 is new and open.
- **Required follow-up:** coder applies the remaining bounded controls and cleanup, refreshes the handoff, and reruns focused validation. Verification execution—including raw Git—stays human-gated until the hardened executor/sandbox path has separate security approval. Then obtain the human-operated installed-Claude canary receipt.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; edited no coder-owned file; and used only dummy temporary fixtures.
- **Checkpoint compliance/deviation:** legacy delegated bypass and coms transport remain unchanged, and no sandbox was activated. Checkpoint 2 still deviates from approved F1/F2/R2/R5/R6 and repository hygiene; no acceptable exception closes those gaps. The branch also became three commits behind `origin/main` during the run; no history mutation was attempted, and final validation must be repeated after an authorized freshness update.

## Checkpoint 2 re-review — revision 3

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-3 working tree.
- **Verdict:** `revision_requested`.
- **Summary:** seven prior code/evidence findings and the KISS finding now close. The focused suite passes 31/31. Three bounded security controls remain incomplete, followed by the already-recorded human-operated installed-Claude canary gate.

### Finding disposition

| Finding | Revision-3 status | Evidence |
| --- | --- | --- |
| V243-C2-001 | Resolved | policy/settings/audit, `build/**`, and the directly executed native wrapper are protected; direct-wrapper edit negative passes |
| V243-C2-002 | Resolved | every Bash command, including all Git, now hard-denies; no sandbox/executor is active |
| V243-C2-003 | Open | case handling is fixed, but a credential-name denylist still passes common secret-bearing variables |
| V243-C2-004 | Open | listed credential/config paths deny, but obvious secret-bearing filenames remain outside the deny |
| V243-C2-005 | Open | atomic/audit trust improved, but sticky world-writable ancestors are accepted contrary to approved F2 |
| V243-C2-006 | Resolved | invalid existing policy fails setup and trusted revocation persists |
| V243-C2-007 | Resolved | exact nested-key validation rejects async and extra settings fields |
| V243-C2-008 | Open, human gate | installed-Claude 2.1.195 settings-isolation canary has no sanitized receipt |
| V243-C2-009 | Resolved | handoff has one current status/scope/validation/next-action record plus labeled history |
| V243-C2-010 | Resolved | all changed files and functions satisfy explicit KISS limits |
| V243-C2-011 | Resolved with deferred final cleanup | `.ralph/` is absent and retained paths are listed; Steward classifies the sole backlog timestamp as generated drift to remove before final bug-check |

### Remaining coder findings

#### V243-C2-003 — High — Credential stripping remains denylist-based

The lower/mixed-case wrapper test closes the case-sensitivity defect. The native process still inherits all names that do not match the finite pattern. Independent dummy checks show `SESSION_COOKIE`, `DATABASE_URL`, `WEBHOOK_URL`, and `JWT` survive `sanitizeAutonomousEnv`; the Bash scrub uses the same finite categories. These are common secret-bearing credentials. The checkpoint's own sandbox/security design requires an allowlist-constructed native child environment, not a name denylist.

**Required bounded action:** after subscription preflight, construct the final Claude environment from a documented minimal allowlist plus required AgentOps/coms/autonomy variables. Do not pass arbitrary inherited names. Add end-to-end wrapper tests proving unrelated required variables survive while cookie, database URL, webhook URL, JWT, cloud profile/config, preload/runtime injection, and unknown names do not.

#### V243-C2-004 — High — Secret-path classification still has obvious omissions

The revision correctly denies `.envrc`, token/config/provider directories, tfvars, and key extensions, and broad Grep/Glob/LS remains denied. Independent checks still classify `secrets.yaml`, `service-account.json`, `.pypirc`, and `auth.json` as ordinary readable paths.

**Required bounded action:** extend the conservative deny to standard secret/auth/service-account/package-manager filenames and secret-like basename patterns, with focused tests. Ambiguous local credential/config files must remain human-gated rather than relying on exact prior examples.

#### V243-C2-005 — High — Sticky world-writable ancestors violate approved F2

Atomic policy/settings replacement, invalid-state failure, audit `O_NOFOLLOW`, audit mode checks, and non-sticky world-writable rejection are implemented. `trustedControlParent()` and `trustedAncestors()` deliberately accept a world-writable ancestor when its sticky bit is set, so `/tmp` remains accepted.

A bounded Researcher recheck on 2026-07-18 confirmed that sticky semantics restrict rename/removal but do not make the ancestor non-world-writable or satisfy the literal approved “no world-writable ancestor” condition. Accepting sticky ancestors requires a separately recorded security exception; none exists.

**Required bounded action:** use a verified owner-private runtime/state base and reject every group/other-writable or symlinked component through the control root. Adjust temporary tests to create fixtures under a trusted private base, or obtain explicit renewed security approval for a precisely bounded sticky-directory exception.

Sources: POSIX directory protection, Linux sticky-directory behavior, and CWE-367 TOCTOU guidance, retrieved 2026-07-18.

### Remaining human evidence gate

#### V243-C2-008 — Medium — Installed-Claude settings-isolation canary

No coder change can replace this evidence. After V243-C2-003/004/005 close, the human operator must run the version-pinned local canary and write a sanitized receipt proving user/project/local allow rules and hooks are excluded under `--setting-sources ''`. Until then checkpoint 2 cannot be approved.

### Steward and KISS notes

Steward reports no placement issue beyond the harness-generated `dev-plans/prd-backlog.md` timestamp. That unrelated diff may remain during active work but must be restored before final bug-check, followed by verifier recheck. `.ralph/` is absent. All retained implementation/tests/docs/run evidence are in expected locations and contain no raw secrets/transcripts.

`launchPlan.ts` is 296 lines; all new files are below 300. Functions remain below 20 lines, nesting and parameters are bounded, comments explain the umask constraint, and no dead/commented-out code was found.

## Validation Receipt — Checkpoint 2 Revision 3

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement, revision 3
- **Decision:** revision_requested
- **Final review:** no
- **Acceptance criteria reviewed:** project/session default deny; kill-switch persistence; always-gate ordering; protected launcher/build/control state; atomic trusted policy/audit; strict settings schema; credential environment; secret paths; full Bash denial; sanitized audit; F1-F5; R1-R7; KISS; artifact hygiene.
- **Reviewed files/surfaces:** all handoff-listed implementation/test/doc/run paths, current diff/untracked scope, native launcher environment, control ancestry, installed Claude 2.1.195 requirements, and Steward cleanup classification.
- **Commands/results:**
  - `npm --prefix term-control-center run typecheck` — passed.
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/autonomyControlPlane.test.ts tests/nativeClaudeLauncher.test.ts tests/nativeClaudeLaunchPlan.test.ts` — 31/31 passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Independent dummy classification checks — case-insensitive `_SECRET` now denies; common cookie/URL/JWT environment names and several common secret filenames still pass.
  - Researcher ancestor-trust recheck — sticky world-writable ancestry does not comply with approved F2 absent an explicit security exception.
  - Steward hygiene consult — no placement defect; backlog timestamp cleanup deferred to pre-final.
- **Skipped checks/reasons:** installed-Claude canary is a pending human operation; full suite/app build, sandbox work, checkpoint-3 conformance, live smoke, final Steward recheck, and final bug-check remain later gates.
- **Edge cases:** secret values under non-obvious environment names; common auth/service-account files; sticky shared ancestors; symlink/TOCTOU state; malformed/revoked relaunch; async/extra hook settings; direct launcher edits; generated backlog drift.
- **Regression risks:** inherited secret disclosure, credential-file reads, control-root substitution below shared directories, and claiming fake launcher tests prove installed-Claude source isolation.
- **Relevant canonical standards checklist summary:** code structure, deterministic focused tests, revocation, direct execution denial, strict schema, and KISS now align. Fail-closed secret/environment and trusted-ancestry controls remain incomplete; no security deviation may be normalized without explicit approval.
- **Findings:** V243-C2-003, V243-C2-004, V243-C2-005, and V243-C2-008 remain open. All other checkpoint-2 findings are resolved or deferred to the recorded pre-final cleanup.
- **Required follow-up:** coder applies the three bounded control fixes and reruns focused/typecheck/build/diff validation. Then the human operator performs the installed-Claude canary and records its sanitized receipt.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; edited no coder-owned file; and used only dummy local checks.
- **Checkpoint compliance/deviation:** no sandbox, legacy delegation, or coms transport change occurred. Checkpoint 2 still deviates from the approved secret/environment boundary and literal F2 ancestry rule. The generated backlog timestamp is an accepted temporary Steward-classified deviation with mandatory pre-final cleanup. The branch remains three commits behind `origin/main`; final validation must repeat after an authorized freshness update.

## Checkpoint 2 re-review — revision 4

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-4 working tree.
- **Verdict:** `needs_human`.
- **Why escalation is now required:** focused tests pass and the revision improves all three remaining coder-controlled surfaces, but each security finding still has a reproducible gap after three bounded remediation attempts. The researcher/security consult budget for this checkpoint has been used, and V243-C2-008 independently requires a human-operated canary. Per the continuation contract, the next decision belongs to the human/security reviewer rather than another unbounded coder loop.

### Revision-4 finding disposition

| Finding | Status | Revision-4 evidence |
| --- | --- | --- |
| V243-C2-003 | Open; needs security decision | final environment uses an allowlist, but broad AgentOps/browser/coms prefixes admit secret-bearing unknown names |
| V243-C2-004 | Open; needs taxonomy decision | secret-path regex/list expanded, but common password/API/access-key/webhook filenames still auto-read |
| V243-C2-005 | Open; needs trust-policy decision | world-writable and symlink ancestors now reject, but group-writable ancestors remain accepted contrary to the last bounded safe rule |
| V243-C2-008 | Open; human validation | installed-Claude settings-isolation canary receipt remains absent |
| All other checkpoint-2 findings | Resolved/deferred as recorded | no regression observed in revision 4 |

### Human/security questions requiring a binding answer

#### V243-C2-003 — Environment namespace prefixes

`env -i` is now used and arbitrary unrelated names are removed. However `safeEnvKey()` and the shell wrapper allow every name under `AGENTOPS_RUNTIME_*`, `AGENTOPS_AUTONOMY_*`, `PI_COMS_*`, and `TERM_CONTROL_BROWSER_*`. Dummy checks confirm `AGENTOPS_RUNTIME_SECRET`, `AGENTOPS_AUTONOMY_PASSWORD`, `PI_COMS_AUTH_TOKEN`, and `TERM_CONTROL_BROWSER_TOKEN` survive. Therefore the handoff claim that unknown secret-bearing names deny is not true for approved namespaces.

**Human/security decision needed:** either require an exact finite name allowlist for each namespace, optionally with a second credential-name rejection, or explicitly approve broad namespace prefixes as a bounded exception with owner, risk, mitigation, and review date. The default safe recommendation is exact names.

#### V243-C2-004 — Secret-path taxonomy limit

The revision adds secret/auth/service-account patterns and closes the previously named examples. Dummy checks still classify `passwords.txt`, `api-key.json`, `access-key.csv`, and `webhook-url.txt` as ordinary readable paths.

**Human/security decision needed:** choose a binding conservative pattern taxonomy that includes password/passphrase/API/access-key/webhook/provider credential names, or remove `local_read` from automatic permission and keep exact file reads human-gated. Repeated example-by-example expansion is not a stable security boundary.

#### V243-C2-005 — Group-writable ancestor policy

The revision correctly rejects sticky and non-sticky world-writable ancestors and symlinks, and uses an owner-0700 immediate control parent. `trustedAncestors()` checks only the world-write bit, so a mode-0770 higher ancestor is accepted; a dummy fixture reproduced `groupWritableAncestorAccepted:true`.

The prior Researcher consult's minimal safe rule was no group/other-writable component through the trusted base. **Human/security decision needed:** enforce that rule, or explicitly approve group-writable ancestry as a documented exception tied to a trusted group model. The current handoff records no exception.

#### V243-C2-008 — Installed-Claude canary

The operator must run the version-pinned Claude Code 2.1.195 canary and write a sanitized receipt proving user/project/local settings allow rules and hooks are excluded by `--setting-sources ''`. Fake CLI tests remain insufficient.

### Code quality and resolved controls

The revision preserves full Bash/Git denial, atomic policy/settings writes, invalid-state failure, revocation persistence, audit no-follow/mode checks, strict nested settings schema, protected wrapper/build/state paths, sanitized bounded audit, same-worktree coms mapping, and legacy-path exclusion. `launchPlan.ts` remains 296 lines; other changed files/functions, parameters, nesting, comments, and dead-code checks remain KISS-compliant.

## Validation Receipt — Checkpoint 2 Revision 4

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement, revision 4
- **Decision:** needs_human
- **Final review:** no
- **Acceptance criteria reviewed:** final child environment, secret/config path boundary, trusted control ancestry, default deny/revocation, all-Bash denial, strict settings, audit safety, KISS, durable handoff, and installed-Claude evidence.
- **Reviewed files/surfaces:** current full scope with focused attention to `nativeClaudeSettings.ts`, `claude-native.sh`, `autonomyPaths.ts`, `autonomyControlPlane.ts`, their focused tests, current handoff, and prior source-cited Researcher/Security/Steward decisions.
- **Commands/results:**
  - `npm --prefix term-control-center run typecheck` — passed.
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/autonomyControlPlane.test.ts tests/nativeClaudeLauncher.test.ts tests/nativeClaudeLaunchPlan.test.ts` — 31/31 passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Independent dummy negatives — unrelated environment name denied; four secret-bearing approved-prefix names survived; four common secret filenames remained readable; a mode-0770 ancestor was accepted.
- **Skipped checks/reasons:** installed-Claude canary awaits human operation; full suite/app build, sandbox implementation, checkpoint-3 conformance, live smoke, final Steward cleanup/recheck, and bug-check remain gated.
- **Edge cases:** future secret variables inside approved prefixes; credential filenames outside a finite list; trusted-group versus owner-only ancestry; auth-token necessity for Claude itself; generated backlog timestamp; branch freshness.
- **Regression risks:** secret propagation through future namespace keys, secret-file auto-read, same-group control-root substitution, and false confidence from fake settings tests.
- **Relevant canonical standards checklist summary:** modularity, KISS, deterministic focused tests, default deny, side-effect isolation, and most control-plane safeguards pass. Security exceptions and ambiguous secret/trust boundaries require explicit human approval; the verifier cannot normalize them after three unsuccessful bounded fixes.
- **Findings:** V243-C2-003, V243-C2-004, V243-C2-005, and V243-C2-008 remain open.
- **Required follow-up:** human/security reviewer records binding decisions for environment namespaces, secret-path/read taxonomy, ancestor trust, and the installed-Claude canary. If bounded code changes are authorized, coder applies only those decisions and re-requests review.
- **Next actor:** human/security reviewer.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; edited no coder-owned file; and used only dummy local validation.
- **Checkpoint compliance/deviation:** no sandbox, legacy-delegation, or coms transport mutation occurred. The generated backlog timestamp remains a Steward-approved temporary deviation requiring pre-final cleanup. The branch remains three commits behind `origin/main`, so final validation must repeat after authorized freshness handling. The three unresolved security-policy interpretations have no approved exception and therefore fail closed.

## Checkpoint 2 re-review — revision 5

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-5 working tree and human canary receipt.
- **Verdict:** `revision_requested`.
- **Summary:** the human decisions resolve the prior policy ambiguity, the installed-Claude canary passes, and fixed control-state placement closes V243-C2-005. Two implementations do not yet match the binding decisions, and the handoff describes them as closed despite contradictory current evidence. These are bounded coder corrections, not a new human-policy question.

### Finding disposition

| Finding | Revision-5 status | Evidence |
| --- | --- | --- |
| V243-C2-003 | Open | exact-name allowlist is implemented except wildcard `LC_*`, which admits `LC_SECRET` |
| V243-C2-004 | Open | binding basename taxonomy names password/passphrase/API/access-key/webhook, but code/tests omit them |
| V243-C2-005 | Resolved | state moved under a fixed owner-0700 base; writes validate base-to-leaf owner/mode/symlink properties |
| V243-C2-008 | Resolved | sanitized installed-Claude 2.1.195 differential canary records `result: passed` |
| V243-C2-009 | Reopened | handoff says the passed canary is still the only gate and claims incomplete controls are addressed |

### Bounded coder corrections

#### V243-C2-003 — High — Environment allowlist is not exact

The broad AgentOps/coms/browser namespace prefixes are removed and the wrapper uses `env -i`, which closes the prior ambiguity. `safeEnvKey()` still accepts every `LC_*` name and the shell wrapper mirrors that wildcard. A dummy `LC_SECRET` survives, contradicting the binding human decision that only exact variable names are allowed.

**Required action:** enumerate the supported locale variables (`LC_ALL`, `LC_CTYPE`, and any other explicitly required POSIX locale categories) in both implementations; remove both `LC_*` wildcard branches; add TypeScript and end-to-end wrapper negatives for `LC_SECRET`/unknown locale-like names plus positive required-locale checks.

#### V243-C2-004 — High — Binding secret basename categories are missing

The human decision recorded in the handoff requires password/passphrase/secret/credential/token/auth/API/access-key/webhook/cookie/JWT/wallet/private-key config/data names while leaving ordinary source files readable. `SECRET_CONFIG_NAME` contains secret, credential, service-account, private-key, auth, token, cookie, JWT, and wallet, but omits password, passphrase, API key, access key, and webhook. Dummy checks show `passwords.txt`, `api-key.json`, `access-key.csv`, and `webhook-url.txt` remain readable; the focused test also omits these categories.

**Required action:** implement every binding category with delimiter-aware config/data basename matching, add the missing positive-deny cases, and retain a negative case proving ordinary source names are readable.

#### V243-C2-009 — Medium — Current handoff is internally inconsistent

The first paragraph says the passed canary remains the only known evidence gate, while the finding disposition later says V243-C2-008 is addressed. It also marks V243-C2-003/004 addressed despite the reproducible decision/code mismatch, and says backlog drift was removed while the Steward-classified generated timestamp is currently present.

**Required action:** refresh current status, finding disposition, validation, risk, cleanup-deviation, and next actor after the two code fixes. Keep the passed canary and generated-backlog cleanup timing explicit and non-contradictory.

### Resolved human gate evidence

`installed-claude-settings-canary.json` is sanitized and records Claude Code 2.1.195, `--setting-sources ''`, explicit hook execution, absence of project/local/user source loading, one successful Read canary, no bypass mode, no retained raw debug/prompt/response, and `result: passed`. V243-C2-008 is closed. The strict MCP wrapper remains independently required because setting-source isolation is not an MCP isolation claim.

### KISS and safety recheck

All Bash/Git remains denied; no sandbox is active. Policy/settings/audit, wrapper, and built enforcement paths remain protected. Revocation, invalid-state, strict schema, audit, MCP mapping, legacy exclusion, and KISS checks show no regression. Files remain below 300 lines and changed functions remain below 20 lines with bounded nesting/parameters and permissible comments.

## Validation Receipt — Checkpoint 2 Revision 5

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up
- **Project ID:** `agentops-harness`
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement, revision 5
- **Decision:** revision_requested
- **Final review:** no
- **Acceptance criteria reviewed:** binding environment decision, binding secret-path taxonomy, fixed owner-private control root, installed-Claude canary, full Bash denial, strict settings/MCP isolation, revocation/audit safety, KISS, and durable evidence consistency.
- **Reviewed files/surfaces:** current complete scope, binding decisions in the handoff, `installed-claude-settings-canary.json`, native environment code/wrapper, path taxonomy, control-plane code/tests, and prior Steward/research evidence.
- **Commands/results:**
  - `npm --prefix term-control-center run typecheck` — passed.
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/autonomyControlPlane.test.ts tests/nativeClaudeLauncher.test.ts tests/nativeClaudeLaunchPlan.test.ts` — 31/31 passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Canary receipt parse/review — passed and sanitized for Claude Code 2.1.195.
  - Independent dummy checks — unknown AgentOps runtime name denied; `LC_SECRET` survived; four binding secret basename categories remained readable; ordinary source remained readable.
- **Skipped checks/reasons:** full suite/app build, sandbox implementation/activation, checkpoint-3 conformance, live smoke, final Steward cleanup/recheck, and bug-check remain later checkpoints.
- **Edge cases:** fake locale-prefixed secrets; plural/delimited password/passphrase/API/access-key/webhook basenames; config/data versus ordinary source distinction; generated backlog timestamp; branch freshness.
- **Regression risks:** secret propagation through locale wildcard, credential-config auto-read, and downstream reliance on a stale handoff.
- **Relevant canonical standards checklist summary:** fixed state ownership, default deny, strict settings, environment reconstruction, deterministic canary evidence, and KISS substantially comply. The last two binding security rules must match code/tests exactly, and durable evidence cannot claim closure early.
- **Findings:** V243-C2-003, V243-C2-004, and V243-C2-009 remain open. V243-C2-005 and V243-C2-008 are resolved.
- **Required follow-up:** coder applies the exact locale and basename fixes, refreshes the handoff, and reruns the same focused/typecheck/build/diff checks. No additional human decision is needed for these bounded corrections.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; edited no coder-owned file; and used only dummy local checks.
- **Checkpoint compliance/deviation:** human canary and fixed-base decisions are satisfied. Environment/path code still deviates from two binding categories. The generated backlog timestamp remains a Steward-approved temporary deviation requiring pre-final cleanup. The branch remains three commits behind `origin/main`; final validation must repeat after authorized freshness handling.

## Checkpoint 2 re-review — revision 6

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-6 working tree.
- **Verdict:** `approved`.
- **Scope:** the three revision-5 findings only, with regression checks for full Bash denial, sandbox non-activation, KISS, and current evidence hygiene.
- **Final review:** no; final Steward cleanup, later PRD checkpoints, and final bug-check remain outstanding.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical PRD, branch, and worktree agree | Pass | Issue #243 independently retrieved with `gh`; `prd/native-session-coms-followup-243`; expected worktree root |
| V243-C2-003 uses an exact inherited-environment allowlist | Pass | TypeScript and shell lists have identical 72-name sets; only `LC_ALL` and `LC_CTYPE` locale names are present; independent checks deny `LC_SECRET`, `LC_FAKE`, broad-prefix secret names, and unknown names |
| V243-C2-003 has end-to-end wrapper coverage | Pass | Wrapper fixture retains `LC_ALL`/`LC_CTYPE` and an approved runtime key while rejecting unknown, credential-like, and locale-like inherited names |
| V243-C2-004 implements the binding basename taxonomy | Pass | Delimiter-aware config/data matching denies password, passphrase, secret, credential, service-account, API-key, access-key, private-key, auth, token, webhook, cookie, JWT, and wallet categories |
| V243-C2-004 preserves ordinary source reads | Pass | `auth.ts`, `authorization.ts`, and `notsecret.ts` independently classify readable; focused tests pin `auth.ts` |
| V243-C2-009 handoff is singular and current | Pass with deferred hygiene qualifier | Current status, authorization, dispositions, validation, risks, touched scope, and next actor agree. It explicitly identifies the backlog timestamp as harness-generated and requires cleanup before final review |
| All host Bash remains denied | Pass | Classifier returns `deny_always_gate` for Git, npm/node/build/test, and every otherwise unmatched Bash command |
| Bubblewrap implementation or activation is absent | Pass | No `bwrap`, Bubblewrap, verification executor, namespace, or activation surface exists in the delivered implementation/test scope |
| Legacy delegated-Claude and coms transport remain unchanged | Pass | No diff in those surfaces; option B remains documentation/policy mapping only |
| KISS review | Pass | Reviewed files are 66–246 lines; changed functions/test callbacks stay within limits with bounded nesting/parameters; comment density is 0–2.5% and comments explain the umask constraint; no commented-out or newly dead code found |

### Finding disposition

| Finding | Revision-6 status | Evidence |
| --- | --- | --- |
| V243-C2-003 | Resolved | Exact TypeScript/shell allowlist parity and locale negatives pass |
| V243-C2-004 | Resolved | Every approved config/data basename category and ordinary-source negative pass |
| V243-C2-009 | Resolved | Handoff presents one current revision-6 record and accurately bounds remaining risks/cleanup |

No findings are open for checkpoint 2.

### Generated backlog observation

`dev-plans/prd-backlog.md` currently has timestamp-only runtime drift. Its mtime is later than the revision-6 handoff, and the timestamp changed again while this review ran, demonstrating active harness regeneration rather than retained implementation scope. This is the already accepted V243-C2-011 pre-final deviation, not a reopened checkpoint-2 finding. It must be restored after runtime stabilization and rechecked by Steward/verifier before final bug-check; this approval is not final hygiene approval.

## Validation Receipt — Checkpoint 2 Revision 6

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2 — safe autonomy policy and launcher enforcement, revision 6.
- **Decision:** approved.
- **Final review:** no.
- **Acceptance criteria reviewed:** exact final native environment; conservative secret/config basename denial; global-bypass rejection; full host Bash/Git/npm/node denial; no Bubblewrap implementation/activation; current durable evidence; KISS and artifact hygiene.
- **Reviewed files/surfaces:** all files in the revision-6 request, complete current handoff, prior finding history, canonical issue #243, installed-Claude canary, current changed-path inventory, launcher/settings/path classifiers, focused tests, and current dirty-tree state.
- **Commands/results:**
  - `bash -n scripts/agentops/claude-native.sh` — passed.
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/autonomyControlPlane.test.ts tests/nativeClaudeLauncher.test.ts tests/nativeClaudeLaunchPlan.test.ts` — 31/31 passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Independent environment parity check — shell and TypeScript exact sets match at 72 names; locale wildcard is absent.
  - Independent path cases — five named revision-5 misses deny; `auth.ts` and ordinary lookalikes remain readable.
  - Implementation-scope search — no Bubblewrap/executor/namespace activation; all Bash classifier paths deny.
- **Skipped checks/reasons:** full suite/app build, sandbox design implementation/activation, coms conformance and delayed-response smoke, final Steward review, and bug-check belong to later checkpoints/final review.
- **Edge cases:** locale-like secret names; delimited/plural config basenames; ordinary source names containing auth-like text; active runtime rewriting generated backlog status; branch freshness before final validation.
- **Regression risks:** future exact allowlist additions could expose secret-bearing names; secret taxonomy additions could overblock source files; a later sandbox could accidentally re-enable raw host execution; generated backlog drift could be retained at final review.
- **Relevant canonical standards checklist summary:** the delivered revision is fail-closed, explicit at environment/path boundaries, deterministic under focused IO tests, and within KISS limits. No exception or reusable repo-local skill was introduced.
- **Findings:** none open for this checkpoint.
- **Required follow-up:** proceed only to the separately reviewed Bubblewrap implementation checkpoint; do not activate autonomous verification without its required human/security approval. Restore generated backlog drift and resolve the three-commit main-branch freshness gap before final validation.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; and edited only this verifier-owned report.
- **Checkpoint compliance/deviation:** checkpoint 2 now meets its binding security decisions. The timestamp-only backlog diff remains an accepted temporary active-runtime deviation, and the branch remains three commits behind `origin/main`; both are later gates, not checkpoint-2 approval claims.

## Checkpoint 2b review — revision 1

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the checkpoint-2b working tree.
- **Verdict:** `revision_requested`.
- **Scope:** non-activated Bubblewrap plan construction, host preflight, command IDs, mount/environment boundary, direct-Bash regression, structural tests, and evidence only.
- **Authorization:** the existing security review permits bounded implementation under #243 but independently forbids activation until security/human sign-off and the required adversarial containment proof.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical PRD, branch, and worktree agree | Pass | Issue #243 independently retrieved with `gh`; expected branch/worktree; branch remains three commits behind `origin/main` |
| Implementation remains non-activated | Pass | `verificationSandbox.ts` is referenced only by its test and emitted build output; no launcher, hook, MCP, or native settings imports it; no executor/spawn path exists |
| Direct host Bash remains denied | Pass | Focused tests and source inspection show npm, node, Git, metacharacter forms, and all unmatched Bash return deny |
| Finite typed command declarations exist | Partial | Five compile-time IDs map to fixed argv, but V243-C2B-004 shows runtime input is not validated |
| Bubblewrap/userns preflight fails closed | Fail | V243-C2B-003 |
| Environment is explicitly reconstructed | Pass for plan shape | `--clearenv`, exact `--setenv` entries, and a five-name spawn environment contain no inherited credential variable |
| Namespace has no shared network/sysfs/home/socket bind | Pass for static nominal plan | `--unshare-all`, no `--share-net`, no `/sys`, `/run`, resolver, or broad home bind; `/proc`, minimal `/dev`, and `/tmp` are namespaced |
| Worktree/control-plane/artifact boundary is safe | Fail | V243-C2B-001 |
| Worktree/Git roots are trusted and correctly resolved | Fail | V243-C2B-002 |
| Planned toolchain can run the finite commands | Fail | V243-C2B-005 |
| Adversarial structural coverage is sufficient | Fail through findings | Current `includes()` assertions do not detect extra/wrong mounts, unsafe roots, fail-open preflight, runtime-ID TypeErrors, protected-path writes, or toolchain incompatibility |
| KISS review | Pass | New source/test files are 57/39 lines; functions are below 20 lines with at most three parameters and shallow nesting; no comments, commented-out code, or dead layers were added |

### Research/design evidence relied upon

No new researcher query was needed. This review relies on the source-cited, host-verified 2026-07-18 `security-review-sandbox.md`, which requires: a host-owned executor boundary, no control-plane/handoff write access, actual fail-closed userns availability, a fixed sanitized environment, read-only Git metadata, a compatible pinned toolchain, and no activation before the package-script adversarial tests and resource limits pass.

### Open findings

#### V243-C2B-001 — Critical activation blocker — The writable worktree bind contains enforcement and durable evidence

- **Evidence:** `verificationSandbox.ts:38-40` binds the entire worktree read-write and adds no nested protected mounts. The currently executed native wrapper is `scripts/agentops/claude-native.sh`; the hook/import graph is `term-control-center/build/server/**`; the `.git` pointer and this run's durable handoff/report are also inside that writable bind. A sandboxed package script bypasses the host path classifier and can overwrite those paths directly. This contradicts the requested no-control-plane plan and security-review §§2, 5, 6, and T-controlplane.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, its tests, and the current native enforcement placement.
- **Bounded action:** make the enforcement launcher/hook/import graph execute from an owner-private control-plane snapshot outside the sandbox and protect every remaining in-worktree launcher, `.git` pointer/private gitdir, and durable run-evidence path with exact read-only nested mounts. Add structural negatives that parse mount pairs and prove no protected path is writable; defer live package-script proof to the activation gate.
- **Decision impact:** the dormant module is not safe to wire or approve as the required containment plan.

#### V243-C2B-002 — High — Sandbox root validation accepts arbitrary files, symlinks, and `/`

- **Evidence:** `trustedDirectory()` uses only `path.resolve()` plus `existsSync()`. Independent fixtures were accepted with `/` as the read-write worktree, a regular file as `commonGitDir`, and a symlink as the worktree. The committed test passes this worktree's `.git` pointer file as `commonGitDir`; it never tests the actual common directory (`git rev-parse --git-common-dir`). No owner/mode/type, canonical-realpath, worktree identity, Git relationship, disjointness, or `.git` pointer/private-gitdir read-only check exists.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`.
- **Bounded action:** derive roots from trusted session context rather than requester-controlled strings; canonicalize and require trusted directories; reject `/`, symlinks, regular files, mismatched/overlapping roots, and paths outside the active worktree contract; verify the actual common and worktree-private Git directories plus pointer relationship and mount all Git metadata read-only. Add the reproduced negatives.
- **Decision impact:** a future caller could widen the sandbox to host filesystem authority or produce a nonfunctional/unsafe Git boundary.

#### V243-C2B-003 — High — Host preflight is fail-open and does not probe user namespaces

- **Evidence:** `assertSandboxHost()` checks only `existsSync('/usr/bin/bwrap')`; it does not require a regular executable or execute a bounded namespace probe. `userNamespacesRestricted()` treats an unreadable/missing AppArmor sysctl as unrestricted and ignores `kernel.unprivileged_userns_clone`, `user.max_user_namespaces`, runtime/AppArmor profile denial, and bwrap startup failure. No negative preflight test is possible with the hardcoded host reads.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`.
- **Bounded action:** use an injectable host adapter; require a trusted executable bwrap and a bounded no-op bwrap/userns probe (or an equivalently complete, fail-closed host capability check). Treat unknown/read/probe errors as `deny_sandbox_unavailable`, never success. Test missing, non-executable, restricted, zero-namespace, read-error, and probe-failure cases without executing a verification command.
- **Decision impact:** the explicit fail-closed preflight acceptance condition is not met.

#### V243-C2B-004 — Medium — Command IDs are compile-time-only

- **Evidence:** `COMMANDS[request.commandId]` is used without a runtime membership check. Independent input `commandId: 'deploy'` throws the incidental JavaScript error `command is not iterable`; the test accepts any throw. A future MCP/JSON boundary cannot rely on TypeScript types.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`.
- **Bounded action:** validate runtime input against the finite ID set before plan construction and return one stable enumerated denial. Assert the exact denial and exact argv for every allowed ID.
- **Decision impact:** the typed finite command contract is incomplete and unauditable at the runtime boundary, although the current error happens to fail closed.

#### V243-C2B-005 — Medium — The plan selects an incompatible host Node toolchain

- **Evidence:** the plan sets `PATH=/usr/bin:/bin`, selecting Node 18.19.1/npm 9.2.0 instead of the active Node 22.22.3/npm 10.9.8. This project uses Vite 8.0.16 and `@vitejs/plugin-react` 6.0.2, both requiring Node `^20.19.0 || >=22.12.0`. A verifier probe under the planned PATH failed immediately with Vite's Node-version error and `CustomEvent is not defined`. The finite `lint` ID also targets a package script that does not exist.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`, `term-control-center/package.json`.
- **Bounded action:** resolve and read-only mount a supported, host-owned Node/npm toolchain at a neutral in-sandbox path; set the exact PATH to it plus required system Git bins; validate compatibility at plan/preflight time. Remove command IDs without repository scripts or define the intended command. Add deterministic exact toolchain/command tests without activating autonomous execution.
- **Decision impact:** `build` is guaranteed to fail under the nominal plan, so the finite command implementation does not satisfy its purpose.

### Validation Receipt — Checkpoint 2b Revision 1

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2b — Bubblewrap implementation without activation, revision 1.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** finite runtime command surface; bwrap/userns fail-closed preflight; clear environment; namespace/network/mount boundary; no control-plane/handoff authority; direct Bash denial; non-activation; structural adversarial tests; KISS.
- **Reviewed files/surfaces:** all four request-listed files, current handoff, complete security sandbox review, current native enforcement placement, package scripts/engines, build output references, worktree Git topology, branch/dirty-tree state, and canonical issue #243.
- **Commands/results:**
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/verificationSandbox.test.ts` — 22/22 passed, but tests do not cover the reproduced unsafe cases.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Reference search — no native launcher/hook/MCP wiring or execution path; implementation remains dormant.
  - Independent plan fixtures — `/` read-write root, regular-file Git root, symlink worktree, and actual `.git` pointer file were accepted; unknown command ID failed with incidental TypeError.
  - Host facts — bwrap is currently a root-owned executable and current namespace sysctls permit use, but the implementation does not prove those conditions fail closed; actual common Git dir differs from the tested `.git` file.
  - Planned toolchain probe — Node 18.19.1 selected; Vite 8 rejects it, while the active project runtime is Node 22.22.3.
- **Skipped checks/reasons:** no bwrap package script, network, secret, Git-write, control-plane, fork/resource, timeout, output-cap, or revocation execution test was run because activation remains human/security-gated. Resource limits, bounded output capture, sanitized sandbox audit fields, executor ownership, and the complete §9 adversarial suite remain activation prerequisites rather than claims of this dormant checkpoint.
- **Edge cases:** hostile/mistyped JSON IDs; symlinked or root mount sources; `.git` pointer versus common/private gitdirs; nested protected paths under a read-write bind; unreadable/missing sysctls; bwrap present but unusable; incompatible system Node; absent package scripts.
- **Regression risks:** next-launch guard overwrite, hook/import rewrite, durable evidence mutation, writable Git pointer, host-root bind expansion, fail-open namespace assumptions, unstable denial reasons, and verification commands that cannot run.
- **Relevant canonical standards checklist summary:** the module is small, flat, and non-activated, and direct Bash remains safely denied. It does not yet provide trusted state ownership, complete fail-closed IO boundaries, deterministic runtime validation, compatible external-tool selection, or adversarial boundary coverage.
- **Findings:** V243-C2B-001 through V243-C2B-005 are open.
- **Required follow-up:** coder applies the five bounded plan/preflight/test corrections without adding native wiring or executing sandboxed agent code, refreshes the handoff, and reruns focused/typecheck/build/diff validation. Activation and live §9 tests remain separately human/security-gated.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; did not run the Bubblewrap verification plan; edited only this verifier-owned report; and used dummy plan inputs plus a host toolchain version probe.
- **Checkpoint compliance/deviation:** implementation stayed within the approved dormant follow-up and did not wire/activate the sandbox. The generated backlog timestamp reappeared during review as the known active-runtime drift. Five plan/preflight defects prevent approval; none requires a new human policy decision.

## Checkpoint 2b re-review — revision 2

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-2 dormant sandbox working tree.
- **Verdict:** `revision_requested`.
- **Scope:** bounded recheck of V243-C2B-001 through V243-C2B-005, non-activation, direct-Bash denial, environment/mount regressions, KISS, and durable evidence.
- **Final review:** no.

### Finding disposition

| Finding | Revision-2 status | Evidence |
| --- | --- | --- |
| V243-C2B-001 | Open | `protectedRoots` is only used to reject a worktree located below a protected root; protected children remain writable and no nested read-only mounts/snapshot exist |
| V243-C2B-002 | Open, partially improved | direct directory symlinks/files and `/` now reject; arbitrary unrelated directories still pass and Git/session relationships remain unverified |
| V243-C2B-003 | Open, partially improved | host adapter and executable-bit check exist; production probe is constant `true` and capability checks remain incomplete |
| V243-C2B-004 | Open, nearly resolved | runtime ID now gets stable `deny_sandbox_start`; required exact denial/argv tests were not added |
| V243-C2B-005 | Open, partially improved | nonexistent `lint` ID removed; nominal PATH still selects incompatible Node 18 |
| V243-C2B-006 | New, open | required temp/worktree environment contract regressed |
| V243-C2B-007 | New, open | durable handoff was not refreshed for revision 2 |
| V243-C2B-008 | New, open | single-responsibility KISS was replaced with compressed multi-purpose lines |

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, and worktree | Pass | Issue #243 independently confirmed; expected branch/worktree; branch still three commits behind `origin/main` |
| Dormant/unwired state | Pass | Source references remain limited to planner tests; no hook, launcher, MCP, or executor wiring and no sandboxed command execution |
| Direct host Bash denial | Pass | 22 focused tests pass and npm/node/Git/metacharacter Bash classifications remain deny |
| Runtime finite ID guard | Partial | Code rejects unknown IDs with a stable reason, but test still accepts any throw and does not assert exact allowed argv |
| Protected/control-plane boundary | Fail | V243-C2B-001 |
| Trusted worktree/Git roots | Fail | V243-C2B-002 |
| Fail-closed host capability preflight | Fail | V243-C2B-003 |
| Clear/no-network nominal namespace shape | Pass with environment regression | `--clearenv`, `--unshare-all`, no `--share-net`, `/sys`, broad home, sockets, or resolver bind; V243-C2B-006 remains |
| Compatible toolchain | Fail | V243-C2B-005 |
| Current handoff evidence | Fail | V243-C2B-007 |
| Explicit KISS review | Fail | Files are below 300 lines and parameter/nesting/comment/dead-code checks otherwise pass, but V243-C2B-008 violates single-responsibility/readability |

### Research consult note

A focused Researcher consult was attempted for V243-C2B-003 while the coder was blocked, but its reply failed the transport response schema and was not relied upon. No raw response was retained. The existing source-cited, host-verified 2026-07-18 security review plus deterministic local evidence is sufficient for this bounded `revision_requested` decision; no human escalation is needed at revision 2.

### Open finding evidence and bounded actions

#### V243-C2B-001 — Critical activation blocker — Protected children remain writable

- **Evidence:** the plan still has one read-write bind of the entire worktree. Passing the real wrapper and `term-control-center/build` as `protectedRoots` adds no read-only bind. The condition checks whether the worktree is equal to/below each protected root, the inverse of the delivered risk. A dummy protected child was accepted and absent from read-only args.
- **Bounded action:** preserve the revision-1 action: move/snapshot the executor, launcher, hook, and import graph into the owner-private external control plane; emit exact nested read-only mounts for every remaining in-worktree protected path, `.git` pointer/private metadata, and durable run evidence; add mount-pair assertions and protected-child negatives.
- **Decision impact:** unchanged; no-control-plane containment is not implemented.

#### V243-C2B-002 — High — Roots still are not session/Git bound

- **Evidence:** `root()` now rejects a direct symlink or non-directory and canonicalizes accepted paths. It still accepts any two unrelated existing directories; independent fixtures passed an arbitrary worktree and unrelated `commonGitDir`. Caller strings are not tied to trusted session state, common Git structure is not verified, and worktree `.git` pointer/private gitdir remain inside the writable bind.
- **Bounded action:** derive/cross-check roots from trusted session context, validate the actual common/private Git relationship and worktree pointer, reject unrelated/overlapping roots and symlinked ancestry, and mount all Git metadata read-only. Add exact unrelated-directory, parent-symlink, mismatched Git, and writable-pointer negatives.
- **Decision impact:** reduced input-shape risk does not close host-scope or Git-boundary risk.

#### V243-C2B-003 — High — Production userns probe is a stub

- **Evidence:** executable bits and injectable host methods are improvements. The production `probe` is `() => true`, so no bwrap/userns capability is exercised. `userns()` checks only one AppArmor sysctl; read/probe exceptions are not normalized to `deny_sandbox_unavailable`, and no injected preflight negatives exist.
- **Bounded action:** implement the bounded no-op bwrap/userns probe or complete equivalent fail-closed checks; normalize unknown/read/probe failures; add missing/non-executable/restricted/zero-namespace/read-error/probe-failure tests using the host adapter.
- **Decision impact:** preflight still assumes the property it must prove.

#### V243-C2B-004 — Medium — Exact finite-command tests are still absent

- **Evidence:** runtime membership now rejects `deploy` with `deny_sandbox_start`, resolving the incidental-TypeError defect in code. The test still uses unqualified `assert.throws`, and nominal tests only check that `--` exists; they do not prove each ID's exact argv or prevent extra arguments.
- **Bounded action:** assert the exact denial message and exact post-`--` argv for every finite ID. Close the finding when those deterministic assertions pass.
- **Decision impact:** the runtime boundary is improved but its finite mapping is not pinned against regression.

#### V243-C2B-005 — Medium — Toolchain remains incompatible

- **Evidence:** `lint` was correctly removed. `PATH=/usr/local/bin:/usr/bin:/bin` still resolves Node 18.19.1/npm 9.2.0 on this host. A repeat probe fails because Vite 8 requires Node `^20.19.0 || >=22.12.0`; the active runtime is Node 22.22.3.
- **Bounded action:** read-only mount a supported host-owned Node/npm toolchain at a neutral sandbox path, select it exactly in both spawn and bwrap environments, and add deterministic version/path/command tests without activating package scripts.
- **Decision impact:** the `build` command remains guaranteed to fail.

#### V243-C2B-006 — Low — Required temporary environment fields were dropped

- **Evidence:** revision 1 set `TMPDIR=/tmp`; revision 2 omits it from both the spawn environment and bwrap `--setenv`, despite the dedicated `/tmp` tmpfs and the security review's exact environment contract. No worktree-path environment is present either.
- **Bounded action:** restore `TMPDIR=/tmp`, add the approved worktree-path name if the executor contract requires it, and assert exact equality of both environment representations so credentials or omissions cannot drift.
- **Decision impact:** `/tmp` remains namespaced, so this is not an active escape, but the approved deterministic environment contract is incomplete.

#### V243-C2B-007 — Medium — Handoff is stale for revision 2

- **Evidence:** the handoff still describes five IDs including removed `lint`, the old signal-only planner, revision-1 validation, and no V243-C2B finding dispositions or revision-2 changes. Its mtime predates this revision request, while the code materially changed.
- **Bounded action:** record revision-2/next-revision status, each finding disposition, exact changed files/validation, remaining activation blockers, and next actor in one current section.
- **Decision impact:** the durable evidence cannot support checkpoint approval.

#### V243-C2B-008 — Medium — Physical line compression violates KISS single responsibility

- **Evidence:** `verificationSandbox.ts` is only 19 physical lines because seven lines are 199–472 characters. `verificationPlan()` performs runtime schema validation, host preflight, path trust, cross-root policy, command construction, mount construction, and environment construction in one compressed block. `root()` compresses validation/stat/realpath into one line. This meets a superficial line count but not the repository's single-responsibility/readability rule.
- **Bounded action:** restore small named helpers for runtime command validation, host preflight, root/Git validation, mount argv, and exact environment construction; format arrays and types normally. Keep each function below 20 lines and the file below 300 without semicolon compression.
- **Decision impact:** mandatory explicit KISS review fails.

## Validation Receipt — Checkpoint 2b Revision 2

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2b — Bubblewrap implementation without activation, revision 2.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** all revision-1 findings; finite runtime IDs; bwrap/userns preflight; trusted mounts; exact environment; compatible toolchain; direct Bash denial; no activation; structural tests; KISS; handoff accuracy.
- **Reviewed files/surfaces:** revised planner/test, autonomy reason codes and Bash classifier, current handoff/report/security design, package engines/scripts, current Git topology, dirty tree, and canonical issue.
- **Commands/results:**
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/verificationSandbox.test.ts` — 22/22 passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Reference search — planner remains dormant/unwired; direct Bash unchanged and denied.
  - Independent revision-1 negatives — stable unknown-ID denial now passes; unrelated roots and protected child remain accepted/unprotected.
  - Nominal plan inspection — no shared network, but no protected nested mounts or `TMPDIR`; only common Git root is read-only.
  - Planned toolchain probe — still selects Node 18 and Vite fails its engine requirement.
  - KISS metrics — source 19 lines with seven 199–472-character compressed lines and multiple responsibilities in `verificationPlan()`.
- **Skipped checks/reasons:** live bwrap/package-script containment, resource/timeout/output/audit/executor tests remain forbidden until the distinct activation gate. No sandbox verification plan was executed.
- **Edge cases:** protected children versus protected ancestors; arbitrary unrelated directories; parent-symlink ancestry; mismatched common/private Git dirs; stubbed production probes; thrown host-adapter errors; extra command argv; environment drift; incompatible Node.
- **Regression risks:** overwrite of next-launch enforcement/evidence, host-scope widening, fail-open capability assumptions, finite-command mapping drift, nonfunctional builds, and unreadable security code.
- **Relevant canonical standards checklist summary:** direct denial and dormant scope remain sound; revision 2 improves runtime IDs, direct path types, and executable checking. Trusted-root ownership, fail-closed capability proof, protected mounts, deterministic environment/toolchain, current evidence, adversarial tests, and KISS still fail.
- **Findings:** V243-C2B-001 through V243-C2B-008 are open.
- **Required follow-up:** coder performs one more bounded revision for these findings, keeps the planner unwired, refreshes the handoff, and reruns focused/typecheck/build/diff checks. If any same security finding survives revision 3, follow the continuation escalation rules; activation remains separately human/security-gated.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; did not execute the Bubblewrap plan; edited only this verifier report; and used dummy root/plan inputs plus a host toolchain compatibility probe.
- **Checkpoint compliance/deviation:** no activation or native wiring occurred. Generated backlog drift reappeared during review as the known active-runtime deviation. Revision 2 is bounded but incomplete; no finding requires a new policy decision.

## Checkpoint 2b re-review — revision 3

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-3 dormant sandbox working tree.
- **Verdict:** `revision_requested`.
- **Scope:** V243-C2B-001 through V243-C2B-008, focused validation, dormant/unwired status, direct host-Bash denial, KISS, and current handoff.
- **Final review:** no.

### Finding disposition

| Finding | Revision-3 status | Evidence |
| --- | --- | --- |
| V243-C2B-001 | Open, substantially improved | nested RO mounts now work, but only one hook file is protected and the build IDs conflict with that mount; external immutable runtime remains absent |
| V243-C2B-002 | Resolved for dormant scope | request contains only command ID; host context derives private/common Git from the trusted linked-worktree gitfile and rejects malformed/unrelated roots |
| V243-C2B-003 | Resolved | root-owned executable checks, strict sysctls, normalized failures, and a real bounded no-op bwrap/userns probe are implemented and tested |
| V243-C2B-004 | Resolved | runtime IDs and exact argv/denials are pinned |
| V243-C2B-005 | Resolved | supported owner-controlled Node 22 prefix is mounted RO at a neutral path; `lint` is removed |
| V243-C2B-006 | Resolved | exact environment restores `TMPDIR` and worktree identity with plan/argv parity |
| V243-C2B-007 | Resolved | handoff is current for revision 3 and records remaining activation boundaries |
| V243-C2B-008 | Resolved | 171-line module uses small named helpers with bounded parameters/nesting and normal formatting |

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical task/branch/worktree | Pass with source-access note | Canonical #243 was independently reviewed earlier in this run; the repeat authenticated `gh` query hit the account API rate limit. Branch/worktree remain correct and three commits behind `origin/main` |
| Dormant/unwired | Pass | no source reference outside the planner/test; no hook, launcher, MCP, or executor activation path |
| Direct host Bash denial | Pass | 24 focused tests pass; npm/node/Git and all other Bash remain denied by the existing hook |
| Finite commands and exact env | Pass | four IDs map to exact npm argv; non-string/unknown inputs deny; six-name environment matches all `--setenv` pairs |
| Host preflight | Pass | production plan construction completed the bounded no-op bwrap probe; injected unavailable/restricted/read/probe failures normalize closed |
| Namespace/network/toolchain shape | Pass for dormant static plan | unshared user/all namespaces, clear env, no shared network/resolver/home/run/sysfs/socket bind, namespaced proc/dev/tmp, RO supported Node prefix |
| Worktree/Git/protected mounts | Partial | worktree is the sole RW real-data bind and Git/evidence/listed paths are nested RO; V243-C2B-001 remains |
| Handoff and generated artifacts | Pass with known qualifier | handoff is current; `.ralph` absent; timestamp-only backlog drift regenerated after the handoff and remains the accepted pre-final deviation |
| KISS | Pass | source/test are 171/114 lines; functions stay below 20 lines with 2–4 parameters, shallow nesting, no redundant comments, and no dead/commented-out code |

### Research consult relied upon

A focused Researcher consult on 2026-07-18 confirmed V243-C2B-001 remains open:

- Bubblewrap applies filesystem operations in argument order, so nested RO mounts protect only the exact destinations named after the RW worktree bind.
- `pretoolHook.js` loads a transitive local module graph; protecting only the entry file leaves sibling enforcement imports writable.
- `build:server` emits the hook and then runs `chmod build/server/*.js`, so a RO-bound hook output makes the allowed build unreliable/nonfunctional.
- The bounded safe resolution is an owner-private external snapshot of the complete enforcement runtime, not mounted into the sandbox; until then, build IDs must not be represented as runnable through this plan.

Sources cited by Researcher: Ubuntu Noble Bubblewrap 0.9 manpage (<https://manpages.ubuntu.com/manpages/noble/man1/bwrap.1.html>) and Node ESM module-graph behavior (<https://nodejs.org/api/esm.html>), checked 2026-07-18. No raw transcript was retained.

### Remaining finding

#### V243-C2B-001 — Critical activation blocker — Protected mount set is incomplete and conflicts with build commands

- **Evidence:** the nominal context RO-binds `.git`, the wrapper, only `term-control-center/build/server/pretoolHook.js`, and run evidence after the RW worktree bind. `pretoolHook.js` imports `autonomyGates`, `autonomyPaths`, `autonomyPolicy`, and `autonomyAudit`, whose built siblings remain writable. The planner itself/executor runtime also remains in the RW worktree. An empty `protectedRoots` context is accepted and protects only `.git`, so mandatory enforcement coverage is caller-conventional rather than structural. Finally, both `build-server` and `build` run `tsc` followed by `chmod build/server/*.js`; the RO hook output blocks their intended write/chmod path.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`, and the future external control-plane snapshot/wiring surface.
- **Bounded action:** choose one bounded dormant resolution before re-review: (A) implement the owner-private external snapshot contract for the planner/executor, wrapper, hook, and full transitive enforcement graph, validate integrity, and keep it outside every sandbox bind; or (B) remove `build-server`/`build` from the dormant command IDs and derive/require the whole current built enforcement root plus wrapper/evidence as mandatory RO paths until the external snapshot lands. Do not accept an empty/partial protected set. Add an assertion that every remaining command's intended outputs do not intersect RO mounts.
- **Decision impact:** all other revision-2 findings close, but the plan still cannot safely and functionally represent the claimed build commands. The module remains harmless only because it is unwired.

## Validation Receipt — Checkpoint 2b Revision 3

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2b — Bubblewrap implementation without activation, revision 3.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** all C2B findings; finite command/runtime schema; trusted linked-worktree Git topology; exact environment; bwrap/userns preflight; supported Node toolchain; nested mounts; direct denial; non-activation; KISS; durable evidence.
- **Reviewed files/surfaces:** revised planner/test/handoff, security design, current wrapper/hook import graph, build scripts, report history, branch/status, current mount plan, and prior canonical PRD evidence.
- **Commands/results:**
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/verificationSandbox.test.ts` — 24/24 passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed on host.
  - `git diff --check` — passed.
  - Production `verificationPlan()` construction — passed the real bounded no-op bwrap/userns probe; no npm/package script was executed.
  - Plan inspection — exact four command argv, six-name environment, one RW worktree, RO common/private Git and supplied protected paths; empty protected set still accepted.
  - Reference search — no native wiring/activation.
  - Researcher consult — confirms incomplete graph protection and build-output/RO conflict.
- **Skipped checks/reasons:** the plan itself and package scripts were not executed under Bubblewrap; network/secret/Git/control-plane/fork/resource/timeout/output/audit tests remain behind the separate human/security activation gate.
- **Edge cases:** empty/partial protected set; transitive ESM import graph; build emit/chmod against RO outputs; future executor restart after worktree overwrite; generated backlog drift; main-branch freshness.
- **Regression risks:** next-session enforcement rewrite, nonfunctional build IDs, treating dormant safety as activation proof, and incomplete mandatory mount coverage.
- **Relevant canonical standards checklist summary:** revision 3 now has clear boundaries, deterministic runtime validation, compatible tool selection, trusted Git derivation, readable KISS structure, and useful adversarial structural tests. One security/functional boundary remains incomplete.
- **Findings:** V243-C2B-001 remains open; V243-C2B-002 through V243-C2B-008 are resolved.
- **Required follow-up:** coder performs the remaining bounded V243-C2B-001 fix while keeping the planner unwired. This is the third permitted bounded fix after the finding; if it survives the next re-review, escalate `needs_human` under the continuation contract. Activation remains separately human/security-gated regardless of checkpoint approval.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; did not execute a sandboxed verification command; edited only this verifier report; and ran only focused host validation plus the bounded production no-op preflight.
- **Checkpoint compliance/deviation:** no activation or native wiring occurred. Generated backlog drift reappeared during review as expected. Revision 3 resolves seven of eight findings; the remaining control-plane/build conflict is bounded and coder-remediable.

## Checkpoint 2b re-review — revision 4

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-4 dormant sandbox working tree.
- **Verdict:** `needs_human`.
- **Why escalation is required:** option B closes the enforcement-graph/build-command conflict, but V243-C2B-001 still has one reproducible mandatory-evidence gap after the permitted bounded revisions and the focused Researcher consult. Per the continuation contract and the coder's own stop record, the verifier cannot silently grant another revision loop.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical PRD, branch, and worktree | Pass | REST-backed `gh api` independently confirmed open approved issue #243; expected branch/worktree; branch remains three commits behind `origin/main` |
| Dormant/unwired status | Pass | no planner reference from launcher, hook, MCP, or server runtime; no sandboxed package command executed |
| Direct host Bash denial | Pass | npm typecheck/test, node, Git, and unmatched Bash all independently classify `deny_always_gate` |
| Finite non-emitting command IDs | Pass | only `typecheck` and `test`; build/build-server/deploy/non-string inputs return `deny_sandbox_start` |
| Mandatory enforcement mounts | Pass | `.git`, wrapper, complete `build/server`, common/private Git, and nominal evidence root are RO after the sole RW worktree bind |
| Mandatory evidence mount fails closed | Fail | V243-C2B-001 |
| Environment, namespace, preflight, toolchain | Pass for dormant plan | exact environment; no shared network/sensitive bind; real no-op bwrap probe; supported Node 22 RO toolchain |
| Focused validation | Pass | 24/24 focused tests, typecheck, host build:server, production no-op plan construction, and diff check passed |
| KISS | Pass | source/test are 175/115 lines; small single-purpose functions, bounded parameters/nesting, no redundant comments or dead code |
| Handoff | Pass with minor typo | revision-4 status and substantive dispositions are current; one bullet says “revision-3 handoff” but does not alter authority or validation |

### Finding disposition

V243-C2B-002 through V243-C2B-008 remain resolved. V243-C2B-001 is narrowed but still open.

#### V243-C2B-001 — Critical activation blocker — Evidence protection is still caller-conventional

- **Evidence:** `SandboxContext.evidenceRoot` remains an arbitrary string. `resolveProtected()` realpaths it and checks only that the resolved target is somewhere inside the worktree; it does not require a non-empty canonical evidence directory or bind it to the active run/session. Independent construction with `evidenceRoot: ''` succeeds because Node resolves the empty path to the current `term-control-center` directory. The plan then RO-binds that unrelated directory while the actual durable run evidence remains writable. Any other existing in-worktree file/directory can likewise substitute for the required evidence root.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/tests/verificationSandbox.test.ts`, and the host-context contract for later wiring.
- **Required human decision:** either authorize one additional bounded correction that derives/cross-checks the active evidence directory from trusted runtime/session context and rejects empty, file, wrong-run, and unrelated in-worktree values, or explicitly accept host-context evidence selection as a bounded exception. The default safe recommendation is the additional fail-closed correction while keeping the planner unwired.
- **Decision impact:** the nominal plan now protects the right roots and build IDs no longer conflict, but the mandatory evidence invariant is not structural. Because this is the same consulted finding after the recorded revision budget, the decision escalates rather than requesting another automatic coder revision.

### Resolved V243-C2B-001 portions

- Build and build-server IDs are removed.
- The entire current `term-control-center/build/server` graph is mandatory RO.
- The native wrapper and `.git` pointer are mandatory RO.
- Common/private Git directories are derived and RO.
- The caller can no longer pass an empty protected-root list.
- External owner-private snapshot and all live containment/resource/audit tests remain explicit activation prerequisites, not checkpoint-2b approval claims.

## Validation Receipt — Checkpoint 2b Revision 4

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2b — Bubblewrap implementation without activation, revision 4.
- **Decision:** needs_human.
- **Final review:** no.
- **Acceptance criteria reviewed:** option-B V243-C2B-001 closure, finite non-emitting commands, mandatory RO roots, dormant state, direct Bash denial, prior resolved findings, KISS, and current evidence.
- **Reviewed files/surfaces:** revised planner/test/handoff, report/research history, current mount plan, native enforcement graph, worktree Git topology, canonical issue, branch/status, and generated drift.
- **Commands/results:**
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/verificationSandbox.test.ts` — 24/24 passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed on the host validation path.
  - `git diff --check` — passed.
  - Production plan construction — real bounded no-op bwrap/userns probe passed; no sandboxed npm command ran.
  - Independent plan inspection — only typecheck/test; one RW worktree; nominal `.git`/wrapper/build/evidence roots RO; exact environment.
  - Independent negative — build/build-server/deploy/non-string commands deny; undefined evidence denies, but empty-string evidence incorrectly succeeds and leaves actual run evidence unprotected.
  - Reference/Bash checks — no native wiring; all host Bash remains denied.
- **Research relied upon:** the revision-3 focused consult confirming ordered nested RO semantics, complete module-graph protection, and build-output conflict; sources were the Ubuntu Noble Bubblewrap 0.9 manpage and Node ESM documentation, checked 2026-07-18.
- **Skipped checks/reasons:** live package-script containment, network/secret/Git/control-plane/fork/resource/timeout/output/audit tests and external runtime snapshot remain behind the separate human/security activation gate.
- **Edge cases:** empty/wrong evidence path; file instead of evidence directory; different run directory; CWD-dependent empty-path resolution; active-runtime backlog regeneration; main freshness.
- **Regression risks:** durable evidence mutation under a malformed future host context and treating dormant plan approval as activation approval.
- **Relevant canonical standards checklist summary:** the implementation is now small, readable, deterministic, fail-closed across command/host/Git/toolchain boundaries, and non-activated. One trusted-context invariant remains non-structural after the bounded retry budget.
- **Findings:** V243-C2B-001 remains open; all other checkpoint-2b findings are resolved.
- **Required follow-up:** human/security reviewer chooses whether to authorize the final evidence-root correction or accept a documented exception. No activation, PR, merge, deployment, or GitHub mutation is authorized.
- **Next actor:** human/security reviewer.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; did not execute a sandboxed verification command; edited only this verifier report; and ran only focused host validation plus the bounded production no-op preflight.
- **Checkpoint compliance/deviation:** no activation or native wiring occurred. Generated backlog timestamp drift reappeared after handoff as expected. Revision 4 resolves the substantive graph/build conflict, but evidence-root trust remains incomplete and has reached the workflow escalation boundary.

## Checkpoint 2b re-review — revision 5

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the revision-5 dormant sandbox working tree.
- **Verdict:** `approved`.
- **Authorization:** the current durable handoff records explicit operator/human-security authorization for one additional fail-closed evidence-root correction after revision 4; activation remains unapproved.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical task/branch/worktree | Pass | REST-backed GitHub issue #243 independently confirmed open/approved; expected branch/worktree; branch still three commits behind `origin/main` |
| Evidence selection is host-derived | Pass | `SandboxContext` contains only the trusted worktree; no evidence path/list is accepted from the command request or context |
| Issue binding is exact | Pass | worktree basename must match `agentops-prd-<digits>` and only `issue-<same digits>-*` entries under the fixed runs root are considered |
| Evidence directories are mandatory and trusted | Pass | zero matches deny; matching entries must be canonical owner directories; wrong-issue and matching-file fixtures deny |
| Evidence mounts are complete | Pass | every matching issue-243 run directory is included in mandatory RO mounts after the RW worktree bind |
| Enforcement/Git mounts remain mandatory | Pass | `.git`, wrapper, full `build/server`, common Git, and private Git remain RO; build/build-server IDs remain absent |
| Dormant/unwired status | Pass | no source wiring from launcher, hook, MCP, or server runtime; no sandboxed npm command executed |
| Direct host Bash denial | Pass | npm/node/Git and unmatched Bash independently remain `deny_always_gate` |
| Focused validation | Pass | 25/25 focused tests, typecheck, host build:server, production no-op plan construction, and diff check pass |
| KISS | Pass | planner/test are 187/128 lines; functions remain small/single-purpose with bounded parameters/nesting, no redundant comments, and no dead code |

### Finding disposition

`V243-C2B-001` is resolved for this dormant checkpoint. The approved correction removes caller evidence selection and derives every matching evidence directory from the trusted issue worktree. All V243-C2B findings are closed.

This approval does **not** activate the planner or approve autonomous verification. The external owner-private runtime snapshot, executor/resource/output/audit controls, and live package-script adversarial suite remain required at the separate human/security activation gate.

## Validation Receipt — Checkpoint 2b Revision 5

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 2b — Bubblewrap implementation without activation, revision 5.
- **Decision:** approved.
- **Final review:** no.
- **Acceptance criteria reviewed:** human-approved V243-C2B-001 correction; derived evidence roots; mandatory RO evidence/enforcement/Git mounts; finite non-emitting commands; dormant state; direct Bash denial; prior C2B findings; KISS; evidence accuracy.
- **Reviewed files/surfaces:** revised planner/test/handoff, report/research history, current mount plan, issue/worktree naming contract, runs directory, enforcement graph, canonical issue, branch/status, and generated drift.
- **Commands/results:**
  - `cd term-control-center && node --import tsx --test tests/autonomyHook.test.ts tests/verificationSandbox.test.ts` — 25/25 passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed on the host validation path.
  - `git diff --check` — passed.
  - Production plan construction — real bounded no-op bwrap/userns probe passed; no sandboxed npm command ran.
  - Independent plan inspection — only typecheck/test; one RW worktree; `.git`/wrapper/full build graph/current issue evidence roots RO; exact environment.
  - Independent negatives — build/build-server/deploy/non-string IDs deny; tests prove zero/wrong-issue/file evidence candidates deny.
  - Reference/Bash checks — no native wiring; all host Bash remains denied.
- **Research relied upon:** the earlier focused consult on ordered nested RO semantics, complete module-graph protection, and build-output conflict; Ubuntu Noble Bubblewrap 0.9 manpage and Node ESM documentation, checked 2026-07-18.
- **Skipped checks/reasons:** live package-script containment, network/secret/Git/control-plane/fork/resource/timeout/output/audit tests and external runtime snapshot remain behind the distinct activation gate.
- **Edge cases:** no matching evidence directory; wrong issue prefix; matching file/symlink/noncanonical directory; multiple matching issue runs; worktree-name mismatch; active backlog regeneration; main freshness.
- **Regression risks:** future wiring could supply an untrusted worktree or mistake dormant approval for activation authority; both remain explicitly gated.
- **Relevant canonical standards checklist summary:** the dormant planner is now compact, readable, deterministic, fail-closed at command/host/Git/toolchain/evidence boundaries, and covered by structural negatives. No exception remains for this checkpoint.
- **Findings:** none open for checkpoint 2b.
- **Required follow-up:** proceed to the next non-activation PRD checkpoint. Do not wire or activate autonomous verification until the separate human/security gate and full containment suite pass. Restore generated backlog drift and handle main freshness before final review.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, sandbox activation, trade, or backtest; accessed no real secret; did not execute a sandboxed verification command; edited only this verifier report; and ran focused host validation plus the bounded production no-op preflight.
- **Checkpoint compliance/deviation:** checkpoint 2b is approved only as dormant implementation. Generated backlog timestamp drift reappeared after handoff as the known active-runtime deviation; no activation or native wiring occurred.

## Checkpoint 3 review — revision 1

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the live-validated, unwired executor working tree.
- **Verdict:** `revision_requested`.
- **Authorization:** the handoff records human approval for live sandbox validation only. This review does not authorize native wiring or activation.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical task/branch/worktree | Pass | REST-backed GitHub issue #243 independently confirmed open/approved; expected branch/worktree; branch remains three commits behind `origin/main` |
| Native activation/wiring remains absent | Pass | executor is imported only by its live test; no launcher, hook, MCP, or server runtime calls it |
| Existing host Bash stays denied | Pass | classifier and structural suite retain deny for npm/node/Git/metacharacter/unmatched Bash |
| Structural/live suite executes | Pass with coverage gaps | 25 structural and 2 live tests pass; C3-001/C3-003/C3-004 identify claims the suite does not prove |
| Public versus validation-only surface | Fail | V243-C3-001 |
| Sanitized enumerated audit | Fail | V243-C3-002 |
| Whole-run termination | Fail | V243-C3-003 |
| Aggregate resource containment | Fail | V243-C3-004 |
| Revocation immediately before launch | Fail | V243-C3-005 |
| Output capture bound | Pass for simple fixture | combined buffer returns exactly 1 MiB and reports `deny_output_limit`; descendant cleanup remains under C3-003 |
| Authorization audit failure blocks launch | Pass | live negative returns `deny_audit_write_failed` before plan execution |
| KISS review | Fail | file/function-size, nesting, comments, and dead-code checks otherwise pass; V243-C3-006 |
| Durable receipt/handoff | Partial | sanitized shape and disabled wiring are accurate; process/resource/validation-surface `passed` claims must be revised with the findings below |

### Research relied upon

A focused Researcher consult on 2026-07-18 concluded:

- Killing negative `systemd-run` PID targets only one Unix process group; `setsid()`/double-fork can leave it. A named non-delegated scope must be killed through the user manager, then verified inactive/cgroup-empty.
- `KillMode=control-group`, `SendSIGKILL=yes`, bounded stop timeout, `OOMPolicy=kill`, and effective scope-property checks are needed for the claimed whole-run boundary.
- `MemoryMax` does not cap disk. `RLIMIT_FSIZE` is a per-file/process limit and does not cap aggregate bytes across many files. Bare bwrap `--tmpfs /tmp` has no configured size cap, and the RW worktree has no quota.

Sources checked/cited 2026-07-18: systemd scope/kill/resource-control documentation, Linux `getrlimit(2)`, and Ubuntu Noble Bubblewrap 0.9 manpage. No raw transcript was retained.

### Open findings

#### V243-C3-001 — High — Validation-only authority is exposed through the production API

- **Evidence:** `VerificationCommandId` and `COMMANDS` include `sandbox-adversarial`, `sandbox-output`, and `sandbox-timeout`; `verificationPlan()` and `runVerification()` accept all three under the ordinary `verification_command` policy. Independent plan construction confirms every validation ID is accepted. `runVerification()` also exposes caller-supplied mutable limits. Separately, the normal `npm test` glob includes `verificationExecutor.live.test.ts`, so the public `test` command will attempt nested live executor/systemd validation inside the sandbox rather than remain an ordinary project test.
- **Affected paths:** `term-control-center/server/verificationSandbox.ts`, `term-control-center/server/verificationExecutor.ts`, `term-control-center/package.json`, live tests.
- **Bounded action:** create a production parser/executor surface that accepts only `typecheck`/`test` with immutable validated limits. Move validation IDs and limit overrides behind a test-only/internal harness that cannot be reached by future native input. Exclude the live executor test from the default/public `npm test` selection. Add negatives proving production `runVerification()` denies all validation IDs and cannot override limits.
- **Decision impact:** wiring the current API exposes deliberate timeout/output/adversary commands and makes the nominal public test path recursive/nonfunctional.

#### V243-C3-002 — High — Arbitrary command strings are persisted before validation

- **Evidence:** `runVerification()` writes the authorization audit before `verificationPlan()` parses the ID. `AuditRecord.command_id` is an unrestricted string and `sanitize()` copies it verbatim. An independent dummy request `NOT_A_SECRET_CANARY_243` returned `deny_sandbox_start` but produced both allow and deny records containing that raw value. A real caller could persist a secret/raw command-like value, contradicting the enumerated audit contract.
- **Affected paths:** `term-control-center/server/verificationExecutor.ts`, `term-control-center/server/autonomyAudit.ts`, tests and activation receipt.
- **Bounded action:** validate to the public command enum before any audit write; type/sanitize `command_id` as that enum; never emit an allow record for an invalid/unlaunched request. Add arbitrary-string/long-string/secret-canary negatives and completion-audit-failure coverage.
- **Decision impact:** the non-negotiable secret-free, enumerated audit boundary is bypassable without launching the sandbox.

#### V243-C3-003 — Critical activation blocker — Timeout/output kill is not cgroup-complete

- **Evidence:** the executor starts an unnamed systemd scope but on timeout/output calls only `process.kill(-child.pid, SIGKILL)`. No trusted unit name, user-manager kill, `KillMode=control-group`, `OOMPolicy=kill`, inactive/cgroup-empty verification, or cleanup-denial state exists. Current timeout/output fixtures contain one simple Node process and do not fork, call `setsid()`, double-fork, or leave a canary-writing descendant.
- **Affected paths:** `term-control-center/server/verificationExecutor.ts`, live fixtures/tests, activation receipt.
- **Bounded action:** use a unique trusted scope name; set and verify control-group kill/OOM/stop/runtime properties; terminate through `systemctl --user ... --kill-whom=all`, wait for inactive, and verify no cgroup PID remains. If manager cleanup/verification fails, disable further verification for the session. Add timeout and output fixtures with setsid/double-fork descendants and assert every host PID/canary is gone.
- **Decision impact:** the executor cannot yet prove that a malicious descendant stops at timeout/output/OOM.

#### V243-C3-004 — Critical activation blocker — Aggregate disk/resource claims are not enforced

- **Evidence:** bwrap uses bare `--tmpfs /tmp`; no `--size` is set. The whole host worktree remains RW without quota. `RLIMIT_FSIZE=1 GiB` only rejects one file above the limit; many sub-limit files can fill `/tmp` or the host worktree. The live fixture tests a single `ftruncate` and a 5 GB `Buffer.alloc` that may fail at Node's buffer limit before proving cgroup OOM behavior. It neither fills aggregate tmpfs/worktree storage nor verifies an OOM sibling is killed. The receipt nevertheless marks file/memory/process limits fully enforced.
- **Affected paths:** `verificationSandbox.ts`, `verificationExecutor.ts`, adversarial fixture/live tests, activation receipt.
- **Bounded action:** use a sized `/tmp` tmpfs; make public typecheck/test worktree read-only with explicitly bounded writable cache/output mounts, or apply and verify a real filesystem/project quota. Keep RLIMIT_FSIZE only as a supplement. Add many-file ENOSPC/quota, OOM-with-sibling, effective scope-property, and cgroup-empty tests; narrow receipt claims until they pass.
- **Decision impact:** an activated malicious test can exhaust host disk despite the claimed limits.

#### V243-C3-005 — High — Revocation can race the synchronous plan/preflight window

- **Evidence:** policy is read once at the start of `runVerification()`, then authorization audit and `verificationPlan()` run before spawn. Plan construction includes a bounded synchronous bwrap probe of up to two seconds. An external operator can revoke during that interval and the command still launches under the stale allow. The live test revokes only between separate invocations, not between check and spawn.
- **Affected paths:** `term-control-center/server/verificationExecutor.ts` and live tests.
- **Bounded action:** parse/build the plan first, then re-read and match policy immediately before the synchronous authorization-audit/spawn sequence; add an injected revocation-between-plan-and-launch test. Preserve the documented limitation that revocation does not cancel an already-running contained action.
- **Decision impact:** kill-switch semantics are not immediate at the actual execution boundary.

#### V243-C3-006 — Medium — Executor/audit test code violates explicit KISS limits

- **Evidence:** `auditRecord()` has seven parameters, above the 3–4 parameter limit, and is compressed into a 351-character return line. The main live-test callback spans more than 20 lines and combines adversary, output, timeout, revocation, and audit assertions. Other files/functions remain below 300/20 lines with shallow nesting and zero redundant comments.
- **Affected paths:** `term-control-center/server/verificationExecutor.ts`, `term-control-center/tests/verificationExecutor.live.test.ts`.
- **Bounded action:** pass a small typed audit-event object/context rather than seven parameters; split the live callback into single-purpose helpers or tests while preserving serial cleanup.
- **Decision impact:** mandatory KISS review fails even though overall module placement/size is reasonable.

## Validation Receipt — Checkpoint 3 Revision 1

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 3 — Bubblewrap executor live validation and activation review, revision 1.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** executor containment; public/test-only command separation; immutable limits; policy/revocation; authorization/completion audit; process-group/cgroup cleanup; memory/process/file/output/time limits; structural/live evidence; dormant native wiring; KISS; final human gate.
- **Reviewed files/surfaces:** all request-listed executor/planner/tests/fixtures/package/receipt files, audit/policy modules, current handoff/security design, build/runtime references, canonical issue, branch/status, and generated drift.
- **Commands/results:**
  - `npm --prefix term-control-center run test:sandbox` — 25/25 structural and 2/2 live passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Reference search — executor remains unwired from native/runtime paths.
  - Independent unknown-ID audit fixture — reproduced raw arbitrary `command_id` in pre-validation allow/deny records.
  - Independent planner check — validation-only IDs are accepted by the same production parser; default test glob includes the live executor test.
  - Researcher process/resource consult — whole-cgroup termination and aggregate disk containment are not established by the current mechanisms/tests.
- **Skipped checks/reasons:** no native wiring or activation was performed; no destructive aggregate-disk or escaped-descendant fixture was run because the safe harness for those tests is itself a requested correction. Full suite/app build, coms smoke, Steward final review, and final bug-check remain later gates.
- **Edge cases:** invalid string containing secrets; validation-only production invocation; mutable/invalid limits; nested live test recursion; revocation during preflight; setsid/double-fork descendants; OOM sibling; many-file disk fill; systemd user-manager cleanup failure; completion audit failure.
- **Regression risks:** secret-bearing audit logs, deliberate DoS command exposure, stale-policy launch, surviving descendants, host disk exhaustion, misleading activation receipt, and future wiring of a test-only seam.
- **Relevant canonical standards checklist summary:** the implementation has good module separation, exact environment/mount planning, bounded output capture, and useful live evidence. It does not yet provide fail-closed production/test separation, enumerated audit input, complete cleanup/resource guarantees, immediate revocation, or KISS compliance.
- **Findings:** V243-C3-001 through V243-C3-006 are open.
- **Required follow-up:** coder applies bounded executor/planner/test/receipt fixes and re-requests security review. Keep native wiring disabled. Even after verifier approval, final activation still requires explicit human/security authorization.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, native wiring, sandbox activation, trade, or backtest; accessed no real secret; used only a dummy audit canary; and ran the already human-authorized live sandbox validation suite.
- **Checkpoint compliance/deviation:** validation authorization was honored and native activation remained off. The sanitized receipt is structurally clean but overstates several activation guarantees; six bounded findings block activation approval.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "3 - Bubblewrap executor live validation and activation review",
  "revision_reviewed": 1,
  "open_findings": 6,
  "finding_ids": [
    "V243-C3-001",
    "V243-C3-002",
    "V243-C3-003",
    "V243-C3-004",
    "V243-C3-005",
    "V243-C3-006"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 3 re-review — revision 2

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the checkpoint-3 revision-2 working tree.
- **Verdict:** `revision_requested`.
- **Scope:** bounded recheck of V243-C3-001 through V243-C3-006 only. Native launcher, hook, MCP, coms, and runtime activation remain forbidden and absent.
- **Authorization:** the durable handoff records operator continuation authorization and human approval for local sandbox validation only. This supports another bounded coder revision, not activation.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and checkpoint agree | Pass | Issue #243 independently retrieved through authenticated `gh`; expected branch/worktree; checkpoint request and durable handoff agree |
| Dirty tree stays within the active PRD run | Pass with known freshness qualifier | Current implementation/test/run artifacts are listed; `dev-plans/prd-backlog.md` is restored; `.ralph/` is absent; the branch remains behind current `origin/main` and final freshness validation is still pending |
| Native activation/wiring remains absent | Pass | Executor/runtime references are confined to the executor modules and focused tests; no launcher, hook, MCP, or server-runtime import reaches `runVerification()` |
| Production command parser is finite | Pass | `runVerification()` validates before audit and accepts only `typecheck`/`test`; validation IDs deny through that parser |
| Validation-only authority is structurally isolated | Fail | V243-C3-001 |
| Default test glob excludes the live executor test | Pass | `tests/*.test.ts` does not expand into `tests/live/` |
| Production command baseline is demonstrated within immutable limits | Fail | V243-C3-001; the handoff records the default suite exceeding 600 seconds while the production limit is 300 seconds, and no production `runVerification()` live pass is present |
| Invalid command audit is sanitized and pre-validation allow is absent | Pass | Invalid secret-canary request returns `deny_sandbox_start` without creating the audit file; runtime sanitizer filters `command_id` |
| Required completion-audit failure path is covered | Fail | V243-C3-002 |
| Named scope and effective resource properties exist | Pass | UUID scope; control-group kill, SIGKILL, stop timeout, runtime/tasks/memory/swap/OOM/delegate properties are set and checked |
| Cleanup verification fails closed on manager errors | Fail | V243-C3-003 |
| Sized aggregate disk and read-only worktree boundary | Pass | Worktree is read-only; validation tmpfs is 16 MiB and many-file fill reaches ENOSPC; production tmpfs is 1 GiB; FSIZE remains supplemental |
| OOM-specific sibling cleanup is proven | Fail | V243-C3-004 |
| Revocation is re-read at the launch boundary | Pass | Policy is re-read after plan/preflight and the injected race produces `deny_policy_revoked` with no allow record |
| Explicit KISS review | Pass | C3 source/test files are 8–220 lines; AST check found maximum 16-line functions and four parameters; nesting is bounded, comments are absent, and no dead/commented-out code was found |
| Focused validation | Pass | 25/25 structural and 7/7 live tests, typecheck, server build, and `git diff --check` pass; no verification scopes remain after the suite |

### Finding disposition

| Finding | Revision-2 status | Evidence |
| --- | --- | --- |
| V243-C3-001 | Open, partially resolved | production parser/default-glob fixes pass; test authority remains exported from production modules and the public `test` ID lacks a passing baseline under its immutable timeout |
| V243-C3-002 | Open, substantially resolved | arbitrary command persistence is fixed; required completion-audit-failure validation remains absent |
| V243-C3-003 | Open, activation blocker | scope naming/properties/kill path improved, but manager verification errors are treated as successful drainage and successful exits are not drain-verified |
| V243-C3-004 | Open, narrowed | aggregate disk/worktree containment is fixed; OOM cause and sibling cleanup are not independently established despite the receipt claim |
| V243-C3-005 | Resolved | second policy read and revocation-in-window test pass |
| V243-C3-006 | Resolved | typed audit event and focused live-test split meet the explicit KISS checks |

### Open findings

#### V243-C3-001 — High activation blocker — Validation authority is still in production modules and the public test profile is unvalidated

- **Evidence:** `verificationSandbox.ts:6,51` exports validation IDs and `validationVerificationPlan()` from the production server module. `verificationExecutor.ts:37` exports `runValidationVerification()`, which accepts a caller-provided plan and mutable `VerificationLimits`; `verificationRuntime.ts:47` also exports direct execution with caller limits. `verificationExecutorTestHarness.ts` is only an eight-line forwarding wrapper, so it does not enforce a module boundary. Its validation planner also has no runtime validation-only membership check; a runtime production ID can traverse that mutable-limit seam. Separately, the handoff records the normal default test suite exceeding a 600-second command budget, while `DEFAULT_VERIFICATION_LIMITS.timeoutMs` is 300,000 and no live pass of either production ID through `runVerification()` is recorded.
- **Affected paths:** `term-control-center/server/{verificationSandbox,verificationExecutor,verificationExecutorTestHarness,verificationRuntime}.ts`, `term-control-center/package.json`, and focused production validation evidence.
- **Bounded action:** keep validation IDs, mutable limits, and arbitrary test plans in a test-only module excluded from the production server build; runtime-validate the validation-only enum. Limit the production-facing module to the finite parser/executor with immutable limits. Demonstrate each retained production ID through the actual production entrypoint under those limits; remove or narrow `test` if the baseline cannot complete within the approved timeout.
- **Decision impact:** the raw native path is still unwired, but the delivered API boundary does not meet the requested production/test separation and one of two proposed production actions has no usable baseline.

#### V243-C3-002 — Medium — Completion-audit failure coverage requested in revision 1 is still absent

- **Evidence:** the invalid command canary now correctly produces no audit, and `autonomyAudit.ts` filters `command_id`. The seven live tests include only `authorization audit failure blocks validation launch`; none makes the authorization record succeed and the completion record fail. The revision-1 bounded action explicitly required completion-audit-failure coverage, while `sandbox-activation-validation.json` broadly records `audit_failure_denied: true`.
- **Affected paths:** `term-control-center/server/verificationExecutor.ts`, `term-control-center/tests/live/verificationExecutor.live.test.ts`, and `sandbox-activation-validation.json`.
- **Bounded action:** add deterministic completion-audit failure injection after a contained command starts, assert the returned enumerated denial and the subsequent fail-closed behavior, and distinguish authorization-only evidence in the receipt until that case passes. Add the requested long invalid command negative while touching this audit boundary.
- **Decision impact:** the original secret-bearing input defect is closed, but the promised failure-path evidence is incomplete and the receipt is broader than the live test.

#### V243-C3-003 — Critical activation blocker — Cleanup verification fails open when systemd-manager inspection fails

- **Evidence:** `verificationRuntime.ts:120-124` ignores the statuses from `systemctl kill` and `stop`. `scopeProperties()` returns `{}` for every nonzero `systemctl show`, and `scopeDrained()` at line 161 treats missing `ActiveState` as successful drainage. Therefore a user-manager/DBus timeout or error across kill/stop/show yields `cleanupVerified: true` and does not add the session to `disabledSessions`, even though no inactive state or empty cgroup was observed. The live suite covers nominal cleanup only and has no injected manager failure. In addition, the `code === 0` branch at line 192 returns allow without a final drain check.
- **Affected path:** `term-control-center/server/verificationRuntime.ts` and live cleanup tests.
- **Bounded action:** isolate systemd-manager IO behind an injectable adapter with status-aware results. Require successful kill/stop and a positively identified inactive/failed, empty-or-absent scope; distinguish a known collected unit from a manager error. On any unverifiable cleanup, disable the session and prove the next same-session call denies. Verify drainage on every completion path, including exit zero.
- **Decision impact:** the requested fail-closed whole-run guarantee is not implemented under the exact cleanup-verification failure it claims to handle.

#### V243-C3-004 — High activation evidence blocker — OOM cleanup receipt is not OOM-specific

- **Evidence:** the OOM fixture prints a sibling identifier, but `assertOomCleanup()` ignores the output and asserts only generic `deny_sandbox_start` plus `cleanupVerified`. Every nonzero sandbox exit maps to that same reason. Neither runtime nor test checks an OOM-specific scope result, `memory.events`/`oom_kill`, or equivalent evidence that memory pressure—not a normal JavaScript/startup failure—killed the run and its sibling. The receipt nevertheless sets `memory_oom_scope_cleanup_verified` to true.
- **Affected paths:** `term-control-center/server/verificationRuntime.ts`, `term-control-center/tests/fixtures/verificationSandboxOom.mjs`, `term-control-center/tests/live/verificationExecutor.live.test.ts`, and `sandbox-activation-validation.json`.
- **Bounded action:** capture a trusted OOM-specific systemd/cgroup signal before scope collection, assert it in the live test together with positively verified empty cgroup cleanup, and fail if the fixture exits through an ordinary exception/nonzero path. Until then set the receipt claim false or explicitly mark it unproven. The sized tmpfs and read-only worktree portions of this finding need no further change.
- **Decision impact:** aggregate disk exhaustion is now contained, but the claimed memory/OOM whole-scope validation is not established for activation review.

### Resolved finding evidence

- **V243-C3-005:** plan/preflight completes before the second policy read; revocation injected in that interval returns `deny_policy_revoked`, writes no allow record, and launches no sandbox command.
- **V243-C3-006:** `AuditEvent` replaces the seven-parameter audit helper, and seven single-purpose serial live tests replace the combined callback. All changed C3 files, functions, nesting, parameters, comments, and dead-code checks pass.

### Validation Receipt — Checkpoint 3 Revision 2

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 3 — Bubblewrap executor live validation and activation review, revision 2.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** production/test-only command separation; immutable limits; enumerated audit and audit failures; named systemd scope; whole-cgroup termination; effective resource properties; aggregate disk and memory containment; launch-boundary revocation; focused live evidence; dormant wiring; KISS; durable receipt.
- **Reviewed files/surfaces:** all request-listed C3 implementation/tests/fixtures/package/evidence files, current handoff, prior C3 findings, canonical issue #243, security sandbox review, current branch/worktree/status, reference graph, and active systemd-unit state.
- **Commands/results:**
  - `npm --prefix term-control-center run test:sandbox` — passed, 25 structural plus 7 live.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed.
  - `git diff --check` — passed.
  - Default glob expansion — confirmed `tests/live/verificationExecutor.live.test.ts` is excluded.
  - Reference search — no native launcher/hook/MCP/coms/server runtime reaches the executor.
  - Systemd scope inventory before/after — no `agentops-verify-*.scope` remains after the suite.
  - AST KISS check — files below 300 lines, maximum 16-line function and four parameters, zero comments in C3 files.
- **Skipped checks/reasons:** the known over-600-second default suite was not repeated; no native wiring/activation was performed; no final Steward review or bug-check applies because later PRD checkpoints remain and this checkpoint is not approved.
- **Edge cases:** future import of mutable validation seams; baseline test exceeding immutable timeout; transient completion-audit failure; systemd kill/stop/show failure; collected unit versus manager error; successful exit with residual scope; generic nonzero versus cgroup OOM; receipt overstatement.
- **Regression risks:** future native wiring accidentally importing a test seam, unusable production verification, unrecorded completion, surviving cgroup members after manager failure, false cleanup success, and an ordinary nonzero failure being accepted as OOM containment proof.
- **Relevant canonical standards checklist summary:** finite production parsing, path/environment containment, sized temporary storage, revocation ordering, and KISS improved materially. Explicit production/test boundaries, deterministic audit-failure evidence, fail-closed side-effect cleanup, and honest OOM observability remain incomplete. No exception is recorded or accepted.
- **Findings:** V243-C3-001, V243-C3-002, V243-C3-003, and V243-C3-004 remain open; V243-C3-005 and V243-C3-006 are resolved.
- **Required follow-up:** coder applies one bounded revision for the four remaining C3 findings, keeps all native wiring disabled, narrows the receipt to proven facts, and reruns focused/typecheck/build/diff validation plus production-entrypoint checks. Continuation authorization permits this revision loop.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, native wiring, sandbox activation, trade, or backtest; accessed no secret; edited only this verifier-owned report; and ran only the already authorized local validation suite and read-only checks.
- **Checkpoint compliance/deviation:** live validation authorization and dormant status were preserved. The branch freshness gap remains a later human-gated final-validation issue. Four bounded gaps prevent checkpoint-3 approval and do not authorize activation.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "3 - Bubblewrap executor live validation and activation review",
  "revision_reviewed": 2,
  "open_findings": 4,
  "finding_ids": [
    "V243-C3-001",
    "V243-C3-002",
    "V243-C3-003",
    "V243-C3-004"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 3 re-review — revision 3

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the checkpoint-3 revision-3 working tree.
- **Verdict:** `revision_requested`.
- **Scope:** remaining V243-C3-001 through V243-C3-004 only, with regression checks for C3-005/C3-006. Native/autonomous activation remains forbidden and absent.
- **Authorization:** the durable handoff retains operator continuation authorization and human approval for local sandbox validation only.
- **Final review:** no.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and checkpoint | Pass | Authenticated `gh` independently confirms open issue #243; expected branch/worktree; branch is three commits behind `origin/main`, a later final-validation gate |
| Dirty-tree and forbidden-scope hygiene | Pass | Current PRD implementation/tests/run evidence remain expected; `dev-plans/prd-backlog.md` is clean; `.ralph/` is absent; no native wiring or forbidden action occurred |
| Finite production API and immutable command | Pass | Production accepts only `typecheck`; `test` and every validation ID deny; the actual production entrypoint passes live under the 300-second fixed limit |
| Validation-only IDs and plan transformation excluded from build | Pass | They live under `tests/support`; clean `build:server` leaves no `build/tests` or validation harness artifact |
| Invalid command and audit failure coverage | Pass | Long/validation IDs create no audit; authorization failure blocks launch; completion failure returns denial and the persistent audit failure blocks the next request |
| Systemd status and natural-exit drainage | Pass in code/nominal live path | Kill/stop statuses are checked; manager inspection is structured; known cgroup fallback is required; natural production typecheck returns only after drainage |
| Disabled-session audit is deny-only | Fail | V243-C3-003 |
| Production timeout/output/OOM lifecycle is live-tested | Fail | V243-C3-003 and V243-C3-004 |
| OOM-specific result and empty-scope evidence | Pass for the test-only executor, fail for shipped runtime | Test harness observes `Result=oom-kill` and drainage; V243-C3-004 remains for production evidence |
| Revocation boundary | Pass | Second policy read remains immediately after plan/preflight; injected revocation launches nothing |
| KISS review | Partial | All reviewed files are 81–260 lines, functions max at 16 lines, parameters max at four, nesting/comments/dead code pass; V243-C3-003/C3-004 cover the avoidable duplicate 167-line lifecycle implementation in the test harness |
| Validation commands | Pass | 25/25 structural and 10/10 live, typecheck, clean server build, build-output exclusion check, and `git diff --check`; no verification scope remains |

### Finding disposition

| Finding | Revision-3 status | Evidence |
| --- | --- | --- |
| V243-C3-001 | Resolved | only live-proven `typecheck` remains public/immutable; test IDs and transforms are runtime-enumerated, test-only, and excluded from the server build |
| V243-C3-002 | Resolved | long invalid IDs, authorization-audit failure, completion-audit failure, and persistent fail-closed behavior are covered |
| V243-C3-003 | Open, narrowed | manager/drain mechanics improved, but a disabled session receives a false allow audit and timeout/output live tests exercise a duplicate executor rather than production lifecycle code |
| V243-C3-004 | Open, narrowed | OOM-specific evidence passes only through the duplicate test executor; shipped OOM handling is not exercised despite the unqualified receipt claim |
| V243-C3-005 | Resolved, no regression | launch-boundary reread remains in place |
| V243-C3-006 | Resolved for numeric/comment/dead-code rules | prior audit helper/test split remains compliant; duplicate execution logic is addressed under the still-open lifecycle findings |

### Open findings

#### V243-C3-003 — High activation blocker — Disabled sessions are audited as allowed, and lifecycle negatives validate a duplicate executor

- **Evidence:** `runCommand()` in `verificationExecutor.ts` writes the authorization allow record before invoking `prepared.run(session)`. The first `disabledSessions.has(session)` check is inside `executePrepared()` in `verificationRuntime.ts`, after that audit. An independent manager-failure probe produced the sanitized sequence `allow, deny, allow, deny`: the second request was correctly not spawned but was still recorded as `allow_verification_command` before its denial. The committed manager-failure test checks only the returned reason, not its audit. Separately, timeout and output tests call `runSandboxValidation()`, whose `tests/support/verificationValidationHarness.ts` contains its own spawn, scope args, capture, timeout, kill/stop, cgroup, and finish implementation. They do not execute production `verificationRuntime.ts` timeout/output paths.
- **Affected paths:** `term-control-center/server/{verificationExecutor,verificationRuntime}.ts`, `term-control-center/tests/support/verificationValidationHarness.ts`, and `term-control-center/tests/live/verificationExecutor.live.test.ts`.
- **Bounded action:** move the disabled-session guard ahead of the authorization allow audit and retain a second pre-spawn check; assert the next same-session request creates no allow record and spawns nothing. Replace the duplicate test executor with a test-only plan/limit adapter over the single shipped lifecycle implementation, while keeping validation IDs/transforms absent from the public native entrypoint and production build surface. Exercise timeout/output cleanup through that exact lifecycle.
- **Decision impact:** execution itself stays closed, but the audit falsely records authorization after the session kill switch has disabled verification, and the principal whole-scope negative evidence does not cover the code proposed for later activation.

#### V243-C3-004 — High activation evidence blocker — OOM validation exercises the harness clone, not production OOM handling

- **Evidence:** `assertOomCleanup()` calls the test-only `runSandboxValidation()`. That harness independently spawns `systemd-run`, reads `Result`, and drains the cgroup. Production `verificationRuntime.ts` has a separate `finish()` OOM/result/drain path which no live OOM test reaches; production is exercised only by successful typecheck and mocked manager-inspection failure. The receipt records unqualified `memory_oom_scope_cleanup_verified: true`, so it overstates shipped-executor evidence even though the harness result itself is valid.
- **Affected paths:** `term-control-center/server/verificationRuntime.ts`, `term-control-center/tests/support/verificationValidationHarness.ts`, `term-control-center/tests/live/verificationExecutor.live.test.ts`, and `sandbox-activation-validation.json`.
- **Bounded action:** run the OOM fixture through the same lifecycle implementation used by production, with only validation command/limit selection supplied from excluded test support. Require `Result=oom-kill` plus positive cgroup drainage and ordinary-nonzero rejection on that path. Until then qualify the receipt as harness-only or set the production claim false.
- **Decision impact:** the operating-system mechanism works in the test clone, but the proposed production executor's OOM classification/cleanup remains unvalidated for activation review.

### Resolved finding evidence

- **V243-C3-001:** `VERIFICATION_COMMAND_IDS` is now only `typecheck`; production live completion passes in about five seconds; test-only IDs/transforms are under `tests/support`, runtime-validated, and absent after a clean production build.
- **V243-C3-002:** a 100,000-character ID and validation ID produce no audit; authorization failure blocks before spawn; a completion audit made unwritable after authorization returns `deny_audit_write_failed`, and the next request remains blocked.

### Validation Receipt — Checkpoint 3 Revision 3

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 3 — Bubblewrap executor live validation and activation review, revision 3.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** test-only isolation; immutable production entrypoint; audit enumeration/failures; status-aware systemd cleanup; session disable; timeout/output/OOM evidence; aggregate storage; revocation; dormant wiring; KISS; receipt accuracy.
- **Reviewed files/surfaces:** all request-listed revision-3 source/tests/support/fixture/package/tsconfig/evidence paths, current handoff, prior findings, canonical issue, security sandbox review, build output, branch/status, reference graph, and systemd unit state.
- **Commands/results:**
  - `npm --prefix term-control-center run test:sandbox` — passed, 25 structural plus 10 live.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed from a clean server/test output state.
  - Build search — no compiled tests or validation harness remains.
  - `git diff --check` — passed.
  - Production manager-failure audit probe — both first failure and second disabled request produced allow+deny pairs; second request did not spawn.
  - Reference search — validation harness is referenced only from tests; native launcher/hook/MCP/coms/server runtime do not reach the executor.
  - AST KISS check — all files below 300; maximum 16-line function and four parameters; no comments or dead/commented-out code found.
  - Systemd inventory before/after — no `agentops-verify-*.scope` remains.
- **Skipped checks/reasons:** no native wiring/activation; no final Steward review or bug-check because checkpoint 3 remains open and later PRD checkpoints remain. The prior focused Researcher consult already covers systemd whole-cgroup requirements; no second consult was made for the same findings.
- **Edge cases:** cleanup-disabled but valid next command; false allow audit before in-memory guard; future drift between duplicated executors; production timeout/output/OOM path regressions invisible to harness tests; ordinary nonzero versus OOM; build exclusion versus shared runtime testability.
- **Regression risks:** audit claiming launch authority where none existed, dormant activation based on a test clone, divergence in manager-error handling, and untested production OOM/timeout/output cleanup.
- **Relevant canonical standards checklist summary:** public/test command separation, immutable entrypoint, IO status handling, audit failure coverage, file/function limits, and clean build placement are improved. One source of lifecycle truth and accurate deny-only observability remain mandatory; the duplicated side-effect engine is not accepted as proof of the shipped runtime.
- **Findings:** V243-C3-003 and V243-C3-004 remain open; V243-C3-001 and V243-C3-002 are resolved.
- **Required follow-up:** coder applies one further bounded revision to share the actual lifecycle, moves session disable before allow audit, narrows or corrects the receipt, and reruns the same checks. Keep native wiring disabled. If the same findings survive the next bounded fix, follow the continuation escalation rule rather than extending the loop silently.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, native wiring, sandbox activation, trade, or backtest; accessed no secret; edited only this verifier-owned report; and ran only the human-authorized local sandbox suite plus sanitized temporary probes.
- **Checkpoint compliance/deviation:** live-validation authorization and dormant status were preserved. Two bounded activation-evidence defects remain; no activation authority is implied.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "3 - Bubblewrap executor live validation and activation review",
  "revision_reviewed": 3,
  "open_findings": 2,
  "finding_ids": [
    "V243-C3-003",
    "V243-C3-004"
  ],
  "bug_check_status": "not_applicable",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 3 re-review — revision 4

- **Reviewed revision:** base `2e80015f72b3fa5abeebd6967715674997afe540` plus the checkpoint-3 revision-4 working tree.
- **Verdict:** `approved`.
- **Scope:** final bounded recheck of V243-C3-003 and V243-C3-004, with regression checks for C3-001/C3-002/C3-005/C3-006.
- **Authorization:** human-authorized local sandbox validation only. This approval does not authorize native wiring, autonomous execution, PR creation, deployment, or any other forbidden action.
- **Final PRD review:** no; later contract/live validation, Steward, freshness, and final bug-check gates remain.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and checkpoint | Pass | Authenticated `gh` independently confirms open issue #243; expected branch/worktree; branch remains three commits behind `origin/main` for later final validation |
| Dormant/unwired state | Pass | No launcher, hook, MCP, coms, or server runtime reaches `runVerification()`; direct host Bash remains unchanged and denied |
| One shipped scope lifecycle | Pass | Production runtime and excluded test adapter both call `verificationScopeLifecycle.runScopeLifecycle()`; the duplicate systemd/output/timeout/OOM engine is removed |
| Validation authority remains bounded | Pass | Production parser exposes only immutable `typecheck`; validation IDs, finite cases, plan transformation, and alternate limits remain in `tests/support` and are absent from a clean server build |
| Disabled-session pre-authorization guard | Pass | Executor checks before policy/allow audit and again immediately before the allow audit; shared lifecycle checks synchronously before spawn |
| Disabled-session audit/spawn negative | Pass | Manager failure disables the session; the next request adds no allow record and a mocked spawn is never called |
| Status-aware cleanup | Pass | Manager errors fail closed; forced termination checks kill/stop plus known inactive/failed drained scope; collected-unit fallback requires known cgroup evidence |
| Successful/timeout/output cleanup | Pass | Production success and validation timeout/output execute the same shipped lifecycle and require verified drainage |
| OOM-specific evidence | Pass | Shared lifecycle requires the unique scope's `Result=oom-kill`, inactive/failed state, `OOMPolicy=kill`, and separately verified known-cgroup drainage |
| Audit/revocation regressions | Pass | Invalid/long IDs remain unaudited; authorization/completion failures deny; policy is re-read after planning; validation revocation launches nothing |
| KISS review | Pass | C3 files are 20–274 lines; AST check found maximum 17-line functions and four parameters; nesting is bounded, comments are absent, duplicate lifecycle code is removed, and no dead/commented-out code remains |
| Repository hygiene | Pass for checkpoint | `dev-plans/prd-backlog.md` is clean, `.ralph/` absent, build output excludes test support, and no verification scope remains |

### Finding disposition

| Finding | Revision-4 status | Evidence |
| --- | --- | --- |
| V243-C3-003 | Resolved | deny-only disabled-session audit/no-spawn behavior and exact shared-lifecycle timeout/output/success/manager cleanup pass |
| V243-C3-004 | Resolved | OOM runs through the shipped lifecycle and proves trusted OOM result plus drained cgroup |
| V243-C3-001 | Resolved, no regression | finite immutable production command and excluded validation adapter remain intact |
| V243-C3-002 | Resolved, no regression | invalid input and both audit-failure phases remain covered |
| V243-C3-005 | Resolved, no regression | launch-boundary policy reread remains intact |
| V243-C3-006 | Resolved, no regression | explicit KISS limits and focused tests pass |

No findings remain open for checkpoint 3.

### Research relied upon

The durable handoff records a bounded Researcher consult dated 2026-07-18. Its recommended boundary is reflected in the approved implementation: one shipped generic scope lifecycle with no command-ID, policy, or audit authority; excluded finite validation cases; pre-audit and pre-spawn disabled checks; and OOM evidence bound to `Result=oom-kill`, verified OOM policy/state, and known-cgroup drainage. Sources recorded in the handoff are systemd scope/resource-control documentation, Linux cgroup-v2 documentation, and Node 22 test-runner documentation. No raw transcript was retained.

### Validation Receipt — Checkpoint 3 Revision 4

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 3 — Bubblewrap executor live validation and activation review, revision 4.
- **Decision:** approved.
- **Final review:** no.
- **Acceptance criteria reviewed:** shared shipped lifecycle; finite/excluded validation adapter; disabled-session deny-only audit/no spawn; status-aware cleanup; successful/timeout/output/OOM drainage; OOM-specific evidence; audit/revocation regressions; dormant wiring; KISS; evidence accuracy.
- **Reviewed files/surfaces:** all request-listed revision-4 source/test/support/evidence files, current handoff, previous C3 findings, canonical issue, security sandbox review, production build output, reference graph, branch/status, and systemd scope state.
- **Commands/results:**
  - `npm --prefix term-control-center run test:sandbox` — passed, 25 structural plus 10 live.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build:server` — passed from a clean server/test output state.
  - Build search — no compiled tests or validation harness present.
  - `git diff --check` — passed.
  - Reference search — production and test support share `runScopeLifecycle`; no native/runtime activation reference exists.
  - AST KISS check — files below 300 lines, maximum 17-line function and four parameters, zero comments in C3 files.
  - Systemd inventory before/after — no `agentops-verify-*.scope` remains.
  - Backlog hygiene — no `dev-plans/prd-backlog.md` diff.
- **Skipped checks/reasons:** no native activation/wiring was attempted; full default suite remains intentionally absent from the production command surface; Steward final review, branch freshness handling, later native↔Codex validation, and final bug-check belong to subsequent gates.
- **Edge cases:** cleanup failure before/after scope collection; disabled-session request before policy and before spawn; collected unit with known cgroup; ordinary nonzero versus OOM; timeout/output descendants; validation adapter accidentally entering production build.
- **Regression risks:** future import of the internal generic lifecycle by an agent-facing input path, future command/limit expansion without review, or treating dormant containment approval as activation authority. These remain guarded by later wiring/human review, not silently accepted.
- **Relevant canonical standards checklist summary:** one lifecycle source, finite input ownership, synchronous fail-closed guards, status-aware side-effect cleanup, enumerated observability, deterministic IO-boundary tests, clean test/build separation, and KISS now pass for this checkpoint. No exception is accepted.
- **Findings:** none open for checkpoint 3.
- **Required follow-up:** proceed only to the next PRD checkpoint. Keep the executor dormant until a separate explicit human activation decision. Complete later contract/live validation, Steward cleanup, branch freshness handling, and final bug-check before final approval.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier created no PR, GitHub mutation, push, merge, deployment, approval, native wiring, sandbox activation, trade, or backtest; accessed no secret; edited only this verifier-owned report; and ran only the human-authorized local sandbox suite plus read-only checks.
- **Checkpoint compliance/deviation:** checkpoint 3 now meets its bounded containment/executor evidence requirements. Approval is for dormant implementation and validation only; activation remains forbidden.

## Machine Status

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "3 - Bubblewrap executor live validation and activation review",
  "revision_reviewed": 4,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "not_applicable",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 final safety review — revision 1

- **Reviewed revision:** `91ba35b7fec05827feba3a869881b7c7cd4de797` plus the current handoff update and untracked sanitized native-coms receipt.
- **Verdict:** `revision_requested`.
- **Final PRD review:** no; this final-checkpoint attempt found one sandbox lifecycle bug and one live-validation evidence gap.
- **Bug-check:** completed over the final touched-file scope; two findings remain open.
- **Authorization:** the durable handoff records operator continuation authorization. These are bounded code/test/evidence corrections; no new authority or human-policy decision is required.

### Findings

#### V243-C4-001 — High — Natural command exit can return while a detached descendant remains in the verification scope

- **Confidence:** confirmed.
- **Location:** `term-control-center/server/verificationScopeLifecycle.ts:218-231`; missing edge coverage in `term-control-center/tests/live/verificationExecutor.live.test.ts:32-68`.
- **Trigger:** a contained command starts a `setsid`/detached descendant and its main process then exits normally, with either zero or nonzero status, before timeout, output-limit, or OOM handling runs.
- **Failure mechanism:** the natural-close branch only calls `finalizeKnownScope()`. When the scope is still active, that helper reports `cleanupVerified: false`, but the branch never calls `terminateScope()` before resolving. The forced timeout/output paths do call termination. A bounded verifier fixture reproduced a returned `deny_sandbox_start`/`cleanupVerified:false` while the named scope remained active with a live `sleep` process in its cgroup. The verifier then stopped the fixture scope and confirmed no test scope remained.
- **Impact:** a command can continue consuming bounded sandbox resources after its caller has received a terminal result. This violates the claimed whole-run lifecycle and the final safety requirement even though network, credentials, and real-data writes remain contained and the session is disabled.
- **Coverage:** missing test — a shared-lifecycle validation case whose parent exits zero and nonzero after creating a detached descendant, asserting the result is not returned until the cgroup is drained.
- **Bounded action:** on every natural close, positively drain the scope; if it is not already drained, terminate the full scope and verify inactive/failed plus empty/missing cgroup before resolving. Preserve fail-closed session disabling when termination or verification fails. Add the zero/nonzero detached-descendant live cases through the shipped lifecycle.
- **Decision impact:** final bug-check cannot approve the lifecycle or later activation while a descendant can outlive the returned result.

#### V243-C4-002 — Medium — The live-coms receipt does not prove the deterministic responder lifecycle required by the PRD

- **Confidence:** confirmed evidence gap.
- **Location:** `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/native-coms-validation-243.md` and the corresponding final handoff claim.
- **Trigger:** final approval relies on the receipt as proof of acceptance criteria 4 and 5.
- **Failure mechanism:** the receipt proves same-worktree discovery, a short timeout, pending state, later schema-conforming completion, and correlation from the caller side. It does not identify a deliberate/controlled responder delay, explicitly record that the responder used one normal Pi correlated response rather than `coms_send`, or demonstrate that the verifier resumed bounded availability after responding. The validation verifier's launch contract required resumed availability, but a post-run isolated-pool discovery check found no live peer.
- **Impact:** the run shows an observed timeout-first round trip, but not the deterministic timeout method and complete responder lifecycle that make the result repeatable and contract-conformant.
- **Coverage:** missing validation evidence — controlled delayed response, exactly-one normal-response classification, no reply-via-`coms_send`, and post-response availability discovery.
- **Bounded action:** rerun the same sanitized local validation with an explicit bounded delay longer than the caller's short await. Record only structural states proving one correlated normal Pi response, no `coms_send` reply, and successful post-response same-pool discovery after the verifier resumes availability. Retain no prompt, response, token, or transcript content.
- **Decision impact:** PRD acceptance criteria 4 and 5 are not yet durably demonstrated.

### Atomic final checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and checkpoint agree | Pass | REST-backed `gh api` independently retrieved open PRD #243; expected worktree and `prd/native-session-coms-followup-243` branch |
| Branch freshness | Pass | `HEAD^` equals current `origin/main` (`cf008400...`); branch is exactly one local checkpoint commit ahead and zero behind |
| Current dirty scope | Pass with expected verifier activity | Before this report update, only the current handoff and co-located native-coms receipt were uncommitted; no backlog or `.ralph` drift existed |
| Global bypass and authority boundaries | Pass | Native wrapper still rejects bypass/settings substitution; no push, PR, merge, deploy, GitHub mutation, trading, backtest, activation, or native verification wiring occurred |
| Project-scoped default deny, kill switch, audit, secret/path/env boundaries | Pass | Prior approved checkpoints remain unchanged; focused structural tests pass and current code inspection found no regression |
| Sandbox command, mount, environment, audit, timeout/output/OOM boundaries | Pass except natural-close lifecycle | Finite immutable `typecheck`, test-only harness exclusion, read-only worktree/Git/evidence, exact child environment, and existing live negatives pass; V243-C4-001 remains |
| Native Claude→Codex same-worktree correlation | Partial | Caller-side receipt proves discovery/timeout/pending/completion/schema/correlation; V243-C4-002 remains for deterministic delay and responder lifecycle |
| Steward and placement hygiene | Pass | Durable handoff records a clean Steward review; independent changed-path, generated-output, JSON/Markdown, build-exclusion, and KISS checks found no placement drift |
| Explicit KISS review | Pass | Product files are below 300 lines; changed functions remain below 20 lines with at most four parameters and bounded nesting; comments record the umask constraint; no dead/commented-out code was found |
| Final bug-check | Fail with findings | Fast, silent-failure, and edge-case passes found V243-C4-001 and V243-C4-002; no broad tool escalation was needed after direct source verification and bounded reproduction |

### Bug-check summary

- **Scope:** all 27 implementation/test files in `91ba35b`, immediate launcher/policy/audit/sandbox call edges, eight committed run-evidence files, and the current native-coms receipt/handoff.
- **Review lanes:** fail-closed policy/configuration; trust and secret boundaries; process/systemd lifecycle; silent failure/cleanup; timeout, output, OOM, audit failure, revocation, missing config, invalid IDs, symlinks, detached descendants, and correlated coms lifecycle.
- **Fast pass:** no new permissive fallback, settings bypass, raw host Bash path, production validation ID, inherited environment leak, writable Git/control/evidence mount, or production test-harness import was found.
- **Silent-bug pass:** natural-close cleanup was the surviving candidate and was confirmed by a bounded fixture; audit/config errors otherwise surface as denials rather than false success.
- **Edge-case pass:** existing tests cover missing/malformed/revoked policy, secret/config paths, symlinks, audit failures, timeout, output cap, OOM, manager failure, and launch-time revocation. Natural zero/nonzero exit with a detached descendant is missing. The live-coms receipt covers timeout/pending/completion but not deterministic responder delay or resumed availability.
- **Tool escalation:** Semgrep/CodeQL/fuzzing were not warranted; both surviving issues are local control-flow/evidence defects confirmed directly. The earlier source-cited systemd researcher consult already defines the required full-cgroup drainage boundary and was relied upon without a new query.

### Validation Receipt — Checkpoint 4 Revision 1

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 4 — final safety review, revision 1.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** recorded security decisions and global-bypass rejection; project-scoped default deny/kill switch/always-gates; explicit option-B coms mapping; same-pool correlation; timeout-first behavior; audit secrecy; branch freshness; Steward hygiene; no authority regression; final bug-check.
- **Reviewed files/surfaces:** canonical issue and context brief; complete commit/touched scope; current handoff and both validation receipts; prior verifier findings/history; native wrapper/settings/hook/policy/audit/path classifier; sandbox planner/executor/scope lifecycle; live and structural tests; package/build configuration; final reference graph and generated output.
- **Commands/results:**
  - `gh api repos/hyperbotsx/agentops-harness/issues/243` — passed; GraphQL `gh issue view` was skipped after the account rate limit, with REST as the authenticated source.
  - branch/status/base checks — passed: `91ba35b...`, one ahead/zero behind, parent equals `origin/main`.
  - `npm --prefix term-control-center run test:sandbox` — passed: 25 structural and 10 live tests.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed; only the recorded non-failing Vite static-script/chunk warnings appeared.
  - `git diff --check` — passed; JSON evidence parsed; Markdown trailing-whitespace checks passed; server build excludes tests/validation harness.
  - verifier isolation note — a `json.tool` invocation briefly treated the canary path as its output path and replaced it with another sanitized receipt; the verifier immediately restored it byte-for-byte from reviewed `HEAD`, parsed both files separately, and confirmed no canary diff remains.
  - post-suite `systemctl --user list-units 'agentops-verify-*' --all` — empty.
  - bounded natural-exit descendant fixture — confirmed V243-C4-001; fixture process/scope was stopped and the final scope inventory was empty.
  - isolated validation-pool post-run discovery — no live peer, confirming the V243-C4-002 availability evidence gap.
- **Skipped checks/reasons:** the full default `npm test` was not repeated because the approved production surface intentionally removed the previously over-budget `test` ID and the PRD-focused 35-test sandbox suite passed. No activation, native verification wiring, push, PR creation, deployment, external network test, or raw transcript retention was performed. Broad static-analysis escalation was unnecessary for the confirmed local defects.
- **Edge cases:** detached descendants after natural zero/nonzero exit; systemd scope collection versus active cgroup; cleanup verification failure; completion audit failure; invalid/long IDs; revocation during planning; timeout/output/OOM; same-pool delayed response; exactly-one normal reply; post-response peer availability.
- **Regression risks:** a sandbox process outliving its returned result; activation based on incomplete whole-scope evidence; non-repeatable timeout-first validation; a responder appearing complete without resuming standing-peer availability.
- **Relevant canonical standards checklist summary:** placement, modular boundaries, fail-closed configuration, secret-free observability, deterministic focused testing, and numeric KISS limits pass. Complete side-effect cleanup and deterministic IO-boundary evidence remain required; no exception is accepted.
- **Findings:** V243-C4-001 and V243-C4-002 are open.
- **Required follow-up:** coder applies the natural-close cleanup/test correction and reruns the bounded deterministic native-coms validation with complete sanitized responder lifecycle evidence. Then rerun focused validation and request checkpoint-4 revision 2.
- **Next actor:** coder.
- **Forbidden-action confirmation:** no coder-owned change is retained; the transient canary overwrite described above was restored exactly before the decision. The verifier retained edits only to this report, removed temporary fixtures, created no PR, GitHub mutation, commit, push, merge, deployment, approval, activation, trade, or backtest, and retained no raw prompt/response/transcript or secret.
- **Checkpoint compliance/deviation:** branch freshness, prior checkpoint approvals, Steward hygiene, and authority boundaries pass. The restored verifier tooling mistake is recorded as a non-retained process deviation. Final approval is withheld solely for the two bounded findings; continuation authorization permits the normal revision loop.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - final safety review",
  "revision_reviewed": 1,
  "open_findings": 2,
  "finding_ids": [
    "V243-C4-001",
    "V243-C4-002"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 final safety bug-check recheck — revision 2

- **Reviewed revision:** `4a89d341e010145c3e4e0e99ccb03b047347e40a`.
- **Verdict:** `revision_requested`.
- **Final PRD review:** no; V243-C4-001 is resolved, but the unchanged record still does not satisfy V243-C4-002.
- **Bug-check:** completed over the revision-2 delta plus the cumulative final scope; one evidence finding remains open.

### Open finding

#### V243-C4-002 — Medium — Deterministic responder lifecycle evidence remains absent

- **Status:** open, unchanged.
- **Confidence:** confirmed evidence gap.
- **Evidence:** `native-coms-validation-243.md` is byte-for-byte the revision-1 caller-side receipt. It records same-worktree discovery, short timeout, pending, later completion, schema conformance, and correlation. It still does not identify a controlled responder delay, explicitly classify the response as exactly one normal Pi correlated reply with no reply-via-`coms_send`, or prove post-response same-pool availability. The revision-2 handoff explicitly records that no new sanitized receipt was produced.
- **Bounded action:** run the already-specified local validation with a deliberate bounded responder delay, exactly one normal Pi correlated response, no `coms_send` reply, and post-response same-pool discovery after resumed availability. Update only sanitized structural evidence and the current handoff.
- **Decision impact:** PRD acceptance criteria 4 and 5 remain incomplete; final approval cannot be inferred from the existing observed-but-not-deterministic timeout.

### Resolved finding

#### V243-C4-001 — Resolved — Natural zero/nonzero exits now drain detached descendants

- `verificationScopeLifecycle.ts` now attempts verified natural drainage first and invokes full scope termination when the scope remains active; failure still disables the session.
- The excluded validation harness adds finite zero/nonzero natural-exit cases that execute the shipped lifecycle, and production still exposes only immutable `typecheck`.
- Independent revision-2 execution passed the natural-exit detached-descendant test and left no `agentops-verify-*` scope. The complete focused suite passed 25 structural plus 11 live tests.
- The change is bounded and KISS-compliant: the lifecycle remains 274 lines, the changed `finish()` function remains below 20 lines with four parameters and shallow nesting, and the five-line fixture adds no comments or dead code.

### Atomic recheck

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, worktree, branch, and revision | Pass | Authenticated REST `gh api` confirmed open issue #243; expected worktree/branch; exact HEAD `4a89d341...` |
| Branch freshness and tree | Pass | Branch is two commits ahead and zero behind `origin/main`; worktree was clean before this verifier-owned report update |
| V243-C4-001 code path | Pass | Natural close now falls back from positive drainage to full scope termination and verification |
| V243-C4-001 zero/nonzero coverage | Pass | Shipped-lifecycle validation handles both detached-descendant parent exit statuses and asserts verified cleanup |
| Scope cleanup after tests | Pass | No `agentops-verify-*` unit remained after the independent suite |
| Production/test authority separation | Pass | Natural-exit IDs remain test-only; clean server build contains no tests or validation harness |
| V243-C4-002 deterministic timeout-first proof | Fail | No new receipt or responder-lifecycle evidence exists |
| Authority and activation boundaries | Pass | Native verification remains dormant/unwired; no bypass, push, PR, merge, deploy, GitHub mutation, activation, trade, or backtest occurred |
| KISS and hygiene | Pass | Changed product/test files remain within file/function/parameter/nesting/comment/dead-code limits; changed paths are colocated and build output is clean |

### Bug-check recheck summary

- **Fast pass:** the two-line lifecycle delta closes the previously reproduced path without changing command parsing, policy, audit, sandbox mounts, environment, timeout/output/OOM handling, or production wiring.
- **Silent-failure pass:** natural-close descendants are now terminated and positively drained before return. Manager/termination failure remains explicit and disables the session.
- **Edge-case pass:** zero and nonzero parent exit are both covered; timeout, output, OOM, manager error, revocation, and audit failures continue to pass. The only remaining gap is the unchanged deterministic coms-responder evidence.
- **Tool escalation:** none required; the lifecycle fix is directly verifiable through source and the focused live suite. Prior systemd research remains applicable.

### Validation Receipt — Checkpoint 4 Revision 2

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 4 — final safety bug-check recheck, revision 2.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** natural-exit whole-scope cleanup; finite production authority; focused containment regressions; deterministic timeout-first coms validation; responder reply discipline and resumed availability; branch freshness; KISS; forbidden-action boundaries.
- **Reviewed files/surfaces:** revision-2 commit and all nine changed paths; lifecycle and direct tests/support/fixture/package call edges; current handoff; unchanged native-coms receipt; prior final bug-check report; canonical issue; branch/status/build output and systemd scope state.
- **Commands/results:**
  - `gh api repos/hyperbotsx/agentops-harness/issues/243` — passed.
  - branch/status/revision checks — passed: `4a89d341...`, two ahead/zero behind, clean.
  - `npm --prefix term-control-center run test:sandbox` — passed: 25 structural plus 11 live tests.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed with only the previously recorded non-failing Vite warnings.
  - `git diff --check` — passed.
  - production build-exclusion check — passed.
  - post-suite systemd scope inventory — empty.
- **Skipped checks/reasons:** no new native Claude→Codex validation was available to run or classify; this is the reason V243-C4-002 remains open. The over-budget default test surface remains intentionally excluded from production; the PRD-focused suite passed. No activation or forbidden external action was attempted.
- **Edge cases:** natural zero/nonzero parent exit with detached descendant; failed manager cleanup; collected scopes; timeout/output/OOM; validation IDs entering production; controlled short-timeout ordering; duplicate responder reply; post-response availability.
- **Regression risks:** the lifecycle correction is low and focused. Final risk remains approving an observed timeout race as deterministic contract proof or accepting a responder that did not prove resumed availability.
- **Relevant canonical standards checklist summary:** the lifecycle now has complete bounded side-effect cleanup with deterministic IO tests and preserves module/KISS boundaries. Secret-free deterministic coms evidence remains mandatory; no exception is accepted.
- **Findings:** V243-C4-001 resolved; V243-C4-002 open.
- **Required follow-up:** produce the bounded sanitized deterministic coms receipt and refresh the handoff, then request checkpoint-4 revision 3. No additional product-code change is requested by this review.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier edited only this verifier-owned report; created no coder-owned change, commit, push, PR, merge, deployment, GitHub mutation, approval, activation, trade, or backtest; retained no raw prompt/response/transcript or secret.
- **Checkpoint compliance/deviation:** code bug-check is clean after V243-C4-001. Final completion remains blocked only by the explicit unchanged V243-C4-002 evidence requirement.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - final safety bug-check recheck",
  "revision_reviewed": 2,
  "open_findings": 1,
  "finding_ids": [
    "V243-C4-002"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 final safety review — revision 3

- **Reviewed revision:** `63b7a103f65cedb3440852dfe3085a6db7aed9a7` and the cumulative ten-commit branch diff from `origin/main`.
- **Verdict:** `revision_requested`.
- **Final PRD review:** no; V243-C4-001 and V243-C4-002 are resolved, but final bug-check found a false-positive schema-validation defect and stale durable handoff metadata.
- **Bug-check:** completed over the new coms/policy/launcher delta plus the cumulative final scope; two findings remain open.

### Open finding

#### V243-C4-003 — Medium — `schema_conformant` reports true for responses that violate the supplied JSON schema

- **Confidence:** confirmed.
- **Location:** `term-control-center/server/comsWire.ts:31-34`, consumed by `term-control-center/server/comsReply.ts:6-9`; incomplete coverage in `term-control-center/tests/comsAdapter.schema.test.ts:7-66` and the delayed responder test.
- **Trigger:** a schema-bound request supplies ordinary JSON Schema constraints beyond presence of `required` keys, such as property types or `additionalProperties:false`, and the peer returns all required keys with a wrong value type or an extra field.
- **Failure mechanism:** `conformsToSchema()` only verifies that the response is an object and every `required` name is present. It ignores `type`, `properties`, property types, `additionalProperties`, `const`, `enum`, and nested constraints. A bounded verifier check against `{type:'object', required:['ack'], properties:{ack:{type:'boolean'}}, additionalProperties:false}` returned `true` for both `{ack:'yes'}` and `{ack:true, extra:1}`. The delayed responder test uses `{ack:'boolean'}`, which is not a meaningful JSON Schema and therefore does not cover this defect.
- **Impact:** callers and receipts can silently classify a nonconformant response as conformant. The r4 payload was independently exact-matched and therefore still closes V243-C4-002, but the newly shipped annotation is unsafe evidence for subsequent schema-bound requests.
- **Bounded action:** either validate the supported response-schema contract accurately and fail closed for unsupported schema shapes, or remove/rename the `schema_conformant` claim so it cannot imply JSON Schema validation. Add wrong-type, forbidden-extra-field, enum/const, and relevant nested-constraint negatives using a valid schema. Keep response delivery separate from the annotation result.
- **Decision impact:** final bug-check cannot approve a new silent false-positive validation signal.

#### V243-C4-004 — Low — The durable handoff still records a stale branch-ahead count

- **Confidence:** confirmed.
- **Location:** `dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/coder-handoff.md`, Current risks and cleanup deviation.
- **Evidence:** the handoff says the branch is eight commits ahead, while the reviewed branch and request are ten commits ahead and zero behind. The synchronization section correctly avoids a self-invalidating exact count, but the later stale count contradicts it and the claimed final metadata cleanup.
- **Bounded action:** remove the exact ahead count from durable committed evidence and record only the stable fact that the branch is zero behind with local evidence commits unpushed; refresh the validation summary after the C4-003 correction.
- **Decision impact:** final durable evidence must be internally current and unambiguous, although this is not a product-code or authority defect.

### Resolved findings

#### V243-C4-001 — Resolved, no regression

The shipped lifecycle continues to terminate and verify scopes after natural zero/nonzero exits. The independent sandbox suite passed 25 structural plus 11 live tests and left no verification scope.

#### V243-C4-002 — Resolved by the approved two-layer evidence model

- The committed test uses two production `ComsAdapter` instances and real local sockets to deterministically prove short timeout → pending → controlled delayed release → exactly one correlated completion → duplicate rejection → responder listable.
- The r4 human-visible run separately proves exactly one same-worktree Codex verifier, one native outbound request, one normal Pi correlated response with no reply-via-`coms_send`, exact required four-field payload, and post-response `alive:true` discovery.
- Independent structural inspection of the still-live r4 panes and pool metadata corroborated the single normal Pi response and post-response liveness without retaining raw transcript content.
- The live run need not reproduce human/model timing because the approved deterministic test layer owns that requirement. Together the two layers satisfy PRD acceptance criteria 4 and 5.

### Atomic final checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and revision | Pass | Authenticated REST `gh api` confirmed open issue #243; expected branch/worktree; exact HEAD `63b7a103...` |
| Branch freshness and tree | Pass | Ten commits ahead and zero behind `origin/main`; worktree clean before this verifier-owned report update |
| C4-001 lifecycle and containment | Pass | Natural-exit correction and 36-test sandbox suite pass; no remaining scope |
| C4-002 deterministic timeout lifecycle | Pass | Real-socket production adapters with controlled response release, one completion, duplicate denial, and liveness |
| C4-002 human native→Pi path | Pass | r4 exact payload/correlation, normal Pi reply, no `coms_send` reply, and post-response verifier liveness |
| Strict tool discovery | Pass | Only the exact six-method ToolSearch query with exact keys/count maps to `peer_coms`; all tested variations deny |
| Context and history handling | Pass with scope qualifier | Native prompt supplies the trusted context path for Read; wrapper forwards only exact history-skip value `1`; neither broadens tool authority |
| Schema conformance annotation | Fail | V243-C4-003 reproduces wrong-type and extra-field false positives |
| Durable handoff metadata | Fail | V243-C4-004: handoff says eight commits ahead; reviewed state is ten ahead/zero behind |
| Always-gates and activation boundary | Pass | Bash/GitHub/WebFetch and unknown tools remain denied; native verification remains dormant/unwired; no permission bypass added |
| Steward, placement, generated output, and KISS | Pass with metadata exception | Changed paths are colocated; build excludes test support; files stay below 300 lines (`comsAdapter.ts` 297); functions/parameters/nesting/comments/dead-code checks pass; V243-C4-004 remains |
| Final bug-check | Fail with two findings | Fast, silent-failure, edge-case, and evidence passes leave V243-C4-003 and V243-C4-004 open |

### Bug-check summary

- **Scope:** all revision-3 coms adapter/wire/reply, autonomy gate, native wrapper/prompt, tests, and run evidence, plus regression checks over the approved sandbox and authority boundaries.
- **Fast pass:** no cross-pool fallback, production delayed-test helper, extra MCP method, raw Bash allowance, settings bypass, activation wiring, or KISS regression was found.
- **Silent-bug pass:** the schema annotation false positive was confirmed; response delivery itself remains correlated and does not fail or mutate authority.
- **Edge-case pass:** timeout/pending/late completion, duplicate reply, wrong endpoint, same-worktree isolation, post-response liveness, missing schema keys, schema-free responses, tool-discovery variants, history values, and C4-001 cleanup are covered. Wrong types, extra fields, enum/const, and nested schema constraints are missing; the committed branch-count metadata is stale.
- **Tool escalation:** no Semgrep/CodeQL/fuzzing was warranted; direct source inspection and a bounded runtime check confirmed the defect.

### Validation Receipt — Checkpoint 4 Revision 3

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 4 — final safety review, revision 3.
- **Decision:** revision_requested.
- **Final review:** no.
- **Acceptance criteria reviewed:** safe autonomy default deny and always-gates; option-B runtime mapping; deterministic timeout-first lifecycle; one normal Pi correlated response; exact response/liveness evidence; same-worktree/pool isolation; schema observability; branch freshness; Steward hygiene; final bug-check.
- **Reviewed files/surfaces:** canonical issue/context; cumulative handoff/report; r3/r4 receipts; all 17 paths changed after `4a89d341`; adapter/wire/reply call graph; ToolSearch policy; native wrapper/prompt; sandbox regression scope; current build output and live validation process/pool metadata.
- **Commands/results:**
  - `gh api repos/hyperbotsx/agentops-harness/issues/243` — passed.
  - branch/status/revision checks — passed: `63b7a103...`, ten ahead/zero behind, clean.
  - focused adapter/native suite — passed: 44/44.
  - `npm --prefix term-control-center run test:sandbox` — passed: 25 structural plus 11 live.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed with only the recorded non-failing Vite warnings.
  - `git diff --check` and production build-exclusion checks — passed.
  - post-suite systemd scope inventory — empty.
  - bounded schema negative — confirmed V243-C4-003: wrong type and forbidden extra field both returned `true`.
- **Skipped checks/reasons:** full default `npm test` remains outside the approved immutable production command because its earlier runtime exceeded the bound; the focused 44-test and sandbox 36-test suites cover the changed/final risk surfaces. No activation or forbidden external action was attempted.
- **Edge cases:** schema wrong types/extras/enum/const/nesting; controlled delayed response; duplicate response; post-response liveness; strict ToolSearch shape; missing context; history-skip value; natural/timeout/output/OOM/manager cleanup.
- **Regression risks:** false schema assurance on future correlated replies; future expansion of strict ToolSearch; prompt-schema drift between native and non-native peers; self-invalidating exact Git counts in committed evidence. ToolSearch is currently bounded by exact tests and policy.
- **Relevant canonical standards checklist summary:** isolation, fail-closed authority, deterministic transport tests, observability boundaries, placement, and KISS pass. Validation truthfulness remains incomplete because unsupported schema constraints silently pass; no exception is accepted.
- **Findings:** V243-C4-001 and V243-C4-002 resolved; V243-C4-003 and V243-C4-004 open.
- **Required follow-up:** correct or narrow the schema-conformance annotation, add valid negative tests, remove the stale exact branch count, rerun focused/typecheck/build/diff validation, refresh the handoff, and request checkpoint-4 revision 4. No new live native round trip is required unless the wire/prompt contract changes.
- **Next actor:** coder.
- **Forbidden-action confirmation:** verifier edited only this verifier-owned report; created no coder-owned change, commit, push, PR, merge, deployment, GitHub mutation, approval, activation, trade, or backtest; retained no raw private transcript, prompt, response, token, or secret.
- **Checkpoint compliance/deviation:** the approved two-layer C4-002 evidence is sufficient and the prior lifecycle defect remains closed. Final completion is withheld for V243-C4-003 and the bounded durable-evidence correction V243-C4-004.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - final safety review",
  "revision_reviewed": 3,
  "open_findings": 2,
  "finding_ids": [
    "V243-C4-003",
    "V243-C4-004"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 final safety review — revision 4

- **Reviewed revision:** `2514e453c1f6448726b33fecb6531b101df3df00` and the cumulative branch diff from current `origin/main`.
- **Verdict:** `approved`.
- **Final PRD review:** yes.
- **Bug-check:** completed with no open findings.
- **Scope boundary:** this approval accepts the implementation and evidence for PRD #243. It does not activate native autonomous verification or authorize push, PR creation, merge, deployment, GitHub mutation, approval, trading, or backtesting.

### Finding disposition

| Finding | Final status | Evidence |
| --- | --- | --- |
| V243-C4-001 | Resolved | Natural zero/nonzero exits terminate and positively drain detached descendants through the shipped lifecycle; independent sandbox suite passes |
| V243-C4-002 | Resolved | Approved two-layer proof combines deterministic real-socket timeout/pending/late-reply lifecycle with one human-visible native→normal-Pi exact response and post-response liveness |
| V243-C4-003 | Resolved | Unsafe broad `schema_conformant` annotation, helper, and tests are removed; correlated response delivery is restored unchanged and r4 relies on explicit exact payload equality |
| V243-C4-004 | Resolved | Durable handoff records the stable zero-behind/unpushed state and no self-invalidating ahead count |

No findings remain open.

### Atomic final checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and revision | Pass | Authenticated REST `gh api` confirms open issue #243; expected branch/worktree; exact HEAD `2514e453...` |
| Branch freshness and tree | Pass | Eleven commits ahead and zero behind `origin/main`; worktree clean before this verifier-owned report update |
| Global bypass and always-gate rejection | Pass | Native wrapper continues rejecting bypass/settings substitution; Bash/GitHub/WebFetch, secrets, destructive/external/money actions, and unknown tools remain denied |
| Project/session policy and kill switch | Pass | Owner-private strict policy remains worktree/session bound, default deny, re-read per action, revocable, audit-fail-closed, and protected from autonomous writes |
| Secret/path/environment boundary | Pass | Exact child environment, secret/config path denial, `.git`/protected-root denial, and strict MCP isolation remain covered |
| Sandbox containment and lifecycle | Pass | Finite immutable production `typecheck`, read-only worktree/Git/evidence, no network/credentials/sockets, resource/output/time limits, audit failure/revocation, OOM, manager failure, and all natural/forced cleanup cases pass |
| Native tool discovery and context | Pass | Only the exact six-method ToolSearch request maps to peer coms; the launch-supplied context path is readable without Bash/GitHub/WebFetch expansion |
| Deterministic timeout-first proof | Pass | Production adapters over real sockets prove timeout → pending → controlled release → one correlated response → duplicate rejection → responder listable |
| Human native→Codex/Pi proof | Pass | r4 records one same-worktree peer, one outbound request, one exact four-field normal Pi correlated response with no reply-via-`coms_send`, and post-response `alive:true` |
| Correlation behavior after C4-003 | Pass | Adapter `get`/`awaitReply` returns the original correlated response behavior with no unsupported conformance assertion |
| Durable evidence and Steward hygiene | Pass | Handoff/receipts are colocated and current; no backlog or `.ralph` drift; generated/test build output is excluded; final Steward classification is clean |
| Explicit KISS review | Pass | Changed product/test files remain below 300 lines (`comsAdapter.ts` 298, `launchPlan.ts` 296); functions remain below 20 lines with at most four parameters and shallow nesting; comments are constraint-only; no dead/commented-out code remains |
| Forbidden-action boundary | Pass | Native verification remains dormant/unwired and no forbidden action occurred during implementation or review |

### Final bug-check summary

- **Scope:** cumulative changed implementation/tests/run evidence plus the revision-4 removal delta and immediate adapter, policy, launcher, sandbox, and lifecycle call edges.
- **Fast pass:** C4-003 removal restores the prior response path exactly; no stale import, schema annotation, test artifact, cross-pool fallback, extra MCP method, raw Bash allowance, activation path, or generated output remains.
- **Silent-failure pass:** no false schema-success signal remains. Policy, audit, cleanup, timeout, and response failures stay caller-visible and fail closed where required.
- **Edge-case pass:** missing/malformed/revoked policy; secret/config paths; symlink/escape; invalid/long command IDs; audit failure; timeout/output/OOM; natural zero/nonzero descendant exit; manager failure; ToolSearch variants; immediate and delayed replies; duplicate/wrong-peer responses; post-response liveness; and stale metadata were reviewed and covered.
- **Tool escalation:** no further Semgrep/CodeQL/fuzzing was justified after the bounded defect was removed and the focused/runtime suites passed.

### Validation Receipt — Checkpoint 4 Revision 4

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 4 — final safety review, revision 4.
- **Decision:** approved.
- **Final review:** yes.
- **Acceptance criteria reviewed:** recorded CEO/security decision and global-bypass rejection; project-scoped default deny/kill switch/always-gates; explicit option-B contract; same-pool/worktree isolation; exactly one normal Pi correlated response; deterministic timeout-first behavior; secret-free bounded evidence; no authority regression; Steward hygiene; final bug-check.
- **Reviewed files/surfaces:** canonical issue/context; cumulative coder handoff and all receipts; complete verifier history; current revision-4 eight-path delta; native wrapper/settings/prompt/hook/policy/audit/path boundary; coms adapter/wire/MCP tests; sandbox/executor/lifecycle and build output; branch/status and current systemd scope state.
- **Commands/results:**
  - `gh api repos/hyperbotsx/agentops-harness/issues/243` — passed.
  - branch/status/revision checks — passed: `2514e453...`, eleven ahead/zero behind, clean.
  - focused adapter/native suite — passed: 39/39.
  - `npm --prefix term-control-center run test:sandbox` — passed: 25 structural plus 11 live.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed; only the previously recorded non-failing Vite static-script/chunk warnings appeared.
  - `git diff --check` and production build-exclusion checks — passed.
  - schema/helper/stale-count reference checks — no live product/test annotation or exact current handoff count remains; historical verifier evidence is retained as history.
  - post-suite `agentops-verify-*` systemd scope inventory — empty.
- **Skipped checks/reasons:** full default `npm test` remains outside the approved immutable production command because its earlier runtime exceeded the bound; the focused 39-test and sandbox 36-test suites cover the final changed/risk surfaces. No native activation, push, PR creation, merge, deployment, or other forbidden action was performed.
- **Edge cases:** all prior C4 findings and regression edges listed above; human model timing is intentionally covered by the separate deterministic real-socket test layer rather than claimed by the prompt-driven live turn.
- **Regression risks:** future ToolSearch expansion, response-schema drift, or verification-command expansion require new review. Current exact gates, finite production command, tests, and human activation boundary contain those risks.
- **Relevant canonical standards checklist summary:** implementation boundaries, fail-closed security, deterministic validation, secret-free observability, placement, evidence hygiene, and explicit KISS checks pass. No exception is open.
- **Findings:** none open; V243-C4-001 through V243-C4-004 are resolved.
- **Required follow-up:** report final approval to the operator. Any PR preparation/push requires the existing separate human confirmation and Git Manager workflow. Enabling native autonomous `typecheck` remains a distinct human/security action and is not performed by this approval.
- **Next actor:** human/operator.
- **Forbidden-action confirmation:** verifier edited only this verifier-owned report; created no coder-owned change, commit, push, PR, merge, deployment, GitHub mutation, activation, approval, trade, or backtest; retained no raw private transcript, prompt, response, token, or secret.
- **Checkpoint compliance/deviation:** final implementation and evidence satisfy PRD #243. The default full-suite omission is the previously reviewed bounded validation choice; focused and final risk suites pass. No authority or safety deviation remains open.

## Machine Status

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "4 - final safety review",
  "revision_reviewed": 4,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "completed_no_findings",
  "next_actor": "human",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 independent final safety review — revision 5

- **Reviewed revision:** `257eadf922c9d6ebc7a804d536fdd95ccc4b992c` and the complete 12-commit diff from `origin/main`.
- **Verdict:** `revision_requested`.
- **Final PRD review:** no. The prior revision-4 approval is preserved as history, but its durable evidence update is internally contradictory and the independent lifecycle probe found a new fail-closed availability defect.
- **Bug-check:** completed over the final diff and immediate call paths; three bounded findings are open.

### Current repository state

Before this report edit, the worktree was clean, `HEAD` was 12 commits ahead and zero commits behind `origin/main`, and `git diff --check origin/main...HEAD` passed. The latest commit changes only the co-located handoff and prior verifier report. It did not change product code or test sources.

### Finding disposition

| Finding | Status | Evidence |
| --- | --- | --- |
| V243-C4-001 | Remains resolved | The 25 structural plus 11 live sandbox suite passes natural zero/nonzero detached-descendant cleanup. |
| V243-C4-002 | Remains resolved | The real-socket adapter test proves timeout → pending → controlled response → one completion → liveness; r4 supplies the isolated native→harness-native exact-payload/liveness receipt. |
| V243-C4-003 | Reopened — Low | A current receipt and handoff prose still claim schema conformance although the removed annotation was the only local validation signal and no payload is retained there for independent proof. |
| V243-C4-004 | Reopened — Low | The committed handoff simultaneously records final approval and earlier current-looking statements that final review/bug-check were skipped or still required. Steward independently reported `S243-HYG-001`. |
| V243-C4-005 | New — Medium | A fast, successful scope exits fail closed and permanently disable that session because scope discovery starts only after a fixed 500 ms delay. |

### Open findings

#### V243-C4-003 — Low — Superseded receipt still makes an unsupported schema-conformance claim

- **Evidence:** `native-coms-validation-243.md:21,33` says the response conformed to the requested JSON schema and calls it schema-conforming. `coder-handoff.md:17,25` repeats that claim as active validation evidence. The receipt deliberately retains no response payload, while current `comsWire.ts`/`comsAdapter.ts` deliver correlated responses without JSON-Schema validation after the unsafe `schema_conformant` signal was removed. The r4 artifact correctly relies instead on explicit four-field payload equality.
- **Impact:** the final evidence still overstates a validation capability that C4-003 deliberately removed. This is an evidence-truthfulness defect, not a response-delivery regression.
- **Bounded action:** retain the receipt only as clearly labeled historical/superseded structural evidence, remove its schema-conformance assertion, and make the handoff name r4 exact-payload equality as the sole final payload evidence. Do not restore an adapter annotation or add a broad schema validator.

#### V243-C4-004 — Low — Final handoff has conflicting current status and obsolete gates

- **Evidence:** `coder-handoff.md:5` and the new Final verifier outcome state approval, but lines 17–19 say final review and bug-check were skipped/pending; lines 31–32 say final acceptance is still required and the recheck awaits completion. These entries are not labeled historical. The final evidence commit is otherwise clean, correctly zero-behind, co-located, and has an inventory matching the 43 `origin/main...HEAD` changed paths and 12 retained run artifacts. The Steward recheck found no placement, generated-output, secret, raw-transcript, or private-artifact defect, only this contradiction (`S243-HYG-001`).
- **Impact:** the durable handoff cannot be used as one unambiguous final gate record or PR-preparation input.
- **Bounded action:** move the pre-final assertions under an explicitly dated superseded revision section, or update them to the final state; retain the historical facts without presenting them as current. Then refresh the handoff's validation counts to the final 25 structural plus 11 live result and request a metadata-only recheck.

#### V243-C4-005 — Medium — Fast successful scopes are denied and disable the session

- **Location:** `term-control-center/server/verificationScopeLifecycle.ts:69,119–142,150–156,218–237`.
- **Trigger:** a scope's main process exits successfully before the delayed `verifyRunningScope()` callback first captures its control group. An independent isolated lifecycle probe using the harmless `/usr/bin/true` plan returned `deny_sandbox_start` with `cleanupVerified:false`; after 800 ms `isVerificationSessionDisabled(session)` was true and a second request in the same session also denied. No scope remained afterward.
- **Failure mechanism:** control-group discovery is deferred by 500 ms. A fast natural exit can reach `finish()` before `running.controlGroup` is known; the later verifier treats the collected unit as an unverified manager failure and disables the session. Existing natural-exit coverage retains a detached descendant, so it does not cover a clean fast exit with an already-collected scope.
- **Impact:** the immutable permitted `typecheck` path can become unavailable and permanently deny the session when it completes quickly. This is fail-closed rather than an authority escape, but it contradicts successful verification behavior and leaves an untested lifecycle boundary.
- **Bounded action:** make successful fast-scope cleanup positively verifiable without relying on the delayed callback, preserve fail-closed behavior when proof is genuinely unavailable, and add a live test for a clean fast exit that asserts `ok`, verified cleanup, no remaining unit, and a second same-session run is not disabled. Do not wire or activate the native autonomous path.

### Atomic recheck

| Check | Result |
| --- | --- |
| Scope, placement, secrets, raw transcripts, and private artifacts | Pass apart from V243-C4-003/004 evidence truthfulness; all retained artifacts are in the approved run directory |
| Branch/worktree state before this report edit | Pass — clean, 12 ahead, zero behind `origin/main` |
| C4-002 isolation, one request/reply, harness-native response, exact r4 payload, liveness, deterministic delayed lifecycle | Pass |
| C4-003 response delivery after removal | Pass; no live schema helper/test/annotation remains; unsupported retained evidence claim fails |
| C4-004 inventory, backlog state, r4 nested path | Placement/inventory/r4 path pass; durable status consistency fails |
| Always-gates, fail-closed controls, dormant activation, legacy delegated-Claude scope, and human gates | Pass; no activation or legacy-path expansion found |
| KISS | Pass — changed product files remain below 300 lines; functions, nesting, parameters, comments, and dead-code checks remain within the recorded limits |

### Validation and bug-check record

- Focused adapter/native/autonomy suite: 41/41 passed.
- `npm --prefix term-control-center run test:sandbox`: 25 structural plus 11 live tests passed; no `agentops-verify-*` unit remained.
- `npm --prefix term-control-center run typecheck`, `npm --prefix term-control-center run build`, server build-exclusion check, and cumulative `git diff --check`: passed. Build emitted only the known non-failing Vite static-script and chunk-size warnings.
- Fast pass found no cross-pool fallback, extra MCP method, host-Bash allowance, activation wiring, secret leak, stale schema helper, or build inclusion of test support.
- Silent-failure pass confirmed V243-C4-005; evidence-truthfulness pass confirmed V243-C4-003/004. The relevant edge cases are otherwise covered by the focused and live suites.
- No Semgrep, CodeQL, or fuzzing escalation was warranted: the findings are direct lifecycle/evidence control-flow defects with bounded reproductions.
- The default `npm test` remains intentionally excluded from the immutable production command; it was not rerun.

### Required follow-up

Coder: apply only the three bounded remediations above, preserve native autonomy as dormant/unwired, refresh the sanitized handoff/evidence, run the focused suite, sandbox suite, typecheck, build, and diff checks, then request revision 6. Git/PR/deploy/GitHub mutation, activation, permission bypass, and legacy delegated-Claude changes remain out of scope.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - independent final safety review",
  "revision_reviewed": 5,
  "open_findings": 3,
  "finding_ids": [
    "V243-C4-003",
    "V243-C4-004",
    "V243-C4-005"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 independent final safety review — revision 6

- **Reviewed revision:** `4f9f0e75f8ed44c77edf4d92b1be943daaebc601` and the complete 20-commit diff from current `origin/main`.
- **Verdict:** `revision_requested`.
- **Final PRD review:** no. The fast-success regression is fixed and the prior schema evidence is corrected, but one cleanup-proof defect, one retained out-of-scope artifact, and explicit KISS violations remain.
- **Bug-check:** completed over the revision-6 delta, cumulative final diff, and immediate policy/sandbox/lifecycle call paths; three bounded findings are open.

### Current repository state

Before this verifier-owned report update, the worktree was clean. Local and GitHub `main` both resolved to `cf008400af963b244a83e53c8abb4dddc3cfebe2`; the branch was 20 commits ahead and zero behind. The cumulative diff contains 44 paths and no terminal/tmux implementation or test path. `dev-plans/prd-backlog.md`, `.ralph/`, and generated build output are clean/untracked as expected.

### Finding disposition

| Finding | Revision-6 status | Evidence |
| --- | --- | --- |
| V243-C4-003 | Resolved | The superseded receipt is explicitly historical, no longer asserts adapter-level schema validation, and the current handoff relies on r4 exact four-field payload equality. |
| V243-C4-004 | Open | The current touched-file inventory omits a newly committed, unrelated, stale session-handover artifact outside the approved run directory; Steward records `S243-HYG-002`. |
| V243-C4-005 | Resolved | The verify timer is tracked/cleared, collected successful scopes are accepted, settlement retries before forced cleanup, and the new fast-success live test proves two same-session successes. |
| V243-C4-006 | New — Low | Explicit KISS analysis found branch-introduced/worsened function-size violations. |
| V243-C4-007 | New — Medium | A status-zero but incomplete or invalid `systemctl show` result can be accepted as positive scope-cleanup proof. |

### Open findings

#### V243-C4-004 — Low — Revision-6 retains an unrelated and stale session handover

- **Evidence:** `dev-plans/agentops/session-handover-2026-07-19.md:5,22–47,58–63` records the reverted tmux copy-mode scope, deploy instructions, and stale claims that the terminal fix exists on this branch and revision-5 work is still active. The terminal code was reverted by `ebc52fe`; the cumulative PRD diff contains no terminal/tmux path. The artifact is outside the approved issue-243 run directory and is absent from `coder-handoff.md:93–142`, whose inventory substitutes a net-zero `comsAdapter.ts` entry for this actual changed path. Steward independently classified this as `S243-HYG-002` and found no other revision-6 placement/generated-output defect.
- **Impact:** the final branch and durable inventory do not represent one bounded PRD scope, and the retained deployment guidance describes code no longer present on this branch.
- **Bounded action:** remove this file from the PRD #243 branch or move it to the separate terminal-fix documentation/branch, then make the current handoff inventory exactly match the retained cumulative diff.
- **Decision impact:** final Steward hygiene and durable-evidence checks do not pass.

#### V243-C4-006 — Low — Changed functions remain outside KISS bounds

- **Evidence:** an AST pass over all 22 changed TypeScript source/test files found `writeControlFile()` at `term-control-center/server/autonomyControlPlane.ts:20–39` spanning 20 lines. The changed native-browser launch test callback at `term-control-center/tests/nativeClaudeLaunchPlan.test.ts:59–83` spans 25 lines and grew from 24 lines on `origin/main`. File sizes, parameter counts, nesting, comment rules, and dead/commented-out-code checks otherwise pass; the largest changed product files are 296 and 292 lines.
- **Impact:** the cumulative final implementation does not pass the mandatory explicit KISS gate even though no runtime bug is established by this finding.
- **Bounded action:** extract the atomic write/post-write verification steps and split the browser prompt assertions into a named helper or smaller focused tests; keep behavior unchanged and rerun the structural check.
- **Decision impact:** final KISS approval is withheld.

#### V243-C4-007 — Medium — Incomplete manager state is treated as verified cleanup

- **Confidence:** confirmed.
- **Location:** `term-control-center/server/verificationScopeLifecycle.ts:148–156,180–186,210–214,230–250`.
- **Trigger:** `systemctl --user show` exits with status zero but omits `LoadState` and `ControlGroup`, or returns an unexpected load state together with `ActiveState=inactive|failed` and no known control group.
- **Failure mechanism:** `inspectScope()` marks every status-zero response `ok`; `scopeDrained()` checks only `state.ok` and inactive/failed, then returns true when both reported and previously captured control groups are absent. `finalizeKnownScope()`/`settleScope()` therefore report `cleanupVerified:true`, avoid disabling the session, and may return success without proving the expected scope was loaded or collected. A bounded verifier mock with status-zero stdout containing only `ActiveState=inactive` reproduced an `ok:true`, `cleanupVerified:true` result.
- **Impact:** a malformed, incomplete, or mismatched manager response is silently upgraded to positive cleanup evidence. The executor is dormant, so no current authority escape occurred, but this violates the required fail-closed activation boundary.
- **Test shape:** missing. Add a status-zero manager-response matrix covering absent `LoadState`, absent `ControlGroup`, unexpected load states, wrong active states, and the two accepted exact cases.
- **Bounded action:** distinguish absent properties from explicit empty values. Accept collected proof through exact `LoadState=not-found`; otherwise require the expected successfully inspected loaded scope, exact inactive/failed state, an explicit `ControlGroup` property, and a drained reported/previously captured cgroup as applicable. Reject every other state and preserve session disablement on unverifiable cleanup.
- **Decision impact:** final safety/bug-check approval is withheld.

### Atomic final checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and revision | Pass | Authenticated GitHub REST issue #243; expected worktree/branch; exact HEAD recorded above |
| Branch freshness and dirty tree | Pass before this report update | GitHub `main` equals local `origin/main`; 20 ahead/zero behind; clean tree and cumulative `git diff --check` |
| C4-003 evidence correction | Pass | Historical label and exact-payload wording are present; no live schema helper/annotation remains |
| C4-005 fast-success behavior | Pass | Two same-session `/usr/bin/true` lifecycle runs pass in the committed live test; timer remains cleared after 600 ms |
| Cleanup-proof fail-closed behavior | Fail | V243-C4-007 reproduces false positive cleanup from incomplete status-zero manager output |
| Default native pane authority | Pass | New default policy excludes `verification_command`; the one existing sanitized host policy is version 2 with only local read/edit/coms; all Bash remains hard denied and the executor remains unwired |
| Coms contract and isolation | Pass | Exact six-tool discovery, same-pool/worktree response correlation, deterministic timeout/pending/late response, one reply, and post-response liveness remain covered |
| Scope and Steward hygiene | Fail | V243-C4-004 / `S243-HYG-002`; no other revision-6 hygiene issue found |
| Explicit KISS review | Fail | V243-C4-006; other file/function structure, nesting, parameters, comments, and dead code pass |
| Forbidden actions | Pass | No native activation, permission bypass, push, PR, merge, deployment, GitHub mutation, trading, or backtest occurred |

### Research relied upon

A bounded Researcher recheck on 2026-07-19 validated the systemd v255 cleanup contract. `LoadState=not-found` from the same user manager is narrow collection proof because garbage collection refuses to unload a recursively populated cgroup. A no-control-group inactive/failed state is acceptable only from a successful exact response for the expected loaded scope with the required properties present; child exit or inactive state alone is not proof. Missing/malformed properties, wrong manager/identity, and name reuse must fail closed. The recheck also noted the later-identified cgroup-empty notification race, so state alone cannot replace cgroup/GC proof.

Sources:

- <https://raw.githubusercontent.com/systemd/systemd/v255/man/systemd.scope.xml>
- <https://github.com/systemd/systemd/blob/v255/src/core/unit.c>
- <https://github.com/systemd/systemd/blob/v255/src/core/dbus-unit.c>
- <https://github.com/systemd/systemd/releases/tag/v255>
- <https://github.com/systemd/systemd/pull/36797>

The reviewed host runs systemd `255.4-1ubuntu8.16` on kernel `6.8.0-90-generic`.

### Validation and bug-check record

- Focused adapter/native/autonomy coverage passed: 48 unique focused tests across the 42-test combined command plus the six sandbox structural cases.
- `npm --prefix term-control-center run test:sandbox` passed: 25 structural plus 12 live tests.
- `npm --prefix term-control-center run typecheck` passed.
- `npm --prefix term-control-center run build` passed; only the known non-failing Vite static-script and chunk-size warnings appeared.
- `git diff --check origin/main...HEAD` passed; no `agentops-verify-*` scope remained.
- Twenty additional harmless fast-output `/usr/bin/printf` lifecycle probes all returned success with verified cleanup and left no scope, ruling out the speculative fast-output variant as a finding.
- A mocked status-zero incomplete manager response reproduced V243-C4-007 without starting a real scope.
- Fast pass found no terminal/tmux code residue, cross-pool fallback, extra MCP authority, direct Bash allowance, native activation wiring, secret leak, schema helper, or generated build drift.
- Silent-failure pass found V243-C4-007's false cleanup success and V243-C4-004's stale final evidence. Edge-case review marks fast success, second same-session reuse, timeouts, output, OOM, natural descendant exit, revocation, audit failure, and manager status failure covered; successful-but-incomplete manager output is missing coverage.
- No Semgrep, CodeQL, or fuzzing escalation was justified after the bounded lifecycle reproduction and focused tests.

### Required follow-up

Coder: apply only V243-C4-004, V243-C4-006, and V243-C4-007; keep native verification dormant/unwired; rerun the focused, sandbox, typecheck, build, diff, scope-residue, and structural checks; obtain the bounded Steward artifact recheck; then request revision 7. Do not push, open a PR, merge, deploy, mutate GitHub, activate native verification, or weaken permissions.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - independent final safety review",
  "revision_reviewed": 6,
  "open_findings": 3,
  "finding_ids": [
    "V243-C4-004",
    "V243-C4-006",
    "V243-C4-007"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 independent final safety review — revision 7

- **Reviewed revision:** `d40074348109b37b3b8960252c251cf9b726531d` and the complete 21-commit diff from current `origin/main`.
- **Verdict:** `approved`.
- **Final PRD review:** yes. All C4 findings are resolved.
- **Bug-check:** completed over the revision-7 delta, cumulative final diff, and immediate policy, launcher, coms, sandbox, executor, and scope-lifecycle call paths with no open finding.
- **Scope boundary:** this approval does not activate native autonomous verification or authorize push, PR creation, merge, deployment, GitHub mutation, approval, trading, or backtesting.

### Finding disposition

| Finding | Final status | Evidence |
| --- | --- | --- |
| V243-C4-001 | Resolved | Natural zero/nonzero exits terminate and positively drain detached descendants through the shipped lifecycle. |
| V243-C4-002 | Resolved | The deterministic real-socket test proves timeout/pending/late-reply behavior; r4 proves one exact harness-native correlated response and post-response liveness. |
| V243-C4-003 | Resolved | Historical structural evidence no longer claims adapter-level schema validation; r4 exact payload equality is the sole final payload evidence. |
| V243-C4-004 | Resolved | The stale terminal handover is absent, the cumulative diff has no terminal/tmux artifact, and the 43-path handoff inventory exactly matches the retained diff. Steward returned clean. |
| V243-C4-005 | Resolved | Fast successful scopes clear the pending verifier timer, retain positive cleanup proof, and remain reusable in the same session. |
| V243-C4-006 | Resolved | Control-file and browser-prompt functions are split without behavior change; all branch-introduced or worsened functions/callbacks now pass the structural KISS check. |
| V243-C4-007 | Resolved | Cleanup accepts only exact collected proof or an exact loaded inactive/failed scope with an explicit, drained reported/known cgroup; incomplete status-zero manager state denies and disables the session. |

No findings remain open.

### Atomic final checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue, branch, worktree, and revision | Pass | Authenticated GitHub REST issue #243; expected branch/worktree; exact revision above |
| Branch freshness and tree | Pass before this report update | GitHub `main` equals local `origin/main` at `cf008400...`; 21 ahead/zero behind; clean tree and cumulative diff check |
| Scope and Steward hygiene | Pass | 43 retained paths exactly match the handoff; no terminal/tmux artifact, backlog drift, `.ralph`, generated tracked output, private artifact, or raw transcript; Steward independently returned `CLEAN` |
| Default native authority and activation | Pass | Existing sanitized policy is version 2 with only local read/edit/coms; all Bash stays denied; executor imports remain dormant outside tests and no native path wires it |
| Policy, kill switch, audit, paths, and environment | Pass | Strict owner/session/worktree policy, revocation, audit-fail-closed behavior, protected enforcement, exact environment names, and secret/config path denials remain covered |
| Sandbox containment and lifecycle | Pass | Finite production `typecheck`, Bubblewrap isolation, read-only roots, no network/credentials/sockets, bounded resources/output/time, OOM/timeout/natural cleanup, audit failures, fast success, manager failure, and incomplete manager state pass |
| Manager cleanup proof | Pass | Four independent malformed-state cases deny; exact collected and loaded-drained cases pass; twenty real fast scopes complete with verified cleanup and no residue |
| Coms contract and isolation | Pass | Exact six-tool discovery, same-worktree/pool identity, one correlated normal-Pi reply, no reply-via-`coms_send`, deterministic late response, and post-response liveness remain proved |
| Explicit KISS review | Pass | All changed files remain below 300 lines (`verificationScopeLifecycle.ts` 298; `launchPlan.ts` 296); branch-introduced/worsened functions remain below the function bound, parameters/nesting are bounded, comments are constraint-only, and no dead/commented-out code was found |
| Forbidden actions | Pass | No activation, bypass, push, PR, merge, deploy, GitHub mutation, trade, or backtest occurred |

### Final bug-check summary

- **Fast pass:** the revision changes only the bounded lifecycle proof, KISS refactors, handoff/report evidence, and stale-artifact removal. No terminal/tmux code, extra MCP authority, direct Bash allowance, policy expansion, native wiring, secret exposure, schema helper, or generated build drift exists.
- **Silent-failure pass:** incomplete or unexpected status-zero manager responses now remain caller-visible failures and disable the session. Cleanup, audit, policy, timeout, and response failures do not degrade into success.
- **Edge-case pass:** missing `LoadState`; missing `ControlGroup`; unexpected load state; wrong active state; exact collected state; exact loaded/drained state; fast clean success; same-session reuse; output, timeout, OOM, natural descendant exit, audit failure, revocation, manager error, delayed response, duplicate response, and peer liveness were covered by committed tests or independent bounded probes.
- **Potential false positives removed:** a reported control group is returned by the exact queried unique unit through the trusted same-user manager; absence/drainage of that manager-reported path is valid scope proof and is not caller-controlled. The stricter code may deny ambiguous states but does not expand authority.
- **Tool escalation:** no Semgrep, CodeQL, fuzzing, or further Researcher consult was justified after the direct reproduction matrix, prior source-cited systemd v255 research, and passing live suite.

### Validation Receipt — Checkpoint 4 Revision 7

- **PRD/title:** #243 — Native Session Safe Autonomy and Coms Contract Follow-up.
- **Project ID:** `agentops-harness`.
- **Checkpoint:** 4 — independent final safety review, revision 7.
- **Decision:** approved.
- **Final review:** yes.
- **Reviewed files/surfaces:** canonical issue; current handoff and all retained receipts; revision-7 seven-path delta; cumulative 43-path diff; native wrapper/settings/prompt/hook/policy/audit/path boundary; coms adapter/wire tests; sandbox/executor/runtime/lifecycle; build output; branch and systemd state.
- **Commands/results:**
  - canonical issue and GitHub/local main comparison — passed; remote/local `cf008400...`.
  - focused autonomy/native suite — 32/32 passed.
  - `npm --prefix term-control-center run test:sandbox` — 25 structural plus 13 live passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `npm --prefix term-control-center run build` — passed; only known non-failing Vite warnings.
  - cumulative `git diff --check` — passed.
  - handoff/diff inventory comparison — 43/43 exact.
  - JSON artifact parsing and production build-exclusion checks — passed.
  - AST structure check — no branch-introduced/worsened KISS violation; the sole strict-span flag is an unchanged baseline test callback.
  - independent manager-state matrix — four reject and two accept cases matched the intended contract.
  - twenty real fast-success scopes — 20/20 passed; final `agentops-verify-*` inventory empty.
  - Steward final hygiene recheck — `CLEAN`.
- **Skipped checks/reasons:** the known over-bound default full test suite remains outside the immutable production command and was not rerun; focused risk suites and the full application build cover this final delta. No activation or forbidden action was performed.
- **Regression risks:** future verification-command expansion, native wiring, systemd-version change, ToolSearch/MCP expansion, response-schema change, or legacy delegation change requires new review. Current finite commands, exact policy, tests, and human activation gate contain those risks.
- **Relevant canonical standards checklist summary:** boundaries, fail-closed behavior, deterministic validation, secret-free evidence, artifact placement, and explicit KISS checks pass. No exception is open.
- **Findings:** none open; V243-C4-001 through V243-C4-007 are resolved.
- **Required follow-up:** report final approval to the human/operator. Any PR preparation/push follows the separate human gate and Git Manager workflow. Enabling native autonomous `typecheck` remains a distinct human/security action and is not performed by this approval.
- **Next actor:** human/operator.
- **Forbidden-action confirmation:** verifier edited only this report; created no coder-owned change, commit, push, PR, merge, deployment, GitHub mutation, activation, approval, trade, or backtest; retained no raw private transcript, prompt, response, token, or secret.
- **Checkpoint compliance/deviation:** final implementation and evidence satisfy PRD #243. No authority, safety, KISS, or hygiene deviation remains open.

## Machine Status

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "4 - independent final safety review",
  "revision_reviewed": 7,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "completed_no_findings",
  "next_actor": "human",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 post-PR Kody remediation — revision 8

- **Reviewed revision:** PR head/local HEAD `f4c68e365199ff0477283f7a1b69cd0978b734fb` plus the seven-path uncommitted remediation working tree.
- **PR:** #252 is open, non-draft, and targets `main`; the remediation has not been pushed.
- **Verdict:** `revision_requested`.
- **Bug-check:** completed over the remediation delta and immediate policy/audit/executor call paths; one bounded regression remains.
- **Scope boundary:** review only. No PR comment/review, push, merge, deployment, activation, permission bypass, or other GitHub mutation was performed.

### Kody finding disposition

| Finding | Status | Evidence |
| --- | --- | --- |
| `d2c6d5a895e49ec6` | Resolved | Rotation and append share one owner-only exclusive per-audit lock. The committed held-lock negative passes, and an independent 20-process threshold race produced one rotation marker plus 20 intact records with no failure or leftover lock. |
| `9bb14d1106c62f3b` | Resolved | `verificationExecutor.ts` passes the configured `controlRoot`; audit append rejects paths outside it before creation. A direct verifier `runVerification()` probe returned `deny_audit_write_failed` and created no out-of-root audit file. |
| `66b3ba19e981fec2` | Non-actionable | Exact `LoadState=not-found` from the same successfully queried systemd v255 user manager is collection proof. v255 garbage collection retains units whose cgroup is recursively non-empty; the proposed remembered-cgroup check is not required and the strict C4-007 state/error guards remain unchanged. |

### Open finding

#### V243-C4-008 — Medium — Policy reads no longer validate the control-root parent

- **Confidence:** confirmed.
- **Location:** `term-control-center/server/autonomyControlPlane.ts:5–11`; `term-control-center/server/autonomyPolicy.ts:41–47`.
- **Trigger:** a valid policy is created under a trusted control root, then the immediate parent of `controlRoot` becomes group/world writable or otherwise untrusted before the next policy read.
- **Failure mechanism:** the remediation correctly adds lexical containment, but changes the trust traversal anchor from `path.dirname(controlRoot)` to `controlRoot`. `chain()` therefore stops at the control root and omits the parent that the prior approved ancestry check covered. An independent fixture created a policy, changed the control-root parent from `0700` to `0777`, and observed `readPolicy()` return `ok:true` with the allowed policy.
- **Impact:** the standalone policy/kill-switch reader no longer fails closed on a control-plane ancestry change. Current hook/executor actions still deny at the later audit append because `ensureControlDir()` rechecks the parent, so this does not create an immediate authority escape; it is nevertheless a regression in the approved policy trust boundary and an unsafe contract for any read-before-audit caller.
- **Bounded action:** keep the new requirement that every leaf be contained within `controlRoot`, while restoring trust traversal through the immediate parent of `controlRoot`. Add a regression that writes a valid policy, loosens or symlinks that parent, and expects `readPolicy()` to return `deny_policy_untrusted`. Preserve the new out-of-root audit rejection and lock behavior.
- **Decision impact:** the post-PR correction is not approved for commit/push until this bounded trust regression closes.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue/PR/branch/base | Pass | REST issue #243 and PR #252; PR head/local/remote branch `f4c68e3...`; base/local/remote `main` `cf008400...` |
| Expected working tree | Pass | Seven coder-owned remediation paths were dirty before this report update; fixes remain unpushed |
| Audit rotation serialization | Pass | Exclusive `wx` lock covers rotate plus append; held-lock fail-closed test and 20-process race pass |
| Audit root containment | Pass | Explicit control root propagated by both hook and executor; out-of-root direct and executor probes deny without creating evidence |
| Policy ancestry | Fail | V243-C4-008 reproduces `readPolicy().ok === true` after the control-root parent becomes `0777` |
| LoadState Kody report | Non-actionable | Prior source-cited systemd v255 GC analysis remains applicable; no lifecycle code changed |
| Default authority/activation | Pass | Native executor remains dormant/unwired; policy default excludes verification command; Bash and always-gated actions remain denied |
| Explicit KISS review | Pass for this delta | Remediation functions/files, parameters, nesting, comments, and dead-code checks pass; the sole strict-span AST flag is unchanged baseline test code |
| Forbidden actions | Pass | No push, PR mutation, merge, deploy, activation, bypass, trading, or backtest |

### Focused bug-check summary

- **Fast pass:** mandatory `controlRoot` propagation is complete across the autonomy audit callers; lock coverage encloses size check, rotation, marker creation, and append. No new authority, secret field, raw audit payload, or activation path was added.
- **Silent-failure pass:** Kody's two audit failures now fail closed. V243-C4-008 is the remaining silent trust downgrade: the parser returns a success-shaped policy even after its approved parent ancestry becomes untrusted, although later audit currently prevents action execution.
- **Edge-case pass:** held lock, threshold rotation, 20 simultaneous writers, symlink/loose audit file, out-of-root audit file, verification audit redirection, absent lock residue, malformed policy, revoked policy, and LoadState collection were reviewed. The newly missing parent-trust read case is now reproduced and requires a committed regression.
- **Residual fail-safe behavior:** a process killed while holding the audit lock can leave a stale lock and deny future actions. This is an availability-only fail-closed outcome inside the owner-protected control root and is not actionable for this bounded correction.
- **Tool escalation:** no broad static scan was warranted after direct concurrency and trust-boundary reproductions. The recorded v255 Researcher evidence is sufficient for `66b3ba19e981fec2`; no duplicate consult was made.

### Validation receipt

- Focused audit/control/lifecycle coverage passed: 39/39 (20 hook + 6 control-plane + 13 live).
- `npm --prefix term-control-center run test:sandbox` passed: 26 structural plus 13 live.
- `npm --prefix term-control-center run typecheck` passed.
- `npm --prefix term-control-center run build` passed; only known non-failing Vite warnings appeared.
- `git diff --check` passed and no `agentops-verify-*` scope remained.
- Independent 20-process audit race: 20/20 writers succeeded; current audit contained 21 records including the marker; rotated file existed; lock was absent afterward.
- Independent verification audit redirect: `deny_audit_write_failed`; no out-of-root audit file created.
- Independent policy-parent fixture: reproduced V243-C4-008 (`readPolicy()` returned `ok:true` after parent mode changed to `0777`); end-to-end hook still denied later with `deny_audit_write_failed`.
- KISS AST: 22 cumulative TypeScript files / 427 functions checked; no remediation-introduced violation.
- GitHub GraphQL PR query was rate-limited; authenticated REST independently confirmed PR #252 state/head/base and supplied all required review comments.

### Required follow-up

Coder: apply only V243-C4-008, add the bounded policy-parent regression, rerun the focused 39-test coverage, sandbox suite, typecheck, build, diff, and scope checks, then request revision 9. Keep the audit lock, explicit root propagation, lifecycle code, native wiring, and authority boundaries otherwise unchanged. Do not push or mutate PR #252 before verifier approval and the configured Git Manager/human gate.

## Machine Status

```json
{
  "decision": "revision_requested",
  "checkpoint_reviewed": "4 - post-PR Kody remediation",
  "revision_reviewed": 8,
  "open_findings": 1,
  "finding_ids": [
    "V243-C4-008"
  ],
  "bug_check_status": "completed_findings_open",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```

## Checkpoint 4 post-PR Kody remediation — revision 9

- **Reviewed revision:** PR head/local HEAD `f4c68e365199ff0477283f7a1b69cd0978b734fb` plus the current eight-path uncommitted remediation working tree.
- **PR:** #252 remains open and non-draft against `main`; the correction remains uncommitted and unpushed.
- **Verdict:** `approved`.
- **Bug-check:** completed over the Kody remediation, V243-C4-008 correction, and immediate policy/audit/executor call paths with no open finding.
- **Scope boundary:** this approval accepts the local correction only. It does not itself authorize a push, PR mutation, merge, deployment, activation, permission bypass, trading, or backtest.

### Finding disposition

| Finding | Final status | Evidence |
| --- | --- | --- |
| Kody `d2c6d5a895e49ec6` | Resolved | One owner-only exclusive per-audit lock serializes size check, rotation, marker creation, and append across processes; held-lock and real concurrent-writer checks pass. |
| Kody `9bb14d1106c62f3b` | Resolved | Hook/executor audit writes pass the configured control root, and contained trust validation rejects out-of-root evidence before creation. |
| Kody `66b3ba19e981fec2` | Non-actionable | Exact `LoadState=not-found` from the successfully queried same systemd v255 user manager remains valid GC proof; no lifecycle code changed and C4-007 guards remain intact. |
| V243-C4-008 | Resolved | `assertTrustedTree()` first requires containment within `controlRoot`, then validates the complete chain through its immediate parent. The new policy regression returns `deny_policy_untrusted` after that parent becomes `0777`. |

No findings remain open.

### Atomic checks

| Check | Result | Evidence |
| --- | --- | --- |
| Canonical issue/PR/branch/base | Pass | Authenticated REST issue #243 and PR #252; local/remote PR head `f4c68e3...`; local/remote base `cf008400...` |
| Expected working tree | Pass | Eight scoped remediation/report paths are dirty and unpushed; cumulative diff check passes |
| Control-root containment | Pass | Outside leaves reject before filesystem mutation |
| Immediate-parent trust | Pass | Policy read checks leaf → control root → immediate parent; independent `0777` fixture returns `deny_policy_untrusted` |
| Audit lock and rotation | Pass | Held lock denies unchanged audit; current ten-process and prior twenty-process races serialize without loss or residue |
| Verification audit root | Pass | Direct executor redirect returns `deny_audit_write_failed` and creates no outside file |
| LoadState Kody report | Non-actionable | Recorded source-cited systemd v255 GC evidence still applies; lifecycle delta is empty |
| Default authority/activation | Pass | Native execution remains dormant/unwired; verification is absent from default policy; Bash and always-gated actions remain denied |
| Scope/Steward hygiene | Pass | No placement, backlog, `.ralph`, generated-output, terminal/tmux, secret, or raw-transcript drift; Steward result is clean |
| Explicit KISS review | Pass for remediation | Changed functions/files, parameter counts, nesting, comments, and dead code pass; the sole strict-span flag is unchanged baseline test code |
| Forbidden actions | Pass | No commit, push, PR mutation, merge, deploy, activation, bypass, trade, or backtest occurred during review |

### Final focused bug-check

- **Fast pass:** V243-C4-008 restores the dropped parent check without weakening the new control-root containment. All autonomy audit callers provide the root, and the lock still covers the complete rotate/append critical section.
- **Silent-failure pass:** loosened control ancestry, out-of-root evidence, held locks, and audit write/rotation failures now produce caller-visible denials. No success-shaped policy or audit result remains for the reproduced cases.
- **Edge-case pass:** contained and sibling paths; trusted and `0777` parents; symlinked/loose/out-of-root audit files; malformed/revoked policies; held/stale lock; threshold rotation; ten current plus twenty prior concurrent writers; executor audit redirection; and exact collected systemd state were reviewed.
- **Residual fail-safe behavior:** an abruptly killed lock owner can leave a stale lock and deny later actions. The lock is inside the protected owner-only root and the outcome is fail-closed availability loss, not an authority expansion; it remains non-actionable for this correction.
- **Tool escalation:** direct trust and concurrency probes plus existing source-cited systemd research were sufficient; no broad scanner or duplicate Researcher consult was warranted.

### Validation receipt

- Focused audit/control/lifecycle coverage passed: 40/40 (20 hook + 7 control-plane + 13 live).
- `npm --prefix term-control-center run test:sandbox` passed: 26 structural plus 13 live.
- `npm --prefix term-control-center run typecheck` passed.
- `npm --prefix term-control-center run build` passed; only known non-failing Vite warnings appeared.
- `git diff --check` passed; no `agentops-verify-*` scope remained.
- Independent policy-parent fixture: `readPolicy()` returned `deny_policy_untrusted` after parent mode changed to `0777`.
- Independent current lock race: 10/10 writers succeeded; the audit contained the marker plus ten records, rotated evidence existed, and no lock remained.
- KISS AST: 22 cumulative TypeScript files / 428 functions checked; no remediation-introduced violation.
- PR/issue/main state was independently confirmed through authenticated GitHub REST; no GitHub write was made.
- Skipped: no Kody rerun or PR comment/review was triggered because fixes are not yet committed/pushed and those actions belong to the configured Git Manager/Code Reviewer gates.

### Required follow-up

The correction is verifier-approved. Git Manager is the next implementation-workflow actor for any authorized commit/push to PR #252; Code Reviewer may coordinate an explicit Kody rerun only after the pushed head exists. This verdict does not supply or bypass the configured human GitHub-mutation gate. Native activation remains a separate human/security action.

## Machine Status

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "4 - post-PR Kody remediation",
  "revision_reviewed": 9,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "completed_no_findings",
  "next_actor": "git-manager",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/issue-243-native-session-safe-autonomy/verifier-report.md"
}
```
