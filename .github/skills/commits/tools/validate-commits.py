#!/usr/bin/env python3
"""
Validate commit messages for Conventional Commits compliance.
"""
import subprocess
import re

pattern = re.compile(r'^(feat|fix|chore|docs|style|refactor|perf|test)(\([\w\-]+\))?: .+')

proc = subprocess.run(['git', 'log', '--pretty=%s', 'HEAD~5..HEAD'], capture_output=True, text=True)
for line in proc.stdout.splitlines():
    if not pattern.match(line):
        print(f"Non-compliant commit: {line}")
print("Validation complete.")
