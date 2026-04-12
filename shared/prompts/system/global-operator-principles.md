# Global operator principles

- Prefer this vault at `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools` as the canonical location for reusable prompts, skills, workflows, agent docs, and reusable wiki-maintenance templates.
- Apply that rule globally, not just inside one repo or worktree.
- Resolve tool requests from this vault first: tool-specific folders before shared folders.
- Treat repo-local duplicates as mirrors or compatibility copies unless the user explicitly says otherwise.
- Keep secrets outside the vault.
- Keep prompts concise, durable, and tool-agnostic where possible.
- Put deep implementation detail into skill/reference files rather than bloating global prompts.
- Update the canonical file here first; let wrappers and symlinks make tools consume it.
- When working inside a vault that uses an LLM Wiki schema, treat source folders as read-mostly and write persistent synthesis into `wiki/`.
- For LLM Wiki workflows, maintain `wiki/index.md` and `wiki/log.md` as first-class navigation and history files.
