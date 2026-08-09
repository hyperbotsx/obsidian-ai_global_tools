# FRD (draft) — Plan Reconciliation: keeping the master PRD and waves current as FRDs land

Status: draft · 2026-07-25 · author: lead (Fable 5) · provisional cut code: **PL6**
Canonical source once filed: the GitHub issue created from this draft. Vault copy: this file.
Owner role: **Planner** (existing page bot) — explicitly *not* a new agent.

## 1. Problem

FRDs enter the system from several places: the in-app planning intake and Studio, GitHub issues created
directly, drafts written as files in a PR, and conversations in other sessions. The master PRD
(`docs/product-prd.md`, 17 sections incl. a §17 Revision log) and the wave/flight plan are supposed to
describe the product's intended shape. Nothing currently reconciles the two.

The Z4 Modula Runner is the worked example: a significant platform capability was designed in another
session, landed as a draft file plus PR (#299) with master-PRD amendments in a second PR (#300), and the
only thing that carried it into the plan was the operator remembering to say so. That is the failure mode —
**silent plan drift**. Its consequences compound: work gets built that the plan does not know about, planned
waves keep pointing at superseded shapes, and the PRD slowly stops describing the product.

The reconciliation loop is intentionally the same shape as the review-fix convergence loop: detect
divergence, classify it, propose a bounded correction, and let a human accept the residual risk.

> **Scope amended 2026-07-25 (any-source).** Widened from FRD-driven reconciliation to *any producer of
> product-implicating change*, adding **design changes** as a fifth discovery source, a **`cosmetic`** drift
> class with an explicit materiality rule, and a separate reverse-direction list (PRD statements with no
> surface = design **work requests**, not amendments). Bilateral role-to-role channels are an explicit
> non-goal — one pipeline, one gate, one audit trail. Canonical detail lives in issue #301.

## 2. Goals

- **Discover** every FRD relevant to a project, whether it originated inside or outside the app.
- **Classify drift** between the FRD set, the master PRD, and the active wave plan.
- **Notify** the operator when new FRDs have landed, through the existing F3 fan-out.
- **Propose** a bounded, attributable master-PRD amendment plus a wave/plan delta — as a proposal, never
  an automatic edit.
- Run on **triggers**: FRD created, on a schedule, N-since-active-plan, and on demand.
- Be **idempotent and non-nagging**: a declined proposal is suppressed and not re-raised unchanged.

## 3. Non-goals

- Not a new agent. This is Planner behaviour, consistent with brief 02 §6 (proposes, flags, never resolves).
- Does not author FRD content (Studio) or approve FRDs (CEO review).
- Does not activate waves — activation stays with the plan engine (PL2).
- Never edits the master PRD without operator approval, and never adjudicates a contradiction itself.
- No cross-project discovery. Discovery is strictly project-bound (house isolation rule).

## 4. Design

### 4.1 FRD registry and reconciliation ledger

A per-project registry keyed by a stable FRD identity (issue number where one exists, else a
content-derived fingerprint for file-only drafts), recording: source, title, status, cut code if assigned,
the PRD sections it claims to touch, linked PRs, and **reconciliation state** — `unreconciled`,
`in-proposal`, `reconciled`, or `suppressed` (with the reason and who declined).

Discovery sources, each project-scoped:

1. **In-app** — planning intake reaching arm-state, and Studio-created FRDs.
2. **GitHub** — issues carrying the house FRD/PRD labels in the project's code home (REST-first; the
   GraphQL pool is a known bottleneck).
3. **Merged PRs** referencing an FRD — the signal that a capability actually *landed*.
4. **Repo and vault drafts** — `dev-plans/drafts/frd-*.md` and the vault mirror. This is the source that
   would have caught Z4.

### 4.2 Drift classes

| Class | Condition | Proposed correction |
|---|---|---|
| **Missing from plan** | FRD exists, absent from the wave plan | Insert into a wave; propose slot/order |
| **Landed, plan stale** | FRD merged, plan still lists it pending | Mark done; re-derive downstream waves |
| **Superseded** | A newer FRD replaces an older one | Mark superseded, link successor |
| **PRD-silent** | FRD adds a capability the PRD does not describe | Amendment adding/extending the relevant sections |
| **PRD-contradiction** | FRD conflicts with an existing PRD statement | **Escalate — never auto-amend.** Route to review as a product decision |

