#!/usr/bin/env pwsh
<#
.SYNOPSIS
    CoDev submodule bootstrap — PowerShell wrapper.

.DESCRIPTION
    Delegates to codev.py in the same directory. Requires Python 3.9+.
    On Windows, also detects Developer Mode and warns if symlinks are unavailable.

.EXAMPLE
    .\codev.ps1 init
    .\codev.ps1 init --strategy override --overrides-dir my-overrides
    .\codev.ps1 update
    .\codev.ps1 teardown
    .\codev.ps1 teardown --force
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0, Mandatory)]
    [ValidateSet('init', 'update', 'teardown')]
    [string]$Command,

    [Parameter(ValueFromRemainingArguments)]
    [string[]]$Rest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Locate codev.py relative to this script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CoDev = Join-Path $ScriptDir 'codev.py'

if (-not (Test-Path $CoDev)) {
    Write-Error "codev.py not found at: $CoDev"
    exit 2
}

# Prefer .venv python if present in the CoDev submodule
$VenvPython = Join-Path $ScriptDir '.venv\Scripts\python.exe'
$Python = if (Test-Path $VenvPython) { $VenvPython } else { 'python' }

# Windows Developer Mode advisory (init only)
if ($Command -eq 'init') {
    $DevMode = $false
    try {
        $RegVal = Get-ItemProperty `
            'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock' `
            -ErrorAction SilentlyContinue
        $DevMode = ($RegVal.AllowDevelopmentWithoutDevLicense -eq 1)
    } catch { }

    if (-not $DevMode) {
        Write-Warning 'Windows Developer Mode is not enabled.'
        Write-Warning 'CoDev will use lockfile mode (file copy) instead of symlinks.'
        Write-Warning 'To enable symlink mode: Settings > System > For developers > Developer Mode.'
        Write-Warning ''
    }
}

& $Python $CoDev $Command @Rest
exit $LASTEXITCODE
