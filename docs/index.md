# Flashbox Documentation

## The Flashbox Value Proposition

Flashbox was engineered to solve two critical bottlenecks in modern AI Agent frameworks:

### 1. Persistent Sandboxing Saves Time and Tokens (Money)
Most Agent tools spin up **ephemeral** containers that die when the chat session ends. Every new conversation requires the Agent to spend minutes (and thousands of API tokens) re-downloading `node_modules`, `pip` dependencies, or rebuilding code. 

**Flashbox is persistent.** The container lifecycle maps directly to your local project folder and survives agent restarts. This drastically reduces LLM API costs by instantly granting the agent access to previously compiled environments.

### 2. CLI + Skill.md is Superior to MCP Servers
Model Context Protocol (MCP) servers are powerful, but they constantly inject heavy JSON-RPC schema definitions into the context window on every single turn, bottlenecking latency and increasing token consumption.

Flashbox uses a radically simplified architectural approach: a globally accessible Python CLI paired with a simple agent instruction prompt (`SKILL.md`). This guarantees **zero hidden schema overhead**, total architectural transparency, and vastly superior script execution mapping. It replaces latency-prone MCP servers with native Docker system telemetry.

## Structure of this Documentation

If you are new to the Diátaxis framework, you'll find our documentation cleanly separated by its purpose:

*   **[Tutorials](tutorials/getting-started.md)**: A step-by-step learning guide teaching you how to install Flashbox and instruct an AI to use it.
*   **[How-to Guides](how-to/setup-persistent-volumes.md)**: Directions addressing specific problems, like securely mapping your repository code or tuning performance limits.
*   **[Reference](reference/cli-commands.md)**: Accurate technical descriptions and lookup tables detailing the CLI flags, system dependencies, and telemetry components.
*   **[Explanation](explanation/architecture.md)**: Broad conceptual discussions about the shift from BoxLite MCP to Flashbox CLI and why dynamic namespace routing makes your AI faster.

Enjoy building safely!
