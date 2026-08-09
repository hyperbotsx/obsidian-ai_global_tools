# Coder Handoff — Issue #249 Term Diff View Improvements

## Scope and authority

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/249 (approved specification only).
- Branch/worktree: `prd/term-diff-view-improvements-249` at `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-249`.
- Context brief re-read 2026-07-19: `/home/hyperbots/.local/state/agentops/term-control-center/runtime/agentops-prd-249-d3da57bf19fa/artifacts/project-context-brief.md`.
- Operator continuation authorization: implement DIFF-1..6 through ordinary bounded verifier revisions only; it excludes PR creation, merge, deployment, approval, trading, and backtesting.
- Allowed: `term-control-center` diff/explain surfaces, tests/styles/docs, authenticated pin-artifact route, and this run folder. Forbidden: coms wire/envelopes, launcher/session behavior, authority, deployment, GitHub mutation, secrets, PR/merge/deploy actions, and silent fallback.
- Pre-edit baseline was clean. Current dirty paths are only the declared P1 implementation, tests/styles, and this run folder.

## Checkpoints and stop condition

1. P1 — DIFF-1 layout and DIFF-2 resilience/content identity/sequencing/parser corrections.
2. P2 — DIFF-6 explain hardening and DIFF-5.2 untracked cap (blocking security checkpoint).
3. P3 — remaining DIFF-5 server work.
4. P4 — DIFF-3 renderer.
5. P5 — DIFF-4 workflow/evidence, steward review, verifier recheck, and final bug-check.

Stop only after final verifier bug-check approval or a genuine human escalation. **P1 was approved at revision 4; P2 at revision 2; P3 at revision 5; P4 at revision 4, all with zero open findings. The operator authorized P5 on 2026-07-19; P5 DIFF-4 implementation revision 1 is complete and awaiting the required Steward hygiene review.**

## Research

Researcher consult completed 2026-07-19 before P1: React recommends effect cleanup with `AbortController` plus a monotonic sequence guard; last-good data must remain local to its request identity and `AbortError` is ignored. Node `node:test`/`tsx` supports pure transition and static-rendering tests, while browser interaction remains P5 Browser QA. Sources: official React `useEffect`, React state-preservation, `renderToStaticMarkup`, and Node `node:test` documentation (accessed 2026-07-19). No dependency was added.

P2 freshness consult completed 2026-07-19: official Codex guidance supports `codex exec --sandbox read-only --ephemeral` without `disk-full-read-access`; use an explicit allowlist (`PATH`, isolated `CODEX_HOME` only if needed, one intentional Codex auth variable, optional TLS certificates), never inherited `process.env`. Node v22 docs require a `child.stdin` error listener before `.end()` and once-only settlement for EPIPE/close/timeout races. Sources: OpenAI Codex noninteractive/config/environment docs and Node v22 stream docs, accessed 2026-07-19.

## P1 revision 2 changes and finding reconciliation

- **V249-P1-001:** `AllotmentShell` now keeps `TerminalArea` at the same `section > div` ancestry for both Diff states and only toggles the stable terminal slot's visibility; the inspector is a sibling. A structural regression assertion verifies no 62/38 split remains. Browser/session smoke remains P5 QA.
- **V249-P1-002:** `src/diffClient.ts` is the one checked-response boundary. It preserves safe structured non-2xx errors, distinguishes 401/403 as `auth_error`, rejects malformed replies to a generic fail-closed error, and applies the same classification while resolving groups. Tests cover `git_lock`, 401/403, malformed server responses, and matching active group selection.
- **V249-P1-003:** scoped last-good/error state is computed by source plus group; a scope change clears selection and retained state, while a stale sequence cannot apply. Pure tests cover same-group retention/recovery, cross-group clearing, and stale-response rejection.
- **V249-P1-004:** extracted `server/diffContentToken.ts` parses full `--no-abbrev` old/new blob IDs plus status. Only working/untracked content appends size/mtime; committed-only content stays stable under metadata-only touches. Deterministic token tests cover tracked/dirty, binary/blocked/oversized-shaped working entries, rename/copy, untracked fallback, and a repository metadata-touch regression.
- **V249-P1-005:** destination statistics now come only from that destination's parsed numstat entry; the source stat is not combined. The staged copy-plus-modified-source fixture asserts independent copy/source totals and selected hunks.
- **V249-P1-006:** parser emits no-newline markers as zero-counter `annotation` lines; `DiffPatchView` renders subtle annotation rows, not code/context rows. Parser and render-structure tests cover this.
- **V249-P1-007:** porcelain records an `MM` staged/worktree-divergence flag and the summary exposes `staged content differs`; parser coverage includes `MM`.
- **V249-P1-008:** `startDiffPolling` accepts source identity and returns before creating a timer for completion diffs; the client passes the source and tests prove completion starts no timer. Refresh stays explicit.
- **V249-P1-009:** pins carry an optional stable `hunkIndex`; outline pins derive it from the selected file. Jumps resolve the owning hunk before the line selector. Repeated-line and migrated-pin tests cover the behavior.
- **V249-P1-010:** added deterministic Node-level client, scope/sequence, polling, jump, content-token, parser/copy, terminal-structure, storage-error, and rename-pin coverage without a DOM dependency. Storage persistence failure remains visibly surfaced by the existing review-aids status UI; P5 retains live Browser QA.
- **V249-P1-011:** extracted narrow client transport (`diffClient.ts`), request identity transitions (`diffRequestScope.ts`), jump selection (`diffJumpTarget.ts`), and server token construction (`diffContentToken.ts`); removed the unused `contentTokenFor` and source-stat combiner. `gitDiffReader.ts` is 251 lines and the inspector is 294 lines after focused extraction; P2/P3 server work remains isolated outside it.

