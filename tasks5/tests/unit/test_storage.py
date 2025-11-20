import os
from pathlib import Path
import json
import tempfile

from tasks.storage import save_tasks, load_tasks
from tasks.model import Task


def test_save_and_load(tmp_path):
    p = tmp_path / "tasks.json"
    tasks = [Task(id=1, description="A", completed=False)]
    save_tasks(p, tasks)
    loaded = load_tasks(p)
    assert len(loaded) == 1
    assert loaded[0].id == 1
    assert loaded[0].description == "A"
