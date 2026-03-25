# Explaining the Architecture

Flashbox fundamentally alters how your AI Coding Agent accesses the host machine. Instead of using complex MCP (Model Context Protocol) Server endpoints, it simplifies execution routing.

## The Problem: BoxLite MCP Payload Density
Before Flashbox, if an AI agent wanted to run a sandboxed bash command, it connected to an external **BoxLite MCP server**.
This caused severe context bloating: 
1. The AI agent had to read an injected massive JSON-RPC 2.0 schema defining all tool endpoints.
2. The agent formulated nested JSON string commands.
3. BoxLite parsed the payload, locked the filesystem, and piped the output context dynamically.
4. Total latency and context window burn skyrocketed on basic `git commit` requests.

## The Solution: Flashbox CLI Path Routing
Flashbox cuts out the server entirely. It utilizes your host OS natively.

When the agent wants to execute a command, it simply calls the `sandbox exec` CLI binary in its own environment.

### The DockerManager Bridge
Behind the scenes, the `DockerManager` python wrapper evaluates your actual system directory (`cwd`).
If your Host Path is `/Users/markeyser/Projects/My-App`, the sandbox immediately generates a clean string `flashbox-my_app`.

It explicitly checks the active daemon using `subprocess.run(["docker", "ps"])` to see if a Docker instance exists for that exact repository name. If false, it triggers `docker run -d -v /cwd:/vault` mapped symmetrically.

### Tying the Agent Context Locally
The AI no longer requires external server payloads. Natively executing `sandbox exec` returns standard input logs immediately without nested JSON encoding. The resource cost of running isolated environment queries drops near zero, and total latency is dictated purely by the binary container layer executing underlying queries.
