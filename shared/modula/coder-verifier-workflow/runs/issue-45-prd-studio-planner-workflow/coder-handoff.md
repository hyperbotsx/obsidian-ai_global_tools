# Coder Handoff — PRD #45 PRD Studio Planner Workflow

## Checkpoint

- Checkpoint: 1 — Planner entry checkpoint
- Revision: 1
- Status: verifier approved
- PRD: https://github.com/hyperbotsx/agentops-harness/issues/45
- Branch: `prd/prd-studio-planner-led-authoring-quality-review-approval-45`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Preflight

- Git status before editing: clean on `prd/prd-studio-planner-led-authoring-quality-review-approval-45...origin/main`.
- Canonical issue #45 status checked with `gh issue view`: open with labels `type:prd`, `agent:agentops`, `status:approved`.
- Branch suffix check: current branch ends in `-45`.
- Pre-existing dirty files: none.

## Scope controls

- Allowed paths touched for this checkpoint:
  - `pipeline-diagram/board.html`
  - `scripts/agentops/pi-agent.sh`
  - `term-control-center/server/index.ts`
  - `term-control-center/server/launchPlan.ts`
  - `term-control-center/shared/launcher.ts`
  - `term-control-center/shared/protocol.ts`
  - `term-control-center/src/App.tsx`
  - `term-control-center/src/TerminalPane.tsx`
  - focused Term Control Center tests
- Forbidden paths/actions observed:
  - no product implementation outside PRD Studio/Term Control launch surfaces
  - no project-local skills
  - no GitHub issue creation or approval mutation
  - no PR creation, merge, deploy, trading, or backtest
- Stop condition: stop after verifier approval for Planner entry checkpoint before moving to planning brief / execute-gate work.

## Research freshness consult

Mandatory PRD #45 research-first consult completed with Researcher before code edits.

Researcher summary:
- Current Create PRD board flow immediately launches `prd-author + researcher + codebase-expert` via `mode: 'prd-authoring'`.
- Current launch roles and protocol lacked `planner`.
- `/launch` validates requests, overlays configured authoring workspace, and starts every pane immediately.
- Term UI already renders a single attached pane full-size when only one pane exists.
- Recommended implementation: add a Planner-only launch state and keep existing downstream `prd-authoring` behind a future explicit execute gate.

## Changes made

- Added `planner` as an allowlisted Term Control / pi-agent role.
- Added `prd-planning` launch mode with planner-only validation/default panes.
- Mapped planner wrapper role to the existing global `project-prd-author` skill to avoid project-local skills.
- Added Planner task prompt that limits the role to one-to-one PRD intake and forbids downstream launch / GitHub mutation / approval / PR / merge / deploy actions.
- Updated Create PRD board flow to open `PRD Studio Planner` first using `mode: 'prd-planning'` and a single planner pane.
- Kept existing downstream `prd-authoring` cohort configuration present but hidden behind the gate.
- Updated embedded Term app profile/protocol types to accept planner attachments while keeping Planner out of multi-peer pair/trio layout logic, so planner-only groups render as one full-pane terminal.
- Added focused tests for planner launch validation, wrapper allowlist, server launch, board behavior, protocol parsing, and full-pane layout guard.

## Validation

