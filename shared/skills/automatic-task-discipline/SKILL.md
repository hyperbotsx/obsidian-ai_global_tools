---
name: automatic-task-discipline
description: Proactively creates and maintains a task list for a user request with multiple requested outcomes, dependent implementation and verification steps, or enough scope that progress tracking prevents omissions. Use before executing such work; skip direct answers and genuinely one-step requests.
---

# Automatic Task Discipline

Create the list without asking the user to request a todo list. Use the native task tool available in the current harness.

## 1. Decide whether a list pays for itself

Create a list when the request has two or more independently verifiable outcomes, spans planning plus execution plus verification, changes multiple files or systems, or is likely to need more than a few tool calls.

Do not create a list for a direct answer, a single read, a one-command check, or a narrow one-file edit with an obvious verification step. Do not split one coherent action into artificial tasks.

## 2. Start the list before acting

1. Create a concise, outcome-oriented list of 2–7 tasks. Include verification when it is distinct work.
2. Mark the first task in progress before non-read work.
3. For a request such as “do A, B, and C,” create one task per independently deliverable outcome, in dependency order.

### Harness bindings

| Harness | Task tool | Start a list |
| --- | --- | --- |
| Pi | `TaskCreate`, `TaskUpdate`, `TaskList` | Create the tasks with `TaskCreate`, mark the first `in_progress` with `TaskUpdate`, and keep the list current with `TaskList`. |
| Claude Code | `TodoWrite` | Write the tasks with exactly one `in_progress` item. |

If no task tool is available, do not claim that a list exists.

## 3. Keep it truthful

1. Mark a task done immediately after its acceptance condition is met.
2. Mark the next task in progress before beginning it.
3. Update the list if the scope materially changes; do not retain stale tasks.
4. Before the final response, ensure every task is done or state the blocker plainly.

## Success criteria

A multi-step request has a small, current task list without the user needing to ask. Simple requests stay free of process overhead.
