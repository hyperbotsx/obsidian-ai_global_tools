# FRD Term-3 — Narrated workspace: structured transcript rendering

Status: **CEO-APPROVED 2026-08-05** (smart review, comment 12192 on #405) · draft v1 · 2026-08-05 · owner: Erik + Lead · priority: completes the operator's 100%-match order for the terminal view — Term-2 (#364) is the frame, this is what plays inside it.
Canonical FRD source: **forge issue #405** (ModulaStack/modulastack). Vault working draft: this file.
Companions: FRD Term-1 — #363 (backend/wiring; FR-29 context feed shares the runtime-telemetry pattern) · FRD Term-2 — #364 (visual parity; its §4 names this FRD as owner of the narrated-terminal exclusion).
Design sources of truth: `dev-plans/drafts/modula-stack-design-prototype.html` (published at proto.modulastack.com) · `dev-plans/drafts/page-briefs/01-workspace.md` · prototype-reference gate (`prototype-reference-gate-workflow.md`).

## 1. Problem

The operator's order (2026-07-29) is a 100% match of the terminal view to the prototype. Term-2 closes that for everything around the scrollback — envelope, topbar, sidebar, modebar, pane heads, composer, diff, FRD tab. But the scrollback interior itself cannot be closed by styling, because the two sides are different kinds of things. The prototype's scrollback is a **narrated activity log**: proportional-font italic entry labels over mono payload lines, semantic colour spans, 24px block rhythm, an 880px measure, dim/standby entry states (prototype 465–482, 2459–2482). The app's scrollback is a **character grid**: xterm.js attached over WebSocket to a tmux pane where the agent's TUI redraws itself (`src/TerminalPane.tsx`, `server/tmuxSupervisor.ts`). A terminal emulator cannot express per-block layout, proportional labels, or entry-level states — which is why #364 §4 excluded the "narrated-terminal look" as "a large functional build, not styling."

This FRD is that build. The gap is not a parsing problem: the agents' own runtime already records a typed, structured transcript of everything the prototype narrates — we render terminal pixels while sitting on the exact data the design asks for. The industry pattern is settled: every polished agent surface (opencode's session-ui, Sculptor, Conduit, assistant-ui) renders a typed event timeline and keeps a raw terminal as an escape hatch, not as the primary surface. Conduit states the ruling verbatim: *"Is this a terminal wrapper? No. It doesn't scrape or parse terminal output."*

## 2. Grounded facts (verified 2026-08-05)

