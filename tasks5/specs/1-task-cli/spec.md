# Feature Specification: Task CLI (add/list/complete)

**Feature Branch**: `1-task-cli`
**Created**: 2025-11-19
**Status**: Draft
**Input**: User description: "Using the existing constitution, write a detailed specification for a Python CLI task manager with commands: add, list, and complete. Include: data model (id, description, completed), JSON file storage, and basic command-line usage examples."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add task (Priority: P1)
A user wants to add a new task with a short description so they can track work.

**Why this priority**: Core user flow; enables creation of content used by other commands.

**Independent Test**: Run the CLI `add` command and verify the task is persisted to the configured JSON file.

**Acceptance Scenarios**:

1. **Given** an empty tasks file, **When** the user runs `task add "Buy milk"`, **Then** a new task is appended with `id` = 1, `description` = "Buy milk", and `completed` = false.
2. **Given** existing tasks with ids 1..N, **When** the user adds a task, **Then** the new task receives `id` = N+1 and the file reflects the new entry.
3. **Given** the storage file is temporarily locked or unavailable, **When** `task add` runs, **Then** the CLI returns a non-zero exit code and a helpful error message; no partial/corrupt writes occur.

---

### User Story 2 - List tasks (Priority: P1)
A user wants to view all current tasks in a human-readable list or machine-readable JSON.

**Why this priority**: Observation/read operations are critical for verifying state and for UX.

**Independent Test**: Run `task list` after adding tasks and verify output contains the expected tasks.

**Acceptance Scenarios**:

1. **Given** tasks exist, **When** the user runs `task list`, **Then** tasks are displayed ordered by `id` ascending, showing `id`, `description`, and `completed` status.
2. **Given** the user requests machine output (`--json`), **When** `task list --json` runs, **Then** the output is valid JSON representing an array of task objects matching the data model.

---

### User Story 3 - Complete task (Priority: P1)
A user wants to mark a task as completed so it is known to be done.

**Why this priority**: Fundamental state change enabling task lifecycle.

**Independent Test**: Add a task, run `task done <id>`, and assert the stored task's `completed` is true.

**Acceptance Scenarios**:

1. **Given** a task with `id` 1 and `completed` = false, **When** the user runs `task done 1`, **Then** the stored task has `completed` = true and `task list` shows it as completed.
2. **Given** a non-existent id, **When** `task done <id>` is invoked, **Then** the CLI returns a non-zero exit code and a clear error ("Task not found") without modifying the file.

---

### Edge Cases

- Attempting to add an empty description should return an error; the CLI MUST validate input.
- Duplicate descriptions are allowed (system identifies tasks by `id`, not description).
- Concurrent writers: the system assumes single-user CLI in typical usage; behavior under concurrent modifications MUST be documented and is out-of-scope for the MVP.
- File corruption: the system MUST perform atomic writes to avoid partial updates.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a task with a non-empty description via a CLI command: `task add "<description>"`.
- **FR-002**: System MUST allow users to list tasks via `task list` and support a machine-readable JSON flag `--json`.
- **FR-003**: System MUST allow users to mark a task completed via `task done <id>` (or `task complete <id>` alias).
- **FR-004**: The system MUST persist tasks to a JSON file on disk and load from it on startup of CLI commands.
- **FR-005**: Task `id` MUST be an integer, unique, and assigned monotonically increasing by the system.
- **FR-006**: All writes to the JSON file MUST be atomic (write-temp → fsync → rename) to prevent corruption on crashes.
- **FR-007**: The CLI MUST return standard Unix exit codes: 0 for success, non-zero for errors; error messages MUST be user-friendly.
- **FR-008**: The system MUST provide a configurable storage path (default: `tasks.json` in repository root or user home config) and document it.

### Non-functional Requirements

- **NFR-001**: Typical commands (`add`, `list`, `done`) MUST complete within 1 second for normal taskset sizes (<= 1000 tasks).
- **NFR-002**: The implementation MUST minimize external dependencies; stdlib solutions preferred.
- **NFR-003**: Tests MUST be runnable with `pytest` and exist for the three primary user stories and key edge cases.

## Key Entities *(include if feature involves data)*

- **Task**: Represents a single task with attributes:
  - `id`: integer (unique, monotonic)
  - `description`: string (non-empty)
  - `completed`: boolean

- **Storage**: JSON file containing an array of Task objects. The storage interface SHOULD allow reading the full list and writing an updated list atomically.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of acceptance scenarios (per-user-stories above) pass in automated tests.
- **SC-002**: `task add` / `task list` / `task done` commands complete in <1s for datasets up to 1000 tasks on developer machines.
- **SC-003**: Tasks persist across CLI invocations and system restarts (verified by tests that restart state between runs).
- **SC-004**: No corrupted storage files after simulated crash during write in tests (atomic write behavior validated).

## Assumptions

- The tool is primarily single-user, invoked interactively on a developer or user machine; heavy concurrent access is out-of-scope for MVP.
- The requester specified Python and JSON storage; these are recorded here as explicit constraints to guide implementation and tests.
- Default storage file: `tasks.json` at repository/project root. Implementations MAY provide an environment variable or CLI flag to override.
- Target environment: POSIX-compatible shells, with `zsh` as the default development shell.

## Basic Command-line Usage Examples (for users)

- Add a task (human-friendly):

```
$ task add "Buy milk"
Added task 1: "Buy milk"
```

- List tasks (human-friendly):

```
$ task list
1. [ ] Buy milk
2. [x] Pay bills
```

- List tasks (machine-readable JSON):

```
$ task list --json
[ { "id": 1, "description": "Buy milk", "completed": false }, { "id": 2, "description": "Pay bills", "completed": true } ]
```

- Mark a task completed:

```
$ task done 1
Task 1 marked completed.
```

## Implementation Constraints (documented for planners)

- The user requested Python and JSON file storage; this constraint is recorded to ensure the implementation and test artifacts align.
- The constitution requires a library/CLI separation; plans should provide an importable module containing the task logic and a thin CLI wrapper.


---

*Spec generated from user feature request and aligned to project constitution.*
