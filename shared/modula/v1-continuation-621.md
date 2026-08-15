# Modula V1 — Session Continuation Brief (plan #621)

_Handoff written 2026-08-15. Give this file's path to the new (Opus) Lead session._

## Session guidance (read before starting)

- **Model:** Opus / GPT-5.6 (Fable weekly quota is exhausted, resets ~2026-08-19). Reserve Opus.
- **Ultracode: selective, not blanket.** The #621 implementation runs through the **product's own
  cohort loop** (launch → context brief → coder/verifier → review → merge) — that IS the dogfood, so
  don't implement via the Workflow tool. Reach for a targeted workflow only where fan-out genuinely
  wins and the app doesn't do it: the cross-surface styling-parity audit (#617), L1 Reviewer FRD
  authoring research (#620), and pre-PR adversarial review passes. Turn ultracode ON for those
  discrete research/design turns, OFF for focused implementation. Blanket ultracode on Opus burns the
  weekly quota fast.
- **#603 live host cutover — do it FIRST, supervised, in a quiet window.** Not a blocker (the review
  server runs fine today on cron), but the thing being cut over IS the review server the lanes depend
  on — so cut it over BEFORE lanes spin up, never mid-flight. It's a gated host mutation (operator
  approval + presence required); run the no-op previews (`--dry-run`,
  `--preview-legacy-cron-retirement`) first, then `--apply` + enable + smoke-test
  (`127.0.0.1:8801/health`, old `@reboot` cron gone, a test push still triggers review), rollback
  ready (`--rollback`). Keep it out of the autonomous lanes. Commands:
  `pipeline-diagram/deploy/REVIEW-SETUP.md` + `INSTALL-ops.md`.

---

## Continuation prompt

You are the Lead engineer continuing the Modula V1 push. Read these first, in order:
- Plan: forge issue #621 (ModulaStack/modulastack on https://forge.modulastack.com) — the 4-day
  V1 execution plan; its body has a "Linked FRDs & follow-ups" index. This is your task list.
- Scope contract: dev-plans/gtm/mvp-scope.md (v1.0 = the governed loop, 8 roles, §9 exclusions —
  do NOT over-scope). Master plan: docs/implementation-plan.md + issue #455 (dual-home).
- New FRD drafts to advance: SP-1 parity #617, Coms Delivery #618, Admin groundwork #619,
  L1 Reviewer #620, Lead fallback #634. Security-hygiene: #622 + #632.

STATE (as of 2026-08-15):
- #603 was the first FRD taken end-to-end IN-PRODUCT (Studio → brief → authoring → FRD approval →
  Context Brief gate → cohort → 4 Kody review rounds → merged 4d575f5). Its live host cutover is
  NOT done — a separate gated operator action (commands in pipeline-diagram/deploy/REVIEW-SETUP.md).
- L2 spine surfaces (#524) are SHIPPED. Phase E is done pending one CP-6 receipt-PR merge.
- Fable quota was exhausted; you are on Opus/GPT-5.6. Reserve Opus — don't blanket-ultracode.

HOW TO WORK (hard-won this session):
- Run each FRD through the PRODUCT's cohort loop (the dogfood), not the Workflow tool. Lane A =
  functionality (start with Coms Delivery #618 — it fixes the peer-coms failures that forced manual
  bridging all of #603). Lane B = styling parity #617. Lane C = FRD authoring.
- Priority #1 is Coms Delivery #618: today every peer handoff dead-ended because coms delivery was
  silently down (#613) and the lead had to bridge via disk artifacts + tmux send-keys. Fix that first.
- Merge discipline: 5-round cap; classify by composition (self-inflicted breakage %), not count.
  "Clean" = review complete AND zero findings anchored to the CURRENT head SHA (check commit_id on
  inline comments — a "success" status is not the same as zero findings).
- Gated closeout chain, in order: API merge (verify .merged) → `git -C
  /mnt/hyperliquid-data/projects/repos/agentops-harness fetch origin` then `merge --ff-only
  origin/main` (NEVER switch that checkout's branch) → merge-base --is-ancestor guard → retire
  cohort panes → worktree remove → branch -d (local) + push origin --delete → POST
  push_mirrors-sync → close the FRD with a receipt.
- Secrets: never print AGENTOPS_SESSION_CREDENTIAL; push over SSH (no token in output); create PRs
  via API (token in header, never echoed). Pass secrets via env, never argv/plaintext git config.
- Watchers: anchor on OBSERVED rows/SHAs, never guessed timestamps. Kody auto-reviews on push
  (~11-13 min); check the automation_execution table in db_kodus_postgres (db kodus_db).
- Keep a task list; arm a watcher on every delegated cohort.

STANDING OPERATOR GATES (do not clear autonomously): FRD approvals, PR merges, the #603 host
cutover, merchant-of-record choice for L4, and the W2 leadHistory sign-off (#391 single-owner).

CARRIED-OVER CLOSEOUT (from the prior session, not yet done):
- Master-plan amendment (dual-update rule): update issue #455 AND docs/implementation-plan.md to
  record L2 (#524) as SHIPPED, mark Phase E done pending the CP-6 receipt PR, and slot the new FRDs
  (#617/#618/#619/#620/#634) into Phase L / their lanes. #455 and the doc are ONE document — touch both.
- L2 run report on #524 (the AC-1 receipt is already posted as comment 16717; a consolidated run
  report + findings ledger is the remaining write-up).

FIRST ACTIONS: rebuild your task list from #621's body; confirm the CP-6 receipt PR / Phase-E
close status; do the master-plan amendment above; then (a) supervise the #603 host cutover if the
operator is present, and (b) start Lane A on Coms Delivery #618 (author to review-ready, then launch
the implementation cohort in-app). Report the plan before launching cohorts.
