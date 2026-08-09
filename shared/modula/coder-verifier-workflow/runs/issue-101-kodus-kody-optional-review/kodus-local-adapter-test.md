# Kodus local adapter test — Issue #101

Date: 2026-06-29

## Goal

After verifier-approved Sprint 0 stopped for lack of documented Claude/Codex MAX subscription support, the operator approved an unsupported local experiment: try to make a Kodus-compatible OpenAI endpoint backed by local Claude/Codex CLI tooling.

## Environment

- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-101`
- Docker: unavailable (`docker: command not found`)
- Docker Compose: unavailable (`docker: command not found`)
- Claude CLI: available at `/home/hyperbots/.nvm/versions/node/v22.22.3/bin/claude`
- Codex CLI: available at `/home/hyperbots/.nvm/versions/node/v22.22.3/bin/codex`

## What was tested

1. Cloned `kodustech/kodus-installer` into `/tmp/agentops-kodus-101/kodus-installer`.
2. Confirmed the installer requires Docker and Docker Compose for a real Kodus instance.
3. Inspected installer env schema and confirmed the relevant provider variables:
   - `API_OPEN_AI_API_KEY`
   - `API_OPENAI_FORCE_BASE_URL`
   - `API_LLM_PROVIDER_MODEL`
   - `KODUS_TELEMETRY_DISABLED`
4. Added an experimental local OpenAI-compatible gateway in `src/agentops_harness/kodus_max_gateway.py`.
5. Ran unit tests for prompt conversion, OpenAI-compatible payload shape, Claude output parsing, Codex output-file parsing, and network-free echo mode.
6. Ran a local echo-mode HTTP smoke against `/v1/models` and `/v1/chat/completions`.
7. Ran a local Claude-backed HTTP smoke against `/v1/chat/completions`; the response was a valid OpenAI-compatible `chat.completion` with expected assistant content.
8. Generated a temporary Kodus `.env` under `/tmp/agentops-kodus-101/env-validation`, pointed it at the local gateway shape, disabled telemetry, and ran the installer env validator.
9. Added `agentops_harness.kodus_sprint0` to prepare a repeatable Docker-sandbox config and compose override for Linux host-gateway resolution.

## Results

- `PYTHONPATH=src python3 -m unittest tests.unit.test_kodus_max_gateway` — passed, 5 tests.
- Echo-mode gateway HTTP smoke — passed.
- Claude-backed gateway HTTP smoke — passed.
- Kodus installer `validate-env.sh` — passed with one expected warning: Docker unavailable, so runtime drift check skipped.
- `PYTHONPATH=src python3 -m agentops_harness.kodus_sprint0 --work-dir /tmp/agentops-kodus-101/docker-sandbox --gateway-url http://host.docker.internal:18082/v1 --model claude-cli --report dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/kodus-sandbox-prep-report.json` — passed with status `ready` before Docker path discovery.
- `PATH=/snap/bin:$PATH PYTHONPATH=src python3 -m agentops_harness.kodus_sprint0 --work-dir /home/hyperbots/agentops-kodus-101/docker-sandbox --gateway-url http://host.docker.internal:18082/v1 --model claude-cli --start --report dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/kodus-sandbox-start-report.json` — passed with status `running`.
- Private exposure check — passed after revision: web/API/webhooks/MCP publish on `127.0.0.1`; RabbitMQ/Postgres/Mongo publish no Kodus host ports; gateway listens on `172.17.0.1:18082`.
- HTTP smoke — passed: web UI returned 200 at `http://127.0.0.1:13000`.
- Container-to-gateway smoke — passed from `kodus_api` to `http://host.docker.internal:18082/v1`, including a Claude-backed chat completion returning `private-gateway-ok`.

## Safety notes

- No real Kodus `.env` was committed.
- No provider API key, GitHub App secret, webhook token, or auth file was committed.
- The temporary Kodus env used a placeholder local key value only.
- Gateway HTTP request logging is suppressed to avoid prompt leakage.
- Claude CLI smoke outputs were kept in `/tmp` and not committed because they include runtime metadata.

## Conclusion

The local gateway path is viable enough for the next Sprint 0 step: run one sample Kodus review and inspect logs. It is not yet a full Sprint 0 pass because no real Kodus review has completed through the gateway.
