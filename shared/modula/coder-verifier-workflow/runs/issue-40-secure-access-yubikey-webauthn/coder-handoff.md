# Coder Handoff: Issue #40 Secure Access Layer with YubiKey WebAuthn

## Task source

- GitHub issue: https://github.com/hyperbotsx/agentops-harness/issues/40
- Branch: `feat/secure-access-yubikey-webauthn-40`
- Worktree: `/mnt/hyperliquid-data/projects/worktrees/agentops-term`
- Status: final verifier checkpoint and bug-check approved.

## Pre-edit status

- `git status --short --branch`: clean before task work.
- Pre-existing dirty files: none.
- Initial peer pings before edits: researcher freshness consult complete; verifier live; steward live.

## Scope controls from PRD

Allowed paths:

- Repository documentation for security architecture, provider decisions, templates, and runbooks.
- Non-secret Authentik-first deployment templates and runbooks.
- Authelia fallback notes if useful for comparison or rollback.
- nginx/reverse-proxy config templates for AgentOps routes through the selected auth gateway.
- Validation scripts for headers, auth enforcement, route reachability, WebSocket protection, and external exposure checks.
- Safe profile/schema fields only if needed and without secrets.
- Run artifacts under this folder.

Forbidden:

- Live host mutations, sudo, nginx reloads, DNS/firewall/certificate changes, Docker/systemd changes, or identity-provider bootstrap.
- Secrets, `.env` files, private keys, recovery codes, bootstrap credentials, cookies, provider tokens, raw transcripts, or private account data.
- Removing existing auth before replacement validation.
- Fail-open bypasses for Term Control, review APIs, completion actions, browser live feed, CDP/noVNC/VNC, or WebSocket endpoints.
- SMS/voice/email-only MFA for production AgentOps access.
- PR creation, merge, deploy, production-readiness claims, trading, paper trading, backtests, or bypassing human gates.

Required validation:

- Static scan for committed secrets and accidental `.env`/key material.
- Config lint for nginx/auth gateway templates where tooling is available.
- Header/auth/reachability/WebSocket validation scripts in dry-run mode.
- `git diff --check`.
- Tests only if code is introduced.

Stop condition:

- Stop after final verifier bug-check approval and validation, or human escalation. Do not open a PR unless explicitly asked.

## Verifier checkpoints

1. Architecture/provider decision.
2. Identity/WebAuthn policy templates.
3. Reverse proxy/security route templates.
4. Deployment/runbook/rollback validation.
5. Final security validation.

## Research-first summary

Researcher was consulted before implementation on 2026-06-19 for the PRD's named research-first surfaces.

Key dated/source-cited guidance recorded for implementation:

- OWASP MFA, Authentication, and Session Management cheat sheets remain the baseline: require MFA for all users, prefer phishing-resistant FIDO2/WebAuthn/passkeys, avoid SMS/PSTN for high-value apps, require reauthentication for sensitive actions and risk events, rotate/invalidate sessions after reauth, and use Secure/HttpOnly/SameSite cookies with server-side idle/absolute timeouts.
- Authentik docs support YubiKey/platform passkey WebAuthn stages, user verification/resident-key controls, validation stages that can deny/configure rather than skip missing authenticators, and proxy provider forward-auth. Single-application forward-auth is preferred for per-app AgentOps policies.
- Authelia is a credible lightweight fallback. Current docs note multiple WebAuthn credentials since v4.38.0 and passwordless passkeys since v4.39.0; passkeys may count as one factor by default, so two-factor policy behavior must be documented if used.
- Kanidm is a comparator because it treats passkeys/WebAuthn as preferred unphishable MFA and emphasizes correct domain/origin alignment for WebAuthn/OAuth2.
- WireGuard/private access remains preferred. Headscale ACLs must be explicit because omitted ACLs can mean allow-all; DERP is connectivity fallback, not a security boundary. Public firewall exposure should be minimized.
- nginx WebSocket proxying requires explicit Upgrade/Connection forwarding and timeouts. WebSockets also need strict origin allowlists, authentication before connect, message-level authorization, and size/rate limits.
- Chrome CDP remote debugging and noVNC/websockify must never be public unauthenticated surfaces; CDP should remain localhost/private-network only and noVNC tunnels must sit behind TLS/auth/token routing.
- Templates/runbooks must use placeholders only for domains, cookie names, client IDs, CIDRs, policy names, and paths; no private keys, tokens, recovery codes, or real user identifiers.

Primary sources cited by Researcher:

- OWASP MFA Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- Authentik WebAuthn stage: https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_webauthn/
- Authentik validate stage: https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/authenticator_validate/
- Authentik forward auth: https://docs.goauthentik.io/add-secure-apps/providers/proxy/forward_auth/
- Authelia WebAuthn/security key docs: https://www.authelia.com/overview/authentication/security-key/ and https://www.authelia.com/reference/guides/webauthn/
- Kanidm credentials docs: https://kanidm.github.io/kanidm/stable/accounts/authentication_and_credentials.html
- Headscale ACL docs v0.27.1: http://headscale.net/0.27.1/ref/acls/
- nginx WebSocket proxy docs: https://nginx.org/en/docs/http/websocket.html
- OWASP WebSocket Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html
- Chrome remote debugging profile hardening dated 2025-03-17: https://developer.chrome.com/blog/remote-debugging-port

