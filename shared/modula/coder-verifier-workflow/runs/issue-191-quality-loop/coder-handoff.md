# Coder handoff — Issue #191 Quality Loop

## Continuation authorization

The operator authorizes iterative coder/verifier revisions for issue #191 through final verifier bug-check. Do not pause for routine implementation findings, tests, coverage, KISS cleanup, or validation evidence. Escalate only for the contract's true human-gate conditions; this authorization does not permit PR creation, GitHub mutation, merge, deployment, approval, trading, or backtesting.

## Source of truth

- PRD: https://github.com/hyperbotsx/agentops-harness/issues/191
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-191`
- Branch: `prd/quality-loop-ceo-review-followup-191`
- Status: checkpoint 1 design pending verifier review

## Pre-edit state

- `git status --short --branch`: clean (`prd/quality-loop-ceo-review-followup-191...origin/main`)
- Pre-existing dirty files: none.
- Memory is disabled and was not used; the PRD, repository, project configuration, GitHub state, and verifier evidence govern.

## Scope controls

- Allowed scope: the issue #191 quality-loop implementation, focused tests/docs, and this run folder.
- Forbidden: PR/merge/deploy, PRD approval, autonomous Issue/PRD creation, GitHub mutation without explicit confirmation, #190 Git/PR workflow, secrets/raw transcripts/private data, and repo-local copies of the standards pack.
- Stop condition: final verifier bug-check approval or human escalation.

## Checkpoints

1. Context brief foundation: read-only role/step, run/skip routing, durable `project-context-brief.md`, and pre-coder sequencing.
2. Coder handoff and verifier validation receipt.
3. Planner configured-Claude default and plan-mode fallback.
4. CEO review audit/calibrated evidence-backed output.
5. Completed Jobs Follow-Up capture and explicit Issue/PRD route confirmation.
6. Steward hygiene review, required validation, and final verifier bug-check.

## Mandatory researcher consults (2026-07-14)

1. Planner model and `/plan`: current default profile is `pi-claude-opus` (`opus`) when no admin override exists, but the implementation must select the first configured Claude profile rather than hardcoding that ID. Claude Code 2.1.195 supports plan permission mode; current delegated task transport cannot truthfully claim a literal `/plan` invocation, so use explicit planning instruction/plan mode fallback unless transport changes.
2. Term Control launch: Board submits explicit Planner panes, so server profile selection plus `/launch-profiles` default metadata and Planner-only UI selection are required; preserve authoring/review/implementation defaults.
3. Completed Jobs: add Follow-Up at `pipeline-diagram/completed.html` `actionsCell(row)` with a separate follow-up record/session; never reuse completion lifecycle state or attach to an old implementation group.
4. CEO review: calibrate `ceo_review_answers.py`/review output while preserving existing `ceo_review.py` fail-closed gate and approval apply path; use golden fixtures.
5. Follow-Up Issue route: existing `POST /coworker/issues/create` requires server-held pending draft, matching session/project scope, and exact `create issue` confirmation. It needs isolated auth, timeout, and canonical readback before this feature may report success.
6. Standards: canonical pack is `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1/`; use role-specific canonical files and do not duplicate the pack locally.

## Checkpoint 1 design

- Add a dedicated read-only Project Context Brief role rather than making coder/verifier perform the brief.
- Route medium/large, cross-cutting, frontend/backend-contract, shared-schema, launch/completion, prompt/memory/GitHub/browser-QA work to the brief; skip tiny, docs-only, one-file, and explicitly disabled work with a recorded reason.
- Persist only the concise source-cited `project-context-brief.md` in the job artifact folder. The prompt will require binding scope, reuse candidates, duplicate-code traps, architecture/state/security boundaries, validation, verifier/steward focus, and fact-vs-assumption separation.
- The design must prevent coder start until the brief is completed or the operator explicitly chooses a documented degraded/skip path. The role remains read-only and cannot mutate GitHub or implementation files.
- Expected implementation surfaces: `scripts/agentops/pi-agent.sh`, Term Control launcher/profile/prompt and launch-transition code, Board launch UI, focused Term Control tests, and this run folder. No product feature routes outside launch/context behavior.

## Checkpoint 1 design revision

### Deterministic routing contract

`TaskContext.contextBrief` will be an optional structured launch input, not inferred from later changed files:

- `policy`: `auto`, `required`, or `skip`; `required` and `skip` are explicit operator overrides and `skip` requires a non-empty `reason`.
- `scope`: `tiny`, `small`, `medium`, `large`, `xl`, `one-file-fix`, `docs-only`, or `unknown`, supplied by the PRD/task launcher.
- `surfaces`: a bounded set of declared classifications: `cross-cutting`, `frontend-backend-contract`, `shared-schema`, `launch-flow`, `completion-state`, `agent-prompts`, `memory`, `github-integration`, or `browser-qa`.

The pure router returns `{ decision, reason, operatorOverride }` and is covered at the lowest layer. Precedence is: explicit `required`; explicit `skip` (durably marked as a human override); declared high-risk surface; `medium`/`large`/`xl`; declared `tiny`/`small`/`docs-only`/`one-file-fix`; otherwise `needs_operator_decision`. A high-risk surface wins over an automatic small-scope skip. Unknown or conflicting automatic inputs fail closed as `needs_operator_decision`; they cannot silently launch coder. The decision/reason is persisted beside the brief in `context-brief-state.json` and is propagated into the normal implementation task/handoff context.

### Minimal two-phase contract

- Role ID: `context-brief`. `scripts/agentops/pi-agent.sh` will map it to the canonical global Codebase Expert skill at `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/codebase-expert/SKILL.md`, with a Context Brief-specific runtime prompt. No repo-local skill is created or copied.
- Phase 1: a new `context-brief` launch mode starts only that read-only role. It gets an implementation-style runtime/artifact root and writes `project-context-brief.md` and `context-brief-state.json` in that root. The prompt requires sourced facts vs assumptions and bans edits/GitHub mutation/PR/merge/deploy/trading/backtest.
- Readiness: the server validates the brief/state structure and the recorded `ready` decision before it permits phase 2. A missing, malformed, or failed brief is not treated as ready.
- Phase 2: `POST /groups/:id/context-brief/continue` starts the normal implementation group only after readiness validation. It passes the durable brief path and recorded route decision to coder/verifier. The old brief group is retired only after the new group starts successfully.
- Recovery: `retry` keeps the brief group and re-prompts the read-only role with the missing/invalid artifact feedback. Explicit degraded continuation requires the exact action `continue_without_brief`, a non-empty operator reason, and writes the degraded decision before starting phase 2. Automatic or malformed continuation fails closed. A direct `skip` route writes the same durable skip state before the implementation group starts.

Focused tests: pure required/skip/high-risk/small/unknown/conflict routing; brief role/prompt read-only boundaries; ready artifact allows continuation; missing/failed artifact blocks; retry does not launch coder; explicit degraded continuation records reason; direct skip records the override; and no phase-1 group contains coder/verifier panes.

## Validation planned for checkpoint 1

- Focused Term Control launcher/launch-plan tests for routing, skip/default behavior, read-only prompt boundaries, and pre-coder gate.
- `npm --prefix term-control-center run typecheck` and targeted Node tests if environment permits.
- `git diff --check`.

## Checkpoint 1 implementation

- Added the `context-brief` role and `context-brief` workspace mode. The wrapper maps it to the canonical global Codebase Expert skill; no repository-local skill was created.
- Added typed `TaskContext.contextBrief` policy/scope/surface input and a pure router: explicit required/skip overrides are durable, high-risk and medium+ scope run, declared small scope skips, and unknown input fails closed.
- Implementation launches carrying a run decision start a single context-brief pane instead of coder/verifier panes. The role prompt is read-only and writes `project-context-brief.md` plus `context-brief-state.json` in the runtime artifact root.
- Added `POST /groups/:id/context-brief/continue`: ready artifacts launch the normal implementation group; missing artifacts block, `retry` re-prompts only the brief pane, and `continue_without_brief` requires a non-empty operator reason before writing degraded state and launching the group.
- Direct skip launches persist the durable skip decision beside the implementation artifact root.
- Added focused route tests in `term-control-center/tests/contextBrief.test.ts`.

## Validation

- `npm --prefix term-control-center ci` — completed temporarily for validation; `node_modules` was removed afterward.
- `npm --prefix term-control-center run typecheck` — passed after dependency install.
- `npm --prefix term-control-center run test -- --test-name-pattern='context brief|launch contract|pi-agent wrapper'` — the three new context-brief tests passed, but the package script forwards the pattern after the test glob and ran the broader suite until the 600-second command timeout. Do not treat it as a full-suite pass.
- `git diff --check` — passed.
- `bash -n scripts/agentops/pi-agent.sh` — passed.

## Changed files (checkpoint 1)

- `scripts/agentops/pi-agent.sh`
- `term-control-center/server/contextBrief.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/protocol.ts`
- `term-control-center/tests/contextBrief.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/`

## Checkpoint 1 verifier outcome — needs human

Verifier requested revision 3 with four blocking findings: `F191-C1-001` through `F191-C1-004` in `verifier-report.md`.

- The Board does not supply context-brief metadata or phase controls, leaving normal production launches able to bypass the feature.
- Route state must be server-owned, schema-validated, compared with the task decision, and persisted before any skip/degraded implementation launch.
- Phase 2 must use shared normal-launch lifecycle behavior and phase 1 needs idempotency plus transition coverage.
- The lifecycle handler needs extraction/splitting to meet KISS limits.

The operator authorized continuation on 2026-07-14, including the larger combined UI/lifecycle revision.

### Authorized checkpoint 1 revision

- Board launch now creates structured `contextBrief` metadata from PRD title/body/labels, classifies known workflow surfaces, and gives unknown scope an explicit server-blocked result rather than bypassing the brief.
- After a context-brief group starts, Board shows Continue, Retry, and Continue without brief controls; degraded continuation requires an operator-entered reason.
- Launch-group state writes the server-owned pending/skip decision before starting any pane. Ready state requires the exact task decision/reason/override and a `## Sources` brief section.
- Phase 1 reuses a live context-brief group. Phase 2 uses the shared implementation launcher, including browser activation and reuse handling.
- Validation after temporary `npm ci`: typecheck passed; `tests/contextBrief.test.ts`, `tests/launcher.test.ts`, `tests/launchPlan.test.ts`, and `tests/protocol.test.ts` passed (68 tests). Removed `node_modules` afterward. `git diff --check` and shell syntax passed.

