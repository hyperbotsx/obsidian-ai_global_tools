# AI Maestro coordination boundary

- Mode: `read_only`
- PRD: `934`

## Display-only session names
- `evonome/admin/prd-934-coder` — coder; display_only
- `evonome/admin/prd-934-verifier` — verifier; display_only
- `evonome/admin/orchestrator` — orchestrator; display_only

## Message and memory policy
- Messages: `reminder_only_not_approval_or_evidence`
- Memory: `cache_only_with_canonical_links_no_secrets`
- CORS boundary: `localhost_only_required_because_ai_maestro_api_allows_wildcard_origin`

## Forbidden uses
- approval decisions
- verifier evidence
- checkpoint status changes
- GitHub or Project 2 mutation
- real-session create/delete/rename/injection
- secret, token, provider config, or raw transcript storage
