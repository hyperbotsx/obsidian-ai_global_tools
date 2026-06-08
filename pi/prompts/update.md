---
description: Non-invasive coder/verifier progress update with plain-English and technical summaries
argument-hint: "[artifact-folder|issue]"
---
Use the `update` skill to provide a non-invasive progress update for the active coder-verifier flow.

If arguments are supplied, use them as the run/artifact/issue hint: $ARGUMENTS

Rules:
- Do not edit files.
- Do not send socket messages.
- Do not run deployments, validation suites, bug-checks, or GitHub mutations.
- Prefer local coder/verifier artifacts.
- Include a short human-readable summary first, then technical bullets.
