from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable

from langchain_core.tools import tool


def _safe_cwd(root_dir: Path, cwd: str) -> Path:
    if cwd.startswith("/"):
        cwd = cwd.lstrip("/")
    resolved = (root_dir / cwd).resolve()
    if root_dir not in resolved.parents and resolved != root_dir:
        raise ValueError(f"cwd must be inside {root_dir}")
    return resolved


def _allowed(command: str) -> bool:
    normalized = command.strip()
    return normalized.startswith("pytest") or normalized.startswith("python -m pytest")


def make_run_tests_tool(
    root_dir: Path,
    default_command: str,
    allow_any_command: bool,
) -> Callable:
    @tool
    def run_tests(command: str = default_command, cwd: str = ".") -> str:
        """Run tests from within the project directory.

        Use pytest by default. Returns stdout/stderr and exit code.
        """

        if not allow_any_command and not _allowed(command):
            return (
                "Refusing to run command. Allowed: pytest, python -m pytest. "
                "Provide one of those commands."
            )

        workdir = _safe_cwd(root_dir, cwd)
        proc = subprocess.run(
            command,
            cwd=str(workdir),
            shell=True,
            text=True,
            capture_output=True,
        )
        return (
            "exit_code: {code}\nstdout:\n{stdout}\nstderr:\n{stderr}".format(
                code=proc.returncode,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
            )
        )

    return run_tests
