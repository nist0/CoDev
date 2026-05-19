---
name: codev-submodule
description: Full reference for managing CoDev as a Git submodule — init, update, override authoring, teardown, and troubleshooting.
argument-hint: "[operation: init|update|teardown|override|troubleshoot]"
user-invocable: true

disable-model-invocation: false
---

# CoDev Submodule Management

## When to use

- Setting up CoDev in a new host repository (`codev init`).

- Syncing after a CoDev version bump (`codev update`).

- Authoring host-specific overrides in `codev-overrides/`.

- Removing CoDev from a repository (`codev teardown --force`).

- Diagnosing bootstrap failures, symlink issues, or lockfile drift.

---

## Prerequisites

| Requirement | Minimum | Notes |
| --- | --- | --- |
| Git | 2.25+ | For submodule support |
| Python | 3.9+ | For `codev.py` |
| VS Code | Latest stable | For Copilot customization |
| Windows Developer Mode | Optional | Required for symlink mode on Windows; lockfile mode is the fallback |

---

## 1. Init — add CoDev to a repository

### Step 1 — Add the submodule

```bash
# Bash / Linux / macOS / Git Bash
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
bash tools/codev/codev.sh init
```

```powershell
.\tools\codev\codev.ps1 init
```

**What happens:**

1. Detects symlink availability (Windows Developer Mode → symlink; otherwise → lockfile).

2. Creates `codev.json` at the repo root (JSON-Schema-validated manifest).

3. Links or copies `.github/{agents,skills,prompts,instructions}/` from the submodule.

4. Generates `copilot-instructions.md` with `<!-- codev:begin -->` / `<!-- codev:end -->` markers.

5. Installs a pre-commit hook that blocks unauthorized edits to managed files.

**Verify:**

```bash
python tools/codev/scripts/validate-route-smoke.py
```

Expected: `Route smoke validation passed: 27 case(s).`

### Step 3 — Commit the bootstrap artefacts

```bash
git add codev.json codev-lock.json .github/ .pre-commit-config.yaml
git commit -m "chore: bootstrap CoDev submodule"
```

> In symlink mode, commit the symlinks (not the submodule files directly).
> In lockfile mode, commit `codev-lock.json` and all copied files under `.github/`.

---

## 2. Override — host-specific customization

All host-specific assets live in `codev-overrides/`. The pre-commit hook prevents direct
edits to submodule-managed files.

### Extend `copilot-instructions.md`

Create `codev-overrides/copilot-instructions.override.md` — its content is **appended**
after the submodule base:

```markdown
# Host-Specific Instructions

## My project conventions
- Always use kebab-case for all file names.
- All new endpoints must be documented in `docs/api/`.
```

### Add a host-specific agent

```bash
mkdir -p codev-overrides/agents
```

```markdown
<!-- codev-overrides/agents/my-domain.agent.md -->
---
name: "My Domain Agent"
description: "Domain expert for <your domain>."
tools: []
---

# My Domain Agent
...
```

### Add a host-specific skill

```bash
mkdir -p codev-overrides/skills/my-skill/examples
```

```markdown
<!-- codev-overrides/skills/my-skill/SKILL.md -->
---
name: my-skill
description: ...
---
...
```

### Override strategies

| Strategy | `codev.json` value | Effect |
| --- | --- | --- |
| `extend` (default) | `"strategy": "extend"` | Override file appended after submodule base |
| `override` | `"strategy": "override"` | Override file fully replaces submodule base |

---

## 3. Update — sync after a CoDev version bump

```bash
# Pull the latest submodule commit
git -C tools/codev fetch origin main
git -C tools/codev checkout origin/main

# Re-sync the bootstrap artefacts
bash tools/codev/codev.sh update
# or on Windows:
.\tools\codev\codev.ps1 update
```

**What happens:**

- Lockfile mode: re-copies updated files; refreshes `codev-lock.json` SHA entries.

- Symlink mode: symlinks already point to the submodule — only `copilot-instructions.md`
  is regenerated if the base changed.

**Verify:**

```bash
python tools/codev/scripts/validate-route-smoke.py
```

**Commit:**

```bash
git add tools/codev codev-lock.json .github/copilot-instructions.md
git commit -m "chore: update CoDev submodule to <version>"
```

---

## 4. Teardown — remove CoDev from a repository

> **Windows / non-interactive shells**: always use `--force`. Without it the CLI waits
> for a keystroke that PowerShell cannot forward — it appears frozen until killed.

```bash
bash tools/codev/codev.sh teardown --force
```

```powershell
.\tools\codev\codev.ps1 teardown --force
```

**What happens:**

- Removes all managed files / symlinks under `.github/`.

- Removes `codev-lock.json` and the pre-commit hook entry.

- **Keeps** `codev-overrides/` intact (your host-specific assets are never deleted).

- **Keeps** `tools/codev/` — remove the submodule separately:

```bash
git submodule deinit -f tools/codev
git rm -f tools/codev
rm -rf .git/modules/tools/codev
git commit -m "chore: remove CoDev submodule"
```

---

## 5. Troubleshooting

### Symptom: symlinks not created on Windows

**Cause**: Windows Developer Mode is not enabled.
**Fix**: Enable Developer Mode in Settings → Privacy & Security → For Developers, then re-run `codev init`. Or accept lockfile mode (no action needed — auto-detected).

### Symptom: `codev init` fails with JSON decode error

**Cause**: `codev.json` has a UTF-8 BOM (from PowerShell `Set-Content`).
**Fix**: Open `codev.json` in VS Code, save with encoding "UTF-8 (without BOM)". Or use `Set-Content -Encoding UTF8` (not the default in PowerShell 5).

### Symptom: pre-commit hook blocks edits to `.github/` files

**Cause**: The hook correctly prevents direct edits to submodule-managed files.
**Fix**: Put your changes in `codev-overrides/` instead. To propose a change to the submodule itself, open a PR to the CoDev repo (see `codev-contributing` skill).

### Symptom: `validate-route-smoke.py` fails after `codev update`

**Cause**: A routing YAML in the updated submodule references an agent or capability that does not match.
**Fix**: Check the CoDev changelog for breaking changes. If needed, pin to the previous submodule commit until the host is updated.

### Symptom: `codev teardown` appears frozen (Windows)

**Cause**: Missing `--force` flag; CLI is waiting for a keystroke.
**Fix**: Kill the process (Ctrl+C), then re-run with `--force`.

---

## Self-check

After every operation:

- [ ] `validate-route-smoke.py` passed

- [ ] No managed files edited directly (only `codev-overrides/` was touched)

- [ ] `codev-lock.json` committed (lockfile mode) or symlinks verified (symlink mode)

- [ ] Pre-commit hook active (`pre-commit install` ran and hook is in `.pre-commit-config.yaml`)

- [ ] All changes committed and pushed; CI green

---

## Elite practices

- **Pin the submodule commit** in CI: use `git submodule update --init --recursive` in your pipeline so the exact pinned commit is always used.

- **Automate version bumps**: create a GitHub Actions workflow that opens a PR when the CoDev submodule has a newer commit on `origin/main`.

- **Test overrides in isolation**: validate `codev-overrides/` files with the customization-registry validator before committing.

- **Document your overrides**: maintain a `codev-overrides/README.md` explaining each host-specific asset, why it exists, and who owns it.
