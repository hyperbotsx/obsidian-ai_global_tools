# Verifier Request

```json
{
  "type": "review_request",
  "checkpoint": "8 - Coder/verifier launch profiles",
  "revision": 14,
  "requested_action": "initial_review",
  "prd": "https://github.com/hyperbotsx/agentops-harness/issues/21",
  "issue": "https://github.com/hyperbotsx/agentops-harness/issues/21",
  "handoff_path": "dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/coder-handoff.md",
  "changed_files": [
    "term-control-center/server/index.ts",
    "term-control-center/shared/protocol.ts",
    "term-control-center/src/App.tsx",
    "term-control-center/src/TerminalPane.tsx",
    "term-control-center/tests/protocol.test.ts",
    "term-control-center/tests/server.test.ts",
    "dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/coder-handoff.md",
    "dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/decision-log.md",
    "dev-plans/agentops/coder-verifier-workflow/runs/term-control-center-21-phase1/coder-ready.md"
  ],
  "validation_results": [
    { "command": "npm --prefix term-control-center run build", "result": "pass" },
    { "command": "npm --prefix term-control-center run test", "result": "pass" },
    { "command": "npm --prefix term-control-center audit --audit-level=moderate", "result": "pass" },
    { "command": "git diff --check", "result": "pass" },
    { "command": "tokenized node build/server/index.js health smoke", "result": "pass" }
  ],
  "finding_ids_addressed": []
}
```
