# Example: file-list.py
"""
List all files in the repository for repo-inventory skill.
"""
import pathlib
for f in pathlib.Path('.').rglob('*'):
    if f.is_file():
        print(f)
