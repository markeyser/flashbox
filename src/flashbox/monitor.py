import os
import json
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
import subprocess

console = Console()

class FlashboxMonitor:
    def __init__(self, manager):
        self.manager = manager
        self.cooldown = 30 # seconds to determine "Idle" vs "Active"
        self.last_active_time = 0
        self.total_size = 0
        self.total_files = 0
        
    def _get_docker_stats(self):
        """Fetches real-time CPU and RAM limits from docker stats."""
        if not self.manager.is_running():
            return "N/A", "N/A"
        try:
            # We use no-stream to get a single snapshot of the active container
            out = self.manager._run_cmd(
                f"docker stats --no-stream --format '{{{{.CPUPerc}}}}|{{{{.MemUsage}}}}' {self.manager.container_name}", 
                check=False
            )
            if out and "|" in out:
                cpu, mem = out.split("|")
                return cpu.strip(), mem.strip()
            return "0.00%", "0B / 0B"
        except Exception:
            return "Error", "Error"

    def _get_sandbox_size(self):
        """Scans the volume mount directory specifically for its size."""
        total_size = 0
        total_files = 0
        
        for dirpath, _, filenames in os.walk(self.manager.cwd):
            if '.git' in dirpath or '.venv' in dirpath:
                continue
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    try:
                        total_size += os.path.getsize(fp)
                        total_files += 1
                        # Check modification time
                        mtime = os.path.getmtime(fp)
                        if time.time() - mtime < self.cooldown:
                            self.last_active_time = time.time()
                    except (OSError, FileNotFoundError):
                        pass
                        
        self.total_size = total_size
        self.total_files = total_files

    def _format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def generate_dashboard(self) -> Layout:
        self._get_sandbox_size()
        cpu, mem = self._get_docker_stats()
        
        is_active = (time.time() - self.last_active_time) < self.cooldown
        status_color = "green" if is_active else "yellow"
        status_text = "🟢 ACTIVE" if is_active else "🟡 IDLE"

        # Build Metrics Table
        metrics_table = Table(show_header=False, expand=True, box=None)
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", justify="right")
        
        metrics_table.add_row("Dynamic Container", self.manager.container_name)
        metrics_table.add_row("Agent State", f"[{status_color}]{status_text}[/{status_color}]")
        metrics_table.add_row("Mounted Vault Files", str(self.total_files))
        metrics_table.add_row("Vault Source Vol.", self._format_size(self.total_size))
        metrics_table.add_row("Container CPU", cpu)
        metrics_table.add_row("Container RAM", mem)

        panel = Panel(
            Align.center(metrics_table, vertical="middle"),
            title=f"[b blue]Flashbox Telemetry[/b blue]",
            border_style="blue",
        )
        return panel

    def run(self, refresh_rate=1.0):
        if not self.manager.is_running():
            console.print(f"[red]Flashbox '{self.manager.container_name}' is not currently running.[/red]")
            console.print("Start it first with: [cyan]sandbox start[/cyan]")
            return

        console.clear()
        try:
            with Live(self.generate_dashboard(), console=console, screen=True, refresh_per_second=1/refresh_rate) as live:
                while True:
                    time.sleep(refresh_rate)
                    live.update(self.generate_dashboard())
        except KeyboardInterrupt:
            console.print("\n[dim]Monitor stopped.[/dim]")
