---
name: modula-runner-merge
description: The correct, repeatable way to merge a PR into main on the PUBLIC ModulaStack/modula-runner repo — always squash, with a rich hand-written message, then the exact closeout. Use before merging anything on modula-runner, or when asked how to merge/land/close out a runner PR. Triggers on merge runner, squash merge, land the runner PR, close out modula-runner, merge to main runner.
---

# Merging on modula-runner (public repo) — always squash

`ModulaStack/modula-runner` is **public from its first commit**, and its GitHub mirror
(`github.com/modulastack/modula-runner`, `sync_on_commit`) shows `main` to the world. So the
one rule this skill exists to enforce: **every PR lands on `main` as a single squash commit
with a hand-written message.** Never a merge commit, never the forge's default.

## Why squash here (and why the default is wrong)

- **The default merge style on this repo is `merge`, not squash.** A plain merge drags every
  branch commit onto `main`. CP-1 was merged that way, and its seventeen `fix(runner): Nth
  review round` commits are now permanently visible on public `main` — the exact mess to avoid.
  History on a public repo cannot be rewritten to undo it, so the only lever is to never repeat
  it: choose squash **deliberately every time**, or set the repo default to squash (below).
- **"History is the trust artifact" is still satisfied.** The repo's README says history is the
  trust artifact — but that artifact is the *public PR*: all commits, every review round, and
  the reasoned routing comments stay visible on the forge and mirror forever. Squash keeps
  `main` a clean one-commit-per-slice record while the granular audit trail lives in the PR.
- A squash commit is a *fresh* commit, so the branch name never appears in `main`'s history —
  the squash **message** is the only public artifact. That makes the message load-bearing.

## Preconditions — refuse to merge without all of them

1. **The operator said merge, explicitly, for this PR.** The agent never merges on its own
   initiative. "Review is clean" is not "merge it."
2. **A review round returned zero findings**, confirmed against artifacts (execution complete,
   zero new review objects, no in-flight review) — not assumed.
3. **Gate green at the exact head being merged** (`npm run gate`), and the working tree clean.
4. **Not already merged**; branch head == origin head.

## One-time hardening (do this once, then it protects every future merge)

Set the repo default so the wrong button can't be clicked by accident:

```bash
curl -sS -X PATCH "$AGENTOPS_FORGE_FORGEJO_URL/api/v1/repos/ModulaStack/modula-runner" \
  -H "Authorization: token $AGENTOPS_FORGE_FORGEJO_TOKEN" -H "Content-Type: application/json" \
  -d '{"default_merge_style":"squash"}'
```

This changes the default; it does not remove the per-merge responsibility to pass a proper
message (the forge otherwise auto-builds the squash body by concatenating every commit message
— that concatenation IS the mess).

## The merge — squash with a hand-written message

Write the title and body yourself. Do **not** accept the forge's auto-generated squash body.
`MergeMessageField` replaces it entirely.

```bash
# PR number and the two message halves are the only things that change per merge.
PR=4
TITLE='feat(runner): CP-2 — pty host and worktree provisioning behind the wire contract'
BODY="$(cat /path/to/squash-message-body.txt)"   # the rich body — see template below

python3 - "$PR" "$TITLE" <<'PY' > /tmp/runner-merge.json
import json, sys
pr, title = sys.argv[1], sys.argv[2]
body = open('/path/to/squash-message-body.txt').read()
json.dump({"Do":"squash","MergeTitleField":title,"MergeMessageField":body,
           "delete_branch_after_merge": False}, open('/tmp/runner-merge.json','w'))
PY

curl -sS -X POST "$AGENTOPS_FORGE_FORGEJO_URL/api/v1/repos/ModulaStack/modula-runner/pulls/$PR/merge" \
  -H "Authorization: token $AGENTOPS_FORGE_FORGEJO_TOKEN" -H "Content-Type: application/json" \
  -d @/tmp/runner-merge.json
```

- `Do: "squash"` is mandatory. `merge`/`rebase` are forbidden on this repo.
- `delete_branch_after_merge: false` — the closeout deletes the branch, gated on ancestry (below).
  Letting the forge auto-delete skips the local-main-first ordering that makes deletion safe.