## P1 revision 3 changes and finding reconciliation

- **V249-P1-007:** added a pure summary-label boundary and render it in each file rail row, so an `MM` summary visibly reads `+A -D · staged content differs` without replacing blocked/binary/oversize labels.
- **V249-P1-008:** successful server default selection no longer mutates request selection state. Completion now has one initial request, no poll/visibility request, and later requests only from explicit file selection or Refresh.
- **V249-P1-009:** each render tree has a named `data-diff-view`; jump resolution selects only the media-query active tree before finding its owning hunk/line. A pure narrow/desktop view selection test complements repeated-hunk coverage.
- **V249-P1-010:** added visible-MM, requested-rail-path, active-render-view, and actual same-size dirty rewrite-to-unreview regressions. Node-level tests stay deterministic and P5 retains live browser/session smoke.
- **V249-P1-011:** split parser transition setup, removed the five-argument pin target helper, formatted/extracted dense changed render boundaries, and injected a single migration timestamp from the React effect rather than calling time inside the reducer.
- **V249-P1-012:** requested path now wins rail highlighting while retained content remains visible, with A→B pending/success selection coverage through the pure rail-selection boundary.

## P1 revision 4 changes and finding reconciliation

- **V249-P1-007:** moved staged/worktree divergence into its own `DiffFileSummary.stagedDiverges` field. It now composes with binary and selected-too-large safety state rather than being overwritten by `note`. Repository-backed `MM` binary and oversized tests prove both retain divergence.
- **V249-P1-010:** added those server-combination regressions. Completion's one-shot behavior remains implemented through the absence of any response-driven request-path mutation; the existing polling test proves no timer/visibility request and the source path has only initial, explicit selection, and explicit refresh fetch triggers.

## P2 implementation revision 1

- **DIFF-6 least privilege:** Codex now executes with `--sandbox read-only --ephemeral` in a fresh empty temporary cwd; the full-disk sandbox override is removed. All explain runtime and preflight child spawns receive only an explicit environment allowlist (path/home/locale/TLS roots plus intentional provider auth), never inherited server, GitHub, Term, or generic secret-token variables.
- **DIFF-6 process safety and filters:** stdin installs an error listener before `.end()` and all close/timeout/EPIPE paths settle once. The shared path blocklist covers `.env` variants, `.npmrc`, `.netrc`, `id_rsa*`, PEM/KEY files, and service-account JSON; explain text rejects JWT, Google API, Slack, and conservative long-token shapes. Focused regressions include the no-token child environment, empty Codex cwd, `--ephemeral`, EPIPE, ordinary source false-positive control, and supported secret shapes.
- **DIFF-5.2 DoS cap:** `TERM_CONTROL_DIFF_MAX_UNTRACKED_STATS` defaults to 20 (0–500). It caps only untracked `--no-index --numstat` spawns before they occur; oversized or cap-excess untracked files receive a visible `stats unavailable` summary marker and are never content-read for those stats. A 1,000-file fixture proves three configured stat spawns and the oversized skip.

## P2 revision 2 finding reconciliation

