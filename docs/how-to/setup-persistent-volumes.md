# How to Set Up Custom Persistent Volumes

The primary strength of the Flashbox sandbox is its dynamic volume mounting. When AI agents execute code on their local host, it's often hard to confine their changes to the sandbox while simultaneously allowing their code modifications to reflect permanently in your repository.

Flashbox uses Docker Volumes to map your native codebase into the container's isolated Linux file system automatically.

## Understanding the Default `/vault` Integration

By default, any time you run `sandbox start` or `sandbox exec`, the `DockerManager` detects your `Current Working Directory` and executes the following underlying Docker volume mount:
```bash
-v /absolute/path/to/cwd:/vault
```

The container sees your code completely transparently at `/vault`. If it creates a file named `/vault/test_artifact.py`, you will instantly see `test_artifact.py` natively on your macOS drive. However, if the agent runs `apt-get install malicious-software`, it installs into the isolated Debian root OS memory, leaving your macOS system pristine.

## Managing Dependency Clashes (Node.js/Python)

### The Problem
If you instruct an agent to run `npm install` inside the sandbox, the `node_modules` folder generated *will* appear on your host because the folder is mapped explicitly to `/vault`. Often, Linux-compiled binaries inside `node_modules` or `.venv` will clash with your macOS host when you switch back.

### The Solution: Targeted `.dockerignore` Overrides
Currently, Flashbox maps the entire CWD. If you want to instruct your AI to download massive libraries but *don't* want them syncing back to your raw macOS repo, configure your `.gitignore` so your host repository ignores the locally synced `.venv` or `node_modules` folders. 

## Rebuilding the Mount
To reset the volume mapping if things become corrupt or out of sync:
1. Delete the hidden host caching directory (e.g. `rm -rf node_modules`).
2. Type `sandbox remove`.
3. Type `sandbox start` and have your agent rebuild the dependencies cleanly into the empty host wrapper.
