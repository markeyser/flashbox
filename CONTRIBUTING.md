# Contributing to Flashbox

First off, thank you for considering contributing to Flashbox! It's people like you that make Flashbox such a great tool.

## Setup Local Environment

To set up your local development environment:
1. Clone the repository.
2. Install virtual environment tools (e.g. `python3 -m venv .venv`).
3. Activate the environment: `source .venv/bin/activate`.
4. Install all dependencies, including dev requirements: `pip install -e ".[dev]"`.

## Testing

Flashbox uses `pytest` for unit testing the logic paths within the DockerManager and TUI Monitor.
Run tests locally via:
```bash
pytest tests -v
```
All new features must include relevant tests within the `tests/` directory ensuring both standard path execution and edge cases (macOS permission/socket drops) are safely evaluated.

## Linting & Formatting

Flashbox strictly enforces styling via `ruff`. 
To automatically format and fix simple style errors, run:
```bash
ruff check . --fix
ruff format .
```
Please ensure `ruff` returns a pass before submitting any Pull Requests.

## Submitting Pull Requests
1. Fork the repo and create your branch from `main`.
2. Add tests for any new logic.
3. Update the documentation in `docs/` or `README.md` if you changed the CLI behavior.
4. Ensure the test suite passes locally on macOS or Linux.
