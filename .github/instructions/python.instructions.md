---
name: "Python Defaults"
description: "Python guidance: readability, safety, robust CLI/script behavior."

## applyTo: "**/*.py"

# Python Defaults

## Code style

- Prefer clear, explicit code; avoid cleverness.

- Use type hints for all public functions and complex logic — `mypy --strict` is the target.

- Follow PEP 8; enforce with `ruff` or `flake8` in CI.

- Use `black` for formatting; never debate whitespace in reviews.

## Error handling

- Add specific error handling (`except ValueError` not bare `except`).

- Print actionable CLI messages: include what went wrong, what was expected, and what to try.

- Use `sys.exit(1)` on fatal errors; never silently swallow exceptions.

## Script & CLI conventions

- Keep scripts idempotent where possible (safe to rerun).

- Use `argparse` or `typer` for CLI interfaces; always include `--help`.

- Separate `__main__` guard from logic: `if __name__ == "__main__": main()`.

- Include a usage example in the module docstring.

## Project structure

- Prefer `src/` layout (`src/<package>/`) over flat layout for installable packages.

- Use `pyproject.toml` as single source of truth for deps, tools, and metadata.

- Pin dependencies in `requirements.txt` or `poetry.lock`; use Dependabot for updates.

## Environment & dependency policy

- Always run Python tooling inside a virtual environment (`.venv`).

- Reuse an existing `.venv` when present; create it if missing (`python -m venv .venv`).

- Install dependencies with the venv interpreter (`./.venv/bin/python -m pip ...` on Bash, `.venv\Scripts\python.exe -m pip ...` on Windows).

- Never run project Python commands against the system interpreter.

## Examples

✅ Correct — typed, explicit, idempotent:

```python
from pathlib import Path

def ensure_dir(path: Path) -> None:
    """Create directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)
```

❌ Wrong — bare exception, no type hints:

```python
def ensure_dir(path):
    try:
        os.makedirs(path)
    except:
        pass  # silently swallowed
```

---

## 🏆 Elite Section — Top 5% Python Practices

- **`mypy --strict` as CI gate**: Enforce strict type checking from day one. Disabling rules in `pyproject.toml` must be accompanied by an inline comment explaining why.

- **`ruff` for linting + formatting**: Replace `flake8` + `isort` + `black` with a single `ruff` invocation for speed and consistency.

- **Protocol-based interfaces**: Prefer `typing.Protocol` over ABC for structural subtyping. Avoids inheritance coupling and makes testing with fakes trivial.

- **`hypothesis` for property tests**: For any function that transforms data, write at least one property-based test asserting invariants (e.g. round-trip, idempotency).

- **Async-first for I/O-bound services**: Use `asyncio` + `httpx` + `asyncpg` for service code. Never mix sync and async without explicit bridging (`asyncio.run`, `loop.run_in_executor`).

- **Dependency injection via `__init__`**: Inject all external dependencies (DB, HTTP clients, clocks) via constructor. This enables fast unit tests with fakes without monkey-patching.
