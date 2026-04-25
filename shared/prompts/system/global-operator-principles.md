# Global operator principles

- Prefer this vault at `/mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools` as the canonical location for reusable prompts, skills, workflows, agent docs, and reusable wiki-maintenance templates.
- Apply that rule globally, not just inside one repo or worktree.
- Resolve tool requests from this vault first: tool-specific folders before shared folders.
- Treat repo-local duplicates as mirrors or compatibility copies unless the user explicitly says otherwise.
- Keep secrets outside the vault.
- Keep prompts concise, durable, and tool-agnostic where possible.
- Put deep implementation detail into skill/reference files rather than bloating global prompts.
- Update the canonical file here first; let wrappers and symlinks make tools consume it.
- Prefer KISS defaults: small focused functions, low nesting, flat control flow, and naming over comments.
- Prefer precise internal names over metaphor, brand, or mode-specific terms; keep branded wording in display copy or compatibility layers.
- Prefer reusable shared components, props, capability flags, and injected actions before creating forks or near-duplicate UI.
- Prefer shared design tokens, UI primitives, and established layout patterns over hardcoded one-off CSS.
- Keep one canonical type, schema, or contract per concept; extend existing models before creating parallel versions.
- When working inside a vault that uses an LLM Wiki schema, treat source folders as read-mostly and write persistent synthesis into `wiki/`.
- For LLM Wiki workflows, maintain `wiki/index.md` and `wiki/log.md` as first-class navigation and history files.
