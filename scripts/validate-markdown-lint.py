from __future__ import annotations

from pathlib import Path
import importlib.util
import math
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

_REPO_FILE_INDEX_SPEC = importlib.util.spec_from_file_location(
    "repo_file_index",
    ROOT / "scripts" / "repo-file-index.py",
)
_REPO_FILE_INDEX = importlib.util.module_from_spec(_REPO_FILE_INDEX_SPEC)  # type: ignore[arg-type]
_REPO_FILE_INDEX_SPEC.loader.exec_module(_REPO_FILE_INDEX)  # type: ignore[union-attr]

MAX_COMMAND_CHARS = 7000


def _batched_markdown_files(markdown_files: list[str], base_command: list[str]) -> list[list[str]]:
    batches: list[list[str]] = []
    current_batch: list[str] = []
    current_length = len(" ".join(base_command))

    for markdown_file in markdown_files:
        file_length = len(markdown_file) + 1
        if current_batch and current_length + file_length > MAX_COMMAND_CHARS:
            batches.append(current_batch)
            current_batch = []
            current_length = len(" ".join(base_command))

        current_batch.append(markdown_file)
        current_length += file_length

    if current_batch:
        batches.append(current_batch)

    return batches


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

    markdown_files = [
        path.relative_to(ROOT).as_posix()
        for path in _REPO_FILE_INDEX.list_repo_files_by_name(ROOT, suffix=".md")
    ]
    if not markdown_files:
        print("No markdown files found in tracked or non-ignored repository files.")
        return 0

    print("Running markdown lint via markdownlint-cli2...")
    failed = False
    for index, batch in enumerate(_batched_markdown_files(markdown_files, command), start=1):
        batch_command = command + batch
        print(f"Batch {index}: {' '.join(batch_command)}")

        try:
            completed = subprocess.run(batch_command, cwd=ROOT, check=False)
        except FileNotFoundError:
            print("Failed to run markdown lint: unable to execute npx.")
            return 1

        if completed.returncode != 0:
            failed = True

    if failed:
        print("Markdown lint validation failed.")
        return 1

    print("Markdown lint validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
