# PRD #24 UX / Launch / Peer Contract Checkpoint

## Human clarification

The four configured implementation agents are a bidirectional peer mesh: coder, verifier, researcher, and steward can each communicate directly with any other role when needed. PRD authoring uses a default three-role peer mesh: prd-author, researcher, and codebase-expert. Coder/verifier review traffic remains mandatory, but it is not a hierarchy and it must not block direct bounded peer consults between any other two roles.

## Implementation launch contract

- Default implementation workspace roles: verifier, coder, researcher, steward.
- Default desktop/tablet visible pair: verifier + coder.
- Alternate desktop/tablet visible pair: researcher + steward.
- Phone visible mode: one active role terminal at a time, with role buttons for all launched agents.
- Hidden roles remain live and reattachable; switching visibility must not kill PTYs or erase attach tokens.
- Status states for every role: idle, starting, working, waiting, blocked, error, exited, done. Status badges remain visible for hidden roles in the pair switcher, phone role buttons, menu, or compact rail.
- Pinning the active pair or active phone role prevents any automatic working-agent surfacing from stealing focus until the operator unpins it.
- Mandatory linked implementation pair: verifier + coder for checkpoints and final bug-check.
- Researcher and steward are always launched; usage is trigger-based and broad, not emergency-only.
- Coder priming must warn that steward will review structure/hygiene before PR readiness.
- Required final workflow order when structure, docs, generated output, run artifacts, launch scripts, or workflow documentation changed: implementation checkpoint review, bounded steward hygiene pass, coder cleanup if needed, verifier recheck of cleanup, then final verifier bug-check.
- If steward is unavailable when the hygiene gate is required, the flow stops for human escalation instead of silently skipping the gate.
- Known steward cleanup must finish before final bug-check to avoid unnecessary duplicate bug-check cycles.

## PRD authoring launch contract

- Default non-trivial authoring workspace roles: prd-author, researcher, codebase-expert.
- Desktop/tablet default authoring view: three visible panes for PRD Author, Researcher, and Codebase Expert.
- Phone authoring mode: one active authoring role terminal with buttons for every launched role.
- Researcher and codebase-expert receive bounded context requests unless compact small-fix mode is explicitly selected and recorded.
- Steward is not a default visible PRD authoring pane; every full PRD should include concise implementation hygiene / Steward readiness instructions.
- Large or cross-cutting drafts may request an optional Steward hygiene review before the PRD is finalized.
- PRD authoring never approves PRDs or mutates GitHub without the existing explicit human-confirmation flow.

## Bidirectional peer coms contract

- Any role may send a bounded request to any other role in the same worktree/coms pool.
- Every request must include sender, target, worktree/cwd, purpose, expected response shape, and stop condition.
- Worktree isolation, one-in-flight peer request per agent, no-loop response discipline, and no cross-worktree fallback remain mandatory.
- Role norms remain scoped: coder edits, verifier reviews, researcher answers sourced questions, steward audits structure/hygiene, prd-author drafts, codebase-expert gives read-only repo context.
- Direct peer communication does not bypass human approval, verifier bug-check, PR creation, merge, deploy, or production-readiness gates.

## Responsive/mobile guidance from researcher freshness consult

- Use feature/responsive detection rather than iPad user-agent assumptions.
- Account for iOS visual viewport and on-screen keyboard behavior; avoid `100vh`-only layouts.
- Do not rely on hover-only controls; use touch-friendly buttons.
- xterm.js mobile/touch support remains fragile; provide role switchers outside the terminal input area and refit terminals when panes become visible.
- Hidden panes must either stay mounted or retain PTY/session state outside mounted UI and reattach cleanly.

## Checkpoint stop condition

Verifier approval of this contract authorizes implementation of launch/profile, layout, peer-coms documentation, and skill/workflow changes within PRD #24 scope. Any disagreement on the bidirectional peer mesh, hidden-session liveness, command-launch allowlist, or approval gates should be raised before broad implementation.
