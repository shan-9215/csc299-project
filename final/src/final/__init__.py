from final import commands


def main() -> None:
    from final.storage import load_state, save_state

    state = load_state()

    print("Welcome to final.")
    print("Type 'help' to see commands.")

    while True:
        try:
            cmd = input("> ")
        except (EOFError, KeyboardInterrupt):
            save_state(state)
            print("\nGoodbye.")
            break

        if cmd is None:
            continue
        cmd = cmd.strip()
        if not cmd:
            continue

        cmd_l = cmd.lower()

        if cmd_l == "quit":
            save_state(state)
            print("Goodbye.")
            break
        elif cmd_l == "help":
            print("Commands:")
            print("  add-task")
            print("  list-tasks")
            print("  complete-task <id>")
            print("  add-note")
            print("  list-notes")
            print("  view-note <id>")
            print("  ai-plan        # generate a daily plan from open tasks")
            print("  reset-state          # delete ALL tasks and notes (with confirmation)")
            print("  search <query>")
            print("  help")
            print("  quit")
        elif cmd_l == "add-task":
            commands.add_task(state)
            save_state(state)
        elif cmd_l == "list-tasks":
            commands.list_tasks(state)
        elif cmd_l.startswith("complete-task"):
            parts = cmd_l.split()
            if len(parts) != 2:
                print("Usage: complete-task <id>")
                continue
            try:
                task_id = int(parts[1])
            except ValueError:
                print(f"Invalid task id: {parts[1]}")
                continue
            commands.complete_task(state, task_id)
            save_state(state)
        elif cmd_l == "add-note":
            commands.add_note(state)
            save_state(state)
        elif cmd_l == "list-notes":
            commands.list_notes(state)
        elif cmd_l == "ai-plan":
            commands.ai_plan(state)
        elif cmd_l == "reset-state":
            commands.reset_state(state)
            save_state(state)
        elif cmd_l.startswith("view-note"):
            parts = cmd_l.split()
            if len(parts) != 2:
                print("Usage: view-note <id>")
                continue
            try:
                note_id = int(parts[1])
            except ValueError:
                print(f"Invalid note id: {parts[1]}")
                continue
            commands.view_note(state, note_id)
        elif cmd_l.startswith("search"):
            parts = cmd.split()
            if len(parts) == 1:
                print("Usage: search <query>")
                continue
            query = " ".join(parts[1:])
            commands.search_all(state, query)
        else:
            print("Unknown command. Type 'help'.")
