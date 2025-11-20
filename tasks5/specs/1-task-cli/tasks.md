---

description: "Task list for Task CLI feature (add/list/done)"

---

# Tasks: Task CLI (add/list/complete)

**Input**: Design docs from `/specs/1-task-cli/`
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories), `data-model.md`, `contracts/`, `research.md`, `quickstart.md`

## Phase 1: Setup (Project initialization)

- [ ] T001 Initialize Python project skeleton and folders: create `src/tasks/`, `src/__init__.py`, `tests/`, `tests/unit/`, `tests/integration/` (path: project root)
- [ ] T002 Add `.gitignore` that excludes `tasks.json`, `.venv/`, `__pycache__/` (path: project root)
- [ ] T003 Create minimal `pyproject.toml` or `requirements.txt` listing `pytest` as dev dependency (path: project root)

## Phase 2: Foundational (Blocking prerequisites)

- [ ] T004 [P] Implement project logging and helper utilities in `src/tasks/utils.py` (path: `src/tasks/utils.py`) — include safe file path helpers and simple logger used by other modules
- [ ] T005 [P] Define `Task` dataclass and validators in `src/tasks/model.py` (path: `src/tasks/model.py`)
- [ ] T006 [P] Implement atomic JSON read/write utilities in `src/tasks/storage.py` (path: `src/tasks/storage.py`) — functions: `load_tasks(path)`, `save_tasks(path, tasks)` (use tempfile+fsync+os.replace)
- [ ] T007 [P] Implement ID allocation helper in `src/tasks/storage.py` or `src/tasks/service.py` to return `max_id + 1` (path: `src/tasks/storage.py`)
- [ ] T008 Add CI/test configuration placeholder (e.g., `tox.ini` or GitHub Actions workflow stub) in `.github/workflows/ci.yml` (path: `.github/workflows/ci.yml`) to run `pytest` (optional minimal stub)

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add a task via CLI and persist it.
**Independent Test**: Run CLI `add` and assert new task appears in storage file with `completed=false` and monotonic id.

- [ ] T010 [US1] Create business logic `add_task(description: str, file_path: Path)` in `src/tasks/service.py` (path: `src/tasks/service.py`)
- [ ] T011 [US1] Wire `add_task` to storage: call `load_tasks` then `save_tasks` with new entry (path: `src/tasks/service.py`)
- [ ] T012 [US1] Implement CLI command mapping for `add` in `src/cli.py` (path: `src/cli.py`) — parse description, call library, print success message
- [ ] T013 [US1] Add unit tests for `add_task` behavior in `tests/unit/test_service.py` (path: `tests/unit/test_service.py`) (TDD: write test first)
- [ ] T014 [US1] Add integration test for `task add` end-to-end using `subprocess` or `click.testing` style in `tests/integration/test_cli_end_to_end.py` (path: `tests/integration/test_cli_end_to_end.py`)
- [ ] T015 [US1] Validate input: implement description non-empty validation in `src/tasks/model.py` or `service.py` and test (path: `src/tasks/model.py`)
- [ ] T016 [US1] Document `add` usage in `specs/1-task-cli/quickstart.md` and update README (path: `specs/1-task-cli/quickstart.md`)

## Phase 4: User Story 2 - List Tasks (Priority: P1)

**Goal**: Allow users to list tasks in human-readable and JSON formats.
**Independent Test**: After adding tasks, `task list` returns ordered IDs and `task list --json` returns valid JSON matching the data model.

- [ ] T020 [US2] Implement `list_tasks(file_path: Path, as_json: bool=False)` in `src/tasks/service.py` (path: `src/tasks/service.py`)
- [ ] T021 [US2] Implement CLI mapping for `list` and `--json` flag in `src/cli.py` (path: `src/cli.py`)
- [ ] T022 [US2] Add unit tests for `list_tasks` in `tests/unit/test_service.py` (path: `tests/unit/test_service.py`)
- [ ] T023 [US2] Add integration test validating `task list` output formats in `tests/integration/test_cli_end_to_end.py` (path: `tests/integration/test_cli_end_to_end.py`)
- [ ] T024 [US2] Ensure `list` output is ordered by `id` ascending; add test to validate ordering (path: `tests/unit/test_service.py`)
- [ ] T025 [US2] Add CLI option to override storage file (`--file`) and test its behavior (path: `src/cli.py` and `tests/unit/test_service.py`)
- [ ] T026 [US2] Document `list` usage and `--json` flag in `specs/1-task-cli/quickstart.md` (path: `specs/1-task-cli/quickstart.md`)

