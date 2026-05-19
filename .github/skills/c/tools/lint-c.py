#!/usr/bin/env python3
"""
Simple C linter: checks for missing free() and unsafe gets().
"""
import sys

if len(sys.argv) != 2:
    print("Usage: lint-c.py <c-file>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    code = f.read()

if 'gets(' in code:
    print("Warning: Use of unsafe gets().")
if 'malloc(' in code and 'free(' not in code:
    print("Warning: malloc() without free().")
print("Lint complete.")
