# codev-submodule — Examples

## Example 1: minimal `codev.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/nist0/CoDev/main/schemas/codev.schema.json",
  "version": "1",
  "strategy": "extend",
  "managed": [
    ".github/agents",
    ".github/skills",
    ".github/prompts",
    ".github/instructions",
    ".github/copilot-instructions.md"
  ]
}
```

## Example 2: `codev.json` with override strategy

```json
{
  "$schema": "https://raw.githubusercontent.com/nist0/CoDev/main/schemas/codev.schema.json",
  "version": "1",
  "strategy": "override",
  "managed": [
    ".github/agents",
    ".github/skills",
    ".github/prompts",
    ".github/instructions",
    ".github/copilot-instructions.md"
  ]
}
```

## Example 3: host-specific `copilot-instructions.override.md`

```markdown
# My Project — CoDev Overrides

## Project-specific conventions

- All API controllers must inherit from `BaseApiController`.
- Use `IResult` return types for minimal API endpoints.
- Database migrations must include a rollback script.

## Extra agents active in this repo

- `my-domain.agent.md` — domain expert for order management.
```

## Example 4: full init and verify sequence (PowerShell)

```powershell
# 1. Add submodule
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive

# 2. Bootstrap
.\tools\codev\codev.ps1 init

# 3. Validate
python tools/codev/scripts/validate-route-smoke.py

# 4. Commit
git add codev.json codev-lock.json .github/ .pre-commit-config.yaml
git commit -m "chore: bootstrap CoDev submodule"
git push
```
