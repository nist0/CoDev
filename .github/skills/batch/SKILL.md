---
name: batch
description: Windows batch/CMD scripting -- safe patterns, error handling, and migration guidance. Prefer PowerShell for complex logic.
argument-hint: "[script-name or automation goal]"
user-invocable: true

disable-model-invocation: false
---

# Batch / CMD Scripting (Elite)

## When to use

- Writing Windows batch scripts for legacy automation or bootstrap tasks.

- Maintaining existing `.bat`/`.cmd` scripts.

- **Prefer PowerShell for any complex logic** (loops, error handling, parsing).

## Safe Skeleton

```batch
@echo off
setlocal EnableDelayedExpansion

if "%~1"=="" (
    echo Usage: script.bat ^<arg^>
    exit /b 1
)

rem Main logic here

endlocal
exit /b 0
```

## Workflow

### 1. Headers and isolation

- Always start with `@echo off` and `setlocal`.

- Use `setlocal EnableDelayedExpansion` only if `!var!` syntax needed.

### 2. Input validation

- Check required parameters with `if "%~1"==""`.

- Validate paths exist with `if not exist`.

### 3. Error propagation

- Check `%errorlevel%` or `if errorlevel 1` after each critical command.

- Use `exit /b <code>` instead of `exit` to avoid closing the parent shell.

### 4. Prefer PowerShell for complex logic

- String manipulation, JSON, REST APIs, complex conditionals -> use PowerShell.

- Batch scripts: bootstrap/launch/legacy only.

### 5. Test on target environment

- Run on the exact Windows version and context (32/64-bit cmd, UAC level).

## Self-check

- [ ] Starts with `@echo off` + `setlocal`.

- [ ] Inputs validated before use.

- [ ] Error codes checked after critical operations.

- [ ] `exit /b` used (not bare `exit`).

- [ ] Complex logic offloaded to PowerShell.

## Outputs

- Script skeleton (copy/paste-ready).

- Common patterns (error exit, variable handling).

- Usage examples.
