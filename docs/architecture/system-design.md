# Architecture

## Overview

Python Automation Scripts is a collection of standalone CLI utilities for common file management, data processing, and system administration tasks. Each script is self-contained with shared utility modules for configuration, logging, and argument parsing.

## Project Structure

```
scripts/
  file_organizer.py     # Sort files by extension into categorized folders
  csv_report.py         # Parse CSV files and generate summary reports
  backup_script.py      # Create timestamped zip archives
  log_analyzer.py       # Parse and summarize log files
  utils/
    config.py           # Load JSON/YAML configuration files
    logger.py           # Structured logging setup (JSON to stdout)
    cli.py              # Shared argparse helpers and validators
    fs.py               # Safe file operations (atomic moves, temp dirs)
tests/
  python/               # Pytest unit tests for each script module
  integration/          # E2E tests that invoke scripts as subprocesses
  unit/                 # JS-bridged tests for CI pipeline
```

## Design Principles

1. **Single responsibility** -- each script does one thing well and exposes composable functions for its core logic so they can be unit-tested independently.
2. **Idempotent operations** -- running a script twice produces the same result. The file organizer skips already-categorized files; the backup script avoids re-archiving unchanged content.
3. **Dry-run support** -- all scripts that modify the filesystem accept a `--dry-run` flag that logs intended operations without executing them.
4. **Structured output** -- scripts default to JSON output for machine consumption. A `--format table` flag provides human-readable output.

## Error Handling

All scripts use a common error hierarchy defined in `utils/errors.py`:
- `FileNotFoundError` -- input path does not exist
- `PermissionError` -- insufficient filesystem permissions
- `ParseError` -- malformed input data (bad CSV, unparseable log lines)

Errors are logged with full context (file path, line number) and scripts exit with non-zero codes.

## Configuration

Scripts read defaults from `config/defaults.json` and accept CLI overrides. Environment variables prefixed with `PYAUTO_` override config file values (e.g., `PYAUTO_BACKUP_DEST`).

## Testing Strategy

| Layer | Tool | Description |
|-------|------|-------------|
| Unit | pytest | Test individual functions (categorize_extension, parse_log_line, etc.) |
| Integration | Node.js child_process | Invoke full scripts against temp directories and verify filesystem state |
| Linting | flake8 + black | Code style enforcement on pre-commit |

## Dependencies

- Python 3.9+
- Standard library only for core functionality (os, csv, zipfile, json, re, argparse)
- Optional: `pyyaml` for YAML config support, `rich` for colored table output
