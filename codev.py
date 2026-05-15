#!/usr/bin/env python3
"""
codev - CoDev submodule bootstrap CLI.

Commands:
  init      Wire CoDev into the current repository.
  update    Re-sync after 'git submodule update'.
  teardown  Remove all CoDev-managed assets.

Usage:
  python codev.py init [--strategy extend|override] [--overrides-dir PATH]
  python codev.py update
  python codev.py teardown [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1"
LOCK_FILE = "codev-lock.json"
CODEV_JSON = "codev.json"
MANAGED_PATHS_DEFAULT = [
    ".github/agents",
    ".github/skills",
    ".github/prompts",
    ".github/instructions",
    ".github/copilot-instructions.md",
    "routing",
    "scripts",
    "schemas",
]
# Paths where per-FILE wiring is used (agents, prompts, instructions)
PER_FILE_PATHS = [
    ".github/agents",
    ".github/prompts",
    ".github/instructions",
]
# Paths where per-THEME-DIR wiring is used (skills)
PER_THEME_DIR_PATHS = [
    ".github/skills",
]
HOOK_MARKER = "# codev-managed: pre-commit hook"
GITIGNORE_MARKER = "# codev-managed"
MERGE_BEGIN = "<!-- codev:begin -->"
MERGE_END = "<!-- codev:end -->"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def repo_root() -> Path:
    """Return the git repository root."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("ERROR: Not inside a git repository.", file=sys.stderr)
        sys.exit(2)


def load_codev_json(root: Path) -> dict[str, Any]:
    """Load and minimally validate codev.json."""
    path = root / CODEV_JSON
    if not path.exists():
        print(f"ERROR: {CODEV_JSON} not found at {root}.", file=sys.stderr)
        print("       Run 'codev init' to create it.", file=sys.stderr)
        sys.exit(1)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    _validate_codev_json(data, root)
    return data


def _validate_codev_json(data: dict[str, Any], root: Path) -> None:
    """Validate required fields in codev.json."""
    errors: list[str] = []
    if data.get("version") != SCHEMA_VERSION:
        errors.append(f"'version' must be '{SCHEMA_VERSION}'.")
    if not data.get("submodulePath"):
        errors.append("'submodulePath' is required.")
    if data.get("overrideStrategy") not in ("extend", "override"):
        errors.append("'overrideStrategy' must be 'extend' or 'override'.")
    submodule_path = root / data.get("submodulePath", "")
    if not submodule_path.exists():
        errors.append(f"'submodulePath' does not exist: {submodule_path}")
    if errors:
        print("ERROR: codev.json validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)


def normalize_managed_paths(managed_paths: Any) -> list[str]:
    """Return managed paths with current defaults appended in stable order."""
    normalized: list[str] = []
    candidates = managed_paths if isinstance(managed_paths, list) else []
    for path in [*candidates, *MANAGED_PATHS_DEFAULT]:
        if isinstance(path, str) and path not in normalized:
            normalized.append(path)
    return normalized


def sync_codev_manifest(root: Path, cfg: dict[str, Any]) -> list[str]:
    """Backfill current managed path defaults into codev.json when needed."""
    managed_paths = normalize_managed_paths(cfg.get("managedPaths"))
    manifest_path = root / CODEV_JSON
    if manifest_path.exists() and cfg.get("managedPaths") != managed_paths:
        cfg["managedPaths"] = managed_paths
        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
            f.write("\n")
    return managed_paths


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def symlinks_supported() -> bool:
    """Return True if the OS supports creating directory symlinks without elevation."""
    if platform.system() != "Windows":
        return True
    # Check Windows Developer Mode registry key
    try:
        import winreg  # type: ignore[import]

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock",
        )
        val, _ = winreg.QueryValueEx(key, "AllowDevelopmentWithoutDevLicense")
        winreg.CloseKey(key)
        return bool(val)
    except Exception:
        return False


def running_in_wsl() -> bool:
    """Return True when running inside Windows Subsystem for Linux."""
    if platform.system() != "Linux":
        return False

    if os.environ.get("WSL_DISTRO_NAME"):
        return True

    release = platform.release().lower()
    version = platform.version().lower()
    return "microsoft" in release or "microsoft" in version


