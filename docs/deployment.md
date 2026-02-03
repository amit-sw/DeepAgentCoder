# Deployment Guide

This project is a teaching series for building a coding agent with DeepAgents.
Each app runs locally from the CLI. Use this guide to configure API keys and
run the apps safely.

## Prerequisites
- Python 3.10+
- A model provider account (OpenAI, Anthropic, Groq, etc.)

## Environment Variables
Set keys in a local `.env` file (see `.env.example`). The apps load `.env`
automatically when they start.

Common options:
- `OPENAI_API_KEY` for OpenAI
- `ANTHROPIC_API_KEY` for Anthropic
- `GROQ_API_KEY` for Groq
- `DEEPAGENT_MODEL` model identifier passed to LangChain

Example:
```
OPENAI_API_KEY="your-key-here"
DEEPAGENT_MODEL="openai:gpt-4.1-mini"
```

## Running
From the repo root:
```
python apps/app_01_minimal/main.py
python apps/app_02_tools_fs/main.py
python apps/app_03_tests/main.py
python apps/app_04_final_cli/main.py
```

## Safety
- The agent is configured to work only inside the current directory.
- The test tool only allows pytest commands by default.

## Tips
- If you use a different model provider, set the matching API key and update
  `DEEPAGENT_MODEL` accordingly.
- Use a dedicated project folder when experimenting with file changes.
