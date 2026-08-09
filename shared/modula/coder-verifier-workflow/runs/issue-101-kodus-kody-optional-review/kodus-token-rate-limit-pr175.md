# Kodus token and live queue-timeout evidence — PR #175

- Test PR: https://github.com/hyperbotsx/agentops-harness/pull/175
- Branch: `test/kodus-token-smoke-pr172-20260629213203`
- Status: closed after validation; remote branch deleted.
- Purpose: validate Kodus after the operator replaced the GitHub token with a new 7-day token, and validate live gateway queue behavior.

## Result

Kodus could still read PR data and post review output using the replaced token.

First run with `--queue-timeout 30`:

- Kody posted start/completion comments and one review.
- Pipeline completed with `status=partial_error`.
- Logs showed one review agent failed with `Too Many Requests` from the gateway.
- This proved the new token worked, but showed the live queue timeout was too short for Kodus parallel agents.

Mitigation:

- Gateway default `--queue-timeout` was raised from 30 seconds to 600 seconds.
- Live gateway restarted with `--max-concurrency 1 --queue-timeout 600`.

Rerun on the same PR:

- Kody completed with `status=success`.
- No `Too Many Requests` agent failure occurred in the successful rerun.
- Gateway logs showed queued requests waited rather than failing:
  - `queued_ms=171354`, `status=200`
  - `queued_ms=50938`, `status=200`

GitHub cleanup:

- PR #175 was closed after validation.
- Remote branch `test/kodus-token-smoke-pr172-20260629213203` was deleted.
- No merge was performed.

## Safety notes

- The new token value was never pasted into chat or written to git.
- This confirms token replacement did not break the self-hosted Kodus review path.
- Expiry/refresh itself is still not fully validated until the token approaches expiry or a forced-expiry scenario is available.
