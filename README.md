# AI Coding Harness

A coding harness built from scratch to understand how LLM-powered coding agents work internally.

This is not an agent — the intelligence comes from the LLM. The harness is everything around it. Instead of using an agent framework, this project implements that scaffolding manually: from LLM tool calling to tool execution, context management, error handling, and evaluation.

## Harness vs Agent

The "agent" in an AI coding agent is mostly the LLM deciding what to do next. Everything that makes those decisions actually work is the harness:

- The **LLM** provides the reasoning — it decides which tool to call and with what arguments.
- The **harness** provides everything else — the loop, tool definitions, the tool registry, tool execution, context assembly, safety guards, and evaluation.

The harness doesn't think. It takes the LLM's tool calls, executes them safely, feeds the results back into the context, and lets the LLM continue until the task is done. That loop is what makes an LLM behave like an agent — and it is exactly what this project builds by hand.

## Architecture

The harness runs the loop between the user and the LLM:

```text
User
  ↓
Harness (agent loop)
  ↓
LLM Provider
  ↓
LLM
  ↓
Tool Call
  ↓
Tool Registry
  ↓
Tool Execution
  ↓
Tool Result
  ↓
Context
  ↓
LLM
  ↓
Final Response
```

## Features

- Agent loop driven by the LLM
- Manual function calling
- Tool abstraction and registry
- File system operations
- Shell command execution
- Type-safe tool arguments
- Context management
- Error handling and recovery
- Workspace path protection
- Tool output limits
- Execution tracing
- LLM provider abstraction
- Basic agent evaluation

## Available Tools

| Tool           | Purpose                         |
| -------------- | ------------------------------- |
| `list_files`   | List files and directories      |
| `read_file`    | Read a file                     |
| `write_file`   | Create or overwrite a file      |
| `edit_file`    | Replace specific text in a file |
| `search_files` | Search for text across files    |
| `run_command`  | Execute development commands    |

## Project Structure

```text
agent-learning/
├── notebooks/
│   └── learning.ipynb
│
├── src/
│   └── agent_learning/
│       ├── __init__.py
│       ├── agent.py
│       ├── config.py
│       ├── context.py
│       ├── evaluator.py
│       ├── main.py
│       ├── provider.py
│       ├── registry.py
│       ├── tool.py
│       │
│       ├── providers/
│       │   ├── __init__.py
│       │   └── gemini.py
│       │
│       └── tools/
│           ├── __init__.py
│           ├── filesystem.py
│           └── shell.py
│
├── tests/
│   ├── __init__.py
│   └── eval_cases.py
│
├── scripts/
│   ├── __init__.py
│   └── run_evals.py
│
├── workspace/
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

## Run

Start the coding harness:

```bash
uv run python -m agent_learning.main
```

Example task:

```text
Create hello.py containing print("Hello World") and run it.
```

Inside the loop, the model can inspect the workspace, modify files, execute commands, observe the results, and continue reasoning until the task is complete.

## Evaluation

Run a specific evaluation:

```bash
uv run python -m scripts.run_evals --case create_python_file
```

Run all evaluations:

```bash
uv run python -m scripts.run_evals
```

Evaluations verify the actual workspace state instead of relying on the model's final response.

## Learning Goal

This project is primarily a from-scratch learning implementation.

The accompanying notebook documents the progression from:

```text
LLM
 ↓
Function Calling
 ↓
Tool Execution
 ↓
Agent Loop
 ↓
Tool Abstraction
 ↓
Context Management
 ↓
Coding Agent
 ↓
Safety & Evaluation
 ↓
Provider Abstraction
```

The goal is to understand what actually happens inside an AI coding agent — the harness, not just the model — rather than treating an agent framework as a black box.

## Safety

The current implementation includes basic safety mechanisms:

- File operations are restricted to the workspace
- Path traversal is prevented
- Shell commands use an allowlist
- Commands have execution timeouts
- Tool outputs are size-limited
- Tool arguments are validated

This is not a production-grade sandbox. Strong process isolation and sandboxing are future improvements.

## Tech Stack

- Python
- Google Gemini API
- Google GenAI SDK
- uv
- python-dotenv

## Status

Core harness functionality is implemented.

Future improvements may include:

- Stronger sandboxing
- Better context management
- Persistent sessions
- More comprehensive evaluations
- Additional LLM providers
- Parallel tool execution
- MCP integration
