# Coder Handoff — Issue #283

## Active authority state — CP-3 authorized

- CP-2 is verifier-approved at revision 7. Lead authorized CP-3 (FR-6/7/8/9/12) on 2026-07-24; CP-3 is active.
- CP-3 implementation history: shared panel mounts, receipted injection endpoint, lazy pool runtime seam, review-server conversation adapter, and preview-only QA receipt matrix were added. Final visual capture evidence remains pending browser availability.

## Active authority state — CP-2 revision 4

- **Active checkpoint:** CP-2 only. CP-1 is approved and retained below as history; CP-3 has not started and remains unauthorized.
- **Authority:** Lead authorized bounded CP-2 implementation, ordinary verifier revisions, and final CP-2 validation on 2026-07-23. After revision 4's verifier cap, lead explicitly authorized the five remaining in-scope CP-2 integration fixes on 2026-07-24; this continuation remains active.
- **Allowed now:** CP-2 structured-memory/budget seams, existing launch/delegation integration, page-bot bootstrap/dedication seams, focused tests, and this run folder.
- **Forbidden now:** `sessionStore.ts` unless genuinely shared, `comsAdapter.ts`, `comsWire.ts`, `comsTransport.ts`, bridge enablement, CP-3 panel/injection/review-server work, deployment, PR, merge, GitHub mutation, secrets, and raw transcript persistence.
- **Stop condition:** verifier approval of CP-2 followed by its required final bug-check approval. No CP-3 work or PR creation.

## Authority and scope

- Canonical source: GitHub issue #283. CP-1 is approved; the active checkpoint is CP-2 (FR-3, FR-4, FR-5, FR-10, guardrails (b)/(c)).
- Lead authorized ordinary CP-2 implementation and verifier-revision continuation on 2026-07-23. CP-3 remains unauthorized.
- Allowed: conversation-store/control-pool history; CP-2 memory, existing launch/delegation, bootstrap, focused tests, and this run folder.
- Forbidden: `sessionStore.ts` changes unless genuinely shared; `comsAdapter.ts`, `comsWire.ts`, `comsTransport.ts`, bridge enablement, CP-3 panel/injection/review-server work, deployment, PR, merge, GitHub mutation, secrets, and raw transcripts.
- Stop condition: verifier-approved CP-2. Do not begin CP-3 or open a PR.

## Pre-edit record

