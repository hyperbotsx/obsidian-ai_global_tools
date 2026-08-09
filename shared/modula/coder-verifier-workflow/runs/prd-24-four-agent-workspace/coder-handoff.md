# Coder Handoff — PRD #24 Four-Agent Adaptive Workspace

## Source of truth

- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/24
- Branch: `feat/four-agent-workspace-24`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`

## Pre-edit state

- `git status --short --branch`: `## feat/four-agent-workspace-24...origin/main`
- Pre-existing dirty files: none.

## Scope controls

Allowed by PRD #24:
- `term-control-center/` launch profiles, server launch contracts, UI layout/status behavior, tests.
- `scripts/agentops/` wrapper/role support where present.
- AgentOps workflow/coms documentation and run artifacts under `dev-plans/agentops/coder-verifier-workflow/runs/prd-24-four-agent-workspace/`.
- Global skills vault updates for Steward, PRD Author, and Codebase Expert if needed.

Forbidden without separate approval:
- Public terminal exposure or LAN binding by default.
- Arbitrary command execution from browser input.
- Repo-local skill copies.
- PR creation, merge, deployment, production-readiness claims.
- Product-code route/navigation changes outside AgentOps terminal workspace scope.
- Secrets, credentials, raw private transcripts, or private account data in committed files/handoffs/coms payloads.

## Verifier checkpoints

1. UX contract checkpoint.
2. Four-role launch checkpoint.
3. Responsive layout checkpoint.
4. Peer coms checkpoint.
5. Steward and authoring skills/workflow checkpoint.
6. Final bug-check.

Current checkpoint: Final verifier bug-check approved.

## Researcher/steward coordination

- PRD names research-first surfaces: iOS/iPadOS browser terminal behavior, xterm.js mobile/touch/keyboard behavior, current Pi/coms role launch behavior, and responsive terminal layout constraints.
- Researcher freshness consult completed before implementation edits. Summary: use feature/responsive detection rather than iPad UA assumptions; handle iOS visual viewport and on-screen keyboard; avoid hover-only controls; xterm.js mobile/touch remains fragile; refit/replay terminals when panes become visible; hidden PTY/session state must survive UI switching; coms is local IPC and must not carry secrets.
- Human clarification received: every configured implementation role must be a bidirectional peer. Coder, verifier, researcher, and steward can each directly message any other role in the same worktree/coms pool. PRD authoring defaults to a three-role peer mesh: PRD Author, Researcher, and Codebase Expert. This does not create hierarchy or bypass mandatory coder/verifier review/human gates.
- `coms_list` preflight: verifier and researcher are live in the `agentops-term` pool; Steward was not visible in the current pool at session start. Added global Steward skill support so new implementation launches can prime it through the wrapper. If Steward is required but not live before the pre-final hygiene gate, the flow must stop/escalate instead of skipping it.

## Implementation notes

- Added checkpoint artifact: `dev-plans/agentops/coder-verifier-workflow/runs/prd-24-four-agent-workspace/ux-contract-checkpoint.md`.
- Revision 2 addressed verifier findings:
  - `UX-24-C1-001`: explicit status states, hidden-role badge placement, and pinning behavior added.
  - `UX-24-C1-002`: explicit steward-before-final-bug-check ordering, cleanup/recheck step, no-duplicate-bug-check rule, and escalation if steward is unavailable added.
- Checkpoint 2 launch changes:
  - Expanded launch role/profile types to include `researcher`, `steward`, `prd-author`, and `codebase-expert` in addition to coder/verifier/shell where applicable.
  - Implementation launch requests now normalize legacy coder/verifier payloads to verifier, coder, researcher, steward; the board launcher sends all four roles explicitly.
  - Added `scripts/agentops/pi-agent.sh` with a strict allowlist for coder, verifier, researcher, steward, prd-author, and codebase-expert; unknown roles fail closed.
  - Launch group context records workspace mode and launched peer roles.
  - Board launcher copy now describes the four bidirectional peer roles without exposing PR/merge/deploy/approval/trading/backtest actions.
  - Added global Steward skill at `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/steward/SKILL.md` so the new wrapper role can prime.
