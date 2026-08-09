# GitHub Issue Workflow

Use this only when the human explicitly asks to create or update a PRD issue.

## Inputs

- Active AgentOps Harness profile.
- Target repository from the profile.
- GitHub Project owner and number from the profile.
- Tracker issue from the profile.
- Draft PRD that passed readiness self-review.
- Existing issue number for updates, or a new issue title for creation.

## Create Draft PRD Issue

1. Verify the configured GitHub Project has launch metadata fields `Working Branch` and `Worktree Path`. If either is missing, create text fields when the human authorized Project setup; otherwise stop and report the exact missing fields.
2. Create the issue in the configured repository with draft PRD labels from the profile.
3. Add the issue to the configured GitHub Project.
4. Update the body with:
   - final issue URL;
   - exact metadata labels `Worktree` and `Proposed working branch`;
   - issue-numbered branch name ending with `-<issue-number>`;
   - tracker issue;
   - dependencies;
   - profile-derived worktree/code home.
5. Set configured Project fields:
   - Type: PRD when available;
   - Pipeline Status: Draft or PRD review when available;
   - PRD Review Status: Draft or Needs Review when available;
   - CEO Approved: No when available;
   - Working Branch ending with `-<issue-number>`;
   - Base Branch when available;
   - Worktree Path.
6. Read back the Project item and fail closed if `Working Branch` or `Worktree Path` is blank.

## Update Existing PRD Issue

1. Read the current issue body first.
2. Preserve canonical sections unless the human requested changes.
3. Ensure the issue body has exact `Worktree` and `Proposed working branch` metadata, deriving values from the active profile and issue number when missing.
4. Update only the PRD body and configured draft fields relevant to the request.
5. Set/read back `Working Branch` and `Worktree Path` Project fields for every open, not-yet-implemented PRD.
6. Leave approval fields unchanged unless a separate CEO review workflow explicitly authorized the change.

## Safety Rules

- Prefer authenticated `gh` CLI operations for GitHub.
- Do not use memory as a source of truth over current issue/project/profile state.
- Do not create repo-local PRD copies as live sources.
- Do not approve PRDs, open implementation PRs, merge, deploy, or start execution.
- If a configured Project field or label is missing, report it and continue only with safe draft defaults.

## Completion Message

```text
I created/updated the draft PRD in <issue URL>. It is not approved yet. Next step is CEO review when you are ready.
```
