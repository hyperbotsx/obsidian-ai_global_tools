# Read-only Project 2 control tower

Generated: 2026-06-07T21:12:36.200136Z


## Active work
- #564 [Task] Finish Phase 1 config completeness hardening — In Progress; deterministic blocker fixes and false-positive reducer checks
- #612 [PRD] TikTape-backed Hyperliquid datafeed catalog enablement — In Progress
- #641 PRD: Frontend layout responsiveness and job-loading fixes — Done
- #646 PRD: NOME chat integration UX across desktop and mobile — In Progress; implementation_status: approved for Checkpoint A no-code baseline audit; product-code changes remain blocked until baseline target UX approval
- #681 [PRD] DSP-ready market data foundation for algorithmic trading research — In Progress; Known limitations, license restrictions, and blocked symbols.
- #682 [PRD] Datafeed multi-resolution extension and UI coexistence — In Progress; The job launcher should show compatible datasets and fail before execution if requirements are missing, stale, or license-blocked.
- #701 [PRD] Chart Grid Overlays V2: Volatility (ATR) — Done; blocked_by_prd: https://github.com/hyperbotsx/SoldierOne/issues/725
- #730 [PRD] Safe all-asset/all-timeframe TikTape historical backfill — Done; Storage space is not expected to be a blocker as long as data lands on the `/mnt/hyperliquid-data` drive. The agent must still refuse or pause if:
- #756 [PRD] Trading Section Foundation: Paper, Live, and Portfolio — Done; Connection state for each supported exchange/broker: unavailable, not connected, sandbox-ready, connected-read-only, blocked, or error.
- #766 [Tracker] Adversarial debate hardening execution order — Done; | 3a | Family 3 Funding/carry canonical activation/F2 smoke | Done | PR #669 merged; promotion remains blocked by expected immutable funding artifact gate. |
- #820 PRD: Validated chart market catalog for asset dropdowns — In Progress; | Data-preview API times out | Treat as blocker; do not fall back to full candle scans. |
- #824 PRD: Canonical candle adapter readiness and controlled writer contract — In Progress
- #860 [Tracker] Adversarial debate production readiness execution order — In Progress; what must remain blocked without explicit approval,

## Ready for agent
- #565 [Task] Add Phase 1 config import smoke test — Ready for Agent
- #566 [Task] Define portable config artifact schema — Ready for Agent

## Blocked / needs human
- #887 PRD: Genesis Portfolio Ensemble Allocation Persistent Source-Authority Resolution Loop — Blocked; Implementation status: Blocked at Checkpoint 2 — #894 is CEO-approved, but `portfolio_ensemble_allocation` remains fail-closed until #894 implementation produces a verifier-approved `portfolio_component_registry_v1` artifact.
- #586 PRD: Genesis ideator family module refactor and 50-cycle hardening gate — Blocked; Mirrored lessons use the existing hardening lesson schema and include source family, track, run, attempt, blocker title, outcome, transferability, and sanitized artifact references.
- #611 [PRD] Pattern Discovery Native Method — Done; Truthful handoff readiness: `ready` only with a valid Strategy Configuration / Handoff Package; otherwise `unavailable`, `blocked`, `incomplete`, or `decision_required`.
- #632 PRD: Charts page indicator foundation — frontend V1 — Blocked; CEO approval: Approved for V1 chart indicator foundation, blocked until #633 lands
- #647 [PRD] Signal Discovery Job Creation Verification and Repair — Done; If the method is not ready to emit a valid configuration package, it must fail closed through the shared readiness vocabulary (`unavailable`, `incomplete`, `blocked`, or `decision_required`). Candidate previews, local `config_ready` booleans, and method-specific preview JSON are not valid configuration output by themselves.
- #649 [PRD] System Builder Job Creation Verification and Repair — Blocked; If the method is not ready to emit a valid configuration package, it must fail closed through the shared readiness vocabulary (`unavailable`, `incomplete`, `blocked`, or `decision_required`). Candidate previews, local `config_ready` booleans, and method-specific preview JSON are not valid configuration output by themselves.
- #650 [PRD] Evolutionary Strategy Discovery-Owned Job Creation Verification and Repair — Blocked; If the method is not ready to emit a valid configuration package, it must fail closed through the shared readiness vocabulary (`unavailable`, `incomplete`, `blocked`, or `decision_required`). Candidate previews, local `config_ready` booleans, and method-specific preview JSON are not valid configuration output by themselves.
- #705 [PRD] Discovery Runtime Foundation for Method-Owned Execution — Blocked; This PRD defines the shared runtime foundation that the method-specific runtime PRDs (#676-#679) should use. The goal is to avoid four different lifecycle implementations and instead provide one Discovery-owned execution, progress, blocker, readiness, and artifact contract.
- #740 [PRD] Discovery preview execution QA re-check after DATA backfill — Approved; Discovery preview originally blocked #637 execution-to-output QA because the preview backend had no OHLCV candles for the tested market contexts. That original zero-data blocker was manually mitigated for the current BTC preview QA path on 2026-05-23 by seeding Hyperliquid BTC candles:
- #777 [PRD] Trading Route QA and Safety Hardening Pass — Blocked; > Status: CEO approved for bounded implementation; blocked until the #776 PR is merged to `main`.

