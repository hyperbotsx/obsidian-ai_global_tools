# AI Maestro read-only enforcement report

- Mode: `read_only`
- Service URL: `http://127.0.0.1:23000`
- Status source: `evonome-orchestrator-status --format json`
- Validation HTTP methods: GET
- Runbook: `docs/ai-maestro-runbook.md`
- Restart policy: `restart_localhost_only_then_run_runtime_check_and_bridge_render`
- Recovery policy: `discard_local_cache_and_rehydrate_from_control_tower_output`
- Secret policy: `no_secrets_tokens_provider_config_raw_transcripts_or_private_account_data`

## Forbidden patterns
- `gh issue edit`
- `gh issue create`
- `gh issue comment`
- `gh project item-edit`
- `gh project item-add`
- `git commit`
- `git push`
- `git checkout -b`
- `git town`
- `send-keys`
- `sessions/create`
- `sessions/delete`
- `sessions/rename`
- `aws ec2`
- `aws ecs`
- `docker run`
