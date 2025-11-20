from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Task:
    id: int
    description: str
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "description": self.description, "completed": self.completed}

    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> "Task":
        try:
            tid = int(obj["id"])
            desc = str(obj["description"]).strip()
            completed = bool(obj.get("completed", False))
        except Exception as e:
            raise ValueError(f"Invalid task object: {e}")
        if not desc:
            raise ValueError("Task description must be non-empty")
        return Task(id=tid, description=desc, completed=completed)