## CEO review / PRD draft queue
- #563 [PRD] Adversarial debate operational matrix and portable config artifacts — PRD Draft; Phase 1 config completeness and blocker taxonomy
- #584 [PRD] Operator Matrix category expansion — PRD Draft
- #585 [PRD] Hardening LCM blocker memory — PRD Draft; Create a PRD for hardening-specific LCM blocker memory and cross-family lesson retrieval.
- #586 PRD: Genesis ideator family module refactor and 50-cycle hardening gate — Blocked; Mirrored lessons use the existing hardening lesson schema and include source family, track, run, attempt, blocker title, outcome, transferability, and sanitized artifact references.
- #621 PRD: Strategy complexity profiles for seed generation — Future; As a hardening operator, I want complexity profile metadata recorded now, so future corpus/reporting work can analyze blocker rates by complexity profile.
- #623 [PRD] Portfolio Management Agent Council — Todo
- #688 [PRD] Strategy and training data compatibility gate — PRD Draft; Add a compatibility gate to strategy and training launch flows so jobs declare data requirements, show compatible datasets, and block runs with missing, stale, low-quality, or license-blocked data.
- #745 [PRD] Account AI provider connections and routing — PRD Draft
- #799 [PRD] DATA Knowledge Foundation: IA, Ownership, and Compatibility Map — PRD Draft
- #800 [PRD] Canonical Knowledge Read API and Schema Contracts — PRD Draft
- #801 [PRD] Knowledge Provenance and Promotion Contract — PRD Draft; Promotion requires a source locator that can be resolved or clearly marked as stale/missing. If the source cannot be resolved, promotion must fail or produce a visible blocked state; it must not silently create trusted Knowledge.
- #802 [PRD] Shared Signals Neutral Registry Surface — PRD Draft
- #803 [PRD] DATA Section Shell and Knowledge Page Foundation — PRD Draft
- #805 [PRD] Active Market Workspace Foundation and Scope Contract — PRD Draft
- #806 [PRD] Provider Context Metadata and Backend Filtering Contract — PRD Draft
- #807 [PRD] Memory and Knowledge Provider-Aware Retrieval — PRD Draft
- #808 [PRD] Cross-Provider Strategy Portability and Validation Gate — PRD Draft; blocked / not recommended
- #809 [PRD] App-Wide Provider Context UI Adoption — PRD Draft
- #826 [PRD] Provider-Neutral C++ Cipher DSP Adaptive Signal Runtime — PRD Draft; Raw-event support is blocked until #810 or a successor provider-neutral raw-event PRD provides:
- #831 PRD: Proportional and Adaptive Grid Overlays — Done
- #832 PRD: Footprint Chart and Volume Delta Order Flow Indicators — PRD Draft
- #890 PRD: Genesis Adversarial Debate Maintainability Consolidation Pass — PRD Draft
- #891 PRD: Fix with Nome gate-blocker architecture hardening — PRD Draft; Proposed working branch: `prd/fix-with-nome-gate-blocker-architecture-891`

