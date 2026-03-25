import argparse

from flashbox.docker_manager import DockerManager
from flashbox.monitor import FlashboxMonitor


def main():
    parser = argparse.ArgumentParser(
        description="Flashbox: A dynamic, repository-aware persistent Docker sandbox CLI for AI Agents."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    subparsers.add_parser(
        "start", help="Initialize and start the Flashbox for the current directory"
    )
    subparsers.add_parser("stop", help="Stop the active Flashbox")
    subparsers.add_parser("remove", help="Destroy the Flashbox. Good for a clean slate rebuild.")

    # Monitor command parser
    monitor_parser = subparsers.add_parser(
        "monitor", help="Launch the real-time telemetry dashboard"
    )
    monitor_parser.add_argument(
        "-r", "--refresh", type=float, default=1.0, help="Refresh rate in seconds"
    )

    # Exec command parser
    exec_parser = subparsers.add_parser(
        "exec", help="Execute a raw bash command securely inside the sandbox"
    )
    exec_parser.add_argument("command", nargs="+", help="The command string to run")

    args = parser.parse_args()

    # Initialize the docker manager which dynamically detects the CWD
    manager = DockerManager()

    if args.action == "start":
        manager.start()
    elif args.action == "stop":
        manager.stop()
    elif args.action == "remove":
        manager.remove()
    elif args.action == "monitor":
        monitor = FlashboxMonitor(manager)
        monitor.run(args.refresh)
    elif args.action == "exec":
        # Join the command pieces back together preserving spaces
        manager.exec_command(" ".join(args.command))


if __name__ == "__main__":
    main()