- Branch: `prd/page-bot-platform-283`.
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-283`.
- `git status --short --branch`: clean; no pre-existing dirty files.
- Existing placement evidence: state persistence lives under `term-control-center/server`; focused Node tests live under `term-control-center/tests`; no new directory is needed.
- Coms identity: `coder@agentops-trio`; live pool peers observed: `lead`, `verifier`. The lead's task direction identifies this worktree and verifier as the active run. Before the first verifier request, re-run liveness/isolation preflight and record the result.

## CP-1 design

- New `conversationStore.ts`: persistent state-directory store with discriminated keys: `{ scope: "project", projectId, conversationId }` and `{ scope: "job", jobId, conversationId }`. Each append increments a per-conversation revision and stamps the retained turn; fresh store instances reload the same file. The store is a new path, separate from `sessionStore.ts`, and uses the latter only as a persistence/permissions model.
- Extend `draftComs.ts` with separate control-plane/project and implementation/job pool derivation. Scope-prefixed pool names and scope-bound digests prevent a control-plane pool identity from equalizing with an implementation pool identity for the same worktree and identifier.
- An attestation must exactly match the derived pool scope and pool name before an adapter configuration can be created. The existing adapter then retains its configured project and cannot discover a peer in the other pool. Tests cover both bootstrap attestation rejection and both cross-pool send directions.
- `agentopsComsBridge.ts` remains untouched; its bridge is not enabled and no bridge-on behavior is added.

## Validation plan

1. Focused conversation-store and pool-isolation tests.
2. `cd term-control-center && npm test`
3. `cd term-control-center && npm run typecheck`
4. `cd term-control-center && npm run build`
5. `PYTHONPATH=src python3 -m pytest tests -q`

Known baseline exceptions may be recorded only if reproduced: the Python `test_unlinked_merged_pr...` failure and the documented Node flakes.

## CP-1 implementation

- Added `term-control-center/server/conversationStore.ts` as the standalone state-directory persistence path. It stores both discriminated key shapes in `conversations.json`, increments a conversation revision on every append, stamps each stored turn with that revision, preserves files at mode `0600` under a `0700` directory, and fails closed rather than overwriting malformed audit state.
- Extended `term-control-center/server/draftComs.ts` without changing `draftComs()` compatibility. `controlPlaneComs()` and `implementationComs()` create scope-prefixed, scope-hashed pool identities under distinct coms directories. `attestedComsConfig()` rejects any operator pool-name attestation not exactly matching the derived identity before configuring the existing `ComsAdapter`.
- No changes were made to `sessionStore.ts`, `comsAdapter.ts`, `comsWire.ts`, `comsTransport.ts`, or `agentopsComsBridge.ts`. The bridge therefore gains no enablement behavior.
- Added focused tests: restart-equivalent fresh-store reload with both key shapes and monotonic stamps; malformed audit-state rejection; control-plane↔implementation attestation rejection and bidirectional no-delivery through the existing adapter protocol.

## Changed files

- `term-control-center/server/conversationStore.ts`
- `term-control-center/server/draftComs.ts`
- `term-control-center/tests/conversationStore.test.ts`
- `term-control-center/tests/comsPool.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-283-page-bot-platform/coder-handoff.md`

Two unowned files appeared after the recorded pre-edit clean status and remain untouched/excluded from CP-1: `dev-plans/agentops/coder-verifier-workflow/modula-workflow-requirements.md` and `dev-plans/agentops/coder-verifier-workflow/operating-model.md`.

## Validation

- Focused: `cd term-control-center && node --import tsx --test tests/conversationStore.test.ts tests/comsPool.test.ts` — passed, 3/3.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build` — passed; existing Vite non-module-script and chunk-size warnings only.
- `cd term-control-center && npm test` — 1121 passed, 5 documented baseline failures: PI_COMS label, fix-loop findings, Browser-QA pane, lane slots, verification-sandbox protected child.
- `PYTHONPATH=src python3 -m pytest tests -q` — 1321 passed and 60 subtests passed; sole documented baseline failure: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`.
- `git diff --check` — passed.

This fresh worktree has no local `term-control-center/node_modules`. For the Node checks only, an ephemeral symlink to the already-installed sibling worktree dependency directory was created and removed after each command; the commands executed the current worktree's sources and tests. No dependency, lockfile, or generated source change was retained.

## Revision 2 — verifier findings addressed

- Lead disposition on `V283-CP1-001`: upheld. CP-1 owns the storage seam, while E0 alone owns the future closeout trigger. `archiveJob(jobId, artifactRoot)` now copies all revision-stamped job conversations into an artifact-root `conversations/` store; the regression removes the live file and reloads the archived job record, while proving project records do not enter that archive.
- `V283-CP1-002`: persisted conversations now require a complete ordered `1..N` turn-revision chain with conversation revision exactly `N`. Reversed, duplicated, and conversation/last-turn mismatch regressions fail closed.
- `V283-CP1-003`: persisted collection validation now rejects duplicate logical keys across either discriminator shape.
- `V283-CP1-004`: added a two-page-bot control-plane request/reply test through unchanged `ComsAdapter`, including `conversation_id` preservation, alongside the bidirectional cross-pool rejection test.
- `V283-CP1-005`: split pool exchange and isolation into focused tests and helpers; test callbacks remain under the 20-line gate.

### Revision 2 validation

- Focused store/pool tests — passed, 6/6.
- `cd term-control-center && npm test` — 1124 passed; 5 documented Node baseline failures only.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build` — passed; existing Vite warnings only.
- `PYTHONPATH=src python3 -m pytest tests -q` — 1321 passed plus 60 subtests; sole documented Python baseline failure only.
- `git diff --check` — passed.

## CP-1 approval

- Verifier approved CP-1 revision 2 with zero open findings: FR-1/AC-1, FR-2/AC-2, and guardrail (a) are complete. The approved verdict is recorded at `dev-plans/agentops/coder-verifier-workflow/runs/issue-283-page-bot-platform/verifier-report.md`.
- `V283-CP1-001` through `V283-CP1-005` are all addressed. The lead's archive-seam disposition is implemented without adding E0 closeout triggering or any CP-2/CP-3 work.
- CP-1 is complete. No PR was opened.