Request verifier re-review before checkpoints 2–5.

## Checkpoint 2 — validation receipts and handoffs

Checkpoint 1 is approved through explicit human override recorded by verifier. Checkpoint 2 will add concise coder/verifier prompt contracts and operator documentation only; it will reference the canonical global standards pack, not copy it. The implementation will require coder handoffs to name context-brief use/skip, acceptance coverage, commands/results, skips, risks, cleanup, and standards exceptions. It will require final verifier receipts at the runtime artifact root with acceptance coverage, reviewed surfaces, commands, skips, edge cases, risks, standards summary, findings, follow-up, and next actor.

### Checkpoint 2 implementation

- Updated coder/verifier launch prompts with the required handoff and final validation-receipt fields.
- Prompts reference the canonical global standards location and explicitly forbid local copies.
- Added `docs/implementation-quality-loop.md` for context-brief use, handoff/receipt expectations, scoped validation, and standards references.
- Added launch-prompt regression coverage.
- Validation: typecheck passed; `tests/launchPlan.test.ts` and `tests/contextBrief.test.ts` passed (31 tests); diff/shell checks passed. Temporary dependencies removed.

### Checkpoint 2 revision

- Added implementation-summary/finality, forbidden-action, checkpoint/deviation, and fail-closed evidence requirements to coder/verifier prompts and docs.
- Standardized the receipt as a `## Validation Receipt` section inside co-located `verifier-report.md`.
- Completion discovery now requires that section before treating an approved/passed verifier report as completion evidence.
- Typecheck and `tests/launchPlan.test.ts` passed after temporary dependencies; dependencies removed.

