# Coder Handoff — Issue #56 Diff Inspector Review Aids

## Scope

Allowed paths:

- `term-control-center/src/` for Diff Inspector review-aid UI/state/helper modules.
- `term-control-center/shared/` for small review-aid types if needed.
- `term-control-center/server/` only if a later checkpoint needs safe-read/existence helpers through existing #54 guards.
- `term-control-center/tests/` for unit/static coverage.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/` for workflow artifacts.

Forbidden paths/actions:

- No PR creation, commits, merges, deployments, staging, or GitHub/project/PRD status mutation.
- No git-state mutation from the Diff Inspector.
- No raw code, raw diff, selected snippets, prompts, terminal transcripts, or private data in `localStorage`.
- No new unguarded file-read surface; reuse #54 diff payload/safe path patterns if server helpers become necessary.
- No heavy language-server/indexing dependencies.
- No auto-running or auto-filling test commands.
- No product-name hardcoding.

Pre-existing dirty files before editing: none (`git status --short --branch` was clean on `prd/diff-inspector-review-aids-56`).

## PRD / Issue

- Canonical PRD: https://github.com/hyperbotsx/agentops-harness/issues/56
- Branch: `prd/diff-inspector-review-aids-56`
- Dependency #54 status: closed/merged 2026-06-20.
- Current checkpoint: Final verifier bug-check — approved revision 12 (`bug_check_status: passed`).
- Stop condition: reached; stop before PR creation.

## Research Summary

Mandatory researcher consult completed 2026-06-21 for PRD research-first surfaces. Guidance:

- Namespace browser storage with repo+branch+issue identifiers, wrap `localStorage` in `try/catch`, cap entries, evict by age, and fall back to in-memory when blocked/quota fails.
- Store only metadata; do not persist raw code, raw diff text, extracted symbols, or generated hints. Treat SHA-256 fingerprints as staleness identifiers, not encryption.
- Use browser Web Crypto SHA-256 over canonical strings for fingerprints.
- For outlines, prefer bounded best-effort line scanners for the selected file only, with no TypeScript/Babel/tree-sitter/Python AST dependency.
- Risk and test hints should be deterministic, path-first, transparent, labeled advisory, and should not execute commands or invent unavailable tests.

Sources cited by researcher: MDN localStorage/storage quotas/SubtleCrypto.digest, OWASP HTML5 Security Cheat Sheet, ECMAScript spec, Python ast docs, npm scripts docs.

## Verifier Checkpoints

1. Review pins/bookmarks, reviewed-file local state, namespacing, and eviction caps.
2. Changed-function outline best-effort accuracy, graceful/oversized fallback, and performance.
3. Risk badge heuristic clarity, path-first rule sourcing, and false-positive-safe wording.
4. Test-impact hints derived from existing repo patterns, copy-only, existence-checked.
5. Read-surface safety: operates on #54 payload/safe read path, reuses blocked-path module, no unguarded reads.
6. Visual/accessibility fit with Diff Inspector and Term Control Center.
7. No mutation or persistence of raw code/diff content.
8. Final validation and verifier bug-check.

## Changed Files

- `term-control-center/shared/diff.ts`: diff OK responses now expose repository, issue number, and test hint metadata.
- `term-control-center/server/gitDiffReader.ts`: populates repository/issue metadata from the launch task and attaches test-impact hints.
- `term-control-center/server/diffTestHints.ts`: existence-checked package script and nearby test-file hint collector.
- `term-control-center/src/diffReviewState.ts`: local review metadata model, namespaced storage keys, caps, eviction, reviewed fingerprints, and no-raw-code fingerprint helpers.
- `term-control-center/src/diffOutline.ts`: best-effort selected-file TS/JS/Python changed-symbol scanner with unsupported/oversized fallback.
- `term-control-center/src/diffRisk.ts`: deterministic path-first and sparse changed-hunk risk hint rules.
- `term-control-center/src/DiffReviewAids.tsx`: review rail, hide-reviewed toggle, outline list, risk hint badges, copy-only test hints, mark/unmark reviewed controls, pin list/note editing, and pin target menus.
- `term-control-center/src/DiffPatchView.tsx`: extracted patch renderer with line/hunk pin markers and jump-to-pin scrolling.
- `term-control-center/src/DiffInspector.tsx`: wires review state into the file rail, selected diff content, and review rail.
- `term-control-center/src/styles.css`: compact review rail, pin menus/markers, reviewed controls, responsive layout, and jump flash styles.
- `term-control-center/tests/diffReviewState.test.ts`: coverage for namespacing, caps/eviction, fingerprint reset, storage fallback, and no raw diff persistence.
- `term-control-center/tests/diffOutline.test.ts`: coverage for TS/JS symbols, Python qualified symbols, unsupported files, and oversized fallback.
- `term-control-center/tests/diffRisk.test.ts`: coverage for starter path rules, changed-hunk content rules, and heuristic/hint wording.
- `term-control-center/tests/diffTestHints.test.ts`: coverage for existing package scripts, nearby test file discovery, and no invented hints.
- `term-control-center/tests/termBasePath.test.ts`: updated static coverage for extracted patch renderer.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/coder-handoff.md`: this handoff.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r1-checkpoint-1.json`: checkpoint 1 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r2-checkpoint-1-fixes.json`: checkpoint 1 revision verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r3-checkpoint-2-outline.json`: checkpoint 2 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r4-checkpoint-3-risk.json`: checkpoint 3 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r5-checkpoint-4-test-hints.json`: checkpoint 4 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r6-checkpoint-4-test-hints-retry.json`: checkpoint 4 verifier retry after invalid JSON transport response.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r7-checkpoint-5-read-safety.json`: checkpoint 5 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r8-checkpoint-5-read-safety-fixes.json`: checkpoint 5 revision verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r9-checkpoint-6-visual-a11y.json`: checkpoint 6 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r10-checkpoint-7-no-mutation-raw.json`: checkpoint 7 verifier request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/steward-request-r11-final-hygiene.json`: final steward hygiene request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r11-final-bug-check.json`: final verifier bug-check request.
- `dev-plans/agentops/coder-verifier-workflow/runs/issue-56-diff-inspector-review-aids/review-request-r12-final-bug-check-retry.json`: final verifier bug-check retry after invalid JSON transport response; approved.

