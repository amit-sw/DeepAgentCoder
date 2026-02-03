from __future__ import annotations

from typing import Optional

from deepagents import create_deep_agent

from .config import AgentConfig, Stage
from .tools.test_runner import make_run_tests_tool


def resolve_model(model: Optional[str]):
    if not model:
        return None
    from langchain.chat_models import init_chat_model

    return init_chat_model(model)


def build_agent(config: AgentConfig):
    model = resolve_model(config.model) if config.model else None
    if model is None and config.model:
        model = config.model

    backend = None
    additional_tools = None

    if config.stage in {Stage.TOOLS_FS, Stage.TESTS, Stage.FINAL}:
        from deepagents.backends import FilesystemBackend

        backend = FilesystemBackend(root_dir=str(config.root_dir), virtual_mode=True)

    if config.test_command:
        additional_tools = [
            make_run_tests_tool(
                root_dir=config.root_dir,
                default_command=config.test_command,
                allow_any_command=config.allow_any_test_command,
            )
        ]

    return create_deep_agent(
        model=model,
        system_prompt=config.system_prompt,
        tools=additional_tools,
        backend=backend,
    )
