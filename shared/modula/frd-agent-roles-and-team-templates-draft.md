# FRD Teams-1 — Agent roles as one library + composable team templates

Status: draft v1 · 2026-07-30 · owner: Erik + Lead · CEO review: **pending**
Canonical FRD source (once approved): a forge issue on `ModulaStack/modulastack`.
Vault working draft: `AI_Global_Tools/shared/modula/frd-agent-roles-and-team-templates-draft.md`.
Harvest: formalizes [[trio-workflow-is-modula-product]] — surfaced live on 2026-07-30 when the
operator had to hand-paste a role brief to the coder, verifier, and git-manager every round.

Related: FRD Term-1 (#363, launch reliability / session lifecycle — **this builds on it**) ·
FRD Term-2 (#364) · **FRD Tasks-1 (portable task ledger — the Lead role mandates it, FR-2)** ·
Git Manager agent decision (MW-19) · frd-agent-comms-contract-draft (coms pool) ·
frd-review-fix-controller-draft (decision-authority tiers = role gates) ·
frd-z4-modula-runner-proposal (launcher seam) · #103 agentic co-worker (staffs work via teams).

---

## 1. Problem

The Lead / Coder / Verifier / Git-Manager team we run in the terminal is Modula's reference
workflow, but two things are only half-built:

1. **A role's operating contract is not owned in one place.** Each round the operator re-pastes
   "you are the Coder, no git, report to the Lead…" by hand. The workers *do* already receive a
   system prompt at launch — but from a source that is incomplete (no `lead`, no real
   `git-manager`) and **duplicated** (the app builds role prompts from `rolePrompts.ts`; the CLI
   appends a *different* body from `pi/skills/<role>/SKILL.md`). The two drift: the coder skill
   predates the git-manager split and still tells the coder to commit.
2. **A team is not a first-class thing.** The only multi-role launch is a hardcoded
   coder+verifier plan. There is no Lead pane, no Git-Manager pane, no way to compose an
   arbitrary set of roles, and no named team a person (or the app) can pick and launch. Modula's
   product story is "different teams of agents", but the code can only ever spawn one implicit
   pair.

The result: launching a working team is a manual ritual, and "teams" cannot be a product
surface until roles are a single library and teams are composable data.

## 2. Grounded facts (verified 2026-07-30 on `main`; read-only)

| # | Fact | Evidence |
|---|------|----------|
| GF-1 | Roles are a first-class `AgentRole` union of **19** roles; there is **no `lead`** — the orchestrator is always a human-driven raw `claude`. | `term-control-center/shared/launcher.ts:1`; `agentops-trio-lead` wrapper `exec claude …` with no `--append-system-prompt` |
| GF-2 | The app generates a role's launch prompt from `rolePrompts.ts` (`taskPrompt(role,…)`) plus coms/security overlays. | `term-control-center/server/delegationPrompts.ts:2,22,39` |
| GF-3 | The **same** roles get a **second, independent** system prompt on the CLI path — vault skill files appended by pi-agent. Two sources of truth for one role. | `scripts/agentops/pi-agent.sh:248` (`--append-system-prompt "$skill_file"`); skills at `…/pi/skills/<role>/SKILL.md` |
| GF-4 | The library is incomplete: `git-manager` and `code-reviewer` have **no** SKILL.md (pi-agent uses a one-line inline fallback); `lead` has neither a skill nor a pi-agent role. | `pi-agent.sh:29,50,65`; `…/pi/skills/{git-manager,code-reviewer}/SKILL.md` absent |
| GF-5 | A "team" is not first-class: the only multi-role launch is the **hardcoded** `buildCoderVerifierLaunchPlan` → a coder+verifier(+browser-qa) `SessionGroup`. No lead/git-manager pane, no composition, no named template. | `term-control-center/server/launchGroup.ts:44,152,160,166` |
| GF-6 | Per-role model defaults are already an established pattern → reusable for team seeding (operator decision D3). | `term-control-center/server/pageBotModelSettings.ts:8`; `launchProfiles.ts` per-role profiles |
| GF-7 | Coms pools already isolate a team instance per project/worktree; pool name is parametric. | `agentops-trio*` pools; wrappers honor `PI_AGENT_COMS_PROJECT` (default `agentops-trio`) |
| GF-8 | Coder/verifier skills are already rich (checkpoint loop, Machine-Status verdict); the missing contracts are lead, git-manager, and the coder↔git-manager handoff. | `…/pi/skills/coder/SKILL.md` (111 lines), `…/verifier/SKILL.md` (97 lines) |

## 3. Goals / Non-goals

**Design principle (P-1) — harness-portable behavior.** A role's behavior is backed by durable,
harness-agnostic artifacts and a uniform tool interface, never a single harness's native feature,
so the same role behaves identically on Claude Code, pi, codex, and any future CLI. The portable
task ledger (FRD Tasks-1) is the first instance: even Claude Code agents use our ledger instead of
their built-in to-do, so one improvement reaches the whole fleet.

**Goals**
- G-1 One canonical **role library**: a single per-role definition (identity, operating
  contract, coms discipline, human gates, default model profile, default effort) consumed by
  **both** the app launch path and the CLI/pi-agent path.
- G-2 Complete the roster: add `lead`; give `git-manager` a real definition; reconcile
  coder/verifier with the git-manager split.
- G-3 **Teams as first-class, named, composable templates** — an ordered set of members
  `{role, model, effort, gates}`; the current coder+verifier plan becomes one built-in template.
- G-4 **One-action team launch** (app + CLI) into a coms pool/worktree, each agent auto-oriented
  from its role, so kickstart = one Lead task brief and zero per-worker prompting.
- G-5 Ship **several** teams (implementation quad, planning, review) and let teams be edited.

**Non-goals**
- The per-checkpoint **task** content stays with the Lead/operator (roles are stable; tasks are
  dynamic). This FRD does not automate task authoring.
- Not the coms transport/contract (that is comms-contract / Relay v2).
- Not launch-reliability/session-lifecycle (that is #363 Term-1 — this builds on it).
- Not the runner split (Z4), but team-launch must respect its launcher seam.

## 4. Functional requirements

- **FR-1 — Single role source.** One canonical store per role (id, display, purpose,
  system-prompt body, coms discipline, gates, default model profile, default effort). Both the
  app (`rolePrompts.ts`) and the CLI (pi-agent skill append) resolve the **same body**; kill the
  duplication in GF-3.
- **FR-2 — Add `lead`.** Author the standing Lead orchestrator prompt (the *stable* half of the
  hand-written kickoff: operating model, hub role, checkpoint loop, gates, escalation). Add
  `lead` to `AgentRole` and pi-agent roles; wire `agentops-trio-lead` to inject it via
  `--append-system-prompt`. The Lead prompt **mandates the portable task ledger** (FRD Tasks-1):
  decompose the FRD into the ledger at kickoff, re-read it every turn (compaction-safe), and keep
  it current as verifier verdicts and coder completions arrive.
- **FR-3 — Complete `git-manager`.** Author its definition (VCS ownership, commit-from-intent,
  MW-19 push/merge/force human gates, forge-primary, review-trigger rule); remove the pi-agent
  inline fallback.
- **FR-4 — Reconcile coder/verifier.** Coder: no git, hand a commit-intent to the git-manager,
  and ship a **checked-in** regression guard with every fix ([[correct-code-absent-protection]]).
  Verifier: keep the Machine-Status verdict but report to the **Lead** (never dead-end to the
  coder, per [[trio-lead-hub-reporting-protocol]]).
- **FR-5 — Team template model.** `TeamTemplate = { id, name, description,
  members: [{ role, modelProfileId, effort, gates? }], comsPoolPrefix }`, persisted as data,
  project-scoped ([[agentops-strict-project-isolation]]).
- **FR-6 — Template-driven launch planner.** Replace hardcoded `buildCoderVerifierLaunchPlan`
  with a planner that emits `panes` from `template.members`. Current coder+verifier(+browser-qa)
  becomes the built-in **implementation** template; add **implementation-quad**
  (lead+coder+verifier+git-manager).
- **FR-7 — One-action launch.** App workspace action + CLI (`agentops-team <template> [pool]`)
  launch all members into one pool/worktree, each auto-oriented; operator then briefs only the
  Lead.
- **FR-8 — Per-role model defaults + lazy pool.** Seed each member's model/effort from the
  template (operator decision D3); create the pool lazily (D4).
- **FR-9 — Built-in templates.** implementation, implementation-quad, planning
  (lead+prd-author+codebase-expert+researcher), review (code-reviewer+ceo-reviewer).
- **FR-10 — Gates travel with the role.** Human gates (git-manager push/merge, planner
  plan-mode, browser-qa allowlist) live in the role definition, not re-specified per launch.

## 5. Checkpoints

- **CP-1 — Role library + complete roster.** FR-1..FR-4. Single source of truth; add lead +
  git-manager; reconcile coder/verifier; wire the trio wrappers. **Independent of #363 and
  immediately dogfoodable in the terminal** — after CP-1, a team kickstarts from just the Lead
  task brief.
- **CP-2 — Team-template data model + template-driven planner.** FR-5, FR-6, FR-8, FR-10.
  **Sequenced after #363** (shares `launchGroup.ts` / `launchPlan.ts`).
- **CP-3 — App surfaces.** FR-7 + template/role-model management in settings. In-app dogfood
  (mandatory from this checkpoint). Requires a **prototype pass** (see §8).
- **CP-4 — Built-in team set + dogfood parity.** FR-9; migrate our terminal workflow onto the
  app team-launch so the product path and our path are the same.

## 6. Sequencing / dependencies

- **Builds on #363 (Term-1).** CP-2+ touch the same launch-group/plan files #363 owns, so they
  land **after** #363's launch-group work stabilizes to avoid churn. CP-1 is safe to do now and
  in parallel (vault skills + wrapper only).
- Respect the **Z4 runner seam** — team-launch is a launcher operation that must work under the
  hosted-control-plane / local-runner split.
- Relates to **#103** (the agentic co-worker staffs work by launching a team) and the
  **review-fix controller** (its decision-authority tiers are the role gates in FR-10).

## 7. Open decisions (operator)

- **OD-1** Single-source direction: app role library is source and vault skills are generated
  from it, or vault skills stay source and the app reads them? (Recommend: one vault-backed store
  per CLAUDE.md's "skills live in the vault", with the app reading the same bodies.)
- **OD-2** Team-template storage: per-project data vs global-with-per-project-override.
- **OD-3** Built-in template set for v1.
- **OD-4** Is `lead` always a Claude model, or configurable per template?
- **OD-5** Product noun: "team" vs "squad" vs "crew".

## 8. Prototype reference (mandatory gate)

Launch lives in the workspace (`page-briefs/01-workspace.md`); template/role-model management in
settings (`09-settings.md`); shell in `10-global-shell.md`. **Teams are not yet represented in the
prototype** (`dev-plans/drafts/modula-stack-design-prototype.html`), so CP-3 is gated on a
prototype pass adding the team picker/launch and template-management surfaces
(`prototype-reference-gate-workflow.md`).
