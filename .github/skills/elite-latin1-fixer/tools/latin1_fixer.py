#!/usr/bin/env python3
"""
latin1_fixer.py

Scan Markdown files for characters not encodable in ISO-8859-1 (Latin-1)
and common mojibake sequences, offer deterministic replacements, and
optionally apply changes with in-place `.bak` backups and a JSON report.

This script intentionally keeps files encoded as UTF-8 on disk but ensures
the visible characters are within the Latin-1 repertoire (or ASCII sequences).
"""

from __future__ import annotations
import argparse
import json
import shutil
import unicodedata
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set


MOJIBAKE_MAP: Dict[str, str] = {
    # common mojibake sequences -> intended characters
    'Ã©': 'é', 'Ã¨': 'è', 'Ãª': 'ê', 'Ã«': 'ë', 'Ã´': 'ô', 'Ã§': 'ç', 'Ã ': 'à',
    'Ã¡': 'á', 'Ãº': 'ú', 'Ã±': 'ñ', 'Ã¶': 'ö', 'Ã¯': 'ï', 'Ã®': 'î', 'Ã¢': 'â',
    'Ãœ': 'Ü', 'Ã–': 'Ö', 'Ã€': 'À', 'â€”': '--', 'â€“': '-', 'â€¦': '...',
    'â„¢': '(TM)', 'â€˜': "'", 'â€™': "'", 'â€œ': '"', 'â€': '"',
    'Â©': '©', 'Â§': '§', '\u00a0': ' ',
}

# Unicode char -> Latin-1 safe replacement (ASCII preferred where reasonable)
UNICODE_MAP: Dict[str, str] = {
    '—': '--', '–': '-', '…': '...', '‘': "'", '’': "'", '“': '"', '”': '"',
    '•': '-', '·': '-', '→': '->', '←': '<-', '⇒': '=>', '⇐': '<=',
    '≥': '>=', '≤': '<=', '≠': '!=', '≈': '~', '✓': 'OK', '✔': 'OK', '✗': 'X',
    '™': '(TM)', '€': 'EUR', '‚': ',', '„': '"',
}


def list_tracked_github_md_files() -> List[Path]:
    # Prefer git-tracked files under .github; fallback to glob if git not available
    try:
        import subprocess
        p = subprocess.run(['git', 'ls-files', '.github'], capture_output=True, text=True, check=True)
        files = [Path(line.strip()) for line in p.stdout.splitlines() if line.strip().lower().endswith('.md')]
        return files
    except Exception:
        return list(Path('.github').rglob('*.md'))


def find_offending_characters(text: str) -> Set[str]:
    offenders: Set[str] = set()
    for ch in set(text):
        if ord(ch) > 255:
            offenders.add(ch)
    # also detect known mojibake sequences
    for seq in MOJIBAKE_MAP:
        if seq in text:
            offenders.add(seq)
    return offenders


def apply_mappings(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    replacements: List[Tuple[str, str]] = []
    # First pass: mojibake sequences (multi-char)
    for old, new in MOJIBAKE_MAP.items():
        if old in text:
            text = text.replace(old, new)
            replacements.append((old, new))

    # Second pass: single unicode chars -> latin1-safe sequences
    for old, new in UNICODE_MAP.items():
        if old in text:
            text = text.replace(old, new)
            replacements.append((old, new))

    # Finalize: replace any remaining non-latin1 chars with NFKD ascii fallback
    changed_pairs: List[Tuple[str, str]] = []
    chars = sorted({ch for ch in text if ord(ch) > 255})
    for ch in chars:
        nfkd = unicodedata.normalize('NFKD', ch)
        ascii_fallback = ''.join(c for c in nfkd if ord(c) < 128)
        if ascii_fallback:
            text = text.replace(ch, ascii_fallback)
            changed_pairs.append((ch, ascii_fallback))
        else:
            # last resort: use U+XXXX notation
            rep = f'U+{ord(ch):04X}'
            text = text.replace(ch, rep)
            changed_pairs.append((ch, rep))

    replacements.extend(changed_pairs)
    return text, replacements


def process_file(path: Path, apply: bool, backup: bool) -> Dict:
    data = {
        'file': str(path),
        'changed': False,
        'pre_size': None,
        'post_size': None,
        'replacements': [],
    }
    text = path.read_text(encoding='utf-8')
    data['pre_size'] = len(text.encode('utf-8'))
    offenders = find_offending_characters(text)
    if not offenders:
        data['changed'] = False
        data['post_size'] = data['pre_size']
        return data

    new_text, replacements = apply_mappings(text)
    if new_text != text:
        data['changed'] = True
        data['replacements'] = replacements
        data['post_size'] = len(new_text.encode('utf-8'))
        if apply:
            if backup:
                bak = path.with_suffix(path.suffix + '.bak')
                if not bak.exists():
                    shutil.copy2(path, bak)
            path.write_text(new_text, encoding='utf-8')
    else:
        data['changed'] = False
        data['post_size'] = data['pre_size']

    return data


def main(argv=None):
    p = argparse.ArgumentParser(description='Elite Latin-1 fixer: detect and replace non-Latin-1 characters in .github markdown files')
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', help='Single file to check/apply', type=Path)
    group.add_argument('--glob', '-g', help='Glob pattern to match files (e.g. ".github/**/*.md")')
    p.add_argument('--list-only', action='store_true', help='List offending files and characters; do not apply')
    p.add_argument('--apply', action='store_true', help='Apply replacements')
    p.add_argument('--backup', action='store_true', help='Create in-place .bak backup for each modified file')
    p.add_argument('--log', help='JSON log path (writes summary)')
    p.add_argument('--verbose', '-v', action='store_true')
    args = p.parse_args(argv)

    if args.file:
        files = [args.file]
    else:
        # naive glob using pathlib
        files = [Path(p) for p in sorted(Path('.').glob(args.glob))]
        # If glob matches nothing and pattern appears to be .github, fallback to git-tracked
        if not files and args.glob and args.glob.startswith('.github'):
            files = list_tracked_github_md_files()

    summary = []
    for fp in files:
        if not fp.exists():
            continue
        text = fp.read_text(encoding='utf-8')
        offenders = find_offending_characters(text)
        if offenders:
            if args.list_only:
                print(f'{fp}:', ''.join(sorted(set(offenders))))
                summary.append({'file': str(fp), 'offenders': sorted(list(offenders))})
            else:
                res = process_file(fp, apply=args.apply, backup=args.backup)
                summary.append(res)
                if args.verbose:
                    print(json.dumps(res, ensure_ascii=False, indent=2))

    if args.log:
        log_path = Path(args.log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
        if args.verbose:
            print(f'Wrote log to {log_path}')

    # exit code 0 if no errors; non-zero if there were offenders and we did not apply changes
    if any((s.get('changed') for s in summary)):
        # changed files were produced
        return 0
    if any((s.get('offenders') for s in summary)):
        # offenders found but not applied
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
