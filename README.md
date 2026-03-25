# Flashbox ⚡️

A lightning-fast, repository-aware persistent Docker sandbox CLI designed specifically for AI Coding Agents.

Flashbox allows your AI coding agents (like Antigravity or Cursor) to safely execute terminal commands, run scripts, and compile code in an isolated Linux environment without polluting your local macOS host. It completely replaces the heavy, latency-prone Boxlite MCP server with a streamlined local Python CLI mapping directly to your Docker daemon.

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

Because Flashbox is packaged cleanly, you can install it globally via `pipx` or your preferred Python package manager:

```zsh
# Run this inside the cloned repo
pipx install .
```

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
