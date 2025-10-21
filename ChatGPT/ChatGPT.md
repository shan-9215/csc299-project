# CSC 299 — PKMS/TMS Chat Agent

A compact end‑to‑end plan to ship a terminal‑based PKMS + task manager with AI‑assisted agents by **Nov 24, 2025 (1:30 PM)**.

---

## 0) Project elevator pitch

**Codename:** `pocket-sage`

A portable Python app that lets you:

* Capture notes/snippets and link them (PKMS)
* Track tasks with priorities, tags, deadlines (TMS)
* Chat in the terminal to **add/search/summarize/plan**
* Lightweight **agent** that reviews tasks/notes and proposes next steps
* Pluggable storage (start with **SQLite**, offer **JSON** fallback; optional **Neo4j** for links)

**Why this fits the rubric:**

* Uses AI‑coding assistants throughout (planning, specs, tests)
* Terminal chat interface (single binary‑like Python script)
* Multiple prototypes (JSON → SQLite → optional Neo4j; CLI → richer TUI)
* Versioned in GitHub with specs, tests, docs, video walkthrough

---

## 1) Milestones & timeline (shipping focus)

**Today → Deadline runway: ~34 days**

### Week 1 (Oct 21–27) — Foundation & Prototype A (JSON)

* Repo init with README + MIT license + `CONTRIBUTING.md`
* Define **command spec** (see §3)
* Implement core models (Note, Task) and JSON store
* Minimal chat loop (REPL): `add`, `list`, `find`, `done`, `link`, `help`, `quit`
* Unit tests: models + store + parser
* Smoke demo recorded (for YouTube draft)

### Week 2 (Oct 28–Nov 3) — Prototype B (SQLite) & Search

* Swap storage to SQLite via DAL interface
* Implement full‑text search (FTS5 if available; fallback LIKE)
* Add import/export JSON ⇄ SQLite
* Add basic **agent-draft**: daily review → propose top 3 tasks & relevant notes
* Tests for DAL & search; CLI snapshot tests

### Week 3 (Nov 4–10) — Quality, TUI polish, Spec/Docs

* Optional TUI polish with `rich` prompts; improve errors and help
* Add recurrence & deadlines; calendarish view
* Agent v2: tag inference + “next actionable step” suggestions
* Begin **spec.md** and test plan; add `video.txt` placeholder (YouTube URL later)

### Week 4 (Nov 11–17) — Optional Prototype C (Neo4j) & Integrations

* Optional: Neo4j DAL for rich linking graph (if time). Else ship Graph‑lite on SQLite
* Add `summarize` and `plan` commands using local heuristics (no external API required)
* Freeze features; start perf pass and portability test (Windows/OSX/Linux)

### Final Week (Nov 18–24) — Stabilize & Ship

* Fill docs: README, INSTALL, USAGE, DESIGN, SPEC, TESTING, CHANGELOG
* Record 6–8 min demo (script in §10)
* Tag `v1.0.0`, verify `video.txt` contains YouTube URL
* Final checklist run (see §11)

---

## 2) Architecture (portable, layered)

```
┌───────────────────────────────┐
│           CLI / Chat          │  ← REPL parser, commands, help
├───────────────────────────────┤
│       Services / Agents       │  ← suggest_next_actions(), summarize(), plan()
├───────────────────────────────┤
│     Domain (Models & Ops)     │  ← Note, Task, Link, Tag; search(), link(), etc.
├───────────────────────────────┤
│        Data Access (DAL)      │  ← JSONStore | SQLiteStore | Neo4jStore
├───────────────────────────────┤
│       Persistence / Files     │  ← data/*.json, pocket.db, config.toml
└───────────────────────────────┘
```

* **DAL interface** keeps storage pluggable
* **Services/Agents** work on DAL; no UI or storage coupling
* **CLI** stays thin: parse → call service → pretty‑print

**Dependencies (kept light):** `rich` (nice terminal), `pydantic` (validation), `sqlalchemy` (SQLite), `typer` or simple REPL; *optional* `py2neo` for Neo4j.

---

## 3) Command design (chat‑style)

Use natural prompts; we parse with simple intent rules:

* `add task "title" [--due YYYY-MM-DD] [--p N] [--tags x,y] [--note "text"]`
* `add note "title" --body "..." [--tags x,y]`
* `link note:<id> task:<id> [label:"context"]`
* `find task "query" [--tag x] [--due <op>date] [--open]`
* `find note "query" [--tag x]`
* `list tasks [--open|--done] [--sort due|p]`
* `done <task_id>` / `reopen <task_id>`
* `summarize [today|week]` → agent digest of top items
* `plan [today|week]` → agent proposes schedule/next steps
* `import json <path>` / `export json <path>`
* `help` / `quit`