- `npm --prefix term-control-center run test` — passed, 173 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_preflight.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py` — passed, 69 tests.
- `git diff --check` — passed.

## Changed files

- `pipeline-diagram/board.html`
- `scripts/agentops/pi-agent.sh`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/protocol.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/src/TerminalPane.tsx`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/protocol.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-45-prd-studio-planner-workflow/coder-handoff.md`

## Verifier result

- Checkpoint 1 revision 1 approved by verifier.
- Open findings: 0.
- Bug-check status: not applicable for this checkpoint.
- Verdict report path: `dev-plans/agentops/coder-verifier-workflow/runs/issue-45-prd-studio-planner-workflow/verifier-report.md`.

## Checkpoint 2 — Planning brief schema

- Revision: 1
- Status: verifier approved
- Scope: add a versioned planning brief schema/template/validator and make Planner launch prompts require the artifact.

### Changes made

- Added `src/agentops_harness/prd_studio_artifacts.py` with `planning-brief.v1`, required fields, a template, and validation.
- Required planning brief fields now cover refined idea, problem, scope, goals, non-goals, assumptions, risks, unresolved questions, domain/effort classification, agent routing, recommended agents, per-agent prompts, expected artifacts, validation strategy, stop conditions, and operator decisions.
- Updated Planner launch prompt to name `planning-brief.v1`, list required fields, and point Planner at the session artifact file `planning-brief.json` next to `task-context.md`.
- Threaded Term Control launch context path into role prompt construction without exposing command internals in API responses.
- Added focused tests for planning brief validation/template, Planner prompt schema/artifact path, and existing Planner launch behavior.

### Verifier revision

- `V-CP2-001` found malformed scalar planning brief fields could pass validation.
- Fixed by validating every scalar text field as a string and adding a regression test for malformed `problem`, `scope`, and `validation_strategy`.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py` — passed, 5 tests after `V-CP2-001` fix.
- `npm --prefix term-control-center run test -- --test-name-pattern="Planner|planning|launch plan|protocol|launcher"` — passed; due shell pattern expansion this ran the full Term Control suite, 174 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_studio_artifacts.py` — passed, 28 tests.
- `git diff --check` — passed.

### Additional changed files

- `src/agentops_harness/prd_studio_artifacts.py`
- `tests/unit/test_prd_studio_artifacts.py`
- `term-control-center/tests/launchPlan.test.ts`

### Verifier result

- Checkpoint 2 revision 2 approved by verifier.
- `V-CP2-001` closed.
- Open findings: 0.

## Checkpoint 3 — Execute gate

- Revision: 1
- Status: verifier approved
- Scope: add explicit downstream authoring execution gate; ambiguous praise must not launch downstream agents.

### Changes made

- Added shared `EXPLICIT_PRD_EXECUTE_PHRASE` / `isExplicitPrdExecute()` helper; only exact `execute this plan` (case/space normalized) is accepted.
- Added guarded Term Control endpoint `POST /groups/:id/execute-authoring`.
- Endpoint only accepts existing `prd-planning` groups, rejects non-planning groups, and rejects ambiguous confirmations such as `looks good`.
- Endpoint launches the existing downstream `prd-authoring` cohort after exact confirmation and avoids reusing planner groups as downstream authoring groups by making group reuse mode-aware.
- Added PRD Studio UI action visible only on live Planner groups; it prompts for the exact phrase and posts to the execute endpoint.
- Added tests for shared phrase parsing, server-side ambiguous rejection / exact acceptance, and board execute-gate wiring.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="execute gate|execute|Planner|planning|server|launcher"` — passed; due shell pattern expansion this ran the full Term Control suite, 177 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_author.py` — passed, 29 tests.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 3 revision 1 approved by verifier.
- Open findings: 0.

## Checkpoint 4 — Domain routing and Frontend Expert

- Revision: 2
- Status: verifier approved
- Scope: add frontend-domain routing for downstream PRD authoring and Frontend Expert role.

### Changes made

- Added `frontend-expert` role to Term Control launch/profile/protocol surfaces and `pi-agent.sh` allowlist.
- Mapped `frontend-expert` to the existing global `frontend-skill` markdown in the shared skills vault; no project-local skill was created.
- Added authoring-domain routing so frontend/browser-visible PRD authoring defaults to `prd-author`, `researcher`, `codebase-expert`, and `frontend-expert`.
- Non-frontend/backend-only PRD authoring remains baseline and skips Frontend Expert.
- Added Frontend Expert prompt covering user journey, visual hierarchy, interaction states, accessibility, responsiveness, component reuse, preview/manual QA, loading, empty, and error states.
- Updated PRD Studio board setup to expose Frontend Expert and include it for frontend authoring payloads.
- Added tests for frontend inclusion, non-frontend exclusion, Frontend Expert prompt, protocol parsing, wrapper allowlist, and execute downstream inclusion.

### Verifier revision

- `V-CP4-001` found preview-URL-only authoring could skip Frontend Expert.
- Fixed shared server-side Frontend Expert routing to treat `previewUrl` as browser-visible unless skip hints are present.
- Added regression coverage for preview-url-only PRD authoring including Frontend Expert.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="preview-url-only|frontend|Frontend|launcher"` — passed; due shell pattern expansion this ran the full Term Control suite, 183 tests passed.
- `npm --prefix term-control-center run test -- --test-name-pattern="frontend|Frontend|domain|authoring|execute|launcher|protocol"` — passed; due shell pattern expansion this ran the full Term Control suite, 182 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_studio_artifacts.py` — passed, 29 tests.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 4 revision 2 approved by verifier.
- `V-CP4-001` closed.
- Open findings: 0.

## Checkpoint 5 — PRD quality controls

- Revision: 2
- Status: verifier approved
- Scope: add lightweight artifact schemas and checks for quality rubric, evidence matrix, requirements smells, synthesis notes, and open-question surfacing.

### Changes made

- Extended `prd_studio_artifacts.py` with versioned schemas/templates/validators for:
  - `quality-rubric.v1`
  - `evidence-matrix.v1`
  - `requirements-smells.v1`
  - `synthesis-notes.v1`
- Added validation for rubric criteria/status/rationale/blocker/fix fields, evidence item fields, smell item fields/severity, and synthesis notes fields.
- Added requirements smell detection for vague terms, unresolved TBD/TBR/TODO, compound requirements, and passive voice.
- Updated PRD Author launch prompt to require `quality-rubric.json`, `evidence-matrix.json`, and `requirements-smells.json` artifacts and to surface blocker failures, weak evidence, high-severity smells, and unresolved open questions before final draft confirmation.
- Added focused tests for rubric validation, evidence matrix required fields, smell detector output, invalid rubric statuses, invalid smell severities, and PRD Author quality artifact prompt wiring.

### Revision 2 fix for `V-CP5-001`

- Made `synthesis_notes_template()` include all schema-required top-level fields.
- Tightened `validate_synthesis_notes()` to reject missing required synthesis fields and wrong list/text types.
- Tightened row validators to reject malformed scalar/boolean field types in quality rubric, evidence matrix, and requirements smell rows.
- Added regression tests for valid synthesis template, missing synthesis fields, and malformed row types.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py` — passed, 13 tests.
- `npm --prefix term-control-center run test -- --test-name-pattern="quality|evidence|smell|PRD Author|Frontend|launcher"` — passed; due shell pattern expansion this ran the full Term Control suite, 184 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_studio_artifacts.py` — passed, 34 tests.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py` — passed, 13 tests.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 5 revision 2 approved by verifier.
- `V-CP5-001` closed.
- Open findings: 0.

