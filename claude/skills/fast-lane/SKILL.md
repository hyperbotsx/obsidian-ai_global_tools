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
clean) land with the last fix push before merge. A fast-lane run without a tracker row
didn't happen.

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
