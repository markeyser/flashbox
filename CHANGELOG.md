# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2024-03-24

### Changed
- Injected `[project.urls]` directly into `pyproject.toml` to dynamically link the GitHub repository, open source issue tracker, and Zensical documentation pages to the PyPI sidebar interface.

## [0.1.0] - 2024-03-24

### Added
- Initial release of the `flashbox` package.
- Dynamic directory mounting mapping cleanly to the `sandbox start` command.
- Real-time `rich` based system telemetry using native `docker stats` via `sandbox monitor`.
- Seamless pipeline passing bash commands to containers without JSON-RPC handshakes via `sandbox exec`.
- The `sandbox stop` and `sandbox remove` cleanup lifecycle elements.
- Initial structural components replacing the deprecated BoxLite MCP server integration.