- **V249-P2-001:** added Codex `--ignore-user-config` and `--ignore-rules` to the runtime and fail-closed preflight, with argument and fake-runtime coverage; this excludes user configuration/rule surfaces while preserving read-only ephemeral execution.
- **V249-P2-002:** Claude auth now deterministically prefers `CLAUDE_CODE_OAUTH_TOKEN`; it only falls back to `ANTHROPIC_API_KEY`, so each child gets exactly one provider credential. A both-present fixture asserts the precedence.
- **V249-P2-003:** untracked stats use `lstat`, reject symlinks/non-regular entries before any stat spawn, and selected-patch reads reject the same entries. A symlink regression proves no `--no-index --numstat` spawn and an empty selected patch with the visible unavailable marker.
- **V249-P2-004:** passed one runtime input object instead of six positional parameters and extracted focused runtime/untracked fixture helpers. Changed source/tests remain under the 300-line limit; bounded test callbacks are below the function-size rule.
- No P3 route, ETag, context, completion, renderer, or workflow work was started.

## P2 approval

- Verifier approved P2 revision 2 with zero open findings. The compact verdict is the authoritative checkpoint result; no P2 report detail was re-read after approval.
- **P3 option 1 authorized by the operator:** use the minimal shared completion schema extension for DIFF-5.5. P3 is active; its final verifier checkpoint remains pending the other approved DIFF-5 work.

## P3 DIFF-5.5 slice

- Added optional persisted `CompletionState.completionBase` evidence (`baseRef`, immutable `mergeBase`, capture timestamp); the completion store validates and round-trips it without accepting malformed values.
- Completion discovery and accepted completion events capture a base once with Git argv; completion diffs receive the stored base. `readTaskDiff` verifies the pinned commit before use, falls back to the live base only when an existing pinned commit is unavailable, and flags `baseStale`; legacy completion diffs are explicitly marked stale.
- Focused coverage proves persistence/malformed rejection and that an old pinned base keeps the completion diff visible after `origin/main` advances.

## P3 completion revision 1

- ETag identity now contains HEAD, merge base, ordered content tokens, selected path, limits, and whitespace mode. Both live and completion diff routes return ETags and 304 before numstat, selected-patch, or test-hint work; the client sends `If-None-Match` and preserves last-good state on 304.
- Added the bounded authenticated group/completion context routes. They require current diff membership plus normalized/non-blocked paths; reject leading-colon paths and worktree symlinks; realpath-check worktree content; and cap base/worktree reads with `TERM_CONTROL_DIFF_MAX_CONTEXT_BYTES`.
- The toolbar's Ignore whitespace control maps only selected tracked patches to Git `-w` and participates in the ETag. Unknown requested paths now return `requestedPathMissing` with no substitute patch, and tracked pathspecs use Git literal top-level pathspecs.
- Base resolution supports a safe `TERM_CONTROL_DIFF_BASE_REF`, then prefers `refs/remotes/origin/main` and retains legacy origin/main/main fallbacks. Completion-base capture shares the resolver.
- Test hints memoize directory/package lookups per request and omit copy-paste commands for shell-metacharacter package directories.
- `gitDiffReader.ts` is 234 lines and `DiffInspector.tsx` is 291 lines after extracting `DiffToolbar`; focused P3 tests cover ETag short-circuit and HEAD changes, whitespace, explicit unknown paths/literal pathspecs, context guards/cap, base config, hint sanitization, and route ETag/304/context behavior.
- P3 is complete and awaiting its first verifier checkpoint review; P4 has not started.

## P3 revision 2 finding reconciliation

- **V249-P3-001:** added per-hunk Base context and Worktree context controls with scoped loading/error/content states. They use the authenticated live or completion context route and remain bound to the currently selected diff path. Added base-read, live-route, completion-route, and static rendered-control coverage.
- **V249-P3-002:** worktree verification now compares canonical realpaths; a symlink-addressed repository fixture succeeds while context reads continue to reject file symlinks.
- **V249-P3-003:** completed-report preparation is async and captures completion-base evidence; retry completion events preserve an existing valid pin; store validation now requires an exact valid ISO timestamp. Added retry/persistence/malformed-time coverage and completion ETag/304 coverage.
- **V249-P3-004:** a shared request-options parser accepts only absent or `whitespace=ignore`; invalid or repeated forms return bounded 400 responses for live and completion routes.
- **V249-P3-005:** conditional Git reads, diff-state readers, client fetches, and inspector loading use focused request objects; unchanged completion is extracted into a small helper. Existing oversized route/store hosts only received bounded wiring.
- P3 revision 2 validation: `npm --prefix term-control-center run typecheck`, focused diff/completion/base-path suites (146/146), and `git diff --check` all passed. P4 remains unstarted.

