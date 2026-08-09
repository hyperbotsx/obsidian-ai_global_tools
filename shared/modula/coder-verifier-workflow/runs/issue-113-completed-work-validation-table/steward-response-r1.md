Decision: cleanup_recommended

Summary: file placement appropriate; run artifacts should stay; public symlinks match static asset pattern. Recommended cleanup was limited to Python cache dirs:
- `pipeline-diagram/__pycache__/`
- `pipeline-diagram/deploy/__pycache__/`

Coder applied that cleanup. Steward noted `node_modules` may remain for verifier reruns; ignored build outputs are optional to remove before PR/commit, not required for final bug-check. Branch behind origin/main by 2 should be considered by final verifier/human workflow.
