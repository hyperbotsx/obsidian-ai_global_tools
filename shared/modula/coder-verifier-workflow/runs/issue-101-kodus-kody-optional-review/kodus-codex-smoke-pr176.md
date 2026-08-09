# Kodus Codex backend smoke evidence — PR #176

- Test PR: https://github.com/hyperbotsx/agentops-harness/pull/176
- Branch: `test/kodus-codex-smoke-pr172-20260629221605`
- Status: closed after validation; remote branch deleted.
- Purpose: validate Codex CLI as an optional/fallback local gateway backend for self-hosted Kodus.

## Direct gateway smoke

A standalone Codex gateway was started on `172.17.0.1:18083`.

- `kodus_api` → `GET /v1/models`: 200
- `kodus_api` → `POST /v1/chat/completions`: 200
- Response content: `codex-smoke-ok`
- Gateway prompt-marker leakage grep: 0 hits

Sanitized gateway sample:

```json
{"backend": "codex", "duration_ms": 4252, "error": "", "event": "kodus_gateway_request", "method": "POST", "model": "codex-cli", "path": "/v1/chat/completions", "queued_ms": 0, "request": 2, "status": 200}
```

## Kodus PR smoke

Temporary live changes for the smoke:

- `API_LLM_PROVIDER_MODEL=codex-cli`
- Gateway on `172.17.0.1:18082` restarted with `--backend codex --max-concurrency 1 --queue-timeout 600`.

Kodus review result:

- Logs showed Kodus agents using `openai_compatible:codex-cli`.
- PR #176 review completed with `status=success`.
- One GitHub review was posted.
- Gateway requests all returned 200.
- Queued requests waited instead of failing, including `queued_ms=114201` and `queued_ms=25408`.

Sanitized gateway samples:

```json
{"backend": "codex", "duration_ms": 114202, "error": "", "event": "kodus_gateway_request", "method": "POST", "model": "codex-cli", "path": "/v1/chat/completions", "queued_ms": 0, "request": 2, "status": 200}
{"backend": "codex", "duration_ms": 139618, "error": "", "event": "kodus_gateway_request", "method": "POST", "model": "codex-cli", "path": "/v1/chat/completions", "queued_ms": 114201, "request": 3, "status": 200}
```

Privacy checks:

- Gateway raw patch/source marker grep: 0 hits
- Docker `api` log Mongoose/raw patch grep: 0 hits

Cleanup:

- PR #176 closed after validation.
- Remote branch `test/kodus-codex-smoke-pr172-20260629221605` deleted.
- No merge performed.
- Live Kodus config restored to `API_LLM_PROVIDER_MODEL=claude-cli`.
- Live gateway restored to `--backend claude` on `172.17.0.1:18082`.
