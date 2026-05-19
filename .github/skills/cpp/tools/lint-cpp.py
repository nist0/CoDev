#!/usr/bin/env python3
"""
Simple C++ linter: checks for missing smart pointers and raw new/delete.
"""
import sys

if len(sys.argv) != 2:
    print("Usage: lint-cpp.py <cpp-file>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    code = f.read()

if 'new ' in code and 'delete ' not in code:
    print("Warning: new without delete.")
if 'unique_ptr' not in code and 'shared_ptr' not in code:
    print("Warning: Consider using smart pointers.")
print("Lint complete.")