| # | Fact | Evidence |
|---|---|---|
| N-1 | The prototype scrollback spec is a block log, not a grid: `.log` (max-width 880px), `.entry` (24px margin), `.entry-label` (UI font, italic, 13px), `.line` (pre-wrap mono), span classes `prompt/key/string/path/mutedtext/ok/warn`, states `.entry.dim` and `.entry.standby`, blinking `.caret`, 210px bottom fade | prototype 451–506 (CSS), 2459–2482 (coder entries), 2546–2549 (standby entry) |
| N-2 | The app renders raw PTY: xterm.js over the pane WebSocket to tmux; the scrollback is the agent TUI's own full-screen redraw — there is no linear stdout to parse | `src/TerminalPane.tsx` (Terminal + FitAddon + WS), `server/tmuxSupervisor.ts:138,151` (attach/capture-pane) |
| N-3 | Every trio agent already writes a typed session transcript to disk: pi session JSONL v3 at `~/.pi/agent/sessions/<cwd-slug>/<ts>_<uuid>.jsonl` with entries `session` (version 3, cwd), `session_info` (name = role, e.g. "verifier"), `model_change`, `thinking_level_change`, `compaction`, and `message` whose content blocks are `thinking` / `toolCall` / `toolResult` / text | inspected live verifier session from this worktree (697 message entries: 421 toolResult, assistant messages carrying thinking+toolCall blocks) |
| N-4 | Pi persists **each entry synchronously as it happens** (`appendFileSync` per entry once the first assistant message has flushed the file) — a tail-follower gets block-granularity live updates mid-turn, including tool results as they complete | `@earendil-works/pi-coding-agent/dist/core/session-manager.js` `_persist`/`_appendEntry` (lines ~663–697) |
| N-5 | Pi supports `--mode json` and `--mode rpc`, plus `--session-id <id>` to pin session identity at launch — deterministic pane→file mapping needs no newest-file guessing | `pi --help` |
| N-6 | Codex CLI 0.146.0 is installed; `codex exec --json` emits typed JSONL thread events (`thread.started`, `turn.*`, `item.*` with `agent_message`, `reasoning`, `command_execution`, `file_change`, `mcp_tool_call`, `todo_list`); the server already shells `codex exec` today | `codex --version`; openai/codex `exec_events.rs`; `server/explainProvider.ts:28` |
| N-7 | Claude Code emits the same shape via `--output-format stream-json` (NDJSON events incl. tool calls/results, permission requests) with a documented bidirectional stdin protocol | code.claude.com/docs/en/headless; community typed parser (claude-code-parser) |
| N-8 | Industry pattern: opencode renders sessions as Message/Part/ToolPart timelines (virtualized, tool-specific renderers); Sculptor renders Claude Code stream events as pills/popovers; Conduit connects to the agent server's event API — "doesn't scrape or parse terminal output" — and still keeps xterm.js tabs as the escape hatch | deepwiki opencode session-ui; imbue-ai/sculptor PR #265; dibstern/conduit README |
| N-9 | Trio launchers name each pi session by role (`session_info.name` = coder/verifier/…) and the session dir derives from the pane cwd — a workable fallback mapping exists even without `--session-id` | `~/.local/bin/agentops-trio-verifier` → `scripts/agentops/pi-agent.sh <role>`; N-3 session_info |
| N-10 | Term-1 FR-29 (context-percent feed) is the same runtime→server telemetry pattern; `context_used_pct` is hardcoded 0 in the registry today — the narrated feed must not bind to registry percent either | #363 FR-29; `server/comsAdapter.ts:208,255` |

## 3. Goals

1. **The default pane view is the narrated transcript** — live, rendered per the prototype scrollback spec, for every workspace agent pane.
2. **The raw terminal stays one action away on every pane, always working** — for interactive TUI moments, debugging, and any feed fault.
3. **v1 requires zero agent-runtime changes** — the feed is a read-only tail of the session log pi already writes (N-3/N-4).
4. **The renderer is runtime-agnostic** behind one small event vocabulary, so codex `--json` or claude `stream-json` panes can join later without a rewrite.

## 4. Non-goals

- Replacing or bypassing the PTY/tmux plane. Recovery, steer, resize, and **all input paths stay PTY** — the composer keeps sending keys exactly as today.
- Token-level streaming inside a block. v1 streams at entry granularity (N-4); pi `--mode rpc` is the named upgrade path, not this FRD.
- Lead dock / lead runtime surfaces — #391 single-owner (`leadRuntime.ts`, `comsAdapter.ts` untouched).
- Narrating sessions that predate the feed; backfill covers the current session file only.
- Parsing PTY bytes or ANSI for meaning. The feed reads the runtime's own log, never scrapes the screen.
- Term-2 chrome (pane head anatomy, composer styling, gauges) — #364 owns those regions; this FRD only adds the view toggle to the pane-head actions Term-2 ships.

## 5. Design rulings

### 5R.1 — Sidecar projection; fail closed to Raw.
The narrated view is a read-only projection of the runtime's session log, relayed by the server beside the PTY stream on the existing pane WebSocket. It never becomes a second source of truth and never gates any action. Any feed fault — file missing, unknown session version, parse error, tail stall — drops that pane to the Raw view with a visible one-line banner. Never a blank pane, never best-effort parsing of an unknown format: the parser is pinned to session version 3 and refuses others explicitly.

