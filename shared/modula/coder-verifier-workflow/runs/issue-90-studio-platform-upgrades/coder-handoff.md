# Coder Handoff

## Task

- GitHub issue: `https://github.com/hyperbotsx/agentops-harness/issues/90`
- PRD: `GitHub issue #90 (canonical PRD source)`
- Branch: `feat/prd-studio-platform-upgrades-90`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-laneD`
- Artifact folder: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades`

## Scope

Allowed paths:

- `src/agentops_harness/**`
- `term-control-center/**`
- `pipeline-diagram/**`
- `scripts/agentops/**`
- `tests/**`
- `docs/**`
- `profiles/*.example.yaml`
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/**`

Forbidden paths:

- secrets, local config outside explicit docs/runbooks, deployment mutation, PR creation, merge/deploy flows outside PRD #90 scope, unrelated product repos/worktrees, raw private transcripts

Validation:

- `PYTHONPATH=src python3 -m pytest tests/unit`
- `npm --prefix term-control-center run test`
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run build`
- `git diff --check`

Stop condition:

- stop after final verifier bug-check approval or human escalation / `needs_human`

## Dirty Tree Before Editing

- none (`git status --short --branch` showed only branch line)

## Verifier Checkpoints

| Checkpoint | Trigger | Status | Verifier Report |
|---|---|---|---|
| 1 | Project isolation checkpoint — one shared active-project identity binds repo, GitHub Project, review/create/apply flows, review jobs, discussion/coworker sessions, and codebase roots with no cross-project leakage. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| 2 | Billing/auth checkpoint — supported Claude path, auth source, and fail-closed behavior for Max-backed local Claude Code usage. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| 3 | Approval-flow checkpoint — workflow-reachable CEO review/apply path uses the real review/apply engine with explicit human confirmation preserved. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| 4 | UX reliability checkpoint — low-friction confirmations, parked-launch guard, pane controls, and clickable terminal links. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| 5 | Native Claude / frontend QA checkpoint — approved phase-bound first-party Claude participation and Opus+Chrome frontend QA default lane without launch regressions. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| 6 | Codebase-intelligence checkpoint — backend choice, per-project isolation, freshness strategy, and at least one working agent integration path. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |
| Final bug-check | GitHub token separation, cross-project leakage, unsupported billing assumptions, and rollback behavior for launch/config changes. | `approved` | `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md` |

## Research-first Notes

### Billing/auth researcher summary (2026-06-21)

- Claude Code subscription/OAuth auth (`CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`, or interactive `claude auth login`) is the documented subscription path for Pro/Max/Team/Enterprise.
- `claude auth login --console`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and cloud-provider envs like `CLAUDE_CODE_USE_BEDROCK` / `...VERTEX` / `...FOUNDRY` indicate API or cloud-billed usage instead of subscription usage.
- Anthropic docs do not state “wrapper/subprocess = first-party” verbatim, but the supported CI/scripts OAuth path implies a local wrapper that launches the user’s own local `claude` CLI remains on the subscription path if the CLI itself is authenticated with subscription/OAuth auth.

### Codebase-intelligence researcher summary (2026-06-21)

- Backend researched: `DeusData/codebase-memory-mcp`, release `v0.8.1` (2026-06-12), MIT licensed.
- README/docs claim local-only processing with bundled embeddings and no API key, Ollama, or Docker requirement.
- Claude Code can consume it through stdio `mcp_config`; no separate cloud auth is needed for the MCP server itself.
- Per-project isolation should use a project-scoped MCP config plus a unique `CBM_CACHE_DIR` per project/worktree; default shared cache can create cross-repo results and `CROSS_*` edges.
- Freshness caveat: backend supports `index_repository` / `detect_changes`; a first-run or stale-index refresh is expected when the current project cache is empty or drifted.

## Implementation Summary

- Project routing is now shared and fail-closed across review/create/apply flows.
- Claude panes now require the supported subscription/OAuth path and fail closed on API/cloud auth.
- Approval flow is explicitly routed to the real PRD Studio review/apply path.
- UX confirmations now use low-friction `launch` / `create` choices, downstream authoring requires a completed planning brief, terminal links are clickable, and pane-control regressions are covered.
- `frontend-expert` now defaults to Claude Code Opus with Chrome-required guidance.
- `codebase-memory-mcp@0.8.1` is available as a project-bound provider with a strict per-project Claude MCP config and MCP-first guidance only on panes that actually receive MCP access.
- Agent-side `gh` runtime now uses a dedicated `GH_CONFIG_DIR` / optional dedicated token path instead of the operator’s default `gh` auth context.

## Changed Files

Product/runtime/config files:

- `docs/operations.md`
- `scripts/agentops/pi-agent.sh`
- `src/agentops_harness/ceo_review_evonome_apply.py`
- `src/agentops_harness/ceo_review_mutations.py`
- `src/agentops_harness/ceo_review_source.py`
- `src/agentops_harness/github_cli_env.py`
- `src/agentops_harness/prd_author_github.py`
- `src/agentops_harness/prd_create.py`
- `src/agentops_harness/project_context.py`
- `src/agentops_harness/review_server.py`
- `pipeline-diagram/README.md`
- `pipeline-diagram/board.html`
- `pipeline-diagram/coworker-launcher.js`
- `pipeline-diagram/global-nav.js`
- `pipeline-diagram/pipeline.html`
- `pipeline-diagram/review-notify.js`
- `pipeline-diagram/wip.html`
- `term-control-center/README.md`
- `term-control-center/server/adminHtml.ts`
- `term-control-center/server/index.ts`
- `term-control-center/server/laneOrchestrator.ts`
- `term-control-center/server/launchPlan.ts`
- `term-control-center/server/planningBrief.ts`
- `term-control-center/server/projectMemory.ts`
- `term-control-center/shared/launcher.ts`
- `term-control-center/src/TerminalPane.tsx`

Tests:

- `term-control-center/tests/boardGuardrails.test.ts`
- `term-control-center/tests/coworkerLauncher.test.ts`
- `term-control-center/tests/launchPlan.test.ts`
- `term-control-center/tests/launcher.test.ts`
- `term-control-center/tests/projectMemory.test.ts`
- `term-control-center/tests/server.test.ts`
- `term-control-center/tests/termBasePath.test.ts`
- `tests/unit/test_ceo_review_evonome_apply.py`
- `tests/unit/test_ceo_review_source.py`
- `tests/unit/test_github_cli_env.py`
- `tests/unit/test_prd_author_github.py`
- `tests/unit/test_prd_create.py`
- `tests/unit/test_project_context.py`
- `tests/unit/test_review_server_coworker.py`

Artifacts:

- `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/*`

## Validation

- `PYTHONPATH=src python3 -m pytest tests/unit`: `pass` (827 tests)
- `npm --prefix term-control-center run test`: `pass` (375 tests)
- `npm --prefix term-control-center run typecheck`: `pass`
- `npm --prefix term-control-center run build`: `pass`
- `git diff --check`: `pass`

## Steward Review

Steward reviewed changed-file placement before final bug-check and found placement clean. The only requested cleanup was to resolve untracked intended deliverables/history files. Those new source/test/artifact files are now staged, so no separate steward re-pass is needed before the final verifier bug-check.

## Final Bug-Check Fix

Revision 11 addressed verifier finding `V-FINAL-001` by introducing an agent-dedicated GitHub CLI environment:

- new helper `agent_gh_env(...)` always forces agent-side `GH_CONFIG_DIR` to `~/.config/agentops-harness/gh-agent` (or `AGENTOPS_GH_CONFIG_DIR`),
- ambient `GH_TOKEN` / `GITHUB_TOKEN` from the operator shell are stripped,
- optional dedicated token injection is supported via `AGENTOPS_GITHUB_TOKEN`, and
- all changed agent-side GitHub read/write paths (`ceo_review_source`, `prd_create`, `ceo_review_mutations`, `ceo_review_evonome_apply`) now run `gh` with that isolated environment.

This keeps agent traffic off the operator’s default `gh` credential store and rate-limit bucket, while failing naturally if the dedicated auth/config is missing.

## Assumptions / Risks

- Final verifier bug-check is still pending.
- The `claude auth status --text` parsing is heuristic because Anthropic docs do not publish a strict machine-readable contract for subscription-vs-console wording; the guard intentionally fails closed when status text is ambiguous.
- Approval owner-routing policy is still profile-driven in the existing CEO apply engine; repo/project binding is now project-scoped, but owner-policy generalization remains for a later checkpoint if needed.
- Direct inbound-native Claude hooks are still not claimed; the supported lane is local Claude Code under the existing peer orchestration boundary.
- `codebase-memory-mcp` multi-worktree semantics are still evolving upstream; this slice intentionally isolates one cache per project/worktree and does not promise shared cross-worktree graphs.

## Verifier Pairing

- Required: `yes`
- Reason: coder-verifier workflow requires checkpoint review before continuing.
- Pool preflight: `verifier`, `researcher`, and `steward` were live in the local `agentops-laneD` coms pool before the first review request.
- Coder ready file: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/coder-ready.md`
- Verifier report: `dev-plans/agentops/coder-verifier-workflow/runs/issue-90-studio-platform-upgrades/verifier-report.md`

## Coder Decision

`complete`

## Revision Log

| Revision | Trigger | Changed Files | Validation | Decision |
|---:|---|---|---|---|
| 1 | initial setup / checkpoint planning | artifact files | none | in_progress |
| 2 | checkpoint 1 implementation | project routing, review/create/apply code, board/coworker assets, tests, artifact files | listed validation passed | revision_requested |
| 3 | V-CP1-001 | strict project resolver, shared review/apply fail-closed policy, extra regression tests, artifact files | listed validation passed | approved |
| 4 | checkpoint 2 implementation | Claude auth guard env/plumbing, wrapper preflight, README note, launch tests, artifact files | listed validation passed | approved |
| 5 | checkpoint 3 implementation | PRD Author shortcut-routing prompt + approval-flow regression tests + artifact files | listed validation passed | approved |
| 6 | checkpoint 4 implementation | low-friction confirmations, intake-complete launch guard, clickable links, pane-control regression coverage, artifact files | listed validation passed | approved |
| 7 | checkpoint 5 implementation | Claude Opus + Chrome frontend-expert defaults, prompt/env updates, board defaults, regression coverage, artifact files | listed validation passed | approved |
| 8 | checkpoint 6 implementation | project-bound codebase-memory-mcp provider, MCP config materialization, Claude integration prompt, admin option, regression coverage, artifact files | listed validation passed | revision_requested |
| 9 | V-CP6-001 | gated MCP-first guidance to panes that actually receive MCP access; non-Claude panes now point to Claude-integrated peers or normal repo inspection | listed validation passed | approved |
| 10 | pre-final bug-check stewardship follow-up | staged intended new source/test/artifact files per steward recommendation; no product-code delta | `git diff --check` passed | revision_requested |
| 11 | V-FINAL-001 | dedicated agent `GH_CONFIG_DIR` / token env helper threaded through agent-side GitHub reads and writes, docs note, regression coverage | listed validation passed | approved |