## CP-2 authority and scope

- Lead authorized CP-2 (FR-3, FR-4, FR-5, FR-10, guardrails (b)/(c)) on 2026-07-23; CP-3 remains forbidden.
- Allowed: project-memory structured-record/budget seams, existing launch/delegation integration, page-bot bootstrap seam, focused tests, and this run folder.
- Forbidden: raw transcript or secret persistence, a new launch path, routes/UI beyond the existing configuration seam, bridge enablement, CP-3 panel/injection/review-server work, PRs, or deployment.

## CP-2 implementation — pending verifier review

- Added `pageBotPlatform.ts`: per-surface D3 defaults, model/effort rebind values compatible with `AgentPaneConfig`, structured turn shape, and a bootstrap that selects only the requested page key.
- `projectMemory.ts` now has `writeStructuredTurnRecord()` that persists a typed record separately from legacy checkpoint text and supports a validated per-call recall budget rather than forcing every consumer to `RECALL_LIMIT=5`.
- Added focused bootstrap isolation, secret-shaped structured-turn rejection, runtime rebind, structured-record/no-text, redaction, and recall-budget tests.

### CP-2 validation

- Focused page-platform/project-memory tests — passed, 17/17.

### CP-2 revision 2

- Bound structured turn records to the page-bot surface adapter and use the surface recall budget for write→recall.
- Unified the memory record type with the page-bot record, validate page identities, resolve configured model provider metadata, bind bootstrap state to a session identity, and expose start/compaction/clear/renewal re-bootstrap.
- Full gates: Node 1129 passed with five documented baselines; build/typecheck passed; Python 1321 passed plus 60 subtests with the sole documented baseline.
- `cd term-control-center && npm test` — 1128 passed; five documented Node baseline failures only.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build` — passed.
- `PYTHONPATH=src python3 -m pytest tests -q` — 1321 passed plus 60 subtests; sole documented Python baseline failure only.

## CP-2 revision 4 — round-3 findings addressed

- `V283-CP2-002` / guardrail (c): moved page-bot memory records to `pageBotMemoryRecord.ts`. Records contain only typed event/outcome/identifier fields; they have no free-text summary or references. The lowest writer validates the record and recall renders meaningful event/outcome/subject data. Regression coverage proves raw user/assistant transcript-shaped text is rejected and absent from retained export/recall.
- `V283-CP2-003` / FR-10: the lowest structured writer accepts only the canonical six roles and a canonical role-owned surface ID. Subject/reference metadata is restricted to bounded identifiers and rejects GitHub/OpenAI/token-shaped IDs. `safeSource()` now redacts token-shaped checkpoint provenance before disk write.
- `V283-CP2-004`: added persisted `pageBotModelSettings.ts`, with schema versioning and all six D3 defaults (Planner/Author/CEO Reviewer deep; Review Manager/QA Manager/Editor fast). A saved editor override is re-read and resolves into `defaultPageBotSurface()`.
- `V283-CP2-005`: extended the existing role/launch protocol for the six page roles. `pageBotPane()` and `rebindPageBot()` resolve profiles through `resolvePaneLaunchPlan`; `pageBotLaunchPlan()` invokes the existing `buildCoderVerifierLaunchPlan()` machinery, preserving page role identity and its configured provider/model/effort/runtime. Focused coverage executes configured Codex, delegated Claude, and Pi-compatible bindings plus switching.
- `V283-CP2-006` / guardrail (b): `PageBotSurfaceRegistry` owns canonical surfaces and server-held session IDs. Session opening rejects role/surface mismatch; forged IDs fail before access. `runPageBotOperation()` and `sendPageBotComs()` enforce the registry may/may-not capability list at tool/coms operation boundaries. Regressions cover forged sessions, cross-role open, and disallowed capability denial.
- `V283-CP2-007`: lifecycle bootstrap now has one `PageBotStateLoader` and calls it on start, compaction, clear, and renewal for current role prompt, master PRD, board, and the registry-selected own page only. A versioned counting loader proves each lifecycle event re-reads new own state and never reads an Editor sibling.
- `V283-CP2-009`: the active authority section above supersedes no historical record; it makes CP-2 scope/stop state explicit while the CP-1 and earlier CP-2 sections remain durable history. `review-request-r4-cp2.json` is the active complete request artifact.

### Cumulative CP-2 changed files

- `term-control-center/server/pageBotPlatform.ts`
- `term-control-center/server/pageBotMemoryRecord.ts`
- `term-control-center/server/pageBotModelSettings.ts`
- `term-control-center/server/projectMemory.ts`
- `term-control-center/server/rolePrompts.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/protocol.ts`
- `term-control-center/tests/pageBotPlatform.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- this handoff and the CP-2 review-request artifacts

