---
name: coms-peer-panes
description: Launch or remount the coder, verifier, researcher, git-manager, or steward Pi pane for the current Git worktree and branch in one shared harness-native coms pool. Use when asked to set up coder, start verifier, launch researcher, mount git manager, restore a closed peer pane, or attach the current worktree's peer team.
---

# Coms Peer Panes

Launch the requested peer role in the current worktree's shared coms pool, or return the tmux command for its already-running pane.

## Essential rules

- The Git worktree root is the pool boundary. Its basename is the default coms project; never borrow a pool from another worktree.
- Reuse a live matching role pane instead of launching a duplicate. A tmux session is only the terminal wrapper; Pi's JSONL session is the conversation state.
- Use `PI_AGENT_COMS_MODE=harness-native`. Do not manufacture `.coms` files or set `PI_COMS_DIR` by hand; that is not the named-coms artifact format.
- Launch detached, then give the operator an attach command. This keeps the requester’s current pane intact.
- A role may not perform its governed work merely because it was launched. Its existing role skill and human gates still apply.

## Phase 1 — Select the role

**Entry:** The operator requests a peer pane.

1. Accept exactly one of: `coder`, `verifier`, `researcher`, `git-manager`, or `steward`.
2. Run `git rev-parse --show-toplevel` and `git branch --show-current`; stop if outside a worktree or detached.
3. Treat an explicit worktree, branch, model, or session-resume request as an override only after reporting it back.

**Exit:** One valid role and one current worktree are known.

## Phase 2 — Reuse or launch

**Entry:** Phase 1 is complete.

Run the launcher from this skill directory:

```bash
scripts/launch-peer-pane.sh <role>
```

To restore a role after its tmux pane exited, pass the exact prior Pi session JSONL file or session ID:

```bash
scripts/launch-peer-pane.sh <role> --resume <session-file-or-id>
```

The launcher first finds a live matching role in the current worktree. If none exists, it creates a detached tmux session using the platform launcher, the harness-native coms extension, `openai-codex/gpt-5.6-sol`, and maximum thinking by default. `PI_COMS_PANE_MODEL` and `PI_COMS_PANE_THINKING` may override those defaults.

**Exit:** The launcher reports a tmux session name and an attach command, or fails with an actionable setup error.

## Phase 3 — Mount and verify

**Entry:** Phase 2 returned a session name.

Use a separate terminal:

```bash
tmux attach-session -t <session-name>
```

Inside an existing tmux client, use:

```bash
tmux switch-client -t <session-name>
```

Confirm the Pi footer shows the requested role, current worktree, chosen model, and intended coms peers. Detach with `Ctrl-b d`; do not quit Pi to leave the pane.

**Exit:** The requested role is visible in the same coms pool as its peers.

## Success criteria

- Exactly one live pane for the requested role and current worktree is selected or created.
- The pane’s current path is the worktree root and its model is explicit.
- Existing conversations are resumed only when the supplied Pi session is the requested role’s prior session.
- The operator receives an exact tmux attach command.
