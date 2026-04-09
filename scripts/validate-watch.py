"""
validate-watch.py — Watch mode for CoDev routing validation.

Monitors routing/ and .github/ directories for file changes and re-runs
all validation scripts automatically. Provides fast feedback (< 5 sec cycle).

Usage:
  python scripts/validate-watch.py                     # watch with all validators
  python scripts/validate-watch.py --validators smoke  # watch with specific validator(s)
  python scripts/validate-watch.py --once              # single run (no watch), useful in CI

Supported validators:
  smoke      — validate-route-smoke.py
  autofix    — validate-autofix.py (detect only)
  registry   — validate-customization-registry.py
  readme     — validate-readme-registry.py
  coverage   — validate-routing-coverage.py
  all        — all of the above (default)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"

WATCH_DIRS = [
    ROOT / "routing",
    ROOT / ".github" / "agents",
    ROOT / ".github" / "prompts",
    ROOT / ".github" / "skills",
    ROOT / ".github" / "instructions",
]

WATCH_EXTENSIONS = {".yaml", ".yml", ".md", ".py"}

VALIDATORS: dict[str, str] = {
    "smoke": "validate-route-smoke.py",
    "autofix": "validate-autofix.py",
    "registry": "validate-customization-registry.py",
    "readme": "validate-readme-registry.py",
    "coverage": "validate-routing-coverage.py",
}

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def collect_mtimes() -> dict[Path, float]:
    """Return a mapping of watched file → mtime."""
    mtimes: dict[Path, float] = {}
    for watch_dir in WATCH_DIRS:
        if not watch_dir.exists():
            continue
        for path in watch_dir.rglob("*"):
            if path.is_file() and path.suffix in WATCH_EXTENSIONS:
                try:
                    mtimes[path] = path.stat().st_mtime
                except OSError:
                    pass
    return mtimes


def detect_changes(
    old: dict[Path, float],
    new: dict[Path, float],
) -> list[Path]:
    """Return list of paths that were added or modified."""
    changed: list[Path] = []
    for path, mtime in new.items():
        if path not in old or old[path] != mtime:
            changed.append(path)
    return changed


def run_validators(selected: list[str]) -> dict[str, bool]:
    """Run each selected validator. Returns {name: passed}."""
    results: dict[str, bool] = {}
    for name in selected:
        script = VALIDATORS[name]
        script_path = SCRIPTS_DIR / script
        if not script_path.exists():
            print(f"  {YELLOW}[SKIP]{RESET} {script} — not found")
            results[name] = True
            continue
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        passed = result.returncode == 0
        results[name] = passed
        icon = f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"
        label = f"{CYAN}{script}{RESET}"
        print(f"  {icon} {label}")
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                print(f"     {line}")
        if not passed and result.stderr.strip():
            for line in result.stderr.strip().splitlines():
                print(f"     {RED}{line}{RESET}")
    return results


def print_summary(results: dict[str, bool], elapsed: float) -> None:
    passed = sum(1 for ok in results.values() if ok)
    total = len(results)
    color = GREEN if passed == total else RED
    print(
        f"\n{BOLD}{color}{'✅ All passed' if passed == total else f'❌ {total - passed}/{total} failed'}"
        f" ({elapsed:.2f}s){RESET}\n"
    )


def run_once(selected: list[str]) -> int:
    """Run validators once and return exit code."""
    print(f"\n{BOLD}{CYAN}▶ CoDev validation — {len(selected)} validator(s){RESET}")
    t0 = time.monotonic()
    results = run_validators(selected)
    elapsed = time.monotonic() - t0
    print_summary(results, elapsed)
    return 0 if all(results.values()) else 1


def watch_loop(selected: list[str], poll_interval: float = 0.5) -> None:
    """Poll for file changes and re-run validators when changes are detected."""
    print(f"{BOLD}{CYAN}👁  CoDev watch mode — monitoring {len(WATCH_DIRS)} directories{RESET}")
    print(f"    Validators: {', '.join(selected)}")
    print(f"    Poll interval: {poll_interval}s")
    print(f"    Press Ctrl+C to stop.\n")

    # Initial run
    run_once(selected)
    mtimes = collect_mtimes()

    try:
        while True:
            time.sleep(poll_interval)
            new_mtimes = collect_mtimes()
            changed = detect_changes(mtimes, new_mtimes)
            if changed:
                print(
                    f"\n{YELLOW}⚡ Change detected in "
                    f"{', '.join(p.relative_to(ROOT).as_posix() for p in changed[:3])}"
                    f"{'...' if len(changed) > 3 else ''}{RESET}"
                )
                run_once(selected)
                mtimes = new_mtimes
    except KeyboardInterrupt:
        print(f"\n{CYAN}Watch mode stopped.{RESET}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Watch mode for CoDev routing validation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--validators",
        nargs="+",
        choices=[*VALIDATORS.keys(), "all"],
        default=["all"],
        help="Validators to run (default: all).",
        metavar="VALIDATOR",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (no watch loop). Useful in CI.",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=0.5,
        help="Poll interval in seconds (default: 0.5).",
    )
    args = parser.parse_args(argv)

    selected: list[str]
    if "all" in args.validators:
        selected = list(VALIDATORS.keys())
    else:
        selected = args.validators

    if args.once:
        return run_once(selected)

    watch_loop(selected, poll_interval=args.poll)
    return 0


if __name__ == "__main__":
    sys.exit(main())
