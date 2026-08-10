---
name: fast-lane
description: "Build a full feature slice end-to-end in one strong-model session: approved FRD in, self-QA'd + regression-tested PR out, review after instead of checkpoints during. Harness-portable: Claude Code (Fable 5 / Opus 5) and Pi running Codex models. The Lean workflow preset Modula will productize. Triggers on: fast lane, fast-lane, build slice, lean build, feature lane, build this feature fast."
---

# Fast Lane — spec in, verified PR out

One session builds one complete FRD slice. Quality lives at the two ends — a sharp spec
before, hard verification after — not in mid-flight checkpoints. No agent team, no coms
choreography, no waiting mid-build. The two human gates that remain: the FRD was approved
before you start, and the merge happens only on the operator's word.

## Model & harness selection (credit-aware)

The lane is harness-portable: the same workflow runs on Claude Code and on Pi driving
Codex models. The operator picks the executor per slice before the session starts:

| Tier | When to use |
|------|-------------|
| Fable 5 (Claude Code) | First run of a new slice *type*, architecture-heavy or novel slices. Credit-limited — spend deliberately, never on repeat patterns. |
| Opus 5 (Claude Code) | Default lane once a slice type has a proven pattern in the codebase to follow. |
| Codex via Pi | Overflow capacity and pattern-repetitive slices; bonus: model diversity against the Kody reviewer. |

Downgrade rule: the first slice of a kind runs on the strongest available tier; repeat
slices of the same shape run one tier down. If a downgraded run needs noticeably more
review rounds than its Fable predecessor, record it in the tracker and move that slice
type back up a tier.

## Preconditions (refuse to start without them)

1. **An approved FRD or slice** with acceptance criteria, ideally prototype-anchored. No
   FRD → stop and say so; building from a conversation is how sloppy code happens.
2. **Grounding read** (the Context Brief function, inlined): the FRD, the prototype anchors
   it cites, CLAUDE.md standards, and any seam/contract docs for the areas touched
   (e.g. docs/runner-seam.md). List the files you own for this slice; if another live lane
   owns one of them, stop and flag the collision.
3. **Fresh worktree + branch** per repo conventions (create-branch / git-town).

## Build loop

- Plan internally; don't emit ceremony. Implement the **entire slice** — feature-complete,
  not a scaffold. Match surrounding code style. KISS rules apply (small functions, flat
  structure, no hardcoded product names).
- Slice too big to land inside ~2 days? Split it and say so — long-lived branches drift
  and rot; small merges keep main green.
- **Protection is not optional.** The dominant agent defect on record is *correct code,
  absent protection*. Every seam you touch gets a regression test in the same diff. Before
  pushing, re-read your own diff and reject it yourself if behavior changed without a test
  pinning it.

## Stacked checkpoints (multi-checkpoint slices)

A slice with several sequential checkpoints lands as a PR stack — never as one big PR,
and never by piling more commits onto an already-proposed branch:

- **Branch per checkpoint.** Finish, verify locally, open the PR, then `git town append`
  a child branch and keep building. Each PR diffs against its parent checkpoint branch,
  so every review covers exactly one checkpoint.
- **In-flight window: default depth 3** — the current value lives in the tracker
  (`docs/fast-lane-pilot.md`) and is tuned from run-log data, not here. Review latency
  (~12 min) vs build time means depth 2-3 captures the whole throughput gain; deeper
  stacks only grow the rework blast radius of an early finding. Window full → stop
  stacking, drain reviews.
- **Stack-stop on contract findings.** A review finding that changes an interface halts
  stacking until resolved — everything above is built on it. Local findings don't stop
  the stack.
- **Batch review fixes; `git town sync` once per batch.** Every child push triggers an
  auto re-review, so per-commit syncing multiplies review rounds for nothing.
- **Merge bottom-up only**, each on the operator's word; children retarget when a parent
  merges — run `git town sync` after each closeout to repair local lineage.

## Verify before you ship (receipts, not claims)

1. **Self-QA in the running app**: launch it, drive the feature in the browser against the
   FRD's prototype anchors, fix what you find. Save evidence (screenshots, notes) to the
   repo's QA/receipt location for the slice.
