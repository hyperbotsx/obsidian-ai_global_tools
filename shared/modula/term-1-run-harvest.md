# Term-1 run harvest (FRD #363) — Modula product/workflow rules

Live harvest from the four-agent run on FRD Term-1 (Lead=Opus 5, Coder/Verifier=gpt-5.6-sol,
Git Manager=gpt-5.6-terra). Dual-purpose run: ship the FRD **and** capture product rules where the
workflow hit friction. Started 2026-07-30.

Related: [[coms-reliability-audit-2026-07-29]], [[frd-agent-comms-contract-draft]],
[[buzz-relay-study-and-modula-relay-v2-plan]], [[frd-agent-wake-renewal-driver-draft]].

---

## H-1 — Trio doctor conflates "not launched by the app" with "unhealthy"

`scripts/agentops/agentops-trio-doctor.py` includes `implementation_stamped:
bool(entry.get("implementation"))` in the per-agent check set, and the pool verdict is
`all(checks.values())`. A hand-launched trio is never stamped, so **every manually-driven pool
reports `FAIL … [implementation_stamped]` on all agents and the tool exits 1 — permanently red**,
even when pid, socket, heartbeat freshness and session/socket match all pass.

**Why it matters:** the doctor is the operator's preflight. A check that can never go green for the
most common bring-up path trains operators to ignore the exit code, which is exactly when a real
failure gets missed.

**Rule:** health checks must separate *liveness* from *provenance*. Provenance ("did the app launch
this?") is useful metadata but must not gate the health verdict. Either drop it from `ok`, or split
the report into `healthy` and `app-managed` and exit on the former only.

## H-2 — Coms single outbound slot makes the Lead-as-hub pattern serial

Commit `ce25224` ("per-recipient slots") is merged on main, but the coms-mcp process actually
serving pools still enforces **one outbound request per session**: a Lead fanning out to three
peers gets `coms: outbound request already in flight` on calls 2 and 3. Confirms F-28's "hard single
outbound slot" as a *live operational* constraint, not just a code smell.

Compounding it: the **5-minute outbound TTL** means any peer whose turn runs longer than 5 minutes
has its reply silently dropped. Observed end-to-end this run — the Coder consumed a CP-1 brief and
began work (proved by file changes + rising `context_used_pct`), but its ack never arrived because
the turn exceeded the TTL. From the Lead's seat this is indistinguishable from an agent that never
woke.

**Why it matters:** the Lead is the hub for every checkpoint. Serial fan-out plus silent reply-loss
means the orchestration layer's primary primitive is unreliable exactly at the scale it exists for.

**Rules:**
1. A Lead must **never** treat a coms reply as its drive signal for long work. Drive off disk
   artifacts + a filesystem watch; use coms only for short acks and "artifact ready" pings.
2. Big briefs go to a **file**, not into a coms payload. Steer the agent with a pointer to the path.
   This survives TTL expiry, survives compaction, is re-readable by the agent, and does not consume
   the outbound slot.
3. The outbound slot is a shared, blocking resource — treat sending as a scarce operation and batch
   accordingly. Reply-loss must be assumed, not exceptional.

## H-3 — The server's logger writes to a channel nobody reads

`term-control-center/server/logging.ts` publishes to a `node:diagnostics_channel` named
`term-control-center.log`. **There is no subscriber anywhere in the repo** — verified by grep: the
only references to that channel name, and to `diagnostics_channel` at all, are its own definition.
Ten server modules already call `getLogger()` (`serverMonitors`, `leadRuntime`, `comsAdapter`,
`pageBotRuntime`, `delegation*`, …). Every one of those lines has always gone nowhere. The logger
also exposes only `warn`/`error` — no `info`.

This materially enlarges FRD #363's fact F-4 ("nothing in the launch path logs"): the launch path is
not a gap in an otherwise-working logging story, it is **one instance of a whole-server no-op**. The
E0 dogfood's "zero spawn activity in the server log" was structural at the sink, not the callsite.

**Why it matters:** a logging facade with no sink is worse than no logging — it makes engineers
*believe* the system is instrumented, and every future "add a log line" fix silently does nothing.

**Rule:** an observability seam is not delivered until something consumes it. Any FRD requiring
"log X" must state where the record lands and ship an assertion that it arrives. Adding callsites
above an unsubscribed channel is a null change.

## H-4 — Idle turn-bound agents need a wake; a queued message is not a work-turn

An idle `pi`/codex agent sitting at its prompt does **not** consume a queued coms message. The pool
registry shows `queue_depth: 1` indefinitely while the agent stays parked. `agentops-steer`
(socket-level `deliverAs:"steer"`, `triggerTurn:true`) is what converts a queued message into an
actual work-turn.

Also observed: the agents in this run are plain SSH sessions (`pts/*`), **not** tmux panes — so
pane-poking is not available as a fallback and the coms socket is the only wake path.

**Rule:** delivery ≠ activation. Any orchestrator that sends work to a turn-bound agent must pair
the send with an explicit wake, and must verify activation by a side-effect signal (file changes,
rising `context_used_pct`) rather than by the message having been accepted.

## H-5 — `context_used_pct` already exists on the pi side

FRD #363 F-27 records that the server hardcodes `context_used_pct` to 0/null
(`server/comsAdapter.ts:208,255`). Worth noting for CP-7/FR-29: **the pi coms registry already
publishes a real value** — the Coder's registry entry read `"context_used_pct": 32` mid-task.

**Consequence:** FR-29's "context-percent feed" is likely a *plumbing* job (read the value the coms
registry already carries) rather than a *build* job (invent a feed from the renewal extension).
Verify at CP-7 before scoping it as new work. Same data also feeds FRD Term-2's gauge.

## H-6 — tmux socket sprawl in `/tmp/tmux-1000/`

Thousands of `agentops-<shorthash>` tmux socket files are accumulating under `/tmp/tmux-1000/`
(one per worktree hash, per `worktreeSocket()`), with no reaping. Not in FRD #363's scope, but it is
a real resource leak on the daily-driver box and will interact with CP-3's session lifecycle work.

**Rule candidate:** the teardown invariant should cover the *socket*, not just the session — an
archived job that leaves its tmux socket behind is not fully torn down.

---

## Registry-entry oddity (low priority, noted not chased)

The coder's pool registry entry showed `heartbeat_at` **identical to** `started_at`, while the
doctor simultaneously computed a fresh ~18s heartbeat age — i.e. `started_at` appears to be
rewritten on each heartbeat rather than pinned at registration. Harmless today, but it makes
"how long has this agent been up?" unanswerable from the registry.

---

# Harvest from CP-1 / CP-2 execution (2026-07-30/31)

## H-7 — "Correct code, absent protection" is real, and only mutation testing finds it

The house failure mode was already recorded ([[correct-code-absent-protection]]). This run measured
it. Three separate times, a fix was genuinely correct and its accompanying test was **insensitive to
the fix being deleted**:

1. CP-1 r0: deleting `verifySpawnGrace`, `installLogSink()`, and the stale-baseline argument each
   left their tests green.
2. CP-1 r1: deleting `refreshGroupLiveness` from `groupSummary` left **all 13** focused tests
   passing — the existing test called that function itself before asserting, so it structurally
   could not detect removal.
3. CP-2 r0: removing `group.mode === request.mode` left **all 11** lane tests passing; removing the
   `contextBriefDecision` attachment left **all 19** focused tests passing.

None were visible to code review. All were found by reverting the production wiring in a scratch
copy and re-running.

**Rule:** a checkpoint is not verified until every new guard has a recorded revert check that (a)
mutates the *exact* production call or branch the guard protects, and (b) fails. "Tests pass" is not
evidence. Additionally, guards should be proven in **both** directions where false positives matter —
a harmless refactor must still pass (CP-1 F008 proved a rename and a legal 299-line file pass, while
a real fifth parameter fails).

**Anti-pattern to name:** a test that calls the very helper it is meant to prove is wired. It asserts
the helper works, not that production calls it.

## H-8 — Fix the class, not the instance: one finding became eight

CP-1's F006 was hostile *agent-written* free text crossing a trust boundary into state/API/render.
It was fixed locally. Two checkpoints later, CP-2's F002 was the identical defect on
*operator-supplied* text in a different field — `String(request.body?.reason || '')` coercing
`{fabricated:true}` into the string `[object Object]`, which then satisfied a human-decision gate.

Rather than accept a second patch, the Lead directed a sweep of the class. Result: **eight**
instances across brief state, group/pane `statusReason` API output, planning decision
question/resolution, planning brief text, operator and injected page-bot messages, injection edit
notes, and planner receipt reasons — consolidated behind one `shared/boundedText.ts` primitive with
its own direct boundary tests.

**Rules:**
1. When the same defect shape appears twice, stop patching and sweep for the class. Require the
   sweep's search method and inspected-file list to be *stated*, so completeness is auditable.
2. **Free-text fields are trust boundaries.** Any `reason`/`statusReason`/message that reaches
   persisted state, an API response, or a gate decision needs: string type only, trim-then-check,
   non-empty, explicit maximum. Agent-written and operator-supplied are equally untrusted.
3. A shared validator must carry its **own** direct tests. Coverage only through consumers is the
   same absent-protection failure one level up.
4. Sweeps create a new risk nobody reports: bounds set **too tight** silently reject legitimate
   content. Review chosen limits as judgement calls, not facts.

## H-9 — Set the verification bar at dispatch, not in review

CP-1 took **three** fix rounds (8 → 4 → 2 → 0 findings) because the mutation-sensitivity bar emerged
*during* review. CP-2 was dispatched with that bar stated up front and round 0 arrived with 14
exact-wiring revert checks already run.

**Rule:** the quality bar belongs in the kickoff brief, not the review. A reviewer discovering the
standard costs a full round per discovery.

Corollary observed: the Lead must also declare **when good is good**. Verification tiers grind
indefinitely otherwise. On CP-1's closing round the Lead explicitly told the verifier "this is a
closing round, do not hunt new categories" and pre-accepted one disclosed low-severity limitation.
That is a Lead call, not a verifier call.

## H-10 — Refresh the verifier *between* rounds, never let it compact *during* one

