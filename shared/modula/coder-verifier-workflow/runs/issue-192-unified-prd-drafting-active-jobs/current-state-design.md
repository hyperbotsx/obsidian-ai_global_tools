# Issue #192 current-state audit and lifecycle design

## Source
- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/192
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-192`
- Branch: `prd/unified-prd-drafting-active-jobs-192`

## Current state summary
- `/groups` is the canonical active-job feed and returns safe `SessionGroup` summaries from `term-control-center/server/index.ts` and `term-control-center/server/launchGroup.ts`.
- `/launch` creates/reuses physical groups. Dedupe keys are `issue:<number>` or `draft:<draftId>` plus project; non-review sessions also match worktree and branch.
- Pre-issue PRD planning already uses `task.draftId` as the only durable identity before a GitHub issue exists.
- Planner launch is `mode: prd-planning` with one `planner` pane. Planner writes `/tmp/agentops/term-context/<plannerGroupId>/planning-brief.json`.
- `/groups/:id/execute-authoring` validates the planning brief and explicit `launch`, then launches `mode: prd-authoring` from the planner task.
- `replaceDraftAuthoringGroups` currently kills/deletes matching draft planning/authoring groups so unrelated drafts survive, but the visible group id changes from planner to authoring.
- Tmux persistence stores safe group metadata and salted attach-token hashes; browser localStorage remembers plaintext attach tokens only client-side for reattach.
- `initialIdea` is intentionally stripped from server persistence and must not be reintroduced into durable metadata.
- Active Jobs in the React Term app and board modal render one row/button per physical group today and require attachable panes.
- React Term and board modal share `evonome-term-groups` localStorage for 12h plaintext attach-token reattach; server persistence stores only salted token hashes.
- Server `sessionStore` does not persist groups without recoverable tmux sessions, so seed-only jobs need adjacent safe storage if they must survive refresh before Planner launch.
- CEO review launch already uses normal `/launch` with `mode: prd-review`, one `ceo-reviewer`, isolated review runtime env/auth, and `reusableGroup` idempotency.
- Approved-review closeout already uses `/approval-review/closeout`, verifies matching `prd-review` metadata, kills only that group, and writes safe closeout evidence when an audit path exists.

## Minimal lifecycle model
Add a tiny logical draft job wrapper without replacing physical `SessionGroup` behavior:

```text
DraftJob
  draftJobId          // alias of existing task.draftId for compatibility
  projectId
  title               // safe short title, not raw prompt/transcript
  comsProject         // draft-scoped Pi coms project for planning/authoring peers
  comsDir             // safe local coms directory derived from comsProject
  currentPhase        // seed | planning | authoring | prd-created | handoff-to-ceo-review | closing | closed | error/recovery
  plannerGroupId?
  authoringGroupId?
  createdIssueNumber?
  createdIssueUrl?
  createdIssueTitle?
  projectPlacementStatus?
  worktreePath?
  workingBranch?
  createdAt
  updatedAt
  error?
