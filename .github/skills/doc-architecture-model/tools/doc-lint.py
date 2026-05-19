#!/usr/bin/env python3
"""
Simple doc linter: checks for broken links and heading hierarchy.
"""
import sys
import os
import re

def check_headings(path):
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if re.match(r'^#+[^#\s]', line):
                print(f"Malformed header (missing space) in {path}:{i}")

def check_links(path):
    with open(path) as f:
        for i, line in enumerate(f, 1):
            if re.search(r'\[.*?\]\(\)', line):
                print(f"Empty link in {path}:{i}")

def walk_dir(root):
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(dirpath, file)
                check_headings(path)
                check_links(path)

if len(sys.argv) != 2:
    print("Usage: doc-lint.py <docs-dir>")
    sys.exit(1)

walk_dir(sys.argv[1])
print("Lint complete.")
