# Researcher Instructions

Use this file when a downstream agent asks for stack-specific architecture, directory layout, boilerplate, test layout, migration layout, state management, design-system structure, SDK/API behavior, auth, rate limits, or deprecations.

## Required Exa workflow

1. Identify the concrete stack, framework versions, runtime, deployment target, and constraints.
2. Search with Exa against official or primary sources first; include current date filters or version terms where useful.
3. Fetch source contents, not only snippets.
4. Prefer official docs, release notes, framework maintainers, standards bodies, and mature ecosystem guidance.
5. Record URL, source type, version/date or fetched date, and the decision impact.
6. Separate universal standards from stack-specific recommendations.
7. Recommend the minimum viable structure that satisfies the project constraints.

## Evidence expectations

For each recommendation, include:

- Source URL.
- Publication date, version, or fetched date when no date exists.
- Why the source is relevant.
- What decision it supports.
- Any conflict, uncertainty, or version risk.

## Fail-closed conditions

Stop and ask the human or requesting agent to escalate when:

- Exa is unavailable or blocked.
- Official/versioned sources cannot be fetched.
- Sources conflict on a safety-sensitive choice.
- Sources are undated for a fast-moving surface and no release/version anchor exists.
- The requested answer would hardcode a stack, cloud, database, test runner, or framework where none has been approved.

## Current research baseline

A mandatory PRD #180 freshness consult on 2026-06-30 found that Exa supports task research, contents extraction, official-domain filtering, date filtering, deep research, structured output, and additional queries; framework layouts, migration commands, UI state guidance, design token specifications, skills, and prompt packaging are version-specific. Treat this baseline as evidence that fresh project-specific research is required, not as a substitute for future research.
