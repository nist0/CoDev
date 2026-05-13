from __future__ import annotations

from pathlib import Path
import subprocess


def list_repo_files(root: Path) -> list[Path]:
    """Return tracked and non-ignored working tree files for the repository."""
    completed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or "git ls-files failed")

    files: list[Path] = []
    for raw_path in completed.stdout.split(b"\0"):
        if not raw_path:
            continue
        relative = Path(raw_path.decode("utf-8", errors="replace"))
        candidate = root / relative
        if candidate.is_file():
            files.append(candidate)
    return files


def list_repo_files_by_name(root: Path, *, suffix: str | None = None, name: str | None = None) -> list[Path]:
    files = list_repo_files(root)
    if suffix is not None:
        files = [path for path in files if path.suffix == suffix]
    if name is not None:
        files = [path for path in files if path.name == name]
    return sorted(files)
