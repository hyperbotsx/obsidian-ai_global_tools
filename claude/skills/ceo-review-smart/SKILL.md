---
name: ceo-review-smart
description: "Intelligence-led CEO PRD review for Evonome. Uses the deterministic 13-question CEO rubric as a baseline checklist but puts the model's own judgment in the driver's seat — reasoning about substance, verifying claims, catching what rules can't, and making the approval call. Keeps a hard non-negotiable safety floor (never approves performing trading/deploy/merge/PR/production-readiness). Triggers on: smart ceo review, intelligent ceo review, deep prd review, ceo review fable, judgment ceo review."
---

# Smart CEO Review (intelligence-led)

A second, judgment-first version of the CEO PRD review. The deterministic baseline (`agentops-harness/src/agentops_harness/ceo_review*.py`) checks the **shape** of a PRD — does it have a "Problem" heading, does it mention "verifier checkpoints", does a phrase appear. This skill does the opposite by default: **you are the reviewer, not the box-ticker.** The rubric is a floor and a checklist you reason *past*; your intelligence is what actually judges the spec and decides approval.

Do not degrade yourself to string-matching. Read the PRD like a thoughtful engineering leader who has to live with the consequences of shipping it.

---

## 1. The hard floor (non-negotiable — never overridden by judgment)

These are not restrictions on how smart the review is; they bound **what an approval is allowed to authorize in the real world.** No amount of PRD quality overrides them.

- **A PRD must never *approve performing* any of:** autonomous PRD approval, PR creation / opening a PR, merge, deploy, production readiness, backtest execution, paper trading, live trading. Describing these as gated, future, or non-goals is fine and expected. A PRD whose text *grants* performing them is **auto-blocked**, however good it is.
- **Human authority boundaries stay intact.** The PRD must preserve explicit human gates for anything outward-facing, irreversible, or money-touching. If it removes a human gate that should exist, block.
- **This review approves SPECS only.** It authorizes no implementation, PR, merge, deploy, trading, or backtest run — ever.

If the floor is violated: stop, state exactly which boundary and where, do not approve. Everything below the floor is yours to judge.

## 2. The baseline rubric (a guideline, not a cage)

Keep these in view as a completeness checklist, but treat each as a prompt for real reasoning, not a yes/no lookup. Weight them by what actually matters for *this* PRD, and add your own questions the rubric doesn't cover.

1. Problem & goal — clear enough to implement, and *is the stated problem actually true*?
2. Non-goals preserve human authority boundaries.
3. Implementation home / worktree / branch clear.
4. Owner / agent label explicit and current.
5. Dependencies & tracker sequencing clear — *and internally consistent* (no cycles, no missing provider).
6. Acceptance criteria specific and testable.
7. Validation plan safe, scoped, runnable.
8. Verifier checkpoints defined for non-trivial work.
9. Project field updates identified without bypassing source of truth.
10. Rollback / recovery clear where mutations are possible.
11. Secrets, raw transcripts, private data protected.
12. Preview / manual verification needed and scoped.
13. Forbidden scope avoided (see §1).

Required sections that must exist (fail-closed if absent — fix or block): **Problem, Goal, Acceptance criteria, Verifier checkpoints.**

## 3. The smart review (this is the actual job)

Go beyond the rubric. For each PRD, reason about — and record your judgment on:

- **Truth of the premise.** The PRD claims a problem with file:line evidence. Spot-check the load-bearing claims against the real code — do they still hold, or has `main` moved / was the claim wrong? A PRD built on a false premise is not approvable, no matter how well-written.
- **Soundness of the approach.** Is this a *good* way to solve the problem? Is there a simpler, safer, or more reuse-first path the PRD missed? Is the scope right-sized — not gold-plated, not too thin to be safe?
- **Internal coherence.** Do the goals, non-goals, phases, and acceptance criteria actually agree with each other? Does the PRD contradict itself anywhere?
- **Cross-PRD reality.** Does this conflict with, duplicate, or silently depend on another PRD? Does a shared contract it touches have a single clear owner? (Consult the playbook / index / any consistency-audit notes if present.)
- **Unaddressed risk.** What could go wrong that the PRD is silent on — data loss, a hidden dependency, a missing rollback, a fail-open hole, a provider assumption?
- **Cross-model implementability.** A *different* model will implement this. Is it concrete enough to execute cold — allowed-paths fence, a way to reproduce the problem, a binary done-check? If not, that's a gap.
- **What's missing.** The rubric can't ask "what isn't here that should be." You can. Name it.

