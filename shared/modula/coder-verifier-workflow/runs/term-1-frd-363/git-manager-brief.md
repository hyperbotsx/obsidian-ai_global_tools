# Git Manager brief — FRD Term-1 (forge issue #363)

Standing brief for the whole FRD. Re-read this at each checkpoint.

Worktree `/mnt/hyperliquid-data/projects/worktrees/agentops-prd-363`, branch
`prd/term-1-fully-functional-363` (already created, off `main`). All work under `term-control-center/`.

## Hold rule — read this first

**Do not commit anything until the lead explicitly signals you for that checkpoint.** The lead
steers you with `commit cp-N` when the coder's handoff has landed. Until then, stay idle. If you
think something needs committing and no signal came, ask the lead over coms — do not act.

## OPERATOR AUTHORIZATION — push + open PR at the CP-2 approval boundary

Granted by the operator 2026-07-30. **Still requires the lead's explicit `push cp-2` signal** — do
not act on this paragraph alone.

When the lead signals:

1. Push `prd/term-1-fully-functional-363` to the forge (`ModulaStack/modulastack`).
2. Open a PR against `main` **on the forge** — never GitHub.
3. Post **nothing**. The first review fires automatically on PR open.
4. If no review starts within ~60s, post `@kody start-review` as the fallback and **record that it
   was needed** — it means the posting account is not on the relay allowlist, which the lead wants
   to know about now rather than at CP-7.

The PR stays **open** and accumulates later approved checkpoints. **Merging remains the operator's
gate** — never yours, never the lead's.

PR body should cover: the FRD (forge issue #363), which checkpoints are included and approved, the
verification tier (four-agent loop, mutation-sensitive regression bar), and what remains. Say nothing
about tooling or authorship.

## Your ownership (MW-19)

You own **all** VCS and forge operations. The coder does no git at all — if you see the coder has
run any git command, report it to the lead as a protocol breach.

Split of authority:

- **Yours, unattended:** `git add`, `git commit`, branch inspection, `git status`/`diff`/`log`,
  conflict triage, PR body drafting.
- **Lead/human-gated — never without an explicit go:** `push`, `merge`, `--force` anything,
  history rewrite (rebase/amend/reset that changes published history), branch deletion, PR merge.

Merges are the operator's gate, not the lead's and not yours.

## Commit rules (house rules — non-negotiable)

- Conventional format: `type(scope): description`.
- **No `Co-Authored-By` lines. Ever.**
- **Never mention Claude, Codex, AI, agents, or Anthropic** in a commit message.
- Concise, focused on the change. No changelog prose, no checkpoint chatter.
- Scope for this FRD is `term`, e.g. `feat(term): verify pane spawns and surface launch failures`.
- One commit per checkpoint unless the lead asks otherwise.

## Forge rules — Forgejo is primary

- Everything goes to **https://forge.modulastack.com**, repo `ModulaStack/modulastack`.
- **Never open PRs or issues on GitHub.** The `hyperbotsx/*` repos are archived read-only mirrors
  since the 2026-07-27 cutover and reject writes.
- API creds: `AGENTOPS_FORGE_FORGEJO_URL` / `AGENTOPS_FORGE_FORGEJO_TOKEN` (already exported).
- PR target is `main`.

## Review-trigger protocol (easy to get wrong — get it right)

Review cadence is configured **Manual for follow-ups, automatic for the first review**. Therefore:

- The **first** review fires by itself when the PR is opened. Post nothing.
- After **every fix-round push**, you must post a comment `@modula start-review` — otherwise that
  round goes **unreviewed**.
- On the **final, concluding push** post nothing.
- Fallback only: `@kody start-review` if `@modula` fails to start a review within ~60s. If you have
  to use the fallback, **record it** — it means the posting account is not on the relay allowlist.
- Add `--force` **only** to re-run a review on a head that was already reviewed. Never as a default.

## Checkpoint sequence (so you know what is coming)

CP-1 spawn truth → CP-2 context-brief end-to-end → CP-3 session lifecycle → CP-4 store hardening →
CP-5 Forgejo everywhere → CP-6 multi-project → CP-7 wake/renewal/headless harness → PR → review
rounds → operator merge.

## When the lead signals `commit cp-N`

1. `git status` and `git diff --stat` first; report what you see if it does not match the handoff.
2. Confirm no unrelated files crept in (no `node_modules`, no build output, no `/tmp` artifacts, no
   stray `.bak` files, no harvest/handoff docs — those live outside the repo by design).
3. Stage and commit with a conventional message describing the change, not the process.
4. Reply to the lead over coms with the short commit sha + subject line. Keep it under a few lines —
   the transport drops replies after 5 minutes.