def is_windows_mount_path(path: Path) -> bool:
    """Return True for WSL-style Windows mounts such as /mnt/c/... ."""
    normalized = str(path).replace("\\", "/")
    parts = normalized.split("/")
    return (
        len(parts) >= 4
        and parts[1] == "mnt"
        and len(parts[2]) == 1
        and parts[2].isalpha()
    )


def symlink_mode_status(root: Path) -> tuple[bool, Optional[str]]:
    """Return whether symlink mode is safe to use for this repository root."""
    if not symlinks_supported():
        return False, "Windows Developer Mode not enabled - using file copy"

    if running_in_wsl() and is_windows_mount_path(root):
        return (
            False,
            "WSL detected on a Windows-mounted repository - using file copy to avoid broken Linux-target symlinks",
        )

    return True, None


def make_symlink(src: Path, dst: Path) -> None:
    """Create a symlink dst -> src, replacing existing symlink if needed."""
    if dst.is_symlink():
        dst.unlink()
    elif dst.exists():
        raise RuntimeError(
            f"Cannot create symlink at {dst}: path exists and is not a symlink.\n"
            "Remove it manually or run 'codev teardown' first."
        )
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(str(src.resolve()), str(dst), target_is_directory=src.is_dir())


def _is_codev_managed_symlink(path: Path, submodule_path: Path) -> bool:
    """Return True if path is a symlink pointing into submodule_path."""
    if not path.is_symlink():
        return False
    try:
        target = Path(os.readlink(str(path))).resolve()
        return str(target).startswith(str(submodule_path.resolve()))
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Manifest merge
# ---------------------------------------------------------------------------

COPILOT_INSTRUCTIONS_DEST = ".github/copilot-instructions.md"
COPILOT_INSTRUCTIONS_OVERRIDE = "copilot-instructions.override.md"


def merge_copilot_instructions(
    root: Path,
    submodule_path: Path,
    overrides_dir: Path,
) -> None:
    """Generate .github/copilot-instructions.md from submodule base + host override."""
    src = submodule_path / COPILOT_INSTRUCTIONS_DEST
    dst = root / COPILOT_INSTRUCTIONS_DEST
    override_file = overrides_dir / COPILOT_INSTRUCTIONS_OVERRIDE

    dst.parent.mkdir(parents=True, exist_ok=True)

    base_content = src.read_text(encoding="utf-8") if src.exists() else ""
    override_content = (
        override_file.read_text(encoding="utf-8") if override_file.exists() else ""
    )

    # Strip any previously generated managed section from override_content
    override_content = _strip_managed_section(override_content)

    lines: list[str] = []
    lines.append(
        f"<!-- AUTO-GENERATED by codev — do not edit this file directly. -->\n"
        f"<!-- Edit the submodule at '{submodule_path.name}' or add host overrides in"
        f" '{overrides_dir.name}/{COPILOT_INSTRUCTIONS_OVERRIDE}'. -->\n\n"
    )
    lines.append(base_content.rstrip("\n") + "\n")

    if override_content.strip():
        lines.append(f"\n{MERGE_BEGIN}\n")
        lines.append("<!-- Host overrides — managed by codev-overrides/ -->\n\n")
        lines.append(override_content.strip() + "\n")
        lines.append(f"\n{MERGE_END}\n")

    dst.write_text("".join(lines), encoding="utf-8")
    print(f"  Generated {COPILOT_INSTRUCTIONS_DEST}")


def _strip_managed_section(content: str) -> str:
    """Remove the <!-- codev:begin/end --> block if present (idempotency)."""
    pattern = re.compile(
        rf"{re.escape(MERGE_BEGIN)}.*?{re.escape(MERGE_END)}\n?",
        re.DOTALL,
    )
    return pattern.sub("", content)


# ---------------------------------------------------------------------------
# Lock file
# ---------------------------------------------------------------------------


def build_lock(managed_files: list[Path], root: Path) -> dict[str, Any]:
    """Build codev-lock.json data."""
    entries: dict[str, str] = {}
    for f in sorted(managed_files):
        if f.is_file():
            rel = f.relative_to(root).as_posix()  # always forward slashes
            entries[rel] = sha256_file(f)
    return {"version": SCHEMA_VERSION, "managed": entries, "overrides": {}}


