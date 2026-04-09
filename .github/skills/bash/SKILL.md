---
name: bash
description: Bash shell automation — safety defaults, idempotency, input validation, error handling, and ShellCheck integration.
argument-hint: "[script-purpose] [inputs]"
user-invocable: true
disable-model-invocation: false
---

# Bash Shell Automation (Elite)

## When to use

- Writing Bash scripts for automation, CI steps, or system administration.

## Procedure

### 1. Safety defaults (always)

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- `set -e`: exit on error.
- `set -u`: error on undefined variables.
- `set -o pipefail`: pipelines fail if any command fails.
- `IFS=$'\n\t'`: safe word-splitting.

### 2. Validate inputs and environment early

```bash
# Check required vars
: "${REQUIRED_VAR:?REQUIRED_VAR is not set}"

# Check required tools
command -v kubectl >/dev/null 2>&1 || { echo "kubectl not found"; exit 1; }
```

### 3. Add usage/help

```bash
usage() { echo "Usage: $0 <arg1> <arg2>"; exit 1; }
[[ $# -lt 2 ]] && usage
```

### 4. Use functions for reusable logic

```bash
log() { echo "[$(date -u +%FT%TZ)] $*"; }
die() { log "ERROR: $*"; exit 1; }
```

### 5. Idempotency and cleanup

- Scripts must be safe to run multiple times.
- Use `trap` for cleanup:

```bash
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
```

### 6. Quote everything

```bash
# WRONG
cp $src $dst
# RIGHT
cp "$src" "$dst"
```

### 7. ShellCheck integration

```bash
shellcheck script.sh
# In CI:
npx shellcheck@latest script.sh
```

Fix all SC warnings before committing. Common patterns:

- SC2086: quote variables.
- SC2046: quote command substitutions.
- SC2148: add shebang.

## Self-check

- [ ] `set -euo pipefail` at top.
- [ ] Required variables and tools validated early.
- [ ] Usage/help block present.
- [ ] All variables quoted.
- [ ] Script is idempotent.
- [ ] `trap` cleanup on exit.
- [ ] `shellcheck` passes with no errors.

## Outputs

- Script skeleton with safety defaults.
- Common patterns (retry, lock, cleanup trap).
- ShellCheck integration CI snippet.
