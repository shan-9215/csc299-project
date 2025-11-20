from pathlib import Path
from typing import List, Optional

from .model import Task
from .storage import load_tasks, save_tasks, next_id


class NotFoundError(Exception):
    pass


def add_task(description: str, file_path: Optional[Path] = None) -> Task:
    if not description or not description.strip():
        raise ValueError("Description must be non-empty")
    file_path = Path(file_path) if file_path is not None else Path("tasks.json")
    tasks = load_tasks(file_path)
    nid = next_id(tasks)
    task = Task(id=nid, description=description.strip(), completed=False)
    tasks.append(task)
    save_tasks(file_path, tasks)
    return task


def list_tasks(file_path: Optional[Path] = None) -> List[Task]:
    file_path = Path(file_path) if file_path is not None else Path("tasks.json")
    tasks = load_tasks(file_path)
    tasks_sorted = sorted(tasks, key=lambda t: t.id)
    return tasks_sorted


def complete_task(task_id: int, file_path: Optional[Path] = None) -> Task:
    file_path = Path(file_path) if file_path is not None else Path("tasks.json")
    tasks = load_tasks(file_path)
    for t in tasks:
        if t.id == task_id:
            if t.completed:
                # idempotent
                save_tasks(file_path, tasks)
                return t
            t.completed = True
            save_tasks(file_path, tasks)
            return t
    raise NotFoundError(f"Task with id {task_id} not found")
