import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

def inc(n: int) -> int:
    return n + 1

def get_tasks_file() -> str:
    return os.getenv("TASKS_FILE", "tasks.json")

def load_tasks() -> List[Dict[str, Any]]:
    tasks_file = get_tasks_file()
    if os.path.exists(tasks_file):
        with open(tasks_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    with open(get_tasks_file(), "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(description: str) -> Dict[str, Any]:
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description,
        "done": False,
        "completed_at": None
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

def list_tasks() -> List[Dict[str, Any]]:
    return load_tasks()

def search_tasks(term: str) -> List[Dict[str, Any]]:
    tasks = load_tasks()
    return [task for task in tasks if term.lower() in task["description"].lower()]

def complete_task(task_id: int) -> Optional[Dict[str, Any]]:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id and not task["done"]:
            task["done"] = True
            task["completed_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None

def main() -> None:
    import sys
    
    help_text = """
Tasks3 - A simple task manager

Usage: tasks3 <command> [args]

Commands:
    add <description>    Add a new task
                         Example: tasks3 add "Buy groceries"
    
    list                 Show all tasks
                         Example: tasks3 list
    
    search <term>        Search tasks by description
                         Example: tasks3 search "groceries"
    
    complete <id>        Mark a task as completed
                         Example: tasks3 complete 1
    """

    if len(sys.argv) < 2:
        print(help_text)
        sys.exit(1)

    command = sys.argv[1]
    if command == "add" and len(sys.argv) > 2:
        task = add_task(" ".join(sys.argv[2:]))
        print(f"Added task {task['id']}: {task['description']}")
    elif command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks found. Add one with: tasks3 add \"my task\"")
        else:
            print("\nYour tasks:")
            for task in tasks:
                status = "✓" if task["done"] else " "
                print(f"[{status}] {task['id']}: {task['description']}")
    elif command == "search" and len(sys.argv) > 2:
        term = " ".join(sys.argv[2:])
        tasks = search_tasks(term)
        if not tasks:
            print(f"No tasks found matching: {term}")
        else:
            print(f"\nTasks matching '{term}':")
            for task in tasks:
                status = "✓" if task["done"] else " "
                print(f"[{status}] {task['id']}: {task['description']}")
    elif command == "complete" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            task = complete_task(task_id)
            if task:
                print(f"✓ Completed task {task['id']}: {task['description']}")
            else:
                print(f"Task {task_id} not found or already completed")
        except ValueError:
            print("Task ID must be a number")
    else:
        print(help_text)
