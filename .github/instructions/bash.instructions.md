---
name: "Bash Defaults"
description: "Bash guidance: safe shell scripting."

applyTo: "**/*.sh"
---

# Bash Defaults

## Safety first

- Always start scripts with `set -euo pipefail`.

- Validate inputs early and fail with clear, actionable error messages.

- Quote all variable expansions: `"$var"`, `"${array[@]}"`.

- Avoid parsing `ls`; use globs or `find` instead.

## Idempotency & robustness

- Keep scripts idempotent where possible (safe to rerun).

- Use `mktemp` for temporary files; clean up with `trap 'rm -f "$tmp"' EXIT`.

- For complex logic, consider using a more robust language (e.g. Python).

## Conventions

- Include usage examples in a `--help` flag or comment header.

- Use consistent formatting; lint with ShellCheck in CI.

- Prefer `[[ ]]` over `[ ]` for conditionals in bash scripts.

- Use `local` for variables inside functions to avoid scope leaks.

Example: safe script skeleton
---

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <environment> <version>"
  exit 1
}

[[ $# -ne 2 ]] && usage

ENV="$1"
VERSION="$2"

echo "Deploying version ${VERSION} to ${ENV}"
```

---

## 🏆 Elite Section — Top 5% Bash Practices

- **ShellCheck in CI as hard gate**: Run `shellcheck -S error *.sh` on every PR. Never merge scripts with ShellCheck errors; warnings must be suppressed with a comment explaining the rationale.

- **BATS for script testing**: Use `bats-core` to write unit tests for non-trivial shell scripts. Test success paths, failure paths, and edge inputs (empty string, spaces in paths).

- **`errexit` + subshell isolation**: Wrap risky sequences in a subshell `(set -e; risky_cmd)` to contain failures without aborting the parent process prematurely.

- **Named pipes over temp files**: For streaming data between processes, prefer `<(cmd)` process substitution or named pipes to avoid disk I/O and temp file cleanup.

- **Structured output for automation**: When a script is consumed by other scripts, emit newline-delimited JSON (`jq -cn`) instead of human-readable text — machine-readable by default, human-readable on demand with `| jq .`.

- **Version-pin external tools**: When a script downloads or relies on external binaries, pin the version and verify the SHA-256 checksum before executing.
