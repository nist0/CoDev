"""Tests for scripts/sync-readme-inventory.py.

Run with:
  python -m pytest tests/test_readme_inventory_sync.py -v
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


sync_readme_inventory = _load_module(
    "sync_readme_inventory",
    ROOT / "scripts" / "sync-readme-inventory.py",
)


def test_repo_readme_inventory_is_idempotent() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert sync_readme_inventory.build_updated_readme(readme) == readme


def test_generated_inventory_covers_real_repo_assets() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    rendered = sync_readme_inventory.build_updated_readme(readme)

    assert "`project-orchestration`" in rendered
    assert "security-agent.agent.md" in rendered
    assert "`/quickstart`" in rendered
    assert "mermaid.instructions.md" in rendered
    assert "`markdown-docops`" in rendered
    assert ".github/workflows/unit-tests.yml" in rendered