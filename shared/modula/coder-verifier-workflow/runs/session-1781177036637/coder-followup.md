Verifier report changed. Read the report file now and act only if its current Next actor is coder.

Report:
dev-plans/agentops/coder-verifier-workflow/runs/session-1781177036637/verifier-report.md

Notification signature: `1781181847309506435:7185:dfad13e95f7a19c5e24bb63631e9589d75e8f32b977f6eac17af629f8512e95b`
Machine summary from notification-time read:
- Decision: `approved`
- Next actor: `human`
- Status validation: passed

The report file is authoritative. If its current Machine Status differs from this notification summary or signature, discard this queued notification and follow the file.

If Machine Status validation failed, stop and request a corrected verifier report. If `revision_requested`, apply only the bounded requested fixes, update coder-handoff.md and coder-ready.md, and request verifier recheck. If `approved`, continue only to the next approved checkpoint or request final bug-check when implementation is complete. If `needs_human` or `rejected`, stop and ask the human.

Snapshot omitted to avoid stale queued verifier-report backlog.