### Revision 4 validation

- Focused: `cd term-control-center && node --import tsx --test tests/pageBotPlatform.test.ts tests/projectMemory.test.ts` — passed, 18/18.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm test` — 1130 passed; five documented baseline failures only: PI_COMS model-label inheritance, fix-loop task-detail wiring, Browser-QA preflight, lane-cap error text, verification-sandbox protected child.
- `cd term-control-center && npm run build` — passed; existing Vite non-module-script and chunk-size warnings only.
- `PYTHONPATH=src python3 -m pytest tests -q` — 1321 passed plus 60 subtests; sole documented baseline failure `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`.
- `git diff --check` — pending final pre-send re-run.

## CP-2 revision 5 — authorized integration in progress

- Lead authorized the five remaining in-scope findings after revision 4. The current bounded integration adds a Settings-owned authenticated page-bot model endpoint, a `pageBotRuntime` launch/lifecycle seam that derives the CP-1 control-plane pool and injects current scoped bootstrap into the existing launch prompt, private registry maps with cloned/frozen surface records, all-role protocol parsing, and grouped structured-turn/memory inputs for KISS.
- The trusted registry now clones/freezes registered surfaces and keeps session/surface maps private. Protocol parsing accepts all six page roles. The runtime regression starts then renews a Planner with a versioned loader and proves that the actual existing launch prompt receives current role/PRD/board/own-page bootstrap plus the CP-1 control-plane env.

### Revision 5 validation

- Focused page-platform/project-memory tests: 19/19 passed.
- `cd term-control-center && npm test`: 1131 passed; five documented baseline failures only (PI_COMS label, fix-loop wiring, Browser-QA preflight, lane-cap text, verification-sandbox protected child).
- `cd term-control-center && npm run typecheck`: passed.
- `cd term-control-center && npm run build`: passed; existing Vite non-module-script/chunk-size warnings only.
- `PYTHONPATH=src python3 -m pytest tests -q`: 1321 passed plus 60 subtests; sole documented baseline `test_unlinked_merged_pr_emits_warning_row`.

## Active authority — CP-3 revision 3 (supersedes every earlier “active” block above)

- **Authority:** Lead authorized CP-3 and ordinary verifier revisions through final CP-3 verification on 2026-07-24. This is the only active authority block; all CP-1/CP-2 and earlier CP-3 authority blocks above are durable history.
- **Allowed:** FR-6/7/8/9/12 wiring, focused regressions, the existing SPA and vanilla shell adapters, CP-1-store integrity repair, and this run folder.
- **Forbidden:** deployment, PR/merge/GitHub mutation, secrets, bridge enablement, raw transcript-to-memory work, and browser capture. CP3-006 remains operator-pending.
- **Stop condition:** verifier approval of CP-3 (excluding CP3-006) followed by the required steward review and verifier bug-check approval.

## CP-3 revision 3 — functional re-anchor and finding disposition

- **V283-CP3-001 / FR-6:** `pipeline-diagram/page-bot-panel.js` is the sole shared DOM render/state contract. It owns the collapsible right panel, role/model header, transcript, visible receipt, and prompt input. The React adapter imports that canonical module through its symlink and mounts it into the terminal workspace; the vanilla shell loads the same file before `coworker-launcher.js`, which mounts the same adapter. SPA conversations are fetched per `{projectId,surfaceId}`; vanilla maps its persisted coworker conversation into the same contract. The panel uses standard responsive right-rail styling.
- **V283-CP3-002 / FR-7 / guardrail (e):** `pageBotInjectionService` validates a fixed trusted surface registry and a non-empty dated edit-note receipt, appends a typed injection record, returns a deep-link target, and its panel-message adapter renders the receipt visibly. `/page-bot/inject`, `/page-bot/message`, and `/page-bot/conversations/:projectId/:surfaceId` are token-gated. `sendToLead()` and `deliverChatPulse()` both reuse that seam; the shared vanilla panel’s send handler opens/collapses through the same adapter. `pageBotInjection.test.ts` proves delivery, visible receipt mapping, receipt-less rejection, and untrusted-target rejection.
- **V283-CP3-003 / FR-8:** `createPageBotRuntime()` now wires accepted messages to an async lazy pool. `spawnConfiguredPageBot()` builds the configured existing launch plan and starts its configured CLI process with the first message, while idle shutdown sends SIGTERM. The server delivery hook invokes it for every trusted non-Lead first-message/injection path. Regression coverage proves absent-before-message, one spawn/reuse, message propagation, and idle stop.
- **V283-CP3-004 / FR-9 / guardrail (d):** `ProjectConversationMap` now provides mutation-aware nested dict/list values, so ordinary `messages.append`, field assignment, and `pop` all persist. Reload uses `dict.__setitem__`, so it never manufactures a revision. Fresh-adapter tests prove session Q&A and CEO round convergence reload, plus exact delete/clear behavior.
- **V283-CP3-005 / CP-1 regression:** the Python adapter is strict and fail-closed: full revision-chain/schema and duplicate-key checks run before every read/write; malformed state is retained and rejected. It writes actual UTC timestamps, uses `0700` state directories and `0600` atomic replacements, exact project/kind deletes, and a shared `conversations.json.lock` exclusive-create lock compatible with the TypeScript store. Concurrent-writer coverage is isolated under temporary `XDG_STATE_HOME`; the previously contaminated real state path was neither read nor changed.
- **V283-CP3-007:** this active, cumulative section and `review-request-r3-cp3.json` record authority, scope, findings, changed files, exact validation, and pending Browser-QA state. Earlier authority sections are historical only.
- **V283-CP3-008:** persistence is split into small typed helpers for state-dir/lock/read/validate/write and mutation-aware values. The oversized `persist()` was replaced; redundant `review_server.py` comments were removed.
- **V283-CP3-006:** operator/browser-QA pending. No screenshot, live/review-server/CDP port, or fabricated evidence was touched. `qa-receipts/f4/cp3-panel-receipts.md` remains a planning matrix, not an AC-11 receipt.

### CP-3 revision 3 changed files

- `pipeline-diagram/page-bot-panel.js`, `pipeline-diagram/{board,completed,matrix,timeline}.html`, `pipeline-diagram/coworker-launcher.js`
- `term-control-center/src/{PageBotPanel.tsx,pageBotPanelContract.js,pageBotPanelContract.d.ts,App.tsx}`
- `term-control-center/server/{conversationStore.ts,pageBotInjection.ts,pageBotLazyPool.ts,pageBotRuntime.ts,index.ts}` and `term-control-center/vite.config.ts`
- `term-control-center/tests/{conversationStore,pageBotInjection,pageBotLazyPool,pageBotPlatform}.test.ts`
- `src/agentops_harness/{conversation_store.py,review_server.py}` and `tests/unit/test_conversation_store.py`
- this handoff and `review-request-r3-cp3.json`

### CP-3 revision 3 validation

- Focused Node: `cd term-control-center && node --import tsx --test tests/conversationStore.test.ts tests/pageBotLazyPool.test.ts tests/pageBotInjection.test.ts tests/pageBotPlatform.test.ts` — passed, 14/14.
- `cd term-control-center && npm run typecheck` — passed using an ephemeral sibling dependency symlink; removed afterward.
- `cd term-control-center && npm run build` — passed; existing Vite non-module-script and chunk-size warnings only.
- `cd term-control-center && npm test` — 1135 passed and five documented baseline failures only: PI_COMS label, fix-loop wiring, Browser-QA preflight, lane-cap error text, and verification-sandbox protected child. The coworker-cache baseline was rechecked after restoring its existing cache key and passed.
- `XDG_STATE_HOME=$(mktemp -d) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — 1325 passed plus 60 subtests; sole documented baseline failure: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`.
- `git diff --check` — passed.

### CP-3 revision 4 — bounded integrity and token corrections

- `pageBotInjectionService` is now created per `createTermServer({stateDir})` with a per-server delivery closure; it no longer uses a module-global default store/hook. Its configured state directory is the same context as the term server.
- Python rejects boolean revision values, and `tests/conftest.py` establishes a temporary `XDG_STATE_HOME` before review-server imports, making the canonical Python house command non-destructive to operator state.
- The canonical shared panel CSS now uses only unprefixed design tokens and has no legacy `--ao-*`, raw hex fallback, or raw pixel font-size values.
- Remaining round-3 panel/runtime functional findings are still under active bounded repair; this revision is submitted for recheck only if verifier can confirm the fixed integrity and F1/F2 sub-findings without treating browser QA as required.

### Lead ruling after revision 4

Lead explicitly authorized continuation beyond the ordinary revision cap on 2026-07-24. CP3-001/002/008 remain in scope. CP3-003 is narrowed to one real configured generic runtime proving spawn → message → reply → idle-out; full six-role page-bot behavior remains PL1+/E0 out of scope. CP3-002 requires a demonstrable Lead stub consumer, not E0 Lead behavior. CP3-006 remains operator-pending.

### CP-3 revision 5 request

- Vanilla no longer creates `#coworker-panel`; its retained legacy content is hidden while the shared `page-bot-panel` is the only visible frame. The shared lead adapter consumes the `agentops-page-bot-injection` stub event and opens with the receipted message.
- `sendToLead` and `deliverChatPulse` are directly covered against the same persistent service seam. The configured runtime now sends every user turn through child stdin and appends stdout replies to the mounted conversation store.
- Focused Node 10/10, typecheck/build passed. Full pytest: 1325 passed + 60 subtests; one documented baseline failure. CP3-006 remains operator-pending.

