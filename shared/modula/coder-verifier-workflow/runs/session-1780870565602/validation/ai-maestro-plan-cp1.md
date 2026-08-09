# AI Maestro read-only integration plan

- Mode: `read_only`
- Install state: `not_started`
- Source: https://github.com/23blocks-OS/ai-maestro
- Required bind address: `127.0.0.1`
- Planned local ports: 23000, 23001

## Data paths
- ~/.config/ai-maestro-evonome
- ~/.aimaestro
- ~/.agent-messaging
- /mnt/hyperliquid-data/agent-sandboxes/ai-maestro-safe

## Allowed inputs
- evonome-orchestrator-status --format json
- evonome-orchestrator-status --format markdown
- existing coder/verifier artifact paths
- local reminder-only AMP messages

## Forbidden actions
- GitHub issue, Project, branch, pull request, or deployment writes
- tmux send-keys or terminal injection into real sessions
- AI Maestro real-session create, delete, or rename calls
- public gateway, webhook, cloud, or Docker-agent setup
- secret, token, provider config, or raw transcript storage

## Fail-closed gates
- capture exact version, install source, command, ports, bind address, and data paths
- prove localhost-only binding before browser or message use
- consume control-tower output instead of duplicating Project 2 logic
- show drift as warnings only; never auto-fix drift
- obtain verifier approval before any harmless synthetic session test

