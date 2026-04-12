---
name: pre-pr
description: "Run quality gate checks and adversarial code review before creating a PR. Includes TypeScript, Vite build, Python syntax, ESLint, import check, and 13-category adversarial bug scan. Triggers on: pre-pr, pre pr, review before pr, adversarial review, check for bugs, quality gate."
---

# Pre-PR Quality Gate & Adversarial Code Review

Run all quality checks against the current branch before creating a PR. Two phases: automated checks (fast) then adversarial review (thorough).

---

## The Job

### Phase A: Automated Quality Checks (run first, fail fast)

Run these in order. Stop and fix if any fail:

1. **TypeScript type check:**
   ```bash
   cd frontend && npx tsc --noEmit --pretty
   ```
   Must produce zero errors.

2. **Vite build check:**
   ```bash
   npx vite build --logLevel error
   ```
   Must produce zero errors.

3. **ESLint check (if configured):**
   ```bash
   npx eslint src/ --ext .ts,.tsx --quiet 2>/dev/null || echo "ESLint not configured — skipping"
   ```
   Fix any errors. Warnings are acceptable.

4. **Python syntax check (all backend files):**
   ```bash
   cd /mnt/hyperliquid-data/projects/worktrees/SoldierOne-mllab
   python3 -c "
   import py_compile, os
   errors = []
   for root, dirs, files in os.walk('backend/app'):
       dirs[:] = [d for d in dirs if d != '__pycache__' and d != '.venv']
       for f in files:
           if f.endswith('.py'):
               try: py_compile.compile(os.path.join(root, f), doraise=True)
               except py_compile.PyCompileError as e: errors.append(str(e))
   print(f'FAIL: {len(errors)} errors') if errors else print('ALL OK')
   for e in errors: print(f'  {e}')
   "
   ```
   Must produce zero compile errors (warnings are acceptable).

5. **Backend import check (catches circular imports):**
   ```bash
   source backend/.venv/bin/activate && PYTHONPATH=backend python3 -c "from app.main import app; print('FastAPI app imports OK')" 2>&1
   ```
   Must not raise ImportError or circular import exceptions.

6. **Python unit tests (if available):**
   ```bash
   source backend/.venv/bin/activate && PYTHONPATH=backend python3 -m pytest backend/tests/ -x -q 2>/dev/null || echo "No pytest suite — skipping"
   ```
   All tests must pass. If no test suite exists, skip with note.

7. **Check for uncommitted changes:**
   ```bash
   git status --short | grep -v "^??"
   ```
   Should be empty — all work committed before PR.

Report Phase A results as a table before proceeding to Phase B.

### Phase B: Adversarial Code Review

8. Get the list of changed code files (exclude docs, PRDs, marketing):
   ```bash
   git diff --name-only dev-main...HEAD | grep -E '\.(py|tsx?|js)$'
   ```

9. Read the full prompt from `docs/prompts/adversarial-code-review.md`

10. Get the diff for code files only:
    ```bash
    git diff dev-main...HEAD -- backend/ frontend/src/ scripts/
    ```

11. Execute the adversarial review following the prompt's Phase 1 (show traces) and Phase 2 (13 bug categories)

12. For any "Verification Needed" flags (Ghost Parameter category), grep the codebase to verify callers:
    ```bash
    grep -rn "function_name(" backend/ frontend/src/
    ```

13. Present findings in the prompt's output format:
    ```
    [SEVERITY: Critical/High/Medium] | [CATEGORY: #N Name]
    - Location: file:line
    - The Bug: ...
    - Why it's Silent: ...
    - Impact: ...
    - Fix: ...
    ```

### Phase C: Language Semantic Traps Review

14. Read the language semantics prompt from `docs/prompts/language-semantic-traps.md`

15. Run the same diff through the language semantics checklist (P1-P7 for Python, T1-T5 for TypeScript)

16. Present findings in the prompt's output format:
    ```
    [LANGUAGE: Python/TypeScript] | [TRAP: P1-P7 or T1-T5]
    - Location: file:line
    - The Code: ...
    - Expected Behavior: ...
    - Actual Behavior: ...
    - Fix: ...
    ```

### Final Summary

17. Summarize with a final table:
    ```
    QUALITY GATE RESULTS
    | Check              | Result |
    |--------------------|--------|
    | TypeScript         | PASS/FAIL |
    | Vite build         | PASS/FAIL |
    | ESLint             | PASS/SKIP |
    | Python syntax      | PASS/FAIL |
    | Backend imports    | PASS/FAIL |
    | Unit tests         | PASS/SKIP |
    | Uncommitted changes| NONE/EXISTS |
    | Adversarial review | X findings (N critical, N high, N medium) |
    | Language traps     | X findings (N python, N typescript) |

    Verdict: READY / NEEDS FIXES
    ```

18. If fixes are needed, ask the user: "Want me to fix these now?"

19. **NEVER create the PR automatically.** Wait for the user to say "create PR".

## Important

- Always run Phase A first — if TypeScript or build fails, fix before running Phase B
- Always show Phase 1 traces for the 3 most complex changes — don't skip
- If the diff is too large (>2000 lines), split into backend and frontend passes
- Don't flag style issues unless they cause bugs
- Don't flag pre-existing code unless it interacts with modified code
- The prompt file at `docs/prompts/adversarial-code-review.md` is the source of truth for all 13 bug categories
- Checks marked SKIP are acceptable — they mean the tooling isn't configured yet
