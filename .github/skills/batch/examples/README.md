# Batch Skill — Examples

## 1. Safe Batch Script Skeleton

```bat
@echo off
setlocal enabledelayedexpansion
REM Main logic
set VAR=Hello
if "%VAR%"=="Hello" echo World
```

## 2. Lint Batch Script (with batchlint)

```text
batchlint my_script.bat
```

## 3. Migrate to PowerShell (Python script)

```sh
python tools/migrate-to-powershell.py my_script.bat
```
