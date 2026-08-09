# FRD #391 — delta notes, 2026-08-08

**Written by:** the Opus 5 Lead of the FRD #363 trio run, at the operator's request, as mandatory
grounding for the #391 fast-lane pilot.

**What this is:** two things only I currently have — (1) what three commits landed in #391's territory
*after* the FRD was written, and (2) fresh dogfood evidence from a multi-day Lead-as-hub run. Read this
before the reconciliation note; it is input to that note, not a substitute for it.

**What this is not:** a re-statement of the FRD or of `frd-391-standing-peer-handoff-from-355.md`. Those
remain the brief. Where this contradicts them, this is newer — but verify against code before trusting
either.

---

## Part 1 — the three commits, and what they change for #391

All three are on `main` and all three touch files #391 owns. I read the diffs rather than the titles.

### `7ece01f` — coms socket paths bounded (ENAMETOOLONG)

**What it fixed:** generated implementation pool names produced endpoints of **142–146 bytes**, past the
**108-byte** unix socket path limit, so the coms child **died with `ENAMETOOLONG` on every launch from a
job worktree**. Short paths are kept as-is; longer ones are derived under a fixed short directory.

Files: `comsAdapter.ts`, `comsMcp.ts`, `shared/comsEndpoint.ts`, tests.

**Why #391 must care:** the standing Lead is **per-job**, and job pool names are exactly the long ones
that broke. This bug sat directly on #391's path. It is fixed — but the fix introduces
`comsSocketDirectory(comsDir, sessionId, platform)` as the way to derive the directory. **#391 must call
it, never construct socket paths itself.** Hand-rolling a path is how the 108-byte limit comes back for
the standing peer specifically.

### `0a988c3` — per-user socket isolation + session-id validation

**What it fixed:** the shared socket directory was **world-predictable**, so another local user could
pre-create or symlink it and take over hashed sockets. Now: a per-user runtime directory verified for
ownership, mode and symlinks. Separately, session ids are validated as single path segments before any
failure-record filename is built, so a traversal value cannot escape.

New surface in `shared/comsEndpoint.ts`:

```
comsRuntimeDirectory(uid)        ensureComsRuntimeDirectory()
ensureComsSocketDirectory(path)  isSafePathSegment(value)
```

`comsAdapter.ts` now calls `ensureComsSocketDirectory(this.endpoint)` after creating the directory, and
`sameComsEndpoint` validates against `comsSocketDirectory(...)` rather than a hardcoded `sockets` join.

**Why #391 must care — this is the sharpest one.** #391 adds a *new* registration path: a standing peer
that registers and re-registers across renewals and crashes (CP-1, CP-5). **Every one of those paths must
go through `ensureComsSocketDirectory` and `isSafePathSegment`.** A standing peer that sets up its own
socket reintroduces a local-privilege hole that was closed nine days ago, and it will not fail visibly —
it will just be insecure. Treat this as a hard constraint, not a style preference.

### `cce7c7a` — serialized registry writes + legacy project alias

Large change to `adminProjects.ts` (+156), and **it changed `leadRuntime.ts` — the file #391 single-owns**:

```diff
-storeFor: (projectId: string) => PageBotModelSettingsStore
+storeFor: (projectId: string) => PageBotModelSettingsStore | Promise<PageBotModelSettingsStore>

-entry.runtime ??= createLeadRuntime(target, { ..., store: dependencies.storeFor(target.projectId), ... })
+if (!entry.runtime) {
+  const store = await dependencies.storeFor(target.projectId)
+  entry.runtime = createLeadRuntime(target, { ..., store, ... })
+}
```

**Why #391 must care:** `startRuntime` — the exact function residency work extends — is now
async-aware, and `createLeadRuntimes`' dependency shape changed. **FR-29 specifies exposing
`leads.refresh` on `createLeadRuntimes` at `leadRuntime.ts:117`; that line number is stale** and the
surrounding code no longer looks as the FRD describes. Re-derive the seam from current code.

### Summary for the reconciliation note

| FRD assumption | Status |
|---|---|
| Socket paths safe for job-pool names | **Was broken, now fixed** — use `comsSocketDirectory` |
| Socket dir setup is the adapter's business | **Changed** — must use `ensureComsSocketDirectory` |
| Session ids are free-form | **Changed** — must pass `isSafePathSegment` |
| `createLeadRuntimes` deps are sync | **Changed** — `storeFor` may return a promise |
| `leadRuntime.ts:117` locates `leads.refresh` | **Stale line reference** |