## Checkpoint 6 — Observability pagination

- Revision: 2
- Status: verifier approved
- Scope: page downstream PRD authoring agents so every active agent remains inspectable while no desktop/iPad-landscape page shows more than two terminals.

### Changes made

- Changed PRD authoring workspaces to use pair navigation instead of a three-pane desktop view.
- Added authoring pages:
  - `PRD Author + Researcher`
  - `Codebase Expert` or `Codebase Expert + Frontend Expert` when frontend routing is active.
- Kept phone/narrow layouts on the existing one-pane role switcher behavior.
- Preserved hidden-session behavior by keeping all panes mounted and hiding inactive pages through the existing `hidden={!visible.has(pane.id)}` focus-slot path.
- Removed the unused three-pane CSS grid mode.
- Updated layout guardrail tests to assert authoring pagination, no `terminal-grid-trio`, mobile single-pane switching, full-screen Planner before execute, and Browser QA pager behavior.

### Revision 2 fix for `V-CP6-001`

- Expanded the one-pane responsive query to include coarse-pointer portrait layouts: `(max-width: 760px), (pointer: coarse) and (orientation: portrait)`.
- This keeps desktop and tablet landscape pair pages while routing iPad/tablet portrait through the existing one-pane role switcher.
- Updated layout tests to assert tablet portrait coverage, not only phone width.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="authoring workspace|browser QA workspace|planner workspace|mobile view"` — passed; due shell pattern expansion this ran the full Term Control suite, 184 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_author.py` — passed, 37 tests.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `npm --prefix term-control-center run test -- --test-name-pattern="mobile view|authoring workspace|planner workspace"` — passed; due shell pattern expansion this ran the full Term Control suite, 184 tests passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 6 revision 2 approved by verifier.
- `V-CP6-001` closed.
- Open findings: 0.

## Checkpoint 7 — Optional multi-model review

- Revision: 2
- Status: verifier approved
- Scope: add opt-in bounded multi-model review and synthesis launch support without enabling GitHub mutation or approval authority.

