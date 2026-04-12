# Claude runtime bridge

The `claude` command is wrapped locally so that normal launches:

- append `claude/prompts/system/claude-global.md`
- add the vault as an accessible directory
- load MCP definitions from `mcp/claude/mcp-config.json`
- ignore non-vault MCP configs unless the caller explicitly overrides them