### CP-3 revision 6 request

- The shared mount now adopts the existing coworker content as its transcript/content slot rather than hiding it. `#coworker-panel` is absent; the legacy content is moved into the only shared panel frame.
- Shared shell header has model and effort picker controls; vanilla binds its configured provider selection to the shared header.
- Typecheck and JS syntax passed. CP3-006 remains operator-pending.

### CP-3 revision 7 request

- Shared shell mount is split into creation, controls, composer, rendering, and binding helpers. Adopted vanilla content has its legacy bar/input/provider removed before slot adoption; only the outer shared header/compose controls remain.
- Vanilla supplies canonical lower-case provider IDs and effort values with an `onBinding` handler. React supplies the same state shape. The contract declaration now covers content, effort, binding, and exported helpers.
- Focused Node 10/10 and typecheck pass; no Browser-QA capture attempted.

### CP-3 revision 8

- Retained legacy coworker references are now hidden rather than removed before existing initialization binds them, so the adopted shared content no longer dereferences null controls while only the shared controls are visible.

### CP-3 revision 9

- Shared composer exposes `prefill()` and proposal supersede/timeline replan now target that visible composer rather than the retained hidden legacy textarea.

### CP-3 revision 10 — CP3-001 and CP3-008 only

- **V283-CP3-001:** The shared shell now owns the authenticated Settings binding client: it loads each role's persisted model profile, its allowed effort choices, and the configured selection from `/api/admin/projects/:id/page-bot-models` plus `/launch-profiles`; it saves selection changes through that Settings endpoint with the admin CSRF token. React delegates its `onBinding` to this client; vanilla reloads it at mount and active-project changes. The vanilla send now passes the configured profile provider plus effort to its runtime endpoint; the Python handler passes effort as `reasoning` to `call_cli`. Term-page sends carry the binding, and the lazy page-bot runtime detects a saved binding change, stops the stale process, and starts the next send with the saved model/effort.
- Added the `lead` binding to the persisted settings schema for the existing vanilla Lead shell; it seeds deep/xhigh and remains backward-compatible with prior six-role settings files. The six page-bot roles retain their D3 defaults.
- **V283-CP3-008:** `PageBotPanel()` is six lines; `panelState()` uses one typed panel-state object instead of seven positional state values. `createPageBotInjectionService()` delegates target/message/read responsibilities to small helpers. The stale `refs` locals were deleted from proposal supersede and timeline replan. Vanilla panel host/content/state setup is split out of `ensure()`.
- Regression coverage saves Planner and Lead bindings, re-reads the persisted store, verifies both adapter sources use the shared Settings load/save methods, and proves a changed saved effort restarts the lazy runtime on the next send. The coworker route regression proves the vanilla effort reaches `call_cli(reasoning=...)`.
- CP3-006 remains **operator-deferred**. No browser capture, live/review-server/CDP port, or receipt fabrication was attempted.

