from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TaskRequest:
    prompt: str
    context: Optional[str] = None


@dataclass
class TaskResult:
    answer: str
    steps: List[str]
