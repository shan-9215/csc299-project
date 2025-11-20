# Task CLI

Simple command-line task manager storing tasks in a JSON file.

Usage examples:

```bash
python -m src.cli add "Buy milk"
python -m src.cli list
python -m src.cli list --json
python -m src.cli done 1
```

Default storage file: `tasks.json` in project root. Override with `--file /path/to/tasks.json`.
