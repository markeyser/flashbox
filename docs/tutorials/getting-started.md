# Getting Started with Flashbox

This tutorial will guide you through setting up Flashbox from scratch and performing your first AI-assisted isolated code execution.

If you complete all the lessons here, you will be able to hand off an entire development environment securely to an LLM without risking your host operating system.

## Prerequisites
Before beginning this tutorial, please ensure you have:
1. macOS (Tested on Apple Silicon).
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [OrbStack](https://orbstack.dev/) running in the background.
3. Python 3.10+ and `pipx` installed.

## 1. Installation

Flashbox is a fully open-source Python CLI published gracefully to PyPI. To configure it globally so your AI Agents can freely invoke it across any host directory, we recommend installing via `pipx`:

```bash
pipx install flashbox
```
Validate the installation by typing:
```bash
sandbox --help
```

## 2. AI Agent Integration (Crucial)

To actually allow your AI (Cursor, Antigravity, etc.) to use Flashbox autonomously without MCP, you must pass it our official instructional "Skill" prompt. 

We have bundled the prompt directly in the repository at `agent-skill/SKILL.md`.

Clone or download the repository, then copy that file into your system's global agent `skills` directory:
```bash
git clone https://github.com/markeyser/flashbox.git
mkdir -p ~/.agents/skills/persistent_sandbox
cp flashbox/agent-skill/SKILL.md ~/.agents/skills/persistent_sandbox/SKILL.md
```
*Note: Your agent may look for skills in `.agents/` inside your user directory or your specific project directory.*

## Step 2: Initialize a Sandbox
Navigate your terminal to any project folder you'd like your agent to be able to access. We'll use a hypothetical `MyAgentApp`.

```bash
cd ~/Projects/MyAgentApp
sandbox start
```
*What happens:* Flashbox instantly detects the folder `MyAgentApp`, translates it into a docker container named `flashbox-myagentapp`, starts a fresh Debian environment, and mounts your project's code structure natively through `/vault`. The entire boot sequence avoids the previous MCP JSON-RPC handshakes entirely!

## Step 3: Command the Agent
Instead of telling your AI "run this in your environment," you can now instruct them to prefix any bash pipeline with `sandbox exec`. 

Tell your coding agent:
> "Hey, can you try running `sandbox exec 'python3 my_script.py'` to test if my code works?"

The agent will execute the command safely within the Debian walls! 

## Step 4: Monitor Resources
While the AI processes large builds or runs node packages inside the sandbox, you can track its host overhead in real-time.

```bash
sandbox monitor
```
The terminal will transform into a rich dashboard analyzing the CPU and memory consumption.

## Step 5: Clean the Slate
Did your agent install a rogue dependency? No problem. Wipe the environment entirely without touching your real `MyAgentApp` code.

```bash
sandbox remove
```

Congratulations! You have completed the basic Flashbox tutorial. To learn more specialized behaviors, view the **[How-to Guides](../how-to/setup-persistent-volumes.md)**.
