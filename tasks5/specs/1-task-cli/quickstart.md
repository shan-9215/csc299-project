# Quickstart: Task CLI

## Prerequisites

- Python 3.11+
- `pytest` (for running tests)

## Install (developer)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest
```

## Run (examples)

- Add a task:

```bash
python -m src.cli add "Buy milk"
```

- List tasks:

```bash
python -m src.cli list
```

- List tasks as JSON:

```bash
python -m src.cli list --json
```

- Mark a task completed:

```bash
python -m src.cli done 1
```

## Storage

Default storage file: `tasks.json` in the project root. Override with `--file /path/to/tasks.json` on any command or set environment variable `TASKS_FILE`.

## Tests

Run all tests:

```bash
pytest -q
```

## Repair

If the storage file is corrupted, consult `research.md` for repair suggestions. The recommended step is to restore from a backup copy or move the corrupted file and re-run commands.