## Checkpoint 1 implementation notes

Changed files:

- `docs/secure-access-yubikey-webauthn.md`
- `docs/security.md`

Implemented architecture/provider decision note:

- Selects Authentik as the default provider.
- Compares Authentik, Authelia, Keycloak, and Kanidm against PRD #40.
- Documents VPN/private-access-first stance and identity-gateway-only public exposure model.
- Records fail-closed reverse-proxy and no-public-control-endpoint boundaries.
- Defines initial admin/operator/readonly role model.
- Documents WebAuthn, admin two-authenticator, SMS/email/voice MFA prohibition, TOTP break-glass limitation, session, audit, and reauth baseline.
- Reiterates repository-only scope and human-confirmed ops gates for deployment mutations.

Verifier approved checkpoint 1 revision 1 with zero findings.

## Checkpoint 2 implementation notes

Changed files:

- `config/templates/secure-access/authentik-agentops-identity.template.yaml`
- `docs/runbooks/secure-access-identity.md`

Implemented identity/WebAuthn policy templates and runbook:

- Adds non-secret Authentik identity policy template with placeholder-only origin, group, WebAuthn, session, audit, and recovery values.
- Defines `agentops-admin`, `agentops-operator`, and `agentops-readonly` groups and initial access intent.
- Requires WebAuthn/FIDO2/passkeys for interactive users and two owner/admin authenticators before cutover.
- Forbids SMS, voice, and email-only MFA for ready status.
- Keeps TOTP disabled by default and limited to documented temporary break-glass use.
- Documents reauthentication, session hardening, factor change audit, suspicious-event log review, lost-factor recovery, and compromised user/device revocation.

Verifier approved checkpoint 2 revision 1 with zero findings.

## Checkpoint 3 implementation notes

Changed files:

- `config/templates/secure-access/nginx-agentops-authentik-forward-auth.template.conf`
- `config/templates/secure-access/agentops-route-protection.template.yaml`
- `docs/secure-access-yubikey-webauthn.md`

Implemented reverse-proxy/security route templates:

- Adds Authentik forward-auth nginx template with global auth request, sign-in redirect, outpost route, secure headers, noindex behavior, loopback upstream placeholders, and fail-closed intent.
- Protects static, `/admin/`, `/api/admin/`, `/api/review/`, `/api/board/`, broad `/api/`, terminal REST, completion, and terminal WebSocket paths behind identity gateway.
- Preserves Term Control app-local token checks by routing to the loopback service rather than replacing backend authorization.
- Adds WebSocket upgrade forwarding, long timeouts, and strict Origin allowlist check for `/term/ws`.
- Adds explicit direct-public denial for CDP/devtools/json/noVNC/VNC-style paths.
- Adds route inventory with group intent, anonymous access denial, app token preservation, and forbidden public surfaces.

Checkpoint 3 revision 2 addressed verifier findings:

- V40-CP3-001: outpost auth subrequest, sign-in redirect, and `/outpost.goauthentik.io/` routes now set `auth_request off;` so Authentik start/callback/outpost paths do not inherit the protected app auth check.
- V40-CP3-002: added `authentik-agentops-route-authorization.template.py` as the concrete fail-closed Authentik provider-policy enforcement point; route inventory now points to it and requires deny-on-missing-groups and deny-unknown-routes. nginx overwrites `X-Authentik-*` app headers with values from the auth subrequest and clears extra identity headers.
- V40-CP3-003: tightened policy route matching so unknown static paths deny, `/api/board/...` allows readonly, admin/operator routes deny insufficient groups, and CDP/noVNC/VNC prefixes deny all app groups.

Verifier approved checkpoint 3 revision 3 with zero findings.

## Checkpoint 4 implementation notes

Changed files:

- `docs/runbooks/secure-access-deployment.md`
- `config/templates/secure-access/validate-secure-access-templates.py`
- `docs/secure-access-yubikey-webauthn.md`

Implemented deployment/runbook/rollback validation:

- Adds human-gated deployment phases covering repository preflight, private-network gate, identity bootstrap, WebAuthn enrollment, reverse-proxy dry run, cutover, external reachability validation, and rollback.
- Explicitly blocks agent-executed host mutations and requires human confirmation before firewall, VPN, DNS, certificate, Docker, systemd, nginx, Authentik, or identity changes.
- Documents WireGuard/Headscale private-access preflight and explicit Headscale ACL expectation.
- Documents external unauthenticated HTTP checks and WebSocket denial/authenticated smoke validation expectations.
- Provides rollback steps that prefer disabling public access and allow prior Basic Auth only as a temporary secondary guard while preserving Term Control app-local checks.
- Adds local validator for required files, secret-like markers, nginx auth/outpost/WebSocket/header controls, route inventory controls, and policy behavior probes.

