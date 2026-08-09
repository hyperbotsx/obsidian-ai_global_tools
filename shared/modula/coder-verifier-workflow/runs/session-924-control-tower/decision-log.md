# Decision Log

## 2026-06-07T18:18:27Z Intake

- Canonical PRD read via `gh api repos/hyperbotsx/SoldierOne/issues/924 --jq '{number,title,body,state}'` because `gh issue view` hit the GraphQL rate limit.
- Branch confirmed: `prd/project2-readonly-control-tower-924` tracking origin.
- Pre-existing dirty tree before edits: untracked `dev-plans/` containing `dev-plans/prd-backlog.md`.
- Allowed implementation paths: `/mnt/hyperliquid-data/projects/worktrees/agentops-harness/**`.
- Forbidden paths: Evonome-admin product code and all mutating GitHub, git branch, PR, merge, deployment, dashboard, Telegram, AI Maestro, Hermes runtime, trading, backtest, paper, and live behavior.
- Validation commands: `PYTHONPATH=src python3 -m pytest -q`, `PYTHONPATH=src python3 -m unittest discover -s tests/unit -p 'test_*.py' -q`, control-tower help/format smoke checks, `python3 -m json.tool`, and `git diff --check`.
- Stop condition: complete #924 read-only control tower checkpoints and stop after final verifier bug-check approval or human escalation.
- Checkpoint plan: use #924 checkpoints 1, 2, 3, and final bug-check.
- Browser QA: not required; checkpoint 1 adds CLI/test code only.
- Preview target: not applicable; `scripts/agentops/preview-target.py --format text` is not present in this harness repo and no preview deployment is in scope.
- Verifier socket `/tmp/agentops/pi-verifier-agentops-harness-924.sock` and coder report socket `/tmp/agentops/pi-coder-agentops-harness-924.sock` were absent at intake; artifact fallback files will be written.
- Tracker #862 was not updated because this PRD explicitly forbids GitHub writes during the read-only implementation run.

## 2026-06-07T18:18:27Z Checkpoint 1

- Added a dedicated `evonome-orchestrator-status` console script entrypoint.
- Added CLI option design for Project 2, repo, worktree, timeout, Markdown, and JSON output.
- Added read-only command allowlist enforcement with tests rejecting issue mutation and branch publication attempts.
- Kept checkpoint 1 output intentionally design-focused; Project 2 reads and worktree summaries remain checkpoint 2 scope.

## 2026-06-07T20:51:40Z Checkpoint 1 Revision 2

- Verifier requested revision `V-924-CP1-001` because `git -C <path> branch ...` allowed mutating branch creation/deletion shapes.
- Tightened `validate_git_command()` so `git branch` is limited to no-argument and explicit read-only inspection flags.
- Added tests proving `git branch new-branch` and `git branch -D old-branch` are rejected.
- Validation passed with 13 pytest tests, 13 unittest tests, CLI smoke checks, JSON parse, and `git diff --check`.
- Initial validation using `/tmp` hit root filesystem exhaustion; reran smoke outputs under the artifact validation folder.

## 2026-06-07T21:00:10Z Checkpoint 2

- Verifier approved checkpoint 1 revision 2 with no findings and cleared coder to proceed to checkpoint 2.
- Added Project 2 item-list reading through the read-only command runner with bounded timeout and graceful degraded health.
- Added section summaries for active work, ready-for-agent work, blocked work, PRD drafts, and approved-not-started PRDs.
- Added worktree branch/dirty-state inspection using `git -C <path> status --short --branch` only.
- Added stable top-level report keys for later JSON consumers while leaving drift warning population for checkpoint 3.
- Added unit tests for Project 2 categorization, worktree health, and degraded Project 2 reads.
- Validation passed with 15 pytest tests, 15 unittest tests, CLI smoke checks, JSON key assertion, JSON parse, forbidden runtime command grep over `src scripts pyproject.toml`, and `git diff --check`.

## 2026-06-07T21:12:49Z Checkpoint 2 Revision 2

- Verifier requested revision `V-924-CP2-001` because Project 2 reads could silently truncate while health remained `ok`.
- Verifier requested revision `V-924-CP2-002` because failed worktree git-status reads could render as `clean`.
- Increased the default Project 2 item limit to 500 and added truncation detection when `totalCount` exceeds returned items.
- Changed truncated Project 2 reads to degraded health with a rerun message.
- Changed failed worktree status reads to `status=degraded`, `dirty=None`, `branch=None`, and included the git error in JSON/Markdown.
- Added tests for Project 2 truncation and failed existing-directory worktree status.
- Validation passed with 17 pytest tests, 17 unittest tests, CLI smoke checks, JSON key assertion, JSON parse, forbidden runtime command grep, and `git diff --check`.

## 2026-06-07T21:23:04Z Checkpoint 3

- Verifier approved checkpoint 2 revision 2 with no findings and cleared coder to proceed to checkpoint 3.
- Added drift detection for active items missing owner metadata, missing referenced worktrees, branch/worktree mismatches, and approved PRDs with stale draft/review pipeline statuses.
- Added Markdown rendering for drift warning reason/code lines while preserving JSON drift warning evidence.
- Added unit tests for synthetic drift warnings and Markdown drift rendering.
- Live JSON smoke produced drift warning evidence in `validation/control-tower-cp3.json`.
- Validation passed with 19 pytest tests, 19 unittest tests, CLI smoke checks, JSON key assertion, JSON parse, live drift assertion, forbidden runtime command grep, and `git diff --check`.

## 2026-06-07T21:31:13Z Final Bug-check

- Verifier approved checkpoint 3 with no findings and cleared coder to proceed to final read-only enforcement and bug-check.
- Added explicit read-only enforcement tests for PRD-forbidden GitHub issue/project mutations, git commit/push/checkout branch creation, and docker run command patterns.
- Revalidated CLI help, Markdown output, JSON output, stable top-level keys, read-only mode, live drift warnings, forbidden runtime command grep, and whitespace diff checks.
- Validation passed with 20 pytest tests plus 9 subtests, 20 unittest tests, CLI smoke checks, JSON key assertion, JSON parse, read-only mode assertion, live drift assertion, forbidden runtime command grep, and `git diff --check`.
- Validation outputs were written under the artifact validation folder because `/tmp` is full on this machine.

## 2026-06-07T21:37:04Z Final Bug-check Revision 2

- Verifier requested revision `V-924-FINAL-001` because system health did not explicitly cover gh auth/read availability or issue-read health.
- Added bounded `gh auth status` health and bounded `gh issue list --repo <repo> --limit 1 --json number` health through the read-only command runner.
- Added JSON `system_health` entries for `gh_auth_read`, `project_2_read`, `issue_read`, and `worktree_read` with overall degradation when any source is unavailable.
- Added Markdown system health rendering for gh auth/read availability and issue-read status, including degraded messages.
- Added tests proving auth/issue health fields degrade on command failure and issue-read degrades when repo is not configured.
- Validation passed with 23 pytest tests plus 9 subtests, 23 unittest tests, CLI smoke checks with `--repo`, JSON key assertion, system health source key assertion, JSON parse, read-only mode assertion, live drift assertion, forbidden runtime command grep, and `git diff --check`.

## 2026-06-07T21:40:06Z Final Approval

- Verifier approved `V-924-FINAL-001` and final bug-check with no findings.
- Required coder action: none.
- Checkpoint sequence is complete for #924 read-only control tower implementation.