def write_lock(root: Path, lock: dict[str, Any]) -> None:
    path = root / LOCK_FILE
    with path.open("w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"  Wrote {LOCK_FILE}")


def load_lock(root: Path) -> dict[str, Any]:
    path = root / LOCK_FILE
    if not path.exists():
        print(f"ERROR: {LOCK_FILE} not found. Run 'codev init' first.", file=sys.stderr)
        sys.exit(1)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def verify_lock(root: Path, lock: dict[str, Any]) -> list[str]:
    """Return list of drift errors (empty = clean)."""
    errors: list[str] = []
    for rel_path, expected_sha in lock.get("managed", {}).items():
        file_path = root / rel_path
        if not file_path.exists():
            errors.append(f"MISSING: {rel_path}")
        else:
            actual = sha256_file(file_path)
            if actual != expected_sha:
                errors.append(f"MODIFIED: {rel_path}")
    return errors


# ---------------------------------------------------------------------------
# Gitignore management
# ---------------------------------------------------------------------------


def update_gitignore(root: Path, paths: list[str], remove: bool = False) -> None:
    gi = root / ".gitignore"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""

    if remove:
        # Remove the codev-managed block
        pattern = re.compile(
            rf"{re.escape(GITIGNORE_MARKER)}.*?{re.escape(GITIGNORE_MARKER)} end\n?",
            re.DOTALL,
        )
        updated = pattern.sub("", existing)
        gi.write_text(updated, encoding="utf-8")
        print("  Cleaned .gitignore")
        return

    if f"{GITIGNORE_MARKER} end" in existing:
        return  # Already present — match end-marker to avoid false positives

    block_lines = [f"\n{GITIGNORE_MARKER}\n"]
    for p in paths:
        block_lines.append(f"/{p}\n")
    block_lines.append(f"{GITIGNORE_MARKER} end\n")

    with gi.open("a", encoding="utf-8") as f:
        f.writelines(block_lines)
    print("  Updated .gitignore")


# ---------------------------------------------------------------------------
# Pre-commit hook
# ---------------------------------------------------------------------------

PRE_COMMIT_SCRIPT = """\
#!/usr/bin/env python3
\"\"\"
CoDev pre-commit hook — blocks commits that modify submodule-managed files.
Installed by 'codev init'. Removed by 'codev teardown'.
\"\"\"
# codev-managed: pre-commit hook
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

def main() -> int:
    root = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
    )
    lock_path = root / "codev-lock.json"
    if not lock_path.exists():
        # Symlink mode: check for managed-paths list instead
        codev_json = root / "codev.json"
        if not codev_json.exists():
            return 0  # CoDev not active
        cfg = json.loads(codev_json.read_text(encoding="utf-8-sig"))
        managed = set((cfg.get("managedPaths") or []) + [
            ".github/agents", ".github/skills", ".github/prompts",
            ".github/instructions", ".github/copilot-instructions.md",
            "routing", "scripts", "schemas",
        ])
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], text=True
        ).splitlines()
        violations = [f for f in staged if any(f.startswith(m) for m in managed)]
    else:
        lock = json.loads(lock_path.read_text(encoding="utf-8-sig"))
        managed = set(lock.get("managed", {}).keys())
        staged = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"], text=True
        ).splitlines()
        violations = [f for f in staged if f in managed]

    if violations:
        print("\\n❌  CoDev: commit blocked — the following files are submodule-managed:")
        for v in violations:
            print(f"     {v}")
        print("\\n   To change a managed asset: open a PR in the CoDev submodule repository.")
        print("   To extend/override: add your file to codev-overrides/ instead.")
        print("   Docs: docs/submodule-guide.md\\n")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
"""


def install_pre_commit_hook(root: Path) -> None:
    hooks_dir = root / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "pre-commit"

    if hook_path.exists() and HOOK_MARKER not in hook_path.read_text(encoding="utf-8"):
        # Pre-existing hook not from CoDev — chain it
        existing = hook_path.read_text(encoding="utf-8")
        chained = (
            PRE_COMMIT_SCRIPT
            + "\n# --- pre-existing hook (preserved by codev) ---\n"
            + existing
        )
        hook_path.write_text(chained, encoding="utf-8")
    else:
        hook_path.write_text(PRE_COMMIT_SCRIPT, encoding="utf-8")

    hook_path.chmod(0o755)
    print("  Installed pre-commit hook")


def remove_pre_commit_hook(root: Path) -> None:
    hook_path = root / ".git" / "hooks" / "pre-commit"
    if not hook_path.exists():
        return
    content = hook_path.read_text(encoding="utf-8")
    if HOOK_MARKER not in content:
        return  # Not installed by CoDev; leave it alone
    # Strip the CoDev section and restore any chained hook
    marker_idx = content.find("# --- pre-existing hook")
    if marker_idx != -1:
        restored = content[marker_idx:].replace(
            "# --- pre-existing hook (preserved by codev) ---\n", ""
        )
        hook_path.write_text(restored, encoding="utf-8")
    else:
        hook_path.unlink()
    print("  Removed pre-commit hook")


# ---------------------------------------------------------------------------
# Collect managed files
# ---------------------------------------------------------------------------


def collect_managed_files(submodule_path: Path, managed_paths: list[str]) -> list[Path]:
    """Enumerate all concrete files under the managed paths inside the submodule."""
    files: list[Path] = []
    for rel in managed_paths:
        # Strip leading .github/ prefix to resolve from within the submodule
        src = submodule_path / rel
        if src.is_file():
            files.append(src)
        elif src.is_dir():
            files.extend(f for f in src.rglob("*") if f.is_file())
    return files


# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------


def cmd_init(args: argparse.Namespace) -> None:
    root = repo_root()
    print(f"CoDev init — repository root: {root}")

    # Create or update codev.json
    codev_json_path = root / CODEV_JSON
    if codev_json_path.exists():
        cfg = json.loads(codev_json_path.read_text(encoding="utf-8-sig"))
    else:
        cfg = {
            "$schema": "https://raw.githubusercontent.com/nist0/CoDev/main/schemas/codev.schema.json",
            "version": SCHEMA_VERSION,
            "submodulePath": args.submodule_path or "tools/codev",
            "overrideStrategy": args.strategy,
            "overridesDir": args.overrides_dir,
            "managedPaths": MANAGED_PATHS_DEFAULT,
        }
        with codev_json_path.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
            f.write("\n")
        print(f"  Created {CODEV_JSON}")

    _validate_codev_json(cfg, root)

    submodule_path = root / cfg["submodulePath"]
    overrides_dir = root / cfg.get("overridesDir", "codev-overrides")
    overrides_dir.mkdir(parents=True, exist_ok=True)
    managed_paths = sync_codev_manifest(root, cfg)
    # Exclude copilot-instructions.md from symlink targets (generated separately)
    asset_paths = [p for p in managed_paths if not p.endswith("copilot-instructions.md")]

    use_symlinks, lockfile_reason = symlink_mode_status(root)
    if use_symlinks:
        print("  Mode: symlink")
        _init_symlinks(root, submodule_path, asset_paths)
        _wire_override_symlinks(root, overrides_dir, asset_paths)
        update_gitignore(root, asset_paths)
    else:
        print(f"  Mode: lockfile ({lockfile_reason})")
        _init_lockfile(root, submodule_path, managed_paths, asset_paths)

    merge_copilot_instructions(root, submodule_path, overrides_dir)
    install_pre_commit_hook(root)

    print("\n✅  CoDev init complete.")
    print(f"    Mode           : {'symlink' if use_symlinks else 'lockfile'}")
    print(f"    Submodule      : {cfg['submodulePath']}")
    print(f"    Strategy       : {cfg['overrideStrategy']}")
    print(f"    Overrides dir  : {cfg.get('overridesDir', 'codev-overrides')}")
    print("\n    Verify Copilot resolves agents:")
    print("      Open VS Code and confirm '.github/agents/' lists CoDev agents.")
    if not use_symlinks:
        print("\n    After 'git submodule update', run: python codev.py update")


def _init_symlinks(root: Path, submodule_path: Path, asset_paths: list[str]) -> None:
    per_file = set(PER_FILE_PATHS)
    per_theme = set(PER_THEME_DIR_PATHS)
    for rel in asset_paths:
        if rel in per_file:
            src_dir = submodule_path / rel
            dst_dir = root / rel
            if dst_dir.is_symlink():
                dst_dir.unlink()
            dst_dir.mkdir(parents=True, exist_ok=True)
            if not src_dir.is_dir():
                print(f"  WARN: submodule path not found, skipping: {rel}")
                continue
            for src_file in src_dir.iterdir():
                if not src_file.is_file():
                    continue
                dst_file = dst_dir / src_file.name
                if dst_file.exists() and not _is_codev_managed_symlink(dst_file, submodule_path):
                    print(
                        f"ERROR: collision — {dst_file.relative_to(root)} already exists and is not a CoDev-managed symlink.\n"
                        f"       Remove it or rename it before running 'codev init'.",
                        file=sys.stderr,
                    )
                    sys.exit(3)
                if dst_file.is_symlink():
                    dst_file.unlink()
                os.symlink(str(src_file.resolve()), str(dst_file))
                print(f"  Symlinked {rel}/{src_file.name}")
        elif rel in per_theme:
            src_dir = submodule_path / rel
            dst_dir = root / rel
            if dst_dir.is_symlink():
                dst_dir.unlink()
            dst_dir.mkdir(parents=True, exist_ok=True)
            if not src_dir.is_dir():
                print(f"  WARN: submodule path not found, skipping: {rel}")
                continue
            for theme_src in src_dir.iterdir():
                if not theme_src.is_dir():
                    continue
                theme_dst = dst_dir / theme_src.name
                make_symlink(theme_src, theme_dst)
                print(f"  Symlinked {rel}/{theme_src.name}/")
        else:
            src = submodule_path / rel
            dst = root / rel
            if not src.exists():
                print(f"  WARN: submodule path not found, skipping: {rel}")
                continue
            make_symlink(src, dst)
            print(f"  Symlinked {rel}")


def _wire_override_symlinks(root: Path, overrides_dir: Path, asset_paths: list[str]) -> None:
    """Symlink individual override files from overrides_dir into the matching host dirs."""
    per_file = set(PER_FILE_PATHS)
    for rel in asset_paths:
        if rel not in per_file:
            continue
        # e.g. rel=".github/agents" -> overrides subdir is overrides_dir/"agents"
        rel_suffix = rel.split("/", 1)[-1]
        overrides_src_dir = overrides_dir / rel_suffix
        if not overrides_src_dir.is_dir():
            continue
        dst_dir = root / rel
        dst_dir.mkdir(parents=True, exist_ok=True)
        for src_file in overrides_src_dir.iterdir():
            if not src_file.is_file():
                continue
            dst_file = dst_dir / src_file.name
            if dst_file.exists() and not dst_file.is_symlink():
                continue  # Existing non-symlink file takes precedence
            if dst_file.is_symlink():
                print(f"  WARN: override '{src_file.name}' shadows CoDev-managed file — using override version")
                dst_file.unlink()
            os.symlink(str(src_file.resolve()), str(dst_file))
            print(f"  Symlinked override {rel}/{src_file.name}")


def _init_lockfile(
    root: Path,
    submodule_path: Path,
    managed_paths: list[str],
    asset_paths: list[str],
) -> None:
    per_file = set(PER_FILE_PATHS)
    per_theme = set(PER_THEME_DIR_PATHS)

    # Load existing lock to allow idempotent re-runs without false collision errors
    existing_managed: set[str] = set()
    lock_path = root / LOCK_FILE
    if lock_path.exists():
        try:
            existing_managed = set(
                json.loads(lock_path.read_text(encoding="utf-8-sig")).get("managed", {}).keys()
            )
        except (json.JSONDecodeError, KeyError):
            existing_managed = set()

    managed_files: list[Path] = []
    for rel in asset_paths:
        if rel in per_file:
            src_dir = submodule_path / rel
            dst_dir = root / rel
            if dst_dir.is_symlink():
                dst_dir.unlink()
            dst_dir.mkdir(parents=True, exist_ok=True)
            if not src_dir.is_dir():
                print(f"  WARN: submodule path not found, skipping: {rel}")
                continue
            for src_file in src_dir.iterdir():
                if not src_file.is_file():
                    continue
                dst_file = dst_dir / src_file.name
                rel_key = dst_file.relative_to(root).as_posix()
                if dst_file.exists() and not dst_file.is_symlink():
                    if rel_key not in existing_managed:
                        print(
                            f"ERROR: collision — {dst_file.relative_to(root)} already exists and is not managed by CoDev.\n"
                            f"       Remove it or rename it before running 'codev init'.",
                            file=sys.stderr,
                        )
                        sys.exit(3)
                if dst_file.is_symlink():
                    dst_file.unlink()
                shutil.copy2(str(src_file), str(dst_file))
                managed_files.append(dst_file)
                print(f"  Copied {rel}/{src_file.name}")
        elif rel in per_theme:
            src_dir = submodule_path / rel
            dst_dir = root / rel
            dst_dir.mkdir(parents=True, exist_ok=True)
            if not src_dir.is_dir():
                print(f"  WARN: submodule path not found, skipping: {rel}")
                continue
            for theme_src in src_dir.iterdir():
                if not theme_src.is_dir():
                    continue
                theme_dst = dst_dir / theme_src.name
                if theme_dst.is_symlink():
                    theme_dst.unlink()
                elif theme_dst.exists():
                    shutil.rmtree(str(theme_dst))
                shutil.copytree(str(theme_src), str(theme_dst))
                managed_files.extend(f for f in theme_dst.rglob("*") if f.is_file())
                print(f"  Copied {rel}/{theme_src.name}/")
        else:
            src = submodule_path / rel
            dst = root / rel
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.is_symlink():
                    dst.unlink()
                shutil.copy2(str(src), str(dst))
                managed_files.append(dst)
                print(f"  Copied {rel}")
            elif src.is_dir():
                if dst.is_symlink():
                    dst.unlink()
                elif dst.exists():
                    shutil.rmtree(str(dst))
                shutil.copytree(str(src), str(dst))
                managed_files.extend(f for f in dst.rglob("*") if f.is_file())
                print(f"  Copied {rel}/")
            else:
                print(f"  WARN: submodule path not found, skipping: {rel}")
    lock = build_lock(managed_files, root)
    write_lock(root, lock)


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


def cmd_update(_args: argparse.Namespace) -> None:
    root = repo_root()
    cfg = load_codev_json(root)
    submodule_path = root / cfg["submodulePath"]
    overrides_dir = root / cfg.get("overridesDir", "codev-overrides")
    managed_paths = sync_codev_manifest(root, cfg)
    asset_paths = [p for p in managed_paths if not p.endswith("copilot-instructions.md")]

    print(f"CoDev update — repository root: {root}")

    # Migrate old per-directory symlinks to per-file wiring
    for rel in PER_FILE_PATHS:
        dst = root / rel
        if dst.is_symlink():
            dst.unlink()
            dst.mkdir(parents=True, exist_ok=True)
            print(f"  Migrating {rel}: old directory symlink -> per-file wiring")

    lock_path = root / LOCK_FILE
    symlink_mode_allowed, lockfile_reason = symlink_mode_status(root)
    use_symlinks = symlink_mode_allowed and not lock_path.exists()

    if use_symlinks:
        print("  Mode: symlink — re-generating manifest only")
        _init_symlinks(root, submodule_path, asset_paths)
        _wire_override_symlinks(root, overrides_dir, asset_paths)
    else:
        if lock_path.exists() and symlink_mode_allowed:
            print("  Mode: lockfile — re-copying changed files")
        else:
            print(f"  Mode: lockfile ({lockfile_reason})")
        _init_lockfile(root, submodule_path, managed_paths, asset_paths)

    merge_copilot_instructions(root, submodule_path, overrides_dir)
    print("\n✅  CoDev update complete.")


# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------


def cmd_teardown(args: argparse.Namespace) -> None:
    root = repo_root()

    if not args.force:
        print("This will remove all CoDev-managed assets from the host repository.")
        print("Your 'codev-overrides/' directory and 'codev.json' will NOT be touched.")
        ans = input("Continue? [y/N] ").strip().lower()
        if ans != "y":
            print("Aborted.")
            return

    cfg = {}
    if (root / CODEV_JSON).exists():
        cfg = json.loads((root / CODEV_JSON).read_text(encoding="utf-8-sig"))

    managed_paths = sync_codev_manifest(root, cfg)
    asset_paths = [p for p in managed_paths if not p.endswith("copilot-instructions.md")]
    submodule_path = root / cfg.get("submodulePath", "tools/codev") if cfg else root / "tools/codev"

    per_file = set(PER_FILE_PATHS)
    per_theme = set(PER_THEME_DIR_PATHS)

    print(f"CoDev teardown — repository root: {root}")

    lock_path = root / LOCK_FILE
    if lock_path.exists():
        # Lockfile mode — remove copied files
        lock = load_lock(root)
        for rel_path in lock.get("managed", {}):
            p = root / rel_path
            if p.exists() and not p.is_symlink():
                p.unlink()
                print(f"  Removed {rel_path}")
        # Remove now-empty directories for per-theme-dir and other paths only
        # (per-file directories are left even when empty — host may add files there)
        for rel in asset_paths:
            if rel in per_file:
                continue
            d = root / rel
            if d.is_dir():
                # Remove empty subdirectories bottom-up, then the top-level dir
                for sub in sorted(d.rglob("*"), reverse=True):
                    if sub.is_dir():
                        try:
                            sub.rmdir()  # only succeeds when empty
                        except OSError:
                            pass  # not empty — leave host files intact
                try:
                    d.rmdir()
                except OSError:
                    pass  # not empty — leave host files intact
        lock_path.unlink()
        print(f"  Removed {LOCK_FILE}")
    else:
        # Symlink mode — remove CoDev-managed symlinks
        for rel in asset_paths:
            if rel in per_file:
                dst_dir = root / rel
                src_dir = submodule_path / rel
                if dst_dir.is_symlink():
                    # Old structure (pre-migration directory symlink)
                    dst_dir.unlink()
                    print(f"  Removed symlink {rel}")
                elif dst_dir.is_dir() and src_dir.is_dir():
                    for src_file in src_dir.iterdir():
                        if src_file.is_file():
                            dst_file = dst_dir / src_file.name
                            if dst_file.is_symlink():
                                dst_file.unlink()
                                print(f"  Removed symlink {rel}/{src_file.name}")
            elif rel in per_theme:
                src_dir = submodule_path / rel
                dst_dir = root / rel
                if dst_dir.is_dir() and src_dir.is_dir():
                    for theme_src in src_dir.iterdir():
                        if theme_src.is_dir():
                            theme_dst = dst_dir / theme_src.name
                            if theme_dst.is_symlink():
                                theme_dst.unlink()
                                print(f"  Removed symlink {rel}/{theme_src.name}/")
                elif dst_dir.is_symlink():
                    dst_dir.unlink()
                    print(f"  Removed symlink {rel}")
            else:
                dst = root / rel
                if dst.is_symlink():
                    dst.unlink()
                    print(f"  Removed symlink {rel}")

    # Remove generated copilot-instructions.md
    ci = root / COPILOT_INSTRUCTIONS_DEST
    if ci.exists():
        content = ci.read_text(encoding="utf-8")
        if "AUTO-GENERATED by codev" in content:
            ci.unlink()
            print(f"  Removed {COPILOT_INSTRUCTIONS_DEST}")

    update_gitignore(root, [], remove=True)
    remove_pre_commit_hook(root)

    print("\n✅  CoDev teardown complete. Host repository is in pre-init state.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codev",
        description="CoDev submodule bootstrap CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Wire CoDev into the current repository.")
    p_init.add_argument(
        "--strategy",
        choices=["extend", "override"],
        default="extend",
        help="Override strategy (default: extend)",
    )
    p_init.add_argument(
        "--overrides-dir",
        default="codev-overrides",
        metavar="PATH",
        help="Host customizations directory (default: codev-overrides)",
    )
    p_init.add_argument(
        "--submodule-path",
        default=None,
        metavar="PATH",
        help="Path to the CoDev submodule (default: tools/codev)",
    )

    # update
    sub.add_parser("update", help="Re-sync after 'git submodule update'.")

    # teardown
    p_tear = sub.add_parser(
        "teardown", help="Remove all CoDev-managed assets."
    )
    p_tear.add_argument(
        "--force", action="store_true", help="Skip confirmation prompt."
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "init": cmd_init,
        "update": cmd_update,
        "teardown": cmd_teardown,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