## Approved but not started
- #897 PRD: Adversarial Debate Backtest Readiness Backend Contracts — Approved; Relationship to #898: this PRD may represent `training_export_prepared`, but Training import remains blocked pending #898 and explicit human approval.
- #896 PRD: Adversarial Debate Workflow Nodes and User-Facing Copy — Approved; the blocker and why local attempts were insufficient;
- #898 PRD: Training Handoff Export and Human Import Handshake — Approved; 7. Required audit fields are approver identity, approval timestamp, source package version/hash, source debate job, explicit non-approval marker, and rejection reason when blocked.
- #870 PRD: Genesis Cross-Family Validation, Backtest, and Robustness Scorecard — Approved; Implementation status: Complete for approved readiness/schema-only scope: validation-admissibility ingestion, blocked-family visibility, provider-neutral validation input contracts, and scorecard schema readiness. Validation/backtest execution remains blocked until at least one selected family has `artifact_gate_passed` or a separately approved named exception.
- #899 PRD: Genesis Evidence Index and Discoverability Pass — Approved; 3. Make current gate states, verifier reports, PR links, blockers, and downstream approval boundaries easy to find.
- #569 [PRD 1] Admin Hardening V2.0 Foundation — Track Registry, DTOs, Run History, and Runner Controls — Approved
- #570 [PRD 2] Admin Hardening Seed Readiness and Golden Corpus — Approved; PRD approved on 2026-05-03 for product shape. Implementation depends on stable PRD 1 DTO/taxonomy foundation. Readiness is deterministic; blocker harvest is post-readiness; validator enforcement requires separate human-approved decision or PRD.
- #571 [PRD 3] Admin Hardening Operator Matrix Dashboard — Approved; PRD approved on 2026-05-03 for product shape as an MVP Operator Matrix after PRD 1–2 foundations are stable. Blocker harvest, validator coverage, and lane coverage are enhanced optional fields and must not block MVP implementation.
- #580 [PRD 3.1] Admin Hardening Coverage Browser — Approved; artifact type, family, readiness, support, run-status, blocker, and stale/fresh filters
- #572 [PRD 4] Admin Hardening Extended Autonomous Operations — Approved; Operators want deeper automation than the normal bounded cap, but longer autonomous runs can edit code, test, deploy, launch rechecks, commit, push, and affect PR state. This PRD defines deliberate extended autonomous mode with initial cap 10, elevated permissions, enforceable cycle/recheck/deploy/wall-clock budgets, durable notification/webhook events, terminal-only or human-reviewed push policy, resume semantics, archival, and advisory blocker harvest by default.
- #579 [PRD 5] Admin Hardening Parallel Lane Operations and Observability — Approved; Approve this PRD for future product shape only. Keep the first four PRDs focused, then add this fifth PRD because parallel hardening lanes with independent branches, worktrees, runtime directories, logs, restart controls, and dashboard sub-pages are a major operational capability. Implementation is blocked until PRD 1–4 are stable, extended-operations safety is proven where longer lane runs are used, and one isolated lane mutation has passed cleanly.
- #575 PRD: Strategy Configuration Contract Program Overview — Approved
- #576 PRD: Strategy Configuration Contract — Approved; blocked/missing-state handling
- #591 [PRD] Data Feed Quality Tab Truthful Recovery State — Approved
- #599 PRD5: Coder-Verifier Agent Workflow POC — Approved
- #613 PRD: Discovery Debate Frontend Fixes — Approved
- #633 PRD: Chart indicator/data foundation — backend V1 — Approved
- #631 [PRD] Frontend Responsiveness, Tokens, and Component Reuse Cleanup — Approved
- #659 [PRD] Datafeed gap assurance and archive-to-live continuity checks — Approved; 2. V1 audits every cataloged Hyperliquid pair/timeframe, including hidden and blocked statuses, as diagnostic rows.
- #663 PRD: Chart page visual polish fixes — Approved
- #666 [PRD] Hyperliquid chart gap visualization and source-quality guard — Approved; Initial investigation suggests this is not primarily a candlestick renderer defect. The chart can silently render sparse live DB candles as a continuous series when the archive source for the selected pair/timeframe is blocked or partial. For example, `BTC 5m` is currently cataloged as partial/blocked in the archive policy, yet the chart can still display live DB candles for that pair/timeframe. Missing intervals are compressed on the category x-axis, so sparse data appears as discontinuous price action without an explicit data-quality warning.
- #670 PRD: Chunked candlestick chart loading and level-of-detail rendering — Approved
- #696 [PRD] Frontend product copy and UI clarity guidelines for coding agents — Approved; 6. Safety clarity is mandatory: warnings, destructive-action consequences, data-risk states, and operational blockers must remain explicit.
- #723 [PRD] Volume Profile V3: Session Order Flow and Liquidity — Approved
- #740 [PRD] Discovery preview execution QA re-check after DATA backfill — Approved; Discovery preview originally blocked #637 execution-to-output QA because the preview backend had no OHLCV candles for the tested market contexts. That original zero-data blocker was manually mitigated for the current BTC preview QA path on 2026-05-23 by seeding Hyperliquid BTC candles:
- #750 PRD: Optional Ehlers DSP Addons for Chart Indicators — Approved
- #781 PRD: Training Chart Overlay API and Chart Integration — Approved
- #787 [PRD] Shared Section Page Header and Breadcrumb Consistency — Approved
- #796 [PRD] Canonical candlestick database for production and preview domains — Approved
- #798 [PRD] Discovery canvas shell source-of-truth hardening — Approved; Discovery execution or data blockers, including #740.
- #814 [PRD] Training Experiment Intake, Context Selector, and Discovery Import Flow — Approved; if the user is on Evaluation or Artifacts, those pages should use the selected experiment context and show empty/blocker states if required records are missing,
- #827 [PRD] Adaptive Signal Modules Program Umbrella — Approved; Raw-event-dependent modules remain blocked until #810 or successor work provides verified raw-event foundations.
- #842 PRD: Global Activity Console for background jobs — Approved; Discovery and Training jobs can run in the background while users move between pages. Today, job state is mostly page-local. A user may start a Signal Discovery run, move to another method or training workflow, and miss that a job completed, failed, or became blocked. During development this also slows QA because operators need to keep multiple pages or API checks open.
- #852 PRD: Genesis Phase 1 Full Suite Failure Cleanup — Approved
- #883 PRD: Genesis Trend Momentum Persistent Source-Authority Resolution Loop — Approved; Approval notes: Approved after CEO-requested revisions added a narrow pass definition, no-close-after-first-failure lifecycle guard, retry-wave governance, escalation rules, blocker inventory, execution-cost decision path, and narrower predecessor-update requirements. Approval does not authorize validation/backtest execution or downstream deployment.
- #889 PRD: Adversarial Debate Backtest Readiness and Training Handoff Workflow — Approved; Approval boundary: this PRD approves the product workflow contract, user-facing copy direction, status semantics, blocker taxonomy, and handoff boundary. It does not approve coding the full workflow in one implementation pass.
- #912 PRD: Genesis Component-Return Source Owner Authority Resolution — Approved; > Historical evidence: PRD #911 artifacts under `docs/evonome/genesis/phase-2/source-manifests/portfolio_ensemble_allocation/source-authority/prd911/` and #887 blocker update https://github.com/hyperbotsx/SoldierOne/issues/887#issuecomment-4637821600.
- #922 PRD: Hermes-safe runtime activation and sandbox verification — Approved; blocker and local attempts;
- #924 PRD: Read-only Project 2 orchestration control tower — Approved; What is blocked and why?
- #925 PRD: Human-confirmed orchestration action assistant — Approved; If implementation is blocked after bounded local attempts, run Exa Search before declaring this infeasible or requesting terminal deferral.
- #929 PRD: Genesis Component-Return Selected Inputs Source Authority — Approved; Non-zero component-return rows are desired but not pass-forcing; a verifier-approved fail-closed blocker packet is the correct outcome if selected-input authority cannot be proven.
- #930 PRD: Main chart dataset selector integration and UI alignment — Approved; The selector is interactive and not blocked by overlay pointer-event layers.
- #931 PRD: Provider-neutral tick data pilot and derived tick-bar read path — Approved; #930 remains a separate frontend PRD for main chart placement and styling. It is not a blocker for backend read-path delivery unless the implementation explicitly targets the #930 main chart surface.
- #934 PRD: AI Maestro read-only orchestration dashboard integration — Approved; If implementation is blocked after bounded local attempts, run Exa Search before declaring the integration infeasible or requesting terminal deferral.
- #935 PRD: Telegram operator gateway for orchestration questions and instructions — Approved; deliver concise notifications about blockers, verifier findings, and next human decisions;

