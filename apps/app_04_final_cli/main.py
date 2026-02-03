import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "packages" / "agent_core"))

from agent_core import Stage, run_interactive_cli  # noqa: E402


def main() -> None:
    run_interactive_cli(stage=Stage.FINAL, model=None)


if __name__ == "__main__":
    main()
