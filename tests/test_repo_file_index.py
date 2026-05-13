from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


repo_file_index = _load_module(
    "repo_file_index",
    ROOT / "scripts" / "repo-file-index.py",
)


def test_list_repo_files_decodes_git_output(monkeypatch) -> None:
    tracked = b"README.md\x00.github/prompts/quickstart.prompt.md\x00external/ignored.md\x00"

    class Completed:
        returncode = 0
        stdout = tracked
        stderr = b""

    monkeypatch.setattr(repo_file_index.subprocess, "run", lambda *args, **kwargs: Completed())
    monkeypatch.setattr(Path, "is_file", lambda self: self.name != "ignored.md")

    files = repo_file_index.list_repo_files(ROOT)

    assert [path.relative_to(ROOT).as_posix() for path in files] == [
        "README.md",
        ".github/prompts/quickstart.prompt.md",
    ]


def test_list_repo_files_by_name_filters_suffix(monkeypatch) -> None:
    paths = [
        ROOT / "README.md",
        ROOT / ".github" / "prompts" / "quickstart.prompt.md",
        ROOT / "routing" / "aliases.yaml",
    ]
    monkeypatch.setattr(repo_file_index, "list_repo_files", lambda root: paths)

    filtered = repo_file_index.list_repo_files_by_name(ROOT, suffix=".md")

    assert [path.relative_to(ROOT).as_posix() for path in filtered] == [
        ".github/prompts/quickstart.prompt.md",
        "README.md",
    ]