Checkpoint 2 revision 2 received `needs_human` for receipt parsing/completion fixtures and KISS extraction. The operator's instruction to do all remaining work is recorded as authorization to continue this bounded revision without narrowing scope.

### Checkpoint 2 continuation revision

- Extracted coder/verifier quality-loop prompt text into `qualityLoopPrompt.ts` with focused tests.
- Receipt parsing now requires an approved final-review declaration plus PRD, checkpoint, acceptance, command, skip, edge-case, regression, and next-actor evidence.
- Added focused receipt/parser and planner-default tests. Typecheck and 10 focused tests passed; temporary dependencies were removed.

### Second authorized checkpoint 1 revision

- Coder-pane implementation launches without `contextBrief` metadata now fail closed; Browser-QA-only launches remain unaffected.
- Board presents an explicit required/skip choice when automatic scope is unknown and restores phase controls on reopening a context-brief group.
- State persistence now creates a private artifact root and atomically replaces the state file.
- Added a fresh-root/exact-decision readiness regression test. Typecheck and all four context-brief tests passed after temporary `npm ci`; dependencies were removed afterward.

## Checkpoint 2 revision 4 — receipt binding and prompt extraction

Addressed verifier findings `F191-C2-002` and `F191-C2-003` under recorded continuation authorization.

- Validation receipts now parse structured, non-empty fields rather than bare substrings. Final completion requires a matching PRD number and title, a final checkpoint, `Decision: approved`, `Final review: yes`, all required receipt fields, and an approved/passed Machine Status in the same report.
- Completion discovery now uses this single receipt/status gate. Focused discovery tests cover valid, missing, malformed, wrong-PRD, non-final, and mismatched-status reports. Existing completion-server fixtures now provide the context-brief skip metadata required by the phase-1 gate and a valid final receipt.
- Extracted role-specific task prompts to `term-control-center/server/rolePrompts.ts` and Claude host/delegation prompts to `term-control-center/server/delegationPrompts.ts`. `launchPlan.ts` is now 255 lines; its launcher orchestration remains separate from prompt construction.
- Prompt output and launch behavior are covered by the existing launch-plan suite; extraction preserved planner, authoring, CEO-review, implementation, memory, browser-QA, and Claude-delegation contracts.

### Changed files (revision 4)

- `term-control-center/server/validationReceipt.ts`
- `term-control-center/server/completionDiscovery.ts`
- `term-control-center/server/rolePrompts.ts`
- `term-control-center/server/delegationPrompts.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/tests/validationReceipt.test.ts`
- `term-control-center/tests/completionDiscovery.test.ts`
- `term-control-center/tests/completion-server.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Validation (revision 4)

- `npm --prefix term-control-center ci` — passed temporarily for validation; `node_modules` was removed afterward.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/validationReceipt.test.ts tests/completionDiscovery.test.ts tests/completion-server.test.ts tests/launchPlan.test.ts` — passed, 38 tests.
- `git diff --check` — passed.