### Revision 10 validation

- Focused Node: `cd term-control-center && node --import tsx --test tests/pageBotPlatform.test.ts tests/pageBotInjection.test.ts tests/pageBotLazyPool.test.ts tests/coworkerLauncher.test.ts` — passed, 19/19.
- Focused Python: `XDG_STATE_HOME=$(mktemp -d) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests/unit/test_review_server_coworker.py -q` — passed, 95/95.
- `cd term-control-center && npm run typecheck` — passed.
- `cd term-control-center && npm run build` — passed; existing Vite non-module-script and chunk-size warnings only.
- Design-token gate: `cd term-control-center && node --import tsx --test tests/designTokens.test.ts` — passed, 11/11.
- `cd term-control-center && npm test` — 1137 passed; five documented baseline failures only: PI_COMS label, fix-loop wiring, Browser-QA preflight, lane-cap error text, and verification-sandbox protected child.
- `XDG_STATE_HOME=$(mktemp -d) PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest tests -q` — 1326 passed plus 60 subtests; sole documented baseline failure: `tests/unit/test_completed_work.py::CompletedWorkTests::test_unlinked_merged_pr_emits_warning_row`.
- `git diff --check`, JS syntax checks for both panel files, and Python compilation passed.

### CP-3 revision 11 — bounded route/auth and KISS completion

