from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    name: str
    output: Any
    success: bool = True
    metadata: Dict[str, Any] | None = None


class Tool:
    name: str
    description: str

    def run(self, payload: Dict[str, Any]) -> ToolResult:
        raise NotImplementedError
