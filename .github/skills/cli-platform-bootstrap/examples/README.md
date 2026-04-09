# cli-platform-bootstrap — Examples

## Example 1: Bootstrap CoDev into a fresh clone on Windows (lockfile mode)

**Scenario**: Windows machine without Developer Mode. CoDev falls back to lockfile.

```powershell
# 1. Clone and branch
git clone https://github.com/myorg/my-cli-platform.git
Set-Location my-cli-platform
git checkout -b feat/bootstrap-codev

# 2. Add submodule
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive

# 3. Bootstrap (extend strategy)
.\tools\codev\codev.ps1 init --strategy extend
# Output includes: "Symlink mode unavailable — using lockfile mode. codev-lock.json created."

# 4. Verify
python tools/codev/scripts/validate-route-smoke.py
# Expected: Route smoke validation passed: 27 case(s).

# 5. Stub overrides
New-Item -ItemType Directory -Force -Path codev-overrides/agents, codev-overrides/skills, codev-overrides/prompts, codev-overrides/instructions

# 6. Validate registry
python tools/codev/scripts/validate-customization-registry.py

# 7. Commit
git add .
git commit -m "chore: bootstrap CoDev submodule (extend strategy, lockfile mode)"
git push origin feat/bootstrap-codev
```

**Expected result**: CI green, `codev-lock.json` committed, `validate-route-smoke.py` passes.

---

## Example 2: Bootstrap on Linux / macOS (symlink mode)

```bash
git clone https://github.com/myorg/my-cli-platform.git && cd my-cli-platform
git checkout -b feat/bootstrap-codev
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
bash tools/codev/codev.sh init --strategy extend
# Output: "Symlink mode active."
python tools/codev/scripts/validate-route-smoke.py
mkdir -p codev-overrides/{agents,skills,prompts,instructions}
python tools/codev/scripts/validate-customization-registry.py
git add . && git commit -m "chore: bootstrap CoDev submodule (extend strategy, symlink mode)"
git push origin feat/bootstrap-codev
```
