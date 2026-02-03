from __future__ import annotations

from typing import List

from .agent_factory import build_agent
from .config import AgentConfig
from .schemas import TaskRequest, TaskResult


class AgentOrchestrator:
    """Orchestrates a single DeepAgents run for the teaching series."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.agent = build_agent(config)

    def run_task(self, request: TaskRequest) -> TaskResult:
        steps: List[str] = ["Received task", f"Prompt: {request.prompt}"]
        if request.context:
            steps.append("Context provided")

        messages = [{"role": "user", "content": request.prompt}]
        if request.context:
            messages.insert(0, {"role": "system", "content": request.context})

        result = self.agent.invoke({"messages": messages})
        final_message = result["messages"][-1]
        answer = getattr(final_message, "content", str(final_message))
        return TaskResult(answer=answer, steps=steps)
