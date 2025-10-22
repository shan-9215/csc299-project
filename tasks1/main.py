#!/usr/bin/env python3

import json
import sys
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "tasks.json"

def init_tasks_file():
    """Initialize tasks file if it doesn't exist"""
    if not TASKS_FILE.exists():
        with open(TASKS_FILE, 'w') as f:
            json.dump([], f)

def load_tasks():
    """Load tasks from JSON file"""
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(title, description):
    """Add a new task"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: {title}")

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    for task in tasks:
        print(f"\nTask {task['id']}:")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")

def search_tasks(keyword):
    """Search tasks by keyword"""
    tasks = load_tasks()
    found = False
    
    for task in tasks:
        if (keyword.lower() in task['title'].lower() or 
            keyword.lower() in task['description'].lower()):
            if not found:
                found = True
                print("\nMatching tasks:")
            print(f"\nTask {task['id']}:")
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
    
    if not found:
        print(f"No tasks found matching '{keyword}'")

def print_usage():
    """Print usage instructions"""
    print("\nUsage:")
    print("  python3 main.py add \"Title\" \"Description\"  - Add a new task")
    print("  python3 main.py list                       - List all tasks")
    print("  python3 main.py search \"keyword\"           - Search tasks by keyword")
    print("  python3 main.py help                       - Show this help message")

def main():
    init_tasks_file()
    
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print_usage()
        return

    command = sys.argv[1].lower()

    if command == "add" and len(sys.argv) == 4:
        add_task(sys.argv[2], sys.argv[3])
    elif command == "list":
        list_tasks()
    elif command == "search" and len(sys.argv) == 3:
        search_tasks(sys.argv[2])
    else:
        print("Invalid command or arguments.")
        print_usage()

if __name__ == "__main__":
    main()