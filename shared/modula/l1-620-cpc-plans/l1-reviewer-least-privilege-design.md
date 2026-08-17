# Design note — least-privilege built-in reviewer: the autonomy foundation

**FRD:** #620 L1 (built-in reviewer) · **Slice:** CP-C live-reviewer, security foundation · **Author:** Lead · 2026-08-17
**Status:** decision recorded (operator: build the foundation now, Lead-built; Lead decides the write mechanism).

## 1. Problem
The built-in reviewer reads **untrusted contributor diff** on the user's own model, so its agent pane must launch
**least-privilege: read + write ONLY its findings artifact; deny source edit / exec / git-mutate / network**
(FRD F5; Kody #3456 critical). A code read (verified against `eb00e1a`) shows this is **not achievable with
existing autonomy infra** — three load-bearing blockers:

- **A — settings policy is frozen.** `scripts/agentops/claude-native.sh:108-125` hard-rejects (exit 5) any
  `settings.json` whose `permissions` block is not *exactly* `{allow:[], deny:[], defaultMode:'default'}`. A
  custom allow/deny policy is impossible; all enforcement is the compiled PreToolUse hook + the autonomy classes.
- **B — no path-scoped write class.** `autonomyGates.ts:1` allows `local_read | workspace_edit |
  verification_command | peer_coms`. Any `Edit`/`Write` classifies as `workspace_edit`
  (`editCandidate`, `:69`), and `autonomyPaths.ts:62` `withinRoots` allows writes to the **whole worktree OR
  artifactRoot**. So a reviewer granted `workspace_edit` can rewrite arbitrary source under review; granting only
  `local_read` leaves it unable to emit findings. There is **no "read + write only this one file" grant**.
- **C — the reviewer runs ungated today.** The autonomy gate env is applied **only to native-claude** panes
  (`launchPlan.ts` `paneEnv`: `if (!nativeClaude(profile) ...) return base`). The reviewer's default profile
  `pi-claude-opus` is **`claude-agent`** (`launchProfiles.ts:79`), and no native-claude profile ships in the
  default set — so a `code-reviewer` pane launches at **full trust, ungated**.

Already-safe on native-claude (bounds the scope): `classifyBash` denies all shell/git-mutate unconditionally
(`autonomyGates.ts:108-116`), `WebFetch`/`WebSearch` deny (`:53`), secrets/`.git`/protected paths deny
(`autonomyPaths.ts:17-19`). The **only** missing capability is the scoped artifact write.

## 2. Options for the write mechanism
**A) Coms-emission** — reviewer emits findings over coms (`peer_coms`, an existing class); grant `[local_read,
peer_coms]`; `readRun` collects from coms instead of a file.
- + no new autonomy class.
- − puts the **flaky coms path in the review loop** (auto-wake broken #665; coms transport stall history);
  − `peer_coms` is a **broad** capability — a prompt-injected reviewer could message the coder / git-manager with
  attacker-chosen instructions; − changes CP-B's file-handoff design + adds server-side coms collection plumbing.

**B) Path-scoped `artifact_write` class** — new autonomy class allowing a write **only** to the run's findings
artifact; grant `[local_read, artifact_write]`; keep CP-B's file handoff (`collectFindings`/`readRun` read
`contextRuntimeDirectory(groupId)/review-findings.json`).
- + **tighter least-privilege** than coms (a single validated file < "talk to any peer"); + no coms dependency
  in the review path; + keeps the clean D-1 file handoff (`readRun` ≈ `readContextBriefState`); + a reusable
  platform primitive (any artifact-producing agent can use it); + output is re-validated outside the model by
  `normalizeFinding` + `sanitizeFinding`.
- − adds a security-critical class to the gate engine (must be scoped carefully).

## 3. Decision — **B, the `artifact_write` class**
It is the *narrower* capability for an agent on untrusted input (the decisive factor), it keeps coms out of the
review loop, and it preserves the file-handoff the feasibility pass validated as the simplest path. The cost — one
new, carefully-scoped autonomy class — is exactly the primitive the platform is missing.

### `artifact_write` scoping (the security-critical detail)
- Add `artifact_write` to `ALLOWED_ACTION_CLASSES` + `ALLOW_REASON`/`REASON_CODES` (`allow_artifact_write`).
- Classification (`classifyTool`): a `Write`/`Edit`/`MultiEdit`/`NotebookEdit` whose target path **equals the
  granted artifact path** → `artifact_write`; any other write → stays `workspace_edit` (so it is denied unless
  `workspace_edit` is also granted — which the reviewer will NOT be). Do **not** widen `withinRoots`.
- Path validation must be **stricter than `withinRoots`**: exact-match (after realpath/symlink + `.git` + secret
  + protected checks reuse) to the single allowed artifact path, which is passed in via `autonomyPaneEnv`
  (the run derives it from `contextRuntimeDirectory(groupId)`). NOT artifactRoot-wide.
- The reviewer's grant is exactly `[local_read, artifact_write]` — no `workspace_edit`, so source edits are denied.

## 4. native-claude provisioning (Blocker C)
The reviewer must run on **native-claude** for the gate to apply at all. Provision a native-claude reviewer
profile (or force the review-only launch shape onto native-claude) so `paneEnv` attaches the autonomy env with
the `[local_read, artifact_write]` grant. This is required for ANY least-privilege option (A or B).

## 5. Slicing (each its own small PR; Lead-built; reviewed before merge given security weight)
1. **Foundation PR — `artifact_write` autonomy class.** `autonomyGates.ts` + `autonomyPaths.ts` (+ the exact-path
   validation) + `autonomyPaneEnv` plumbing for the granted artifact path + unit tests (grants read+scoped-write,
   denies source edit, denies non-artifact writes, denies traversal/symlink/secret). Pure security primitive, no
   reviewer yet. **This design note ships with it** (security-posture doc travels with the change).
2. **Reviewer slice.** native-claude reviewer provisioning + the standalone review-only launch shape (mirror the
   context-brief mode) granting `[local_read, artifact_write]` + `requestRun`/`readRun`/fail-closed
   `requestReview` + reserve-guarded per-round retrigger with PR/head validation.
3. **Config default flip** (kodus→builtin) — separate, gated/revertable via `TERM_CONTROL_REVIEW_PROVIDER`.

Bounded-cap / dismiss-restore / admin-toggle (the FRD's AC-C1/C2/C3 governance work) are independent of this and
can proceed in parallel or after. **D-8 linear-only** confirmed — no E7 logic anywhere.
