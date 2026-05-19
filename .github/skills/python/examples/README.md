# Examples: python skill

This file collects usage examples, CLI invocations, and integration patterns for the python skill.

## Example 1: Linting a Python Script

- Use the python skill to lint a script:

```sh
python -m flake8 my_script.py
```

## Example 2: Running Type Checks

- Use the python skill to run type checks:

```text
python -m mypy my_module/
```

## Example 3: Running Tests

- Use the python skill to run tests:

```sh
python -m pytest tests/
```

## Example 4: Safe Script Skeleton

- Use the python skill to run a safe script skeleton:

```text
python -m argparse my_script.py --name "world"
```

## Example 5: CI Integration

- Use the python skill to run CI integration:

```sh
python -m flake8 scripts/*.py
```

---
Add more examples as new tools or scripts are integrated with this skill.
