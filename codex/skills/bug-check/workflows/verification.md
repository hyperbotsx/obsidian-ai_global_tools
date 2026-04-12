# Verification

Use this to turn candidate findings into high-signal review output.

## Entry Criteria

- There is at least one candidate finding, uncertainty, or testing gap.

## Actions

1. Re-read the exact lines.
   Confirm the candidate on the source itself, not on memory from earlier scanning.
2. State the trigger condition.
   Name the input, state, timing, or configuration needed for the bug to happen.
3. State the failure mechanism.
   Explain what specifically goes wrong and why the code allows it.
4. Assign the confidence tag.
   Use:
   - `confirmed`
   - `probable`
   - `needs_repro`
5. Attach the test shape.
   Add the existing covering test or the missing-test shape.
6. Delete weak findings.
   If the evidence no longer holds after rereading, remove it rather than downgrading it into vague prose.

## Output Order

1. Findings ordered by severity
2. Open questions or assumptions
3. Testing gaps

## Minimum Finding Template

- `Severity`:
- `Confidence`:
- `Location`:
- `Trigger`:
- `Failure mechanism`:
- `Impact`:
- `Test shape`:

## Exit Criteria

- Every surviving finding is actionable.
- The review contains no filler summary before the findings.
- False positives have been reduced by explicit verification.
