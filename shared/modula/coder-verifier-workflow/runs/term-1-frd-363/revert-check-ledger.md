# Revert-check ledger — FRD #363

Exact-wiring mutation evidence. Each entry deleted/neutered the named production wiring in a scratch copy and re-ran the guard's test; all failed as intended.

## revert-checks-final

- `F001` — # pass 0 # fail 1 
- `F002` — # pass 0 # fail 1 
- `F003` — # pass 0 # fail 1 
- `F004` — # pass 0 # fail 1 
- `F005-pty` — # pass 0 # fail 1 
- `F005-reason` — # pass 0 # fail 1 
- `F006` — # pass 0 # fail 1 
- `F007-baseline` — # pass 0 # fail 1 
- `F007-grace` — # pass 0 # fail 1 
- `F007-sink` — # pass 0 # fail 1 
- `F008` — # pass 1 # fail 1 

## revert-checks-r2

- `F002-await` — # pass 0 # fail 1 
- `F006-boundary` — # pass 0 # fail 1 
- `F007-summary` — # pass 0 # fail 1 
- `F008-ast` — # pass 1 # fail 1 

## revert-checks-r3

- `F002-browser` — # pass 0 # fail 1 
- `F002-browser-observer` — # pass 0 # fail 2 
- `F002-browser-prepare` — # pass 0 # fail 1 
- `F002-browser-spawn` — # pass 0 # fail 1 
- `F002-lane-capacity` — # pass 0 # fail 1 
- `F002-lane-slots` — # pass 0 # fail 1 
- `F008-five` — # pass 1 # fail 1 
- `F008-format` — # pass 2 # fail 0 
- `F008-rename` — # pass 2 # fail 0 

## revert-checks-cp2

- `FR5-action-parse` — # pass 0 # fail 2 
- `FR5-board` — # pass 1 # fail 1 
- `FR5-board-light` — # pass 1 # fail 1 
- `FR5-coworker` — # pass 1 # fail 1 
- `FR5-direct-gate` — # pass 0 # fail 1 
- `FR5-intake-snapshot` — # pass 0 # fail 1 
- `FR5-intake-ui` — # pass 1 # fail 1 
- `FR5-intake-validation` — # pass 0 # fail 1 
- `FR5-intake-view` — # pass 0 # fail 1 
- `FR5-launch-context-default` — # pass 0 # fail 1 
- `FR5-launch-default` — # pass 0 # fail 1 
- `FR6-lane-gate` — # pass 0 # fail 1 
- `FR7-continue-wiring` — # pass 0 # fail 1 
- `FR8-operator-reason` — # pass 0 # fail 1 

## revert-checks-cp2-r1

- `F001-parser` — # pass 0 # fail 1 
- `F002-reason` — # pass 0 # fail 1 
- `F003-mode` — # pass 0 # fail 1 
- `F003-skip` — # pass 0 # fail 1 
- `F003-trim` — # pass 0 # fail 1 
- `shared-validator` — # pass 1 # fail 1 
- `sweep-edit-note` — # pass 0 # fail 1 
- `sweep-group-reason` — # pass 0 # fail 1 
- `sweep-pagebot-inject` — # pass 0 # fail 1 
- `sweep-pagebot-send` — # pass 0 # fail 1 
- `sweep-pane-reason` — # pass 0 # fail 1 
- `sweep-planning-text` — # pass 0 # fail 1 
- `sweep-question` — # pass 0 # fail 1 
- `sweep-receipt-reason` — # pass 0 # fail 1 
- `sweep-resolution` — # pass 0 # fail 1 
- `sweep-state-read` — # pass 0 # fail 1 
- `sweep-state-write` — # pass 0 # fail 1 

