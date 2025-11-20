from pathlib import Path
from tasks.service import add_task, list_tasks, complete_task, NotFoundError
from tasks.model import Task


def test_add_and_list(tmp_path):
    p = tmp_path / "tasks.json"
    t = add_task("Do thing", p)
    assert t.id == 1
    items = list_tasks(p)
    assert len(items) == 1
    assert items[0].description == "Do thing"


def test_complete_task(tmp_path):
    p = tmp_path / "tasks.json"
    add_task("X", p)
    res = complete_task(1, p)
    assert res.completed is True


def test_complete_nonexistent(tmp_path):
    p = tmp_path / "tasks.json"
    add_task("X", p)
    try:
        complete_task(99, p)
        assert False, "expected NotFoundError"
    except NotFoundError:
        pass
