import json
import os
from typing import Any, Dict

STATE_FILE = "state.json"


def load_state() -> Dict[str, Any]:
    """Load and return the state from `STATE_FILE`.

    If the file does not exist, return a default state.
    """
    if not os.path.exists(STATE_FILE):
        return {"tasks": [], "notes": []}
    with open(STATE_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_state(state: Dict[str, Any]) -> None:
    """Write `state` to `STATE_FILE` using pretty JSON (indent=4)."""
    with open(STATE_FILE, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=4)


def next_task_id(state: Dict[str, Any]) -> int:
    """Return the next integer id for a new task.

    Looks at `state["tasks"]` for existing integer `id` values and
    returns max(id) + 1 or 1 if there are no tasks.
    """
    tasks = state.get("tasks") or []
    ids = [t.get("id") for t in tasks if isinstance(t, dict) and isinstance(t.get("id"), int)]
    return max(ids) + 1 if ids else 1


def next_note_id(state: Dict[str, Any]) -> int:
    """Return the next integer id for a new note.

    Same logic as `next_task_id` but for `state["notes"]`.
    """
    notes = state.get("notes") or []
    ids = [n.get("id") for n in notes if isinstance(n, dict) and isinstance(n.get("id"), int)]
    return max(ids) + 1 if ids else 1