## Implementation Notes

Checkpoint 1 implementation:

- Added localStorage-backed review state keyed by `diff-inspector-review:v1:<repo>:<branch>:<issue>` with browser-storage error fallback to in-memory state.
- Added ≤500 pin and ≤1,000 reviewed-file caps with oldest-entry eviction.
- Reviewed files store only file path, SHA-256 fingerprint, and timestamps; fingerprints are derived in memory from selected-file diff metadata/hunks and are not treated as secrecy.
- Pins store only path, line range, side, type, optional user-authored note, and timestamps.
- Added pin targets for changed lines and hunk headers; the compact review rail can jump to pinned lines and edit/delete pin notes.
- Added mark/unmark selected file reviewed and hide/show reviewed files in the file rail.
- Notes are never auto-populated from selected code; raw diff text is not persisted.
- Revision 2 now requires a current matching fingerprint before labeling/hiding a file as reviewed, hashes only canonical patch body hunks, removes destructive namespace cleanup until active namespace data exists, and collapses review-aid helper parameters into context objects.
- Checkpoint 2 adds a selected-file-only outline section in the review rail. It scans only the selected diff payload in memory, skips selected patches over 256 KB, supports TS/JS and Python regex patterns, labels results as best-effort, and jumps to the matched line without persisting outline data.
- Checkpoint 3 adds selected-file risk hints in the review rail. Badges are deterministic and non-AI, path-first where available, with sparse changed-hunk content rules for network/process/filesystem write calls. Each badge is clickable and explains the matched rule/reason as heuristic only.
- Checkpoint 4 adds server-generated test-impact hints from existing package.json scripts and real nearby test files. The UI presents hints as copy-only buttons with verifier-judgment wording; it never executes or auto-fills commands.
- Checkpoint 5 tightens `diffTestHints` path safety by normalizing changed-file and candidate test paths through the existing #54 `normalizeGitPath` helper and skipping blocked paths with the shared blocked-path module. Package metadata reads are capped at 256 KB and skipped on oversized/error cases. Regression coverage verifies blocked summaries, blocked paths, escaping paths, and oversized package metadata return no hints.
- Checkpoint 6 makes review-aid sections native collapsible `details` panels, preserves keyboard-accessible buttons/summaries/inputs, adds explicit copy/jump labels, and keeps compact `--ao-*` token styling with responsive review rail behavior.
- Checkpoint 7 is cross-cutting: review aids remain local UI helpers only. Persisted review data stores metadata/user-authored notes/fingerprints but not raw hunk text, selected snippets, outline labels, risk hints, test hint content, prompts, or transcripts. No GitHub, Prepare PR, git mutation, or run-action execution paths were added.

