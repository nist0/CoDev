# validation skill
## Description
Provides methods and scripts for validating CoDev routing, registry, and documentation. Covers auto-fix, reporting, and watch mode.
## Features
- Validate routing, registry, and documentation
- Auto-fix and reporting options
- Watch mode for fast feedback
- Used by CI and contributor flows
## Usage
- Use the provided scripts for validation:
```sh
  python scripts/validate-autofix.py
  python scripts/validate-customization-registry.py
  python scripts/validate-markdown-lint.py
  python scripts/validate-readme-registry.py
  python scripts/validate-route-smoke.py
  python scripts/validate-routing-coverage.py
  python scripts/validate-watch.py
```
- Integrate with CI to enforce quality gates.
## Tools
- `scripts/validate-autofix.py` — routing validation with auto-fix
- `scripts/validate-customization-registry.py` — registry validation
- `scripts/validate-markdown-lint.py` — markdown linting
- `scripts/validate-readme-registry.py` — README registry validation
- `scripts/validate-route-smoke.py` — route smoke tests
- `scripts/validate-routing-coverage.py` — routing coverage analysis
- `scripts/validate-watch.py` — watch mode for all validators
## Examples
See `examples/README.md` for concrete usage patterns.
---
Add more details as the skill evolves.
