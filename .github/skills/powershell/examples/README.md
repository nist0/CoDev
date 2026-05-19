# PowerShell Skill — Examples

## 1. Safe Script Skeleton

```powershell
[CmdletBinding()]
param()
Write-Output "Hello, world!"
```

## 2. Linting with PSScriptAnalyzer

```text
Invoke-ScriptAnalyzer -Path my_script.ps1
```

## 3. CI Integration (GitHub Actions)

```yaml
- name: Lint PowerShell scripts
run: pwsh -Command 'Invoke-ScriptAnalyzer -Path scripts/*.ps1'
```
