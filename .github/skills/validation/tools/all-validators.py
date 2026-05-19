# Example: all-validators.py
"""
Run all validation scripts for validation skill.
"""
import subprocess
scripts = [
    'scripts/validate-autofix.py',
    'scripts/validate-customization-registry.py',
    'scripts/validate-markdown-lint.py',
    'scripts/validate-readme-registry.py',
    'scripts/validate-route-smoke.py',
    'scripts/validate-routing-coverage.py',
]
for s in scripts:
    print(f'Running {s}...')
    subprocess.run(['python', s])
