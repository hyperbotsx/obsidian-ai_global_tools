# LLM Wiki templates

These templates support the LLM Wiki operating model.

Use them when creating a new vault that should behave like a persistent, LLM-maintained wiki.

## Template set

- `AGENTS.template.md`
- `wiki-home.template.md`
- `wiki-index.template.md`
- `wiki-log.template.md`
- `source-summary.template.md`
- `entity-page.template.md`
- `concept-page.template.md`
- `query-page.template.md`
- `lint-report.template.md`

## Usage

1. Create a vault or project root.
2. Add a schema file based on `AGENTS.template.md`.
3. Create `wiki/` and its core files from the templates.
4. Point agents at the schema and instruct them to preserve the source/wiki separation.
5. Keep reusable improvements here in `AI_Global_Tools`.
