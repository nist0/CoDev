#!/usr/bin/env python3
"""Fix common malformed frontmatter patterns in `.github` customization files.

Usage:
  python scripts/fix_frontmatter.py [--apply]

If `--apply` is not given the script runs in dry-run mode and prints proposed changes.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
GLOB_PATTERNS = [
    ".github/agents/*.agent.md",
    ".github/instructions/*.instructions.md",
    ".github/prompts/*.prompt.md",
    ".github/skills/**/SKILL.md",
]


def find_files() -> Iterable[Path]:
    for pat in GLOB_PATTERNS:
        for p in sorted(ROOT.glob(pat)):
            yield p


def backup(path: Path) -> None:
    reports = ROOT / "reports" / "patches-backup"
    reports.mkdir(parents=True, exist_ok=True)
    dest = reports / path.relative_to(ROOT).as_posix().replace("/", "_")
    dest.write_bytes(path.read_bytes())


def fix_text(text: str) -> str:
    # Replace a malformed opening '## ---' (with optional BOM) with '---'
    text = re.sub(r"\A##\s*\ufeff?---\s*\n", "---\n", text)

    # Convert '## applyTo: "..."' into 'applyTo: "..."' and close frontmatter right after it
    def applyto_repl(m: re.Match) -> str:
        val = m.group(1).strip()
        return f"applyTo: {val}\n---\n"

    text, n1 = re.subn(r"^##\s*applyTo:\s*(\".*\"|'.*'|[^\n]+)\s*$", applyto_repl, text, flags=re.MULTILINE)

    # Convert '## send: true' into 'send: true' and close frontmatter
    def send_repl(m: re.Match) -> str:
        val = m.group(1).strip()
        return f"send: {val}\n---\n"

    text, n2 = re.subn(r"^##\s*send:\s*(.+)\s*$", send_repl, text, flags=re.MULTILINE)

    # Convert '## argument-hint: ...' into 'argument-hint: ...' and close frontmatter
    def arg_repl(m: re.Match) -> str:
        val = m.group(1).strip()
        return f"argument-hint: {val}\n---\n"

    text, n3 = re.subn(r"^##\s*argument-hint:\s*(\".*\"|'.*'|[^\n]+)\s*$", arg_repl, text, flags=re.MULTILINE)

    # Generic: convert any '## key: value' at the start of a line into 'key: value'
    # Close frontmatter after the first such conversion to avoid leaving YAML unclosed.
    closed = False

    def generic_repl(m: re.Match) -> str:
        nonlocal closed
        key = m.group(1).strip()
        val = m.group(2).strip()
        if not closed:
            closed = True
            return f"{key}: {val}\n---\n"
        return f"{key}: {val}\n"

    text, n4 = re.subn(r"^##\s*([A-Za-z0-9_-]+):\s*(.+)\s*$", generic_repl, text, flags=re.MULTILINE)

    # Remove top-level 'send: ...' entries from frontmatter (not allowed for agent top-level)
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if m:
        fm = m.group(1)
        cleaned = re.sub(r"(?m)^[ \t]*send:\s*(?:true|false|\".*\"|'.*'|[^\n]+)\s*$", "", fm)
        if cleaned != fm:
            rest = text[m.end():]
            text = "---\n" + cleaned.rstrip("\n") + "\n---\n" + rest

    return text



def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write fixes to files")
    args = parser.parse_args(argv)

    changed = 0
    for path in find_files():
        text = path.read_text(encoding="utf-8")
        new = fix_text(text)
        if new != text:
            changed += 1
            print(f"Would modify: {path.relative_to(ROOT)}")
            if args.apply:
                backup(path)
                path.write_text(new, encoding="utf-8")
                print(f"Applied and backed up: {path.relative_to(ROOT)}")

    if changed == 0:
        print("No files would be modified.")
    else:
        print(f"Files affected: {changed}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