Asymmetric risk, and it took a real decision to see it: a **coder** that compacts mid-task wastes
effort and re-reads its brief. A **verifier** that compacts mid-verification can forget which probes
it already ran, believe it completed the sweep, and issue a **false `approved`** — the only failure
mode that costs a checkpoint rather than a round.

Practice adopted mid-run: refresh the verifier pane while it is idle at ~60–90%, then reconstitute it
from a standing-context file that points at **its own prior verdicts**. The verdicts are the memory —
they carry the closed-findings list, the baseline failure set, the lead rulings in force, and, most
valuably, its own past catches written back as *method*. A fresh verifier told "review this" starts
naive; one told "here is how you previously caught what reading alone missed" starts skeptical.

## H-11 — Lead rulings must be recorded where they outlive everyone's context

Two rulings had to survive coder compaction, verifier refresh, and lead compaction:
the F002 class (a)/(b) split deferring no-observer detection to CP-3, and the pre-accepted F008
limitation. Both were written into the fix briefs and the task ledger, then read back by agents that
had no memory of them.

**Rule:** a scope ruling that lives only in an agent's context window is lost at the next compaction.
Write rulings into (a) the brief the coder reads, (b) the standing context the verifier reads, and
(c) the task carrying the deferred work — with the evidence and measured numbers attached, so the
later checkpoint inherits the reasoning rather than rediscovering the bug.

## H-12 — Reading the code five times could not find what running it found in twenty minutes

CP-1 exists to make "verified" mean something. It went through four internal rounds and five Kody
review rounds. Every one of them read the launch path. None of them ran it.

The AC-1 dogfood — an actual in-app launch against an isolated instance — found in one sitting that
**no in-app launch had ever worked**. `pi-agent.sh` passed `--project` unconditionally, but that flag
is declared by the `pi-coms-local` extension, not by `pi`. In `named` mode (the wrapper's default and
what the launcher sets) only the local bridge loads, so `pi` exited 1 with `Unknown option:
--project` in under two seconds, every time.

Nothing about that is subtle once observed. It was invisible to review because the flag *exists* when
you check `pi --help` — the shell reads correctly, and the defect only appears when the extension set
is narrowed. Reviewers reading argv construction see a valid flag being passed.

**Rule:** an FRD that changes a launch, spawn, or process-startup path is not reviewable by reading.
Schedule a live run of that path against a disposable instance **before** the first review round, not
after the last one. Treat "we reviewed it N times" as evidence about the code's shape, never about
whether it runs.

## H-13 — The mode that hid the bug was the mode we always tested in

My first manual reproduction *succeeded* and briefly convinced me the wrapper was fine. It succeeded
because I set `PI_AGENT_COMS_MODE=harness-native` — the mode the trio itself runs on, and therefore
the mode reflexively used to test. `harness-native` loads `pi-coms-local`, which supplies the missing
flag. The broken mode was the production default, which no one exercised by hand because no one
launches agents that way by hand.

**Rule:** when a code path branches on a mode, the mode you use for your own tooling is the one that
gets tested and the other is the one that ships broken. Name the modes explicitly in the verification
bar and require argv-level assertions **per mode**, not one passing launch.

## H-14 — A guard whose check scope exceeds its apply scope fails closed on healthy systems

Our QW-3 preflight refuses to launch when the pi-coms-local steer handler is missing. It inspects
five installed copies. The steer patch only ever applied to three — the ones `pi` actually loads. The
two nvm-global copies have never had it and never needed it. So the guard FATALs on a correctly
patched machine and would have blocked every harness-native launch after merge.

This is the run's dominant defect class inverted. Elsewhere we found *evidence that doesn't prove its
claim*; here it is a *check that doesn't match the thing it guards*. Same root: the assertion and the
property drifted apart without either being obviously wrong on its own.

**Rule:** a fail-closed guard must assert over exactly the set its remediation writes to. When the two
sets are computed in different places, they will diverge. Derive them from one expression, or have the
guard verify only what will actually be loaded.

## H-15 — A TUI behind a pipe fails silently; always diagnose through a real pane

Two diagnostic dead-ends cost real time, both from the same cause. Running `pi` with stdout piped
(`| tail`, `> log`) makes it exit 1 and print **nothing** — no error, no usage, empty log. The
failure looks like a hang or an inexplicable exit.

What worked: run under tmux, `set-option -g -w remain-on-exit on` so dead panes stay readable, then
`list-panes -a -F '#{pane_dead_status} #{pane_start_command}'` for the exit code and the exact
command. That last field is what revealed the launcher resolves the wrapper through
`TERM_CONTROL_PI_AGENT_PATH` — so the copy I had patched inside the job worktree was never the copy
being executed, and I had "fixed" nothing.

**Rule:** for TUI-hosted agents, capture from a retained pane, never from a pipe — and confirm the
binary under test is the one the launcher execs before drawing any conclusion from a patch.

# Harvest from CP-5 execution (2026-08-01/02, Forgejo-everywhere)

## H-16 — A needs_lead blocker that doesn't HOLD lets the loop run ahead on a guess

The coder hit a genuine scope decision (retire vs. port a Projects-v2-coupled bulk-repair CLI) and
correctly raised a `needs_lead` blocker file. But while the Lead was getting the operator's decision,
the coder did not wait — it chose *port* on its own and iterated with the verifier through **four**
review rounds. The operator then chose *retire*; the port work was deleted (only its byproducts, a
forge issue-body helper + repoints, survived). Four rounds of coder+verifier effort spent on the
branch the operator rejected.

The blocker was advisory (a file + a ping), not a gate — nothing stopped the loop from proceeding on
the agent's own answer.

**Rule:** a `needs_lead` blocker must HARD-GATE the raising agent — it stops and does no further
implementation on the blocked path until the Lead responds. And the Lead must treat an open blocker as
top-priority latency: every minute it sits open is a minute the loop may spend guessing. Record the
ruling to disk the instant it's made; the agent resumes only from that artifact.

## H-17 — Committing on an inferred idle captures a mid-edit snapshot

Twice the Lead inferred the coder was "done" (no worktree writes for a few minutes, tests green) and
committed — but the coder was still editing. The commit captured a partial snapshot; the coder's later,
unverified edits landed uncommitted and had to be reverted to keep the branch at the reviewed state.
Reading a file while the coder edits it likewise returns inconsistent snapshots within one turn.

Idleness is not doneness. An agent between tool calls, or mid-multi-part fix, looks identical to a
finished one from the outside.

**Rule:** commit only on an explicit "done, nothing further" signal from the implementer (completed
handoff + ping), never on an inferred idle. If you must bypass the handoff, capture the exact reviewed
manifest/SHA and diff against it before committing, and re-confirm no writes over a longer settle
window.

## H-18 — Context exhaustion, not laziness, drives "stops mid-task"; renew at a clean boundary

The coder repeatedly finished the substantive work then stopped before the closing ritual, and once
left a multi-part fix half-applied (module deleted, its importer left broken). The common cause was
context pressure: found at 86% self-reporting "couldn't finish this turn," and later proactively
pausing at ~78% before a slice. Renewal is enabled but does not fire mid-task. What worked every time:
the operator clears/renews the pane to fresh context at a clean checkpoint boundary, and the Lead
re-briefs off a disk resume-doc stating done-vs-remaining. Clearing context does not touch the git
worktree, so uncommitted work survives — but a truncated agent can leave the tree half-broken, so
re-verify disk state before steering the fresh agent.

**Rule:** watch `context_used_pct`; renew proactively at a checkpoint boundary before ~75-80% rather
than fighting truncation. Keep the loop drivable off durable disk artifacts so any agent can be
renewed and resumed with zero conversational memory. A fresh/renewed agent reliably idles after its
first steer — expect to send a second, action-forcing steer with a ~150s start-confirmation.

## H-19 — A green suite and a clean grep do not prove a migration; the defects live on the adversarial edges

Every CP-5 slice passed its own test suite and a forbidden-token grep, yet every slice's first review
round surfaced real defects the suite never touched: a label-alias filter that silently dropped board
issues, a per-op backend override that routed a "forgejo-pinned" read back to GitHub, an N+1 detail
fan-out where one 503 aborted the whole board refresh, a merged PR normalized to `closed`, verified
readback deleted so destructive teardown could run on an unverified close, an evidence write that could
still throw, dead config left behind, and a `ValueError` escaping the callers' `ForgeIssueUnavailable`
contract. None showed up green.

**Rule:** for a backend migration, "tests pass + grep clean" is a floor, not proof. The bugs live where
the happy path doesn't go: backend/override selection, alias/label normalization, failure injection on
every remote call, boundary state (merged-vs-closed, empty, truncated), and destructive-action
preconditions. Require adversarial probes on those edges, each with a mutation-sensitive regression, or
the slice is not done.

## H-20 — Partial backend-pinning: pin the target at EVERY adapter construction, reads and writes

Twice the same defect: the coder forced the Forgejo backend on the write path but left a read path on
the unpinned global default, where a higher-precedence per-operation/per-lane override could route the
call back to GitHub — defeating the zero-GitHub invariant even though the module grep was clean. The
write was obvious; the read was forgotten.

**Rule:** a "pin the backend" migration must strip per-operation and per-lane selectors and force the
target at *every* adapter-construction site in the concern — reads, writes, readbacks, health. Derive
it from one `forced_config()` and grep the whole concern for adapter construction, not just the write
you were thinking about. Prove it with a probe that sets global + per-op + per-lane all to the old
backend and asserts the new one still wins.

## H-21 — A port that drops a pre-existing safety behavior is a latent regression

The closeout adapter port silently removed three behaviors that weren't obviously part of "routing":
the verified readback that gates destructive worktree teardown (so teardown could run on a
success-shaped-but-unverified close), the PRD body status stamp, and the injected lifecycle runner
seam. Each was a real safety property the pre-migration code had, dropped because it looked
GitHub-shaped.

**Rule:** before porting a path, enumerate its existing behaviors — safety checks, evidence writes,
ordering guarantees, destructive-action preconditions — and preserve each through the new backend.
"Routing not building" does not license deleting a guard; a diff that removes a check must justify why
the property no longer needs to hold.

## H-22 — Size each slice to one context turn; keep slices sequential under a thorough verifier

