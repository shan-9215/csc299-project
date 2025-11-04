# tasks2 — Simple JSON Task CLI (small iteration)

This folder contains a small iteration of the task CLI with a few targeted improvements over tasks1:

- Added `complete <id>`: marks a task completed and stores `completed_at` as an ISO 8601 timestamp.
- Improved list output: shows a checkbox prefix (`[x]` or `[ ]`) and displays ID, Title, and Description neatly.
- Robust ID generation: uses `max([t["id"] for t in tasks], default=0) + 1` to avoid ID collisions after deletes.
- JSON files are read/written with `encoding="utf-8"`. An empty list file is created if missing.

Quick examples:
```bash
python3 main.py add "Buy milk" "2 liters"
python3 main.py list
python3 main.py search "milk"
python3 main.py complete 3
python3 main.py help
```