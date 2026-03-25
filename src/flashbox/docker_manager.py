import os
import re
import subprocess
import sys

IMAGE_NAME = "python:3.11-slim"


class DockerManager:
    def __init__(self, cwd=None):
        self.cwd = cwd or os.getcwd()
        self.container_name = self._generate_container_name(self.cwd)
        self.vault_path = self.cwd

    def _generate_container_name(self, path):
        """Generates a safe, unique Docker container name based on the current directory."""
        basename = os.path.basename(path).lower()
        # Remove any invalid docker characters
        safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "", basename)
        return f"flashbox-{safe_name}"

    def _run_cmd(self, cmd, check=True):
        """Executes a shell command and returns the stdout."""
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if check and result.returncode != 0:
            print(f"Error executing: {cmd}\n{result.stderr}", file=sys.stderr)
            sys.exit(result.returncode)
        return result.stdout.strip()

    def is_running(self):
        """Checks if this specific project container is currently running."""
        out = self._run_cmd(f"docker ps -q -f name={self.container_name}", check=False)
        return bool(out)

    def start(self):
        """Initializes the persistent container and mounts the local repo to /vault."""
        from rich.console import Console

        console = Console()

        if self.is_running():
            console.print(
                f"[yellow]Flashbox '{self.container_name}' is already running for this directory.[/yellow]"
            )
            return

        # Check if container exists but is stopped
        out = self._run_cmd(f"docker ps -aq -f name={self.container_name}", check=False)
        if out:
            console.print(f"[cyan]Starting existing Flashbox '{self.container_name}'...[/cyan]")
            self._run_cmd(f"docker start {self.container_name}")
        else:
            console.print(
                f"[green]Creating and starting new Flashbox '{self.container_name}'...[/green]"
            )
            # We mount the local directory to /vault inside the container
            self._run_cmd(
                f"docker run -d --name {self.container_name} -v {self.vault_path}:/vault -w /vault {IMAGE_NAME} tail -f /dev/null"
            )

            console.print("[cyan]Installing base AI tools (git, ripgrep, jq, curl)...[/cyan]")
            self._run_cmd(f"docker exec {self.container_name} apt-get update")
            self._run_cmd(
                f"docker exec {self.container_name} apt-get install -y git ripgrep jq curl"
            )
            console.print(
                "[bold green]Flashbox initialized successfully and mounted to /vault.[/bold green]"
            )

    def stop(self):
        """Stops the active container."""
        from rich.console import Console

        console = Console()
        if not self.is_running():
            console.print(f"[yellow]Flashbox '{self.container_name}' is not running.[/yellow]")
            return
        console.print(f"[cyan]Stopping Flashbox '{self.container_name}'...[/cyan]")
        self._run_cmd(f"docker stop {self.container_name}")

    def remove(self):
        """Destroys the container. Useful for a clean slate."""
        from rich.console import Console

        console = Console()
        console.print(f"[red]Destroying Flashbox '{self.container_name}'...[/red]")
        self._run_cmd(f"docker rm -f {self.container_name}", check=False)
        console.print("[bold green]Environment wiped successfully.[/bold green]")

    def exec_command(self, command_string):
        """Executes a raw bash command securely inside the sandbox."""
        if not self.is_running():
            self.start()

        # We pass the execution directly to Docker bypassing capture_output so interactive streams work
        result = subprocess.run(
            ["docker", "exec", "-w", "/vault", self.container_name, "bash", "-c", command_string]
        )
        sys.exit(result.returncode)