Two process costs. A slice large enough to exhaust the coder's context mid-work forces a
truncate-then-renew cycle; splitting the oversized slice (D into D + D2) at a clean file seam avoided
it. And an early attempt to run two slices in parallel (coder on the next while the verifier reviewed
the last) backfired: with an adversarial verifier, rev-1 almost always fails, so the "next" work
interleaves with fix work on the failed slice and the coder can't do both.

**Rule:** scope each slice to comfortably fit one agent's context turn, splitting at disjoint-file seams
when it won't. Keep slices sequential when rev-1 failure is the norm — the verifier's thoroughness is
the throughput bottleneck, and parallel slices just tangle fixes with new work.

## H-23 — A verification gate must reference only roles the team template includes

The verifier's process gates its final bug-check on a "Steward hygiene review." Our operating team
template for this run is the 4-agent trio — Lead / Coder / Verifier / Git-Manager — with no `steward`
peer. So at the end of a bounded slice the verifier dead-ended: it could not run the gate, and escalated
to the Lead to "launch a Steward." The Lead waived it for the slice, but that is an ad-hoc patch, not a
fix.

The gate and the team roster were authored in different places and drifted — the same failure shape as
H-14 (a check whose scope exceeds what it guards), here at the workflow level rather than the code
level.

**Rule:** every role a verification gate depends on must be declared by the team template that runs it,
or the gate must be conditional on that role being present. When assembling a team, resolve each agent's
process gates against the roster up front. Either add the Steward to the trio template, or make the
Steward hygiene gate conditional/removed in the Verifier priming — do not rely on per-slice waivers.

## H-24 — Lead-verification is a smoke check, not a substitute for the verifier's adversarial probes

Believing the verifier was stuck, the Lead "Lead-verified" Slice E green by running the suite and
grepping for a test *named* for the required behavior (`'admits a submitted pull review'`), then
recommended committing on Lead-verification — which the operator approved. The verifier (not stuck,
just slow) returned FAIL: that test served its fixture from the inline `/comments` feed and never
exercised `/pulls/<n>/reviews`, so the required ingestion was still absent and unpaginated. The commit
would have shipped a regression AND clobbered the verifier's real verdict; only a failed file-write
(the verifier had already written the verdict file) plus the operator relaying it prevented that.

**Rule:** the Lead running the suite and reading test names is a smoke check, not verification — a test
named for a behavior can fail to exercise it. Never substitute Lead smoke-checks for the verifier's
adversarial probes. If the verifier is genuinely unavailable, reproduce its probes (assert the actual
request was issued / the later page imported), never grep for a reassuring name. And never overwrite a
verifier artifact without reading it first.

## H-25 — Don't misdiagnose a slow, coms-blocked verifier as stuck

The Lead concluded the verifier pane was "stuck across two renewals" and nearly bypassed it. It was
neither stuck nor idle — it was running a thorough ~10-minute adversarial review whose probe artifacts
went to `/tmp/agentops/...` (not the git worktree), while a coms head-of-line jam (an unackable
dead-session message) suppressed its pings. The Lead's watchers keyed on worktree-mtime plus a
150-170s "not engaging" threshold, so an active-but-slow verifier writing to `/tmp` read as idle.

**Rule:** a thorough adversarial review can take 10+ minutes, emit no worktree changes, and (under a
coms jam) send no ping. Before declaring a reviewer stuck: give it review-scale time, watch its
probe/scratch location (`/tmp/agentops`) as an activity signal — not just the worktree — and confirm
the pane directly. Idle thresholds tuned for the coder mis-fire on the verifier.

## H-26 — "Find issues" is an unbounded question; verify against criteria plus a machine gate

Slice B took nine review rounds. Rounds 7-9 each found something real, so the loop was not noise — but
an open-ended "find issues" prompt has no termination condition: a model samples a different subset each
pass, and every fix applied to a large diff seeds the next round's findings. The rounds only stopped when
the Lead changed the question.

**Rule:** the reviewer answers one bounded question — *does this checkpoint meet its stated acceptance
criteria, and does its deterministic gate pass?* Everything else is an advisory that never blocks. Pair it
with (a) a finding blocks only with a repro or failing test, (b) a hard round cap, after which the outcome
is a **spec or coverage failure** to be escalated, not another coding round. First checkpoint under the new
rules converged in one round versus nine.

## H-27 — A guard that is correct but unreachable is the expensive bug class

Slice B's ownership rule was verified correct by unit tests while three separate routes never called it:
`/launch` returned early when the worktree already existed, completed-work Browser-QA called
`startLaunchGroup` directly, and the scoped-path arm returned before checking anything. Two projects were
granted the same worktree, and an HTTP probe launched both into it with 200/200. Every unit test passed
throughout.

**Rule:** treat *reachability* as a first-class property, separate from correctness. When a rule protects a
resource, enumerate every route that can reach that resource and prove each one passes the guard —
end-to-end, not by unit test. Ask "what calls this?" before "is this right?". A one-line early return is
enough to make a perfect guard decorative.

## H-28 — Never accept "that failure is pre-existing" without proving it at the baseline

A checkpoint reported "zero dirty-only failures" against a baseline sampled in the same session. An
independent run found two real branch-only regressions. The suite is flaky: one sampling produced 25
failures, another 23, and a failure present in both noisy sets reads as pre-existing when it is not. The
same rule later caught a silently weakened input-validation guard that focused tests missed entirely.

**Rule:** compare the full suite on the branch against the **merge-base**, with the baseline computed once
and **cached by merge-base SHA** so every comparison uses the same reference. Re-sampling the baseline per
round hides regressions. Target zero branch-only failures, and treat any "pre-existing" claim without a
baseline run as unevidenced.

## H-29 — For suites with known-red tests, gate on baseline parity, not zero failures

This repo carries ~23 environment-dependent failures (no sandbox binary, tests reaching a live forge).
A gate demanding zero would be permanently red and therefore ignored — the worst possible state for a
gate.

**Rule:** make the gate per-suite. Zero-failure for suites that are genuinely clean; **baseline parity**
("no failure exists that the merge-base lacks") for suites that are not. A gate is only useful if green is
achievable and red always means something.

## H-30 — Shared agents need per-process temp files and non-silent stops

Two defects with one root: several agents share one worktree. (a) The gate wrote to fixed `/tmp` paths, so
concurrent runs raced and produced phantom failures — a reviewer diagnosed this independently. (b) The
git-manager fail-closed on a contradictory instruction and went idle **without reporting**, which is
indistinguishable from success; it cost two re-steers and an unfair "it did nothing" entry in the record.

**Rule:** any tool an agent may run concurrently uses per-process temp files, and shared caches are written
via temp-then-rename so a concurrent reader never sees a half-written file. And make silence a violation:
an agent that stops must name the rule and condition in the same turn, and must write its report before
going idle. Also scope fail-closed rules so they cannot block their own bootstrap — "missing manifest" must
not prevent creating the first manifest.

## H-31 — Model-family diversity is an invariant, and the transport differs per family

Moving the verifier off the coder's model family (GPT → Claude) is what caught the unreachable-guard class.
But the swap surfaced three transport facts: pi's `anthropic` provider uses the API (which can be out of
quota while the *subscription* is fine — route via the Claude CLI instead); `agentops-steer` only speaks the
pi extension's socket protocol and returns `nack: malformed envelope` against a Claude pane; and a Claude
pane is **turn-based**, so it never sees a queued coms message until it calls a coms tool — the sender sees
`pending` forever and it looks like a transport fault.

**Rule:** keep reviewer and implementer in different model families, and treat the coms transport as
family-specific. Claude peers need `coms_send` (not steer), a kickoff turn to start awaiting, and an
instruction to re-await after every reply. Verify a provider by making a **live call**, not by confirming
the model name resolves — auth, quota and routing all fail after the name check passes.

## H-32 — "Pre-existing" must be proved against the MERGE-BASE, not against your own branch's earlier commit

The Lead claimed two suite failures were pre-existing, having stashed the checkpoint's work and re-run at
`04d1b4b`. But `04d1b4b` was that branch's own earlier head (Slice A), already containing the change under
suspicion. It proved only "not introduced by this checkpoint's *fix round*". Against the true merge-base
(`d3a8aec`) one of the two was absent — a genuine Slice A regression that had already shipped in a PR and
was about to be merged. This is the same rule the Lead had spent the day enforcing on everyone else,
applied against the wrong commit.

**Rule:** a "pre-existing" claim names a specific commit, and that commit must be the **merge-base with the
target branch** — never HEAD~n, never a previous checkpoint on the same branch. Stacked branches make this
trap easy: every lower checkpoint looks like "baseline" from above. Encode the baseline commit in the gate
so it cannot be chosen ad hoc, and treat any prose "pre-existing" claim without that commit id as unproven.

## H-33 — Put the gate at the BOTTOM of a stack; a branch without a gate is where regressions enter

`scripts/verify.sh` was committed on cp2, so cp1 — the bottom of the stack, and the first to merge — had no
gate at all. Consequences, all on cp1: three fix rounds lost to untouched-but-affected test files nobody
ran, and a real regression (`pipeline refresh queue…`) that shipped in the PR and survived both Kody review
and verifier approval.

**Rule:** verification tooling belongs at the base of a stack (or on `main`) before any checkpoint builds on
it. A checkpoint that cannot run the gate cannot be verified, only spot-checked — and spot-checks miss the
files a change *affects* rather than *touches*. If tooling must be introduced mid-stack, rebase it to the
bottom rather than leaving lower branches ungated.

## H-34 — A reviewer's finding is a claim, not a fact; verify it before routing

The verifier reported a CRITICAL as "byte-for-byte unchanged since round 1" with a reproducing probe. Reading
the file showed the fix present and correct — a live owner returned before the mtime path. Its probe was
creating a lock with no readable owner record, so the fallback fired legitimately; re-run with a proper owner
record it returned `TIMEOUT_NO_RECLAIM`. Had the Lead routed the report as received, the next step was
reverting a correct concurrency fix and deferring the work.

**Rule:** the same evidence standard applies to the reviewer. Before acting on a finding — especially one
proposing to revert or redesign — read the code it names and check the repro actually reproduces the stated
scenario. Adversarial review earns trust by being checkable, not by being trusted. And when a report's
machine summary (`open_findings`, criteria table) disagrees with its body, the body wins: a lead acting on
the summary routed *around* a CRITICAL for two full rounds because it was marked "met" above and described
below.

