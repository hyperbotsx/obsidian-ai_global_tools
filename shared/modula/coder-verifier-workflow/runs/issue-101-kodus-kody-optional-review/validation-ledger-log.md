# Validation ledger log — Issue #101 Kodus/Kody optional review

## 2026-06-29 — Sprint 0 feasibility checkpoint

- Status: blocked pending human decision.
- Evidence: `docs/kodus-kody-sprint0-feasibility.md`.
- Researcher freshness consult completed before implementation.
- Result: Kodus/Kody docs support self-hosted/API-compatible model endpoints, but no documented local Claude/Codex MAX subscription CLI provider path was found.
- Safety posture: no secrets, provider keys, webhooks, workflows, paid API fallback, branch protection, required checks, service deployment, or debt issue automation added.
- Validation: `git diff --check` passed; secret-pattern grep found only documented environment variable names and no secret values.
- Verifier checkpoint 1: approved revision 1; open findings 0; next actor human.
- Human follow-up decision: operator approved testing an unsupported Claude/Codex MAX CLI path anyway.
- Local adapter result: partial pass. Echo and Claude-backed OpenAI-compatible gateway smokes passed; Kodus installer env validation passed with a local gateway base URL and telemetry disabled.
- Docker sandbox prep helper result: passed with status `ready`; report at `dev-plans/agentops/coder-verifier-workflow/runs/issue-101-kodus-kody-optional-review/kodus-sandbox-prep-report.json`.
- Verifier checkpoint 1b: approved revision 1; open findings 0; next actor human.
- Operator approved proceeding with Docker sandbox prep helper/runbook.
- Verifier checkpoint 1c revision 1 requested fixes CK1C-001 and KISS-001.
- Fixes applied: repo-local work-dir guard before clone/secret generation; result helper parameter count resolved; focused tests added.
- Verifier checkpoint 1c revision 2: approved; open findings 0; next actor human.
- Operator asked coder to run the Docker startup on this host.
- Docker startup result: passed with status `running` using `/snap/bin/docker` and sandbox path `/home/hyperbots/agentops-kodus-101/docker-sandbox`.
- Live smoke: web UI returned 200 at `http://127.0.0.1:13000`; container-to-gateway smoke from `kodus_api` reached `/v1/models` and `/v1/chat/completions` through Claude CLI.
- Verifier checkpoint 1d revision 1 requested fixes CK1D-001 and CK1D-002.
- Fixes applied: published service ports are now loopback-bound, gateway listens on Docker host-gateway IP only, stale/unlisted log artifacts removed, and prior RabbitMQ QueueBind errors are documented as a sample-review readiness risk.
- Private live smoke: web UI returned 200 at `http://127.0.0.1:13000`; container-to-gateway smoke returned `private-gateway-ok`; relevant listeners are loopback or `172.17.0.1` only.
- Verifier checkpoint 1d revision 2 requested fixes KISS-002 and CK1D-003.
- Fixes applied: compose override moved out of oversized function, unused import removed, runbook smoke now targets `DOCKER_HOST_GATEWAY`, and runbook gateway smoke succeeded.
- Verifier checkpoint 1d revision 3: approved; open findings 0; next actor human.
- Remaining gate: sample Kodus review/log inspection before Sprint 1+ work.

## 2026-06-29 — Live Kodus sample PR review

- Status: sample review path passed; Sprint 0 remains blocked by log privacy. Evidence in `kodus-sample-review-pr173.md`.
- Created temporary PR `https://github.com/hyperbotsx/agentops-harness/pull/173` from branch `test/kodus-smoke-pr172-20260629201910`.
- PR purpose: non-merge smoke test; intentionally reverted already-merged PR #172 to create an open reviewable diff.
- Trigger: posted `@kody start-review --force` and injected the local `issue_comment` webhook into self-hosted Kodus.
- Result: Kodus completed PR #173 with `status=success`, posted one review, and created one line comment.
- Model route evidence: Kodus logs recorded `openai_compatible:claude-cli` for both generalist and rules agents.
- Log-privacy result: failed; live Kodus application/database-query logs included raw PR patch and generated suggestion content during the sample window.
- Cleanup: PR #173 closed after validation; remote test branch deleted; no merge performed.
- Follow-up: gateway should gain per-request sanitized logging before treating route evidence as production-grade observability; Kodus source/suggestion logging must be suppressed or explicitly accepted before Sprint 1.

## 2026-06-29 — Kodus log-privacy mitigation rerun

- Status: passed for bounded Docker-log smoke; evidence in `kodus-log-privacy-rerun-pr174.md`.
- Mitigation: local Kodus `.env` set `API_DATABASE_ENV=production` and `API_DATABASE_DISABLE_SSL=true`; `api`, `worker`, and `webhooks` were force-recreated.
- Durable helper updated: future sandbox env generation now writes `API_DATABASE_ENV=production` and `API_DATABASE_DISABLE_SSL=true`.
- Created temporary PR `https://github.com/hyperbotsx/agentops-harness/pull/174` from branch `test/kodus-log-privacy-pr172-20260629204122`.
- Result: Kodus completed PR #174 with `status=success`, posted one review, and created one line comment.
- Model route evidence: Kodus logs recorded `openai_compatible:claude-cli` for both generalist and rules agents.
- Log-privacy result: checked Docker logs from review trigger time returned zero matches for `Mongoose:`, `pullRequests.bulkWrite`, `diff --git`, raw patch markers, and generated suggestion text markers.
- Cleanup: PR #174 closed after validation; remote test branch deleted; no merge performed.
- Remaining gates: legal/policy approval for CLI-as-local-gateway usage, auth-refresh validation, concurrency/rate-limit validation, and sanitized gateway per-request observability.