### Skipped checks and risks

- Full package test suite and production build were not run; focused tests cover the altered parser, completion discovery/server fixtures, and prompt/launch contracts.
- Completion still relies on a verifier-authored report as the artifact boundary; malformed, missing, mismatched, or non-final evidence now fails closed.
- No standards exception, cleanup debt, forbidden action, secret, raw transcript, PR/merge/deploy/trading/backtest, or GitHub mutation was introduced.

Request verifier checkpoint 2 revision 4 review. Checkpoint 2 remains incomplete until verifier approval.

## Checkpoint 2 revision 5 — fail-closed completion evidence

Addressed verifier findings `F191-C2-002`, `F191-C2-003`, and `F191-C2-004` under recorded continuation authorization.

- Completion now binds a final receipt to canonical issue number and normalized task title. It accepts only an unambiguously final checkpoint (`final…` or `N — final…`) and exactly one Machine Status from the dedicated `## Machine Status` section. That status must be approved, bug-check passed, and name the same checkpoint. Multiple/stale/ambiguous status blocks fail closed.
- Added adversarial tests for wrong title, negated finality, wrong issue, missing/malformed receipt, revision-requested status, duplicate status blocks, and receipt/status checkpoint mismatch. The existing server launch-block integration fixture now has required context-brief metadata and the valid receipt/status pair.
- Replaced positional launch/delegation arguments with typed option objects and removed the unused prompt import; changed functions have no more than one parameter.
- Updated verifier prompt, docs, and focused tests to record `Decision: <actual verifier verdict>` and `Final review: yes|no`. Only an approved final review may claim approved/yes.

### Changed files (revision 5)

- `term-control-center/server/validationReceipt.ts`
- `term-control-center/server/completionDiscovery.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/delegationPrompts.ts`
- `term-control-center/server/rolePrompts.ts`
- `term-control-center/server/qualityLoopPrompt.ts`
- `term-control-center/tests/validationReceipt.test.ts`
- `term-control-center/tests/completionDiscovery.test.ts`
- `term-control-center/tests/completion-server.test.ts`
- `term-control-center/tests/qualityLoopPrompt.test.ts`
- `term-control-center/tests/server.test.ts`
- `docs/implementation-quality-loop.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Validation (revision 5)

- `npm --prefix term-control-center ci` — passed temporarily for validation; `node_modules` was removed afterward.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/validationReceipt.test.ts tests/completionDiscovery.test.ts tests/completion-server.test.ts tests/qualityLoopPrompt.test.ts tests/launchPlan.test.ts` — passed, 40 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='blocks fresh launch when verifier report says the PRD is complete' tests/server.test.ts` — passed, 1 test.
- `git diff --check` — passed.

### Skipped checks and risks

- Full package suite and production build were not run; the directly affected parser, completion discovery/server, launch, prompt, and regression tests passed.
- Completion fails closed unless the final receipt and exactly one current Machine Status agree; future report writers must preserve the documented `## Machine Status` and `## Validation Receipt` layout.
- No standards exception, cleanup debt, forbidden action, secret, raw transcript, PR/merge/deploy/trading/backtest, or GitHub mutation was introduced.

Request verifier checkpoint 2 revision 5 review. Checkpoint 2 remains incomplete until verifier approval.

## Checkpoint 2 revision 6 — strict Machine Status layout

Addressed the remaining `F191-C2-002` parser ambiguity under recorded continuation authorization.

- Completion requires exactly one `## Machine Status` section and exactly one JSON fence within it. The fence must parse and agree with the matching final Validation Receipt; extra, empty, text-only, or malformed status sections/fences fail closed.
- Expanded focused receipt tests for an empty duplicate status section, malformed duplicate status section, and malformed-plus-valid fences in one status section.
- Documented the required Machine Status/Validation Receipt completion layout in the quality-loop guide.

### Changed files (revision 6)

