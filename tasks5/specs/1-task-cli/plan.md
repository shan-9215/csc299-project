# Implementation Plan: Task CLI (add/list/complete)

**Branch**: `1-task-cli` | **Date**: 2025-11-19 | **Spec**: /Users/shan/Downloads/tasks5-spec-kit/specs/1-task-cli/spec.md
**Input**: Feature specification from `/specs/1-task-cli/spec.md`

## Summary

Deliver a small Python project that provides a CLI `task` with three user commands: `add`, `list`, and `done` (alias `complete`). The implementation MUST follow the project constitution: library/CLI separation, file-backed JSON persistence, atomic writes, deterministic ID assignment, test-first development, and minimal dependencies.

## Technical Context

**Language/Version**: Python 3.11 (recommended)
**Primary Dependencies**: stdlib only (prefer `argparse`, `json`, `pathlib`, `tempfile`, `os`, `typing`); `pytest` for tests.
**Storage**: File-backed JSON (`tasks.json` by default). Access via a storage abstraction that performs atomic writes (write temp → fsync → rename).
**Testing**: `pytest` for unit and small integration tests.
**Target Platform**: POSIX-compatible shells (`zsh`, `bash`) and cross-platform where feasible.
**Project Type**: Single small CLI project with importable library under `src/`.
**Performance Goals**: CLI operations complete within 1 second for <= 1000 tasks.
**Constraints**: Minimal dependencies; single-user cooperative concurrency assumed.

## Constitution Check

Gates: Must demonstrate compliance with the project's Core Principles as specified in
`/Users/shan/Downloads/tasks5-spec-kit/.specify/memory/constitution.md`:
- Library/CLI separation (core logic importable under `src/tasks/`, CLI thin adapter)
- Data model enforcement: `id`, `description`, `completed`
- JSON persistence with atomic writes and documented storage path
- Tests covering user stories and edge cases (`pytest`)
- Minimal external dependencies; justify any additional dependency

Document any deviation in the Complexity Tracking section below.

## Project Structure

``text
src/
├── tasks/
│   ├── __init__.py
│   ├── model.py        # Task dataclass + validation
│   ├── storage.py      # Read/write JSON atomically
│   └── service.py      # Business logic: add/list/done
├── cli.py              # Thin CLI adapter using argparse

tests/
├── unit/
│   ├── test_model.py
│   ├── test_storage.py
│   └── test_service.py
└── integration/
    └── test_cli_end_to_end.py

tasks.json (default storage; not checked into VCS by default)
```

**Structure Decision**: Single project layout (src + tests). Keep CLI top-level `cli.py` to make invocation easy (`python -m src.cli` or make a small console script in package metadata later).

## Phase 0: Outline & Research (deliverable: research.md)

Unknowns / NEEDS_CLARIFICATION resolved by default choices:
- Atomic write approach: use write-to-temp + os.fsync + os.replace (cross-platform safe pattern documented in research.md).
- ID assignment: monotonic integer using max(existing_ids) + 1; document behavior when file empty or corrupted.
- Storage path default: project root `tasks.json` or override via `TASKS_FILE` env var or `--file` flag.
- CLI arg parsing library: use `argparse` from stdlib.

Research tasks:
- Research atomic write patterns in Python (tempfile, fsync, os.replace).
- Document best practice for locking vs. cooperative concurrency and state assumptions.
- Provide example code snippets for atomic write and ID allocation.

## Phase 1: Design & Contracts (deliverables: data-model.md, contracts/, quickstart.md)

Data model: See `data-model.md` (generated).

Contracts: CLI contract enumerating commands, flags, exit codes, and machine-readable output (`--json`) will be written to `/specs/1-task-cli/contracts/cli-contract.md`.

Quickstart: `quickstart.md` (deliverable) with usage examples and default config.

Agent context update: Script `.specify/scripts/bash/update-agent-context.sh` not executed here due to environment constraints. Manual note: update agent context with Python/CLI requirement if automated agent context tracking is used.

## Phase 2: Implementation Tasks (high-level)

Phase 2 is the start of implementation and mapping tasks to backlog items.

### Setup
- [ ] T001 Initialize project skeleton (create `src/tasks`, `tests/`), add `.gitignore` ignoring `tasks.json`.
- [ ] T002 Create `pyproject.toml` or minimal `requirements.txt` (only `pytest` as dev dependency).

### Core Implementation
- [ ] T010 [P] `src/tasks/model.py` — define `Task` dataclass and validation helpers.
- [ ] T011 [P] `src/tasks/storage.py` — implement `load_tasks(path)` and `save_tasks(path, tasks)` with atomic writes; include helper to get next id.
- [ ] T012 [P] `src/tasks/service.py` — implement `add_task(description, path)`, `list_tasks(path)`, `complete_task(id, path)` using storage layer.
- [ ] T013 `src/cli.py` — argparse-based thin CLI mapping to service functions; support `--file` override and `--json` output for `list`.

### Tests
- [ ] T020 Unit tests for model, storage, and service (fail-first approach).
- [ ] T021 Integration test: end-to-end CLI invocation using `subprocess` in a temporary directory to validate file writes and outputs.

### Documentation
- [ ] T030 `quickstart.md` with example commands and config.
- [ ] T031 Update README with how to run tests and contribute.

## Complexity Tracking

Any deviation from the constitution must be justified here. Current plan adheres to constitution principles. If a third-party library (e.g., `click`) is requested for improved CLI ergonomics, that must be justified and approved (MINOR version bump rationale).

## Delivery & Next Steps

- Create tasks in tracker or as GitHub issues using the task list above.
- Implement tests T020/T021 first and ensure they fail, then implement functionality until they pass.
- After Phase 1 artifacts (data-model.md, contracts/, quickstart.md) are created, re-run Constitution Check to confirm compliance.

**Plan file path**: /Users/shan/Downloads/tasks5-spec-kit/specs/1-task-cli/plan.md
