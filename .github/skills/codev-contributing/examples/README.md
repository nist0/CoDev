# codev-contributing -- Examples

## Example 1: well-formed bug report issue body

```markdown
## Summary

The `codev update` command does not regenerate `copilot-instructions.md` when the
submodule base changed but the lockfile SHA for that file is unchanged.

## Reproduction

1. Run `codev init` on a fresh repo.
2. Update `tools/codev` to a commit that changes `.github/copilot-instructions.md`.
3. Run `codev update`.
4. Observe: `copilot-instructions.md` in the host repo is not updated.

## Expected behavior

`codev update` should always regenerate `copilot-instructions.md` when the submodule
base changes, regardless of the lockfile SHA.

## Acceptance criteria

- [ ] `codev update` regenerates `copilot-instructions.md` when the submodule base changed.
- [ ] Regression test added: `test_update_regenerates_instructions_on_base_change`.
- [ ] All 23 existing tests still pass.
```

## Example 2: PR body for a new skill

```markdown
## Summary

Adds `codev-submodule` skill: full reference for init, update, override authoring,
teardown, and troubleshooting.

## Changed files

- `.github/skills/codev-submodule/SKILL.md` (new)
- `.github/skills/codev-submodule/examples/README.md` (new)
- `README.md` -- Skills table updated (new row under "Development Environment")
- `.github/copilot-instructions.md` -- capabilities list updated

## Routing smoke-test phrases

| Phrase | Expected capability | Expected agent |
| --- | --- | --- |
| "codev init my repo" | `codev-management` | `CoDev Consumer` |
| "update codev submodule" | `codev-management` | `CoDev Consumer` |

## Verification

All validators pass locally:

```bash

python scripts/validate-route-smoke.py          # 29/29 cases
python scripts/validate-customization-registry.py  # PASS
python scripts/validate-readme-registry.py        # PASS
python scripts/validate-routing-coverage.py       # PASS
python scripts/validate-markdown-lint.py          # 0 errors

```

Closes #105

## Example 3: upstream sync after merge (PowerShell)

```powershell

# After your PR is merged to CoDev main:

Set-Location tools/codev
git fetch origin main
git checkout origin/main
Set-Location ../..

.\tools\codev\codev.ps1 update

python tools/codev/scripts/validate-route-smoke.py

git add tools/codev codev-lock.json .github/copilot-instructions.md
git commit -m "chore: update CoDev submodule (includes fix for #N)"
git push

```