## Worktree health
- /mnt/hyperliquid-data/projects/worktrees/agentops-harness — prd/project2-readonly-control-tower-924; dirty
- /mnt/hyperliquid-data/projects/worktrees/Evonome-admin — prd/agentops-harness-repo-foundation-936; dirty
- /mnt/hyperliquid-data/projects/worktrees/Evonome-data — feat/datafeed-multiresolution-coexistence-682; dirty
- /mnt/hyperliquid-data/projects/worktrees/Evonome-frontend — feat/main-chart-dataset-selector-integration-930; dirty
- /mnt/hyperliquid-data/projects/worktrees/Evonome-training — chore/training-discovery-handoff-readiness-867; clean
- /mnt/hyperliquid-data/projects/worktrees/Evonome-trading — feat/live-readiness-paper-evidence-source; clean
- /mnt/hyperliquid-data/projects/worktrees/Evonome-discovery — fix/discovery-preview-execution-qa-740; clean
- /mnt/hyperliquid-data/projects/worktrees/Evonome-adversarial-hardening — feat/adversarial-debate-readiness-contracts-897; clean

## Drift warnings
- None found.

## System health / data freshness
- Overall: ok
- Project 2 read: ok
- Worktree read: ok

## Recommended next human action
Review blocked items and choose whether a human decision is needed.

## Read-only command allowlist
- `gh auth status`
- `gh project item-list`
- `gh issue list`
- `gh issue view`
- `git -C`