## Risk Rule Catalog

Implemented checkpoint 3 catalog:

- `auth-permissions`: path rule for `auth`, `permission`, and `rbac`.
- `secrets-config`: path rule for `.env`, `secret`, `credential`, `/config/`, `.pem`, and `.key`.
- `migrations-schema`: path rule for `/migrations/`, `.sql`, and `schema*` paths.
- `dependency-manifest`: path rule for `package.json`, `package-lock.json`, `requirements*.txt`, `pyproject.toml`, and `poetry.lock`.
- `ci-workflow`: path rule for `.github/workflows/**`, `Dockerfile*`, and `*.ci.*`.
- `network-call`: changed-hunk content rule for `fetch(`, `axios`, `http`, and `request(`.
- `process-exec`: changed-hunk content rule for `child_process`, `execFile(`, `spawn(`, `subprocess`, and `os.system(`.
- `filesystem-write`: changed-hunk content rule for `writeFile(`, `unlink(`, `rmdir(`, `fs.rm(`, and `open(..., 'w')`.

All badge labels include `review hint`; badge detail text states `Heuristic only` and names the matched rule.

## Steward Review

- Steward final hygiene review: clean.
- Steward noted implementation/test files and run artifacts are correctly placed, no raw transcripts/log dumps are present, and no cleanup is required before final verifier bug-check.
- Generated validation artifacts `term-control-center/build/` and `term-control-center/dist/` were removed after the final build.

## Findings Addressed

- `V56-C1-001`: reviewed labels/hide filtering now require a current matching fingerprint; missing or changed fingerprints do not count as reviewed. Regression added.
- `V56-C1-002`: selected-file fingerprint input now hashes only canonical hunk/patch-body data; metadata-only changes do not alter the fingerprint, while hunk text changes do. Regression added.
- `V56-C1-003`: collapsed review helper argument lists into small context objects to satisfy KISS parameter bounds.
- `V56-C1-004`: removed destructive namespace cleanup behavior until an explicit active namespace/session list exists; per-namespace caps remain intact.
- `V56-C5-001`: package.json script discovery now normalizes package metadata paths, rejects blocked paths, checks file size against a 256 KB cap, and returns no scripts on oversized/error cases. Regression added.
- `V56-C5-002`: test hint collection now skips summaries already marked `blocked` by the diff reader. Regression added.

## Validation

Checkpoint 1 validation:

- `npm --prefix term-control-center run typecheck` — passed.
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffReviewState.test.ts tests/diffState.test.ts tests/termBasePath.test.ts` — passed (34/34 after revision 2 fixes).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffOutline.test.ts tests/diffReviewState.test.ts tests/termBasePath.test.ts` — passed (30/30 for checkpoint 2).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffRisk.test.ts tests/diffOutline.test.ts tests/termBasePath.test.ts` — passed (27/27 for checkpoint 3).
- `cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffTestHints.test.ts tests/diffState.test.ts tests/termBasePath.test.ts` — passed (30/30 for checkpoint 4).
- `npm --prefix term-control-center run typecheck && cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffTestHints.test.ts tests/diffState.test.ts && git diff --check` — passed (11/11 focused safety tests after revision 8 fixes).
- `npm --prefix term-control-center run typecheck && cd term-control-center && node --import tsx --test --test-concurrency=1 tests/termBasePath.test.ts tests/diffRisk.test.ts tests/diffReviewState.test.ts && git diff --check` — passed (31/31 for checkpoint 6).
- `npm --prefix term-control-center run typecheck && cd term-control-center && node --import tsx --test --test-concurrency=1 tests/diffReviewState.test.ts tests/diffOutline.test.ts tests/diffRisk.test.ts tests/diffTestHints.test.ts tests/termBasePath.test.ts && git diff --check` — passed (38/38 for checkpoint 7).
- `git diff --check` — passed.

Final validation:

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (311/311).
- `npm --prefix term-control-center run build` — passed with existing Vite warnings about non-module scripts in `index.html` and chunk size.
