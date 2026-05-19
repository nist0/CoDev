#!/usr/bin/env python3
"""
Suggest improvements for a skill directory (missing files, examples, onboarding).
"""
import os
import sys

if len(sys.argv) != 2:
    print("Usage: improve-skill.py <skill-dir>")
    sys.exit(1)

skill_dir = sys.argv[1]
required = ["SKILL.md", "onboarding.md", os.path.join("examples", "README.md")]
missing = [f for f in required if not os.path.exists(os.path.join(skill_dir, f))]

if missing:
    print(f"Missing files: {', '.join(missing)}")
else:
    print("All required files present.")

# Suggest checking for at least 3 examples
ex_path = os.path.join(skill_dir, "examples", "README.md")
if os.path.exists(ex_path):
    with open(ex_path) as f:
        content = f.read()
    if content.count("```") < 6:
        print("Less than 3 code examples found in examples/README.md.")
