# Onboarding: Bash Skill
Welcome to the bash skill! This guide helps you write, lint, and maintain safe Bash scripts for automation and CI.
## Quickstart Checklist
1. Read SKILL.md for safety patterns and best practices.
2. Use tools in the tools/ directory (e.g. shellcheck) to lint scripts.
3. See examples/README.md for copy-paste script patterns.
4. Integrate shellcheck into CI for automated validation.
## Troubleshooting
- **Script fails unexpectedly?**
- Check for set -euo pipefail and input validation.
- Run shellcheck for diagnostics.
## Resources
- [SKILL.md](SKILL.md): Full procedure and best practices.
- [examples/README.md](examples/README.md): Script patterns and CLI usage.
- [tools/shellcheck.txt](tools/shellcheck.txt): Linting and validation.
_Last reviewed: 2026-05-19_
