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

1. Create the issue in the configured repository with draft PRD labels from the profile.
2. Add the issue to the configured GitHub Project.
3. Update the body with:
   - final issue URL;
   - issue-numbered branch name;
   - tracker issue;
   - dependencies;
   - profile-derived worktree/code home.
4. Set configured Project fields only when available:
   - Type: PRD;
   - Pipeline Status: Draft or PRD review;
   - PRD Review Status: Draft or Needs Review;
   - CEO Approved: No;
   - Working Branch;
   - Base Branch;
   - Worktree Path.

## Update Existing PRD Issue

1. Read the current issue body first.
2. Preserve canonical sections unless the human requested changes.
3. Update only the PRD body and configured draft fields relevant to the request.
4. Leave approval fields unchanged unless a separate CEO review workflow explicitly authorized the change.

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
