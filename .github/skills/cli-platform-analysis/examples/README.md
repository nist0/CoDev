# cli-platform-analysis -- Examples

## Example: Deduced CI/CD Pipeline section (from a real workflow scan)

After running Step 1 on a project with two workflow files:

```markdown
## CI/CD Pipeline

### ci.yml
- **Trigger**: `pull_request` (target: `main`), `push` (branch: `main`)
- **Jobs**: `build-and-test` -> `lint` -> `security-scan`
- **Build toolchain**: `dotnet restore --locked-mode`, `dotnet build -c Release -warnaserror`, `dotnet test -c Release --collect:"XPlat Code Coverage"`
- **Test gates**: Coverage uploaded to Codecov; no threshold enforced yet U+26A0U+FE0F (gap)
- **Lint**: `dotnet format --verify-no-changes`
- **Security**: `dotnet list package --vulnerable --include-transitive` -- fails on Critical/High
- **Artifact strategy**: None (CI only, no publish)
- **Secrets**: `CODECOV_TOKEN`
- **Action pin hygiene**: `actions/checkout` pinned to SHA U+2705; `codecov/codecov-action` uses `@v4` tag U+26A0U+FE0F (unpin risk)

### release.yml
- **Trigger**: Push of tag matching `v*.*.*`
- **Jobs**: `validate` -> `build-artifact` -> `publish` -> `smoke-test`
- **Artifact**: `dotnet publish -c Release -r win-x64 --self-contained`; packed as NuGet tool
- **Publish**: NuGet.org via `NUGET_API_KEY` secret; GitHub Release created with CHANGELOG section
- **Deployment**: None -- CLI is distributed as a NuGet tool, not deployed to Azure
- **Smoke test**: Installs the published NuGet tool in a clean environment; runs 3 CLI commands
- **Secrets**: `NUGET_API_KEY`, `GITHUB_TOKEN`
```

---

## Example: Deduced Infrastructure section (from a Bicep scan)

```markdown
## Infrastructure & Deployment Topology

**No Bicep or ARM files found.** The CLI is distributed as a NuGet tool -- no Azure resources are deployed by this repo.

Monitoring: Application Insights connection string is injected at runtime via environment variable `APPLICATIONINSIGHTS_CONNECTION_STRING` (referenced in `appsettings.json`). The Application Insights resource is managed externally (not in this repo).

Drift risk: None -- no cloud resources to track.
```

---

## Example: <=10-line summary output

```text
CI/CD toolchain   : dotnet publish -> NuGet tool -> NuGet.org + GitHub Releases
Deploy target     : None (CLI tool, no server deployment)
CLI framework     : System.CommandLine v2.0.0-beta4
Solution layers   : Entry (MyCli) -> Application (MyCli.Application) -> Domain (MyCli.Domain) -> Infrastructure (MyCli.Infrastructure)
Persistence       : EF Core 9 + SQLite (local config store)
Environments      : None (CLI tool; no environment separation in Bicep)
Test coverage     : Partial -- unit (good) + integration (limited) + smoke (3 flows)
Monitoring        : Application Insights (injected at runtime)
Top risk area     : No coverage threshold enforced in CI; smoke tests cover only 3 of 12 commands
Next action       : /cli-platform-task task="<your assigned task>"
```
