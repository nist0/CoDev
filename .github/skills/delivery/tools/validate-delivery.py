#!/usr/bin/env python3
"""
Validate PR hygiene: checks for lint/test/AC in PR description.
"""
import sys

if len(sys.argv) != 2:
    print("Usage: validate-delivery.py <pr-desc-file>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    desc = f.read()

for item in ["tests pass", "lint passes", "AC ticked"]:
    if item not in desc:
        print(f"Missing: {item}")
print("Validation complete.")