```

Design constraints:
- Key pre-issue draft jobs by `draftJobId`, never by `issueNumber` before issue creation.
- Store only safe metadata; no raw terminal output, raw prompts, attach tokens, secrets, environment dumps, or unredacted browser state.
- Continue using physical groups for panes/tmux attach; logical draft rows should reference group ids and reuse existing attach behavior.
- Preserve `planningBriefGuard`, explicit `launch`, default authoring role resolution, and scoped group retirement.
- Add an execute transition guard so duplicate execute clicks cannot launch duplicate authoring groups.
- Pass the planning brief path to downstream authoring as safe artifact context.
- Isolate parallel draft coms by deriving a stable per-draft `comsProject` from the worktree name plus safe `draftJobId`/`draftId`, and a matching `PI_COMS_DIR` under the existing coms base. Planner and downstream authoring phases for the same logical draft use the same coms project; unrelated drafts in the same worktree do not share discovery pools.
- Extend launch environment for `prd-planning`/`prd-authoring` draft tasks with draft-scoped coms metadata (for example `PI_AGENT_COMS_PROJECT` and/or explicit `PI_COMS_DIR`) and update `scripts/agentops/pi-agent.sh` to honor that override while defaulting implementation/review sessions to the existing worktree-scoped project.
- Update authoring coms instructions so peers verify the expected draft-scoped project/pool with `coms_list` and fail closed with `needs_human` if expected same-draft peers are absent instead of falling back to the worktree-wide pool.
- For active jobs, render logical draft rows preferentially and hide superseded physical planner rows once authoring is live.
- Use existing `killGroup` semantics for retiring only groups referenced by the target draft job.
- Authoring-to-CEO review should launch the normal `prd-review` flow, reuse existing review dedupe, then retire draft groups only after review launch succeeds.
- Post-approval close should remain `/approval-review/closeout`; generic delete only closes sessions and must not imply approval.

## Proposed implementation checkpoints
1. Current-state audit and lifecycle design (this artifact only).
2. Draft job sidebar visibility: add safe draft job state/summary and render one active row for seed/planning/authoring without changing execution/review rows.
3. Planner-to-authoring transition: preserve logical identity, retire planner, pass brief path, and guard duplicate execute.
4. Parallel draft isolation: test multiple draft IDs, localStorage/server recovery, no cross-linking.
5. CEO review handoff and close: launch/reuse `prd-review`, retire draft groups on success, focus review, keep failed handoff recoverable, and preserve closeout authority.
6. Steward hygiene review, final validation, verifier final bug-check.

## Validation plan
- Focused tests first for draft job metadata/lifecycle and execute transition.
- `npm --prefix term-control-center run typecheck`
- `npm --prefix term-control-center run test`
- `npm --prefix term-control-center run build`
- `git diff --check`

## Open implementation risks
- Seed-only sidebar visibility currently has no server group; implementing it may require creating a server-side draft job record before panes exist or reflecting board modal setup state as a logical job.
- Persisted short titles must be derived safely without storing raw seed ideas.
- Current board modal and React Term app both maintain remembered group caches; any logical row support must avoid duplicate localStorage merge paths or plaintext attach-token leaks.
- Logical rows must not reuse role-based attach-token matching across planner → authoring replacement; pane credentials should remain tied to physical `sessionId`/group metadata.
- CEO review launch from a terminal authoring pane likely needs a small API plus prompt instructions; terminal text alone should not parse model output for privileged actions.

## Parallel draft coms isolation design
- Existing `scripts/agentops/pi-agent.sh` currently derives `PI_COMS_DIR` and `--project` from only the worktree name, which is acceptable for one implementation session but not for multiple same-worktree PRD drafts.
- Draft lifecycle metadata should persist `comsProject` and `comsDir` as safe identifiers, not message contents. Suggested shape: `comsProject = <worktree-name>-draft-<short safe draft id/hash>` and `comsDir = ${PI_AGENT_COMS_BASE:-/tmp/agentops/coms}/<comsProject>`.
- `launchPlan.ts` should include these values in pane env for `prd-planning` and `prd-authoring` when `task.draftId`/`draftJobId` exists. The same values must survive planner → authoring transition.
- `pi-agent.sh` should honor `PI_AGENT_COMS_PROJECT`/draft override by setting `PI_COMS_DIR` to that project-specific directory and invoking `pi --project "$PI_AGENT_COMS_PROJECT"`, while retaining current worktree defaults for implementation, PRD review, and legacy launches.
- Fail-closed behavior: if an authoring peer's expected same-draft role is not discoverable in its draft-scoped pool, the peer should report `needs_human` rather than querying the worktree-wide project or cross-project names.
- Tests should cover: two draft authoring launches in the same worktree get different `PI_COMS_DIR`/`--project`; planner and authoring for the same draft get the same coms project; implementation/review launches keep existing worktree coms behavior; prompt text no longer says authoring peers share the worktree-local coms pool for draft jobs.