## H-35 — In a stack, a finding on a lower PR may already be fixed above it

Kody flagged the sidebar empty-string fallback on cp1. The suggested fix was verbatim what cp2 had already
implemented. The finding was correct *for cp1 in isolation* — reviewers see each PR as of its own commit —
but routing it would have had the coder re-implement finished work and then hit a conflict on restack.

**Rule:** triage in a stack asks "is this still true at the stack tip?" before "is this real?". Findings on
lower PRs are evaluated against the tip, and the residual risk (the lower PR briefly carrying the bug on
`main` before the upper merges) is accepted explicitly and kept short by merging bottom-up promptly — not
by duplicating the fix downward.

## H-36 — A single-run baseline manufactures false regressions as easily as it hides real ones

The gate caches one full-suite run at the merge-base as "the baseline". A timing-sensitive test happened to
pass in that run, so when it later failed it was classified branch-only — and the Lead escalated it as a
regression introduced by an already-merged checkpoint, blocking a merge and dispatching a fix. The coder
disproved it by running the test directly at the merge-base in a detached worktree: it fails there 3/3.
Worse, the test's outcome depends on execution context — it fails in isolation at the merge-base but passed
there under full-suite load.

This is the mirror of H-28. There, re-sampling a noisy baseline every round *hid* real regressions; here, a
single lucky sample *invented* one. Both come from treating one observation of a flaky suite as ground truth.

**Rule:** a baseline must distinguish *stably failing*, *stably passing*, and *flaky*. Compute it from
repeated runs (or record per-test pass rates) and classify a test as flaky rather than forcing it into
pass/fail. A branch-only failure is only evidence of a regression when the test is stably green at the
merge-base — otherwise the correct verdict is "unreliable test", tracked separately, never a merge blocker.
And before escalating any branch-only failure, reproduce it at the merge-base *directly*, in isolation and
under suite load; the cached list is an index, not proof.

## H-37 — A wrong repro is worse than no repro, and the Lead is the likeliest source of one

The Lead recorded on a tracked issue that a flaky test "fails 3/3 in isolation at the merge-base". The
verifier refused to take it on trust and re-derived it: isolated at the merge-base the test **passes
10/10**. It fails only under full-suite concurrency — and it fails that way at the merge-base too, which
is the fact that actually proves it is not a branch regression. The bottom line ("don't block") was right;
the evidence attached to it was wrong in a way that would have actively misled the next person, who would
have run the test alone, seen it pass, and concluded it was fixed.

