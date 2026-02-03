# DeepAgentCoder - Teaching Series

This repo is a staged series of small apps that teach how to build a coding agent using the DeepAgents library from LangChain.

## Structure
- `packages/agent_core/` Shared core logic used by all apps
- `apps/app_01_minimal/` Minimal CLI agent loop
- `apps/app_02_tools_fs/` CLI agent with tool registry + filesystem access
- `apps/app_03_tests/` CLI agent with test runner and retry loop
- `apps/app_04_final_cli/` Final CLI coding agent (full workflow)

## What Changes Across App Versions (User View)
App 01 (Minimal)
- You run a CLI agent that explains what it would do.
- It does not create or modify files.
- It asks clarifying questions and then responds with a plan.

App 02 (Tools + Filesystem)
- The agent can create or update files in the current directory.
- It still asks clarifying questions, then proceeds to edit files.
- No tests are run.

App 03 (Tests + Retry)
- Everything in App 02.
- The agent can run tests and fix failures based on test output.

App 04 (Final CLI)
- Everything in App 03.
- Full coding-agent workflow with clearer summaries of changes and outcomes.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add your model provider key to environment variables (example in `.env.example`).

## Quick Start
```bash
python apps/app_01_minimal/main.py
```

## Model Configuration
Provide a model identifier via the `DEEPAGENT_MODEL` environment variable.
Example:
```bash
DEEPAGENT_MODEL="openai:o3-mini" python apps/app_01_minimal/main.py
```

## Notes
- Python only. Final app is CLI-based.
- Each app imports shared logic from `packages/agent_core`.
