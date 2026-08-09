# Coder/Verifier Coms Reliability Note

## Observed During PRD #22

The coder/verifier transport repeatedly failed to produce machine-readable verdicts even when the verifier appeared to complete the review in its pane.

Observed failure modes:

- `coms_await` returned `response not valid JSON`.
- `coms_await` returned `No result provided`.
- `coms_await` returned non-verdict text such as `(see attached image)`.
- `verifier-report.md` sometimes remained on the previous checkpoint after the verifier pane produced a compact verdict in the visible UI.
- Human had to paste compact verifier JSON back into the coder pane to unblock checkpoints.

## Likely Root Cause Area

The transport captures the verifier's last assistant message for the inbound turn. If the verifier produces prose, UI artifacts, image references, or does not finish the turn with only the compact JSON object, the coder receives an invalid response even if the verifier's review work happened locally.

There may also be a mismatch between the verifier pane's visible output and the coms response capture path when the pane is interrupted, renders an attachment placeholder, or fails to update the report before replying.

## Follow-up Needed

Create a separate hardening task for the coder/verifier coms workflow:

- Add a deterministic verifier reply wrapper that emits machine-status JSON only.
- Add a local validation hook before verifier reply completion.
- Make report update and verdict response atomic or explicitly ordered.
- Record transport failures with raw response metadata outside the PRD implementation artifacts.
- Add a recovery command for re-sending the last valid Machine Status block from `verifier-report.md`.

Do not expand PRD #22 scope to fix this transport root cause.
