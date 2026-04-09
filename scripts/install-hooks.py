"""
install-hooks.py — Install CoDev git hooks into .git/hooks/.

Usage:
  python scripts/install-hooks.py          # install all hooks
  python scripts/install-hooks.py --check  # verify hooks are installed
"""

from __future__ import annotations

import argparse
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS_SRC = ROOT / "scripts" / "hooks"
HOOKS_DST = ROOT / ".git" / "hooks"


def install_hooks() -> int:
    if not HOOKS_DST.exists():
        print("❌ .git/hooks/ not found — are you in a git repository?")
        return 1

    installed = 0
    for src in HOOKS_SRC.iterdir():
        if src.is_file():
            dst = HOOKS_DST / src.name
            shutil.copy2(src, dst)
            # Make executable
            dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            print(f"  ✅ Installed: .git/hooks/{src.name}")
            installed += 1

    print(f"\nInstalled {installed} hook(s) into .git/hooks/")
    return 0


def check_hooks() -> int:
    failed = 0
    for src in HOOKS_SRC.iterdir():
        if src.is_file():
            dst = HOOKS_DST / src.name
            if dst.exists():
                print(f"  ✅ {src.name} — installed")
            else:
                print(f"  ❌ {src.name} — NOT installed")
                failed += 1
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install CoDev git hooks.")
    parser.add_argument("--check", action="store_true", help="Check if hooks are installed.")
    args = parser.parse_args(argv)

    if args.check:
        return check_hooks()
    return install_hooks()


if __name__ == "__main__":
    sys.exit(main())
