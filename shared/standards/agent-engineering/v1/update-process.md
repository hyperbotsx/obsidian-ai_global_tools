# Update Process

## Ownership

Owner: `agent:agentops` with human review for standards changes.

## Versioning

- Patch: wording clarifications, typo fixes, or examples that do not change obligations.
- Minor: new guidance or role-specific checks that remain backward-compatible.
- Major: changed obligations, source-of-truth layout, mandatory gates, or hard-blocking behavior.

## Change process

1. Open or reference an approved PRD/issue for non-trivial changes.
2. Research volatile or stack-specific surfaces with Exa before changing reusable rules.
3. Update the canonical pack first.
4. Update thin skill pointers or repo references only as needed.
5. Run the validation checklist.
6. Request verifier review; request steward review when paths, skills, prompts, generated docs, or launch context changed.
7. Record changed files, validation results, risks, and exceptions in the handoff.

## Drift prevention

Do not manually maintain duplicate standards across docs, skills, and prompt templates. Prefer references to this pack. Generated copies must carry source path, version, generated timestamp, and drift validation.