**Stretch:** `@ask "How many tasks are due this week?"` → NL query to command translation (rule‑based).

---

## 4) Data model (initial)

**Task**

* id (str/uuid), title, description, status(enum: open/done), priority(int 1–5), due(date|None), tags(list[str]), created, updated

**Note**

* id, title, body(markdown), tags(list[str]), created, updated

**Link**

* id, src(id), dst(id), label(optional)

**Storage**

* JSON: `data/tasks.json`, `data/notes.json`, `data/links.json`
* SQLite tables: `tasks`, `notes`, `links`, `tags` (m2m), plus FTS virtual tables (if enabled)

---

## 5) Prototypes (with explicit goals)

### Prototype A — JSON (Week 1)

* Focus: Command parsing, basic CRUD, simple search, linking
* Success: Add/list/find tasks & notes; links show related info; all covered by tests

### Prototype B — SQLite (Week 2)

* Focus: Reliability, indexing, FTS, import/export
* Success: Same features but faster & robust; CLI parity; tests green

### Prototype C — Agent v1/v2 (Week 2–3)

* **v1**: Daily review summary of open tasks sorted by due/priority with 2 related notes
* **v2**: For each open task, suggest a **next action** sentence and **tag suggestions** (heuristics)

### Prototype D — Neo4j (Optional, Week 4)

* Focus: Visualize rich links, shortest paths between notes/tasks
* Success: Basic create/list/query relationships; optional export graph

---

## 6) Study plan (short, targeted)

**Core topics to review (10–12 hours total):**

1. Python packaging, virtualenv, CLI patterns (Typer / argparse)
2. SQLite + SQLAlchemy; FTS basics
3. Test‑driven dev with `pytest` and fixtures
4. Terminal UX with `rich` (tables, prompts, traceback)
5. Basic heuristics for agents (priority scoring, timeboxing)
6. (Optional) Neo4j node/edge modeling

**Suggested schedule (blended with build):**

* **Day 1–2:** CLI & models refresher; write first 5 tests
* **Day 3:** JSON DAL + CRUD; docstrings & type hints
* **Day 4:** Search + linking; smoke demo
* **Week 2 Mon–Tue:** SQLite DAL; migrations; FTS
* **Week 2 Wed–Thu:** Agent v1; summarize/plan commands
* **Week 3:** Error handling, UX polish, docs; Agent v2
* **Week 4:** Optional Neo4j; perf; portability checks

---

## 7) Test plan (examples)

* **Unit:** Model validation; DAL CRUD; search; link invariants
* **CLI:** Golden output snapshot for `list`, `find`, `summarize`
* **Agent:** Deterministic heuristics with fixed fixtures (no network)
* **Portability:** Run on macOS (your dev), GitHub Actions for Ubuntu/Windows

---

## 8) Repo layout

```
 pocket-sage/
 ├─ src/pocketsage/
 │   ├─ __init__.py
 │   ├─ cli.py            # REPL / command dispatch
 │   ├─ models.py         # pydantic models
 │   ├─ services.py       # business logic + agents
 │   ├─ dal/
 │   │   ├─ base.py       # interface
 │   │   ├─ json_store.py
 │   │   └─ sqlite_store.py
 │   └─ utils.py
 ├─ tests/
 │   ├─ test_models.py
 │   ├─ test_dal_json.py
 │   ├─ test_cli.py
 │   └─ fixtures/
 ├─ data/                 # dev data
 ├─ README.md
 ├─ SPEC.md               # feature spec & acceptance criteria
 ├─ DESIGN.md             # architecture notes
 ├─ TESTING.md            # how to run tests
 ├─ video.txt             # YouTube URL (filled later)
 ├─ pyproject.toml        # build & deps
 └─ LICENSE
```

---

## 9) Acceptance criteria (rubric alignment)

* **Runs in terminal**; commands in §3 supported and documented
* **Portable** (tested on macOS + GitHub Actions on Ubuntu/Windows)
* **State persisted** in JSON and SQLite; import/export works
* **Agent features**: `summarize`/`plan` produce useful output deterministically
* **Multiple prototypes** evidenced by tags/branches & `CHANGELOG`
* **Fine‑grained commits**: specs → tests → impl → docs per feature
* **Demo video (6–8 min)** linked in `video.txt`

---

## 10) Demo video script (6–8 minutes)

1. **Intro (0:30)**: problem + goals; stack; portability
2. **Tour (2:30)**: add/find/link/done; JSON vs SQLite; FTS search
3. **Agent (1:30)**: show `summarize`/`plan` on real data
4. **Design (1:00)**: DAL abstraction; models; tests; CI
5. **Dev story (1:00)**: prototypes, challenges, what changed
6. **Wrap (0:30)**: how to run, limits, future work (Neo4j)

