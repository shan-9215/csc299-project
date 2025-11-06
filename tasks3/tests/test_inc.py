import json
from tasks3 import add_task, complete_task, inc

def test_inc():
    assert inc(5) == 6
  

def test_add_task(tmp_path, monkeypatch):
    tmpfile = tmp_path / "test_tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(tmpfile))
    
    task = add_task("Test task")
    
    assert task["id"] == 1
    assert task["description"] == "Test task"
    assert task["done"] == False
    assert task["completed_at"] == None
    
    # Verify JSON file contents
    with open(tmpfile, encoding="utf-8") as f:
        saved_tasks = json.load(f)
    assert len(saved_tasks) == 1
    assert saved_tasks[0] == task

def test_complete_task(tmp_path, monkeypatch):
    tmpfile = tmp_path / "test_tasks.json"
    monkeypatch.setenv("TASKS_FILE", str(tmpfile))
    
    # Add a task first
    task = add_task("Test task")
    
    # Complete it
    completed = complete_task(1)
    
    assert completed["id"] == 1
    assert completed["done"] == True
    assert completed["completed_at"] is not None
