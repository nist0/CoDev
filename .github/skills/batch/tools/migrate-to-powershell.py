#!/usr/bin/env python3
"""
Suggest PowerShell equivalents for simple batch commands.
"""
import sys

if len(sys.argv) != 2:
    print("Usage: migrate-to-powershell.py <batch-file>")
    sys.exit(1)

print("# This is a stub. For real migration, use a dedicated tool or manual review.")
with open(sys.argv[1]) as f:
    for line in f:
        if line.strip().startswith("echo "):
            print(f"Write-Output '{line.strip()[5:].strip()}'")
        else:
            print(f"# TODO: Migrate: {line.strip()}")
