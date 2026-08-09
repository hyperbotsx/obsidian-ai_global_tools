# Read-only Project 2 control tower

Generated: 2026-06-07T20:59:46.672891Z


## Active work
- #564 [Task] Finish Phase 1 config completeness hardening — In Progress; deterministic blocker fixes and false-positive reducer checks
- #612 [PRD] TikTape-backed Hyperliquid datafeed catalog enablement — In Progress
- #641 PRD: Frontend layout responsiveness and job-loading fixes — Done
- #646 PRD: NOME chat integration UX across desktop and mobile — In Progress; implementation_status: approved for Checkpoint A no-code baseline audit; product-code changes remain blocked until baseline target UX approval
- #681 [PRD] DSP-ready market data foundation for algorithmic trading research — In Progress; Known limitations, license restrictions, and blocked symbols.
- #682 [PRD] Datafeed multi-resolution extension and UI coexistence — In Progress; The job launcher should show compatible datasets and fail before execution if requirements are missing, stale, or license-blocked.
- #701 [PRD] Chart Grid Overlays V2: Volatility (ATR) — Done; blocked_by_prd: https://github.com/hyperbotsx/SoldierOne/issues/725
- #730 [PRD] Safe all-asset/all-timeframe TikTape historical backfill — Done; Storage space is not expected to be a blocker as long as data lands on the `/mnt/hyperliquid-data` drive. The agent must still refuse or pause if:

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

## CEO review / PRD draft queue
- #563 [PRD] Adversarial debate operational matrix and portable config artifacts — PRD Draft; Phase 1 config completeness and blocker taxonomy
- #584 [PRD] Operator Matrix category expansion — PRD Draft
- #585 [PRD] Hardening LCM blocker memory — PRD Draft; Create a PRD for hardening-specific LCM blocker memory and cross-family lesson retrieval.
- #586 PRD: Genesis ideator family module refactor and 50-cycle hardening gate — Blocked; Mirrored lessons use the existing hardening lesson schema and include source family, track, run, attempt, blocker title, outcome, transferability, and sanitized artifact references.
- #621 PRD: Strategy complexity profiles for seed generation — Future; As a hardening operator, I want complexity profile metadata recorded now, so future corpus/reporting work can analyze blocker rates by complexity profile.
- #623 [PRD] Portfolio Management Agent Council — Todo
- #688 [PRD] Strategy and training data compatibility gate — PRD Draft; Add a compatibility gate to strategy and training launch flows so jobs declare data requirements, show compatible datasets, and block runs with missing, stale, low-quality, or license-blocked data.

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
