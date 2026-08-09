# Coder Handoff — Issue #55 Explain Selection Overlay

## Scope

Allowed paths:

- `term-control-center/shared/` for request/response types and shared safety policy reuse.
- `term-control-center/server/` for a token-guarded read-only explanation route, caps, safety checks, prompt construction, rate limiting, and local runtime adapter.
- `term-control-center/src/` for Diff Inspector selection UI, context menu, keyboard fallback, card lifecycle, and styles.
- `term-control-center/tests/` for backend safety/route tests and static UI coverage.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-55-explain-selection-overlay/` for durable workflow artifacts.

Forbidden paths/actions:

- No PR creation, commits, merges, deployments, approvals, staging, or git mutation.
- No product routes/navigation outside the Diff Inspector.
- No new outbound HTTP AI SDK/API-key surface without explicit human sign-off.
- No durable storage of selected snippets, prompts, explanations, provider responses, terminal transcripts, secrets, or private account data.
- No snippet/prompt/response content in logs.
- No editing, patch generation, auto-fix, review approval, or Prepare PR readiness claims from this feature.

Pre-existing dirty files before editing: none (`git status --short --branch` was clean on `prd/explain-selection-overlay-55`).

## PRD / Issue

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/55
- Branch: `prd/explain-selection-overlay-55`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Current checkpoint: Final bug-check — approved

## Research Summary

Researcher consult completed 2026-06-20. Recommendation: implement local-first, explicit-action, read-only, non-persistent explanation. Use a local one-shot CLI/runtime from the backend by default; do not add browser/provider API keys or a new HTTP AI SDK/API surface. Trigger custom menus from `contextmenu`, preserve native behavior unless a valid Diff Inspector selection exists, support Context Menu key/Shift+F10 and a visible button, and render provider output as plain text only. Treat selected code as untrusted: separate instructions from `UNTRUSTED_SELECTED_CODE`, disable tools/network/writes/memory, bound the task to explanation only, and do not execute snippet instructions. Send only selected snippet plus minimal metadata, cap size, scan for secrets before generation, and do not persist or log snippets/prompts/responses.

Cited sources from researcher: OpenAI API key safety doc updated 2026-06-16; Chrome Private Network Access article updated 2022-07-07; MDN `contextmenu` accessed 2026-06-20; WAI-ARIA APG 1.2 (2021-11-29); OWASP LLM01 Prompt Injection (2024-04-10); OWASP Prompt Injection Prevention Cheat Sheet accessed 2026-06-20; NIST AI 600-1 published 2024-07-26 and updated 2026-04-08; OpenAI API data controls page.

Local CLI check: `claude --help` confirms `-p/--print`, `--input-format text`, `--output-format text`, `--no-session-persistence`, `--disable-slash-commands`, `--safe-mode`, `--tools`, and `--system-prompt` options. Adapter passes selected content via stdin, not argv. Provider preflight/tests fail closed if required non-persistence, customization-isolation, or tool-disabling flags are unavailable.

## Provider / Safety Design

- Endpoint: implemented `POST /groups/:id/diff/explain`, protected by existing `x-term-token` guard.
- Default provider: implemented local one-shot CLI runtime only, default command `claude`, env-overridable path/model/timeout/caps; no direct HTTP provider code.
- Runtime args: print/text mode with `--no-session-persistence`, `--safe-mode`, slash commands disabled, tools disabled, explicit explain-only system prompt, prompt body over stdin.
- Fail-closed states: unavailable provider/configuration, blocked path, stale/mismatched selection, secret-like content, timeout, provider failure, and rate limit.
- Server selection binding: client selection payload is untrusted. The route must re-read the active group diff, verify the requested file is current, allowed, non-blocked, non-binary, non-too-large, and renderable, verify side/line range maps to current hunks, derive surrounding context server-side, and compare normalized selected text against current diff lines before any provider call. Mismatches fail closed.
- Safety order before provider call: authorize group, verify active implementation diff, bind selection to current rendered hunks, reuse shared blocked-path policy, cap selected text, run secret-content heuristic, enforce per-session rate cap, then build prompt and invoke local runtime.
- Prompt construction: selected code and server-derived surrounding context are labeled as untrusted data with explicit instructions not to follow instructions from snippets and to explain only.
- Privacy: no prompt files, no response persistence, no logs containing selected text/prompt/response; only in-memory request/card state.

## Env Vars Documented So Far

- `TERM_CONTROL_EXPLAIN_PROVIDER` (default `claude-cli`; any other value fails closed as unavailable).
- `TERM_CONTROL_EXPLAIN_CLAUDE_PATH` (default `claude`).
- `TERM_CONTROL_EXPLAIN_CLAUDE_MODEL` (optional model arg for local CLI).
- `TERM_CONTROL_EXPLAIN_MAX_SELECTED_CHARS` (default `4000`).
- `TERM_CONTROL_EXPLAIN_MAX_SELECTED_LINES` (default `400`).
- `TERM_CONTROL_EXPLAIN_CONTEXT_LINES` (default `20`).
- `TERM_CONTROL_EXPLAIN_TIMEOUT_MS` (default `30000`).
- `TERM_CONTROL_EXPLAIN_RATE_PER_MINUTE` (default `6`).
- `TERM_CONTROL_EXPLAIN_OUTPUT_CHARS` (default `6000`).

## Planned Checkpoints

1. Research + provider/safety design — approved by verifier revision 2.
2. Backend explanation endpoint and provider adapter — approved by verifier revision 4.
3. Selection UI/context menu/keyboard fallback — approved by verifier revision 6.
4. Explanation card lifecycle and accessibility — approved by verifier revision 7.
5. Safety/rate-limit/privacy tests and validation — approved by verifier revision 8.
6. Final bug-check — approved by verifier revision 11 (`bug_check_status: passed`).

## Changed Files

- `term-control-center/shared/diffExplain.ts`: shared request/response/status types for explanation calls.
- `term-control-center/server/explainConfig.ts`: env-overridable caps for selection, context, timeout, output, and per-session rate.
- `term-control-center/server/explainSafety.ts`: selection caps, secret-content heuristic, output sanitization, and normalized text matching helpers.
- `term-control-center/server/explainPrompt.ts`: explain-only system prompt and prompt builder with untrusted code/context boundaries.
- `term-control-center/server/explainSelectionBinding.ts`: server-side validation that selected text maps to current rendered diff hunks before provider calls, including unified display marker normalization for added/deleted lines.
- `term-control-center/server/explainProvider.ts`: local `claude` CLI one-shot runtime adapter with required flag preflight, stdin prompt, `--safe-mode`, disabled tools/slash commands, no session persistence, deterministic timeout/abort, and output cap.
- `term-control-center/server/diffExplain.ts`: route orchestration for active group diff verification, blocked-path/secret/stale-selection/context-secret refusal, rate limiting, prompt construction, provider mapping, and HTTP status mapping.
- `term-control-center/server/index.ts`: token-guarded `POST /groups/:id/diff/explain` route.
- `term-control-center/src/diffSelection.ts`: reads browser selections scoped to diff code cells, line metadata, side, and anchors.
- `term-control-center/src/diffExplainClient.ts`: token-guarded client POST helper for explanation requests under `/term` proxy base paths.
- `term-control-center/src/DiffExplainOverlay.tsx`: selection bubble, context menu, visible keyboard fallback toolbar, Ctrl/Cmd+Shift+E shortcut, Context Menu/Shift+F10 menu path, copy selection, request cancellation, loading/error/timeout/unavailable/rate-limit/success card states, copy explanation, close, dialog labels, and plain-text rendering.
- `term-control-center/src/DiffInspector.tsx`: adds diff code-cell metadata and mounts the explain overlay for renderable selected files.
- `term-control-center/src/styles.css`: terminal-styled selection toolbar/bubble/context menu and explanation card styles with responsive bottom-sheet behavior.
- `term-control-center/tests/diffExplain.test.ts`: backend blocked-path/secret/stale-selection/context-secret/prompt-boundary/rate-limit/provider-disabled/timeout/no-content-logging/no-durable-storage/runtime isolation-arg/fail-closed coverage.
- `term-control-center/tests/termBasePath.test.ts`: static coverage for Diff Inspector explain overlay, context menu, keyboard fallback, token route, card states/accessibility controls, plain-text rendering guard, and styles.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-55-explain-selection-overlay/coder-handoff.md`: this handoff.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-55-explain-selection-overlay/review-request-r1-research-design.json`: checkpoint 1 revision 1 request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-55-explain-selection-overlay/review-request-r2-research-design-fix.json`: checkpoint 1 revision 2 request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-55-explain-selection-overlay/verifier-report.md`: verifier report artifact for checkpoint/final reviews.

## Validation

- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffExplain.test.ts` — passed (7/7 after checkpoint 2 fixes).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffExplain.test.ts tests/termBasePath.test.ts` — passed (29/29 after checkpoint 3 fix).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/termBasePath.test.ts` — passed (21/21 for checkpoint 4 card/accessibility coverage).
- `npm --prefix term-control-center run typecheck` — passed after final bug-check fix.
- `npm --prefix term-control-center test` — passed (264/264) after final bug-check fix.
- `npm --prefix term-control-center run build` — passed after final bug-check fix with existing Vite non-module/chunk-size warnings; ignored `term-control-center/build/` and `term-control-center/dist/` removed after validation.
- Steward final hygiene review — clean; no cleanup needed; `git diff --check` clean per steward.

Final validation targets are satisfied.

## Findings Addressed

- `V55-CP1-001`: revised local runtime design from unsupported `--temporary` to installed `--no-session-persistence`; added fail-closed provider flag preflight/test requirement.
- `V55-CP1-002`: added explicit server-side selection binding to current diff hunks and fail-closed mismatch behavior before provider calls.
- `V55-CP2-001`: added secret-content scanning for server-derived surrounding context before provider invocation; regression proves runtime is not called.
- `V55-CP2-002`: made local runtime timeout settle immediately as `timeout`, sends `SIGTERM`, and schedules `SIGKILL`; regression covers a child that ignores `SIGTERM`.
- `V55-CP2-003`: refactored backend helpers into context objects/smaller functions and removed unused bound-selection data.
- `V55-CP3-001`: backend selection binding now accepts unified-mode synthetic leading `+`/`-` display markers for changed lines without weakening stale-selection checks; regression added.
- `V55-FINAL-001`: local Claude runtime now includes and preflights `--safe-mode`; regression proves provider fails closed when the isolation flag is unavailable.
