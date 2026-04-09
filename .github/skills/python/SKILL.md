---
name: python
description: Python scripting — argparse, error handling, idempotency, type hints, and clean exit codes.
argument-hint: "[script-purpose] [inputs]"
user-invocable: true
disable-model-invocation: false
---

# Python Scripting (Elite)

## When to use

- Writing Python scripts for automation, data processing, or tooling.
- CLI tools and repo utilities.

## Procedure

### 1. Script skeleton

```python
#!/usr/bin/env python3
"""Script description.

Usage:
    python script.py --input <path> --output <path>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main(args: argparse.Namespace) -> int:
    # implementation
    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args()))
```

### 2. Error handling

```python
try:
    result = do_work()
except FileNotFoundError as exc:
    print(f"ERROR: {exc}", file=sys.stderr)
    sys.exit(1)
```

- Use specific exception types; avoid bare `except:`.
- Always exit with non-zero code on failure.
- Write errors to `stderr`; data to `stdout`.

### 3. Idempotency

- Check preconditions before writing files or modifying state.
- Use `if path.exists(): ...` before creating.
- Prefer `pathlib.Path` over `os.path`.

### 4. Type hints

```python
def process(items: list[str]) -> dict[str, int]:
    ...
```

- Add type hints to all function signatures.
- Run `mypy` or `ruff check --select ANN` to enforce.

## Self-check

- [ ] `argparse` (or `click`) used for all inputs; no `sys.argv` parsing.
- [ ] Usage documented in module docstring or `--help`.
- [ ] Errors written to `stderr`; non-zero exit on failure.
- [ ] Script is idempotent (safe to run multiple times).
- [ ] Type hints on all function signatures.
- [ ] `ruff check` passes with no errors.

## Outputs

- Script skeleton with argparse.
- Error handling patterns.
- Usage examples.
