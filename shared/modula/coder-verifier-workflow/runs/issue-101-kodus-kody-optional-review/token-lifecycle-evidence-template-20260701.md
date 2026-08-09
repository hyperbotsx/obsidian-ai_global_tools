# Kodus token lifecycle evidence template — PRD #101

Use this template only for sanitized operator-run evidence. Do not paste token values, token prefixes/suffixes, screenshots with secrets, raw terminal logs, raw prompts, private transcripts, `.env` files, or live Kodus runtime config.

## Test metadata

- Date:
- Operator:
- Repository:
- Test PR:
- Token type: fine-grained PAT / GitHub App token / other
- Expiry path: natural expiry / manual revoke-delete
- Kodus deployment: local sandbox / other approved environment
- Runbook used: `docs/kodus-token-lifecycle.md`

## Pre-expiry / pre-revoke checks

- Replacement-token smoke command used: `kodus-token-smoke --repo <owner/repo> --require-write`
- Pre-expiry smoke result: pass / fail
- Advisory Kody review before expiry/revoke: pass / fail / not run
- Evidence artifact links or paths, sanitized only:
  -

## Expired / revoked behavior

- Expiry/revoke action performed outside repo: natural expiry / manual revoke-delete
- Kody behavior after expiry/revoke: fail-closed / cannot read GitHub / cannot post comment / other
- Duplicate trigger comments observed: no / yes
- Required checks or branch-protection changes observed: no / yes
- PR approval/request-changes automation observed: no / yes
- Automatic issue/debt creation observed: no / yes
- Token value leaked in logs/artifacts: no / yes
- Sanitized evidence artifact links or paths:
  -

## Replacement recovery

- Replacement-token smoke result: pass / fail
- Local Kodus configuration updated outside repository: yes / no
- Required local services restarted: yes / no
- Advisory Kody review after replacement: pass / fail
- Logs/artifacts redacted: pass / fail
- Sanitized evidence artifact links or paths:
  -

## Closeout statement

Choose one:

- Token lifecycle validation passed: expired/revoked token failed closed, replacement recovered, and no token values or forbidden automation were observed.
- Token lifecycle validation failed: details require human follow-up before broader rollout.
- Token lifecycle validation deferred: follow-up issue remains open.

## Notes

-
