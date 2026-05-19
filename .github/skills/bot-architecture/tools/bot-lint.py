#!/usr/bin/env python3
"""
Basic bot code linter: checks for missing error handling and secrets hygiene.
"""
import sys

if len(sys.argv) != 2:
    print("Usage: bot-lint.py <bot-file>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    code = f.read()

if 'token=' in code or 'TOKEN=' in code:
    print("Warning: Hardcoded token found. Use environment variables.")
if 'try:' not in code:
    print("Warning: No error handling found.")
print("Lint complete.")
