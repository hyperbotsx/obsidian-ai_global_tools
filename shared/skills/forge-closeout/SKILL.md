---
name: forge-closeout
description: The stable forge conventions — the @modula review-trigger convention and the post-merge closeout sequence (update main first, ancestor-gate branch deletion, mirror sync) with the reasoning that makes the order mandatory. Use after any forge merge, or when triggering/re-triggering a code review. Triggers on closeout, post-merge, merge closeout, delete merged branch, start-review, trigger review.
---

# Forge Conventions: Review Triggers and Post-Merge Closeout

Portable canonical copy of the **stable** forge procedures. Volatile operational truth —
review cadence, pipeline latency, allowlist state — lives ONLY in the worktrees
`CLAUDE.md` (`/mnt/hyperliquid-data/projects/worktrees/CLAUDE.md`), which is corrected
by observation and must not be duplicated here. When the *procedures* below change,
update both files together.

## Review trigger convention

- **Everyone posts `@modula start-review`** — humans and automation alike. Brand-neutral
  is the point; the review-event notifier relays it, which requires the posting account
  to be on the relay allowlist.
- **`@kody start-review` is the fallback only** — it reaches the reviewer directly
  without the relay. Before concluding `@modula` failed, check whether a review is
  already running (see `CLAUDE.md` for the live liveness query): an in-flight review
  being deduped looks identical to a dropped trigger.
- Never post a trigger after an ordinary fix-round push where auto-review-on-push is
  active — it burns a redundant round. Trigger only to re-run on an already-reviewed
  head, or when the execution ledger shows no run for your push.
- Record any `@modula` relay failure — it usually means the poster is not on the
  relay allowlist, or the webhook secret/event wiring on that repo is broken.

## Post-merge closeout — in this order, every forge merge

The order is the point; each step's failure mode is caused by skipping the previous one.

1. **Update the local canonical main FIRST.** If `main` is checked out in the canonical
   working tree (typical for a worktree-based setup), `git fetch origin main:main`
   CANNOT work — git refuses to update a checked-out branch's ref. Use:
   `git -C <canonical-checkout> fetch origin` then
   `git -C <canonical-checkout> merge --ff-only origin/main`.
   Never switch branches in the canonical tree and never leave it dirty — updating main
   in place is expected; switching it is not.
2. **Then delete the merged branch** (remote + local + worktree). `git branch -d`
   evaluates merged-ness against LOCAL refs, so with local main stale it refuses
   correctly — and looks like a `-D` situation when it is not. Gate every deletion on:
   `git merge-base --is-ancestor <head> origin/main && echo ANCESTOR-OK`.
   **`-D` is never the remedy for staleness; a fetch is.**
3. **Then sync the public mirror.** Repos with `sync_on_commit: true` on their push
   mirror sync automatically — verify via `GET /api/v1/repos/<owner>/<repo>/push_mirrors`
   rather than assuming. Otherwise trigger:
   `POST /api/v1/repos/<owner>/<repo>/push_mirrors-sync`.

Why this is written down: the fetch-after-delete ordering has produced false `-D`
escalations more than once, and one granted `-D` that happened to work made the wrong
lever look correct.

## Concrete anchors (this infrastructure)

- Forge: `https://forge.modulastack.com` · API auth via `AGENTOPS_FORGE_FORGEJO_URL` /
  `AGENTOPS_FORGE_FORGEJO_TOKEN` (exported in `~/.bashrc`).
- Canonical checkouts under `/mnt/hyperliquid-data/projects/repos/`, worktrees under
  `/mnt/hyperliquid-data/projects/worktrees/`.
- Merges happen only on the operator's explicit word — closeout starts after, never
  before.
