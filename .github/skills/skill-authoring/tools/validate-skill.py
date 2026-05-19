#!/usr/bin/env python3
"""
Validate a skill directory for required files and structure.
"""
import os
import sys

if len(sys.argv) != 2:
    print("Usage: validate-skill.py <skill-dir>")
    sys.exit(1)

skill_dir = sys.argv[1]
required = ["SKILL.md", "onboarding.md", os.path.join("examples", "README.md")]
missing = [f for f in required if not os.path.exists(os.path.join(skill_dir, f))]

if missing:
    print(f"Missing files: {', '.join(missing)}")
    sys.exit(2)
print("Skill structure valid.")