None of this invalidates #391's design. The per-job runtime it builds on still exists and still holds one
entry per `jobId`. What changed is the *plumbing underneath*, in ways that are easy to miss and expensive
to get wrong.

---

## Part 2 — dogfood evidence from 2026-08-06 → 08

Posted in full to issue #391; condensed here with the parts that bear on specific checkpoints.

### A reply carrying the whole task still schedules nothing (CP-4)

I answered a coder's ping via `coms_respond` with the **complete** assignment — authority path, defect,
forbidden shortcut, scope, required protection. It consumed the message (20k tokens, 5% context) and
**went idle**. The worktree never changed branch. Only an out-of-band `agentops-steer` produced a turn.

The requirement is sharper than "a queued message is not a work-turn": **delivering content and
scheduling a turn are two different operations**, and today only the out-of-band path performs the
second.

### Three indistinguishable idle states (CP-1, CP-4)

In one session I hit all three:

1. Agent consumed a task and went idle
2. Agent **said** "I'll wait on the coms inbox" and then ended its turn without ever calling `coms_await`
3. Agent had a **composed but unsent turn** sitting in its input box

State 3 is the one to design against. From outside — process alive, present in `coms_list`, pane
rendering, non-zero CPU — **it is indistinguishable from an agent that is thinking**. A wake that assumes
the peer is sitting in `coms_await` covers none of these three. It must be able to drive a pane that is
at a prompt, mid-compose, or holding unsent text.

### The steer path has no integrity guarantee (CP-4)

A steer payload composed as a double-quoted shell string had its backticks **evaluated by bash**; a word
was silently stripped and `agentops-steer` reported success. The agent received a holed instruction with
no way to detect it. Separately, a long payload pasted into a Claude pane was collapsed to
*"paste again to expand"* and never submitted.

A first-class wake must carry a **structured payload** — or a pointer to a durable artifact — not an
interpolated command line, and delivery should be verifiable by the sender.

### `relay_cancel` exists and was undiscoverable (CP-3) — correcting an earlier read

I hit `coms: outbound request already in flight` and routed around it with `agentops-steer` for an entire
run. **My first conclusion, that the send slot is global, was wrong** — `comsAdapter.ts:103` blocks per
**recipient**, so **R5's "done: per-recipient + cancel" in the handoff doc is accurate and should not be
reopened.**

The real gap is discoverability: `relay_cancel` is the one verb with **no `coms_` alias**, so the Lead
that needed it never found it. `autonomyGates.ts:31` already carries a comment saying exactly this. Fix
is an alias, or naming the remedy in the error text — the error is the one moment the stuck caller is
guaranteed to be reading.

### Registry slots leak across relaunches (CP-5)

This Lead is registered as **`lead3`**; two dead predecessors from earlier relaunches are still in the
pool registry. Anything addressed to `lead` reaches a dead slot. **Teardown must reclaim the canonical
name, not increment past it** — a pool where the Lead's name drifts is one where peers cannot reliably
address it.

### The wake path and the roster speak different namespaces (CP-3 + CP-4)

Observed live while writing this note, 15:40. `coms_list` returns peers by **name**:

```json
{"name":"coder","session_id":"01KZGAE28XK6B9G3HT45W6WQCS","alive":true}
```

`relay_dispatch`/`coms_send` address by that **name**. But the out-of-band wake does not:

```
$ agentops-steer coder '<task>'
agentops-steer: no socket for session 'coder' under /tmp/agentops/coms/*/sockets/

$ agentops-steer 01KZGAE28XK6B9G3HT45W6WQCS '<task>'
steered 01KZGAE28XK6B9G3HT45W6WQCS.sock (msg 4d30c9f5)
```

**The identifier you use to *talk* to a peer is not the identifier you use to *wake* it.** The roster
never shows a socket, the socket filenames are opaque ULIDs/hashes, and the one identifier a Lead
naturally holds — the name — is the one the wake path rejects. For #391 this is direct: a standing peer
that dispatches by name (CP-3) and wakes by id (CP-4) has to carry a private name→session_id mapping and
keep it correct across peer renewals, or **CP-4 silently cannot reach the peers CP-3 can.** Whatever wake
verb #391 exposes should accept the same namespace as dispatch.