Verifier approved checkpoint 4 revision 1 with zero findings.

## Checkpoint 5 implementation notes

Changed files:

- `docs/runbooks/secure-access-validation.md`
- `config/templates/secure-access/validate-secure-access-templates.py`
- `docs/secure-access-yubikey-webauthn.md`

Implemented final security validation runbook and updated validator coverage:

- Adds final local repository validation, template assertions, manual deployment validation, WebAuthn validation, WebSocket validation, audit validation, app functionality validation, and readiness caveat.
- Extends the local validator to require the final validation runbook.
- Keeps validation repository-only and explicitly states it does not authorize live host mutation or production readiness claims.

Checkpoint 5 revision 2 addressed verifier finding:

- V40-FINAL-001: repeated the trusted Authentik header overwrite/clear controls in `/term/ws` and `/term/` because those locations define local WebSocket `proxy_set_header` directives and do not inherit parent proxy headers. Extended the validator to fail any AgentOps upstream location with local `proxy_set_header` directives that omits the `X-Authentik-*` overwrite/clear set.

## Validation log

- 2026-06-19 checkpoint 1: documentation-only change; no product code introduced.
- `git diff --check` passed.
- 2026-06-19 checkpoint 2: docs/template-only change; no product code introduced.
- Secret-like marker scan passed for secure-access docs/templates (`BEGIN PRIVATE KEY`, `BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `ghp_`, `xoxb-`, `AKIA`).
- 2026-06-19 checkpoint 3: reverse-proxy template static checks passed for Authentik auth request, WebSocket route, Upgrade header, Origin denial, CDP denial, secure headers, noindex, route anonymous denial, app token preservation, and browser/CDP route inventory controls.
- 2026-06-19 checkpoint 3 revision 2: policy template compiled with `python3 -m py_compile`; generated `__pycache__` removed.
- 2026-06-19 checkpoint 3 revision 2: static checks passed for outpost `auth_request off` exceptions, trusted identity header overwrite/clear behavior, route policy enforcement pointer, deny-on-missing-groups, deny-unknown-routes, and Authentik policy admin/operator/readonly/denied-prefix controls.
- `git diff --check` passed after checkpoint 3 revision 2 fixes.
- 2026-06-19 checkpoint 3 revision 3: policy behavior checks passed for unknown path deny, readonly `/api/board/status` allow, readonly review denial, operator admin denial, admin allow, operator WebSocket allow, readonly WebSocket denial, and CDP/noVNC denial for admin.
- 2026-06-19 checkpoint 3 revision 3: policy template compiled with `python3 -m py_compile`; generated `__pycache__` removed.
- `git diff --check` passed after checkpoint 3 revision 3 fixes.
- 2026-06-19 checkpoint 4: `python3 config/templates/secure-access/validate-secure-access-templates.py` passed.
- `git diff --check` passed after checkpoint 4 changes.
- 2026-06-19 checkpoint 5: `python3 config/templates/secure-access/validate-secure-access-templates.py` passed.
- 2026-06-19 checkpoint 5: final secure-access secret-like marker scan passed for docs/templates.
- 2026-06-19 checkpoint 5: no `.env`, `*.pem`, or `*.key` material found under `config` or `docs/runbooks`.
- `git diff --check` passed after checkpoint 5 changes.
- 2026-06-19 checkpoint 5 revision 2: `python3 config/templates/secure-access/validate-secure-access-templates.py` passed with location-level trusted-header regression coverage.
- 2026-06-19 checkpoint 5 revision 2: `python3 -m py_compile config/templates/secure-access/validate-secure-access-templates.py config/templates/secure-access/authentik-agentops-route-authorization.template.py` passed; generated `__pycache__` removed.
- 2026-06-19 checkpoint 5 revision 2: final secure-access secret-like marker scan passed for docs/templates.
- 2026-06-19 checkpoint 5 revision 2: no `.env`, `*.pem`, or `*.key` material found under `config` or `docs/runbooks`.
- `git diff --check` passed after checkpoint 5 revision 2 fixes.
- 2026-06-19 final post-approval validation rerun: `python3 config/templates/secure-access/validate-secure-access-templates.py` passed.
- 2026-06-19 final post-approval validation rerun: final secure-access secret-like marker scan passed for docs/templates.
- 2026-06-19 final post-approval validation rerun: no `.env`, `*.pem`, or `*.key` material found under `config` or `docs/runbooks`.
- 2026-06-19 final post-approval validation rerun: `git diff --check` passed.

## Verifier log

- Checkpoint 1 revision 1 approved with zero findings.
- Checkpoint 2 revision 1 approved with zero findings.
- Checkpoint 3 revision 1 requested V40-CP3-001 and V40-CP3-002; revision 2 requested V40-CP3-003; revision 3 approved with zero findings.
- Checkpoint 4 revision 1 approved with zero findings.
- Checkpoint 5 revision 1 requested V40-FINAL-001; revision 2 approved with zero findings and bug-check status `passed`.