### Changes made

- Added `multiModelReview: "bounded"` as an opt-in PRD authoring launch option; default remains off and compact/non-authoring modes fail closed.
- Added `model-reviewer` and `synthesizer` roles across launcher validation, protocol parsing, terminal pane/profile typing, launch wrapper allowlist, and PRD authoring pager layout.
- Default bounded multi-model authoring appends `model-reviewer` and `synthesizer` after the baseline PRD Author/Researcher/Codebase Expert cohort and optional Frontend Expert.
- Added role prompts:
  - Multi-Model Reviewer: independent bounded critic; structured output covering agreements, disagreements, missing requirements, risks, and recommended changes; no competing final PRD, GitHub mutation, approval, PR, merge, deploy, trading, or backtest.
  - PRD Synthesizer: reconciles authoring/research/codebase/frontend/reviewer outputs, maintains `synthesis-notes.json` with `synthesis-notes.v1`, and has no mutation/approval authority.
- Mapped wrapper skills without project-local copies: `model-reviewer` uses the global Researcher skill and `synthesizer` uses the global PRD Author skill, with role-specific launch prompts doing the scoping.
- Added tests for opt-in/default-off validation, fail-closed invalid modes, role parsing, launch prompts, wrapper allowlist, and review/synthesis pager visibility.

### Revision 2 fix for `V-CP7-001`

- Added explicit `--name "$role"` to `scripts/agentops/pi-agent.sh` so reused global skill files do not override the requested `model-reviewer` / `synthesizer` peer identities.
- Added regression coverage that the wrapper carries the explicit role identity override.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="multi-model|Multi-model|model-reviewer|authoring workspace|protocol|launcher|launch prompt"` — passed; due shell pattern expansion this ran the full Term Control suite, 188 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_author.py` — passed, 37 tests.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `npm --prefix term-control-center run test -- --test-name-pattern="multi-model|pi-agent wrapper|Multi-model"` — passed; due shell pattern expansion this ran the full Term Control suite, 188 tests passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 7 revision 2 approved by verifier.
- `V-CP7-001` closed.
- Open findings: 0.

## Checkpoint 8 — Final PRD draft confirmation

- Revision: 2
- Status: verifier approved
- Scope: ensure final PRD issue planning presents the final draft and requires explicit final confirmation before any GitHub issue creation mutation.

### Changes made

- Added `FINAL_CREATE_CONFIRMATION = "create GitHub draft issue"` to the GitHub issue planning module.
- Inserted non-mutating issue-plan steps before create mutations:
  - `present final PRD draft`
  - `require final creation confirmation`
- Kept actual issue creation/project/body/field steps marked mutating and sequenced after the non-mutating final-draft/confirmation steps.
- Updated PRD Author launch prompt to require presenting the final PRD draft to the operator and requiring exact final creation confirmation before any GitHub issue creation.
- Added regression tests for the issue-plan step ordering/mutation flags and PRD Author prompt copy.

### Revision 2 fix for `V-CP8-001`

- Moved the final confirmation guard to the live PRD creation mutation helper.
- `create_prd_issue()` now requires the exact `create GitHub draft issue` confirmation phrase and a matching SHA-256 state digest bound to repository, title, labels, owner label, and final draft body before `gh issue create` can run.
- Exposed `prd_creation_state_digest()` for the review server to issue a final-draft state token.
- Updated `/prd/plan` to return `final_confirmation` and `state_digest`; updated `/prd/create` to reject generic boolean confirmation and require the exact phrase before calling the mutation helper.
- Added focused tests proving missing/wrong confirmation does not call `gh`, digest mismatch blocks, and matching confirmation/digest reaches issue creation.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py` — passed, 34 tests.
- `npm --prefix term-control-center run test -- --test-name-pattern="final PRD|PRD Author launch prompt"` — passed; due shell pattern expansion this ran the full Term Control suite, 188 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed; existing Vite warnings only:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author_github.py tests/unit/test_prd_author.py tests/unit/test_prd_studio_artifacts.py` — passed, 47 tests.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `PYTHONPATH=src pytest tests/unit/test_prd_create.py tests/unit/test_prd_author_github.py` — passed, 13 tests.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 8 revision 2 approved by verifier.
- `V-CP8-001` closed.
- Open findings: 0.

