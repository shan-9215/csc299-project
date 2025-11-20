"""Thin CLI adapter for the Task CLI.

Usage (module): python -m src.cli add "Buy milk"
"""
import argparse
import json
import sys
from pathlib import Path

from tasks import add_task, list_tasks, complete_task, Task


def default_tasks_file() -> Path:
    return Path("tasks.json")


def cmd_add(args):
    try:
        task = add_task(args.description, args.file)
        print(f'Added task {task.id}: "{task.description}"')
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args):
    try:
        tasks = list_tasks(args.file)
        if args.json:
            out = [t.to_dict() for t in tasks]
            print(json.dumps(out, ensure_ascii=False))
        else:
            for t in tasks:
                mark = "x" if t.completed else " "
                print(f"{t.id}. [{mark}] {t.description}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def cmd_done(args):
    try:
        task = complete_task(int(args.id), args.file)
        print(f"Task {task.id} marked completed.")
        return 0
    except ValueError:
        print("Invalid id", file=sys.stderr)
        return 1
    except Exception as e:
        # NotFoundError -> 2; other IO -> 3
        msg = str(e)
        if "not found" in msg.lower():
            print(msg, file=sys.stderr)
            return 2
        print(f"Error: {e}", file=sys.stderr)
        return 3


def build_parser():
    parser = argparse.ArgumentParser(prog="task")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", help="Task description")
    p_add.add_argument("--file", type=Path, default=default_tasks_file(), help="Path to tasks JSON file")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--json", action="store_true", dest="json", help="Output JSON")
    p_list.add_argument("--file", type=Path, default=default_tasks_file(), help="Path to tasks JSON file")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark task completed")
    p_done.add_argument("id", help="Task id to mark as done")
    p_done.add_argument("--file", type=Path, default=default_tasks_file(), help="Path to tasks JSON file")
    p_done.set_defaults(func=cmd_done)

    # alias: complete
    p_complete = sub.add_parser("complete", help=argparse.SUPPRESS)
    p_complete.add_argument("id", help=argparse.SUPPRESS)
    p_complete.add_argument("--file", type=Path, default=default_tasks_file(), help=argparse.SUPPRESS)
    p_complete.set_defaults(func=cmd_done)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
