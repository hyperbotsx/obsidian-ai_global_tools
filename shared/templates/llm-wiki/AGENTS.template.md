# Vault agent schema

This vault is operated as an **LLM-maintained wiki**.

## Layers

1. source layer — read-mostly corpus
2. wiki layer — generated synthesis under `wiki/`
3. schema layer — this file and related workflow notes

## Source roots

List the read-mostly source folders here.

## Wiki root

Persistent synthesis belongs under `wiki/`.

## Ingest workflow

1. read source
2. extract durable claims, concepts, and open questions
3. update source-summary and synthesis pages
4. update `wiki/index.md`
5. append to `wiki/log.md`

## Query workflow

1. read `wiki/index.md`
2. read relevant wiki pages
3. use source files as confirmation / expansion
4. save durable answers back into `wiki/queries/` or `wiki/syntheses/`

## Lint workflow

Look for contradictions, stale claims, orphan pages, uncited claims, and missing cross-links.