- **V283-CP3-001:** Settings requests now use the canonical `/term` base on either shell. Before a guarded request, the shared adapter obtains/reuses `window.__TERM_CONTROL__.token` from `/term/term-config.js`; a failed binding load is visible as an explicit vanilla panel status. Vite now proxies canonical and compatibility `/term` launch-profile/Admin Settings routes. The shared client therefore reaches its guarded model-profile source and Settings endpoint in the shipped topology.
- **V283-CP3-008:** React binding saves use one typed update object. Lazy-pool construction/touch/stop are separate small helpers. Vanilla `ensure()` is now a nine-line coordinator with element construction, ref collection, and listener binding separated. The canonical declaration now includes `prefill()` plus the exported model-settings API. The coworker effort is grouped in a `CoworkerRuntime` value rather than adding a sixth `coworker_chat()` parameter.

### Revision 11 validation

- Focused Node (panel, injection, lazy pool, coworker, design tokens): passed, 30/30.
- Focused Python coworker: passed, 95/95.
- `npm run typecheck` and `npm run build`: passed; existing Vite warnings only.
- `npm test`: 1137 passed; five documented baseline failures only.
- `pytest tests -q`: 1326 passed plus 60 subtests; sole documented baseline failure only.
- `git diff --check`, JS syntax, and Python compilation passed.

### CP-3 revision 12 — final CP3-008 API grouping

- Replaced the string-subclass runtime with explicit frozen `CoworkerChatInput` (`provider`, `board_context`, `project_id`, `reasoning`). `coworker_chat()` now accepts only `(session_id, message, input)`. The HTTP handler and every direct coworker test caller construct the typed input; no hidden state remains.
- Focused Python coworker suite passed, 95/95. The four house gates from revision 11 remain green with the documented five Node and one Python baseline failures; this bounded final change was additionally Python-compiled and focused-tested.

### Final bug-check repair

- Added term-token-authenticated page-bot model routes, visible panel error state with restored failed prompts, pending-stop/retry-safe lazy-pool entries, and newline-framed child reply buffering with child liveness/write checks.
- Added lazy-pool pending-stop and failed-spawn retry regressions. Focused lazy tests passed 3/3; typecheck/build passed; pytest retained its single documented baseline (1326 passed plus 60 subtests).
