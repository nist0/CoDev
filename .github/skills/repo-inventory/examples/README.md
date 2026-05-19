# Repo Inventory Skill Examples

## Example 1: List all files

```sh
python tools/file-list.py
```

Output:

```text
.github/skills/prompt-engineering/SKILL.md
scripts/validate-autofix.py
...
```

## Example 2: List all Python files

```sh
python scripts/repo-file-index.py --suffix .py
```

## Example 3: List files in a subdirectory

```text
python scripts/repo-file-index.py --dir scripts/
```

---
**Tips:**

- Use inventory scripts to drive validation and documentation coverage.

- Add new examples as tools/scripts evolve.
_Last reviewed: 2026-05-19_
