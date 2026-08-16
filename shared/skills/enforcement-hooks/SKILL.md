---
name: enforcement-hooks
description: Turn advisory guidelines into deterministic law — binary rules enforced at lifecycle events (session start, pre-compaction, pre-write, pre-commit, stop) instead of competing for attention in the context window. Covers doctrine re-injection, secret-write blocking, commit-format enforcement, file-size and variant-file guards, and periodic nudges. Harness-agnostic by design. Use when configuring how a project's rules are enforced.
---

# Enforcement Hooks

A guideline in `CLAUDE.md` / `AGENTS.md` is advisory: it is text competing for attention, and by
hour three of a session — especially after compaction — compliance drops. A **hook** is
deterministic code at a lifecycle event; it does not compete for attention because it runs
outside the model's judgment. The rule of this tier: *binary rules become law, judgment stays in
the doctrine.*

## Why this tier is engine-side (and why that is the moat)

Hook mechanisms do not port — `allowed-tools`, `disable-model-invocation`, and event hooks are
Claude-Code-only in the Agent Skills standard. So Modula does **not** rely on any harness's hooks:
the enforcement declared here is applied by **Modula's runner/verifier**, deterministically, on
Claude, Codex, Pi, or any future CLI. A portable advisory skill anyone can run, plus enforcement
only Modula wires underneath — a model can be argued out of a guideline; it cannot be argued out
of an engine hook.

This skill therefore ships `hooks.yaml` (a Modula engine extension, like `gates.yaml`) declaring
**what** is enforced at **which lifecycle event**; the harness adapter maps each to the native
mechanism where one exists (a Claude hook) and to runner-level interception where it does not.

## What belongs here vs in a gate

Only **binary, mechanical** rules — decidable without judgment — belong in a hook: does this file
contain a secret, does this commit message match the format, is this filename a variant marker.
Anything needing judgment stays a doctrine gate (`security-per-pr`, `machine-lint-pack`, …). A
hook that needs an exception is a signal the rule was miscategorized — fix the category, do not
weaken the hook.

## The four layers

### 1. Doctrine re-injection — event: session-start, post-compaction
Re-inject a condensed summary of the project's active doctrine (the enabled skills' load-bearing
rules) so it survives context compaction and long sessions. Action: **inject**. This is what keeps
the other skills honest past hour three.

### 2. Deterministic validators — event: pre-write, pre-commit, pre-tool
Binary guards that **block** the action outright:

- **Secret-write guard** — block writing a file that contains a credential. The write-time twin of
  `security-per-pr`'s secrets gate: the gate catches it in review, this stops it entering at all.
- **Commit-format guard** — block a commit message that is not conventional-commits form, and
  block any tool/author attribution the house rules forbid.
- **File-size guard** — flag a file past the size default; block or warn per the KISS escape hatch
  (a cohesive unit may exceed it with a stated reason).
- **Variant-file guard** — block creating `*_v2`/`*_old`/`*_backup`-style residue. The write-time
  twin of `machine-lint-pack`'s variant-files gate.

### 3. Periodic nudges — event: stop (every Nth)
Non-blocking reminders — update the memory layer, re-check the plan, note a decision. Action:
**warn**. Nudges, not gates.

### 4. Lightweight-model judgment — optional
Route a narrow, high-frequency check through a cheap model where a pure regex is too blunt (e.g.
"is this commit actually conventional, or just prefixed"). Kept optional and clearly bounded; it
is the one hook that is not purely deterministic, so it advises rather than blocks.

## As the operator / project owner

Enable the layers a project needs; each is default-considered but individually toggleable. Binary
rules go here so they survive compaction; judgment rules stay in the doctrine skills. Do not patch
a hook with per-case exceptions — amend the rule's category instead.

## As the engine (enforcement)

Apply `hooks.yaml` at each lifecycle event, harness-agnostic, via the runner. A **block** action
refuses the operation and returns the reason; an **inject** action prepends the condensed doctrine;
a **warn** action surfaces a non-blocking note. Every block writes a receipt. Where the active
harness exposes a native hook, the adapter may delegate to it, but correctness never depends on
the harness providing one.

## Notes

- This is the enforcement floor beneath every other skill; it does not restate their doctrine, it
  makes the mechanical slice of it non-negotiable.
- Secret-write and variant-file guards intentionally pair with the review-time gates in
  `security-per-pr` and `machine-lint-pack` — prevention at write time, detection at review time.
