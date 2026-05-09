# CoDev — Consumer Getting-Started Guide

> This guide is for repository maintainers who want to use **CoDev** as a Git submodule.
> It covers: init, extend, override, upgrade, and teardown.

---

## Prerequisites

| Requirement | Minimum version |
| --- | --- |
| Git | 2.25+ |
| Python | 3.9+ |
| VS Code | Latest stable |
| Windows Developer Mode | Required for symlink mode on Windows (optional — lockfile mode is the fallback) |

---

## 1. Init — add CoDev to your repository

### Step 1 — Add the submodule

```bash
# Bash / Git Bash / macOS / Linux
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
```

```powershell
# PowerShell (Windows)
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
```

### Step 2 — Run `codev init`

```bash
# Bash
./tools/codev/codev.sh init
```

```powershell
# PowerShell
.\tools\codev\codev.ps1 init
```

**What happens:**

- CoDev detects whether OS symlinks are available.
  - **Symlink mode** (Linux / macOS / Windows with Developer Mode): creates directory symlinks from `.github/{agents,skills,prompts,instructions}/` to the submodule.
  - **Lockfile mode** (Windows without Developer Mode, or WSL on `/mnt/<drive>/...`): copies all assets to `.github/`; writes `codev-lock.json`.
- `copilot-instructions.md` is generated from the submodule base.
- The pre-commit hook is installed to block unauthorized edits to managed files.
- `codev.json` is created at the repo root.

When Bash is running from WSL against a Windows-mounted repo, CoDev deliberately
avoids symlink mode because WSL would write Linux-target links such as
`/mnt/c/...`, which Windows tooling does not resolve as proper links.

### Step 3 — Verify

Open VS Code in the repository. Confirm that `.github/agents/` lists CoDev agents (e.g. `router.agent.md`). If using the `/route` slash command, confirm it resolves correctly.

```bash
# Run routing smoke tests
python tools/codev/scripts/validate-route-smoke.py
```

---

## 2. Extend — add host-specific assets

Use `codev-overrides/` to add new agents, skills, prompts, or instructions **without touching** any submodule-managed file.

Project-specific agents, prompts, and instructions can also be placed directly in `.github/agents/`, `.github/prompts/`, and `.github/instructions/` alongside CoDev assets. CoDev only wires its own files into those directories; it never deletes or overwrites files with names it does not own. Running `codev teardown` removes only CoDev-managed files, so any host file placed directly in those directories is preserved.

### Create a host-specific agent

```bash
mkdir -p codev-overrides/agents
cat > codev-overrides/agents/my-custom.agent.md << 'EOF'
---
name: my-custom
description: "Custom agent specific to this repository."
tools: []
mode: agent
---

# My Custom Agent

...
EOF
```

With the default `extend` strategy, the bootstrap automatically links/copies `codev-overrides/agents/my-custom.agent.md` alongside the submodule agents so VS Code Copilot sees both.

### Add a host override section to `copilot-instructions.md`

Create `codev-overrides/copilot-instructions.override.md` with any additional context:

```markdown
## Project-specific context

This repository uses PostgreSQL 17 and .NET 9. Prefer EF Core 9 patterns.
```

Re-run `codev update` to regenerate `copilot-instructions.md` with your override section appended.

---

## 3. Override — replace a managed asset with a host version

Use the `override` strategy when you want a host-specific version of an existing CoDev asset to **shadow** the submodule version.

```bash
# In codev.json, set "overrideStrategy": "override"
```

Then place the replacement file in `codev-overrides/` at the same relative path:

```bash
# Example: replace the router agent
mkdir -p codev-overrides/agents
cp tools/codev/.github/agents/router.agent.md codev-overrides/agents/router.agent.md
# Edit codev-overrides/agents/router.agent.md to your needs
```

Re-run `codev update` to apply the override. The host version at `codev-overrides/agents/router.agent.md` will shadow `tools/codev/.github/agents/router.agent.md`.

**Important**: the shadowed original is still present in the submodule; you are only masking it in the host context. `codev-lock.json` lists overridden files under `"overrides"` for auditability.

---

## 4. Upgrade — update to a newer CoDev version

```bash
# Step 1: update the submodule to the latest commit
git submodule update --remote tools/codev

# Step 2: re-sync host .github/ to the updated submodule
./tools/codev/codev.sh update   # Bash
# or
.\tools\codev\codev.ps1 update  # PowerShell

# Step 3: review the generated copilot-instructions.md diff
git diff .github/copilot-instructions.md

# Step 4: commit the submodule pointer + any changed lock/manifest files
git add tools/codev codev-lock.json .github/copilot-instructions.md
git commit -m "chore(submodule): update CoDev to $(git -C tools/codev describe --tags)"
```