The last class is the important one. "New capability" and "the product changed shape" look similar in a
diff and are completely different decisions; conflating them is how a plan silently rewrites its own intent.

### 4.3 Triggers

- **Event** — an FRD is created or merged (in-app event, or the GitHub webhook already relied upon).
- **Schedule** — a periodic sweep (default daily) catching anything created outside the app.
- **Threshold** — N FRDs since the active plan version. This is the *same watcher* PL3 uses for the replan
  chip; consume it, do not build a second one.
- **On demand** — the operator asks the Planner what has changed.

### 4.4 Proposal and human gate

The Planner posts a **reconciliation proposal** as a structured chat message reusing the PL1
plan-proposal rendering contract, containing three parts:

1. **What landed** — the new/changed FRDs with provenance links.
2. **PRD amendment** — a per-section proposed diff plus a §17 Revision-log entry naming the originating
   FRD, so every amendment is attributable.
3. **Wave delta** — inserts, reorders, done-marks and supersessions against the active plan version;
   approval creates plan v+1 (PL2 semantics), it does not activate anything.

Operator acts: **Approve** · **Modify** (natural language) · **Dismiss** (suppresses that fingerprint with
a recorded reason). Approval is a chat act with receipts, not a confirm-phrase gate.

Notification on a new proposal uses the F3 fan-out already specified for unprompted proposals: chat unread
pulse, a Needs-you card, an Activity entry, and email per the user's notification settings.

### 4.5 Authority

Applying the amendment is **risk acceptance about the product's intended shape**, so it is always an
operator decision — the Planner may propose and must never apply. Mechanical parts (discovery,
classification, drafting the diff, suppression bookkeeping) need no human. This mirrors the decision-tier
model in `frd-review-fix-controller-draft.md`: agents apply declared policy, humans accept residual risk.

## 5. Phasing

- **CP-1** — registry + discovery across all four sources + drift classification, read-only. Surfaces
  "N unreconciled FRDs" with no proposals yet.
- **CP-2** — reconciliation proposal: PRD amendment diff + revision-log entry, Approve/Modify/Dismiss,
  receipts, F3 notification, suppression.
- **CP-3** — wave delta against the active plan version (needs PL2's plan object) + the scheduled and
  threshold triggers wired to PL3's watcher.

## 6. Acceptance

- An FRD created entirely outside the app (file + PR, exactly the Z4 shape) is discovered and surfaced
  within the trigger window.
- Approving a proposal produces a master-PRD amendment whose revision-log entry names the originating FRD,
  plus plan v+1 — and activates nothing.
- Dismissing suppresses that fingerprint; it is not re-raised unless the FRD materially changes.
- A PRD-contradiction is escalated as a product decision and never auto-amended.
- Re-running reconciliation with no new input produces no new proposal (idempotent).
- Discovery never returns an FRD from another project.

## 7. Dependencies and sequencing

Requires PL1 (Planner + proposal rendering — merged), **PL2** (plan object/waves — in flight, #293) and
**PL3** (replan watcher + unprompted-proposal fan-out) for CP-3; F3 for notifications; PL4/PL5 (Studio) for
the in-app discovery source. CP-1 and CP-2 can be built against PL1 alone. Schedule after PL2/PL3.

## 8. Risks / open decisions

- **D-1 — sweep cadence.** Default daily; per-project override. Recommend daily plus event-driven.
- **D-2 — discovery breadth.** The project's code home only, or additional declared repos? Recommend
  code-home only in v1, since project isolation is a hard rule.
- **D-3 — any auto-apply class?** Recommend **none** in v1: even a revision-log-only edit asserts that an
  FRD belongs in the plan.
- **D-4 — contradiction adjudication owner.** Recommend routing to CEO review rather than the Planner.
- **D-5 — cut code.** Provisionally PL6; the operator assigns the real code.
