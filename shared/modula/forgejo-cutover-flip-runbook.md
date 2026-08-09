# CP-4 Cutover — freeze/flip runbook (2026-07-27)

Prereqs COMPLETE before freeze:
- [x] Forgejo pulls backend merged (PR #313 — pending its Kody round)
- [x] Kody-on-Forgejo validated: FORGEJO execution + kody-bot comment on scratch PR 310
- [x] Zero open GitHub PRs (except #313 in flight)

Infrastructure facts (validated today):
- Kodus FORGEJO integration repointed: host `http://forge:3000` (container DNS), token = kody bot
  (`dev+kody@modulastack.com`, write collaborator on ModulaStack/modulastack; raw token in
  `/home/hyperbots/forge/.kody-token`, encrypted via kodus crypto.js aes-256-cbc + API_CRYPTO_KEY).
- `forge` container joined to `kodus-backend-services` network + `FORGEJO__webhook__ALLOWED_HOST_LIST=kodus-webhooks-prod`
  — BOTH now durable in /home/hyperbots/forge/docker-compose.yml.
- Repo webhook id 1 → `http://kodus-webhooks-prod:13332/forgejo/webhook` (pull_request/issue_comment/push).
- Forgejo review trigger = plain `@kody start-review` comment via forge API. REAL webhooks work —
  the kodus_agent synthesized-webhook relay is a GitHub-only workaround, not needed on Forgejo.

## Freeze sequence (order matters)

1. Merge #313 on GitHub (last GitHub PR). Local main ff.
2. DELETE ModulaStack/modulastack on forge; re-migrate from GitHub via LOOPBACK, detached
   (`nohup curl -m 3600 http://127.0.0.1:3301/api/v1/repos/migrate ...`). Acceptance: latest PR = #313,
   spot-check comment counts, issue #306 present, main sha == origin/main.
3. Re-apply post-migrate config (migration wipes it): push mirror → github.com/modulastack/modulastack
   (fine-grained PAT, 24h + manual), webhook id → kodus-webhooks-prod, kody collaborator (write).
   **GOTCHA (hit 2026-07-27): delete+remigrate assigns a NEW internal repo id. Kodus matches webhook
   events by that id — refresh the FORGEJO integration's `repositories` configValue id AFTER any
   re-migration, or every review trigger is silently dropped (webhooks deliver 200, no execution).**
4. Manual mirror sync; verify GitHub backup main sha.
5. Flip local tooling: canonical + live worktrees `git remote set-url origin` → forge (https + token,
   or SSH :2225); `git config git-town.forge-type forgejo` + forgejo-token; export
   AGENTOPS_FORGE_FORGEJO_URL/TOKEN for harness tooling.
6. Archive hyperbotsx/agentops-harness (PATCH archived=true) — LAST, after all verification.
7. First Forgejo PRs: (a) coms TTL hotfix `fix/coms-reply-handle-expiry` (canonical checkout sits on it,
   sha f94405b); (b) closeout unpin + real HTTP requester wiring (removes GITHUB_PINNED_OPERATIONS pin
   in prd_closeout_live.py — both #306 CP-4 acceptance items).

## Accepted transitional gaps
- Ledger/board regen still reads archived GitHub (read-only works) until CP-1 wave 3 removes
  Projects-v2 per D-1; new work appears only on the app board/labels.
- ~22 py + 8 TS direct `gh` call sites port incrementally (CP-1 wave 2/3); archived repo serves reads.
- PL2 (#293) lane repoints its worktree remote before pushing; its PR is born on Forgejo.

**GOTCHA (2026-07-27, webhook secrets): Forgejo's hook PATCH API silently drops `config.secret` —
signatures arrive EMPTY afterward. Always DELETE + re-CREATE a hook to set or rotate its secret,
and re-specify `events` on any hook edit (PATCH without events resets the hook to push-only).**
