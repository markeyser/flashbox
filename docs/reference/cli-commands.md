# Reference: Flashbox CLI Commands

This reference page outlines the definitive API specifications and behavioral limits of the active `sandbox` terminal commands, leveraging the `DockerManager` and `FlashboxMonitor` python classes.

## Commands Reference

The Flashbox CLI is driven by the global command `sandbox`, followed by specialized actions mapping explicitly to the dynamic directory structure (CWD).

---

### `sandbox start`
**Description:** Initializes the Docker container if absent or boots it if stopped. Automates the installation of base telemetry (git, ripgrep, jq, curl).
- **Parameters:** None.
- **Behind the Scenes:** Generates a sanitized container name derived directly from your Active Directory (e.g. `/my_app` triggers `flashbox-my_app`), then executes `docker run -v $(pwd):/vault`.

---

### `sandbox exec <"command_string">`
**Description:** Streams standard input commands securely directly to the interior bash terminal of the container without relying on MCP RPC endpoints. Evaluates dynamically if the container needs to be started.
- **Parameters:** `command` - Explicit string or unquoted bash command arguments.
- **Behavior:** Bypasses `ssh` to stream instructions raw:
```bash
sandbox exec "echo 'Hello World'"
sandbox exec python3 test.py
```

---

### `sandbox monitor`
**Description:** Launches the `FlashboxMonitor` TUI system. Renders real-time native telemetry tracking CPU and RAM limits natively polled via `docker stats --no-stream`.
- **Flags:**
    - `-r`, `--refresh`: Float. Set the cycle frequency in seconds (Default: `1.0`).
- **Example:**
```bash
sandbox monitor -r 0.5
```

---

### `sandbox stop`
**Description:** Pauses the container's execution loop without destroying the internal file structures or database limits.
- **Parameters:** None.

---

### `sandbox remove`
**Description:** Forces the Docker daemon to completely wipe and delete the `flashbox-*` container.
- **Tip:** Highly recommended if the AI breaks internal dependencies or the OS filesystem. It performs a clean state reset entirely.
