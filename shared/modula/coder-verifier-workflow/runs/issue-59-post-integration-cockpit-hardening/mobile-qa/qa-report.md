# Issue #59 Mobile/iPad QA Evidence

## Browser smoke matrix

Tooling: Playwright Chromium from `@ogulcancelik/pi-web-browse` dependency. Google Chrome binary crashed in this container, so Playwright Chromium was used as the alternate browser path.

Viewport heights were 900px. Mobile widths used touch/mobile emulation where width < 768.

Covered widths: 320, 375, 390, 430, 520, 768, 1024.

Covered pages with screenshots in `screenshots/` and tabular evidence in `playwright-smoke.tsv`:

- Board: `/pipeline-diagram/board.html`
- Pipeline: `/pipeline-diagram/pipeline.html`
- WIP: `/pipeline-diagram/wip.html`
- Completed validation/completion center surface: `/pipeline-diagram/completed.html`
- Term cockpit shell: built `term-control-center/dist/index.html`

All browser smoke loads returned HTTP 200 and non-empty screenshots.

## Surface evidence map

- Navigation shell, mobile bottom tabs, More sheet, completion center, activity center, review notifications, terminal session list: covered by `boardGuardrails.test.ts` and Playwright screenshots for Board/Pipeline/WIP/Completed widths.
- Term shell, terminal panes, active jobs, Browser-QA toolbar, diff inspector, explain overlay, review aids, mobile pane switching, touch/context-menu/keyboard selection guardrails: covered by `termBasePath.test.ts` and full `npm --prefix term-control-center test`.
- Admin local/hosted auth and responsive admin project defaults: covered by `admin.test.ts`; no live admin screenshot was captured in this pass.
- Slack activity sink delivery: covered by `test_slack_activity_sink.py` and guardrail tests; no live Slack send performed.
- Reduced motion: covered by global CSS guardrails plus terminal xterm reduced-motion static tests.

## Validation commands tied to this QA pass

- `npm --prefix term-control-center run typecheck` — passed.
- `npm --prefix term-control-center test` — passed (593/593).
- `npm --prefix term-control-center run build` — passed with existing Vite warnings.
- `PYTHONPATH=src python3 -m pytest tests/unit -q` — passed (1187 tests, 60 subtests).
- `git diff --check` — passed.

## Residual manual QA notes

- This is automated browser-smoke plus static/test evidence, not a human tactile iPad/phone session.
- Touch/trackpad/context-menu/keyboard selection behavior is validated by existing unit/static guardrails and requires real-device confirmation before production rollout if the team requires hardware-level signoff.
- Local-AI explanation code was not modified in this issue because the mandatory local-AI researcher consult returned unusable responses; existing explain overlay tests remain passing.