## Checkpoint 9 — Inter-agent coms

- Revision: 1
- Status: verifier approved
- Scope: make PRD authoring peer requests explicitly use the existing local pi-coms pool, fail closed on missing peers, and prefer artifact references for large context.

### Changes made

- Added shared PRD authoring coms guard copy to authoring launch prompts.
- PRD Author, Researcher in authoring mode, Codebase Expert, Frontend Expert, Multi-Model Reviewer, and Synthesizer prompts now require:
  - use existing local pi-coms pool;
  - run `coms_list` before outbound authoring requests;
  - fail closed with `needs_human` if the target role is not live in the current worktree pool;
  - pass large PRD context by artifact path instead of unbounded inline text.
- Updated the coms transport contract to include optional authoring peers (`frontend-expert`, `model-reviewer`, `synthesizer`) and the same fail-closed / artifact-reference rules.
- Added tests for PRD Author prompt guard copy and the updated authoring coms contract.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="peer coms|PRD Author launch prompt|Multi-model"` — passed; due shell pattern expansion this ran the full Term Control suite, 188 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 9 revision 1 approved by verifier.
- Open findings: 0.

## Checkpoint 10 — Workspace/branch ownership

- Revision: 2
- Status: verifier approved
- Scope: reinforce that PRD authoring peers share one authoring workspace/coms pool and cannot configure per-agent implementation worktrees or branches.

### Changes made

- Added launch-request validation that rejects pane-level `worktreePath` or `workingBranch` overrides.
- Added PRD authoring prompt copy stating all authoring peers share one workspace, branch, and local coms pool and must not create per-agent implementation branches or product worktrees.
- Kept implementation launch preflight tied to the single task-level worktree and branch through the existing `assertWorktree()` path.
- Added tests for per-pane worktree/branch rejection and PRD Author prompt ownership guidance.

### Revision 2 fix for `V-CP10-001`

- Added implementation-mode validation requiring canonical implementation branches to end with the task issue number, e.g. `-45` for PRD #45.
- Kept pre-issue PRD planning/authoring draft sessions exempt because they use draft IDs rather than approved PRD numbers.
- Added regression coverage that issue 1019 rejects `feature/no-number` and accepts `prd/owned-1019`.

### Validation

- `npm --prefix term-control-center run test -- --test-name-pattern="per-agent|PRD Author launch prompt|workspace|branch"` — passed; due shell pattern expansion this ran the full Term Control suite, 189 tests passed.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `npm --prefix term-control-center run test -- --test-name-pattern="PRD-numbered|per-agent"` — passed; due shell pattern expansion this ran the full Term Control suite, 190 tests passed.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 10 revision 2 approved by verifier.
- `V-CP10-001` closed.
- Open findings: 0.

## Checkpoint 11 — Approval Review integration

- Revision: 2
- Status: verifier approved
- Scope: add a structured PRD Studio Approval Review packet and safe post-creation transition prompt without treating review start as approval.

### Changes made

- Added `prd_studio_approval.py` with:
  - post-creation Approval Review prompt;
  - structured approval packet fields for summary, approved scope, excluded scope, owner/worktree/branch, dependencies, quality rubric, evidence gaps, disagreements, blocking questions, follow-ups, mutation preview, and approve/revise/reject options;
  - fail-closed loaded-issue-state checks;
  - mutation preview that only names `CEO Approved=Yes` when that live project field is present, otherwise uses canonical issue body/labels while leaving Project `Status=Todo`.
- Added `/prd/approval-review` review-server route returning the structured packet.
- Added post-create `approval_review_prompt` to successful `/prd/create` responses; prompt starts review only and does not approve.
- Added unit tests for prompt wording, missing issue-state blocking, live-field-aware mutation preview, and structured decision options.

### Revision 2 fix for `V-CP11-001`

- Approval packets now fail closed until both loaded issue state and loaded Project/profile metadata are present.
- Blocked packets now omit actionable approve/revise/reject options and mutation preview items.
- Ready packets expose decision options and mutation preview only after required live state is present.
- Added regression coverage for missing Project/profile metadata and blocked packets with no actionable options/preview.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_prd_studio_approval.py` — passed, 5 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.
- Revision 2 focused validation:
  - `PYTHONPATH=src pytest tests/unit/test_prd_studio_approval.py` — passed, 5 tests.
  - `npm --prefix term-control-center run typecheck` — passed.
  - `git diff --check` — passed.