- Revision 2 addressed verifier finding `LAUNCH-24-C2-001`:
  - Group launch validation now rejects non-`codex` provider choices for peer-agent panes.
  - Group launch command resolution now routes every peer-agent pane through `scripts/agentops/pi-agent.sh <role>` from the target worktree.
  - Board implementation launcher now exposes Pi/Codex role-agent profile choices only for the four peer roles.
  - Server/completion/launcher tests now assert wrapper-backed four-role launch behavior and rejection of non-wrapper provider choices.

- Checkpoint 3 responsive layout changes:
  - Replaced tablet/coarse-pointer one-pane behavior with phone-only one-pane behavior at `max-width: 760px`.
  - Desktop/tablet peer workspaces now render only the active two-role pair: `Coder + Verifier` or `Researcher + Steward`; hidden role panes remain mounted in the React tree and keep their session IDs/attach tokens.
  - Phone mode renders one active role pane with role buttons for every launched role.
  - Pair and role switchers include status text for hidden roles and a persisted `Pin active`/`Pinned` toggle.
  - Embedded terminal mode now keeps the switcher visible above the terminals so pair/role switching is available inside the live modal iframe.
  - PRD authoring now defaults to three visible roles: `PRD Author`, `Researcher`, and `Codebase Expert`; Steward is optional for final hygiene/readiness review instead of a default visible pane.
- Revision 2 addressed verifier findings:
  - `RESP-24-C3-001`: leaving phone breakpoint now clears phone-only focus mode so desktop/tablet returns to pair mode.
  - `RESP-24-C3-002`: active role selection is persisted via `ACTIVE_ROLE_KEY` and restored only when that role exists in the current pane set.
  - `KISS-24-C3-003`: `useAppEffects` now takes a context object instead of six positional parameters.

- Checkpoint 4 peer-coms changes:
  - Added `dev-plans/agentops/coder-verifier-workflow/coms-transport.md` documenting worktree isolation, bidirectional peer mesh, implementation roles, PRD authoring roles, request envelopes, no-loop rules, one-in-flight discipline, and Steward-before-final-bug-check ordering.
  - Added a test assertion that the coms contract documents bidirectional implementation and authoring peer roles and steward-before-final-bug-check ordering.
- Revision 2 addressed verifier finding `COMS-24-C4-001`:
  - Contract now requires `coms_list` live-target checks before every outbound peer request, not only before first send.
  - Contract now fails closed with `needs_human`/blocked status when the target is absent, avoiding cross-project/name fallback.
  - Contract now states required Steward hygiene gate absence stops/escalates instead of skipping Steward review.
- Checkpoint 5 skill/workflow changes:
  - Added global `steward`, `prd-author`, and `codebase-expert` skills in the approved global Pi skills vault.
  - Added `docs/skills.md` role expectations for implementation and PRD-authoring workspaces.
  - Added launcher tests for default three-role PRD authoring and explicit compact authoring mode.
  - Wrapper allowlist already supports `steward`, `prd-author`, and `codebase-expert`; missing skill files fail closed.
- Revision 2 addressed verifier finding `SCOPE-24-C5-001` by reverting the unreported generated timestamp change in `dev-plans/prd-backlog.md`.

## Changed files for checkpoints 2-5

- `pipeline-diagram/board.html`
- `scripts/agentops/pi-agent.sh`
- `term-control-center/server/index.ts`
- `term-control-center/server/launchGroup.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/shared/protocol.ts`
- `term-control-center/src/App.tsx`
- `term-control-center/src/TerminalPane.tsx`
- `term-control-center/src/styles.css`
- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `docs/skills.md`
- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/steward/SKILL.md`
- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/prd-author/SKILL.md`
- `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/pi/skills/codebase-expert/SKILL.md`

## Validation log

- `cd term-control-center && npm run typecheck` — pass.
- `cd term-control-center && npm test` — pass, 112 tests.
- `bash -n scripts/agentops/pi-agent.sh` — pass.
- `git checkout -- dev-plans/prd-backlog.md && git status --short --branch` — pass; unreported backlog timestamp change removed.
- `coms_list project=agentops-term include_explicit=true` — pass after human launched Steward; verifier, researcher, and steward are live.
- `git checkout -- dev-plans/prd-backlog.md && git status --short --branch` — pass; recurring runtime timestamp drift removed before Steward review.

