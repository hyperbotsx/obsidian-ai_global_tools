# Coder handoff — Completed-list false positive for open PRD #198

## Source of truth

- User report: PRDs #192 and #198 show on both board and completed list.
- PRD #192: https://github.com/hyperbotsx/agentops-harness/issues/192
- Follow-up PRD #198: https://github.com/hyperbotsx/agentops-harness/issues/198
- Branch: `fix/completed-prd-linked-pr-198`

## Pre-edit status

- `git status --short --branch` showed branch `fix/completed-prd-linked-pr-198...origin/main` with one preserved untracked planning file:
  - `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/continuation-prompt-20260629-kody-findings.md`

## Scope boundaries

Allowed:

- Close out PRD #192 because PR #197 is merged and user explicitly asked to do so.
- Fix completed-list false positive so open PRDs with unrelated merged PR cross-references do not appear complete.
- Add focused unit tests.

Forbidden:

- No branch protection, required checks, deployment, runtime config, token/secret handling, auto-merge, or automatic debt issue creation.

## GitHub mutations

- Added closeout comment to #192.
- Closed #192 as completed.
- Set #192 Project 3 status to `Done`.
- Did not close #198; it remains the open token expiry/revoke validation follow-up.

## Code changes

- `pipeline-diagram/completed_work.py`
  - Completion detection now only uses merged timeline PRs for open issues when there is explicit implementation evidence:
    - explicit PR URL in Project/body, or
    - timeline PR matching the issue's working branch.
  - Closed/project-done issues still enrich completed rows from timeline PRs as before.
- `tests/unit/test_completed_work.py`
  - Adds regression coverage for open issue without matching branch ignoring a merged cross-reference.
  - Adds coverage for open issue with matching branch accepting merged implementation PR evidence.

## Validation

- `PYTHONPATH=src python3 -m unittest tests.unit.test_completed_work` — passed, 7 tests.
- `python3 -m py_compile pipeline-diagram/completed_work.py` — passed.
- `git diff --check` — passed.
- `python3 pipeline-diagram/generate.py` — passed; generated local data shows:
  - #192 in completed and not on board.
  - #198 on board and not in completed.

## Known notes

- Generated pipeline files were not staged; this branch changes source logic/tests only.
- The preserved PRD #101 continuation prompt remains untracked and untouched.
