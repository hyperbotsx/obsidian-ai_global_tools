# CP-1 fix round 1 — coder

Lead disposition on the verifier verdict (`/tmp/agentops/term1-363/cp1-verifier-verdict.md`,
decision `revision_requested`, 8 findings).

**I accept all 8 findings.** Read the verdict in full — it carries per-finding evidence, file:line
anchors, and reproduction logs under `/tmp/agentops/term1-363/`. This brief is my prioritisation and
the constraints on top, not a replacement for it.

Your CP-1 work is committed as `a2b0b12`. Keep working in the same worktree; the Git Manager will
commit the fix round. **You still do no git.**

---

## The gate for this round: CP1-F007

Three of the regression guards you shipped **do not fail when the production wiring they protect is
deleted**: the `verifySpawnGrace` call, the executable `installLogSink()`, and the caller-level
stale-baseline argument. Only the reuse-refresh guard was correctly sensitive.

This is the single most important item in the round. A test that passes with the fix reverted is not
protection — it is a green light with nothing behind it, and it is the dominant failure mode on this
codebase.

**Rule for this round: every fix below must be proven by a revert check.** For each one, in a
scratch copy (never in the worktree), delete or neuter the production wiring and confirm the test
actually fails. Record the result per finding in your handoff. A fix without a demonstrated failing
revert check is not done.

---

## Blocking — fix all of these

**CP1-F001 — coms verification only covers implementation groups.** `launchGroup.ts:41` builds a
verification pool only when `mode === 'implementation'`; `:80` records success for everything else.
A context-brief pane that never registers stays `running` with no reason. Browser-QA calls
`verifyComsRegistrations` at `:210` with no pre-spawn baseline. Derive the expected pool + pre-spawn
role snapshot for **every** launched agent pane, context-brief and Browser-QA included. Keep the
non-blocking HTTP contract.

**CP1-F002 — TOCTOU fail-open. This is the defect CP-1 exists to remove.** A wrapper that registers
fresh and *then* exits leaves the group `running`, no `statusReason`, every tmux session gone.
Verification waits on registry/PID state and never re-checks tmux before declaring success. Close
the window with a final stabilized tmux check, and make observed group summaries fail closed when
tmux is gone. Async verification failure must also run the full group-level cleanup.
**Scope guard: do NOT introduce the CP-3 periodic sweep.** This is a check at the end of
verification and on summary read, not a background sweeper.

**CP1-F003 — `refreshGroupLiveness` short-circuits.** `launchGroup.ts:162` uses `Array.every`, so it
stops at the first dead pane and leaves later dead panes marked live. Result: an all-dead lane group
keeps holding lane capacity and its replacement stays queued forever. Refresh **every** pane before
reducing to an aggregate, and retire the all-dead lane out of capacity before starting its
replacement.

**CP1-F004 — concurrent retry orphans panes.** `retryGroupHandler` has no per-group in-flight guard
around `retireGroup` + `startWorkspaceGroup`; two overlapping retries both return 200 and leave an
orphan pane set. Serialize or atomically claim retry per group — a concurrent request either reuses
the in-flight result or gets a bounded 409. It must never spawn a second pane set.

**CP1-F005 — FR-1 records incomplete.** Successful `spawn_outcome` records omit `reason`
(`sessionSupervisor.ts:59,89`), and the PTY launch path emits zero spawn records because logging
lives only in the tmux path. FR-1 is "every spawn attempt/outcome logged with reason" — that means
success too, and both supervisor modes. Keep one-line stdout JSON; no sensitive fields.

**CP1-F006 — brief state is logged but not surfaced.** FR-4 is "logged **and surfaced**". All four
transitions are reachable and logged, but the only reader is the backend gate — `groupSummary`,
the shared launch summaries, `jobView`, and the React UI carry no brief-state field. Expose current
brief status + reason through the existing group/job response and render all four states.

---

## Also fix, bounded

**CP1-F008 — KISS parameter budget.** `verifyComsRegistrations`, `logOutcome`, and `pendingRoles`
each take 5 params; `launchPane` takes 7. House rule is 3–4. Use small request/context objects for
the new verification and launch helper signatures.

Bound this tightly:
- Extract **only** the new CP-1 retry handler and the CP-1 launch-error UI additions into focused
  modules.
- **Do not refactor unrelated legacy code.** `index.ts` (1599 lines) and `App.tsx` (1124 lines) are
  pre-existing and are not CP-1's problem. Adding CP-1 logic into them is the issue; their existing
  size is not.
- `launchGroup.ts` is at **299** lines — one line under the limit. These fixes will push it over, so
  grow the new modules, not that file.

---

## Not in this round

Do not expand scope while fixing. Still out: liveness sweep / Recover / Archive (CP-3), store
hardening and failed-group restart persistence (CP-4), forge/GitHub (CP-5), multi-project (CP-6),
wake/re-drive (CP-7), and the context-brief input surface + lane gate routing (CP-2).

The verifier confirmed two things you got right that I want preserved: the attach-token extraction
is byte-identical to baseline, and the lane delta is a liveness-refresh call only, not CP-2 gate
routing. Don't disturb either.

## When done

Write `/tmp/agentops/term1-363/cp1-coder-handoff-r1.md` — per-finding status, the revert-check result
for each, tests added, and anything you disagree with (say so, don't silently skip). Then
`coms_send` to `lead`: `cp-1 r1 handoff ready`.