## 2026-06-29 — Gateway observability and operational validation

- Status: partial pass; evidence in `kodus-operational-validation.md`.
- Human approval: operator explicitly approved Claude/Codex CLI usage for the local gateway experiment.
- Sanitized gateway observability: implemented per-request JSON metadata logs with allowlisted fields only; prompts/source are not logged.
- Live gateway smoke: `kodus_api` reached `/v1/models` and `/v1/chat/completions`; Claude CLI returned 200 and gateway log contained sanitized request metadata only.
- Timeout/fail-closed validation: fake slow Claude command returned `502 {"error": "TimeoutExpired"}` with zero prompt/response leakage hits in gateway logs.
- Concurrency smoke: echo backend handled five concurrent chat requests with five 200 responses and zero private prompt leakage hits.
- Rate-limit smoke: with `--max-concurrency 1 --queue-timeout 0.5`, two concurrent slow requests returned `[200, 429]`, logged `queued_ms`, and had zero private prompt leakage hits.
- Live PR #175 token smoke exposed that the 30s live queue timeout was too short for Kodus parallel agents; the gateway default was raised to 600s before rerun.
- PR #175 rerun with `--queue-timeout 600` completed with `status=success`; gateway logs showed queued requests waited (`queued_ms=171354` and `queued_ms=50938`) and returned 200.
- Token replacement validation: operator replaced Kodus GitHub token with a 7-day token; PR #175 proved Kodus could still read PR data and post review output.
- Cleanup: PR #175 closed after validation; remote test branch deleted; no merge performed.
- Codex direct gateway smoke: `kodus_api` to `172.17.0.1:18083` returned 200 for `/v1/models` and 200 `codex-smoke-ok` for `/v1/chat/completions`; gateway prompt-marker leakage grep had zero hits.
- Codex PR smoke: temporarily set `API_LLM_PROVIDER_MODEL=codex-cli` and live gateway `--backend codex`; PR #176 completed with `status=success`, one review, queued 200 responses, zero gateway raw patch/source marker hits, and zero Mongoose/raw patch docker log hits.
- Codex cleanup: PR #176 closed, remote test branch deleted, no merge performed, live Kodus config restored to `API_LLM_PROVIDER_MODEL=claude-cli`, and live gateway restored to `--backend claude`.
- Remaining limits: token expiry/refresh is not fully validated until expiry or forced-expiry is available.
- Sprint 1 advisory pilot plan drafted in `docs/kodus-kody-sprint1-advisory-pilot.md`: Claude primary reviewer, Codex fallback/comparison, manual advisory-only triggers, no required checks/branch protection/debt automation.
- Completed page Kody trigger added: rows with open implementation PRs can call `/completed-work/kodus-review`, post `@kody start-review`, and relay the local issue-comment webhook to private Kodus; live closed/merged PRs and PR URL/number mismatches fail closed before commenting.
- PR #177 first Kody attempt exposed large-prompt gateway failure: Claude prompt via argv caused `OSError`/Bad Gateway. Fixed by passing the Claude prompt through stdin; verifier approved checkpoint 1m and bounded bug-check passed.
- PR #177 Kody advisory findings addressed in checkpoint 1n: Codex prompts now use stdin (`codex exec -` confirmed by CLI help), gateway diagnostics use the logging module with sanitized JSON metadata, Completed-page Kody trigger uses async `execFile`/`fetch`, and webhook relay failures best-effort delete the just-posted trigger comment.
- Validation for checkpoint 1n passed: Python unit tests, Python compile, Term Control typecheck, focused Term Control tests, and `git diff --check`.
- Verifier checkpoint 1n implementation review passed with zero findings; verifier default bug-check passed with zero findings.
- Commit `f6b9fb3` pushed. Post-push Kody rerun reached the updated gateway but the live `--timeout 240` setting was too low for the larger PR #177 generalist prompt, producing `TimeoutExpired`/Bad Gateway; live gateway was restarted with `--timeout 900 --queue-timeout 1200` for the next local rerun.
- Follow-up Kody finding KODY-005 addressed: `kodus_sprint0` now emits logging-module console output using a public payload that omits raw captured command stdout/stderr text and includes only byte counts; explicit local `--report` evidence remains unchanged.
- Validation for checkpoint 1o passed: Python unit tests (15), Python compile, Term Control typecheck, focused Term Control tests, and `git diff --check`.
- Checkpoint 1o revision 1 verifier requested CK1O-001: clone/secret-generation failure exceptions could still expose captured stdout/stderr. Revision fixed those errors to report command name plus return code only; focused tests prove raw stdout/stderr markers are omitted. Validation rerun passed with 17 Python tests plus the same compile/typecheck/focused Term Control/diff checks.
- Checkpoint 1o revision 2 verifier requested CK1O-002: public error strings still exposed full command arguments. Revision fixed public command labels to use only the executable basename plus return code; focused tests prove raw stdout/stderr and command-argument `TOKEN` markers are omitted. Python tests, compile, and `git diff --check` reran cleanly.
- Checkpoint 1o revision 3 verifier review passed with zero findings; default bug-check passed with zero findings.
- PR #177 was externally merged at `2026-06-29T22:07:14Z` while checkpoint 1o follow-up was in progress. The follow-up fix is verifier-approved locally, but the planned push/rerun cycle against PR #177 is blocked because that PR is no longer open.
