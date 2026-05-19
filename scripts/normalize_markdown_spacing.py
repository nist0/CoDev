from __future__ import annotations

from pathlib import Path
import importlib.util
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]

# import repo-file-index like other scripts
_SPEC = importlib.util.spec_from_file_location(
    "repo_file_index",
    ROOT / "scripts" / "repo-file-index.py",
)
_repo = importlib.util.module_from_spec(_SPEC)  # type: ignore[arg-type]
_SPEC.loader.exec_module(_repo)  # type: ignore[union-attr]

BACKUP_ROOT = ROOT / "reports" / "patches-backup"
BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

FENCE_RE = re.compile(r'^(?P<fence>```+|~~~+).*')
SETEXT_RE = re.compile(r'^[=-]{2,}\s*$')
ATX_HEADING_RE = re.compile(r'^\s{0,3}#{1,6}\s')
LIST_RE = re.compile(r'^\s*([-*+]|\d+\.)\s+')


def normalize_text(orig_text: str) -> str:
    # Normalize to Unix newlines and split
    lines = orig_text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    result: list[str] = []
    in_fence = False
    fence_marker: str | None = None

    for i, raw in enumerate(lines):
        s = raw.rstrip()
        is_blank = (s.strip() == "")

        # detect fence open/close
        m_f = FENCE_RE.match(s)
        if m_f:
            marker = m_f.group('fence')
            if in_fence and marker.startswith(fence_marker or ''):
                # closing fence
                result.append(s)
                in_fence = False
                fence_marker = None
                # ensure one blank line after closing fence if next line non-blank
                if i + 1 < len(lines) and lines[i + 1].strip() != "":
                    if not result or result[-1].strip() != "":
                        result.append("")
                continue
            elif not in_fence:
                # opening fence: ensure blank before
                if result and result[-1].strip() != "":
                    result.append("")
                result.append(s)
                in_fence = True
                fence_marker = marker[:3]
                continue

        if in_fence:
            result.append(s)
            continue

        # setext-style heading underline conversion
        if SETEXT_RE.match(s) and i > 0 and lines[i - 1].strip() != "":
            # convert previous appended line to ATX
            prev_text = result.pop() if result else lines[i - 1].strip()
            underline = s.strip()
            if underline.startswith('='):
                new_header = '# ' + prev_text.strip()
            else:
                new_header = '## ' + prev_text.strip()
            # ensure blank before header
            if result and result[-1].strip() != "":
                result.append("")
            result.append(new_header)
            # ensure blank after header if next line non-blank
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                result.append("")
            continue

        # ATX heading: ensure blank lines around
        if ATX_HEADING_RE.match(s):
            if result and result[-1].strip() != "":
                result.append("")
            # remove trailing punctuation in headings (MD026) if exists
            heading = s.strip()
            if heading.endswith('.'):
                heading = heading.rstrip('.')
            result.append(heading)
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                result.append("")
            continue

        # lists: ensure blank line before list
        if LIST_RE.match(s):
            if result and result[-1].strip() != "":
                result.append("")
            result.append(s)
            continue

        # collapse multiple blanks
        if is_blank:
            if not result or result[-1].strip() == "":
                continue
            else:
                result.append("")
                continue

        # default: normal paragraph/line
        result.append(s)

    # remove leading blank lines
    while result and result[0].strip() == "":
        result.pop(0)
    # ensure single trailing newline
    out = "\n".join(result).rstrip() + "\n"
    return out


def main() -> int:
    args = sys.argv[1:]
    if args:
        markdown_paths = []
        for a in args:
            candidate = (ROOT / a).resolve()
            if candidate.is_file() and candidate.suffix == '.md':
                markdown_paths.append(candidate)
            elif candidate.is_dir():
                markdown_paths.extend([p for p in candidate.rglob('*.md')])
            else:
                # treat as glob relative to repo root
                for x in sorted(ROOT.glob(a)):
                    xp = Path(x)
                    if xp.is_file() and xp.suffix == '.md':
                        markdown_paths.append(xp)
        # de-duplicate and sort
        markdown_paths = sorted(set(markdown_paths))
    else:
        markdown_paths = [
            Path(p) for p in _repo.list_repo_files_by_name(ROOT, suffix='.md')
        ]
    changed = []
    for p in markdown_paths:
        full = p
        try:
            orig = full.read_text(encoding='utf-8')
        except Exception:
            try:
                orig = full.read_text(encoding='utf-16')
            except Exception:
                orig = full.read_text(errors='ignore')
        new = normalize_text(orig)
        if new != orig:
            # backup
            rel = full.relative_to(ROOT)
            dst = BACKUP_ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            print(f"Copying {full} to {dst}")
            shutil.copy2(full, dst)
            full.write_text(new, encoding='utf-8')
            changed.append(str(p))
    if changed:
        print('Normalized spacing in', len(changed), 'files')
        for c in changed[:200]:
            print('-', c)
    else:
        print('No changes needed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
