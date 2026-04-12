# Tool Routing

Use targeted escalation. Do not run every tool on every bug check.

## Default Order

1. Manual review from audited scope
2. Fast pass on changed files and nearby tests
3. Deep review on silent-bug and edge-case lanes
4. Tool escalation only where the bug class justifies it
5. Verification before reporting

## Routing Table

| Situation | Best Tool Or Skill | Why |
|---|---|---|
| Repeated local code smell or suspicious pattern in changed files | `semgrep` | Cheap, broad pattern coverage with low setup cost |
| Cross-file flow from input to sink, permission boundary, or taint question | `codeql` | Better for interprocedural reasoning |
| Parser, serializer, reducer, or pure-function invariant | `property-based-testing` | Good for boundary and invariant discovery |
| Parser or state machine with complex input space | fuzzing skill such as `atheris`, `libfuzzer`, `cargo-fuzz`, or `aflpp` | Better than hand-picked examples once a harness exists |
| Suspected finding is interesting but shaky | `fp-check` | Forces evidence and removes weak claims |
| One issue is confirmed and sibling variants may exist | `variant-analysis` | Systematic search for same bug family |

## Semgrep First

Prefer `semgrep` when:
- the bug class is mostly local to one file
- you can describe it as a recurring pattern
- you want quick breadth before deep reasoning

Avoid `semgrep` as the only step for:
- state-machine bugs
- stale state bugs
- workflow bugs that depend on ordering

## CodeQL Only When Needed

Prefer `codeql` when:
- the bug depends on dataflow across functions or files
- user-controlled input may cross trust boundaries
- the interesting question is "can this value reach that sink?"

Avoid `codeql` when:
- the issue is already obvious by inspection
- the scope is tiny and local

## Fuzzing And Property-Based Testing

Escalate only when:
- the surface is parser-heavy, stateful, or rich in boundary behavior
- the basic review already found risk worth deeper automated exploration
- the project has or can support a harness without disproportionate setup cost

## Verification Rule

Tool output is evidence, not a finding by itself. Every tool result still needs:
- scope relevance
- code confirmation
- failure mechanism
- confidence tag