- **Attribution check before you send:** the message must carry no `Co-Authored-By` trailer and
  no mention of Claude/Anthropic/any tool (house convention). Branch commits here are
  single-author with no trailers, so a clean `MergeMessageField` stays clean — but *verify the
  body you pass*, because the forge's auto-body would reintroduce whatever the commits carried.

If merging through the web UI instead: pick **"Squash and merge"**, then **replace the entire
auto-filled message** with the hand-written title and body, and confirm no co-author lines.

## Squash message standard

The message is the public face of the slice on `main` and the mirror. It must read as a single
coherent feature commit, in the same engineering voice as the repo's docs.

- **Title:** `type(scope): <slice> — <one-line what it delivers>`, conventional-commit form,
  naming the checkpoint (e.g. `CP-2`). ≤ ~72 chars for the subject.
- **Body:** what the slice delivers and why, as prose or tight bullets — the components, the
  contract it implements, the security/robustness invariants, and the protocol-versioning note
  if the protocol changed. End with a one-line pointer to the PR for the full history. Do **not**
  enumerate review rounds or frame the work as churn; describe the result.
- No tool attribution, no personal emails, no internal business context — engineering content only.

### Worked template (CP-2, ready to use)

Title:
```
feat(runner): CP-2 — pty host and worktree provisioning behind the wire contract
```
Body: see `squash-message-cp2.txt` beside this skill.

## Post-merge closeout (modula-runner) — in this order

The order is the point: update local `main` first, gate branch deletion on ancestry, then sync
the mirror. (Same discipline as the house `forge-closeout` skill, with modula-runner's paths.)

1. **Update the canonical checkout's `main` first.** `main` is checked out at
   `/mnt/hyperliquid-data/projects/repos/modula-runner`, so `git fetch origin main:main` cannot
   update it (git refuses to move a checked-out branch's ref). Use:
   ```bash
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner fetch origin
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner merge --ff-only origin/main
   ```
   Never `checkout`/`switch` branches there; never leave it dirty.

2. **Then delete the merged branch, ancestor-gated.** `git branch -d` checks merged-ness against
   *local* refs, so it only works after step 1. Gate the deletion explicitly:
   ```bash
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner merge-base --is-ancestor <head> origin/main && echo ANCESTOR-OK
   ```
   Only on `ANCESTOR-OK`: remove the worktree, then delete the local and remote branch.
   ```bash
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner worktree remove /mnt/hyperliquid-data/projects/worktrees/modula-runner-<lane>
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner branch -d <branch>
   git -C /mnt/hyperliquid-data/projects/repos/modula-runner push origin --delete <branch>   # if not auto-deleted
   ```
   A squash means the branch's commits are NOT literal ancestors of the squash commit, so
   `-d`/`--is-ancestor` will report not-merged. That is expected for squash: confirm the squash
   commit is on `main` and the PR shows "merged", then delete with `-D` **only** after that
   confirmation. (This is the one place squash legitimately needs `-D`; never use `-D` to paper
   over a stale local main.)

3. **Then refresh the public mirror.** `sync_on_commit` is on (8h fallback), so it updates on its
   own, but trigger it so the mirror is current immediately:
   ```bash
   curl -sS -X POST "$AGENTOPS_FORGE_FORGEJO_URL/api/v1/repos/ModulaStack/modula-runner/push_mirrors-sync" \
     -H "Authorization: token $AGENTOPS_FORGE_FORGEJO_TOKEN"
   ```

## Verify after closeout

- `main` on the forge shows exactly one new commit (the squash), with the hand-written message
  and no co-author lines.
- `git -C repos/modula-runner log --oneline -3` shows the squash commit at the tip, none of the
  branch's fixup commits.
- The mirror (`github.com/modulastack/modula-runner`) shows the same single commit.
- The PR is marked merged; the branch is gone (remote, local, worktree).

## Hard boundaries

- **Never rewrite public `main` history.** Whatever already landed (e.g. CP-1's fixups) stays;
  the fix is forward-only — squash from here on.
- **The agent never merges without the operator's explicit word for that specific PR.**
- Squash is mandatory on this repo. If a future slice genuinely needs its individual commits on
  `main`, that is an operator decision to state explicitly, not a default to fall into.
