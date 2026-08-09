# Kodus local gateway operational validation

Date: 2026-06-29

## Human approval

The operator explicitly approved Claude/Codex CLI usage for this local gateway experiment.

## Sanitized gateway observability

`src/agentops_harness/kodus_max_gateway.py` now emits one JSON line per request with metadata only:

- `event`
- `request`
- `method`
- `path` without query string
- `status`
- `duration_ms`
- `queued_ms`
- `backend`
- `model`
- `error` class name only

The logger allowlists fields and drops unexpected keys, so prompts/source are not emitted even if accidentally supplied to the log helper.

Live container-to-gateway smoke after restart:

- `GET /v1/models` from `kodus_api` returned 200.
- `POST /v1/chat/completions` from `kodus_api` returned 200 through Claude CLI.
- Gateway log entry for the chat request contained method/path/status/duration/backend/model only.

## Timeout/fail-closed validation

A temporary gateway used a fake Claude-compatible command that slept longer than the configured timeout.

Result:

```text
timeout_response=502 {"error": "TimeoutExpired"}
timeout_log_secret_hits=0
```

Sanitized log sample:

```json
{"backend": "claude", "duration_ms": 1000, "error": "TimeoutExpired", "event": "kodus_gateway_request", "method": "POST", "model": "claude-cli", "path": "/v1/chat/completions", "request": 1, "status": 502}
```

## Concurrency smoke

A temporary echo backend gateway processed five concurrent `/v1/chat/completions` requests without invoking paid or subscription CLIs.

Result:

```text
concurrency_response=[200, 200, 200, 200, 200]
concurrency_log_private_hits=0
concurrency_log_request_count=5
```

## Rate-limit smoke

A temporary gateway used `--max-concurrency 1 --queue-timeout 0.5` with a fake slow Claude-compatible command. Two concurrent requests produced one successful completion and one bounded rejection.

Result:

```text
rate_limit_response=[200, 429]
rate_limit_log_private_hits=0
rate_limit_429_count=1
rate_limit_queued_ms_count=2
```

Sanitized 429 log sample:

```json
{"backend": "claude", "duration_ms": 500, "error": "rate_limited", "event": "kodus_gateway_request", "method": "POST", "model": "claude-cli", "path": "/v1/chat/completions", "queued_ms": 500, "request": 1, "status": 429}
```

Live PR #175 showed the original 30-second queue timeout was too short for Kodus parallel agents. The default was raised to 600 seconds and the PR was rerun successfully. Gateway logs from the successful rerun showed queued requests waiting and returning 200, including `queued_ms=171354` and `queued_ms=50938`.

## Provider fallback check

The live Kodus `.env` points at the local gateway and leaves the common hosted provider keys empty:

```text
API_LLM_PROVIDER_MODEL=claude-cli
API_OPENAI_FORCE_BASE_URL=http://host.docker.internal:18082/v1
API_OPEN_AI_API_KEY=<placeholder-or-configured>
API_ANTHROPIC_API_KEY=<empty>
API_GOOGLE_API_KEY=<empty>
API_OPENROUTER_API_KEY=<empty>
API_NOVITA_API_KEY=<empty>
```

Codex was then validated as an optional fallback path:

- Direct Codex gateway smoke from `kodus_api` returned 200 for models and chat completions.
- Temporary PR #176 ran with `API_LLM_PROVIDER_MODEL=codex-cli` and live gateway `--backend codex`.
- Kodus completed PR #176 with `status=success`.
- After validation, live config was restored to `API_LLM_PROVIDER_MODEL=claude-cli` and live gateway `--backend claude`.

## Remaining limits

- Token replacement was validated with a new 7-day GitHub token, but expiry/refresh itself remains constrained until the token approaches expiry or a forced-expiry scenario is available.
- The gateway now has timeout/fail-closed behavior, concurrent request handling, and a default single-slot rate limiter with bounded queue timeout.
