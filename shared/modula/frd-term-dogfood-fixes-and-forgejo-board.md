# FRD — Term fixes (from E0 #355 dogfood) + GitHub→Forgejo board migration

Status: **superseded 2026-07-29** — absorbed into `frd-term-1-fully-functional.md` (Part A defects A1–A6 → its CP-1..CP-4/CP-7; Part B board migration → its CP-5). Kept for the original dogfood evidence.
Previously: draft v1 · 2026-07-29 · owner: Erik + Lead
Origin: hard-won during the live AC-6 dogfood of E0 #355 (CP-6, run on the CP-6 build swapped into the production slot behind app.modulastack.com/Authentik). The dogfood validated the E0 Lead-runtime **plumbing** but could not reach the live **Lead ↔ Coder ↔ Verifier** round-trip because of the Term/launch issues below.

Related: E0 Lead runtime FRD (#355), `frd-agent-comms-contract-draft.md`, `frd-agent-lifecycle-teardown-invariant.md`, `board-regen-github-rate-limit` (agent memory).

## What the dogfood DID validate (context — not defects)
On the live CP-6 build: serves via Authentik + TLS; the **Lead dock renders** (CP-4); `GET /lead/conversations/:projectId/:jobId` → **200**; a Lead message correctly **refuses when there is no live job**; the **launch path** runs (metadata repair → worktree provision → group create → Context-Brief gating); and the CP-6-hardened **`DELETE /groups` fail-closed teardown** executed cleanly on a live group. The E0 code is committed + verifier-approved (9 revisions).

## Part A — Term / launch defects to fix

**A1 — Context-brief agent never spawns from the launch gate (BLOCKER).** A `mode:"context-brief"` launch returns 200 and the group shows `running`, but **no agent process starts**: no tmux session, empty coms pool, `context-brief-state.json` stays `status:"pending"` / `reason:"operator_required"`, and there is **zero spawn activity in the server log** (supervisor is correctly `tmux`). The manual Phase-0 gate → agent-spawn trigger does not fire; `POST /groups/:id/context-brief/continue` only errors `"Project Context Brief artifact is not ready."` (it is the post-brief step). Because implementation launch hard-requires a completed brief (`409 "Project Context Brief metadata is required before coder launch."`), this blocks the entire trio+Lead launch. FIX: make the brief gate actually spawn the brief agent when decision=run/operatorOverride, with a clear API trigger and visible spawn logging; surface spawn failures instead of silently parking `pending`.

**A2 — Launch metadata auto-fix hard-fails on GitHub GraphQL rate-limit.** `Repair metadata` runs `gh project field-list 3 …` (GraphQL). When the shared GraphQL pool is exhausted (observed **5000/5000 used, remaining 0**), it fails with `API rate limit exceeded`, leaving the launch stuck with no graceful degradation or retry. The board's own polling + refresh drains the pool. FIX: cache/back-off GraphQL, degrade gracefully (don't block launch on a metadata cosmetic call), and surface the rate-limit state in the UI. (Part B removes the root cause.)

**A3 — Shared conversation store rejects the whole file on one bad record.** `conversations.json` (prod) had **18 of 44** records with invalid keys (`review-session:` / `review-history:` from the coworker/review feature). `loadConversations` throws `"conversation store is invalid"` for the ENTIRE store on any single invalid record → breaks the coworker/planner page-bot surfaces and floods logs. Pre-existing (not E0). FIX: quarantine/skip malformed records (log + drop) rather than failing the whole store; add a one-time migration/cleanup.

**A4 — "page-bot project is invalid" / "page-bot settings are unavailable" on the Lead dock.** Model-settings load (`pageBotStore`) rejects the project; `pageBotStore` requires a slug-safe `projectId` (`^[a-zA-Z0-9._-]+$`, no slash), so an `owner/repo` id fails. Investigate the projectId resolution path feeding page-bot/lead surfaces (slug vs `owner/repo`) and make it consistent.

**A5 — Dead job sessions with no recovery.** Every existing job showed `status:"error"`, panes `recoverability:"stale"`, `statusReason:"tmux_session_missing"` — sessions die and are unrecoverable, leaving a board full of dead jobs. FIX: session recovery or a clean "dead job" lifecycle + UX (archive/relaunch), so the workspace isn't perpetually red.

**A6 — Browser-automation instability (operational note).** Driving the app via the extension was unreliable (`screenshot` "couldn't determine which page", tab drift, board rows not rendering at some viewports). Not a Term bug per se, but the backend API path proved far more reliable for driving/validation — worth a headless/API test harness for future dogfoods.

## Part B — GitHub → Forgejo board source migration
Today the Term board (launchable FRD list) is **hard-wired to GitHub Projects v2** (`gh api graphql`, `PROJECT_QUERY`/`ITEM_QUERY`) and the launch checks the real GitHub issue for approval (`canonicalPrdApproved`: open + `type:prd` + `status:approved` + `/ceo approved:\s*yes/`). The `forgeBaseUrl` admin field only builds issue links — it does **not** make the board read from Forgejo. Consequences seen in the dogfood: the board can't source FRDs from the forge, and creating a test FRD required un-archiving the (frozen) GitHub mirror.

**Goal:** source the Term board + launch approval from **Forgejo** (`ModulaStack/modulastack`) so FRDs are read from and displayed in the Term, decoupled from GitHub. This also removes the A2 GraphQL rate-limit root cause.
**Scope:** adapt the board reader (project/issue enumeration), the launchable/CEO-approved gate, and `forgeIssueUrl` to the Forgejo API (`AGENTOPS_FORGE_FORGEJO_URL`/token); make the project source configurable (github|forgejo) with forgejo as the target; keep the same label/`ceo approved` contract.

## Acceptance
- A1: launching an approved FRD spawns the context-brief agent (visible tmux/coms + logs), the brief completes, and the trio+Lead launch — a full **Lead ↔ Coder ↔ Verifier** session runs end-to-end with the Lead dock messaging live.
- A2: launch succeeds (or degrades clearly) when the GraphQL pool is exhausted; no silent stuck launches.
- A3: a single malformed conversation record no longer breaks the store or the page-bot surfaces.
- A4: the Lead dock model-settings load succeeds for a real `owner/repo` project.
- A5: dead jobs are recoverable or cleanly archivable; no perpetual error board.
- B: the board lists + launches FRDs sourced from Forgejo; the CEO-approved gate works against forge issues; no GitHub dependency for the board.

## Note
The A1 live round-trip should be re-attempted on a **proper deploy** of the branch (not an ad-hoc process swap) once A1/A2 land — the ad-hoc swap masked the gate/spawn behavior.