### 5R.2 — One small closed event vocabulary; unknown entries render, never vanish.
Pi entries map to the block set in §6. An unknown or future entry type renders as a dim generic entry carrying its raw type name — a runtime upgrade degrades visibly and gracefully, not silently.

### 5R.3 — Prototype-verbatim blocks.
Each CP brief embeds the governing prototype markup/CSS (prototype gate, #364 5R.1 applies here unchanged): entry label + payload lines + span classes + dim/standby states, 24px rhythm, 880px measure, bottom fade, caret. Long tool results truncate to the prototype's own idiom (a `mutedtext` summary line, expandable), and nothing is invented that the prototype does not draw.

### 5R.4 — Deterministic session identity.
The launcher passes an explicit `--session-id` per pane, recorded in the pane registry; the tailer resolves pane→file from that id (N-5). Panes launched outside the app fall back to cwd-slug + role-name + newest-file matching (N-9), and the feed marks itself `degraded` so the UI can say so.

## 6. Event mapping (pi session v3 → prototype blocks)

| pi entry | Narrated block | Prototype anchor |
|---|---|---|
| `message` role=user | Prompt entry — label + `.prompt` line | `.entry-label` + `.line .prompt` (470) |
| assistant `thinking` blocks | Dim reasoning entry | `.entry.dim` (467) |
| assistant `toolCall` blocks | Tool entry per call — label from the call, `$` line for shell | coder entries 2463–2481 |
| `message` role=toolResult | Result lines appended to the owning tool entry, truncated + expandable | `mutedtext` summary idiom (2387) |
| assistant text | Narration entry — plain `.line`s | 465 |
| `compaction` | Boundary marker — dim rule entry ("context compacted · renewed") | dim entry idiom; pairs with Term-1 renewal |
| `model_change` / `thinking_level_change` | Dim meta line | `.entry.dim` |
| `session_info` | Pane binding (role name) — not rendered | — |
| No entries + quiet heartbeat | Standby entry ("Standing by — last active Nm ago") | `.entry.standby` (2546, 552) |

## 7. Functional requirements & checkpoints

**CP-1 — Session feed.** FR-1 server-side session tailer: resolve pane→session file via the `--session-id` recorded at launch **in the server's session store (group/pane record — never the coms registry, which is #391's)** (small launcher change) with the N-9 fallback; tail-follow the JSONL live via polled byte-offset reads (`fs.watch` is best-effort across platforms — poll and read only new bytes), parse v3 fail-closed (5R.1), backfill the current session on connect. Context renewal or fork starts a **new** session file: the tailer re-resolves the pane's current session id from the registry and follows the new file — a stale tail on a dead session is a feed fault (5R.1). FR-2 relay typed block events beside the PTY channel on the existing pane WebSocket, with a feed status of `live` / `degraded` / `absent`. FR-3 fixture-driven tests: recorded session files — including a mid-line partial write, an unknown entry type, and an unknown session version — drive the parser deterministically.

**CP-2 — Narrated renderer + toggle.** FR-4 `NarratedTranscript` component per the embedded prototype spec, virtualized for long sessions, reusing the existing jump-to-bottom behavior. FR-5 per-pane view toggle **Narrated ⇄ Raw** in the pane-head actions (the home Term-2 CP-3 builds), persisted per pane; feed fault auto-switches to Raw with the banner. FR-6 composer and every input path unchanged (PTY); no narrated-view control writes to the session.

**CP-3 — Block fidelity.** FR-7 tool-entry rendering: command entries with `$` lines and `✓`/`⚠` outcome lines, durations as `mutedtext`; file read/write entries with `.path` spans; coms entries per the prototype idiom (2390–2397). FR-8 result truncation/expansion per 5R.3. FR-9 boundary markers (compaction/renewal) and standby entries for idle panes. Screenshot pairs vs the prototype coder + verifier scrollbacks (dark + light).

