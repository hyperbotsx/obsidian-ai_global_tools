# CP-1 verification dispatch — verifier

The coder's handoff is at `/tmp/agentops/term1-363/cp1-coder-handoff.md`. The Git Manager is
committing it now; verify the committed diff (`git show`/`git diff main...HEAD`) so you have a
stable base.

Your pre-brief (`/tmp/agentops/term1-363/cp1-verifier-prebrief.md`) still governs — V1/V2/V3 remain
the priorities. Write the verdict to `/tmp/agentops/term1-363/cp1-verifier-verdict.md`, then
`coms_send` to `lead` with the single line `cp-1 verdict ready`. Report to lead, never to the coder.

## Specific claims from the handoff I want independently checked

**C-1 — the 11 full-suite failures are all pre-existing/environmental.** This is the claim I trust
least, because the coder *modified* `tests/agentopsComsLabel.test.ts` (import redirect to the new
seam) and four of the eleven failures are in that exact file. You already snapshotted pristine main
at `/tmp/agentops/term1-363/base-ce25224/` — use it. Run those failing tests against the baseline
and confirm each one fails there too. Any failure that does **not** reproduce on baseline is a
CP-1 regression and a blocking finding. Enumerate them one by one with a pass/fail on baseline; do
not accept the summary wholesale.

**C-2 — "no FR deviation".** Check FR-1..FR-4 are each genuinely met, not merely touched:
- FR-1: does a spawn attempt *and* an outcome record actually reach stdout at runtime? V1 stands —
  a sink that exists but is not installed on the real server startup path is a fail. The handoff
  says the sink is installed "in executable server startup" — confirm that is the path the deployed
  service actually runs, not just a test harness.
- FR-2: partial-kill really kills; `statusReason` is human-readable and names the true cause; the
  HTTP launch response does not block on the coms-registration deadline; `POST /groups/:id/retry`
  respawns rather than injects, and is correctly restricted to failed groups.
- FR-3: reuse refresh catches an out-of-band tmux kill on **both** the normal path and the lane path
  (`laneOrchestrator.ts` was changed too).
- FR-4: `pending -> ready | degraded | failed` all reachable and logged.

**C-3 — the extraction refactors are behavior-preserving.** `attachToken.ts`, `launchContext.ts`,
and `launchRequestPreparation.ts` were carved out of `launchGroup.ts` to hold the 300-line rule.
The handoff claims "without behavior changes". Attach-token derivation is security-relevant —
confirm the derivation and the salt/hash handling are byte-identical to baseline, not merely
similar. A subtle change here silently breaks pane attach auth.

**C-4 — scope.** `laneOrchestrator.ts` was modified. Lane *gate routing* is CP-2/FR-6 and is out of
scope for CP-1; a mechanical liveness-refresh call-site update is in scope. Confirm which it is.

**C-5 — the new coms-registration check.** It polls the pool registry for a role's agent JSON with a
"stale pre-spawn registration ID" guard. Probe that guard: can a *previous* run's registration
satisfy verification for a newly spawned pane? That would make FR-2 fail open, which is the exact
defect CP-1 exists to remove.

## Bar

A test that would still pass with the fix reverted is not a test — spot-check by reverting a fix in
a scratch copy (never in the worktree) and confirming the test actually fails. The house failure
mode here is correct code with absent protection.
