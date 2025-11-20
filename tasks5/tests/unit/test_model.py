import pytest
from tasks.model import Task


def test_task_from_dict_valid():
    t = Task.from_dict({"id": 1, "description": "Buy milk", "completed": False})
    assert t.id == 1
    assert t.description == "Buy milk"
    assert t.completed is False


def test_task_from_dict_empty_description():
    with pytest.raises(ValueError):
        Task.from_dict({"id": 1, "description": "   ", "completed": False})