**CP-4 — Second runtime + audit.** FR-10 harden the adapter seam: implement one non-pi adapter (Claude Code `stream-json`, N-7) behind the same vocabulary, proving runtime-agnosticism; it binds to a live pane only if a claude-driven workspace pane exists by then, else ships fixture-tested. FR-11 full-sweep audit: a live trio session captured side-by-side against the prototype; closing parity note naming the residual gaps (token-level streaming → pi rpc; TUI-only interactive moments → Raw view) with owners.

## 8. Acceptance criteria

- **AC-1** A live trio session renders as narrated blocks matching the prototype scrollback spec in structure, type, colour, and rhythm (side-by-side capture, dark + light) for every mapped entry type in §6.
- **AC-2** Narrated is the default view; Raw is reachable in one action on every pane and fully functional — input, resize, selection, recovery unchanged.
- **AC-3** Killing the feed mid-session (rotate the file; feed an unknown version) drops the pane to Raw with a visible banner — no blank pane, no crash, no stale-but-live-looking transcript.
- **AC-4** New entries appear in the narrated view within ~1s of the runtime writing them, including mid-turn tool results (N-4).
- **AC-5** A 5,000-entry session scrolls smoothly under virtualization; no horizontal scroll at any prototype breakpoint; both themes pass the contrast gate.
- **AC-6** No PTY regressions: existing terminal tests stay green; steer and recovery flows unaffected.
- **AC-7** An unknown entry type renders as a dim generic entry (fixture-proven), never silently dropped.

## 9. Verification tier

Lead + Coder + Verifier (+ Git Manager). Verifier reviews each CP against the embedded prototype spec and the screenshot pairs; captures use the Term-1 AC-11 headless harness. Sequencing: starts once Term-2 CP-3 lands (the pane head that homes the toggle); runs in parallel with Term-2 CP-4/CP-5 thereafter. Single-owner boundaries: no changes to `leadRuntime.ts` / `comsAdapter.ts` (#391); if Term-1 FR-29's feed lands first, reuse its runtime-telemetry plumbing where it fits.

## Appendix — prototype scrollback spec (embed source for CP briefs)

```css
/* prototype 451–482 (condensed) */
.terminal { min-height: 0; position: relative; overflow: hidden; font-family: var(--mono); font-size: 14px; line-height: 1.7; }
.scrollback { position: absolute; inset: 0; overflow-y: auto; padding: 18px 24px 210px; }
.terminal::after { /* 210px bottom fade to var(--surface) */ }
.log { max-width: 880px; color: var(--fg); }
.entry { margin: 0 0 24px; }
.entry.dim { color: var(--muted-2); }
.entry-label { margin-bottom: 7px; color: var(--muted); font-family: var(--ui); font-size: 13px; font-style: italic; line-height: 1.3; }
.line { white-space: pre-wrap; overflow-wrap: anywhere; }
.prompt { color: var(--accent-warm); } .key { color: var(--syn-key); } .string { color: var(--syn-string); }
.path { color: var(--syn-path); } .mutedtext { color: var(--muted-2); } .ok { color: var(--accent); } .warn { color: var(--warning); }
.entry.standby, .entry.standby .entry-label { color: var(--muted-2); }
```

```html
<!-- prototype 2463–2481 (coder entries, representative) -->
<div class="entry">
  <div class="entry-label">Applying P5 renderer plan</div>
  <div class="line"><span class="warn">…</span> Wrote 73 lines to <span class="path">tests/diffPinExport.test.ts</span></div>
  <div class="line"><span class="ok">✓</span> Focused tests pass · 12/12 · 3.1s</div>
</div>
<div class="entry dim">
  <div class="entry-label">Fixing renderer null-guard finding</div>
  <div class="line"><span class="prompt">$</span> npx vitest run diffPatchView --reporter=dot</div>
  <div class="line"><span class="ok">✓</span> 18 passed · 0 failed · 2.4s</div>
</div>
```