Where you find a gap that is small and safe to close, make the **minimal PRD-body edit** to close it (add the missing section, tighten a boundary, add a repro command) and record what you changed. Where a gap is substantive or you cannot safely resolve it, **flag it and do not approve** — say precisely what must change.

## 4. The approval decision (your judgment, floored by §1)

Approve when — and only when — **your considered judgment** is that the spec is sound, coherent, honestly-scoped, and implementable by another model, **and** the hard floor (§1) is satisfied. This is not "all 13 boxes ticked"; it is "would a thoughtful engineering leader green-light this to build, and stand behind it?"

- Floor violated → **blocked**, regardless of quality.
- Floor satisfied, judgment sound, gaps closed → **approve**.
- Floor satisfied but a real gap remains that you can't safely fix → **flag, not approve**, with the specific required change.

State your reasoning briefly. The point of this skill is that the *reasoning* is the review — not a checklist result.

## 5. Recording approval — set BOTH the label AND the CEO project fields

The board at ops.evono.me reads two signals: the **`status:` label** drives the flowchart status colour (`status:approved` → green), and the **`CEO Approved` project field** drives the per-item "not CEO-approved" flag (`generate.py`). A label-only approval turns the node green but leaves the CEO-Approved flag empty — so **you must set both.** Do all of:

1. **Labels:** remove `status:prd-draft`, add `status:approved` (and the owner `agent:evonome-*` label if missing).
2. **PRD body:** set `PRD status` → Approved and `CEO approved` → today's date.
3. **Project fields — set the canonical CEO-review fields on the PRD's project item(s)** (resolve each field by NAME at runtime via `gh project field-list`; the option/field ids differ per project, so never hardcode them):
   - `Pipeline Status` → `Approved`
   - `PRD Review Status` → `Approved`
   - `CEO Approved` → `Yes`
   - `CEO Approved At` → today's date
   - `CEO Review Notes` → a one-line summary of your verdict
   For each field: if the PRD's project **has** it, set it. If the project **lacks** it (e.g. a minimal board), skip that one, and **report at the end that the CEO fields are missing on that project and should be added** so field-reading surfaces reflect approval. Do not hard-fail the whole approval because one field is absent.
4. **Comment:** post one `### CEO review (smart)` comment with your substantive judgment (not 13 canned answers), any gaps you fixed, and `Approved by intelligence-led CEO review <date>.`
5. **Tracker:** comment the PRD's tracker issue (the `#NNN` named as Tracker in the body) noting approval.

The label is necessary but NOT sufficient — the CEO-review process is defined by the `CEO Approved` field (per `docs/work-management/AGENT_WORKFLOW.md`). Setting the field is what makes the approval real to every downstream reader, not just the flowchart.

## 6. Autonomy & efficiency

- If the operator has said to approve without per-PRD confirmation, **approve as you go** — don't ask each time. Give a one-line result per PRD (#, verdict, any fix made) and a summary table at the end.
- Batch `gh` reads; spot-check code with the file/search tools rather than re-deriving.
- Never let efficiency collapse you back into shape-matching. A fast review that only checked headings is a failed review. The value here is judgment applied at speed, not judgment skipped.

## 7. Relationship to the baseline

The deterministic skill remains the guardrail floor and the completeness checklist. This skill sits **alongside** it: run this when you want an intelligence-led review; the baseline's fail-closed guards (§1) are inherited here as hard limits, everything else is elevated to judgment. If the two ever disagree, the hard floor wins on safety and your judgment wins on quality.