### Verifier result

- Checkpoint 11 revision 2 approved by verifier.
- `V-CP11-001` closed.
- Open findings: 0.

## Checkpoint 12 — Regression validation

- Revision: 1
- Status: verifier approved
- Scope: confirm existing PRD creation, CEO Review entrypoints, issue creation, Project 3 tracking-adjacent tests, and Term Control launch behavior still pass with PRD Studio changes.

### Validation

- `npm --prefix term-control-center run test` — passed, 190 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed with existing Vite warnings:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_author_github.py tests/unit/test_prd_create.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_prd_studio_approval.py` — passed, 85 tests.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 12 revision 1 approved by verifier.
- Open findings: 0.

## Final review revision finding

- Final implementation review revision 1 requested revision for `V-FINAL-001`.
- Remaining scoped gates identified by verifier:
  - profile/project hardening for Approval Review and CEO Review against active AgentOps profile and live Project metadata;
  - artifact gate enforcement before final GitHub creation and Approval Review approval options.

## Checkpoint 13 — Profile/project hardening

- Revision: 3
- Status: verifier approved
- Scope: remove stale Project 2 / tracker assumptions from active CEO/Approval Review surfaces and use active AgentOps profile metadata for CEO apply project/repo writes.

### Changes made

- Updated `ceo_review.py` review questions, source-read labels, and missing tracker checks to reference active Project fields and generic tracker metadata instead of Project 2 / tracker `#862`.
- Updated `ceo_review_evonome_apply.py` to resolve repository, Project owner, and Project number from the active AgentOps profile via `prd_author_github.issue_profile()` instead of hardcoded repo/project constants.
- Updated CEO approval board copy in `pipeline-diagram/board.html` to refer to active Project fields instead of Project 2.
- Updated CEO review test expectation for generic `github_project_fields` source reads.

### Revision 2 fix for `V-CP13-001`

- Updated `ceo_review_answers.py` so approval packages derive project mutation plans from loaded live Project metadata.
- Project 3-style items with only `Status` now plan canonical issue body/label approval and explicitly leave Project `Status=Todo`; they do not emit nonexistent approval fields.
- Optional approval fields such as `CEO Approved=Yes` and `CEO Approved At=<approval date>` are included only when live project metadata exposes those fields/options.
- Updated `ceo_review_evonome_apply.py` so `_resolve_project_writes()` skips absent approval/project fields instead of raising for Project 3 status-only metadata.
- Added regression tests for Project 3 status-only fallback and optional approval-field-present behavior in approval package and apply-write planning.
- Removed stale tracker-specific fixture values from CEO review tests.

### Revision 3 fix for `V-CP13-001` after human authorization

- Updated the legacy `ceo_review_mutations.production_gh_mutation_sink()` path so informational non-mutating Project entries are skipped rather than treated as required GraphQL writes.
- Project 3 status-only metadata now executes canonical issue body/label approval through the legacy sink without attempting nonexistent Project writes.
- Updated `test_live_shaped_project_items_use_issue_labels_without_project_writes` to assert the legacy execute path succeeds and emits issue edit/comment calls with no `gh project item-edit` calls.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_evonome_apply.py -q` — passed, 38 tests.
- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_studio_approval.py tests/unit/test_prd_create.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_evonome_apply.py -q` — passed, 72 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.
- Static search: `rg "Project 2|#862|github_project_2_fields|PROJECT_NUMBER|PROJECT_OWNER|REPO =" src/agentops_harness/ceo_review.py src/agentops_harness/ceo_review_evonome_apply.py pipeline-diagram/board.html -n` — no matches.
- Revision 2 static search: `rg "#862|Project 2|github_project_2_fields|PROJECT_NUMBER|PROJECT_OWNER|REPO =|Pipeline Status=Approved|PRD Review Status=Approved|unrelated Project 2" src/agentops_harness/ceo_review.py src/agentops_harness/ceo_review_evonome_apply.py src/agentops_harness/ceo_review_answers.py pipeline-diagram/board.html tests/unit/test_ceo_review*.py -n` — only legacy optional-field fixture strings remain in `test_ceo_review_apply.py` and negative assertions for `Project 2` remain in `test_ceo_review_answers.py`.

