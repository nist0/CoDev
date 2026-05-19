# Validation Skill Examples

## Example 1: Run all validators

```sh
python tools/all-validators.py
```

Output:

```text
Running scripts/validate-autofix.py...
Running scripts/validate-customization-registry.py...
Running scripts/validate-markdown-lint.py...
Running scripts/validate-readme-registry.py...
Running scripts/validate-route-smoke.py...
Running scripts/validate-routing-coverage.py...
Running scripts/validate-watch.py...
```

## Example 2: Run a single validator

```sh
python scripts/validate-readme-registry.py
```

## Example 3: Watch mode for fast feedback

```text
python scripts/validate-watch.py
```

---
**Tips:**

- Integrate validators into CI for automated checks.

- Use the output to identify and fix issues before PR.

- Add new examples as tools/scripts evolve.
_Last reviewed: 2026-05-19_
