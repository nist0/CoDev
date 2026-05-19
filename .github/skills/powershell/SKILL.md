---
name: powershell
description: PowerShell automation — error handling, param validation, idempotency, WhatIf support, and PSScriptAnalyzer.
argument-hint: "[script-purpose] [inputs]"
user-invocable: true

## disable-model-invocation: false

# PowerShell Automation (Elite)

## When to use

- Writing PowerShell scripts for Windows automation, Azure CLI wrappers, or CI steps.

## Procedure

### 1. Safety defaults (always)

```powershell
#Requires -Version 5.1
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)]
    [string]$InputParam
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
```

### 2. Input validation

```powershell
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Name,

    [ValidateSet('dev', 'staging', 'prod')]
    [string]$Environment = 'dev'
)
```

### 3. Idempotency

- Scripts must be safe to run multiple times without side effects.

- Check preconditions before acting:

```powershell
if (-not (Test-Path $TargetPath)) {
    New-Item -Path $TargetPath -ItemType Directory
}
```

### 4. WhatIf support for destructive operations

```powershell
if ($PSCmdlet.ShouldProcess($Target, 'Delete')) {
    Remove-Item $Target -Recurse -Force
}
```

### 5. Structured output (not Write-Host for data)

```powershell
# For data: output objects
[PSCustomObject]@{ Name = $Name; Status = 'OK' }

# For progress/info: Write-Verbose or Write-Information
Write-Verbose "Processing $Name"
```

### 6. PSScriptAnalyzer

```powershell
Install-Module PSScriptAnalyzer -Scope CurrentUser
Invoke-ScriptAnalyzer -Path .\script.ps1 -Severity Warning,Error
```

Fix all `Error` and `Warning` severity findings before committing.

## Self-check

- [ ] `$ErrorActionPreference = 'Stop'` and `Set-StrictMode -Version Latest` set.

- [ ] All inputs in `param()` block with validation attributes.

- [ ] Script is idempotent (safe to run multiple times).

- [ ] Destructive operations gated with `SupportsShouldProcess` / `ShouldProcess`.

- [ ] Output is structured objects (not raw `Write-Host` for data).

- [ ] `PSScriptAnalyzer` passes with no Error or Warning severity.

## Outputs

- Script skeleton with param block and safety defaults.

- Common patterns (retry, confirm prompt, structured output).

- PSScriptAnalyzer integration CI snippet.