**After upgrade**: if the new CoDev version adds or removes assets, `codev update` will report changed files. Review the diff and verify your overrides are still compatible.

---

## 5. Teardown — remove CoDev from your repository

> **Windows / non-interactive shells**: always pass `--force`.
> Without it, the CLI prints a confirmation prompt and waits for `y` — PowerShell
> cannot forward this input when launched indirectly, causing the process to appear
> stuck until killed.

```bash
./tools/codev/codev.sh teardown --force   # Bash
```

```powershell
.\tools\codev\codev.ps1 teardown --force  # PowerShell
```

Omit `--force` only when running interactively in a terminal that can accept input:

```bash
./tools/codev/codev.sh teardown  # prompts: "Proceed? [y/N]"
```

**What is removed:**

- All symlinks or copied files in `.github/{agents,skills,prompts,instructions}/`
- `codev-lock.json`
- The generated `.github/copilot-instructions.md`
- The pre-commit hook (if it was installed by CoDev)
- CoDev-added lines in `.gitignore`

**What is preserved:**

- `codev.json`
- `codev-overrides/` and all its contents
- Any pre-existing `.git/hooks/pre-commit` content from before CoDev was installed

---

## Common errors and remediation

| Error | Cause | Fix |
| --- | --- | --- |
| `codev.json not found` | Init not run yet | Run `codev init` |
| `submodulePath does not exist` | Submodule not initialized | Run `git submodule update --init` |
| `codev-lock.json not found` | `codev update` not run after `git submodule update` | Run `codev update` |
| `MODIFIED: .github/agents/router.agent.md` in CI | Managed file edited directly | Revert the edit; apply change via submodule PR or override |
| `Windows Developer Mode not enabled` warning | GPO or OS restriction | Use lockfile mode (automatic fallback) or enable Developer Mode |
| Pre-commit hook blocks commit | Staged file is managed by CoDev | Move change to `codev-overrides/` or open a submodule PR |

---

## CI integration

Add the CoDev integrity check to your repository's CI pipeline by calling the reusable workflow:

```yaml
# .github/workflows/ci.yml
jobs:
  codev-check:
    uses: nist0/CoDev/.github/workflows/codev-integrity.yml@main
    with:
      codev-json-path: codev.json
      codev-script-path: tools/codev/codev.py
```

The workflow:

1. Validates `codev.json` against the JSON Schema.
2. Checks `codev-lock.json` is present and parseable (lockfile mode).
3. Verifies no managed file has drifted from its recorded SHA256.
4. On PRs: verifies no managed file is touched in the diff.

Runs on `ubuntu-latest`, `windows-latest`, and `macos-latest`.

---

## Directory reference

```text
<your-repo>/
  .github/
    agents/               ← managed by CoDev (symlink or copy)
    skills/               ← managed by CoDev (symlink or copy)
    prompts/              ← managed by CoDev (symlink or copy)
    instructions/         ← managed by CoDev (symlink or copy)
    copilot-instructions.md  ← generated by codev (submodule base + overrides)
  codev-overrides/        ← YOUR customizations (never touched by codev)
    agents/               ← host-specific agents (extend) or shadow agents (override)
    skills/
    prompts/
    instructions/
    copilot-instructions.override.md  ← host section appended to the generated manifest
  tools/
    codev/                ← the CoDev submodule (never edit here directly)
  codev.json              ← CoDev manifest (committed to your repo)
  codev-lock.json         ← SHA256 lockfile (lockfile mode only; committed to your repo)
```

---

## Authoring rules enforced by CoDev

| Rule | Enforcer |
| --- | --- |
| Never edit files in `.github/agents/`, `.github/skills/`, `.github/prompts/`, `.github/instructions/` directly | Pre-commit hook + CI integrity workflow |
| Never edit the generated `.github/copilot-instructions.md` directly | Pre-commit hook |
| Always run `codev update` after `git submodule update` (lockfile mode) | CI drift check |
| Host customizations belong in `codev-overrides/` | Convention + warning at init time |

---

## Further reading

- [CLI contract reference](submodule-cli-contract.md)
- [`codev.json` JSON Schema](../schemas/codev.schema.json)
- [CoDev architecture map](../README.md)
