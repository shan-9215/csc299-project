from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str
    tags: List[str]
    status: str  # "open" or "done"
    priority: str  # "low", "medium", or "high"
    due_date: Optional[str]  # store as ISO string
    created_at: str = datetime.now().isoformat()


@dataclass
class Note:
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: str = datetime.now().isoformat()