---

## 11) Final checklist

* [ ] README has install/run instructions & screenshots/GIFs
* [ ] Portability verified (macOS/Ubuntu/Windows via CI)
* [ ] `video.txt` populated with final YouTube URL
* [ ] Tags/branches show prototypes A/B/(C)
* [ ] Tests green; coverage > 80% on core modules
* [ ] SPEC/TESTING/DESIGN docs complete

---

## 12) Starter code (drop‑in)

> Minimal REPL and JSON DAL to get moving now.

```python
# src/pocketsage/cli.py
from datetime import date
from rich.table import Table
from rich.console import Console
from .services import Service

console = Console()
svc = Service.default()  # JSON by default; can swap to SQLite later

PROMPT = "pocket> "

def main():
    console.print("[bold cyan]Pocket Sage[/] — type 'help' for commands")
    while True:
        try:
            line = input(PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!")
            break
        if not line:
            continue
        if line in {"q", "quit", "exit"}:
            break
        out = svc.dispatch(line)
        console.print(out)

if __name__ == "__main__":
    main()
```

```python
# src/pocketsage/services.py
from dataclasses import dataclass
from .dal.json_store import JSONStore
from .models import Task, Note

@dataclass
class Service:
    store: object

    @staticmethod
    def default():
        return Service(JSONStore.default())

    def dispatch(self, line: str):
        tokens = line.split()
        cmd = tokens[0].lower()
        args = tokens[1:]
        if cmd == "help":
            return "Commands: add task|note, list tasks, find task|note <q>, done <id>, quit"
        if cmd == "add" and args and args[0] == "task":
            title = " ".join(args[1:]) or "Untitled"
            t = self.store.add_task(Task.new(title=title))
            return f"added task {t.id}: {t.title}"
        if cmd == "list" and args and args[0] == "tasks":
            tasks = self.store.list_tasks()
            return "\n".join(f"[{t.status}] {t.id} {t.title}" for t in tasks)
        if cmd == "find" and args and args[0] == "task":
            q = " ".join(args[1:])
            tasks = self.store.search_tasks(q)
            return "\n".join(f"[{t.status}] {t.id} {t.title}" for t in tasks)
        if cmd == "done" and args:
            tid = args[0]
            self.store.mark_done(tid)
            return f"marked {tid} done"
        return "unknown command; try 'help'"
```

```python
# src/pocketsage/models.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class Task:
    id: str
    title: str
    status: str = "open"
    created: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @staticmethod
    def new(title: str) -> "Task":
        return Task(id=str(uuid4())[:8], title=title)

@dataclass
class Note:
    id: str
    title: str
    body: str = ""
    created: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @staticmethod
    def new(title: str, body: str = "") -> "Note":
        return Note(id=str(uuid4())[:8], title=title, body=body)
```

```python
# src/pocketsage/dal/json_store.py
from __future__ import annotations
import json
from pathlib import Path
from typing import List
from ..models import Task, Note

DATA_DIR = Path.home() / ".pocketsage"
TASKS = DATA_DIR / "tasks.json"
NOTES = DATA_DIR / "notes.json"

class JSONStore:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        for p in [TASKS, NOTES]:
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_text("[]", encoding="utf-8")

    @staticmethod
    def default() -> "JSONStore":
        return JSONStore(DATA_DIR)

    def _load(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def _save(self, path: Path, data):
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # Tasks
    def add_task(self, t: Task) -> Task:
        data = self._load(TASKS)
        data.append(t.__dict__)
        self._save(TASKS, data)
        return t

    def list_tasks(self) -> List[Task]:
        return [Task(**d) for d in self._load(TASKS)]

    def search_tasks(self, q: str) -> List[Task]:
        ql = q.lower()
        return [t for t in self.list_tasks() if ql in t.title.lower()]

    def mark_done(self, tid: str) -> None:
        data = self._load(TASKS)
        for d in data:
            if d["id"] == tid:
                d["status"] = "done"
        self._save(TASKS, data)
```

**Next steps:**

* Add `pyproject.toml`, tests, and upgrade DAL to SQLite in Week 2.
* Keep CLI grammar simple; iterate after tests are stable.

---

## 13) Risk & scope cut lines

* If time tight → **skip Neo4j**; keep SQLite + link table
* Keep agent rule‑based (deterministic) to avoid API costs/keys
* Focus on test coverage + demo clarity over extra features

---

## 14) Future work (beyond class)

* Natural‑language query parser (`ask`)
* Email/Calendar integration for due dates
* Embedding‑based semantic search (local models)
