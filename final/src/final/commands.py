"""Command stubs for the final app.

These functions are placeholders and will be implemented later.
They are intentionally minimal so tests and imports succeed.
"""
from typing import Dict
from final.storage import next_task_id, next_note_id
from final.ai_agent import summarize_description, generate_plan


def add_task(state: Dict) -> None:
    """Add a task to the state (stub).

    This version will ask for a long description first and then use the
    AI summarizer to suggest a short title which the user can accept or
    override.
    """
    description = input("description: ").strip()

    # Ask AI for a suggested short title based on the description.
    try:
        suggested_title = summarize_description(description)
    except Exception:
        suggested_title = ""

    if suggested_title:
        print(f"AI suggestion for title: {suggested_title}")

    title_input = input(f"Title (press Enter to accept AI suggestion): ").strip()
    title = title_input if title_input else suggested_title

    tags_raw = input("tags (comma-separated, optional): ").strip()
    priority_raw = input("priority (low / medium / high) [medium]: ").strip()
    due_date_raw = input("due_date (optional, YYYY-MM-DD or blank): ").strip()

    # Normalize tags into a list
    if tags_raw == "":
        tags_list = []
    else:
        tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]

    # Priority default
    priority = priority_raw.lower() if priority_raw else "medium"

    # Use None for blank due date
    due_date = due_date_raw or None

    # Get a new id using storage helper
    task_id = next_task_id(state)

    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "tags": tags_list,
        "status": "open",
        "priority": priority,
        "due_date": due_date,
    }

    state.setdefault("tasks", []).append(new_task)
    print(f"Added task {task_id}: {title}")


def list_tasks(state: Dict) -> None:
    """List tasks from the state.

    Prints a simple one-line summary per task. If there are no tasks,
    prints "No tasks found.".
    """
    tasks = state.get("tasks") or []
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        tid = task.get("id", "?")
        title = task.get("title", "(no title)")
        status = task.get("status", "?")
        priority = task.get("priority", "?")
        due = task.get("due_date") or "none"
        print(f"[{tid}] {title}  (status: {status}, priority: {priority}, due: {due})")


def complete_task(state: Dict, task_id: int) -> None:
    """Mark a task complete in the state.

    Searches `state['tasks']` for a task with matching `id`. Prints
    messages for not-found, already completed, or successful update.
    """
    tasks = state.get("tasks") or []
    # Find task by id
    target = None
    for t in tasks:
        if isinstance(t, dict) and t.get("id") == task_id:
            target = t
            break

    if target is None:
        print(f"Task {task_id} not found.")
        return

    current_status = target.get("status")
    if current_status == "done":
        print(f"Task {task_id} is already completed.")
        return

    target["status"] = "done"
    print(f"Marked task {task_id} as completed.")


def add_note(state: Dict) -> None:
    """Prompt for a note and append it to `state['notes']`.

    Prompts for title, content, and optional comma-separated tags.
    Uses `next_note_id` to assign a unique id.
    """
    title = input("title: ").strip()
    content = input("content: ").strip()
    tags_raw = input("tags (comma-separated, optional): ").strip()

    if tags_raw == "":
        tags_list = []
    else:
        tags_list = [t.strip() for t in tags_raw.split(",") if t.strip()]

    note_id = next_note_id(state)

    new_note = {
        "id": note_id,
        "title": title,
        "content": content,
        "tags": tags_list,
    }

    state.setdefault("notes", []).append(new_note)
    print(f"Added note {note_id}: {title}")


def list_notes(state: Dict) -> None:
    """List notes from the state.

    Prints a simple one-line summary per note. If there are no notes,
    prints "No notes found.".
    """
    notes = state.get("notes") or []
    if not notes:
        print("No notes found.")
        return

    for note in notes:
        nid = note.get("id", "?")
        title = note.get("title", "(no title)")
        tags = note.get("tags") or []
        tags_str = ", ".join(tags)
        print(f"[{nid}] {title}  (tags: {tags_str})")


def view_note(state: Dict, note_id: int) -> None:
    """View a note by id in the state.

    Searches `state['notes']` for a note with matching `id`. If found,
    prints a simple readable representation. Otherwise prints a not-found
    message.
    """
    notes = state.get("notes") or []
    target = None
    for n in notes:
        if isinstance(n, dict) and n.get("id") == note_id:
            target = n
            break

    if target is None:
        print(f"Note {note_id} not found.")
        return

    title = target.get("title", "(no title)")
    tags = target.get("tags") or []
    tags_str = ", ".join(tags)
    content = target.get("content", "")

    print(f"Title: {title}")
    print(f"Tags: {tags_str}")
    print("Content:")
    print(content)


def ai_plan(state: Dict) -> None:
    """Generate and print an AI plan for open tasks without modifying state.

    - Filters `state['tasks']` for tasks with `status == 'open'`.
    - If none, prints a message and returns.
    - Otherwise calls `generate_plan(open_tasks)` and prints the result.
    """
    tasks = state.get("tasks") or []
    open_tasks = [t for t in tasks if isinstance(t, dict) and t.get("status") == "open"]

    if not open_tasks:
        print("No open tasks to plan.")
        return

    try:
        plan_text = generate_plan(open_tasks)
    except Exception as e:
        print(f"AI planning error: {e}")
        return

    print("AI-generated plan:")
    print(plan_text)


def reset_state(state: Dict) -> None:
    """Prompt the user to confirm and, if confirmed, clear tasks and notes.

    This function does not delete the entire state object, only resets the
    `tasks` and `notes` lists to empty lists after user confirmation.
    """
    choice = input("Are you sure you want to delete ALL tasks and notes? (y/n): ").strip().lower()
    if choice != "y":
        print("State reset canceled.")
        return

    state["tasks"] = []
    state["notes"] = []
    print("State has been reset.")


def search_all(state: Dict, query: str) -> None:
    """Search tasks and notes for a query and print matches.

    - Matches in tasks: if query appears in title or description (case-insensitive).
    - Matches in notes: if query appears in title or content (case-insensitive).
    Prints simple lines for each match or "No matches found." if none.
    """
    q = (query or "").lower()
    found = False

    # Search tasks
    tasks = state.get("tasks") or []
    for t in tasks:
        title = (t.get("title") or "")
        desc = (t.get("description") or "")
        if q in title.lower() or q in desc.lower():
            tid = t.get("id", "?")
            priority = t.get("priority", "?")
            status = t.get("status", "?")
            print(f"Task [{tid}] {title}  (priority: {priority}, status: {status})")
            found = True

    # Search notes
    notes = state.get("notes") or []
    for n in notes:
        title = (n.get("title") or "")
        content = (n.get("content") or "")
        if q in title.lower() or q in content.lower():
            nid = n.get("id", "?")
            print(f"Note [{nid}] {title}")
            found = True

    if not found:
        print("No matches found.")