- `term-control-center/server/validationReceipt.ts`
- `term-control-center/tests/validationReceipt.test.ts`
- `docs/implementation-quality-loop.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Validation (revision 6)

- `npm --prefix term-control-center ci` — passed temporarily for validation; `node_modules` was removed afterward.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/validationReceipt.test.ts tests/completionDiscovery.test.ts tests/completion-server.test.ts tests/qualityLoopPrompt.test.ts tests/launchPlan.test.ts` — passed, 40 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='blocks fresh launch when verifier report says the PRD is complete' tests/server.test.ts` — passed, 1 test.
- `git diff --check` — passed.

### Skipped checks and risks

- Full package suite and production build were not run; all directly affected focused and integration regression tests passed.
- Completion now intentionally fails closed for report layouts that do not have one valid current Machine Status section and a matching final receipt.
- No standards exception, cleanup debt, forbidden action, secret, raw transcript, PR/merge/deploy/trading/backtest, or GitHub mutation was introduced.

Request verifier checkpoint 2 revision 6 review. Checkpoint 2 remains incomplete until verifier approval.

## Checkpoint 2 approval

Verifier approved checkpoint 2 revision 6 on 2026-07-14. Receipt parsing/completion evidence, coder/verifier handoff prompts, global standards references, documentation, and the KISS prompt extraction are accepted. Proceeding to checkpoint 3.

## Checkpoint 3 — planner default and plan-mode fallback

Existing scoped implementation selects the first configured Claude profile for Planner through `plannerDefaultProfileId()`, returns that value from `/launch-profiles`, and makes the Board prefer it when populating the Planner model selector. The role prompt starts with an explicit planning instruction and Claude delegation uses `permission_mode="plan"` for Planner; non-Claude profiles remain selectable and use the instruction fallback.

Checkpoint 3 revision 2: added Claude plan-mode/non-Claude fallback assertions and Board dynamic-default guardrails; updated the stale persistent-state guardrail; and added a `/launch-profiles` route test requiring the advertised Planner default to belong to the returned safe profile list. Validation: temporary `npm ci` passed; typecheck passed; launch profile/plan and Board guardrail suites passed (69 tests); targeted launch-profile route test passed; `git diff --check` passed; `node_modules` removed. Verifier approved checkpoint 3 revision 2 on 2026-07-14. Proceeding to checkpoint 4.

## Checkpoint 4 — CEO review calibration

Added `ceo_review_calibration.py`, an advisory-only calibrated review built from the existing fail-closed findings and human-gated draft answers. It emits strengths, blocking gaps, non-blocking risks, assumptions, missing acceptance/validation/checkpoint evidence, authority concerns, operator questions, source/finding citations, and an evidence-backed approve/revise/reject recommendation. Existing apply and approval paths are untouched. Added a concise audit at `docs/ceo-review-quality-audit.md` and deterministic golden tests for strong, weak-validation, missing-acceptance/checkpoints, forbidden scope, missing owner, dependency ambiguity, and CLI JSON output. Validation: `PYTHONPATH=src python3 -m pytest tests/unit/test_ceo_review.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_calibration.py -q` passed (35 tests); `git diff --check` passed. Checkpoint 4 revision 2: CEO reviewer command guide now runs calibrated-review before an advisory recommendation/approval next action; launch prompt coverage proves this. Calibrated risks exclude owner/dependency conditions already represented as blockers, and finding lines include concrete PRD/label/dependency/section citations. The audit now traces PRD Studio load, issue #191's known-thin fixture, calibration, human answers, preview, approve-intent, stale/auth/readback failures, and unchanged mutation authority. Focused calibration tests pass (7); diff check passes. Checkpoint 4 revision 2: CEO reviewer command guide now runs calibrated-review before an advisory recommendation/approval next action; launch prompt coverage proves this. Calibrated risks exclude owner/dependency conditions already represented as blockers, and finding lines include concrete PRD/label/dependency/section citations. The audit now traces PRD Studio load, issue #191's known-thin fixture, calibration, human answers, preview, approve-intent, stale/auth/readback failures, and unchanged mutation authority. Extracted category/render helpers and promoted the large fixture to a module constant for KISS. `PYTHONPATH=src python3 -m pytest tests/unit/test_ceo_review_calibration.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_answers.py -q` passed (35 tests); diff check passed. Checkpoint 4 revision 3: added a deterministic issue-191 known-thin privacy fixture proving the existing raw-private-transcript boundary stays supported rather than becoming a missing-evidence recommendation. Replaced partial suppression/citation special cases with a complete finding-code→question/evidence mapping shared by blocker suppression and rendered citations; unmapped findings now raise an attribution error. Added mapping coverage; focused calibration tests pass (9); diff check passes. Checkpoint 4 revision 4: missing-body now maps to every body-derived question; non-blocking warnings are also suppressed when their mapped question is already blocked. Answer citations are source-aware (body, labels, tracker/dependency state, Project fields) and the rendered citations section uses precise mapped contexts rather than circular finding IDs. Added empty-body disjointness and source-attribution coverage; calibration tests pass (11); diff check passes. Checkpoint 4 revision 4 returned `needs_human` from verifier. `F191-C4-002` remains after three bounded fixes plus the allowed researcher consult: `project_updates` is derived from the PRD body but currently labeled as active Project-field evidence, which can be unavailable. The verifier requires explicit operator authorization for one additional bounded correction (align citation with PRD-body derivation, suppress Project-field strength when unread, and add per-question/Project-unread/revise-reject CLI tests) or an explicit recorded deviation acceptance. Operator authorized one final bounded correction on 2026-07-14. Revision 5 aligns `project_updates` with its actual PRD-body derivation rather than active Project fields, adds unread-Project provenance coverage, and exercises approve/revise/reject calibrated CLI output and exit behavior. Focused calibration tests pass (12); diff check passes. Verifier approved checkpoint 4 revision 5 on 2026-07-14. CEO review calibration is complete; proceed to checkpoint 5 Completed Job Follow-Up.

## Checkpoint 5 — Completed Jobs Follow-Up

Implemented the completed-job follow-up flow without reopening or mutating the source implementation lifecycle.

- Completed Jobs now exposes **Follow-Up** and loads the existing AI Co-Worker surface for safe Issue drafting.
- The capture validates concise feedback, source type (`manual-qa`, `browser-qa`, `external-browser-qa`, `operator-note`, `reviewer-note`, or `other`), safe HTTPS references, completed job/group ID, and available source PRD/PR links. Feedback that appears to contain credentials is rejected; raw transcripts are never captured.
- The recommendation is advisory: narrow defect signals route to Issue, broader workflow/architecture signals route to PRD, and short feedback requires clarification. The operator selects and types an exact final-route confirmation.
- Issue confirmation consumes only the short-lived Term Control capture and opens the existing AI Co-Worker draft flow. The AI Co-Worker owns the server-held pending draft/session/project binding and requires its separate exact `create issue` confirmation for GitHub mutation. The Term Control endpoint does not create GitHub issues.
- PRD confirmation launches a new seeded `prd-planning` session with source context and an explicit instruction not to reopen the completed job. If launch/configuration is unavailable, it returns a copyable seed instead.

### Changed files (checkpoint 5)

- `pipeline-diagram/completed.html`
- `pipeline-diagram/coworker-launcher.js`
- `term-control-center/server/completedFollowUp.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/completedFollowUp.test.ts`
- `term-control-center/tests/completedStatic.test.ts`
- `term-control-center/tests/server.test.ts`
- `docs/implementation-quality-loop.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Validation (checkpoint 5)