## Phase 5: User Story 3 - Complete Task (Priority: P1)

**Goal**: Allow users to mark a task as completed.
**Independent Test**: After adding a task, `task done <id>` sets `completed=true` and persists change.

- [ ] T030 [US3] Implement `complete_task(task_id: int, file_path: Path)` in `src/tasks/service.py` (path: `src/tasks/service.py`)
- [ ] T031 [US3] Implement CLI mapping for `done` / `complete` in `src/cli.py` (path: `src/cli.py`)
- [ ] T032 [US3] Add unit tests for `complete_task` in `tests/unit/test_service.py` (path: `tests/unit/test_service.py`)
- [ ] T033 [US3] Add integration test for `task done <id>` behavior in `tests/integration/test_cli_end_to_end.py` (path: `tests/integration/test_cli_end_to_end.py`)
- [ ] T034 [US3] Implement and test error path for non-existent id (exit code and message) (path: `src/cli.py`, `tests/unit/test_service.py`)
- [ ] T035 [US3] Ensure atomic write behavior on completion operations; add test that simulates interrupted write (path: `tests/integration/test_cli_end_to_end.py`)
- [ ] T036 [US3] Update quickstart and README with `done` command examples (path: `specs/1-task-cli/quickstart.md`)

## Phase 6: Tests, CI & Validation

- [ ] T040 [P] Write unit tests for `model.py` validation rules in `tests/unit/test_model.py` (path: `tests/unit/test_model.py`)
- [ ] T041 [P] Write unit tests for `storage.py` atomic write/read edge cases in `tests/unit/test_storage.py` (path: `tests/unit/test_storage.py`)
- [ ] T042 [P] Add integration end-to-end tests covering add->list->done flows in `tests/integration/test_cli_end_to_end.py` (path: `tests/integration/test_cli_end_to_end.py`)
- [ ] T043 [P] Ensure tests run in CI by adding `pytest` invocation to `.github/workflows/ci.yml` (path: `.github/workflows/ci.yml`)
- [ ] T044 Add lint/format task (optional): configure `ruff`/`black` or document style guide in `README.md` (path: project root)
- [ ] T045 [P] Add test for corrupted file handling and repair guidance (path: `tests/integration/test_cli_end_to_end.py`)

## Phase 7: Documentation & Quickstart

- [ ] T050 Update `README.md` with project overview and example commands (path: `README.md`)
- [ ] T051 Expand `specs/1-task-cli/quickstart.md` with storage override examples and repair steps (path: `specs/1-task-cli/quickstart.md`)
- [ ] T052 Add CONTRIBUTING.md with development workflow and how to run tests (path: `CONTRIBUTING.md`)
- [ ] T053 Add inline docstrings and module-level docs for `src/tasks/*` (path: `src/tasks/` files)

## Phase 8: Polish & Cross-Cutting Concerns

- [ ] T060 Finalize error codes and messages consistent with CLI contract in `specs/1-task-cli/contracts/cli-contract.md` (path: `specs/1-task-cli/contracts/cli-contract.md`)
- [ ] T061 Evaluate any third-party dependency requests and document justifications (path: `specs/1-task-cli/plan.md`)
- [ ] T062 Prepare release notes / changelog entry for this feature (path: `CHANGELOG.md`)

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 must complete before user story implementation
- User Story phases (US1, US2, US3) depend on Phase 2 (storage & model) but are otherwise independent and can be implemented in parallel once foundational tasks are done.

## Parallel Opportunities

- `T004`, `T005`, `T006`, `T007`, `T040`, `T041` can be implemented in parallel by different contributors (library modules and tests).
- `T010`-`T016` (US1) can be done largely in parallel with `T020`-`T026` (US2) and `T030`-`T036` (US3) after Phase 2.

## Task Counts & Summary

- Total tasks: 62
- Tasks by story:
  - Setup/Foundation/CI/Docs: 22
  - US1 (Add): 7
  - US2 (List): 7
  - US3 (Done): 7
  - Tests & CI: 6
  - Docs & Polish: 7

## MVP Recommendation

- Implement Phase 1 + Phase 2 + Phase 3 (US1) first. Deliver a working `add` command with tests and quickstart. Then implement `list` and `done` in subsequent increments.

## Files generated

- `/Users/shan/Downloads/tasks5-spec-kit/specs/1-task-cli/tasks.md`

