---
name: house-conventions
description: House conventions for commits and product naming — commit message style with no tool attribution, and the no-hardcoded-product-names rule with the APP_NAME config pattern. Use when committing, reviewing commit messages, or naming anything user-visible in code. Triggers on commit style, commit conventions, house conventions, product naming, app name rule.
---

# House Conventions

Portable canonical copy. The worktrees `CLAUDE.md`
(`/mnt/hyperliquid-data/projects/worktrees/CLAUDE.md`) carries the same rules for
auto-loading — **update both together** when they change.

## Commit guidelines

- **No AI tool attribution, ever.** No `Co-Authored-By` bot lines; never mention an
  AI assistant, its vendor, or any generation tooling in commit messages. This applies
  doubly in public repositories.
- No personal email addresses in commits — use the designated bot/noreply identity.
- Conventional commit format: `type(scope): description`.
- Keep messages concise and focused on the change; the body explains *why* when the
  subject line cannot.

## Product naming

**Never hardcode product names in code.** Product names are placeholders until launch
and change; code must not know them.

Forbidden in code: the product name (currently the "SoldierOne" placeholder, in any
casing) in strings, variable/class/function names, database/collection/table names,
package names.

Allowed locations: an `APP_NAME` constant in config (single source of truth),
environment variables, and documentation files (README, PRD) which are cheap to update.

Pattern:

```python
# BAD
title = "SoldierOne API"
database = "soldierone"

# GOOD
from app.core.config import settings
title = f"{settings.APP_NAME} API"
database = settings.DATABASE_NAME
```

```typescript
// BAD
const title = "SoldierOne Dashboard"

// GOOD
import { APP_NAME } from '@/config'
const title = `${APP_NAME} Dashboard`
```

Technical identifiers stay generic and functional: `trading_platform` not the brand,
`codebase` for a vector collection, `indicators-core` for a package.

Exception: a repository whose public identity *is* the product (e.g. the open-source
`modula-runner`) may use its own name in its README, package scope, and binary name —
that name is the shipped identity, not a placeholder.
