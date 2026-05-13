from __future__ import annotations

from pathlib import Path
import importlib.util
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


_SYNC_SPEC = importlib.util.spec_from_file_location(
    "sync_readme_inventory",
    ROOT / "scripts" / "sync-readme-inventory.py",
)
_SYNC = importlib.util.module_from_spec(_SYNC_SPEC)  # type: ignore[arg-type]
_SYNC_SPEC.loader.exec_module(_SYNC)  # type: ignore[union-attr]

_REPO_FILE_INDEX_SPEC = importlib.util.spec_from_file_location(
    "repo_file_index",
    ROOT / "scripts" / "repo-file-index.py",
)
_REPO_FILE_INDEX = importlib.util.module_from_spec(_REPO_FILE_INDEX_SPEC)  # type: ignore[arg-type]
_REPO_FILE_INDEX_SPEC.loader.exec_module(_REPO_FILE_INDEX)  # type: ignore[union-attr]


def validate_required_sections(readme_text: str) -> list[str]:
    errors: list[str] = []
    required_sections = [
        "## Agents",
        "## Instructions",
        "## Prompts",
        "## Skills",
    ]

    for section in required_sections:
        if section not in readme_text:
            errors.append(f"README missing required section: {section}")

    required_paths = [
        ".github/agents/",
        ".github/instructions/",
        ".github/prompts/",
        ".github/skills/",
        "reviewer.agent.md",
    ]

    for marker in required_paths:
        if marker not in readme_text:
            errors.append(f"README missing required path marker: {marker}")

    required_markers = [
        "<!-- codev:generated:capabilities:start -->",
        "<!-- codev:generated:agents:start -->",
        "<!-- codev:generated:prompts:start -->",
        "<!-- codev:generated:skills:start -->",
    ]
    for marker in required_markers:
        if marker not in readme_text:
            errors.append(f"README missing required generated marker: {marker}")

    return errors


def validate_generated_inventory_sync(readme_text: str) -> list[str]:
    expected = _SYNC.build_updated_readme(readme_text)
    if expected != readme_text:
        return [
            "README generated inventory is out of sync. Run: python scripts/sync-readme-inventory.py --write"
        ]
    return []


def validate_readme_links(readme_text: str) -> list[str]:
    errors: list[str] = []
    # Markdown links: [text](target)
    link_targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme_text)

    for target in link_targets:
        target = target.strip()
        if not target or target.startswith("http://") or target.startswith("https://"):
            continue

        # remove anchors for local files
        normalized = target.split("#", 1)[0]
        if not normalized:
            continue

        if normalized.startswith("/"):
            candidate = ROOT / normalized.lstrip("/")
        else:
            candidate = ROOT / normalized

        if not candidate.exists():
            errors.append(f"README link target does not exist: {target}")

    return errors


def validate_file_locations() -> list[str]:
    errors: list[str] = []

    for path in _REPO_FILE_INDEX.list_repo_files(ROOT):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith(".agent.md") and not rel.startswith(".github/agents/"):
            errors.append(f"Misplaced agent file: {rel}")
        if rel.endswith(".prompt.md") and not rel.startswith(".github/prompts/"):
            errors.append(f"Misplaced prompt file: {rel}")
        if rel.endswith(".instructions.md") and not rel.startswith(".github/instructions/"):
            errors.append(f"Misplaced instruction file: {rel}")
        if path.name == "SKILL.md" and not rel.startswith(".github/skills/"):
            errors.append(f"Misplaced skill definition file: {rel}")

    return errors


def main() -> int:
    if not README.exists():
        print("README.md not found")
        return 1

    readme_text = README.read_text(encoding="utf-8")

    errors: list[str] = []
    errors.extend(validate_required_sections(readme_text))
    errors.extend(validate_generated_inventory_sync(readme_text))
    errors.extend(validate_readme_links(readme_text))
    errors.extend(validate_file_locations())

    if errors:
        print("README/registry validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("README/registry validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