## P3 revision 3 finding reconciliation

- **V249-P3-001:** each context expander is keyed by group/path/content token, aborts on identity change/unmount, and uses a monotonic request sequence so only the latest Base/Worktree response may update UI state.
- **V249-P3-003:** completed-report launches now pass an existing synthetic completion pin into preparation, so base capture occurs only for a previously unpinned state.
- **V249-P3-005:** grouped the remaining group-diff reader and conditional Git request inputs; inspector/client request paths remain object-based. Focused validation passed: typecheck, 52 focused P3/completion/renderer tests, and `git diff --check`.

## P3 revision 4 finding reconciliation

- **V249-P3-001:** the expander key now includes group, completion source, path, and content token; abort and monotonic sequence guards remain in place.
- **V249-P3-003:** added a repository-backed completed-report preparation regression that advances `origin/main`, reuses the original pin, and proves the completion diff remains visible.
- **V249-P3-005:** `readTaskDiff` now takes two formal parameters (task plus a typed rest tuple); conditional response construction is extracted into focused helpers. The affected focused suites passed 26/26 with typecheck and `git diff --check`.

## P3 revision 5 — human-authorized extra correction

- Operator authorized one additional bounded P3 correction after revision 4's `needs_human` verdict.
- **V249-P3-001:** extracted a pure identity/sequence gate and added deterministic coverage rejecting late Base/Worktree responses, A→B paths, same-path content rewrites, and group/completion scope changes. The expander uses that gate alongside abort cleanup.
- **V249-P3-005:** `readTaskDiff` now accepts a named options object (requested path, runner, pinned base, and options) with no positional compatibility tuple; its response is passed as one cohesive input. Split the two P3 checkpoint tests into focused helpers below the function-size limit.
- Validation: typecheck, focused P3/context/completion suites (12/12), and `git diff --check` passed. P4 remains unstarted.

## P4 DIFF-3 renderer revision 1

- `DiffPatchView` now mounts exactly one active tree. It defaults to unified on narrow/coarse layouts and side-by-side otherwise, exposes an accessible toggle, and persists only the validated selection under `diff-inspector-view:v1`.
- Extracted bounded row construction, row rendering, intraline comparison, syntax tokenization, and view persistence into focused modules; `DiffPatchView.tsx` is 58 lines and `DiffPatchRows.tsx` is 87 lines.
- Changed-line construction pairs complete adjacent N-delete/M-add blocks: paired rows are rendered as changes and unpaired tails retain their correct add/delete side. Stable hunk/row keys derive from hunk ranges and source line numbers, not render-array indexes.
- Changed side-by-side rows receive bounded prefix/suffix intraline emphasis (skipped above 4,096 characters). A dependency-free tokenizer styles comments, strings, keywords, and numeric literals for a bounded extension allowlist, and leaves unsupported/oversized lines as plain text.
- The patch and row renderers use `memo`; an unchanged ETag poll remains the existing 304 no-state-replacement path, preserving the file/hunk object identity and avoiding patch DOM mutations.
- Tests cover N/M pairing/tails, stable keys, bounded intraline behavior, bounded tokenization, persisted/default view selection, and the single active renderer structure. No P5 workflow/export work was started.

## P4 revision 2 finding reconciliation

- **V249-P4-001:** replaced prefix/suffix emphasis with a bounded character-level LCS calculation, preserving internal unchanged islands. Intraline work now skips only lines over 1,000 characters; tests cover an internal island and the 1,001-character boundary.
- **V249-P4-002:** `useDiffReviewAids` now memoizes its API object against store/UI dependencies. The existing 304 client regression plus explicit memoized patch/row/review API structural coverage verifies the unchanged-poll render boundary; P5 retains the required live MutationObserver/selection/explain Browser QA.
- **V249-P4-003:** hunk keys derive from Git hunk range/header identity and row keys derive from hunk plus source-side line identity. Annotation keys include their stable source offset, so repeated annotations do not collide. Tests prove key uniqueness and invariance when an earlier hunk is inserted.
- **V249-P4-004:** delete/add segments retain intervening newline annotations as old/new metadata, pair their surrounding N/M blocks, and render side annotations in the corresponding side-by-side column. Tests cover both-side, old-only, and new-only marker shapes.
- **V249-P4-005:** pin scrolling uses one focused input object, and `diffViewMode` delegates default selection to the existing `activeDiffView` helper.

