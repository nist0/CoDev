from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    config_path = ROOT / ".markdownlint-cli2.yaml"
    if not config_path.exists():
        print(f"Markdown lint config not found: {config_path.relative_to(ROOT).as_posix()}")
        return 1

    npx_executable = shutil.which("npx.cmd") or shutil.which("npx")
    if npx_executable is None:
        print("Failed to run markdown lint: 'npx' was not found.")
        print("Install Node.js, then rerun this validation.")
        return 1

    command = [
        npx_executable,
        "--yes",
        "markdownlint-cli2",
        "--config",
        str(config_path),
    ]

    print("Running markdown lint via markdownlint-cli2...")
    print(f"Command: {' '.join(command)}")

    try:
        completed = subprocess.run(command, cwd=ROOT, check=False)
    except FileNotFoundError:
        print("Failed to run markdown lint: unable to execute npx.")
        return 1

    if completed.returncode != 0:
        print("Markdown lint validation failed.")
        return completed.returncode

    print("Markdown lint validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
