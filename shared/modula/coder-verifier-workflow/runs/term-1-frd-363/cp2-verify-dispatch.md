# CP-2 verification dispatch — verifier

CP-1 is approved and closed at `af1ed01` (your verdict r3, 0 open findings). CP-2 is
Context-Brief end-to-end, FR-5..FR-8. Coder handoff:
`/tmp/agentops/term1-363/cp2-coder-handoff.md`. Lead brief (with my grounding):
`/tmp/agentops/term1-363/cp2-brief.md`. Git Manager is committing on top of `af1ed01`.

Verdict to `/tmp/agentops/term1-363/cp2-verifier-verdict.md`, then `coms_send` to `lead`:
`cp-2 verdict ready`. Report to lead, never to the coder.

**Scope note:** CP-2 legitimately touches `pipeline-diagram/` (board.html, public/board-light.html,
coworker-launcher.js, planning-intake.js) as well as `term-control-center/`. The board and planner
launch surfaces live there. That is authorized this checkpoint — do not flag it as out-of-scope.

## What CP-2 must deliver

- **FR-5** — board launch and planner handoff produce `task.contextBrief`, defaulted from
  per-project action config.
- **FR-6** — lane launches route through the same gate (the bypass was `index.ts:617-620` returning
  before `contextBriefLaunch`).
- **FR-7** — ready brief → `continue` → implementation cohort + Lead.
- **FR-8** — degraded continuation requires an operator reason, never inferred.

The coder shipped 14 exact-wiring revert checks, all failing as intended; I verified they ran. As
before, what I have **not** verified is that each mutates the right thing — that is yours.

## Six specific claims to attack

**C-1 — the fail-safe default is `{ policy: 'required', scope: 'unknown', surfaces: [] }`.** This is
the most consequential design decision in the checkpoint and it was the coder's call, not mine.
`required` means every implementation launch with an unconfigured project now routes through a brief
agent. Verify: (a) it is genuinely fail-closed and cannot be weakened to `skip` by a malformed or
partial config; (b) `skip` still requires a reason end-to-end; (c) a caller-supplied *valid* config is
honoured and not silently overridden; (d) an *invalid* caller config is rejected rather than falling
back to something permissive.

**C-2 — "removed title/label keyword inference".** The handoff says board tasks no longer fabricate
policy/scope/surfaces from text. Confirm no inference path survives anywhere — board, light board,
coworker launcher, or planner. Scope inferred from a title string is fabricated metadata entering a
gate, which is worse than no gate.

**C-3 — the double-defaulting claim.** "The authoritative lane task is independently defaulted again
inside Term Control before gating, so the Python coworker hop cannot omit or weaken the configured
policy." Probe it: can a hand-crafted coworker/lane request weaken or bypass the policy? Try a
request that supplies `policy: skip` with and without a reason, and one that omits `contextBrief`
entirely.

**C-4 — FR-6 lane semantics.** Confirm a run decision really produces `mode: context-brief` with a
brief pane, that a skip decision carries `contextBriefDecision` into implementation, that queued lane
placeholders preserve the gated mode, and that the new **mode identity in lane reuse** actually
prevents an implementation group being handed back as a reusable brief group. That reuse fix was the
coder's own find — verify it is real and not a no-op.

**C-5 — FR-7 through real wiring.** The test injects a live Lead spawner and asserts four
implementation roles (verifier, coder, researcher, steward) plus one Lead start, then brief-group
retirement *after* phase-two success. Confirm retirement genuinely happens only on success — a brief
group retired on a *failed* phase two would strand the job with nothing running.

**C-6 — FR-8.** Empty reason must 400 and must not start phase two. Also probe whitespace-only,
`null`, and a reason supplied on the *non*-degraded path. Confirm no reason is inferred from route
metadata, scope, or prior state.

## Regression surface

Expect **1401 passed / 11 failed / 1412 total**, +6 net tests, and the same 11 baseline failures you
enumerated by name in your CP-1 r3 verdict. Confirm the failure *set* is unchanged.

Also confirm: no CP-3..CP-7 scope crept in, no Kody-area files touched, no git command run by the
coder, and CP-1's approved behaviour is not regressed (spawn verification, summary observation, lane
liveness, Browser-QA preflight).

## Note on AC-1

CP-2's stated exit is the in-app dogfood on a real deploy. That step is **operator-gated and mine to
arrange** — the coder correctly did not attempt it. Do not hold your verdict for it. Verify FR-5..FR-8
on their merits and say explicitly in your verdict whether the code is dogfood-ready, so I know
whether the remaining gap is deployment or implementation.