- `npm --prefix term-control-center ci` — passed temporarily; `term-control-center/node_modules` removed after validation.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completedFollowUp.test.ts tests/completedStatic.test.ts` — passed (19 tests).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='completed-work Follow-Up confirms an Issue route without GitHub mutation' tests/server.test.ts` — passed (1 test); the endpoint test makes no GitHub request or mutation.
- `git diff --check` — passed.

### Skipped checks and risks

- Full Term Control suite, production build, browser/manual smoke, live GitHub issue creation, PR creation, merge, deployment, trading, and backtesting were not run; live GitHub mutation is forbidden for this checkpoint.
- The Issue path intentionally delegates final GitHub mutation to the existing AI Co-Worker server-held draft/create boundary. If that surface is unavailable, the Completed Jobs UI shows a copyable draft and reports that GitHub was not changed.
- The PRD planner launch is configuration-dependent; its failure path returns the seed and retains the source completed-job lifecycle unchanged.
- No standards exception, secret, raw transcript, GitHub mutation, PR/merge/deploy/trading/backtest action, or cleanup debt was introduced.

Request verifier checkpoint 5 review.

### Checkpoint 5 revision 2 — safe non-lossy Issue staging

Addressed the bounded Issue-path and capture-validation findings from `F191-C5-001`, `F191-C5-002`, and `F191-C5-004`.

- Added the AI Co-Worker's allowlisted `/coworker/issues/stage-followup` endpoint. It stages the validated Term Control title/body verbatim as a fresh, server-held pending draft in the current project/session; it does not invoke GitHub creation. The existing exact `create issue` endpoint remains the only mutation path.
- The completed-job UI now awaits the staging result. AI Co-Worker clears any stale pending draft ID before staging, applies a 10-second request timeout, requires a fresh pending ID, and validates canonical title/body/source readback before reporting success. Failure shows the copyable Term-generated draft and explicitly states GitHub was not changed.
- The staging contract preserves the full bounded feedback body and all completed-job, PRD, PR, source-type, and link context; a new 4,000-character feedback test proves it does not traverse the lossy free-text Issue Logger parser.
- Capture parsing now rejects invalid supplied source/route enums and missing real completed-row identity. The privacy guard rejects assignment-shaped credentials and raw terminal fences while allowing ordinary auth-related bug descriptions.

### Revision 2 changed files

