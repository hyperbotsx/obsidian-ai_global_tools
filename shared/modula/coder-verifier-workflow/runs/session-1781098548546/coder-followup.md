Verifier report changed. Read the report file now and act only if its current Next actor is coder.

Report:
dev-plans/agentops/coder-verifier-workflow/runs/session-1781098548546/verifier-report.md

Notification signature: `1781107002230924318:10953:f1d894cccead8137df33529da9681a5efca79e30178c149108fa996bf49befea`
Machine summary from notification-time read:
- Decision: `approved`
- Next actor: `human`
- Status validation: passed

The report file is authoritative. If its current Machine Status differs from this notification summary or signature, discard this queued notification and follow the file.

If Machine Status validation failed, stop and request a corrected verifier report. If `revision_requested`, apply only the bounded requested fixes, update coder-handoff.md and coder-ready.md, and request verifier recheck. If `approved`, continue only to the next approved checkpoint or request final bug-check when implementation is complete. If `needs_human` or `rejected`, stop and ask the human.

Snapshot omitted to avoid stale queued verifier-report backlog.
