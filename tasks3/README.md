# Tasks3 - A Simple Task Manager

A command-line task management tool built with Python that allows you to create, list, search, and complete tasks.

## Installation

Make sure you have `uv` installed, then run:

```bash
uv pip install -e .
```

## Usage

Run `uv run tasks3` to see available commands:

```bash
Tasks3 - A simple task manager

Usage: tasks3 <command> [args]

Commands:
    add <description>    Add a new task
                         Example: tasks3 add "Buy groceries"
    
    list                Show all tasks
                         Example: tasks3 list
    
    search <term>       Search tasks by description
                         Example: tasks3 search "groceries"
    
    complete <id>       Mark a task as completed
                         Example: tasks3 complete 1
```

### Examples

```bash
# Add a new task
uv run tasks3 add "Buy groceries"

# List all tasks
uv run tasks3 list

# Search for tasks
uv run tasks3 search "groceries"

# Complete a task
uv run tasks3 complete 1
```

## Development

### Project Structure
```
tasks3/
├── src/
│   └── tasks3/
│       └── __init__.py
├── tests/
│   ├── test_inc.py
│   └── test_tasks.py
└── pyproject.toml
```

### Running Tests

Run the test suite using:

```bash
uv run pytest
```

### Configuration

Tasks are stored in `tasks.json` by default. You can change the location by setting the `TASKS_FILE` environment variable:

```bash
export TASKS_FILE=/path/to/my/tasks.json
```

## Features

- UTF-8 JSON storage
- Simple command-line interface
- Search functionality
- Task completion tracking with timestamps
- Configurable storage location
- Unit test coverage