## P4 revision 3 finding reconciliation

- **V249-P4-003:** ordinary context/add/delete/change keys now contain only stable hunk starts and Git old/new line identity, not a source offset or hunk header. Annotation keys instead anchor to their adjacent changed line plus side; this remains collision-free for valid old/new no-newline marker shapes. Added a regression proving an unchanged context-row key survives insertion of an annotation inside the same hunk.

## P4 revision 4 finding reconciliation

- **V249-P4-006:** removed unused positional fields from the intermediate row model. Annotation sources now require their stable anchor by type, eliminating the unreachable text fallback while retaining only loop-local offsets needed to inspect adjacent parsed lines.

## P5 DIFF-4 workflow revision 1

- The review rail now shows deterministic list-wide `N of M files reviewed` progress, copy-path control, and a file filter that composes with Hide reviewed.
- Inspector-focus shortcuts follow the approved mapping: `j`/`k` next/previous hunk, `n`/`p` next/previous filtered file, `v` toggle selected-file reviewed, and `y` copy its path. Input, textarea, select, and contenteditable targets are excluded.
- Pins have one pure shared markdown formatter for clipboard and artifact export. The authenticated `POST /groups/:id/diff/pins-export` route accepts only validated pin metadata, requires a running implementation group with runtime artifact metadata, overrides payload identity from the active task, and writes a generated private atomic `diff-review-pins-*.md` artifact below the resolved artifact root. Unknown/inactive/missing-runtime groups fail closed.
- Extracted focused file-rail, keyboard-navigation, pin client, shared formatter, and server export modules. `DiffInspector.tsx` remains 269 lines.
- Focused UI/server tests cover progress/export formatting/validation, pin artifact authorization, private mode, containment, file filtering, shortcut mappings, and P4 structural compatibility. Browser live-scale screenshots, MutationObserver/network evidence, and in-flight explain survival remain the P5 manual QA sub-gate and have not been fabricated.

## P5 revision 2 finding reconciliation

- **V249-P5-001–007:** corrected filtered navigation, added the keyboard hint and per-file copy control, aligned pins transport with the bounded 500-pin schema via a route-specific parser, unified copy/export snapshots, retained structured actionable export errors, and escaped/bounded Markdown paths. Focused keyboard/pin tests and typecheck pass.
- **V249-P5-008:** remains pending: the required live-scale Browser QA must run on a real local task/session and record sanitized screenshots plus 304/MutationObserver, terminal-preservation, selection/scroll, explain, keyboard/filter/progress/export evidence. No evidence was fabricated.
- Steward re-reviewed P5 after revision 2 and again found placement clean. Removed regenerated ignored `term-control-center/build/` and `term-control-center/dist/`; `git diff --check` passes. Verifier recheck is next.

## P5 Steward hygiene review

- Steward reviewed P5 placement and run artifacts. Source/tests and run evidence are correctly placed; no out-of-scope/generated artifacts were tracked.
- Per Steward cleanup request, removed ignored `term-control-center/build/` and `term-control-center/dist/` validation outputs. `git diff --check` remains clean.
- Required next step: verifier recheck followed by final bug-check. P5 live-scale Browser QA evidence remains an explicit manual sub-gate.

## P4 approval

- Verifier approved P4 revision 4 with zero open findings. The compact verdict is authoritative; the full report was not re-read after approval.
- P5 is intentionally not started under the operator's P4-only boundary. No steward review or final verifier bug-check is due until the final implementation checkpoint.

## Touched files

