# LLM Wiki Pattern

This note instantiates the "LLM Wiki" idea into a concrete operating model for this environment.

## Purpose

The goal is to maintain a persistent markdown wiki that compounds over time instead of rediscovering knowledge from raw documents on every query.

## Three-layer model

### 1. Source layer
Read-mostly source material.

Examples:

- research notes
- articles
- PRDs
- transcripts
- clipped web pages
- imported markdown

Agents may read these freely, but should not rewrite them during ordinary wiki maintenance unless the user explicitly asks.

### 2. Wiki layer
Persistent generated synthesis under a dedicated `wiki/` directory.

Examples:

- overview pages
- domain pages
- concept pages
- source-summary pages
- comparisons
- durable query outputs
- lint reports

### 3. Schema layer
A rules document such as `AGENTS.md`, `CLAUDE.md`, or equivalent workflow notes.

The schema defines:

- folder conventions
- page types
- ingest/query/lint workflows
- indexing and logging rules
- how to handle contradictions and stale claims

## Recommended file layout for a live wiki instance

- `AGENTS.md`
- `Home.md`
- `raw/`
- `wiki/Home.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/overview.md`
- `wiki/source-maps/`
- `wiki/domains/`
- `wiki/concepts/`
- `wiki/sources/`
- `wiki/syntheses/`
- `wiki/queries/`
- `wiki/lint/`

## Default operations

### Ingest
- read a source
- extract durable claims and open questions
- create/update source-summary and synthesis pages
- update `wiki/index.md`
- append to `wiki/log.md`

### Query
- read `wiki/index.md` first
- use wiki pages as the primary context layer
- confirm against source files as needed
- save durable answers back into the wiki

### Lint
- find contradictions, stale claims, orphan pages, and missing links
- write a report under `wiki/lint/`
- update `wiki/index.md` and `wiki/log.md`

## Current live instance

The first live instance created from this pattern is currently:

- `/mnt/hyperliquid-data/projects/obisidan/Evonome-vault`

Important note:

- the requested path `/mnt/hyperliquid-data/projects/obisidan/Evonome` did not exist on disk at implementation time
- the actual vault found and configured was `Evonome-vault`

## What AI_Global_Tools owns

This vault owns the reusable pattern, templates, and global guidance.

Live content wikis such as `Evonome-vault` can use this pattern while keeping their own domain-specific source roots and wiki pages.
