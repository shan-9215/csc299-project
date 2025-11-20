# CLI Contract: Task CLI

**Path**: `/Users/shan/Downloads/tasks5-spec-kit/specs/1-task-cli/contracts/cli-contract.md`

## Commands

- `task add "<description>"`
  - Exit code: `0` on success; `>0` on failure
  - Behavior: Adds a new task, prints summary line `Added task <id>: "<description>"`
  - Errors: empty description -> exit >0 with message

- `task list [--json]`
  - `--json`: outputs valid JSON array of `Task` objects
  - Default: human-readable list
  - Exit code: `0` on success

- `task done <id>` (alias `task complete <id>`)
  - Marks specified task completed; prints `Task <id> marked completed.` on success
  - Exit code: `>0` if task not found

## Output formats

- Human-readable list: one line per task: `<id>. [ ] description` or `<id>. [x] description`
- JSON: array of task objects matching data model

## Exit codes

- `0`: success
- `1`: invalid input (bad args, missing description)
- `2`: not found (task id missing)
- `3`: storage error (I/O, corrupted file)

