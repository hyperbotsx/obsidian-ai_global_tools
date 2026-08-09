# FRD Modes-1 — Workflow modes: verification granularity as a per-job setting

Status: draft v1 · 2026-08-08 · owner: Erik + Lead · CEO review: **pending**
Canonical FRD source (once approved): a forge issue on `ModulaStack/modulastack`.
Vault working draft: `AI_Global_Tools/shared/modula/frd-workflow-modes-draft.md`.
Harvest: operator direction 2026-08-08 (GTM/build-strategy session): "enable different modes in
the Modula app so we have different ways to run verification loops, more or less granularly."
Dual provenance — dogfood experience (trio coordination tax) + the pricing work (quality presets
as tier gates in `dev-plans/gtm/pricing.md`).

Related: frd-agent-roles-and-team-templates-draft (teams supply the lineup; modes decide what
activates) · frd-review-fix-controller-draft (convergence control = Strict machinery) ·
prototype quality presets (Fast/Lean/Strict/Flagship, Admin → Agents & Models) ·
`claude/skills/fast-lane` (the Lean reference implementation, in production use from 2026-08-08) ·
frd-agent-comms-contract-draft (coms pool — Strict+ dependency, not a Lean dependency).

---

## 1. Problem

Modula currently implies one workflow shape: the fully checkpointed team (lead, coder, verifier,
git manager, stacked checkpoint PRs, coms choreography). Running it for every job imposes maximal
process weight on all work regardless of risk:

1. **Coordination tax is real and documented**: coms transport stalls, coders idling before
   handoff, verifier dead-ends, steer daemons, 20-round review loops (PR #396). For routine
   feature work this tax buys little — the granular loop exists to catch mid-flight drift that a
   stronger single-context builder mostly doesn't produce.
2. **The operator's own build experience** (2026-08-08): full features built one-pass by a strong
   model with review-after shipped in hours, not days, at comparable quality — provided the spec
   was sharp and regression tests were enforced at review.
3. The prototype's **quality presets** (Fast/Lean/Strict/Flagship) exist but only toggle add-ons
   (fusion, KISS gates). They don't answer the real question: *how granular is the verification
   loop for this job?*
4. Risk if unaddressed: users (and we) end up in long loops of granular bug-fixes because the
   product imposes one process weight — the exact failure the operator flagged.

## 2. Proposal

Make **workflow mode a first-class, per-job setting** that selects the *gate topology* — team
shape, in-flight loops, and after-the-fact verification — while a non-negotiable governance floor
stays constant. Reuse the existing preset names; extend their meaning from add-on toggles to
workflow shapes.

| Mode | Team shape | During the build | After the build |
|---|---|---|---|
| **Fast** | one agent | deterministic gate before push | self-QA receipts; advisory review optional |
| **Lean** *(default)* | one strong agent | gate + self-QA in the running app | advisory review rounds to clean + operator outcome review, receipts required |
| **Strict** | coder + verifier (+ git manager) | checkpoint loops, verifier Stage 0/1 per checkpoint | advisory review + operator gate |
| **Flagship** | full team | Strict + fusion arbitration, KISS gates, Ponytail | Strict + everything on |

**The floor (identical in every mode, never configurable):** FRD approved before build · the
deterministic gate green before push · advisory review dismissals need a reason · validation
receipts on the ledger · human merge phrase · no autonomous outward actions. **Modes vary
granularity, never governance.**

## 3. Functional requirements

- **FR-1 Per-job mode at launch.** The New-job modal gains a Mode selector beside the Team
  picker. Admin → project settings holds the per-project default (ships as Lean).
- **FR-2 Mode selects gate topology.** Mode determines which roles from the chosen team template
  actually spawn, whether checkpoint loops run, what the after-build verification requires, and
  which receipts are mandatory. Teams supply the lineup; the mode decides what activates.
- **FR-3 Governance floor is mode-independent.** The floor items above are asserted by the
  system in all modes and are not exposed as configuration anywhere, including Flagship.
- **FR-4 Mode is stamped on everything.** The job record, its receipts, and its closeout carry
  the mode they ran under — auditability first, and later the data that tells users which mode
  fits which work.
- **FR-5 Escalation is a ratchet.** The operator may escalate a running job (Fast→Lean→Strict→
  Flagship) at any point — e.g. a slice proves riskier than planned; escalation spawns the
  missing roles mid-job. De-escalation mid-job is not allowed; finish or restart the job.
- **FR-6 Lean is the recommended default** in copy and defaults, with one-line mode descriptions
  at the selection point ("Strict: checkpoint-verified — for engine and protocol work").
- **FR-7 Mode availability may be tier-gated** (pricing integration): candidate mapping — Fast +
  Lean in Free; Strict + Flagship in Pro+. Decision deferred to the pricing doc; the mechanism
  (entitlement check at job launch) is in scope here.

### Design constraint — the goal loop is Modula's, not the harness's (operator note, 2026-08-08)

Lean's engine mechanic — *completion condition + independent cheap evaluator + auto-continue,
stopping short of the human merge gate* — must be implemented **Modula-side**, so it works with
any backing CLI (Claude Code, Codex, local models). Claude Code's `/goal` is the working
**reference implementation we use during our own build, never a product dependency**: Codex and
other harnesses have no equivalent, and Modula's tri-modal doctrine forbids coupling a core loop
to one vendor's harness. Practically: Modula holds the condition, drives the CLI to another
turn when unmet, and evaluates via any cheap model from the user's own model access.

## 4. Prototype obligations (design lands before code)

- New-job modal: Mode selector with the four modes + one-line descriptions; Lean preselected.
- Job cards / workspace sidebar: a small mode chip per job.
- Admin → Agents & Models: quality presets section reframed as workflow modes; per-project
  default control.
- Escalation affordance on a running job (context menu: "Escalate to Strict…" with confirm).

## 5. Non-goals

- No autonomy expansion — the floor is untouched in every mode.
- No automatic mode selection (the system suggesting a mode from the FRD's risk profile is a
  plausible future FRD, not this one).
- No per-checkpoint mode mixing inside one job; the unit of mode is the job.

## 6. Open questions for CEO review

- Q1 Naming: keep "quality presets" merged into "workflow modes", or run them as two settings?
  (Draft assumes merge: one Mode setting owns both topology and add-ons.)
- Q2 May Fast mode skip the advisory review entirely, or is one round the floor for any merge
  to main? (Draft leans: review is floor for merges; Fast without review is for throwaway work.)
- Q3 Tier mapping for FR-7 — decide alongside the pricing doc.
- Q4 Does escalation preserve worktree state verbatim, or re-baseline from the last green gate?

## 7. Evidence

- Lean reference implementation exists and is in use: `claude/skills/fast-lane` (spec-in /
  review-after contract, evidence discipline inherited from the trio's lead/verifier skills).
- Strict reference implementation is the running trio (pi skills: lead, coder, verifier,
  git-manager) — unchanged by this FRD; it becomes Strict/Flagship's engine.
- Coordination-tax record: coms stall root causes, steer-wake mechanism, idle-coder handoffs,
  PR #396's 20 review rounds — vault + memory, cited in the build-strategy session 2026-08-08.
- Market context: BYO-key competitors ship no comparable governed-granularity dial; this is a
  differentiator the pricing research surfaced as "governance is what people pay for."
