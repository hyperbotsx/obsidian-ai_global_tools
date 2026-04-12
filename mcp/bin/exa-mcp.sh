#!/usr/bin/env bash
set -euo pipefail
SECRETS_FILE="${AI_GLOBAL_TOOLS_MCP_SECRETS_FILE:-/home/hyperbots/.config/ai-global-tools/mcp-secrets.env}"
if [ -f "$SECRETS_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$SECRETS_FILE"
  set +a
fi
exec npx exa-mcp-server
