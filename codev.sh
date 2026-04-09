#!/usr/bin/env bash
# codev.sh — CoDev submodule bootstrap (Bash wrapper)
#
# Delegates to codev.py in the same directory. Requires Python 3.9+.
#
# Usage:
#   ./codev.sh init [--strategy extend|override] [--overrides-dir PATH]
#   ./codev.sh update
#   ./codev.sh teardown [--force]
#
# Examples:
#   ./codev.sh init
#   ./codev.sh init --strategy override
#   ./codev.sh update
#   ./codev.sh teardown --force

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEV_PY="${SCRIPT_DIR}/codev.py"

if [[ ! -f "${CODEV_PY}" ]]; then
  echo "ERROR: codev.py not found at: ${CODEV_PY}" >&2
  exit 2
fi

# Prefer .venv python if present in the CoDev submodule
VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python"
if [[ -x "${VENV_PYTHON}" ]]; then
  PYTHON="${VENV_PYTHON}"
elif command -v python3 &>/dev/null; then
  PYTHON="python3"
elif command -v python &>/dev/null; then
  PYTHON="python"
else
  echo "ERROR: Python 3.9+ is required but not found." >&2
  exit 2
fi

exec "${PYTHON}" "${CODEV_PY}" "$@"
