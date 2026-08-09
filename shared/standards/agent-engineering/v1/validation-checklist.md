# Validation Checklist

## Pack completeness

- `README.md` states users, quick start, and source-of-truth.
- `manifest.json` lists version, canonical path, skill entrypoint, owner, consumers, inventory, and update metadata.
- `canonical-standards.md` covers philosophy, backend, frontend, styling, state, database, APIs, tests, configuration, directories, functions/modules, immutability, Exa research, exceptions, and agent workflow boundaries.
- Researcher, coder, verifier, and steward files are concise enough for agent use.
- `exception-policy.md`, `integration-guide.md`, and `update-process.md` are present.

## Policy checks

- Standards remain language-, framework-, database-, cloud-, frontend-library-, and test-runner-neutral.
- Exa research is mandatory before stack-specific structure, boilerplate, migration layout, test layout, state patterns, and design-system layout.
- Exa unavailable, blocked, stale, undated, or conflicting evidence fails closed to human or Researcher review.
- No temporary product name is hardcoded.
- No secrets, private data, raw prompts, raw transcripts, env dumps, or credentials are present.
- No PR creation, merge, deployment, production rollout, hard-blocking enforcement, approval, trading, or backtest authority is implied.

## Structure checks

- The FR-018 pack tree exists exactly or the handoff documents an approved-equivalent path adjustment.
- The shared skill entrypoint exists and points to this canonical pack instead of duplicating it.
- Any Pi wrapper is a symlink or thin pointer.
- Repo-local references point here and do not become divergent copies.

## Suggested commands

```bash
python3 -m json.tool /mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1/manifest.json >/dev/null
find -L /mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/standards/agent-engineering/v1 -maxdepth 1 -type f | sort
find -L /mnt/hyperliquid-data/projects/obisidan/AI_Global_Tools/shared/skills/agent-engineering-standards -maxdepth 1 -type f | sort
```

When a repository installs references or loaders, also run that repository's standard validation suite.
