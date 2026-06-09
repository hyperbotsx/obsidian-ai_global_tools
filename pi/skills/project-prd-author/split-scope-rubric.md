# Split-Scope Rubric

Recommend split PRDs when the request spans ownership boundaries that would make one implementation risky, slow to verify, or unclear to assign.

## Split Signals

- Frontend plus backend/API contract.
- Frontend plus data pipeline or provider behavior.
- Data ingestion/export plus training/model import.
- Trading/backtest plus data contracts or validation gates.
- Admin/orchestration plus product-code changes.
- Shared schema/migration plus multiple UI or service consumers.
- Preview/deployment configuration plus application code.
- Any scope where different agent labels or worktrees own distinct parts.

## Single-PRD Signals

- One owner, one worktree, and one validation surface.
- A documentation-only or process-only change with one authority boundary.
- A small UX copy or configuration change that does not change contracts.
- A follow-up issue that intentionally captures a single bounded slice.

## Required Split Plan Output

```text
I recommend splitting this into N PRDs because <reason>.

1. <Title>
   - Owner/agent label: <profile value>
   - Worktree/code home: <profile value>
   - Dependency order: <first | after #... | parallel-safe>
   - Shared contracts/integration points: <API/schema/data/preview>
   - Preview/manual verification: <required/optional/not applicable>

2. <Title>
   ...
```

## Parallel Safety

- Sequential by default when contracts, migrations, validation gates, or authority boundaries must be established first.
- Parallel-safe only when scopes share no files, do not depend on each other's contracts, and have independent verifier checkpoints.
- If unsure, recommend sequential execution and ask the human whether to trade speed for coordination risk.
