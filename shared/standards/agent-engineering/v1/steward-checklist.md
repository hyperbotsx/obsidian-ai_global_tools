# Steward Checklist

Use this checklist before final bug-check when file placement, artifacts, generated output, prompts, skills, launch context, or source-of-truth layout changed.

## Placement

- Canonical reusable skills and standards are in AI Global Tools shared or harness-appropriate global folders.
- Repo-local files are only docs, config examples, loaders, integration hooks, tests, or references.
- No repo-local `.pi/skills`, `.agents/skills`, `.claude/skills`, or `.codex/skills` directories were created unless explicitly approved.
- Generated files, runtime artifacts, tests, docs, source, schemas, migrations, and fixtures are separated.

## Drift and duplication

- There is one obvious canonical source of truth.
- Thin wrappers or docs point to the canonical pack instead of copying it.
- Any generated sync path has drift detection or a documented manual validation path.
- File names explain ownership and purpose.

## Hygiene

- No raw prompts, raw transcripts, secrets, credentials, private account data, env dumps, or deployment data were written.
- No opportunistic refactors, product code, routes, navigation, deployment files, or unrelated docs were touched.
- Run artifacts are under the expected coder-verifier run folder.
- Temporary files and scratch outputs were removed or documented.

## Handoff readiness

- The handoff lists global files, repo-local files, validation, skipped checks, known risks, and cleanup notes.
- Any path adjustment from the PRD is documented with reason and equivalent responsibilities.