- `src/agentops_harness/review_server.py`
- `tests/unit/test_completed_followup_issue_stage.py`
- `pipeline-diagram/coworker-launcher.js`
- `pipeline-diagram/completed.html`
- `term-control-center/server/completedFollowUp.ts`
- `term-control-center/tests/completedFollowUp.test.ts`
- `term-control-center/tests/completedStatic.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Revision 2 validation

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider tests/unit/test_completed_followup_issue_stage.py tests/unit/test_review_server_coworker.py -q` — passed (88 tests).
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completedFollowUp.test.ts tests/completedStatic.test.ts` — passed (19 tests).
- `git diff --check` — passed.

Remaining scope for verifier review: PRD source-project binding/route-level evidence, complete clarification retry UX, and KISS extraction remain under the active checkpoint revision if the verifier finds them blocking. No GitHub mutation occurred.

Request verifier checkpoint 5 revision 2 review.

## Checkpoint 5 revision 3 — extracted Follow-Up boundaries and fail-closed PRD binding

Addressed `F191-C5-001`, `F191-C5-003`, `F191-C5-004`, `F191-C5-005`, and `F191-C5-006` under recorded continuation authorization.

- Extracted browser Follow-Up orchestration to `pipeline-diagram/completed-followup.js`. The completed-page and AI Co-Worker files are thin adapters; the focused module owns deterministic recommendation/one-clarification flow, Issue fallback, PRD fallback, canonical staging readback, and the abortable 10-second staging request boundary.
- The capture now requires active project identity, treats a blank route as omitted, rejects role-labelled transcript forms, and supports one clarification retry. The PRD route compares captured repository and project identity to the configured authoring workspace before any launch; a mismatch returns a fail-closed error and retains the capture. Successful fresh planner launch consumes only the Follow-Up capture; launch fallback remains retryable and never touches the source completed group.
- Added `completedFollowUpRoutes.ts` for Follow-Up PRD HTTP orchestration, leaving `completedFollowUp.ts` as the pure capture/store/launch-payload domain module and `index.ts` as the thin registration/lifecycle adapter.
- AI Co-Worker staging now requires matching source repository and project, derives the existing canonical issue type/labels from the full staged body, and returns them for browser readback. The only GitHub mutation path remains the existing separately confirmed `create issue` route.
- Added deterministic browser tests for fresh/stale/missing/mismatched readback, timeout abort/timer cleanup, clarification retry, blank-route omission, and Issue/PRD fallback; route tests for confirmation, project/repository mismatch, launch/consume, fallback retention, and source-job preservation; and Python type/label/readback tests for narrow bug versus improvement.

### Research consult (2026-07-15)

Researcher inspected the local repository and recommended the minimal existing-style extraction: a browser global-IIFE beside `completion-center.js`, plus a Follow-Up-only route module modeled on `completionCloseoutRoutes.ts`, with generic lifecycle passed as a narrow callback. The implementation follows that evidence and adds no framework/dependency pattern.

### Revision 3 changed files

- `pipeline-diagram/completed.html`
- `pipeline-diagram/completed-followup.js`
- `pipeline-diagram/public/completed-followup.js`
- `pipeline-diagram/coworker-launcher.js`
- `term-control-center/server/completedFollowUp.ts`
- `term-control-center/server/completedFollowUpRoutes.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/completedFollowUp.test.ts`
- `term-control-center/tests/completedFollowUpBrowser.test.ts`
- `term-control-center/tests/completedFollowUpRoutes.test.ts`
- `term-control-center/tests/completedStatic.test.ts`
- `term-control-center/tests/server.test.ts`
- `src/agentops_harness/review_server.py`
- `tests/unit/test_completed_followup_issue_stage.py`
- `docs/implementation-quality-loop.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Revision 3 validation

- `npm --prefix term-control-center ci` — passed temporarily for validation.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completedFollowUp.test.ts tests/completedFollowUpRoutes.test.ts tests/completedFollowUpBrowser.test.ts tests/completedStatic.test.ts` — passed, 30 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='completed-work Follow-Up confirms an Issue route without GitHub mutation' tests/server.test.ts` — passed, 1 test.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider tests/unit/test_completed_followup_issue_stage.py tests/unit/test_review_server_coworker.py -q` — passed, 90 tests.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` — passed after syncing the new public symlink.
- `git diff --check` — passed.

### Skipped checks and risks

- Full Term Control suite, production build, manual browser smoke, live planner launch, and any live GitHub mutation were not run. An earlier broad `server.test.ts` run exceeded its 600-second limit and showed existing unrelated shared-state failures; the scoped Follow-Up integration test passed independently.
- No GitHub mutation, PR/merge/deploy, source-job reopen, approval, secret, raw transcript, trading, or backtesting occurred. The source completed-job lifecycle remains untouched by both launch and fallback paths.
- No standards exception or cleanup debt is known. `node_modules` will be removed after this handoff update.

Request verifier checkpoint 5 revision 3 review.

## Checkpoint 5 revision 4 — transcript validation and final Follow-Up KISS cleanup

Addressed the remaining `F191-C5-004` and `F191-C5-005` findings under recorded continuation authorization.

- `parseFollowUpCapture()` now checks the original feedback string for credential/fence/role-labelled transcript markers before cleanup can erase newline boundaries. It rejects `operator`, `assistant`, `user`, `system`, and `tool` role markers after any newline; only then does it strip non-printable characters for bounded storage.
- Moved pure AI Co-Worker Follow-Up draft sanitization, source binding, classification, and canonical label construction into `src/agentops_harness/followup_issue.py`. `review_server.py` is now the session/HTTP adapter only.
- Removed unused Follow-Up response fields: recommendation returns only ID/recommendation/rationale; confirmed Issue returns only status/route/capture/draft; PRD fallback returns only status/seed/error. Focused tests assert the trimmed contracts.

### Revision 4 changed files

