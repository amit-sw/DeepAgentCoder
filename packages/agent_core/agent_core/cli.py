from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import find_dotenv, load_dotenv

from .config import AgentConfig, Stage, default_config
from .orchestrator import AgentOrchestrator
from .schemas import TaskRequest
from .prompts import PROMPT_CLARIFY


def _capabilities_text(stage: Stage) -> str:
    if stage == Stage.MINIMAL:
        return (
            "Capabilities: explain approach and clarify requirements. "
            "This stage does not modify files."
        )
    if stage == Stage.TOOLS_FS:
        return (
            "Capabilities: create or edit files in the current directory. "
            "No tests in this stage."
        )
    if stage == Stage.TESTS:
        return (
            "Capabilities: create or edit files in the current directory, "
            "and run tests to fix failures."
        )
    return (
        "Capabilities: create or edit files in the current directory, "
        "and optionally run tests to fix failures."
    )


def run_interactive_cli(
    stage: Stage,
    model: Optional[str],
    test_command: Optional[str] = None,
    allow_any_test_command: bool = False,
    enable_tests: bool = True,
    loop: bool = False,
) -> None:
    load_dotenv(find_dotenv(usecwd=True))
    root_dir = Path.cwd().resolve()

    if model is None:
        model = os.getenv("DEEPAGENT_MODEL")

    if model is None or not str(model).strip():
        print("Error: No model configured. Set DEEPAGENT_MODEL in your environment.")
        raise SystemExit(1)

    print(_capabilities_text(stage))
    print("I only work inside the current directory:", root_dir)

    help_text = (
        "Slash commands:\n"
        "/help  Show this help message\n"
        "/quit  Exit the program"
    )

    while True:
        while True:
            user_prompt = input("What do you want to build?\n> ").strip()
            if not user_prompt:
                continue
            if user_prompt.lower() == "/help":
                print(help_text)
                continue
            if user_prompt.lower() == "/quit":
                print("Exiting.")
                return
            break

        clarifications = _collect_clarifications(user_prompt, model)

        config = default_config(stage=stage, root_dir=root_dir, model=model)
        if not enable_tests:
            config.test_command = None
        elif test_command:
            config.test_command = test_command
        config.allow_any_test_command = allow_any_test_command

        plan = (
            "Plan: analyze requirements, update files under the current directory, "
            "and summarize what changed."
        )
        if stage in {Stage.TESTS, Stage.FINAL} and config.test_command:
            plan = (
                "Plan: analyze requirements, update files under the current directory, "
                f"run tests with `{config.test_command}`, fix failures if any, "
                "and summarize what changed."
            )

        print(plan)

        context = (
            "You must only read/write files inside the current working directory. "
            "Summarize changes with a short bullet list of files touched."
        )
        combined_prompt = f"{user_prompt}\n\nClarifications:\n{clarifications}"

        orchestrator = AgentOrchestrator(config)
        result = orchestrator.run_task(
            TaskRequest(prompt=combined_prompt, context=context)
        )

        print("\n=== Agent Response ===")
        print(result.answer)

        if not loop:
            return


def _collect_clarifications(user_prompt: str, model: Optional[str]) -> str:
    clarifier_config = default_config(
        stage=Stage.MINIMAL, root_dir=Path.cwd().resolve(), model=model
    )
    clarifier_config.system_prompt = PROMPT_CLARIFY
    clarifier = AgentOrchestrator(clarifier_config)

    rounds = 0
    collected = ""
    prompt = user_prompt
    while rounds < 2:
        result = clarifier.run_task(TaskRequest(prompt=prompt, context=None))
        questions = result.answer.strip()
        if questions == "NO_QUESTIONS":
            return collected or "None."

        print("I need a couple clarifications:")
        print(questions)
        response = input("> ").strip()
        if response.lower() == "/help":
            print(
                "Slash commands:\n"
                "/help  Show this help message\n"
                "/quit  Exit the program"
            )
            continue
        if response.lower() == "/quit":
            print("Exiting.")
            raise SystemExit(0)

        collected = f"{collected}\nQuestions:\n{questions}\nAnswers:\n{response}".strip()
        prompt = f"{user_prompt}\n\nClarifications:\n{collected}"
        rounds += 1

    return collected or "None."
