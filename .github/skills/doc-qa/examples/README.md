# Example: Check for broken links

To check for broken links in Markdown files:

```sh
python tools/link-checker.py
```

Output:

```text
docs/example.md:12: Broken link: missing-file.md
```

## Examples: doc-qa skill

This file collects usage examples, CLI invocations, and integration patterns for the doc-qa skill.

## Example 1: Linting Markdown Docs

- Use the doc-qa skill to lint all Markdown files:

```sh
python scripts/validate-markdown-lint.py
```

## Example 2: Checking for Broken Links

- Use the doc-qa skill to check for broken links in documentation:
  (Add script/tool usage here if available.)

---
Add more examples as new tools or scripts are integrated with this skill.
