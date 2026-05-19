---
name: cli-platform-bootstrap
description: Add CoDev as a git submodule to a .NET CLI platform repo, run codev init with the extend strategy, author the codev-overrides/ stub, verify, and commit — ready for full project analysis.
argument-hint: "[repo-root] [submodule-path: tools/codev]"
user-invocable: true

## disable-model-invocation: false

# CLI Platform Bootstrap (Elite)

## When to use

- You have just cloned a .NET CLI platform repository and CoDev is not yet present.

- You want to add CoDev as a temporary or permanent git submodule without overwriting existing `.github/` assets.

- You need to initialize the `codev-overrides/` folder for project-specific skill authoring.

- Prerequisite for running the `cli-platform-analysis` skill.

## Prerequisites

| Requirement | Minimum | Notes |
|---|---|---|
| Git | 2.25+ | Submodule support |
| Python | 3.9+ | For validation scripts |
| VS Code | Latest stable | For Copilot customisation |
| Windows Developer Mode | Optional | Required for symlink mode; lockfile mode is the fallback |

## Procedure

### Step 1 — Clone the target repo (if not already done)

```powershell
# PowerShell
git clone https://github.com/<org>/<repo>.git
Set-Location <repo>
git checkout -b feat/bootstrap-codev
```

```bash
# bash
git clone https://github.com/<org>/<repo>.git && cd <repo>
git checkout -b feat/bootstrap-codev
```

**Verify**: `git status` shows a clean working tree on the feature branch.

### Step 2 — Add CoDev as a git submodule

```powershell
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
```

**What happens**: CoDev is cloned into `tools/codev/`. A `.gitmodules` entry is created.

**Verify**: `Test-Path tools/codev/codev.ps1` returns `True`.

**Rollback**:

```powershell
git submodule deinit -f tools/codev
git rm -f tools/codev
Remove-Item -Recurse -Force .git/modules/tools/codev
```

### Step 3 — Run `codev init` with the extend strategy

```powershell
# PowerShell
.\tools\codev\codev.ps1 init --strategy extend
```

```bash
# bash
bash tools/codev/codev.sh init --strategy extend
```

**What happens**:

1. Detects symlink availability (symlink on Windows with Dev Mode; lockfile fallback otherwise).

2. Creates `codev.json` at the repo root (JSON-Schema-validated manifest).

3. **Extends** (does not overwrite) the existing `.github/{agents,skills,prompts,instructions}/`.

4. Inserts `<!-- codev:begin -->` / `<!-- codev:end -->` markers into `copilot-instructions.md`.

5. Installs a pre-commit hook that blocks unauthorized edits to CoDev-managed files.

**Verify**:

```powershell
python tools/codev/scripts/validate-route-smoke.py
```

Expected output: `Route smoke validation passed: 27 case(s).`

**Rollback**: `git checkout -- .github/` restores any managed files to their pre-init state.

### Step 4 — Author the codev-overrides/ stub

Create the stub folder structure for project-specific assets:

```powershell
New-Item -ItemType Directory -Force -Path codev-overrides/agents
New-Item -ItemType Directory -Force -Path codev-overrides/skills
New-Item -ItemType Directory -Force -Path codev-overrides/prompts
New-Item -ItemType Directory -Force -Path codev-overrides/instructions
```

Create the mandatory `codev-overrides/README.md`:

```markdown
# CoDev Overrides

Project-specific CoDev extensions for <project-name>.
All files here extend CoDev managed assets — never edit managed files directly.

| File | Purpose | Owner | Last reviewed |
|---|---|---|---|
| (add a row for each override authored) | | | |
```

### Step 5 — Run the customisation registry validator

```powershell
python tools/codev/scripts/validate-customization-registry.py
```

Expected: no errors. Fix any reported issues before proceeding.

### Step 6 — Commit all bootstrap artefacts

```powershell
git add .gitmodules tools/codev codev.json codev-lock.json .github/ codev-overrides/ .pre-commit-config.yaml
git commit -m "chore: bootstrap CoDev submodule (extend strategy)"
git push origin feat/bootstrap-codev
```

### Step 7 — Confirm CI passes

Check that the CI workflow triggered by the push is green. If the host repo runs markdown-lint or similar validators, confirm they pass against the new `.github/` content.

### Step 8 — Transition to analysis

Once all self-check items below are ticked, immediately invoke:

```text
/cli-platform-analyze
```

## Self-check

- [ ] `validate-route-smoke.py` passed (all cases).

- [ ] `validate-customization-registry.py` passed (no errors).

- [ ] `codev.json` committed and schema-valid.

- [ ] Symlinks verified OR `codev-lock.json` committed (depending on mode).

- [ ] Pre-commit hook active: `git hook run pre-commit` exits 0.

- [ ] `codev-overrides/README.md` committed with correct structure.

- [ ] Existing `.github/` assets preserved — no managed files overwritten or removed.

- [ ] Working on a feature branch; no direct push to `main`.

- [ ] CI passes on the pushed branch.

## Rollback (full)

```powershell
git submodule deinit -f tools/codev
git rm -f tools/codev
Remove-Item -Recurse -Force .git/modules/tools/codev
Remove-Item -Recurse -Force codev-overrides/
Remove-Item codev.json, codev-lock.json, .pre-commit-config.yaml -ErrorAction SilentlyContinue
git commit -m "chore: remove CoDev submodule"
```

## 🏆 Elite Section

- **Lockfile vs symlink discipline**: On Windows without Developer Mode, CoDev uses a lockfile (`codev-lock.json`). This means after every `git submodule update` (CoDev version bump), you must run `codev update` to refresh the lockfile. Document this cadence in `codev-overrides/README.md`.

- **Extend vs override boundary**: The `extend` strategy leaves the host repo's existing `.github/` assets untouched. If the host already has agents or skills with names that conflict with CoDev's defaults, CoDev will suffix them — inspect the `codev init` output carefully and document any name collisions in `codev-overrides/README.md`.

- **Pre-commit as a safety net**: The pre-commit hook blocks accidental edits to CoDev-managed files. If a teammate bypasses it with `--no-verify`, the CI validator (`validate-customization-registry.py`) is the second line of defence — add it as a CI step.

- **Temporary vs permanent submodule**: If CoDev is added temporarily (for onboarding only), document the removal plan in a GitHub issue before merging the bootstrap PR. Avoids the submodule becoming permanent by neglect.
