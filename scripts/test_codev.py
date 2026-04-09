"""
Tests for codev.py — covers:
  - codev.json validation
  - SHA256 lockfile build + drift detection
  - Manifest merge (marker-based, idempotent)
  - Pre-commit hook install + remove
  - .gitignore management
  - Lockfile init (file-copy mode)
  - update (idempotent)
  - teardown (clean state)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# Allow importing codev.py from the repo root regardless of cwd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import codev  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_repo(tmp_path: Path) -> Path:
    """Create a minimal fake git repo with a fake CoDev submodule structure."""
    # Init git
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        check=True, capture_output=True, cwd=str(tmp_path),
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        check=True, capture_output=True, cwd=str(tmp_path),
    )

    # Fake submodule structure
    codev_sub = tmp_path / "tools" / "codev"
    for folder in [".github/agents", ".github/skills", ".github/prompts", ".github/instructions"]:
        (codev_sub / folder).mkdir(parents=True, exist_ok=True)

    # Add some fake assets
    (codev_sub / ".github" / "agents" / "router.agent.md").write_text(
        "---\nname: router\n---\n# Router\n", encoding="utf-8"
    )
    skill_dir = codev_sub / ".github" / "skills" / "routing"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text("# Routing Skill\n", encoding="utf-8")
    (codev_sub / ".github" / "copilot-instructions.md").write_text(
        "# CoDev Base Instructions\n\nBase content here.\n", encoding="utf-8"
    )

    # codev.json
    manifest = {
        "version": "1",
        "submodulePath": "tools/codev",
        "overrideStrategy": "extend",
        "overridesDir": "codev-overrides",
        "managedPaths": [
            ".github/agents",
            ".github/skills",
            ".github/prompts",
            ".github/instructions",
            ".github/copilot-instructions.md",
        ],
    }
    (tmp_path / "codev.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Minimal .git/hooks dir
    (tmp_path / ".git" / "hooks").mkdir(parents=True, exist_ok=True)

    return tmp_path


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidateCodevJson:
    def test_valid_manifest_passes(self, tmp_repo: Path) -> None:
        cfg = json.loads((tmp_repo / "codev.json").read_text(encoding="utf-8"))
        # Should not raise
        codev._validate_codev_json(cfg, tmp_repo)

    def test_missing_version_fails(self, tmp_repo: Path) -> None:
        cfg = {"submodulePath": "tools/codev", "overrideStrategy": "extend"}
        with pytest.raises(SystemExit) as exc:
            codev._validate_codev_json(cfg, tmp_repo)
        assert exc.value.code == 1

    def test_bad_override_strategy_fails(self, tmp_repo: Path) -> None:
        cfg = {"version": "1", "submodulePath": "tools/codev", "overrideStrategy": "nope"}
        with pytest.raises(SystemExit):
            codev._validate_codev_json(cfg, tmp_repo)

    def test_nonexistent_submodule_path_fails(self, tmp_repo: Path) -> None:
        cfg = {"version": "1", "submodulePath": "does/not/exist", "overrideStrategy": "extend"}
        with pytest.raises(SystemExit):
            codev._validate_codev_json(cfg, tmp_repo)


# ---------------------------------------------------------------------------
# SHA256 lockfile
# ---------------------------------------------------------------------------


class TestLockfile:
    def test_build_lock_captures_all_files(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        files = [
            tmp_repo / ".github" / "agents" / "router.agent.md",
        ]
        (tmp_repo / ".github" / "agents").mkdir(parents=True, exist_ok=True)
        files[0].write_text("content", encoding="utf-8")
        lock = codev.build_lock(files, tmp_repo)
        assert ".github/agents/router.agent.md" in lock["managed"]

    def test_sha256_is_correct(self, tmp_repo: Path) -> None:
        (tmp_repo / ".github" / "agents").mkdir(parents=True, exist_ok=True)
        f = tmp_repo / ".github" / "agents" / "router.agent.md"
        f.write_text("hello", encoding="utf-8")
        lock = codev.build_lock([f], tmp_repo)
        expected = hashlib.sha256(b"hello").hexdigest()
        assert lock["managed"][".github/agents/router.agent.md"] == expected

    def test_verify_lock_clean(self, tmp_repo: Path) -> None:
        (tmp_repo / ".github" / "agents").mkdir(parents=True, exist_ok=True)
        f = tmp_repo / ".github" / "agents" / "router.agent.md"
        f.write_text("hello", encoding="utf-8")
        lock = codev.build_lock([f], tmp_repo)
        codev.write_lock(tmp_repo, lock)
        loaded = codev.load_lock(tmp_repo)
        errors = codev.verify_lock(tmp_repo, loaded)
        assert errors == []

    def test_verify_lock_detects_drift(self, tmp_repo: Path) -> None:
        (tmp_repo / ".github" / "agents").mkdir(parents=True, exist_ok=True)
        f = tmp_repo / ".github" / "agents" / "router.agent.md"
        f.write_text("original", encoding="utf-8")
        lock = codev.build_lock([f], tmp_repo)
        codev.write_lock(tmp_repo, lock)
        # Simulate unauthorized edit
        f.write_text("tampered", encoding="utf-8")
        loaded = codev.load_lock(tmp_repo)
        errors = codev.verify_lock(tmp_repo, loaded)
        assert any("MODIFIED" in e for e in errors)

    def test_verify_lock_detects_missing_file(self, tmp_repo: Path) -> None:
        (tmp_repo / ".github" / "agents").mkdir(parents=True, exist_ok=True)
        f = tmp_repo / ".github" / "agents" / "router.agent.md"
        f.write_text("hello", encoding="utf-8")
        lock = codev.build_lock([f], tmp_repo)
        codev.write_lock(tmp_repo, lock)
        f.unlink()
        loaded = codev.load_lock(tmp_repo)
        errors = codev.verify_lock(tmp_repo, loaded)
        assert any("MISSING" in e for e in errors)


# ---------------------------------------------------------------------------
# Manifest merge
# ---------------------------------------------------------------------------


class TestManifestMerge:
    def test_generates_copilot_instructions(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        overrides = tmp_repo / "codev-overrides"
        overrides.mkdir(exist_ok=True)
        codev.merge_copilot_instructions(tmp_repo, submodule, overrides)
        dest = tmp_repo / ".github" / "copilot-instructions.md"
        assert dest.exists()
        content = dest.read_text(encoding="utf-8")
        assert "CoDev Base Instructions" in content

    def test_appends_override_section(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        overrides = tmp_repo / "codev-overrides"
        overrides.mkdir(exist_ok=True)
        (overrides / "copilot-instructions.override.md").write_text(
            "## My custom section\nProject uses FastAPI.\n", encoding="utf-8"
        )
        codev.merge_copilot_instructions(tmp_repo, submodule, overrides)
        content = (tmp_repo / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        assert "My custom section" in content
        assert codev.MERGE_BEGIN in content
        assert codev.MERGE_END in content

    def test_merge_is_idempotent(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        overrides = tmp_repo / "codev-overrides"
        overrides.mkdir(exist_ok=True)
        (overrides / "copilot-instructions.override.md").write_text(
            "## Override\nSome content.\n", encoding="utf-8"
        )
        codev.merge_copilot_instructions(tmp_repo, submodule, overrides)
        first = (tmp_repo / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        codev.merge_copilot_instructions(tmp_repo, submodule, overrides)
        second = (tmp_repo / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        assert first == second

    def test_strip_managed_section_idempotent(self) -> None:
        content = textwrap.dedent("""\
            # Base
            Some content.
            <!-- codev:begin -->
            <!-- Host overrides -->
            Custom stuff.
            <!-- codev:end -->
        """)
        stripped = codev._strip_managed_section(content)
        assert codev.MERGE_BEGIN not in stripped
        assert "Custom stuff" not in stripped
        # Stripping twice is idempotent
        assert codev._strip_managed_section(stripped) == stripped


# ---------------------------------------------------------------------------
# Pre-commit hook
# ---------------------------------------------------------------------------


class TestPreCommitHook:
    def test_installs_hook(self, tmp_repo: Path) -> None:
        codev.install_pre_commit_hook(tmp_repo)
        hook = tmp_repo / ".git" / "hooks" / "pre-commit"
        assert hook.exists()
        assert codev.HOOK_MARKER in hook.read_text(encoding="utf-8")

    def test_hook_is_executable(self, tmp_repo: Path) -> None:
        if platform.system() == "Windows":
            pytest.skip("chmod not meaningful on Windows")
        codev.install_pre_commit_hook(tmp_repo)
        hook = tmp_repo / ".git" / "hooks" / "pre-commit"
        assert os.access(str(hook), os.X_OK)

    def test_removes_hook(self, tmp_repo: Path) -> None:
        codev.install_pre_commit_hook(tmp_repo)
        codev.remove_pre_commit_hook(tmp_repo)
        hook = tmp_repo / ".git" / "hooks" / "pre-commit"
        assert not hook.exists()

    def test_preserves_existing_hook_content(self, tmp_repo: Path) -> None:
        hook = tmp_repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho 'existing hook'\n", encoding="utf-8")
        codev.install_pre_commit_hook(tmp_repo)
        content = hook.read_text(encoding="utf-8")
        assert "existing hook" in content
        assert codev.HOOK_MARKER in content

    def test_remove_restores_existing_hook(self, tmp_repo: Path) -> None:
        hook = tmp_repo / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho 'existing hook'\n", encoding="utf-8")
        codev.install_pre_commit_hook(tmp_repo)
        codev.remove_pre_commit_hook(tmp_repo)
        assert hook.exists()
        assert "existing hook" in hook.read_text(encoding="utf-8")
        assert codev.HOOK_MARKER not in hook.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Gitignore
# ---------------------------------------------------------------------------


class TestGitignore:
    def test_adds_codev_block(self, tmp_repo: Path) -> None:
        codev.update_gitignore(tmp_repo, [".github/agents", ".github/skills"])
        gi = (tmp_repo / ".gitignore").read_text(encoding="utf-8")
        assert ".github/agents" in gi
        assert codev.GITIGNORE_MARKER in gi

    def test_idempotent_add(self, tmp_repo: Path) -> None:
        codev.update_gitignore(tmp_repo, [".github/agents"])
        codev.update_gitignore(tmp_repo, [".github/agents"])
        gi = (tmp_repo / ".gitignore").read_text(encoding="utf-8")
        # end-marker appears exactly once per block (start marker also appears in "end" text)
        assert gi.count(f"{codev.GITIGNORE_MARKER} end") == 1

    def test_removes_codev_block(self, tmp_repo: Path) -> None:
        codev.update_gitignore(tmp_repo, [".github/agents"])
        codev.update_gitignore(tmp_repo, [], remove=True)
        gi = (tmp_repo / ".gitignore").read_text(encoding="utf-8") if (tmp_repo / ".gitignore").exists() else ""
        assert codev.GITIGNORE_MARKER not in gi


# ---------------------------------------------------------------------------
# Lockfile init (file-copy mode) — integration
# ---------------------------------------------------------------------------


class TestLockfileInit:
    def test_copies_assets_and_writes_lock(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        managed_paths = [".github/agents", ".github/skills", ".github/copilot-instructions.md"]
        asset_paths = [p for p in managed_paths if not p.endswith("copilot-instructions.md")]
        codev._init_lockfile(tmp_repo, submodule, managed_paths, asset_paths)
        assert (tmp_repo / ".github" / "agents" / "router.agent.md").exists()
        assert (tmp_repo / "codev-lock.json").exists()

    def test_update_is_idempotent(self, tmp_repo: Path) -> None:
        """Running _init_lockfile twice produces the same lockfile."""
        submodule = tmp_repo / "tools" / "codev"
        managed_paths = [".github/agents", ".github/skills"]
        asset_paths = managed_paths
        codev._init_lockfile(tmp_repo, submodule, managed_paths, asset_paths)
        lock1 = (tmp_repo / "codev-lock.json").read_text(encoding="utf-8")
        codev._init_lockfile(tmp_repo, submodule, managed_paths, asset_paths)
        lock2 = (tmp_repo / "codev-lock.json").read_text(encoding="utf-8")
        assert lock1 == lock2

    def test_update_reflects_submodule_change(self, tmp_repo: Path) -> None:
        """After a submodule change, _init_lockfile updates the lockfile SHA."""
        submodule = tmp_repo / "tools" / "codev"
        managed_paths = [".github/agents"]
        codev._init_lockfile(tmp_repo, submodule, managed_paths, managed_paths)
        lock1 = json.loads((tmp_repo / "codev-lock.json").read_text(encoding="utf-8"))
        sha1 = lock1["managed"].get(".github/agents/router.agent.md")

        # Simulate submodule update
        (submodule / ".github" / "agents" / "router.agent.md").write_text(
            "updated content", encoding="utf-8"
        )
        codev._init_lockfile(tmp_repo, submodule, managed_paths, managed_paths)
        lock2 = json.loads((tmp_repo / "codev-lock.json").read_text(encoding="utf-8"))
        sha2 = lock2["managed"].get(".github/agents/router.agent.md")
        assert sha1 != sha2

    def test_replaces_existing_symlink_dir_when_switching_to_lockfile(self, tmp_repo: Path) -> None:
        submodule = tmp_repo / "tools" / "codev"
        managed_paths = [".github/agents"]
        dst = tmp_repo / ".github" / "agents"
        dst.parent.mkdir(parents=True, exist_ok=True)

        try:
            os.symlink(str(submodule / ".github" / "agents"), str(dst), target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation not available in this test environment")

        codev._init_lockfile(tmp_repo, submodule, managed_paths, managed_paths)

        assert dst.exists()
        assert dst.is_dir()
        assert not dst.is_symlink()
        assert (dst / "router.agent.md").exists()
        assert (tmp_repo / "codev-lock.json").exists()


class TestSymlinkModeSelection:
    def test_detects_windows_mount_path(self) -> None:
        assert codev.is_windows_mount_path(Path("/mnt/c/work/repo"))
        assert not codev.is_windows_mount_path(Path("/home/user/repo"))

    def test_wsl_windows_mount_forces_lockfile(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
        monkeypatch.setattr(codev.platform, "system", lambda: "Linux")
        monkeypatch.setattr(codev, "symlinks_supported", lambda: True)

        use_symlinks, reason = codev.symlink_mode_status(Path("/mnt/c/work/repo"))

        assert not use_symlinks
        assert reason is not None
        assert "broken Linux-target symlinks" in reason

    def test_wsl_linux_repo_keeps_symlink_mode(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("WSL_DISTRO_NAME", "Ubuntu")
        monkeypatch.setattr(codev.platform, "system", lambda: "Linux")
        monkeypatch.setattr(codev, "symlinks_supported", lambda: True)

        use_symlinks, reason = codev.symlink_mode_status(Path("/home/user/repo"))

        assert use_symlinks
        assert reason is None


class TestWslLockfileFallback:
    def test_cmd_init_uses_lockfile_when_wsl_windows_mount(
        self, tmp_repo: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(codev, "repo_root", lambda: tmp_repo)
        monkeypatch.setattr(codev, "symlinks_supported", lambda: True)
        monkeypatch.setattr(codev, "running_in_wsl", lambda: True)
        monkeypatch.setattr(codev, "is_windows_mount_path", lambda _path: True)

        args = argparse.Namespace(
            submodule_path=None,
            strategy="extend",
            overrides_dir="codev-overrides",
        )

        codev.cmd_init(args)

        assert (tmp_repo / "codev-lock.json").exists()
        assert (tmp_repo / ".github" / "agents" / "router.agent.md").exists()
        assert not (tmp_repo / ".github" / "agents").is_symlink()

    def test_cmd_update_uses_lockfile_when_wsl_windows_mount(
        self, tmp_repo: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(codev, "repo_root", lambda: tmp_repo)
        monkeypatch.setattr(codev, "symlinks_supported", lambda: True)
        monkeypatch.setattr(codev, "running_in_wsl", lambda: True)
        monkeypatch.setattr(codev, "is_windows_mount_path", lambda _path: True)

        codev.cmd_update(argparse.Namespace())

        assert (tmp_repo / "codev-lock.json").exists()
        assert (tmp_repo / ".github" / "agents" / "router.agent.md").exists()
        assert not (tmp_repo / ".github" / "agents").is_symlink()