Note the error message shape, again: it names the failed lookup but not the remedy. Same class as the
`relay_cancel` gap above — and the same cheap fix (accept both, or say which one it wants).

### Residency is runtime-asymmetric (CP-1)

pi panes auto-bind and begin polling on launch. The Claude verifier **registered in the pool but would
not await** until a human pasted a standby instruction into its pane. "Registered" and "listening" are
separate properties and **only the first is visible in the roster.** CP-1 should state which runtimes its
residency guarantee covers.

---

## Part 2b — what FRD #363 CP-7 will need from these same files (read before refactoring)

**Not a request to build it.** CP-7 is a separate, later piece of work. This section exists so the #391
lane does not unknowingly make it harder — and because CP-7's own line anchors are already stale.

CP-7 (FR-29) requires four edits, and **all four are in #391-owned files**:

| CP-7 needs | FRD says | Actually at (2026-08-08) |
|---|---|---|
| Stop hardcoding `context_used_pct` on the pong | `comsAdapter.ts:208` | **`comsAdapter.ts:254`** |
| Stop hardcoding it on the registry entry | `comsAdapter.ts:255` | **`comsAdapter.ts:304`** |
| (unnamed by the FRD, but required) | — | **`comsAdapter.ts:366`** — `publicEntry` forces `context_used_pct: null` |
| `leads.refresh` exposed on `createLeadRuntimes` | `leadRuntime.ts:117` | **`leadRuntime.ts:161`** |

Two things follow.

**The roster lies in two different ways.** The wire protocol reports a hardcoded `0` (`:254`, `:304`)
and `publicEntry` overwrites it with `null` (`:366`) — I confirmed the `null` in a live `coms_list` today.
So context usage is fabricated at the source *and* discarded at the boundary. Anything #391 builds that
reasons about peer context state (renewal pressure, when to hand off) is reading a constant. If the lane
touches `publicEntry` or the registry shape, **leaving a real value plumbable is nearly free now and
expensive later.**

**`refresh` already exists per-runtime** (`leadRuntime.ts:68`, `:147`) with the exact
`'compaction' | 'renewal'` signature CP-7 wants. What is missing is exposure on the **registry**
(`createLeadRuntimes`, `:161`). #391 CP-5 (lifecycle) is in that function anyway. Not asking the lane to
wire it — only: **if you restructure `createLeadRuntimes`' return, keep a place for a registry-level
refresh to hang.**

**Boundary consequence the operator should see:** under the agreement as written, CP-7's FR-29 is not
merely *sequenced* behind #391 — it is **blocked**, because the rule is "stop and escalate rather than
edit" and FR-29 cannot be built anywhere else. That needs an explicit decision (carve-out, absorb into
the lane, or sequence-and-rebase) before CP-7 starts. Flagged to Erik 2026-08-08.

---

## Part 3 — two things worth knowing that are not requirements

**The trio caught three bad instructions from me** over this run — a `git fetch origin main:main` into a
checked-out branch, a branch deletion blocked by an occupying worktree, and a checkout of a branch living
in its own worktree. Each time an agent stopped and reported the contradiction instead of executing it.
Relevant to CP-4: **an agent that is auto-nudged past its own guard rails loses the property that made
this work.** Whatever re-drive gets built should not be able to push an agent through a refusal.

**Concurrent worktree use voids test results** (issue #442). Running the gate in a worktree another
process is mutating produces failures that do not reproduce in a clean checkout — verified with three
invocations: clean merge-base and clean branch head gave byte-identical failure sets, the shared worktree
gave a different set including a phantom branch-only failure. **The fast-lane's own fresh worktree
sidesteps this**, but if the acceptance receipt runs a live multi-agent session, keep the gate off any
worktree those agents are writing to.

---

## Pointers

- Issue #391 + my full dogfood comment (2026-08-08)
- `shared/modula/frd-391-standing-peer-handoff-from-355.md` — the brief; I appended a summary of Part 2 to it
- `shared/modula/term-1-run-harvest.md` — H-2, H-4, H-39, H-47, H-48 (coms/wake/hub), H-59, H-60, H-61 (added this run)
- Issue #442 — gate results void in a concurrently-mutated worktree
