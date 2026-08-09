Verifier report changed. Read the report file now and act only if its current Next actor is coder.

Report:
dev-plans/agentops/coder-verifier-workflow/runs/session-1780990501083/verifier-report.md

Notification signature: `1781011557247013003:6726:c19cdd2bc38df38edb3e3351b1f0f42a7d73c5df694fe3a4f619ee2493a85c9e`
Machine summary from notification-time read:
- Decision: `approved`
- Next actor: `coder`
- Status validation: failed (invalid Bug-check status: pass). Stop and ask the verifier to correct verifier-report.md before proceeding.

The report file is authoritative. If its current Machine Status differs from this notification summary or signature, discard this queued notification and follow the file.

If Machine Status validation failed, stop and request a corrected verifier report. If `revision_requested`, apply only the bounded requested fixes, update coder-handoff.md and coder-ready.md, and request verifier recheck. If `approved`, continue only to the next approved checkpoint or request final bug-check when implementation is complete. If `needs_human` or `rejected`, stop and ask the human.

Snapshot omitted to avoid stale queued verifier-report backlog.
