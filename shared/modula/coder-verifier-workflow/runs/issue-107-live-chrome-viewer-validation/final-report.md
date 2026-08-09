# PRD #107 — Live Chrome Viewer Post-Deploy Validation: FINAL REPORT

> Validates #97 (Frontend-Expert Live Chrome Viewer) per approved validation PRD #107.
> Method: authenticated operator session driving Chrome browser automation against the deployed
> app at https://ops.evono.me; unauthenticated route checks via curl (no cookies).
> Date: 2026-06-26. Validation branch: `test/live-chrome-viewer-validation-107`.
> **Result: FULL PASS — 16/16 checklist items.**

## Action requested (coding agent)
Commit the outstanding work and **prepare a PR** that closes out #107 and records this validation:
- Commit this report (and any **sanitized** run evidence) into the repo at a sensible location
  (e.g. `dev-plans/agentops/coder-verifier-workflow/runs/issue-107-live-chrome-viewer-validation/`).
- Open a PR titled e.g. `docs(agentops): PRD #107 live Chrome viewer validation — full pass`,
  referencing #97 and the fix chain below, and closing #107.
- Follow repo conventions (git-town, conventional commits, **no "Claude/Anthropic/Co-Authored-By" lines**).
- **Sanitize:** do not commit secrets, tokens, cookies, OAuth state, VNC creds, screenshots containing
  private data, or raw transcripts. Group IDs / status strings are fine.
- Do not change product behavior in this PR — it is documentation/closeout only. (All functional fixes
  already merged to `main`; see chain below.)

## Checklist results (16/16 PASS)
| # | Item | Result | Evidence (sanitized) |
|---|---|---|---|
| 1 | PRD Studio launches from ops.evono.me | PASS | `POST /term/launch → 200`; four-agent session for #107. |
| 2 | Frontend scenario includes a frontend-expert pane | PASS | Browser-QA (Claude) pane via force_on / "Open Browser-QA". |
| 3 | Delegate uses real Chrome integration & drives it | PASS | `interactive_auth_detected` → `claude_agent model=opus mcp=custom`; "Chrome DevTools MCP tools are loaded"; **navigated live Chrome to `http://127.0.0.1:3032/`, visible in viewer**; allowlist blocks `ops.evono.me`/`example.com`. |
| 4 | Chrome/live-view button by the pane label | PASS | `Chrome` button on BROWSER-QA pane toolbar. |
| 5 | Button opens the in-app viewer | PASS | Opens `CHROME` viewer pane. |
| 6 | Viewer shows the delegate's live Chrome session | PASS | Status `ready · novnc`; live Chrome window streamed (rendered `127.0.0.1:3032` Term Control Center page). |
| 7 | Terminal + Chrome split-screen | PASS | Terminal left / Chrome viewer right. |
| 8 | Full-screen mode + return | PASS | Full-screen toggle; `Exit full screen` returns. |
| 9 | Delegate reasoning/tool activity visible | PASS | Browser-QA pane shows live delegate reasoning + `claude_agent` activity. |
| 10 | Control states visible/understandable (view-only / agent-control / human-control) | PASS | All three confirmed: `agent-control · capture live`, `human-control · capture paused`, `view-only · capture live`. |
| 11 | Human-control pauses delegate actions + capture | PASS | `Take human control` → `human-control · capture paused · lease until <ts>` (short-lived lease). |
| 12 | Returning control resumes the workflow | PASS | `Return control to agent` → `agent-control · capture live` (capture resumed). |
| 13 | Coms label = configured Claude model, not parent | PASS | `browser-qa` peer labeled "Claude Opus 4.8"; all others `gpt-5.5`. |
| 14 | Routing by coms name, not model label | PASS | Live `coms_send`/`coms_await` use peer names; label display-only. |
| 15 | Unauthenticated browser/CDP/VNC/feed routes don't expose private content | PASS | `/term/`, `/browser-feed` → 302 Authentik; `/browser-feed/novnc`, `/cdp-screencast`, `/novnc/`, `/json/version`, `/json/list`, `/term/ws` → 403; authenticated noVNC/json return only the SPA shell. |
| 16 | No secrets/cookies/screenshots/transcripts/VNC creds/private auth saved | PASS | No tokens/OAuth state/cookies quoted or stored; Claude login not completed by the validator; evidence kept sanitized. |

## Fix chain shipped during validation (already on `main`)
1. **PR #108** (merged `93eaa87`) — resolve PRD Studio launch context: `legacy-default`/stale projectId now
   resolves to the active project; board derives `worktreePath`/`workingBranch` from the PRD body + active project.
2. **PR #109** — workspace **End session** control (`DELETE /term/groups/:id`) + **Open Browser-QA** control
   (`POST /term/groups/:id/browser-qa`); Browser-QA panes show the Chrome live-view button.
3. **PR #110** (merged `ab3c170`) + `fac8f18` — Claude auth preflight (fail-close on API/cloud billing; verify
   subscription/OAuth) and propagate the `AGENTOPS_CLAUDE_AUTH_STATUS` marker into the Browser-QA pane env
   (incl. tmux `-e` env passthrough).
4. `dc8dfac` — **activate the live browser feed** (`TERM_CONTROL_BROWSER_FEED_*` enablement; noVNC/CDP ready).
5. `f56e65c` — install **Chrome 149.0.7827.200** for the sanctioned browser runtime
   (`TERM_CONTROL_BROWSER_CHROME_BINARY`) so the chrome-devtools MCP (`--allowedUrlPattern`, needs Chrome ≥149)
   can attach; hardened the CDP proxy against downstream socket resets.

## Notes / boundaries (by design)
- Browser-QA is **bounded to localhost/preview** (`http://127.0.0.1:*` / `http://localhost:*`); it correctly
  refuses public URLs. To exercise it against richer UI, point it at a local preview server in that range.
- Feed/CDP/VNC remain **localhost-only**; the public auth boundary (Authentik) is intact.

## Optional remaining UX polish (separate, non-blocking — file as follow-ups if desired)
- In-app remediation for launch preflight failures (missing context / branch mismatch / uncommitted changes) — currently dead-end errors.
- Replace blocking `window.alert(...)` in `openBrowserQaPane`/`endSessionGroup` with non-blocking inline/toast errors.
- `endSessionGroup` spawns a default verifier+coder pair after teardown — leave an empty/relaunchable workspace instead.
- (Exposing Open Browser-QA / End session in the board overlay appears addressed — they now show in the overlay tab bar.)
