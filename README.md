# automation_reporter

A GitHub automation tool that monitors repositories for open issues and delegates resolution to AI agents (Claude, Codex, Gemini) in parallel.

## Overview

`automation_reporter` watches GitHub repositories for issues assigned to specific users (via `@mention` in the issue body), generates structured prompts, and dispatches them to AI coding agents to automatically solve issues and create pull requests.

## Features

- Monitors multiple GitHub repositories for open issues
- Routes issues to AI agents based on `@mention` in the issue body
- Supports multiple AI agents: **Claude**, **Codex**, **Gemini**
- Executes agents in parallel using async/await
- Automatically clones repositories locally for processing
- Generates structured prompts with issue context and PR instructions

## Project Structure

```
automation_reporter/
├── src/
│   ├── main.py                   # Entry point
│   ├── agent/
│   │   └── agent.py             # Agent definitions and initialization
│   ├── command/
│   │   └── run.py               # Async command execution
│   ├── environment/
│   │   └── agents.json          # Agent configuration
│   ├── gitmodule/
│   │   ├── gitagent.py          # GitHub API integration
│   │   └── repo_info.py         # Repository cloning and info
│   └── prompt/
│       └── make_prompt.py       # Prompt template generation
├── pyproject.toml
└── .env                         # GitHub credentials (not committed)
```

## Requirements

- Python >= 3.12
- GitHub personal access token
- AI agent CLIs installed (claude, codex, gemini)

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd automation_reporter
   ```

2. Install dependencies using [uv](https://github.com/astral-sh/uv):
   ```bash
   uv sync
   ```

3. Configure environment variables in `.env`:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   REPO_LIST=owner/repo1,owner/repo2
   ```

## Usage

Run the automation reporter:

```bash
uv run python src/main.py
```

The tool will:
1. Connect to GitHub using your token
2. Scan configured repositories for open issues
3. Find issues with `@agent-name` mentions in the body
4. Dispatch matching agents to resolve each issue in parallel
5. Each agent will attempt to solve the issue and create a pull request

## Issue Assignment

To assign an issue to an AI agent, include `@agent-name` in the issue body:

```
@claude
Please fix the bug in the authentication module.
```

Supported agents: `@claude`, `@codex`, `@gemini`

## Agent Configuration

Agents are defined in `src/environment/agents.json`:

```json
[
  { "name": "claude", "command": "claude", "path": "which claude" },
  { "name": "codex",  "command": "codex",  "path": "which codex" },
  { "name": "gemini", "command": "gemini", "path": "which gemini" }
]
```

## License

See [LICENSE](LICENSE) for details.
