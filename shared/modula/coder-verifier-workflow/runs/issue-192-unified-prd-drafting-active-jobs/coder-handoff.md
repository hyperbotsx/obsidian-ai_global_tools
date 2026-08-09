# Issue #192 coder handoff

## Scope / source
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/192
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-192`
- Branch: `prd/unified-prd-drafting-active-jobs-192`
- Pre-edit status: clean (`git status --short --branch` showed no dirty files).
- Memory: disabled/advisory only per launch prompt.

## Allowed paths
- Expected product scope: `term-control-center/server/**`, `term-control-center/shared/**`, `term-control-center/src/**`, `pipeline-diagram/board.html`, focused tests under `term-control-center/tests/**`, and scoped docs/artifacts under this run folder.
- Run artifacts: `dev-plans/agentops/coder-verifier-workflow/runs/issue-192-unified-prd-drafting-active-jobs/**`.

## Forbidden / guarded paths and actions
- No PR creation, merge, deploy, sync main, trading, paper trading, live trading, or backtesting.
- No autonomous PRD approval or implementation launch authority changes.
- Do not store raw terminal transcripts, raw prompts, secrets, credentials, attach tokens, environment dumps, private account data, or unredacted browser state.
- Do not kill unrelated draft/authoring/review jobs.
- Do not reintroduce retired Planner phase after downstream authoring starts.

## Verifier checkpoints
1. Current-state audit and lifecycle design.
2. Draft job sidebar visibility.
3. Planner-to-authoring transition.
4. Parallel draft isolation.
5. CEO review handoff and close.
6. Steward review, final validation, final verifier bug-check.

## Researcher consults
- Consult 1 complete: current Term Control `/groups`, `/launch`, session store, tmux supervisor, and active jobs sidebar behavior. Summary recorded in `current-state-design.md`.
- Consult 2 complete: current `prd-planning` → `prd-authoring` and `execute-authoring` flow. Summary recorded in `current-state-design.md`.
- Consult 3 complete: current CEO / Approval Review launch and close/end behavior. Summary recorded in `current-state-design.md`.
- Consult 4 complete: browser localStorage/refresh recovery for session groups. Key constraints: no plaintext attach tokens in new server storage; logical rows must not reuse role-based tokens across phase replacement; seed-only jobs cannot rely on `sessionStore` because groups without sessions are not persisted.

## Changed files
- `pipeline-diagram/board.html`
- `scripts/agentops/pi-agent.sh`
- `term-control-center/server/draftComs.ts`
- `term-control-center/server/draftJobs.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/tests/agentopsComsLabel.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/terminalJobSidebar.test.ts`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-192-unified-prd-drafting-active-jobs/current-state-design.md`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-192-unified-prd-drafting-active-jobs/coder-handoff.md`

## Implementation summary
- Wrote current-state audit and minimal lifecycle design artifact for Checkpoint 1.
- Added a safe draft job store and logical `/groups` summaries keyed by existing `draftId`, with `draftJob` phase metadata and sanitized task fields.
- Draft planning/authoring physical groups now use the draft id as stable group seed, so the active jobs row remains one logical row across Planner and downstream authoring.
- Board `+` flow now reserves a seed draft job and can reopen seed drafts from the session list; React active jobs labels draft phases for attachable draft phases.
- Revision 4 keeps seed-only draft rows out of the React Term active jobs sidebar until a supported seed/setup route exists, avoiding dead rows while preserving board seed reopen behavior.
- Added draft-scoped coms isolation: launch env supplies `PI_AGENT_COMS_PROJECT`/`PI_AGENT_COMS_DIR`, and `pi-agent.sh` honors those overrides for same-draft PRD planning/authoring peers.
- Planner-to-authoring transition now attaches `planningBriefPath` to the downstream authoring task/prompt/context and uses a per-draft transition lock to prevent concurrent duplicate downstream launches.
- Authoring startup now happens before planner retirement; if authoring launch fails, the planner group remains available and retryable.
- Unsafe draft IDs are rejected before they can become physical group/path/tmux identifiers; allowed characters are constrained to tmux/path-safe `[A-Za-z0-9_-]`.
- Parallel draft rows now remain distinct in `/groups`, and draft-scoped coms projects/dirs differ per draft ID.
- Added draft-authoring-to-CEO-review handoff endpoint `/groups/:id/launch-ceo-review`; successful launch retires/deletes the draft job after the review group starts.
- Board Term live modal exposes a `Launch CEO review` action for PRD Authoring sessions; it posts the created PRD issue metadata, removes the retired draft row from the local cache, remembers the returned review group, and opens/focuses that CEO review group.
- CEO review prompt now asks the operator before closeout and posts `/approval-review/closeout` only after affirmative close confirmation.
- Final bug-check fixes: CEO handoff now rejects non-draft authoring groups, draft-scoped coms names include a stable hash for long-ID uniqueness, and draft jobs can record safe created PRD issue metadata for later handoff/defaults.
- Planner launches clear stale planning briefs for stable draft ids to avoid cross-run artifact reuse.
- Revision 2 adds draft-scoped coms isolation design: `comsProject`/`comsDir` safe metadata, launch env overrides for PRD planning/authoring, `pi-agent.sh` override behavior, fail-closed peer discovery, and focused tests.

## Validation so far
- `git status --short --branch` before editing: clean.
- `npm --prefix term-control-center ci` — passed; installed local dependencies for validation.
- `cd term-control-center && node --import tsx --test --test-name-pattern "logical draft job row|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts` — passed (4 tests).
- `cd term-control-center && node --import tsx --test --test-name-pattern "logical draft job row|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts && git diff --check` — passed (5 tests plus diff check).
- `cd term-control-center && node --import tsx --test --test-name-pattern "logical draft job row|authoring launch failure|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts|unsafe pre-issue" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts tests/launcher.test.ts && git diff --check` — passed (7 tests plus diff check).
- `cd term-control-center && node --import tsx --test --test-name-pattern "parallel PRD authoring drafts|parallel draft PRD Studio|logical draft job row|authoring launch failure|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts|unsafe pre-issue" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts tests/launcher.test.ts && git diff --check` — passed (9 tests plus diff check).
- `cd term-control-center && node --import tsx --test --test-name-pattern "hand off to CEO review|PRD review launch prompt|parallel PRD authoring drafts|parallel draft PRD Studio|logical draft job row|authoring launch failure|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts|unsafe pre-issue" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts tests/launcher.test.ts && git diff --check` — passed (12 tests plus diff check).
- `cd term-control-center && node --import tsx --test --test-name-pattern "board CEO review handoff|hand off to CEO review|PRD review launch prompt|parallel PRD authoring drafts|parallel draft PRD Studio|logical draft job row|authoring launch failure|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts|unsafe pre-issue" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts tests/launcher.test.ts && git diff --check` — passed (13 tests plus diff check).
- `cd term-control-center && node --import tsx --test --test-name-pattern "non-draft authoring|records created issue metadata|long draft-scoped|board CEO review handoff|hand off to CEO review|PRD review launch prompt|parallel PRD authoring drafts|parallel draft PRD Studio|logical draft job row|authoring launch failure|PRD Author launch prompt|pi-agent wrapper honors draft-scoped|PRD planning execute fails closed|seed-only drafts|unsafe pre-issue" tests/server.test.ts tests/launchPlan.test.ts tests/agentopsComsLabel.test.ts tests/terminalJobSidebar.test.ts tests/launcher.test.ts && git diff --check` — passed (16 tests plus diff check).
- `cd term-control-center && npx tsc -p tsconfig.app.json --noEmit && npx tsc -p tsconfig.server.json --noEmit` — failed in server test config on pre-existing `tests/contextRenewal.test.ts` importing `../../pi-packages/agentops-context-renewal/lib/policy.ts` outside `rootDir`; app typecheck completed before this server-config failure.
- An accidental broad `npm test -- --test-name-pattern ...` invocation ran many tests because the pattern was passed after npm's script expansion; it timed out and surfaced unrelated existing implementation-launch validation failures. The focused command above passed.

## Next planned implementation slices
1. Add safe draft job model/store and `/groups` summary integration with tests.
2. Wire board/React active jobs to show logical draft rows without exposing attach tokens beyond current local-only behavior.
3. Harden execute-authoring transition/idempotency and planning brief path handoff.
4. Add remaining final hygiene/validation and steward/verifier bug-check handoff.

## Open risks / notes
- Seed-only visibility has no server group today; implementation must decide whether to create a non-pane draft job record immediately on `+` or after Planner launch while still satisfying PRD requirements.
- Existing `initialIdea` stripping from persistence must be preserved.
- Steward review is required before final bug-check because session lifecycle/sidebar/artifacts change.

## Verifier finding fixes
- `F192-CP1-001`: updated `current-state-design.md` to specify draft-scoped coms isolation across planner/authoring phases, including metadata fields, launch env/pi-agent behavior, fail-closed peer discovery, and tests.
- `F192-CP2-001`: seed-only draft jobs no longer pass React Term active jobs attachability without panes; board modal retains seed-specific reopen handling. Added a focused static test.
- `F192-CP3-001`: changed authoring transition ordering so downstream authoring starts/links before planner retirement; added failure regression proving planner remains visible/retryable.
- `F192-CP3-002`: validated safe draft identifiers before physical group/path use; tightened validation after verifier research to reject tmux-normalized `:` and `.` as well as path separators, with regression coverage.
- `F192-FINAL-001`: CEO review handoff now requires a draft-scoped PRD authoring group and refuses non-draft authoring without retiring unrelated jobs.
- `F192-FINAL-002`: draft-scoped coms project/dir now includes an always-retained stable short hash over full worktree plus draft id to avoid long-prefix and long-worktree collisions.
- `F192-FINAL-003`: added safe `/groups/:id/draft-issue` metadata update path, exposes safe created issue metadata in draft summaries, and defaults CEO handoff from recorded metadata.

## Verifier status
- Checkpoint 1 approved at revision 2.
- Checkpoint 2 approved at revision 4.
- Checkpoint 3 approved at revision 7.
- Checkpoint 4 approved at revision 8.
- Checkpoint 5 approved at revision 11.
- Steward final hygiene review returned clean; no cleanup required before final verifier bug-check.
- Final verifier bug-check approved at revision 15 (`bug_check_status: passed`).
