# CP-C planning notes (from grounding + live-flip feasibility, post-CP-B)

Base: branch off fresh origin/main AFTER CP-B (#667) merges. All line numbers are post-CP-B (worktree agentops-l1-620-cpb).

## Accurate post-CP-B map (FRD anchors are stale)
- Bounded loop: `nextStatus`/`hasRepeatedSurvivor`/`survivorReason` in `reviewProvider.ts:77-90`. `hasRepeatedSurvivor = loopCount>=2` (hardcoded 2, :84-86); `survivorReason` literal "Kody finding survived two fix attempts" (:88-90).
- Cap already exists: session has `maxLoopCount` (default 2, `kodyReview.ts:43,61`); brake at `index.ts:785` ALREADY uses `session.maxLoopCount`. **Asymmetry to fix:** brake uses config value, core escalation uses literal 2 — align.
- Fix loop: `kodyFixLoopHandler` `index.ts:779-794`; launches coder+verifier via `newKodyFixGroup`/`kodyFixLaunch` (`index.ts:808-818`) → `startLaunchGroup` (`launchGroup.ts:41`), onVerified callback, groupId persisted to session (`index.ts:787`).
- Never-merged invariant holds: review status enum has no 'merged' (`reviewProvider.ts:4`); `mergeMain.ts` disjoint, never called by the loop. DO NOT couple them.
- Dismiss today is SESSION-level (`kodyStatusHandler` `index.ts:796-799`, routes POST /kody-review/dismiss + /needs-human `index.ts:466-467`). NO per-finding dismiss yet.
- PROTECTED_STATUSES: `reviewProvider.ts:59` (NOT kodyReviewParsing) = session statuses {canceled,dismissed,needs_human,fixing_findings,re_reviewing}. Per-finding no-resurrection is a SEPARATE mechanism: `survivorStatus`/`mergedFinding` `reviewProvider.ts:61-75` — dismissed passes through unchanged (no-resurrection nearly free).
- selectedFindings `kodyReview.ts:79-82`; selectableStatus = unresolved|survived_re_review (`:99-101`). restore = flip dismissed→unresolved.
- Per-finding mutation precedent: `markSelected` `index.ts:820-823` (load→map findings by fingerprint→update({findings})).
- Store: schemaless JSON `kody-reviews.json`, `updateIfRevision` optimistic concurrency (`kodyReviewStore.ts`). NO migration needed for new optional fields.
- Config seam: `kodyReviewConfig.ts` (CP-B added `provider`); add `maxLoopCount` (positiveInt) + `loopMode` enum mirroring `reviewProviderId` parse. Materialized at `index.ts:1934`.
- AdminSettings store `adminConfig.ts:12-28` (persistent per-project) has no review section; contextBriefDefaults.ts:83-88 is the project→org→default precedent.
- Override plumbing: `resolveReviewerProfileId` `launchProfiles.ts:50-53` exists, NO caller. defaultPane('code-reviewer') hardcodes 'pi-claude-opus' `shared/launcher.ts:359`. Must inject server-side (defaultPane is pure shared — can't import the server resolver); mirror briefPane injection (`contextBriefLaunch.ts:24-31` + `adminRoutes.ts:120,127` task injection). Reviewer fallback = claude-first (NOT briefPane's codex fallback).

## Live-flip feasibility (verdict M) — the pivotal finding
- Reusable (S core): `startLaunchGroup` + `newKodyFixGroup` pattern; deterministic artifact path `contextRuntimeDirectory(groupId)/review-findings.json` (`contextRuntime.ts:7`, keyed off persisted `session.groupId`); reserve/replay/owner-nonce lock stack (`kodyReviewStore.ts:34,67` reserve/finalizeIfOwner; `kodyReviewTrigger.ts:9-32` reserve→replay→finalize pattern); `reusableGroup` dedupe `index.ts:876`; collectFindings parse (CP-B done — only readRun's file read missing).
- NEW (the M delta): (1) **standalone review-only launch shape** in `shared/launcher.ts` (code-reviewer only valid appended to full impl pane set `:410-417`; need new mode/pane-set like context-brief — HIGH-RISK shared launch surface); (2) `requestRun` closure (build request from session, startLaunchGroup, persist groupId) — precedent newKodyFixGroup; (3) `readRun` closure (groupId→path→read+parse JSON) — precedent `readContextBriefState` `contextBrief.ts:44`; (4) thread config.provider + BuiltinReviewDeps into sync/import call sites (extend SyncContext `kodyReviewSync.ts:10`); (5) invoke requestReview at initial + post-fix re-review, reserve-guarded. `.requestReview` is UNWIRED for BOTH providers today (Kodus live path is separate triggerKodyReview→completedKodusReview).

## Kody #667 findings → CP-C slice mapping
- #3453 (fixed in CP-B partial): richer readRun completion signal (done-clean vs pending vs FAILED/needs-human) → part of CP-C4 readRun contract.
- #3454 → CP-C5 (default flip: thread provider+deps into sync/import).
- #3455 → override-plumbing slice (resolveReviewerProfileId live caller + project/org).
- #3456 (CRITICAL, partial-mitigated in CP-B): **least-privilege/read-only reviewer pane launch = HARD SECURITY GATE on CP-C4** (the new standalone launch shape must NOT inherit coder-pane bypassPermissions+full tools; treat diff as data; validate schema-bound output outside model — normalize/sanitize already do part).
- #3457 → CP-C4 (invoke reviewer only after exact PR/head match + retrigger per round; reserve-guarded).

## Proposed decomposition (sequential checkpoint-per-PR; a mini-epic, likely >1 session)
Ordered by value+risk. Each its own small PR off updated main.
1. **CP-C1 — bounded-cap alignment (S).** Align `reviewProvider.ts` literal 2 with `session.maxLoopCount` (add optional maxLoopCount param to nextStatus/hasRepeatedSurvivor/survivorReason, default 2, keep provider-agnostic); thread config.maxLoopCount → newKodySession; make survivorReason count dynamic (update 2 golden assertions same slice: reviewProviderCharacterization.test.ts:82, kodyReview.test.ts:78); reconcile 2-vs-3 default (code=2, page-briefs say 3). Closes AC-C1. No live-reviewer dependency.
2. **CP-C4 — live reviewer wiring + SECURITY GATE (M, higher-risk, own PR).** Standalone reviewer launch shape (least-privilege!) + requestRun/readRun + reserve-guarded request/per-round retrigger + PR/head validation. Addresses #3456-core (HARD gate), #3457, #3453-completion-signal. Highest value (makes the engine live) — consider FIRST if operator prioritizes a working built-in reviewer + the CP-D dogfood.
3. **CP-C5 — config-driven default flip (S).** Thread provider+BuiltinReviewDeps into sync/import; gated/revertable via TERM_CONTROL_REVIEW_PROVIDER. Addresses #3454. Enables CP-D dogfood A/B.
4. **CP-C2 — per-finding dismiss-with-reason + restore (S-M).** Add dismissReason to ReviewFinding; per-finding mutation handler+routes (mirror markSelected); sanitize; no-resurrection test (survivorStatus keeps dismissed); frontend show-dismissed + restore control (kodyReviewView.ts filters them out today). Closes AC-C2.
5. **CP-C3 — admin toggle full-loop vs approve-each + full-loop driver (M).** loopMode config; auto-advance driver in index.ts (NOT the pure sync module) off the sync tick/onVerified, double-launch guarded; tests both modes. Closes AC-C3. Env-only for v1 (no UI, matching provider).
6. **Override plumbing #3455 (S).** resolveReviewerProfileId live caller (server-side inject) + project-scope reviewerModelProfileId; org store optional (defer).

D-8 (scope line vs E7) is ⚠ operator-confirm: CP-C ships linear cap + survivor-escalation + false-positive dismiss ONLY; all oscillation/no-progress/authority-tier logic waits for E7. NOT-E7: no oscillation classification, tension-pairs, accept-and-defer, Tier A/B/C.

Coder near weekly Max quota (resets 08-19) — CP-C mini-epic likely spans sessions; sequence by operator priority.
