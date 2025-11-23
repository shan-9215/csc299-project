
# PKMS + Task Manager (CSC299 Final Project)

## Overview
This is a terminal-based personal knowledge management (PKMS) and task manager system built in Python. It supports task creation, listing, and completion; note storage and viewing; search across tasks and notes; AI-powered task title suggestions and a daily plan generator; JSON-based persistent storage; and a chat-style command interface.

## Installation
1. Install `uv` (if not already installed)
2. Run `uv sync` in the project directory
3. Set the environment variable: `export OPENAI_API_KEY="your key"`
4. Run the program with:
	`uv run final`

## Commands
- `add-task` — create a new task (AI can suggest a short title)
- `list-tasks`
- `complete-task <id>`
- `add-note`
- `list-notes`
- `view-note <id>`
- `search <query>`
- `ai-plan` — generate an AI-based daily plan
- `reset-state` — clears all tasks and notes (with confirmation)
- `help`
- `quit`

## AI Features
- `summarize_description` generates concise (5–10 word) task titles from long descriptions.
- `generate_plan` reads open tasks and produces a short, ordered plan for what to do today. Both features use the OpenAI chat completions API to produce concise outputs.

## Project Structure
- `src/final/__init__.py` — REPL loop
- `src/final/commands.py` — command implementations
- `src/final/storage.py` — JSON read/write
- `src/final/ai_agent.py` — OpenAI integration
- `src/final/models.py` — task/note structures
- `tests/` — pytest suite

## Running Tests
`uv run pytest`

