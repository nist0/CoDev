# readme-inventory skill
## Description
Provides methods and scripts for synchronising and validating README inventory sections. Ensures documentation matches repository state.
## Features
- Synchronise README inventory blocks
- Validate required sections
- Used by CI and contributor flows
## Usage
- Use the provided script to sync README inventory:
```sh
  python scripts/sync-readme-inventory.py --check
  python scripts/sync-readme-inventory.py --write
```
- Integrate with CI to enforce documentation quality.
## Tools
- `scripts/sync-readme-inventory.py` — main sync/validation script
## Examples
See `examples/README.md` for concrete usage patterns.
---
Add more details as the skill evolves.
