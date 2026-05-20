---
name: dotnet-cli
description: .NET CLI build/test/publish workflow -- reproducible CI commands, diagnostics, and artifact strategy.
argument-hint: "[project] [action]"
user-invocable: true

disable-model-invocation: false
---

# dotnet CLI (Build/Test/Publish) (Elite)

## When to use

- You need reliable dotnet commands for local dev and CI.

- You want a standard build/test/publish workflow.

## Workflow

1) Restore/build

   - `dotnet restore`

   - `dotnet build -c Release`
2) Test

   - `dotnet test -c Release --collect:"XPlat Code Coverage"` (optional)
3) Format/lint (if configured)

   - `dotnet format` (optional)
4) Publish

   - `dotnet publish -c Release -o out/`
5) Diagnostics

   - `dotnet --info`, `dotnet --list-sdks`

## Recommended command profiles

- **Fast local feedback**:

  - `dotnet restore`

  - `dotnet build`

  - `dotnet test --no-build`

- **CI deterministic build**:

  - `dotnet restore --locked-mode` (when lock file strategy is used)

  - `dotnet build -c Release --no-restore`

  - `dotnet test -c Release --no-build`

- **Packaging/publish**:

  - `dotnet publish -c Release --no-build -o out/`

## Troubleshooting quick checks

- SDK mismatch: `dotnet --info`, `dotnet --list-sdks`

- NuGet source/auth issues: `dotnet nuget list source`

- Build server stale cache: `dotnet nuget locals all --clear`

## Self-check

- [ ] `dotnet restore --locked-mode` used in CI (if lock file strategy enabled).

- [ ] `--no-restore` / `--no-build` flags used in CI to avoid redundant steps.

- [ ] SDK version pinned in `global.json`.

- [ ] Publish output produces a deterministic artifact.

## Outputs

- Standard command set for CI/local.

- Common troubleshooting commands.

- Publish artifact strategy.

## Microsoft references

- [.NET CLI overview](https://learn.microsoft.com/dotnet/core/tools/)

- [dotnet build](https://learn.microsoft.com/dotnet/core/tools/dotnet-build)

- [dotnet test](https://learn.microsoft.com/dotnet/core/tools/dotnet-test)

- [dotnet publish](https://learn.microsoft.com/dotnet/core/tools/dotnet-publish)