2. **Quality gate**: run `/gate --ml` (or the repo's gate script); green before push.
3. **Test baseline honesty**: compare failures at the merge-base, not just main.

## Ship

- Open the PR per create-pr conventions. Kody reviews automatically on open and on every
  push — do **not** post trigger comments after ordinary fix pushes.
- Work review findings to clean: fix, push, let the auto round run. Route false positives
  with a reason, never silently.
- **Merge only on the operator's explicit word.** Then standard closeout: update canonical
  main, delete the branch, mirror sync.

## Working the review loop without generating it

A review round costs roughly 12-15 minutes and reviews *whatever the head is now*. Three
rules follow from that, and skipping them is how a five-round slice becomes a twenty-round
one. All three are drawn from modula-runner CP-3, where ~85 of ~110 findings were
self-inflicted rather than first-pass defects.

**One push per batch, not per finding.** Every push starts a round on changed code, so
fixing three findings and pushing means the next round reviews three new edges. Collect a
round's findings, fix them together, run the caller audit below, then push once. While a
round is in flight the head stays still — a loop that never sees a stable head cannot
converge on one.

**Sweep the class, never the instance.** When a finding names a site, ask what class it
belongs to and grep for the rest *in the same fix*:

```
# the function whose contract changed — do all callers handle the new answer?
grep -n "thatFunction(" src/*.ts
# the pattern that was wrong — where else does it appear?
grep -rn "\.catch(() =>" src/
```

Ninety seconds. On CP-3 this was done three times and found 2-3 extra instances each time;
it was skipped five times and each skip cost one to three further rounds when the identical
sibling surfaced. **A fix that lands only on the reported line is half a fix.**

**Cap the rounds at five, then stop patching.** At the cap, classify what has been found
rather than fixing more:

- Findings concentrated in one subsystem, and a rising share of each round being breakage
  from the previous round's fix → the *design* is generating them. Restructure, or narrow
  the promise, or escalate the scope question. Do not write the sixth patch.
- Findings spread thin and shrinking → ordinary tail; keep going.

The cap is a prompt to re-diagnose, not a merge trigger. On CP-3 the signal was unmistakable
at round twelve — 71% of findings in one subsystem, fix-introduces-defect near 1:1 — and
fifteen more rounds were spent before acting on it.

**Prefer properties true by construction over properties verified at runtime.** Most of
CP-3's churn was a runtime check trying to establish something an OS-level mechanism would
have made impossible to violate. When a design can only *detect* what it promises to
*prevent*, that gap is a spec decision, not an implementation detail — see the adjudication
gate in `acceptance-specs`.

## Evidence discipline (inherited from the trio's lead/verifier rules)

- **The deterministic gate runs before judgment, always** — gate failures are findings that
  cost nothing to establish; never argue with them, fix them.
- **Verify against artifacts, not your own recollection**: merge SHAs, PR state, test output,
  file contents. A memory of passing tests is not a passing test.
- **Compare members, never counts.** "Same number of failures as baseline" can hide a
  swapped-in regression — diff the failing test *names* at the merge-base.

## Report (what the operator reviews instead of checkpoints)

Outcome first: what shipped, receipts (QA evidence, gate result, review rounds), the diff's
risky seams called out honestly, and anything deferred. Never suppress a risk flag. The
operator's review target is ~20 minutes: working feature vs prototype + a skim of the seams
you flagged.

**Tracker row (mandatory during the pilot):** append a run entry to
`docs/fast-lane-pilot.md` in the same PR — slice, model + harness, wall-clock, review
rounds, and the honesty fields the scale-up decision depends on. Final numbers (rounds to
clean) land with the last fix push before merge; for stacked slices the **top PR of the
stack** carries the row. A fast-lane run without a tracker row didn't happen.

## Run under /goal (Claude Code only)

Set the completion condition at session start so the run continues autonomously until the
slice is *actually* done — judged by Claude Code's independent evaluator, not by the working
model's own sense of completion. Template:

    /goal FRD slice <id> complete: acceptance criteria met, /gate --ml green, regression
    tests exist for every touched seam and pass, self-QA receipts saved, PR open and the
    advisory review round clean or every finding addressed. Do NOT merge — stop at
    review-clean and report.

Rules for the condition: name **artifacts** (gate output, PR state, test names, receipt
paths), never vibes ("code is good"); always end it before the merge — the merge stays a
human gate. `/goal clear` aborts; the condition survives `--resume` for long lanes.

On Pi/Codex there is no independent evaluator: write the same artifact-based completion
condition into the session prompt at start, and verify each artifact explicitly in the
report — the condition still gates the report even without an evaluator enforcing it.

## Hard boundaries

- No autonomous merge, deploy, or scope growth beyond the FRD.
- One slice per worktree; parallel lanes must have disjoint file ownership.
- This lane is for product features. FRDs that ARE the workflow engine (coms, lead runtime,
  agent lifecycle) run in the trio dogfood lane instead — there, the team is the test.
