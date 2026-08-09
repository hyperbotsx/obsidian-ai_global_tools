# AgentOps Peer Coms Transport Contract

This contract governs local Pi-to-Pi peer requests for AgentOps terminal workspaces. It is scoped to one worktree/coms pool and complements the role skills; it does not create any approval, PR, merge, deploy, trading, or production-readiness authority.

## Isolation

- Launch role panes through `scripts/agentops/pi-agent.sh <role>` from the target worktree.
- The wrapper sets `--project <worktree-name>` and `PI_COMS_DIR=${PI_AGENT_COMS_BASE:-/tmp/agentops/coms}/<worktree-name>`.
- An operator-configured pool name (e.g. a launch wrapper setting `PI_AGENT_COMS_PROJECT`) is equally valid when every peer in the pool runs from the same worktree root; a lead/operator attestation of that fact, recorded in the durable handoff, satisfies the isolation requirement. Peers must not fail closed on the pool *name* alone once that attestation exists.
- Before every outbound peer request, the sender checks `coms_list` in the current pool and confirms the target role is live locally before `coms_send`.
- If the intended target is not live in the current pool, the sender fails closed with `needs_human` or an equivalent blocked status instead of relying on cross-project/name fallback.
- Every peer request includes `sender_cwd`; receivers refuse requests whose cwd is outside their current worktree root.
- Do not send secrets, credentials, private account data, raw private transcripts, PR approval tokens, or deployment data over coms.

## Implementation workspace roles

Default implementation peers:

1. `lead`
2. `coder`
3. `verifier`
4. `researcher`
5. `steward`
6. `git-manager`
7. `code-reviewer`

The `lead` peer briefs the coder, receives checkpoint/completion reports, and rules on process/scope dispositions. Lead dispositions never clear human gates (PR, merge, approvals, confirm-phrase actions).

Implementation roles are bidirectional peers. Any role may send a bounded request directly to any other role in the same worktree pool.

Mandatory order remains:

1. Coder requests verifier checkpoint reviews.
2. Researcher and steward consults happen when triggered and may be initiated by any peer.
3. When structure/artifact placement changed, steward hygiene review runs before final verifier bug-check.
4. If steward is required for this gate but is not live in the current pool, the workflow stops/escalates instead of skipping steward review.
5. Coder performs bounded cleanup if needed.
6. Verifier rechecks cleanup, then runs final bug-check.
7. Git Manager receives PR preparation only after implementation is complete, verifier final bug-check evidence exists, and the configured human approval gate is satisfied.
8. Code Reviewer receives Kody/Kodus review coordination only after a PR exists and local/verifier evidence is present.

## Operator continuation authorization

An operator may explicitly authorize iterative coder/verifier revisions for one
PRD/run. Record that authorization in the durable coder handoff with its scope.
While it remains active, routine implementation findings, test failures, missing
coverage, and KISS cleanup use `revision_requested`; coder applies the bounded
fix and re-requests review without pausing the operator.

`needs_lead` sits between `revision_requested` and `needs_human`: process and
scope questions a lead can rule on — branch scope disputes, pool/transport
identity doubts, artifact-placement conflicts, proceed-or-pause calls, peer
re-anchoring after a restart. Send the question to the `lead` peer (or record
it in the durable handoff when no lead is live) and pause only the affected
work. A recorded lead disposition resolves `needs_lead`; it never substitutes
for a human gate.

`needs_human` is reserved for forbidden actions, gate-class decisions (PR,
merge, approvals, confirm-phrase actions), secrets or unsafe-auth ambiguity,
destructive or irreversible changes, conflicting source of truth, unavailable
required peers, or a finding unresolved after three bounded fixes plus any
required researcher consult. Authorization never expands approval, GitHub
mutation, PR, merge, deployment, trading, or backtest authority.

## PRD authoring workspace roles

Default non-trivial authoring peers:

1. `prd-author`
2. `researcher`
3. `codebase-expert`

All default authoring roles are bidirectional peers. PRD Author normally asks Researcher and Codebase Expert for bounded initial context before drafting. Compact small-fix mode may skip those consults only when explicitly selected and recorded.

Optional authoring peers such as `frontend-expert`, `model-reviewer`, and `synthesizer` also use the same local pi-coms pool. Before every outbound authoring peer request, the sender must run `coms_list`, verify the target role is live in the current worktree pool, and fail closed with `needs_human` instead of guessing or silently skipping. Large PRD context must be passed by artifact reference when practical rather than unbounded inline text.

Steward is not a default visible PRD authoring pane. Every full PRD should include implementation hygiene / Steward readiness instructions so later implementation is easy to review. Large or cross-cutting drafts may request an optional Steward hygiene review before the PRD is finalized.

PRD authoring never approves PRDs or mutates GitHub outside the existing explicit human-confirmation flow.

## Request envelope

Each peer request must be concise and include:

```json
{
  "type": "peer_request",
  "sender": "coder",
  "target": "steward",
  "sender_cwd": "/absolute/worktree",
  "purpose": "Check changed-file placement before final bug-check",
  "expected_response": "JSON or concise markdown with findings",
  "stop_condition": "Return cleanup recommendations or clean",
  "context_path": "dev-plans/.../bounded-context.md"
}
```

Use on-disk context files for large evidence. Keep inline prompts below transport line limits.

## Response rules

- Answer inbound requests in the normal assistant response; do not `coms_send` back to reply to the same inbound message.
- At most one outbound peer request per agent may be in flight.
- No ping-pong loops: follow-up requests must be new, bounded, and intentional.
- Role authority remains scoped:
  - Coder edits implementation scope and handoffs.
  - Verifier reviews checkpoints and final bug-check without editing coder-owned files.
  - Researcher answers source-cited technical/context questions and never edits.
  - Steward reviews structure/hygiene and only performs cleanup if explicitly authorized.
  - Git Manager owns Git/Git Town/PR lifecycle actions and sanitized Git action ledger entries after the configured human gate.
  - Code Reviewer owns advisory Kody/Kodus review triggering, finding classification, coder handoff, and re-review coordination without editing files.
  - PRD Author drafts requirements for human review.
  - Codebase Expert provides read-only repo context.

## Verdict response for verifier reviews

Verifier checkpoint responses remain compact machine-status JSON:

`decision` values: `approved` · `revision_requested` · `needs_lead` · `needs_human`.

```json
{
  "decision": "approved",
  "checkpoint_reviewed": "3 - Responsive layout checkpoint",
  "revision_reviewed": 2,
  "open_findings": 0,
  "finding_ids": [],
  "bug_check_status": "not_applicable",
  "next_actor": "coder",
  "report_path": "dev-plans/agentops/coder-verifier-workflow/runs/.../verifier-report.md"
}
```

The full review stays in `verifier-report.md`. Coder reads the full report only when the compact decision is not `approved`.