- `term-control-center/server/completedFollowUp.ts`
- `term-control-center/server/completedFollowUpRoutes.ts`
- `term-control-center/server/index.ts`
- `term-control-center/tests/completedFollowUp.test.ts`
- `term-control-center/tests/completedFollowUpRoutes.test.ts`
- `term-control-center/tests/server.test.ts`
- `src/agentops_harness/followup_issue.py`
- `src/agentops_harness/review_server.py`
- `tests/unit/test_completed_followup_issue_stage.py`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-191-quality-loop/coder-handoff.md`

### Revision 4 validation

- `npm --prefix term-control-center ci` — passed temporarily for validation.
- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/completedFollowUp.test.ts tests/completedFollowUpRoutes.test.ts tests/completedFollowUpBrowser.test.ts tests/completedStatic.test.ts` — passed, 30 tests.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 --test-name-pattern='completed-work Follow-Up confirms an Issue route without GitHub mutation' tests/server.test.ts` — passed, 1 test.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -p no:cacheprovider tests/unit/test_completed_followup_issue_stage.py tests/unit/test_review_server_coworker.py -q` — passed, 91 tests.
- `python3 pipeline-diagram/deploy/sync-public-assets.py --check` and `git diff --check` — passed.

### Skipped checks and risks

- Full Term Control suite, production build, manual browser smoke, live planner launch, and any live GitHub mutation remain intentionally skipped. No source completed job, GitHub issue, PR, merge, deployment, approval, trading, or backtest was mutated.
- No standards exception or cleanup debt is known. `node_modules` will be removed after this handoff update.

Request verifier checkpoint 5 revision 4 review.

## Checkpoint 5 revision 5 — canonical redaction parity and final response cleanup

Addressed `F191-C5-007` and `F191-C5-008` under recorded continuation authorization.

- Term capture now rejects the canonical redactor's Authorization/Bearer, Cookie, identity-header, and sensitive private-path forms before data can enter the in-memory capture, Issue draft, or planner seed. Tests cover those synthetic forms and preserve ordinary auth-related bug prose.
- Extracted the terminal fenced-block replacement into the existing shared validation-redaction module. Both Co-Worker chat sanitization and Follow-Up staging call that helper, eliminating duplicate patterns.
- Removed the dead client recommendation-seed fallback branches; only the confirmed PRD route can return a copyable seed.

### Revision 5 validation

- `npm --prefix term-control-center ci` and `npm --prefix term-control-center run typecheck` — passed; dependencies removed afterward.
- Focused Node Follow-Up suites — passed, 30 tests.
- Focused server Issue-confirmation integration — passed, 1 test.
- Focused Python Follow-Up/Co-Worker suites — passed, 91 tests.
- Asset sync check and `git diff --check` — passed.

No GitHub mutation, source-job reopen, PR/merge/deploy, approval, trading, or backtesting occurred. Full suite/manual browser/live planner/live GitHub checks remain intentionally skipped.

Request verifier checkpoint 5 revision 5 review.

## Checkpoint 5 revision 6 — Follow-Up validate-and-preserve boundary

Addressed the remaining `F191-C5-007` contract conflict under recorded continuation authorization.

- Added a shared strong-sensitive detector for unambiguous Authorization/Bearer, Cookie, assignment, identity-header, private-path, GitHub-token, and terminal-block forms.
- Direct Python Follow-Up staging now rejects those forms rather than applying the ledger summary redactor. Accepted ordinary token-refresh/auth-bug prose is preserved byte-for-byte, keeping canonical browser title/body readback valid. The ledger's broader ambiguous-word redaction behavior remains unchanged for its existing summary consumers.
- Python tests prove safe auth-prose preservation and strong sensitive-input rejection; focused Follow-Up/Co-Worker tests pass (92).

No GitHub mutation, source-job lifecycle action, PR/merge/deploy, approval, trading, or backtesting occurred. `git diff --check` passes.

Request verifier checkpoint 5 revision 6 review.

## Checkpoint 5 approval

Verifier approved checkpoint 5 revision 6 on 2026-07-15. Completed Job Follow-Up is approved through safe capture, staging, source binding, canonical readback, and fallback boundaries. The required Steward review returned `cleanup_recommended` only for generated artifacts; removed `.pytest_cache/`, both identified Python `__pycache__/` directories, and `term-control-center/build/`. Steward found placement, module boundaries, public asset symlink, run artifacts, and secret/transcript hygiene clean. `git diff --check` passes. Final bug-check revision 1 found F191-FINAL-001 through 004. Addressed: restored draft seed/link/retirement lifecycle in shared workspace launches; phase-1 Context Brief now requires an inspectable worktree and applies runtime isolation without provisioning/sync; explicit project ID now binds receipt, Machine Status, prompt, parser, and discovery; extracted Context Brief transition and added retry/block/failed-phase-two coverage. Focused draft lifecycle server tests (5), receipt/discovery/prompt tests (20), context-brief tests (5), typecheck, and diff check pass. Dependencies/build artifacts removed. Requesting final verifier bug-check revision 2.