- Client/layout: `src/App.tsx`, `src/DiffInspector.tsx`, `src/DiffPatchView.tsx`, `src/DiffPatchRows.tsx`, `src/DiffReviewAids.tsx`, `src/DiffToolbar.tsx`, `src/diffClient.ts`, `src/diffFileLabel.ts`, `src/diffIntraline.ts`, `src/diffJumpTarget.ts`, `src/diffPatchRows.ts`, `src/diffPolling.ts`, `src/diffRequestScope.ts`, `src/diffReviewState.ts`, `src/diffSyntax.ts`, `src/diffViewMode.ts`, `src/styles.css`.
- Server/shared: `server/diffContentToken.ts`, `server/diffParsers.ts`, `server/gitDiffReader.ts`, `server/diffConfig.ts`, `server/diffBaseRef.ts`, `server/diffContext.ts`, `server/diffEtag.ts`, `server/diffState.ts`, `server/diffTestHints.ts`, `server/explainProvider.ts`, `server/explainSafety.ts`, `server/completionDiffBase.ts`, `server/completionDiscovery.ts`, `server/completionRoutes.ts`, `server/completionStore.ts`, `server/index.ts`, `shared/diff.ts`, `shared/completion.ts`, `shared/blockedPaths.ts`.
- Tests: `tests/completionDiff.test.ts`, `completion-store.test.ts`, `diffClient.test.ts`, `diffContentToken.test.ts`, `diffExplain.test.ts`, `diffExplainRuntime.test.ts`, `diffFileLabel.test.ts`, `diffIntraline.test.ts`, `diffJumpTarget.test.ts`, `diffP3.test.ts`, `diffPatchRows.test.ts`, `diffPatchView.test.ts`, `diffPolling.test.ts`, `diffRequestScope.test.ts`, `diffReviewState.test.ts`, `diffState.test.ts`, `diffSyntax.test.ts`, `diffViewMode.test.ts`, `termBasePath.test.ts`, plus updated typed fixtures in `diffOutline.test.ts`, `diffRisk.test.ts`, and `diffTestHints.test.ts`.
- Artifact: this handoff, P1 review requests through `review-request-r4-p1.json`, and P2 review requests `review-request-r1-p2.json` and `review-request-r2-p2.json`.

## Validation

- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffFileLabel.test.ts tests/diffState.test.ts` — passed, 11/11.
- Earlier P1 broad focused run: `tests/diff*.test.ts tests/termBasePath.test.ts` — passed, 88/88.
- `git diff --check` — passed.
- P2 revision 1: `npm --prefix term-control-center run typecheck` — passed.
- P2 revision 1: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts tests/termBasePath.test.ts` — passed, 93/93.
- P2 revision 2: `npm --prefix term-control-center run typecheck` — passed.
- P2 revision 2: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts tests/termBasePath.test.ts` — passed, 94/94.
- P2 revision 2: `git diff --check` — passed.
- P3 DIFF-5.5 slice: `npm --prefix term-control-center run typecheck` — passed.
- P3 DIFF-5.5 slice: focused completion/diff suites — passed, 54/54.
- P3 completion: `npm --prefix term-control-center run typecheck` — passed.
- P3 completion: focused diff/completion/base-path suites — passed, 134/134.
- P3 completion: `git diff --check` — passed.
- P3 completion: `npm --prefix term-control-center run build` — passed (existing Vite asset/chunk warnings only).
- P3 completion: `npm --prefix term-control-center audit --audit-level=moderate` — passed, 0 vulnerabilities.
- P3 completion: `npm --prefix term-control-center test` exceeded the 30-minute command limit after 313 passing tests and no reported failures; focused P3/full diff suites above are the checkpoint validation.
- P4 revision 1: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts` — passed, 83/83.
- P4 revision 1: `npm --prefix term-control-center run typecheck` — passed.
- P4 revision 1: `npm --prefix term-control-center run build` — passed (existing non-module script and >500 kB chunk warnings only).
- P4 revision 1: `git diff --check` — passed.
- P4 revision 2: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts` — passed, 85/85.
- P4 revision 2: `npm --prefix term-control-center run build` — passed (existing Vite warnings only).
- P4 revision 2: `git diff --check` — passed.
- P4 revision 3: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts` — passed, 86/86.
- P4 revision 3: `npm --prefix term-control-center run build` — passed (existing Vite warnings only).
- P4 revision 3: `git diff --check` — passed.
- P4 revision 4: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffPatchRows.test.ts` — passed, 5/5.
- P4 revision 4: `npm --prefix term-control-center run typecheck` — passed.
- P4 revision 4: `git diff --check` — passed.
- P5 revision 1: `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diff*.test.ts tests/completion-routes.test.ts tests/termBasePath.test.ts` — passed, 159/159.
- P5 revision 1: `npm --prefix term-control-center run build` — passed (existing Vite warnings only).
- P5 revision 1: `git diff --check` — passed.
- P5 revision 2: `npm --prefix term-control-center run typecheck` — passed.
- P5 revision 2: focused keyboard/pin export suites — passed, 22/22.

## Deferred validation

- Browser QA/screenshots remain P5 final gates. No generated `build/` or `dist/` output is tracked.
- P5 live-scale Browser QA is pending a running local task/session; no screenshots or dry-run artifact has been fabricated.
