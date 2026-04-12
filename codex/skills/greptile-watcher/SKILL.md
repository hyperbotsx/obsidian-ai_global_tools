---
name: greptile-watcher
description: Monitor GitHub pull requests for Greptile review comments, thumbs-up approvals, and re-review cycles. Use when asked to watch PRs, wait for Greptile's all-clear signal, summarize new Greptile findings, or re-trigger @greptile after fixes land.
---

# Greptile Watcher

Use `gh` for GitHub access and the bundled watcher script for repeatable monitoring.

## Quick Start

Run a one-shot scan before starting a long-lived watcher:

```bash
python3 /home/hyperbots/.codex/skills/greptile-watcher/scripts/watch_greptile.py \
  --repo owner/repo \
  --pr 123 \
  --pr 124 \
  --once
```

Start persistent monitoring from the repo or worktree you want to track:

```bash
python3 /home/hyperbots/.codex/skills/greptile-watcher/scripts/watch_greptile.py \
  --repo owner/repo \
  --pr 123 \
  --pr 124 \
  --poll-seconds 120 \
  --settle-seconds 600
```

The watcher stores state under `.codex-local/greptile-monitor` in the current working directory unless you override `--state-dir`.

## Workflow

1. Run `gh auth status` and confirm the GitHub session is authenticated.
2. Run the watcher once with `--once` to inspect the current Greptile cycle.
3. If the user wants continuous monitoring, launch the watcher in a long-lived session.
4. Read `.codex-local/greptile-monitor/state.json` for current cycle status.
5. Read `.codex-local/greptile-monitor/watcher.log` for watcher activity.
6. Read `.codex-local/greptile-monitor/review-cycles.md` for captured Greptile comments and approvals.
7. When Greptile leaves actionable feedback, fix the quick issues directly on the PR branch.
8. For large KISS-only refactors, create a GitHub issue instead of bloating the PR.
9. After fixes land, post a fresh `@greptile` comment and continue watching the next cycle.

## Approval Signal

Treat a Greptile `+1` reaction from `greptile-apps[bot]` on the latest `@greptile` ping comment as the all-clear signal only when there are no Greptile review comments, PR reviews, or inline review comments after that ping.

Ignore `eyes` reactions for approval. Ignore `+1` when Greptile also left review content in that same cycle.

Do not auto re-ping a cycle that already has that clean approval.

If there are no new Greptile comments and the latest ping has Greptile `+1`, treat the PR as quiet from the Greptile side.

## Script

### scripts/
- `scripts/watch_greptile.py`
- Supports repeated `--pr` flags for multi-PR monitoring.
- Captures issue comments, PR reviews, inline review comments, and approval reactions.
- Posts a single re-review ping when a Greptile review cycle settles without approval.
- Writes `watcher.pid`, `state.json`, `watcher.log`, and `review-cycles.md` under the chosen state directory.

## Notes

- Prefer this skill whenever the user explicitly asks to monitor Greptile, wait for a Greptile thumbs-up, or keep re-triggering Greptile on GitHub PRs.
- Keep the monitoring local to the current repo/worktree unless the user asks for a different `--state-dir`.
- Stop a running watcher by killing the PID stored in `.codex-local/greptile-monitor/watcher.pid`.