Two things went wrong. First, the Lead compressed "I ran the suite 3 times" into "3/3 in isolation" —
a summary that quietly changed the claim. Second, that summary was written into durable artifacts (issue
#404 and project memory) where it outlives the session and is read as ground truth by agents who cannot
cheaply re-derive it.

**Rules:**
1. Evidence written to a durable artifact must state the exact invocation used. "Fails 3/3" is not
   evidence; "fails under `npm test` (full suite) at `d3a8aec`, passes 10/10 when run alone" is.
2. For any flaky-test note, record the repro that **does not** work as prominently as the one that does.
   "Do not try to reproduce this alone — it will pass" is the single most useful line on issue #404.
3. The reviewer must re-derive the Lead's evidence, not just the coder's. The Lead's claims arrive with
   authority and no diff attached, which makes them the least-checked and most-trusted input in the loop.
   This verifier caught it because its skill says to reproduce independently rather than accept a premise —
   that instruction earned its keep here.

## H-38 — Fail-closed on bookkeeping is only safe if someone is guaranteed to reconcile it

The git-manager refused to commit approved work because its stack manifest recorded stale heads for two
branches (the Lead had advanced them without updating the file) and had no entry for a third. It was right
by its own rules and it reported precisely instead of going idle — the behaviour we wanted. But the actual
risk was nil: nothing had diverged, every branch was a fast-forward ahead of its manifest entry, and git
itself was verifiable ground truth sitting right there.

The stop cost a full round-trip and, in an unattended run, would have stalled the checkpoint indefinitely —
directly against the product goal of "click an FRD, everything runs to merged PR on its own."

**Rule:** distinguish *contradiction* from *drift*. If the manifest entry is an **ancestor** of the current
branch head, that is drift — reconcile it automatically, log the reconciliation, and proceed. Stop only for
genuine contradiction: a manifest head that is **not** an ancestor of the branch (history was rewritten),
a parent relationship that disagrees with the real merge-base, or a missing entry for a branch being
**rewritten** rather than merely extended. A guard that halts on recoverable bookkeeping trains operators
to bypass the guard, which costs more than the guard ever saved.

## H-39 — One unreachable peer can take out the whole outbound channel

The Lead's coms slot allows a single outbound request at a time. A message sent to a verifier process that
was subsequently killed never resolved, and every later send returned `outbound request already in flight`.
The Lead was cut off from all agents for hours and fell back to writing briefs to disk. The slot only
freed once a *new* verifier answered and cleared the queue — recovery by luck, not by design.

**Rules:** an outbound slot needs (a) a timeout that releases it, (b) liveness checking of the target
before enqueueing, so a send to a dead pid fails fast instead of occupying the slot, and (c) an explicit
cancel. Until then, the disk-brief protocol is not a workaround, it is the primary channel — every
delegation must land in a file the recipient can be pointed at, because the message may never arrive.
Related: 168 stale `agentops-native-claude-*` pool directories have accumulated under `/tmp/agentops/coms`,
one per launch, never cleaned up — the same subsystem leaking in a second way.

## H-40 — `git rebase --update-refs` only moves refs *inside* the replayed range

The Lead instructed a single restack of a three-branch stack: check out the top branch and
`git rebase --update-refs <bottom-branch>`, expecting the middle branch's ref to be carried along. It was
not. `--update-refs` rewrites intermediate refs only when they point at commits **within the range being
replayed**. The middle branch had advanced past the point where the top branch forked from it, so its tip
was not in the top branch's ancestry and could not be updated. The result was a top branch containing
*duplicated* copies of the middle branch's early commits while missing its latest two, and a middle branch
still on its original base.

The single-rebase shortcut is only valid when the stack is **strictly linear** — each child's tip is a
descendant of its parent's tip. Once any parent gains commits after its child forked, the shortcut
silently produces a wrong-but-plausible history. Nothing errors; the rebase reports success.

**Rules:**
1. Before restacking, verify linearity per level: `git merge-base --is-ancestor <parent> <child>` for each
   pair. Only if *all* pass is the one-shot `--update-refs` rebase safe.
2. Otherwise restack **bottom-up, one level at a time**, and for each child replay only its own commits
   with an explicit `git rebase --onto <new-parent> <original-fork-point> <child>`. The fork point must be
   recorded, not guessed — after the parent moves it is no longer derivable from `merge-base`.
3. Assert ancestry *and* commit count after every level (`git log --oneline parent..child` should contain
   exactly the child's own work). Ancestry alone would have passed on a branch carrying four duplicated
   commits.
4. The instructing agent owns this failure. The git-manager executed the instruction exactly and its
   post-condition check is the only reason the bad history never reached the remote — post-conditions on
   delegated work catch the delegator's errors, which is precisely when nothing else will.

## H-41 — The checked-out branch is shared mutable state between agents, and no one owns it

The git-manager finished a restack leaving the shared worktree on `cp3`. The Lead then dispatched the
coder to fix a regression "on `cp2`". The coder began work in a worktree that was silently on the wrong
branch. Nothing in the handoff was false — the brief named the branch — but naming a branch in prose does
not put the worktree on it, and the coder had no reason to doubt the checkout it inherited.

This is a whole class of defect that only exists because multiple agents share one working tree. The role
that *changes* the branch (git-manager) is not the role that *depends* on it (coder), and the dependency
is invisible: `git status` looks clean and healthy on the wrong branch.

**Rules:**
1. Every brief that involves file changes must state the expected branch **and** require the recipient to
   assert it (`git rev-parse --abbrev-ref HEAD`) as its first action, before reading or editing anything.
2. The role handing off must leave the worktree on the branch the next role needs, and say in its report
   which branch it left checked out. "Restack complete" is an incomplete report; "restack complete,
   worktree left on cp3" is not.
3. Gate output must record the branch it ran against. A red gate attributed to the wrong branch sends the
   fix to the wrong place — here the gate ran on cp3 while the fix belonged on cp2.
4. Longer term this argues for per-role worktrees rather than a shared one. Sharing a checkout makes
   branch state a race between agents that have no protocol for it.

## H-42 — A regression can hide inside a baseline failure COUNT; only a per-test diff exposes it

The coder reported its checkpoint as "1,524 tests, 19 failed — known baseline categories". The number was
unremarkable against an expected ~18-19, so it read as clean. One of those 19 was a regression the change
itself had introduced: the fix rewrote a call site that an unrelated test asserted as a literal source
substring, and that test flipped from green to red. It had been failing throughout the coder's own
full-suite run and was never noticed, because a count cannot distinguish "the same N failures" from "N
failures with one swapped out for a new one".

Baseline-parity gating is the right answer to a suite with known-red tests (see H-28, H-36), but parity
must be computed over the **set of failing test names**, never the cardinality. Identical counts with
different members is precisely the case that looks safest and is most dangerous.

**Rules:**
1. Handoffs report the failing test **list**, not the count. A count is not evidence of parity.
2. The gate diffs baseline and branch failure sets by name and prints added/removed separately. "Same
   number of failures" must never render as green.
3. Reviewers re-derive the diff rather than trusting the summary — this one surfaced only because the
   verifier ran the full suite itself and compared members.

## H-43 — Source-text assertions create invisible cross-file coupling

Several frontend tests in this repo assert on literal source substrings (no hook-render harness exists, so
this is a deliberate, reasonable pattern). It has a failure mode nobody had articulated: a test in file A
can assert a literal from file B's call site, with **no compiler-enforced link between them**. Changing
that call site — a correct, well-tested change — silently breaks a test in a file the change never
touched, and reviewing the diff of changed files cannot reveal it. Only a full-suite run does.

Note the two opposite risks of the same technique: the obvious one is that matched text survives while the
behaviour breaks (a false pass). The one that actually fired here is the inverse — correct behaviour, text
changed, unrelated test broken (a false fail, in a distant file).

**Rules:**
1. Before changing any line that a structural test might match, `grep -rn '<literal>' tests/` across the
   whole suite, not just the tests being edited.
2. When a source-text assertion is the only feasible protection, say so explicitly in the handoff and
   state what it does and does not guarantee — the verifier should judge adequacy, not assume it.
3. Prefer asserting on a stable exported symbol or behaviour over call-site wording; wording is the most
   volatile thing in a file and the least meaningful thing to protect.

## H-44 — Post-conditions expire; a stale invariant blocks correct work as effectively as a wrong one

The Lead gave the git-manager four post-conditions to check before pushing, including "`cp2..cp3` must be
exactly 1 commit". That was correct during the *restack* phase, when cp3 carried only its own feature
commit. One phase later, after an approved fix was committed onto cp3, the true count was 2 — and the
Lead had updated the sibling check (`cp1..cp2` from 6 to 7) for precisely that reason while forgetting
this one. The git-manager hit the contradiction, refused to squash or amend a checkpoint to satisfy the
number, and reported. Correct behaviour, and the second time in this run its post-condition check caught a
Lead error.

The failure is that invariants were copied forward between phases as literals. "Exactly N commits" is a
*derived* expectation, not a stable property: it changes every time work is legitimately added.

**Rules:**
1. Express structural post-conditions relationally, not numerically, wherever possible — "cp3 contains its
   own feature commit plus any approved fix commits, and nothing from cp2" survives a phase change;
   "exactly 1 commit" does not.
2. When a numeric expectation is genuinely needed, state what it is derived from and re-derive it at
   dispatch time rather than copying the previous brief's number.
3. An agent that reports a contradiction between its instructions and observed state is doing its job.
   The response is to fix the instruction, never to pressure the agent past the check — the check is the
   only thing standing between a stale brief and a rewritten history.

## H-45 — Comparing timestamps as strings across timezones silently inverts a wait into a no-op

A Lead-authored watcher polled the forge for "has a review completed since I triggered it", comparing the
API's timezone-aware timestamps (`2026-08-05T13:26:02+03:00`) against a cutoff produced by `date -u`
(`2026-08-05T12:50:00`) — as **plain strings**. Lexically the older, offset-bearing timestamp sorts
*after* the newer UTC one, so the check matched immediately and always.

Two failures followed from the one bug, and the second was worse than the first:

1. **Wrong counts.** Findings from earlier rounds were counted as new, producing "24 findings" where the
   real number was unknown. The Lead reported a non-convergent review loop to the operator that had not
   happened.
2. **A wait that never waited.** The same comparison backed a "wait for completion before triggering the
   next" loop. It returned instantly, so three reviews were triggered within six seconds — and because the
   trigger wrapper restarts the review gateway, each trigger killed the review before it. The sequencing
   constraint the loop existed to enforce was silently inverted into the exact behaviour it was written to
   prevent.

**Rules:**
1. Never compare timestamps as strings. Parse to timezone-aware datetimes. Shell `date`/`[[ > ]]`
   comparisons against an API's ISO-8601-with-offset output are a bug, not a shortcut — do the polling in
   a language with real datetime types.
2. A wait-for-condition loop must be tested for the *negative* case: confirm it actually blocks when the
   condition is false. A waiter that returns immediately looks identical to a fast success, and its
   failure only shows up as a downstream race.
3. Sequencing enforced by a poll loop is only as strong as that loop's predicate. When the action being
   sequenced is destructive to its predecessor (here: restarting a shared gateway), an unreliable
   predicate does not degrade to "slower" — it degrades to "destroys the work".
4. Same root cause as H-42: a derived summary value was compared instead of the underlying members. Prefer
   comparing identities (review IDs already seen) over positions in time.

## H-46 — Changing a shared function's failure contract is a breaking change to every caller

A fix made `selectProject()` throw on a non-OK response, replacing an `if (response.ok) reload()` that had
silently done nothing on failure. The calling component was updated correctly: await, restore the control,
rethrow. But a **second** caller elsewhere still invoked it as `void selectProject(...)`. With a throwing
function, `void` does not handle the rejection — so that path gained an unhandled promise rejection it had
never had, *and* still failed silently. The fix removed the defect from one caller and created a new one at
the other.

Adding a `throw` is every bit as breaking as changing a signature, and far more dangerous, because the
compiler says nothing. Nothing fails to build; the damage appears only at runtime, on the error path,
which is the path least likely to be exercised in review.

**Rules:**
1. Changing where a shared function signals failure (throw / return value / silent no-op) requires
   auditing **every** caller in the same change, and each caller's handling belongs in the same diff.
2. Enumerate callers by grepping the repo, not by recalling them — and re-grep after the change, because
   the first sweep is exactly what the author believes is complete.
3. `void somePromise()` is a code smell wherever the callee can reject. It reads as "fire and forget" but
   means "discard the failure".
4. The reviewer must ask "what else calls this?" for any changed failure contract. Here the Lead caught it
   by grepping call sites rather than trusting the handoff's claim that the shared function was checked.

## H-47 — A delayed agent report describes a world that no longer exists

A verifier status arrived describing two checkpoints as awaiting action — one "next actor: git-manager",
one "next actor: coder, round 1 of 2". Both had in fact been fixed, reviewed, committed and **merged**
hours earlier. The report was accurate when written and stale on arrival, and it read exactly like current
status: confident, specific, with file paths and next actors.

Acting on it would have meant re-dispatching merged work, and possibly reopening settled decisions.

**Rules:**
1. Treat any agent report as a *recollection*, not as state. Before acting, confirm against the artifact:
   PR state, merge SHA, file contents, branch ancestry. Ground truth lives in the repo and the forge, never
   in a message.
2. Reports should carry the SHA/PR/revision they describe, so staleness is detectable rather than inferred.
   "cp2-fix approved" is unfalsifiable; "cp2-fix at `e23347f` approved" can be checked in one command.
3. This is the same failure mode as reviewing a stale head (H-45's neighbour): the artifact moved, the
   claim did not. Bind every claim to an identity.

## H-48 — When work moves off-pane, the operator loses the ability to distinguish working from wedged

After the coms outage, verification runs were moved to headless invocations. They worked well and unblocked
the loop. But the operator's mental model of "who is working" comes from watching panes — and the panes
showed an idle coder on `coms_await` and a verifier whose last output was hours old. From outside, a
healthy pipeline mid-review looked identical to a dead one. The operator asked, reasonably, what everything
was waiting for.

**Rules:**
1. Any execution surface that can do real work must report into the same place the operator already
   watches. A headless run that is invisible is indistinguishable from a stall.
2. Status must be derivable from artifacts (process liveness, gate/test activity, report files), not only
   from pane output — and the Lead should be able to answer "what is each agent doing right now" from
   those artifacts in one command.
3. This matters more, not less, as the harness becomes autonomous: CP-7's headless direction makes
   off-pane execution the norm, so observability has to move with it or the operator's only signal becomes
   "the Lead says it's fine".

## H-49 — A one-shot headless agent will happily defer work to a continuation that does not exist

A verifier launched with `claude -p` completed every probe of its review, then ended its turn with: "I'm
now waiting on the long-running gate to finish before writing the final report — I'll pick this back up
automatically when it completes or at the scheduled check-in." There is no check-in. `-p` is a single
turn. The process exited, the report was never written, and roughly forty minutes of correct verification
work was lost — not because it failed, but because it assumed a lifecycle it did not have.

Interactive agents can wait; headless one-shot agents cannot. Nothing in the prompt told it which it was.

**Rules:**
1. A headless prompt must state the execution model explicitly: *you are a single invocation, nothing will
   re-invoke you, produce your artifact before you finish.*
2. Long-running inputs (a full-suite gate) must be resolved **before** the agent is launched and passed in
   as data, or bounded inside the agent's own turn — never left as something it "waits for".
3. The deliverable is the artifact, not the analysis. An agent that verified everything and wrote nothing
   has produced nothing. Say so in the prompt.
4. Detect it: a headless run that exits without its artifact is a distinct failure mode from crashing, and
   both differ from still-running. A watcher must distinguish all three.

## H-50 — `pgrep -f` matches the watcher's own command line, so a liveness check can watch itself

The monitor for that verifier used `pgrep -f "no-mcp.json"` to decide whether it was still alive. The
monitor's own shell command contained that string, so the pattern matched **itself**: liveness was always
true, the death-detection branch never fired, and the "test processes" count was matching the monitor's
own `pgrep` invocation too. It reported "still reviewing (~20min)" and "(~40min)" — twice — while the
subject had been dead for over half an hour. Those reports were relayed to the operator as progress.

This is the second self-matching incident in the same session: earlier, `pkill -f "rereview-chain.py"`
killed the shell running it, because the pattern appeared in that shell's own command line.

**Rules:**
1. Never `pgrep`/`pkill` a pattern that appears in the invoking command. Use `[n]o-mcp.json`-style bracket
   escaping, match on the executable (`pgrep -x claude`) and filter cmdline separately, or exclude `$$`
   and its children explicitly.
2. Sanity-check any liveness predicate against the negative case *before* trusting it — the same rule as
   H-45's wait loops. A liveness check that can never report "dead" is not a liveness check.
3. When a monitor reports progress, that progress must be attributable to the subject: report the
   subject's pid, RSS, and CPU, not merely "a matching process exists". Here 3MB RSS and 0% CPU with a
   `sleep 30` child would have exposed it instantly — and did, once actually inspected.

## H-51 — The Lead can specify a vulnerability, and no amount of careful implementation will catch it

A brief instructed: validate the project's repository "using the project's `forgeBaseUrl` (falling back to
the host's configured forge) and the host token". Both clauses are individually reasonable. Together they
are a credential-disclosure hole: `forgeBaseUrl` is settable by any authenticated admin, so pointing it at
an attacker-controlled origin makes the server hand over `AGENTOPS_FORGE_FORGEJO_TOKEN` in an
`Authorization` header. The coder implemented the brief faithfully. The verifier reviewed against the
brief's criteria and passed it with zero blockers. The external reviewer caught it.

This is categorically different from the other Lead errors in this run (a wrong rebase command, a stale
invariant, a miscounted file list, a self-matching liveness check). Those were **procedural** — the kind a
delegate's pre-flight check catches, and four times it did. This one was **wrong on the merits**, and the
delegates could not catch it, because implementing it correctly *was* their job and the criteria they were
verified against were the flawed ones.

**Rules:**
1. Any brief that combines **caller-controlled input** with an **ambient credential** is a security design
   question, not an implementation detail. Name the trust boundary explicitly in the brief, or do not
   specify the mechanism at all and let the implementer raise it.
2. Verification against the brief cannot detect a bad brief. At least one reviewer must review against the
   *threat model*, not the stated criteria — that is the value an independent external reviewer adds over
   an in-loop verifier, and the argument for keeping both.
3. Ask of every outbound request the design introduces: *who controls this destination, and what
   credentials ride along?* Configurable base URL plus fixed token is the recurring shape.
4. When fixing it, compare **origins** (scheme+host+port), never string prefixes — `forge.example.com`
   as a prefix admits `forge.example.com.evil.tld`, reintroducing the hole inside its own fix.

## H-52 — A config guard fires only at process start, so a bad config is an undetonated mine, and routine automation pulls the trigger

Deploying CP-6 meant fast-forwarding a checkout that two live services import from. Four separate
start-time guards were latent in the new code, and none of them were detectable by reading the running
system: a non-loopback bind now required a token, `--codex-cwd` now rejected a directory inheriting
agent instruction files, the same flag now rejected a directory inside a git checkout, and unrecognised
`--model` args would have been fatal. All four were invisible while the old process kept running.

The dangerous property is not the guards — they are correct. It is that **the fast-forward alone
detonates nothing**, so it looks safe. The trigger was routine automation: the review wrapper restarts
the gateway on every trigger, and the watchdog probes every two minutes. Any lane that advanced that
checkout for unrelated reasons would have taken out code review for every lane, minutes later, with no
causal link visible between the two events.

**Rules:**
1. When code is loaded by a long-running service, treat *updating the source* and *restarting the
   service* as the same deployment event, because something will restart it for you. Enumerate every
   automatic restarter (watchdog, supervisor, wrapper scripts, `Restart=always`) before advancing the
   source.
2. Before deploying, diff the *start-time validation* between the running version and the target
   version, not just the features. `git log -p` over argument parsing and any `return 2` / `sys.exit`
   path is the highest-yield pre-deploy read there is.
3. A guard that fails closed at startup converts a config error into a total outage of that service.
   That is the right design — but it means config must be migrated *before* the code that enforces it,
   never in the same uncoordinated step.
4. Accept that some of this is undiscoverable in advance. Plan the window so the first restart is
   *watched*, with rollback staged, rather than happening at 3am via a watchdog.

## H-53 — Adding authentication turns every unauthenticated health probe into a destructive actuator

The gateway watchdog probed `GET /v1/models` with `curl -sf` and no credentials. The moment the gateway
required a bearer token, that probe returned 401, `-f` reported failure, and the watchdog concluded
"wedged" and restarted a perfectly healthy service — every two minutes, indefinitely. The monitoring
became the outage.

The probe was not wrong when written. It was made wrong by a change somewhere else, and nothing
connected the two. Worse, the failure is self-reinforcing: each restart produces a fresh unauthenticated
401, so the system converges on permanent restart rather than degrading gracefully.

**Rules:**
1. When adding auth to a service, grep for every client of it *including the ones that only look*:
   health checks, watchdogs, dashboards, smoke tests, load balancers. A reader is still a client.
2. A probe whose failure triggers a *remediation action* is not monitoring, it is control. Hold it to
   control-plane standards: it must distinguish "I cannot authenticate" (operator error, do nothing,
   alarm loudly) from "the service is not responding" (act).
3. Never let a probe treat all non-2xx as the condition it remediates. 401/403 in particular mean *the
   probe is broken*, not the subject.
4. Stop the remediator before touching the thing it remediates, and dry-run the probe before re-arming.

## H-54 — Hand-deployed copies drift from a repo that is already correct, and the drift is invisible from either side

Three fixes were applied live under time pressure: authenticate the watchdog probe, repoint the codex
root, add the auth `EnvironmentFile`. All three **already existed in `main`**, better implemented — the
in-repo watchdog even had a real completion probe solving a wedge-detection blind spot that had been
costing review rounds for weeks. The live `/home/hyperbots/ops` copies and the handwritten unit were the
stale artifacts. The repo was authoritative the entire time and nobody could tell.

The cost was not just duplicated effort. It was re-deriving, by hand and under outage pressure, a worse
version of a fix that was sitting in version control, and nearly filing an already-solved problem as a
new gap.

**Rules:**
1. Before hand-fixing a deployed file, diff it against its in-repo template. Always. The question
   "is the thing I am about to write already in `main`?" costs one command and repeatedly pays for itself.
2. Hand-deployed copies of managed artifacts are technical debt with a silent interest rate: every
   incident makes them diverge further, and every managed deploy silently reverts the divergence.
3. A repo that is ahead of production is not "safe because nothing changed" — it is a stack of
   undeployed fixes whose absence is being paid for in incidents.
4. Prefer running the managed installer over hand-patching, even mid-incident, *unless* an identified
   gap makes the render worse. Name the gap; do not hand-patch out of caution alone.

## H-55 — "Worktree" names two different objects, and the destructive reading takes out a peer's uncommitted state

A closeout brief said: *"delete the merged branch — remote, local, and any worktree ref."* The
git-manager read "worktree" as the directory and removed the **shared** worktree while the coder was
working in it. The tracked state survived; `node_modules` did not, because it is untracked and
`git worktree add` does not restore it. That produced a red gate with `tsc: not found`, which then
propagated into a coder handoff as a spurious finding and would have reached the verifier as a phantom
blocker.

Two failure modes compounded: an ambiguous word in the brief, and a shared mutable directory with no
ownership. Extends H-41 — the checked-out *branch* is shared mutable state; so is the working
*directory*, and destroying it costs more.

**Rules:**
1. Write **"delete the branch ref (remote + local)"**. Never "and its worktree". In git the same word
   means a ref and a directory, and only one of those readings is recoverable.
2. Standing rule for any VCS-owning agent: never run `git worktree remove`/`prune` on a path another
   agent occupies. Report a stale worktree and stop. Self-created scratch worktrees are the only ones
   it may remove.
3. Damage assessment beats the incident report. An agent reporting "I destroyed X" and reality can
   disagree in both directions — check `git worktree list`, `git status`, and file mtimes before
   believing either "destroyed" or "fine".
4. Recovery is not complete when tracked files are back. Untracked build state — `node_modules`, venvs,
   caches — is part of a working worktree, and its absence surfaces later as a mysterious gate failure
   rather than an obvious one.

## H-56 — A gate's cache is shared infrastructure across lanes, and a corrupt cache is indistinguishable from a real regression

The Stage 0 baseline-parity cache lives at a single `/tmp/verify-baseline-<sha>.txt` shared by every
worktree on the machine. Concurrent `verify.sh` runs raced on it and left 220 **file paths** where
`not ok` test-description lines belong. The verifier's first gate run went red with 7 "branch-only"
failures that did not exist; only inspecting the cache contents — rather than trusting the red — exposed
it. A forced recompute showed 33 real baseline failures, a proper superset, and the branch clean.

The corruption fails closed here (path strings cannot match test names, so parity fails). That is luck,
not design: the same race with a different interleaving is a cache that is merely *stale*, which fails
**open** and lets a real regression through.

**Rules:**
1. Any cache keyed only by content-SHA is shared across every worktree on the host. Namespace it per
   worktree, or make it content-addressed including its own format version.
2. Atomic *content* writes are not enough. If check-staleness and write are not atomic **across
   processes**, two computations still interleave. Use a lock, or write-once-immutable names.
3. Validate a cache before trusting it. Assert its entries have the shape they should (test names, not
   paths); reject and recompute otherwise. A cache is untrusted input.
4. When a gate goes red, inspect the *evidence the gate used*, not only the diff. The verifier's
   instinct — read the baseline file itself — is the move that separates a real blocker from an
   infrastructure artifact, and a less careful reviewer files a phantom finding and burns a fix round.

## H-57 — Test the workflow belief before redesigning the workflow around it

The operator proposed disabling automatic first-review to stop a final push from burning tokens on an
unwanted review. The premise was checkable in one query: across the two most recent multi-round PRs,
**every** review round was preceded by an explicit trigger comment — zero reviews fired from a push
alone. Cadence was already Manual; the concluding push already cost nothing. The proposed change would
have removed the guarantee that a PR is never silently unreviewed, in exchange for zero savings.

The belief was not foolish — it had been true weeks earlier, before someone changed the setting. That is
the point: workflow beliefs decay silently as configuration drifts under them.

**Rules:**
1. Before redesigning around "the system does X", find the last N occurrences and check whether it did
   X. Event history on the forge answers most of these in one query.
2. Prefer observed behaviour over the configuration field, and over documentation. The behaviour is what
   costs money; the field may not even be where you think it lives (this one was not in the DB record
   that holds the other review settings).
3. When two settings exist to make a safety property and an efficiency property independent, changing
   one to buy the other usually means the split is being misread. Ask what the split was protecting.
4. Re-verify periodically. This behaviour reversed once mid-week already, silently. A belief verified
   two weeks ago is a hypothesis today.

## H-58 — A deployment tool that reports a pin it does not actually use produces a wrong deploy that passes every health check

`install.sh` synced a detached worktree to `origin/main`, printed `pinned to c544362`, and then rendered
its unit templates from `$here` — the directory the script was *invoked from* — rather than from the
`$SOURCE_DIR` it had just pinned. Invoked from a checkout one merge behind, it rendered the **old**
templates while truthfully-but-misleadingly announcing the new pin. The rendered gateway config lost the
`--model`/`--reasoning-effort` flags: exactly the regression the merge it claimed to be pinned to had
just landed to prevent.

The resulting deployment would have been healthy by every observable signal — unit active, auth guard
passing, 401/200 correct, real completions succeeding. The only symptom would have been code review
silently running on the wrong model, invalidating an A/B experiment whose results would still look
valid. It was caught by one manual `grep` of the rendered output before `--apply`.

**Rules:**
1. A tool that reports a version must report the version of **the artifact it actually consumed**. A pin
   describing a different input than the one used is worse than no pin, because it actively buys
   confidence.
2. Never resolve inputs relative to the invocation directory when the tool has already established a
   canonical source. `$here` and `$SOURCE_DIR` disagreeing is a latent wrong-deploy in any tool shaped
   like this — go look for it in the others.
3. Inspect the *rendered artifact* before applying, never just the tool's exit code and log. The one
   grep that mattered took two seconds and was the only thing standing between us and the failure mode
   the entire day's work existed to prevent.
4. Rank deployment defects by **observability of the failure**, not severity of the mechanism. A wrong
   deploy that crashes is cheap; a wrong deploy that serves happily on the wrong configuration is the
   expensive one, and it is the one health checks are structurally unable to catch.

## H-59 — Your own automation is a suspect; run a no-touch control before filing an oscillation bug

An audit log showed a project selection flipping back within 5–75 seconds of every operator switch, all
under one account, repeatedly. It read unmistakably as a rogue writer, and it was filed as a defect with
that framing.

It was the reporter. Browser automation had been clicking that same `<select>`, sending `Down`/`Return`
at it, typing into it, and navigating between two surfaces that each own a writer. Every "unrequested"
PUT was a synthetic event the investigator had generated. Once the automation stopped, the value sat
unchanged for **32.7 minutes with zero PUTs** — the disproof took two minutes and would have prevented
the issue entirely.

The delegate's investigation is what exposed it: told to find the rogue writer, it instead proved no
automatic writer exists (no timer, no page-load assertion, no read of the suspected stale global; page
load performs only GETs), established that both writers fire *only* from UI events carrying the supplied
id, and then **stopped** and asked for `event.isTrusted` before changing code. Synthetic is precisely
what automation produces.

Compounding it, the same session mis-attributed a pushed branch to its own tooling — the branch was six
days old, and one `git log -1` would have shown it. Same error twice in a day: correlation read as
causation because the timing was suggestive.

**Rules:**
1. **For any oscillation or "something keeps undoing X" report, run a no-touch control first**: perform
   the action once, then touch nothing for several minutes and observe. Cheap, decisive, and it belongs
   *before* the issue is filed, not after.
2. When you are driving the system you are investigating, **put your own automation at the top of the
   suspect list**, not the bottom. Synthetic events, retries, and multi-surface navigation all look like
   a rogue actor in an audit log.
3. `event.isTrusted` distinguishes a real user from a script. Any UI-triggered anomaly under automation
   should establish trustedness before anyone edits code.
4. **Timestamp before you attribute.** "I did X and then noticed Y" is not causation. `git log -1`,
   file mtimes, and audit `created_at` are one command each and settle it.
5. A delegate that refuses to confirm your hypothesis is doing its job. The instruction that made this
   work was "report the mechanism before you change behaviour" — without it, a plausible culprit would
   have been fixed and the symptom would have persisted.

## H-60 — Two agents can only disagree about a rule they both own; the fix is to delete one copy, not to correct it

The board rejected valid worktree paths as malformed because `board.html` re-implemented the server's
naming rule as a hand-written suffix test and only knew the legacy form. The server accepted both legacy
and project-scoped names; the client accepted one. Result: the repair wrote a path the server considered
valid, the board called it malformed, and the operator hit a contradictory dead end — *"Launch metadata
is already current … Still missing: Worktree Path malformed"* — with no way forward. Every project using
the newer scoped naming was unlaunchable.

The tempting fix was to widen the literal. That would have been a **third** spelling of the same
contract. The fix taken instead was to delete the client's copy: the generator emits the accepted names
into its data, and the client compares against that, owning no rule at all.

Three further lessons fell out of doing it:
- **A new required field is a deploy hazard.** The client began depending on a field that only exists in
  a *generated* artifact refreshed on a different cadence than the tracked page. A verifier proved with a
  failing test that this converts a scoped-only bug into a **total** launch outage during the window
  where new page meets old data. A labelled legacy-compat branch — old data, old semantics — closed it.
- **A field must survive to the check.** Two functions rebuilt the object before validating it, silently
  dropping the new field, so the fix worked on one path and failed on two others. The acceptance criterion
  ("the client accepts what the server accepts") was satisfied by a test on one path and was still wrong.
- **"It matches exactly" needs the guard compared, not just the body.** A claimed equivalence between two
  copies of a branch rule held for the pattern and failed for the applicability condition.

**Rules:**
1. When two components disagree about a rule, ask which one should not have a copy. Correcting the
   duplicate leaves the duplication — and the next divergence — in place.
2. Resolve derived values **once, at the source that has the authoritative facts**, and pass the answer.
3. Any fix that makes a client depend on a **new** field in a separately-deployed artifact must state what
   happens when that field is absent. Demand the answer before merge; "fails closed, needs a refresh" and
   "silently accepts everything" are both findings.
4. When a fix depends on data reaching a check, enumerate **everything that rebuilds the object in
   between**. This is the question an acceptance criterion phrased as behaviour will not ask for you.
5. Comparing two implementations of a rule means comparing the **guard and the body**. Identical
   predicates under different applicability conditions are not equivalent.

## H-61 — An idle agent, a composing agent, and one with an unsent turn are indistinguishable from outside

Strengthens H-4 ("a queued message is not a work-turn") with three variants observed in a single
session, and one detection rule that H-4 does not give you.

**Variant A — a reply carrying the whole task still schedules nothing.** The Lead answered a coder's
ping via `coms_respond` with the complete assignment: authority path, defect, forbidden shortcut, scope,
required protection. The coder consumed it — 20k tokens in, 5% context — and went idle. The worktree
never changed branch. Delivering content and scheduling a turn are two different operations, and only
the out-of-band steer performed the second.

**Variant B — the agent announced it would wait, then didn't.** The verifier's last line was *"I'll wait
on the coms inbox for the review trigger"* — and then its turn ended without ever calling `coms_await`.
The stated intention and the executed behaviour differed, and the transcript read as if it were waiting.

**Variant C — a composed turn parked in an unsent input box.** The verifier pane had text sitting at the
prompt, typed and never submitted. It had authored a response and not sent it.

C is the one worth internalising. From every external signal — process alive, present in `coms_list`,
pane rendering normally, non-zero CPU — **an agent with an unsent turn looks exactly like an agent that
is thinking**. There is no observable difference between *composing*, *idle*, and *has a half-finished
turn parked in a text box*. The Lead sat waiting on a watcher for a report that could never arrive.

This also meets `trio-coder-idle-before-handoff` from the opposite direction: that note is "finishes the
work, skips the ping"; this is "receives the work, never starts". Same root cause — turn-bound agents
have no scheduler — surfacing at both ends of a task.

**Rules:**
1. **Liveness is not progress.** Never conclude an agent is working from process state, coms
   registration, or a rendering pane. Watch for a change in *work state* — a file written, a branch
   switched, a diff appearing — and make that the monitor's condition.
2. **Check the input line.** `tmux capture-pane` and look at the prompt: text sitting there unsent is a
   parked turn, not activity. Clear it (`send-keys C-u`) before injecting a new instruction, or the two
   concatenate into gibberish.
3. **An agent stating an intention is not the agent doing it.** "I'll wait on coms" and "I am awaiting"
   are different claims. Treat the first as narration.
4. **For a wake design (FRD #391 CP-4):** a wake that assumes the peer is sitting in `coms_await` does
   not cover any of these three states. It must be able to drive a pane that is at a prompt, mid-compose,
   or holding unsent text — otherwise it only fixes the case that was already nearly working.
5. Runtime asymmetry compounds it: pi panes auto-bind and poll; a Claude pane registers in the pool but
   will not listen until given a turn. "Registered" and "listening" are separate properties, and only one
   of them is visible in the roster.

## H-62 — The identifier you talk to a peer with must be the identifier you wake it with

Observed 2026-08-08 while dispatching a final fix round. `coms_list` returns peers by **name**, and
`relay_dispatch`/`coms_send` address by that name. The out-of-band wake does not:

```
$ agentops-steer coder '<task>'
agentops-steer: no socket for session 'coder' under /tmp/agentops/coms/*/sockets/
$ agentops-steer 01KZGAE28XK6B9G3HT45W6WQCS '<task>'
steered 01KZGAE28XK6B9G3HT45W6WQCS.sock (msg 4d30c9f5)
```

Both identifiers refer to the same live agent. The roster never shows a socket, socket filenames are
opaque ULIDs and hashes, and the one identifier a Lead naturally holds — the name — is the one the wake
path rejects.

The cost is not the extra lookup. It is that **the send path and the wake path drift apart**: a hub that
dispatches by name and wakes by id has to carry a private name→session_id mapping and keep it correct
across every peer renewal. When that map goes stale the wake fails while dispatch still appears to work,
which is the worst possible split — the channel that reports success is the one that does nothing (H-4,
H-61).

Same shape as the `relay_cancel` discoverability gap (H-47): the capability exists and works, and is
reachable only by a spelling the caller has no way to guess. The error message names the failed lookup
and not the remedy, at the one moment the stuck caller is guaranteed to be reading.

**Rules:**
1. **One namespace across a peer's whole surface.** Any verb that acts on a peer — dispatch, wake,
   cancel, teardown — should accept whatever identifier the roster hands out. Accepting both is fine;
   accepting only the one the roster does *not* show is not.
2. **A resolver is not a fix, it is the bug deferred.** If a hub must map name→id itself, the mapping
   becomes stale state it has to invalidate on every renewal. Push the resolution down to the verb.
3. **Error text is the documentation people actually read.** "no socket for session 'coder'" should say
   which namespace it wanted. Applies to `relay_cancel`, and to any verb whose remedy is unguessable.
4. **For FRD #391 CP-4:** the wake verb must take the same identifier as CP-3 dispatch, or CP-4 will
   silently be unable to reach peers CP-3 can address.

## H-63 — Correcting a brief on disk does not correct the agent; nothing triggers a re-read

The standing rule "put every delegation on disk, point the agent at the path" (H-14) protects against
agents that compact, crash, or lose context. It does **not** make the file authoritative *over time*.

Observed 2026-08-08 on PR #438 round 7, with exact times:

```
15:40:13  coder commits 81c0f10
15:42:09  Lead corrects the brief on disk, removing a stale "post @modula start-review" instruction
15:51:32  coder writes its handoff — still carrying the stale instruction
```

The correction sat on disk for **nine minutes** before the handoff was written, and had no effect. The
tempting reading — "it read the file too early" — is wrong and matters, because it suggests the fix is
to correct faster. It isn't. The agent had already lifted the instruction into its working context, and
**no event in the loop ever causes a re-read.** A file is consulted when an agent decides to consult it,
which for a brief is once, at the start.

The Lead had also countermanded directly over the wake channel at 15:44, which *did* land — the
git-manager did not post the trigger. So the two channels behaved oppositely: the durable one silently
went stale, the ephemeral one worked.

This is the mirror image of the failure H-14 was written to prevent. Both are true at once: the file
survives the agent's memory, and the agent's memory ignores changes to the file. Neither channel alone
is sufficient.

**Rules:**
1. **A correction is a message, not an edit.** Editing the brief is bookkeeping for the *next* reader.
   To change what a running agent does, you must send it — over whatever channel actually schedules a
   turn (H-4, H-61).
2. **Do both, and say which is which.** Edit the file so the record is right, *and* send the correction.
   State in the message that the file changed and what changed, so the agent knows its copy is stale.
3. **Date or version the correction in the file.** A silent in-place edit is indistinguishable from the
   original text to anyone who reads it later, including a verifier reconstructing what was authorised.
4. **Expect stale instructions to resurface in artifacts.** The coder's handoff propagated the withdrawn
   instruction downstream to the git-manager. Read delegate reports for instructions you have already
   revoked — a report is a recollection of the brief as first read.

### H-62 addendum — a context refresh silently invalidates every stored wake handle

Same day, hours after H-62 was written, the operator refreshed the coder's context to free it up. The
roster name stayed put; the session id did not:

```
before   coder  01KZGAE28XK6B9G3HT45W6WQCS
after    coder  01KZH2BDWMNVMDCE1WCH91YP2M
```

The old socket was removed and the new one created, so nothing was broken at the transport layer. But
every wake handle held anywhere else — a Lead's notes, a script, a queued instruction, a monitor's
liveness check — now points at an id that no longer exists, while `coms_list` still cheerfully returns
`coder` as alive. Dispatch keeps working; wake silently does not.

Note the asymmetry: the Claude-runtime verifier kept its session id through the same operation
(`6fde906e...` unchanged). So whether a refresh rotates your identity is **runtime-dependent** — a hub
cannot even assume the rule is uniform across its own peers.

This is the failure H-62 rule 2 predicted ("a resolver is not a fix, it is the bug deferred; the mapping
becomes stale state it has to invalidate on every renewal"), arriving faster than expected. Renewal is
not a rare event — it is routine context hygiene, and it happens *more* often to the agents doing the
most work.

**Additional rules:**
5. **Never persist a session id.** Resolve name → id at the moment of use, or address by name and let the
   verb resolve. Anything stored is stale from the next renewal onward.
6. **A liveness check keyed on a session id reports death on renewal.** Monitors must key on the peer
   *name*, or they will cry wolf every time an agent is refreshed — and a watcher that false-alarms is
   one the operator learns to ignore.
7. **For FRD #391 CP-5:** renewal must publish an identity-change event, or every peer holding a handle
   is silently broken with no way to learn it. The registry knows; nothing else does.

## H-64 — Ask of every check: "if the thing I fear were true right now, would this fire?"

Three times in one session on PR #471 I built a check that could report success and could not report the
specific failure I was watching for. Each looked like a working check until the failure it was blind to
actually occurred.

**1. A findings monitor keyed on new IDs.** It emitted a Kody finding only if its id exceeded the last
seen. An **unfixed** finding keeps the same id forever, so it never re-fires — and silence read as
"clean". It reported clean while a high-severity trust regression sat open.

**2. A filter that excluded the finding it was about.** Checking for findings "above #13383" excluded
#13383 itself, which was the open one.

**3. Reading only the latest review.** Kody files **each finding as its own review**, so one commit had
reviews 2551 (#13381) and 2552 (#13383). Reading `reviews[-1]` saw one and missed the other. Correct
form: aggregate comments across **every review whose `commit_id` matches the current head**, and print
how many reviews were consulted so `0 OPEN` is a positive statement rather than an absence of news.

A fourth, milder case: a stall detector keyed on "no commit and no dirty files" fired twice on an agent
that was idle **because it had finished**. It could not distinguish delivered from abandoned, because the
distinguishing fact — whether the pushed head already contained the work — was not an input.

**Rules:**
1. **Before arming any check, name the exact bad state and ask whether the check fires in it.** If you
   cannot describe the firing condition for the failure, you have built a success detector.
2. **Prefer positive assertions over absence.** "0 open findings across 3 reviews of `<sha>`" is a claim.
   "No new findings" is silence, and silence has too many causes.
3. **A monitor that false-alarms gets ignored.** Retire a watcher once the thing it watched is delivered,
   rather than letting it cry wolf — the second false alarm costs more than the watcher saved.
4. **Verify before acting on your own alarm.** Both stall alarms would have made me re-dispatch work that
   was already pushed. Checking the artifact took seconds.

## H-65 — Specify the model, not the instance; a brief can encode the defect

PR #471 took seven review rounds. The code work was consistently correct. **At least four rounds trace to
briefs that named an instance or a scope instead of stating a rule**, and each fix then satisfied the
instance while leaving the class open for the next round to find.

Two examples, both mine:

- **Precondition enumeration.** I gated a call on "valid issue number", then on "issue-scoped worktree",
  then a third round found port bounds. Each gate was correct and incomplete. Replacing all three with
  *attempt, and fall back on any failure* closed the class — and reverting that single try/catch turned
  **three** tests red, which is the measure of how much the enumeration had been missing.
- **Unscoped security rule.** I wrote "restore `--approve` for runtime-less launches" thinking of two
  modes. Applied literally and correctly, it granted auto-approval to three more modes that previously
  made their own trust decision. Two further rounds then found that the same rule permitted unvalidated
  and symlink-escaped workspaces. Stating the invariant once — *trust only a canonically issue-scoped
  path; no trust is a safe outcome* — closed two criticals together.

The failure mode is specific: **verification against the brief cannot detect a defective brief.** A
careful implementer will faithfully build the hole you specified, and every test you asked for will pass.

**Rules:**
1. **State the invariant, then let implementation follow.** If a brief lists conditions, ask whether the
   list is knowable in advance. If it is not, the list is the bug.
2. **When a second round touches the same function, stop patching.** The recurrence is the signal that
   the class was not named.
3. **Any rule touching trust, auth, or scope must state its boundary explicitly** — which modes, which
   paths, which callers. "Restore X for Y" without a boundary will be applied wider than intended, and
   correctly so.
4. **Own it in the brief.** Saying "this was my under-scoped rule, not your error" keeps the agent
   reporting contradictions instead of quietly absorbing them — which is how #13609 reached me as an
   escalation rather than a silent weakening.

## H-66 — Every standstill in this run was a notification failure, not a work failure

Catalogue from a single day on PR #471. In **every** case the work was either done or correctly stopped,
and the run halted anyway because the signal never reached the Lead. Recording them together because the
individual glitches look unrelated and the root cause is one thing.

| # | What happened | How long it cost | How it was actually found |
|---|---|---|---|
| 1 | Coder hit a contradiction in the brief, escalated over coms, went idle awaiting an answer | ~1 hour | Lead read the pane |
| 2 | Coder consumed a steer and produced no work at all | ~1 hour | Lead compared commit time to wall clock |
| 3 | Git-manager stopped correctly on `mergeable:false`, wrote a full disk report, coms ping **rejected — "inbound capacity"** | until the operator pasted it | **The operator noticed** |
| 4 | Verifier cannot be steered at all — `agentops-steer` returns `nack: malformed envelope` for a Claude-runtime pane | permanent | Lead tried twice |
| 5 | Verifier relaunch died instantly because the command was piped through `tee`, so `claude` saw no TTY and demanded `--print` input | ~15 min | Lead captured the wrapper's stderr |

**The unifying fact: the Lead cannot read its own coms inbox.** `relay_poll` polls *outbound* replies by
`msg_id`; there is no non-blocking inbound read. So any protocol in which a delegate reports **to** the
Lead over coms is broken by construction — it works only when the Lead happens to be blocking on
`coms_await`, which a working Lead never is.

Case 3 is the sharpest: the git-manager did everything right. It refused an unsafe merge, wrote a precise
report to disk, and attempted to notify. The **only** failure was the notification, and it was enough to
stall the run indefinitely.

Compounding it: **the Lead's own watchers were success-detectors** (H-64). The watcher was keyed on "PR
becomes merged", so a correct *refusal to merge* matched no condition and was indistinguishable from
still-working. A watcher that cannot fire on "stopped and reported" cannot detect the most likely outcome
of a careful delegate.

**Rules:**
1. **Disk is the channel; coms is a courtesy.** Every delegation names a report path, and the Lead polls
   that path's mtime. Say so in the brief — "if the ping is rejected, the disk report is what matters"
   — so the delegate does not treat a failed ping as a failed handoff.
2. **Every watcher needs a stopped-and-reported condition**, not only a success condition. Watch the
   report file's mtime alongside the success artifact. Ask: *if my delegate stopped correctly right now,
   would anything fire?*
3. **Do not build a protocol that requires the Lead to receive a coms message.** Until inbound is
   readable without blocking, delegate→Lead reporting must be disk-first. (FRD #391 CP-2 is exactly this
   gap; this run is the evidence.)
4. **Never pipe a TTY-dependent wrapper.** `| tee`, `> log`, and `2>&1 |` all make `claude` and similar
   CLIs switch to non-interactive mode and exit. To capture output, use `tmux pipe-pane` after launch,
   not a shell pipe in the launch command.
5. **Nested `tmux attach` fails.** From inside a pane use `tmux switch-client -t <name>`, or
   `TMUX= tmux attach -t <name>`. "can't find session" and "sessions should be nested with care" are
   different errors with different fixes — read which one you got.