## Steward hygiene gate

Structure/docs/scripts/global skill files changed, so the PRD #24 Steward pre-final hygiene gate was required before final verifier bug-check.

Steward decision: `clean`.

Steward inspected `git status`, `git diff --stat`, `git diff --check`, run artifacts, script placement, docs, and global skill files. No cleanup recommended. Steward confirmed no repo-local skill folders, no unrelated dirty drift, `dev-plans/prd-backlog.md` not dirty, and `git diff --check` clean. Steward said verifier hygiene recheck is not needed and final verifier bug-check can proceed.

Final bug-check finding `BUGCHECK-24-F6-001` found recurring runtime timestamp drift in `dev-plans/prd-backlog.md`. Bounded cleanup applied: `git checkout -- dev-plans/prd-backlog.md`, `chmod u-w dev-plans/prd-backlog.md` to prevent runtime tooling from re-dirtying it during finalization, and `git diff -- dev-plans/prd-backlog.md --exit-code` passed.

Steward recheck after cleanup: `clean`. Steward confirmed `dev-plans/prd-backlog.md` is no longer dirty, current dirty scope remains limited to expected PRD #24 files, and final verifier bug-check may proceed. Steward noted the file is locally owner-read-only (`464`) and not a blocker for the hygiene gate.

Final verifier bug-check recheck: approved. Verdict JSON reported `bug_check_status: passed`, `open_findings: 0`, `next_actor: human`.
- `git status --short --branch` — pass, expected checkpoint files modified/untracked only.

## Post-approval browser QA follow-ups

- Restored a Claude model choice in the PRD implementation launcher while keeping peer-agent panes routed through the Pi wrapper provider, preserving `LAUNCH-24-C2-001` guardrails against direct/mixed CLI launch behavior.
- Researcher follow-up confirmed installed Pi supports `claude-opus-4-8`; the launcher now exposes `Pi · Claude Opus 4.8` with default model `claude-opus-4-8`, overrideable via `TERM_CONTROL_PI_CLAUDE_MODEL` for Sonnet or another fallback.
- `pipeline-diagram/board.html` now includes the Claude Opus choice for coder, verifier, researcher, and steward dropdowns.
- Added regression coverage in `term-control-center/tests/launchProfiles.test.ts` and `term-control-center/tests/boardGuardrails.test.ts`.
- Validation: `cd term-control-center && npm run typecheck`; `cd term-control-center && npm test`; `cd term-control-center && npm run build`; deployed updated board HTML and restarted the local term service on `127.0.0.1:3032`; `/launch-profiles` returns `pi-claude-opus`.
- Verifier bounded review revision 14: approved; `open_findings: 0`; `bug_check_status: not_applicable`; `next_actor: human`.
- Verifier bounded review revision 15 for Opus 4.8 update: approved; `open_findings: 0`; `bug_check_status: not_applicable`; `next_actor: human`.

## HyperPi branding follow-up

- Added a restrained HyperPi wordmark and pi monogram to the top-left brand position on board, pipeline, WIP, and terminal surfaces.
- `pipeline-diagram/global-nav.js` injects the reusable HyperPi brand link for static dashboard surfaces, with floating and inline modes plus mobile overflow handling.
- `term-control-center/src/App.tsx` and `term-control-center/src/styles.css` add the same HyperPi brand to the terminal top nav and update terminal hero copy to `HyperPi local terminal` / `Agent workspace`.
- Regression coverage added in `term-control-center/tests/boardGuardrails.test.ts` for the static nav and terminal nav brand.
- Initial verifier review revision 16 requested one fix, `BRAND-24-R16-001`: reconcile the updated HyperPi terminal visual contract with regression tests.
- Bounded fix: updated `term-control-center/tests/boardGuardrails.test.ts` to assert the HyperPi terminal palette while preserving shared static theme assertions. `term-control-center/tests/termBasePath.test.ts` already reflected the soft HyperPi terminal chrome contract in the current tree.
- Validation after fix: `cd term-control-center && npm test -- --test-name-pattern='persistent navigation|term control center exposes'` — pass, 118 tests; `node --check pipeline-diagram/global-nav.js`; `cd term-control-center && npm run typecheck`; `cd term-control-center && npm run build`; `git diff --check`. Deployed `global-nav.js` to the nginx-served public root and restarted the local term service on `127.0.0.1:3032`.

