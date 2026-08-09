# Slack Gateway Restart Evidence

Checkpoint: final stability/runbook review for PRD #935.

## Scope

This evidence uses fake token-presence values and a synthetic #924 status JSON file under `/tmp`. It does not configure Slack, send messages, open sockets, mutate GitHub, or store credentials.

## Commands

```bash
SLACK_BOT_TOKEN=present SLACK_APP_TOKEN=present \
  PYTHONPATH=src python3 -m agentops_harness.slack_gateway_cli health \
  --allowed-user-id U_OK \
  --allowed-channel-id C_OK \
  --status-json /tmp/agentops-slack-restart-status.json \
  --format json

PYTHONPATH=src python3 -m agentops_harness.slack_gateway_cli answer \
  --question "what is active?" \
  --status-json /tmp/agentops-slack-restart-status.json \
  --max-age-minutes 0 \
  --format json
```

## Results

- Health JSON parsed successfully.
- Health status was `ok` with token presence booleans only.
- Health output did not include fake token values.
- Two consecutive read-only answer runs produced identical JSON.
- The answer was rebuilt from #924-style JSON and included active item #935.
- No Slack credentials, real Slack user/channel IDs, raw events, transcripts, GitHub writes, git writes, deployments, or terminal injections were used.

## Interpretation

The local gateway is state-light for read-only operation. Restart recovery does not require chat process state because status answers are rebuilt from #924 output, and proposal queue state is represented by bounded outside-repo proposal files when configured.
