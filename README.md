# Flashbox

[![PyPI version](https://badge.fury.io/py/flashbox.svg)](https://pypi.org/project/flashbox/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Flashbox** is an open-source, ultra-fast CLI designed to replace latency-heavy Model Context Protocol (MCP) servers when providing AI Coding Agents with safe, persistent Docker execution environments. (like Antigravity or Cursor) to safely execute terminal commands, run scripts, and compile code in an isolated Linux environment without polluting your local macOS host. It completely replaces the heavy, latency-prone Boxlite MCP server with a streamlined local Python CLI mapping directly to your Docker daemon.

## Why Flashbox?
- **Zero Token Overhead:** Unlike MCP servers, Flashbox doesn't inject massive JSON schemas into your prompt context.
- **Dynamic Repository Mounting:** If you run `sandbox start` in `/Projects/MyCoolApp`, Flashbox dynamically mounts that specific directory to `/vault` inside a dedicated `flashbox-mycoolapp` container.
- **Native Execution Speed:** Bypasses JSON-RPC handshakes. `sandbox exec` streams natively through `subprocess` directly to Docker.
- **Built-in Telemetry:** Ships with a real-time TUI to monitor the active exact CPU and RAM your AI is drawing.

## System Requirements
- **Operating System:** Fully cross-platform. Tested heavily on **macOS (Apple Silicon)**, but works flawlessly on **Linux** and **Windows (via WSL2)**.
- **Docker Daemon:** You **MUST** have the Docker engine running in the background. On macOS/Windows, this means having **Docker Desktop** or **OrbStack** open and active. On Linux, the native `docker` service must be running.
- **Python:** Python 3.10+ installed on the host machine.

## Installation

Because Flashbox is officially published, you can install it globally via `pipx` (recommended) or your preferred Python package manager:

```zsh
pipx install flashbox
```

## AI Agent Integration

For Cursor, Antigravity, or other AI frameworks to autonomously build and use your sandboxes without MCP overhead, they need an instructional "Prompt" or "Skill" file.

We have bundled the official agent prompt in this repository under `agent-skill/SKILL.md`. 

To natively integrate Flashbox into your AI Agent, simply copy this file into your agent's skills directory:
```bash
mkdir -p ~/.agents/skills/persistent_sandbox
cp agent-skill/SKILL.md ~/.agents/skills/persistent_sandbox/SKILL.md
```
Your AI Agents will now immediately understand how to use `sandbox exec`, `sandbox monitor`, and orchestrate your isolated environments autonomously!

## Usage

Once installed, the globally accessible `sandbox` command is available from any directory.

### Quick Start
Navigate to any project directory and initialize the sandbox:
```zsh
cd /Users/markeyser/Projects/MyCoolApp
sandbox start
```
*This instantly spins up a `python:3.11-slim` container uniquely named `flashbox-mycoolapp` and installs base tools (`git`, `rg`, `jq`, `curl`).*

### AI Execution
Instruct your AI agent to execute commands using the `exec` flag. The agent's native system terminal will push the command securely into the container:
```bash
sandbox exec "python3 main.py"
sandbox exec "grep -r 'TODO' ."
```

### Telemetry Dashboard
Launch the TUI to monitor the AI's impact on your system resources and disk space in real-time:
```zsh
sandbox monitor
```

### Clean Slate
If the AI corrupts the environment or installs too many dependencies, instantly wipe the infrastructure (your code on the native host remains untouched):
```zsh
sandbox remove
sandbox start
```
