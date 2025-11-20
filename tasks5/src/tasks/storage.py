import json
import os
import tempfile
from pathlib import Path
from typing import List

from .model import Task


def load_tasks(path: Path) -> List[Task]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    tasks = []
    for obj in data:
        tasks.append(Task.from_dict(obj))
    return tasks


def _atomic_write(path: Path, data: str) -> None:
    # write to a temp file on same filesystem, fsync, then replace
    dirpath = path.parent
    fd, tmp_path = tempfile.mkstemp(dir=dirpath)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, str(path))
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def save_tasks(path: Path, tasks: List[Task]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [t.to_dict() for t in tasks]
    text = json.dumps(data, ensure_ascii=False, indent=2)
    _atomic_write(path, text)


def next_id(tasks: List[Task]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1
