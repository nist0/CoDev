---
name: "PowerShell Defaults"
description: "PowerShell guidance: idempotence, error handling, safe automation."
applyTo: "**/*.ps1"
---

# PowerShell Defaults

## Safety & error handling

- Use strict error handling: `$ErrorActionPreference = 'Stop'`.
- Validate inputs early with `[Parameter(Mandatory)]` or explicit checks.
- Print actionable errors: include what failed, expected values, and remediation hint.
- Avoid destructive actions without explicit confirmation flags (e.g. `-Force`, `-Confirm`).

## Idempotency & style

- Make scripts idempotent (safe to rerun without side effects).
- Use `Test-Path` before creating/deleting files or directories.
- Prefer PowerShell cmdlets over external commands (e.g. `Get-ChildItem` not `ls`).
- Use `PascalCase` for function names matching PowerShell conventions (`Invoke-Deploy`).
- Format long parameter lists vertically with splatting (`@params`).

## Output & automation

- Prefer structured output (`[PSCustomObject]`, `ConvertTo-Json`) for automation pipelines.
- For non-interactive modes, suppress progress bars: `$ProgressPreference = 'SilentlyContinue'`.
- For multiline CLI bodies (e.g. `gh issue comment --body`), use here-strings or `--body-file` to preserve real newlines.
- Include usage examples in a comment header or `Get-Help` documentation block.
- Lint with PSScriptAnalyzer in CI.

## Example: safe script skeleton

```powershell
#Requires -Version 7
<#
.SYNOPSIS
  Deploys a service to the target environment.
.PARAMETER Environment
  Target environment (dev|staging|prod).
.PARAMETER Version
  Semantic version to deploy.
.EXAMPLE
  .\Deploy-Service.ps1 -Environment staging -Version 1.2.3
#>
[CmdletBinding(SupportsShouldProcess)]
param(
  [Parameter(Mandatory)][ValidateSet('dev','staging','prod')][string]$Environment,
  [Parameter(Mandatory)][string]$Version
)
$ErrorActionPreference = 'Stop'

Write-Host "Deploying $Version to $Environment"
```

---

## 🏆 Elite Section — Top 5% PowerShell Practices

- **PSScriptAnalyzer as CI hard gate**: Run `Invoke-ScriptAnalyzer -Severity Error,Warning` on all `.ps1` files. Suppress rules inline with `[Diagnostics.CodeAnalysis.SuppressMessageAttribute]` and a rationale comment.
- **Pester 5 for all non-trivial scripts**: Write `Describe`/`It` tests for every function with side-effects. Mock external cmdlets with `Mock` to ensure unit tests never touch real infrastructure.
- **Module manifests for shared code**: Package reusable functions as a PowerShell module with a `.psd1` manifest. Export only what is needed; keep internals private.
- **`#Requires -Modules` for dependencies**: Declare required modules at the top of scripts; fail fast with a clear message if the module is missing rather than failing mid-execution.
- **Transcript logging for audit trails**: For automation scripts that make infrastructure changes, wrap the script body with `Start-Transcript`/`Stop-Transcript` and ship logs to a central store.
- **Secret retrieval via `SecretManagement`**: Use `Microsoft.PowerShell.SecretManagement` + a vault extension (e.g. `SecretManagement.Azure.KeyVault`) instead of reading secrets from environment variables directly.