### Verifier result

- Checkpoint 13 revision 3 approved by verifier.
- `V-CP13-001` closed.
- Open findings: 0.

## Checkpoint 14 — Artifact gate enforcement

- Revision: 1
- Status: verifier approved
- Scope: fail closed before final GitHub draft creation and Approval Review approval options when required PRD Studio artifacts are missing, schema-invalid, or have blocker-level findings.

### Changes made

- Added `validate_prd_studio_artifact_gate()` to require planning brief, evidence matrix, quality rubric, requirements smells, and synthesis notes artifacts.
- Artifact gate validates schemas and blocks on blocker-level conditions:
  - quality rubric `blocker=true` or `status=fail`;
  - evidence gap status in open/missing/blocked/gap/follow-up values;
  - unresolved high-severity requirement smells;
  - unresolved synthesis assumptions.
- `create_prd_issue()` now requires the artifact gate after exact final confirmation and matching digest but before `gh issue create`.
- `/prd/create` forwards artifact bundles to the creation gate.
- `build_approval_packet()` now requires the artifact gate before exposing decision options or mutation preview.
- `/prd/approval-review` forwards artifact bundles to the approval gate.
- Added regression tests for missing artifacts, blocker artifacts, successful artifact gates, create blocked before GitHub mutation, and Approval Review blocked with no actions/preview.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_studio_approval.py tests/unit/test_prd_create.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_evonome_apply.py -q` — passed, 72 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 14 revision 1 approved by verifier.
- Open findings: 0.

## Checkpoint 15 — Milestone checkpoint

- Revision: 1
- Status: verifier approved
- Scope: confirm every PRD #45 milestone/checkpoint has bounded scope, validation evidence, durable handoff entries, and verifier signoff before moving to final implementation review/bug-check.

### Changes made

- Added `milestone-ledger.json` summarizing approved checkpoints 1–14, closed findings, open finding count, and validation evidence.
- Updated this handoff with checkpoint 15 status and full validation evidence.
- No product code changes were needed for checkpoint 15.

### Validation

- `npm --prefix term-control-center run test` — passed, 190 tests.
- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center run build` — passed with existing Vite warnings:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_author_github.py tests/unit/test_prd_create.py tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_studio_approval.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_evonome_apply.py` — passed, 106 tests.
- `git diff --check` — passed.

### Verifier result

- Checkpoint 15 revision 1 approved by verifier.
- Open findings: 0.

## Final bug-check fix — `V-BUG-001`

- Revision: 1
- Status: verifier approved; final bug-check passed
- Scope: prevent CEO Review from becoming applyable when GitHub Project metadata is unavailable through REST fallback.

### Changes made

- Updated `ceo_review.py` source-state checks to distinguish loaded Project metadata from degraded REST fallback / empty unread Project metadata.
- `degraded_rest: true`, missing `projectItems`, and empty `projectItems` now produce `project_fields_unread` blockers.
- Real Project 3 status-only metadata remains allowed when a loaded project item contains live `status` data.
- Added regression tests for:
  - REST fallback with empty project items blocks approval readiness;
  - empty unread project items block approval readiness;
  - loaded status-only Project 3 metadata remains ready;
  - degraded REST state blocks answer final-confirmation status.

### Validation

- `PYTHONPATH=src pytest tests/unit/test_ceo_review.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_apply.py -q` — passed, 48 tests.
- `PYTHONPATH=src pytest tests/unit/test_prd_author.py tests/unit/test_prd_author_github.py tests/unit/test_prd_create.py tests/unit/test_prd_studio_artifacts.py tests/unit/test_prd_studio_approval.py tests/unit/test_ceo_review.py tests/unit/test_ceo_review_apply.py tests/unit/test_ceo_review_answers.py tests/unit/test_ceo_review_evonome_apply.py -q` — passed, 110 tests.
- `npm --prefix term-control-center run test` — passed, 190 tests.
- `npm --prefix term-control-center run build` — passed with existing Vite warnings:
  - `<script src="./term-config.js">` cannot be bundled without `type="module"`.
  - chunk larger than 500 kB.
- `git diff --check` — passed.

### Verifier result

- Final implementation approval revision 3 approved by verifier.
- Final bug-check status: passed.
- `V-BUG-001` closed.
- Open findings: 0.
