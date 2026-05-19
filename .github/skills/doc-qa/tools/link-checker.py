# Example: link-checker.py
"""
Check for broken links in Markdown files for doc-qa skill.
"""
import sys, re, pathlib
for md in pathlib.Path('.').rglob('*.md'):
    for i, line in enumerate(md.read_text(encoding='utf-8').splitlines(), 1):
        for m in re.finditer(r'\[(.*?)\]\((.*?)\)', line):
            if not pathlib.Path(m.group(2)).exists():
                print(f'{md}:{i}: Broken link: {m.group(2)}')
