# CLI Reference

## file_organizer.py

Sorts files in a directory into subdirectories based on file extension.

```
python scripts/file_organizer.py <directory> [options]
```

| Argument / Flag | Type | Required | Description |
|-----------------|------|----------|-------------|
| `directory` | positional | Yes | Path to the directory to organize |
| `--dry-run` | flag | No | Preview changes without moving files |
| `--recursive` | flag | No | Process subdirectories recursively |
| `--config` | string | No | Path to custom extension-to-category mapping (JSON) |

**Extension categories:** `images` (jpg, png, gif, svg), `pdf`, `documents` (doc, docx, txt), `csv`, `audio` (mp3, wav), `video` (mp4, avi), `misc` (everything else).

## csv_report.py

Reads a CSV file, computes summary statistics, and writes a JSON report.

```
python scripts/csv_report.py <input_csv> [options]
```

| Argument / Flag | Type | Required | Description |
|-----------------|------|----------|-------------|
| `input_csv` | positional | Yes | Path to the input CSV file |
| `--output` | string | No | Output file path (default: stdout) |
| `--group-by` | string | No | Column name to group aggregations by |
| `--sum` | string | No | Column to sum (default: `amount`) |

**Output format:**
```json
{ "total_rows": 100, "total_amount": 5200, "by_category": { "food": 2000, "transport": 3200 } }
```

## backup_script.py

Creates a timestamped zip backup of a source directory.

```
python scripts/backup_script.py <source> [options]
```

| Argument / Flag | Type | Required | Description |
|-----------------|------|----------|-------------|
| `source` | positional | Yes | Directory to back up |
| `--dest` | string | No | Destination for the archive (default: `./backups`) |
| `--exclude` | string | No | Comma-separated patterns to exclude (default: `.git,__pycache__,node_modules`) |
| `--max-backups` | int | No | Keep only the N most recent backups (default: 10) |

## log_analyzer.py

Parses structured log files and outputs error summaries.

```
python scripts/log_analyzer.py <logfile> [options]
```

| Argument / Flag | Type | Required | Description |
|-----------------|------|----------|-------------|
| `logfile` | positional | Yes | Path to the log file |
| `--level` | string | No | Filter to specific level (`ERROR`, `WARNING`, etc.) |
| `--top` | int | No | Number of top error messages to show (default: 5) |
| `--format` | string | No | Output format: `json` (default) or `table` |

**Output format:**
```json
{ "total_lines": 500, "errors": 23, "warnings": 45, "top_errors": [{ "message": "Connection timeout", "count": 12 }] }
```
