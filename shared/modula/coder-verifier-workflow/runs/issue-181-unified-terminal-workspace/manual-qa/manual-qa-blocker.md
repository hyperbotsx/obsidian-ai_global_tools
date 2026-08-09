# Manual QA Attempt — Issue #181

Date: 2026-06-30

## Attempted
- Tried to start `npm run dev:fake` in `term-control-center` for local Browser/manual QA.
- The backend side failed before readiness with `tsx` IPC `EADDRINUSE` under the worktree runtime tmp directory.
- Found port `3032` already owned by a long-running `node build/server/index.js` process outside this dev attempt.
- Started Vite-only preview briefly on `127.0.0.1:3033`, then stopped it.

## Safe stop reason
- I did not open the terminal UI against the already-running backend because it was not the controlled fake backend for this checkpoint, and opening default terminal panes could create or attach real sessions rather than isolated Browser-QA evidence.
- No screenshots or terminal transcripts were captured.

## Required human/operator preview
Please verify in a controlled local terminal workspace/browser preview:
1. Select/copy 3 terminal lines.
2. Select/copy 50+ terminal lines.
3. Select while terminal output is arriving.
4. Sidebar expand/collapse, job switching, selected state, and attention indicators.
5. Pane maximize/restore from a standard two-pane workspace, including restoring prior diff/browser state if open.
6. Pipeline shows selected-job timeline and `Kodus Review` as safe unavailable when no live status exists.
7. Two PRD draft/planner sessions with different draft IDs remain visible/resumable side by side.

