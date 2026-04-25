Use `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools` as the canonical source of truth for reusable prompts, skills, workflows, agent docs, MCP definitions, and reusable LLM Wiki templates. Apply this rule globally for every Codex session, regardless of the current repo, worktree, or working directory.

Resolution order when a skill, workflow, prompt, agent definition, template, or MCP definition is requested:
1. `AI_Global_Tools/codex/` for Codex-specific assets
2. `AI_Global_Tools/shared/` for cross-runtime canonical assets
3. repo-local copies only when the user explicitly asks for them or no canonical vault copy exists

Treat duplicated repo-local copies as mirrors, compatibility shims, or legacy copies unless the user explicitly declares them authoritative. If a repo-local instruction file conflicts with AI_Global_Tools, prefer AI_Global_Tools and treat the repo-local file as secondary guidance.

Do not store secrets in the vault; keep only references to external secret locations when needed. Prefer KISS defaults: small focused functions, low nesting, flat control flow, precise internal naming, reusable shared components before forks, shared design tokens before one-off CSS, and one canonical type/schema/contract per concept. When working inside a vault that defines an LLM Wiki schema, treat raw/source folders as read-mostly, write persistent synthesis into `wiki/`, and keep `wiki/index.md` and `wiki/log.md` current.