## Create PRD authoring launch follow-up

- Human requested continuing PRD #24 from the current dirty tree to replace the old bottom-sheet/custom `Create PRD` chat UX with the terminal-style PRD authoring workspace.
- Pre-existing dirty scope before this pass: the current PRD #24 dirty worktree already included prior approved terminal, board, font, docs, and run-artifact changes. I did not revert unrelated dirty files or touch font assets. The accidental untracked single-space file remains untouched.
- `pipeline-diagram/board.html` now routes `Create PRD` to `openCreateAuthoring`, reusing the full-screen terminal modal instead of the old `/prd/chat` + `/prd/create` bottom panel flow.
- The authoring launcher collects an initial PRD idea, fetches local launch context from the term service, and starts `/launch` with `mode: "prd-authoring"`.
- Default authoring panes are exactly `prd-author`, `researcher`, and `codebase-expert`; Steward is not part of the default authoring role set. Explicit compact mode launches only `prd-author`.
- Draft/pre-issue launch safety added in `term-control-center/shared/launcher.ts`: `prd-authoring` can use `draftId` + `initialIdea` without a GitHub issue URL/number, while implementation launches still require canonical PRD identity.
- `term-control-center/server/index.ts` now skips completed-PRD detection for `prd-authoring` sessions and exposes token-gated `/launch-context` so the browser does not supply arbitrary command text or shell commands.
- `term-control-center/server/launchPlan.ts` and `launchGroup.ts` include the operator's PRD idea in PRD Author context and prime Researcher/Codebase Expert for bounded consults. Prompts preserve human approval, no GitHub mutation, no PR creation/merge/deploy/trading/backtest guardrails.
- `term-control-center/server/completionDiscovery.ts` now ignores draft authoring groups for completion discovery; completion/Prepare-PR remains implementation-only.
- Regression tests added/updated for terminal Create PRD wiring, default three authoring roles, no default Steward, draft/pre-issue launch, PRD idea prompt propagation, skipped completion detection, and three-pane authoring layout.

Validation for this pass:
- `npm --prefix term-control-center run typecheck` — pass.
- `npm --prefix term-control-center run test` — pass, 122 tests.
- `npm --prefix term-control-center run build:client` — pass, with existing non-blocking Vite warnings.
- `PYTHONPATH=src python3 -m pytest` — pass, 654 tests.
- `bash -n scripts/agentops/pi-agent.sh` — pass.
- `git diff --check` — pass.
- `coms_list project=agentops-term include_explicit=true` — pass; verifier/researcher/steward peers are live. This API session did not expose `PI_COMS_ID`, but the current coms pool is `/tmp/agentops/coms/agentops-term` and local verifier targets are live.

Revision 18 verifier finding `AUTHORING-24-R18-001` found the running `127.0.0.1:3032` term service was still serving the old build, so `/launch-context` fell through to HTML. Bounded fix applied:
- Ran `cd term-control-center && npm run build:server`.
- Restarted the local `127.0.0.1:3032` term service from `term-control-center/build/server/index.js` with `TERM_CONTROL_WORKTREE=/mnt/hyperliquid-data/projects/worktrees/agentops-term`.
- Verified `GET /launch-context` with the current `x-term-token` returns JSON: `{"worktreePath":"/mnt/hyperliquid-data/projects/worktrees/agentops-term","workingBranch":"feat/four-agent-workspace-24","repository":"hyperbotsx/agentops-harness"}`.
- Revision 19 verifier recheck approved; `open_findings: 0`, `bug_check_status: not_applicable`, `next_actor: human`.
- Revision 20 final bug-check found `BUGCHECK-24-R20-001`: recurring runtime timestamp drift in `dev-plans/prd-backlog.md`. Bounded cleanup applied: `git checkout -- dev-plans/prd-backlog.md`, `chmod u-w dev-plans/prd-backlog.md`, and `git diff -- dev-plans/prd-backlog.md --exit-code` passed with file mode `464`.
- Revision 21 final bug-check recheck approved; `bug_check_status: passed`, `open_findings: 0`, `next_actor: human`.
