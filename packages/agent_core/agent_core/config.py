from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class Stage(str, Enum):
    MINIMAL = "minimal"
    TOOLS_FS = "tools_fs"
    TESTS = "tests"
    FINAL = "final"


@dataclass
class AgentConfig:
    stage: Stage
    model: Optional[str]
    root_dir: Path
    system_prompt: str
    test_command: Optional[str] = None
    allow_any_test_command: bool = False


DEFAULT_TEST_COMMAND = "pytest"


def default_config(stage: Stage, root_dir: Path, model: Optional[str]) -> AgentConfig:
    from .prompts import PROMPT_FINAL, PROMPT_MINIMAL, PROMPT_TESTS, PROMPT_TOOLS_FS

    if stage == Stage.MINIMAL:
        prompt = PROMPT_MINIMAL
        return AgentConfig(stage=stage, model=model, root_dir=root_dir, system_prompt=prompt)

    if stage == Stage.TOOLS_FS:
        prompt = PROMPT_TOOLS_FS
        return AgentConfig(stage=stage, model=model, root_dir=root_dir, system_prompt=prompt)

    if stage == Stage.TESTS:
        prompt = PROMPT_TESTS
        return AgentConfig(
            stage=stage,
            model=model,
            root_dir=root_dir,
            system_prompt=prompt,
            test_command=DEFAULT_TEST_COMMAND,
        )

    prompt = PROMPT_FINAL
    return AgentConfig(
        stage=stage,
        model=model,
        root_dir=root_dir,
        system_prompt=prompt,
        test_command=DEFAULT_TEST_COMMAND,
    )
