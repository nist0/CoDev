"""Synchronize generated inventory sections in README.md.

Usage:
  python scripts/sync-readme-inventory.py --check
  python scripts/sync-readme-inventory.py --write

The script owns inventory-heavy README sections that should match the repository
state exactly: workflows, routing capabilities/domains, agents, instructions,
prompts, and skills.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

GENERATED_BLOCKS = (
    "workflows",
    "capabilities",
    "domains",
    "agents",
    "instructions",
    "prompts",
    "skills",
)


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at top level in {path.relative_to(ROOT).as_posix()}")
    return data


def _read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def _read_frontmatter(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, flags=re.DOTALL)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return {}
    return data


def _body_summary(path: Path) -> str:
    text = _read_text(path)
    text = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", text, flags=re.DOTALL)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        return line
    return ""


def _escape_cell(value: Any) -> str:
    text = str(value).strip().replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.replace("|", "\\|")


def _render_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_escape_cell(cell) for cell in row) + " |")
    return "\n".join(lines)


def _workflow_triggers(path: Path) -> str:
    text = _read_text(path)
    triggers: list[str] = []
    ordered = [
        (r"^\s*pull_request\s*:", "pull_request"),
        (r"^\s*push\s*:", "push"),
        (r"^\s*workflow_call\s*:", "workflow_call"),
        (r"^\s*workflow_dispatch\s*:", "workflow_dispatch"),
        (r"^\s*schedule\s*:", "schedule"),
    ]
    for pattern, label in ordered:
        if re.search(pattern, text, flags=re.MULTILINE):
            triggers.append(label)
    return ", ".join(triggers) if triggers else "manual/other"


def _workflow_name(path: Path) -> str:
    text = _read_text(path)
    match = re.search(r"^name:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else path.name


def render_workflows() -> str:
    rows: list[list[str]] = []
    workflows_dir = ROOT / ".github" / "workflows"
    for path in sorted(workflows_dir.glob("*.yml")):
        rows.append([
            _workflow_name(path),
            path.relative_to(ROOT).as_posix(),
            _workflow_triggers(path),
        ])
    return _render_table(["Workflow", "File", "Triggers"], rows)


def render_capabilities() -> str:
    data = _read_yaml(ROOT / "routing" / "capabilities.yaml")
    rows: list[list[str]] = []
    for item in data.get("capabilities", []):
        rows.append([
            f"`{item['id']}`",
            item.get("description", ""),
            item.get("default_agent", ""),
        ])
    return _render_table(["Capability ID", "Description", "Default Agent"], rows)


def render_domains() -> str:
    data = _read_yaml(ROOT / "routing" / "domains.yaml")
    rows: list[list[str]] = []
    for item in data.get("domains", []):
        keywords = ", ".join(f"`{kw}`" for kw in item.get("keywords", [])[:8])
        rows.append([f"`{item['id']}`", keywords])
    return _render_table(["Domain ID", "Example Keywords"], rows)


def render_agents() -> str:
    rows: list[list[str]] = []
    for path in sorted((ROOT / ".github" / "agents").glob("*.agent.md")):
        meta = _read_frontmatter(path)
        rows.append([
            meta.get("name", path.name.removesuffix(".agent.md")),
            path.name,
            meta.get("description", ""),
        ])
    return _render_table(["Agent", "File", "Description"], rows)


def render_instructions() -> str:
    rows: list[list[str]] = []
    for path in sorted((ROOT / ".github" / "instructions").glob("*.instructions.md")):
        meta = _read_frontmatter(path)
        rows.append([
            path.name,
            f"`{meta.get('applyTo', '')}`",
            meta.get("description", ""),
        ])
    return _render_table(["File", "applyTo", "Description"], rows)


def render_prompts() -> str:
    rows: list[list[str]] = []
    for path in sorted((ROOT / ".github" / "prompts").glob("*.prompt.md")):
        meta = _read_frontmatter(path)
        command = "/" + path.name.removesuffix(".prompt.md")
        description = meta.get("description") or _body_summary(path)
        rows.append([
            f"`{command}`",
            path.name,
            meta.get("agent", ""),
            description,
        ])
    return _render_table(["Prompt", "File", "Agent", "Description"], rows)


def render_skills() -> str:
    rows: list[list[str]] = []
    for path in sorted((ROOT / ".github" / "skills").glob("*/SKILL.md")):
        meta = _read_frontmatter(path)
        rows.append([
            f"`{path.parent.name}`",
            meta.get("description", ""),
        ])
    return _render_table(["Skill", "Description"], rows)


def rendered_blocks() -> dict[str, str]:
    return {
        "workflows": render_workflows(),
        "capabilities": render_capabilities(),
        "domains": render_domains(),
        "agents": render_agents(),
        "instructions": render_instructions(),
        "prompts": render_prompts(),
        "skills": render_skills(),
    }


def _replace_block(readme_text: str, name: str, content: str) -> str:
    start = f"<!-- codev:generated:{name}:start -->"
    end = f"<!-- codev:generated:{name}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), flags=re.DOTALL)
    replacement = f"{start}\n{content.rstrip()}\n{end}"
    if not pattern.search(readme_text):
        raise ValueError(f"README missing generated block markers for {name}")
    return pattern.sub(replacement, readme_text, count=1)


def build_updated_readme(readme_text: str) -> str:
    updated = readme_text
    for name, content in rendered_blocks().items():
        updated = _replace_block(updated, name, content)
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synchronize generated README inventory blocks.")
    parser.add_argument("--write", action="store_true", help="Write the updated README.md in place.")
    parser.add_argument("--check", action="store_true", help="Exit non-zero if README.md is out of sync.")
    args = parser.parse_args(argv)

    if args.write and args.check:
        parser.error("Use either --write or --check, not both.")

    readme_text = README.read_text(encoding="utf-8")
    updated = build_updated_readme(readme_text)

    if args.write:
        README.write_text(updated, encoding="utf-8")
        print("README inventory blocks synchronized.")
        return 0

    if args.check:
        if updated != readme_text:
            print("README generated inventory is out of sync. Run: python scripts/sync-readme-inventory.py --write")
            return 1
        print("README generated inventory is in sync.")
        return 0

    print(updated)
    return 0


if __name__ == "__main__":
    sys.exit(main())