---
name: cli-platform-analysis
description: Full static analysis of a .NET CLI platform project — GH workflow files, Bicep/ARM/Terraform infra, solution structure, CLI surface, test projects, and existing docs — producing docs/project-context.md as the living context document for all subsequent task prompts.
argument-hint: "[repo-root: .] [output: docs/project-context.md]"
user-invocable: true
disable-model-invocation: false
---

# CLI Platform Analysis (Full Static Analysis) (Elite)

## When to use

- CoDev bootstrap is verified (`validate-route-smoke.py` passed).
- You are starting work on the CLI platform project for the first time.
- `docs/project-context.md` does not yet exist or is stale (older than one sprint).
- A major architectural change, new workflow, or new Bicep resource has been merged.

## Procedure

Run each step in order. Combine all outputs into a single `docs/project-context.md` file.

---

### Step 1 — GitHub Workflow Analysis

**Goal**: Deduce the CI/CD pipeline shape, toolchain, quality gates, and deployment targets entirely from static file reading — no running commands.

For each file in `.github/workflows/`:

| Field | What to extract |
|---|---|
| Filename | The workflow file name |
| Trigger | `on:` — push branches, PR targets, tag pattern, schedule, manual dispatch |
| Jobs | Job names, `needs:` dependencies, runner labels |
| Build toolchain | `dotnet restore`, `dotnet build`, `dotnet publish`, NuGet pack/push |
| Test gates | `dotnet test`, coverage upload, test result publishing, threshold enforcement |
| Lint / format | `dotnet format --verify-no-changes`, EditorConfig checks |
| Security gates | `dotnet list package --vulnerable`, SAST tools, secret scanning |
| Artifact strategy | What is built, how it is signed (Cosign, NuGet signature), where published (NuGet.org, GitHub Packages, GitHub Releases) |
| Deployment steps | `az deployment` (Bicep), AKS deploy, Azure CLI commands, environment names (`environment:`) |
| Secrets referenced | Names of secrets used in `${{ secrets.* }}` — **names only, never values** |
| Action pin hygiene | Whether third-party actions are pinned to SHA (security posture signal) |

**Output section**: `## CI/CD Pipeline` in `docs/project-context.md`.

---

### Step 2 — Infrastructure Analysis (Bicep / ARM / Terraform)

**Goal**: Deduce the deployment topology — what Azure resources exist, in which environments, and how they relate.

For each `*.bicep`, `*.json` (ARM template), `*.tf`, or `*.tfvars` file found anywhere in the repo:

| Field | What to extract |
|---|---|
| Resource types | e.g. `Microsoft.Web/sites`, `Microsoft.ApiManagement/service`, `Microsoft.Insights/components` |
| Environments | Parameter files per environment (`*.dev.bicepparam`, `*.staging.bicepparam`, `*.prod.bicepparam`) |
| Networking | VNets, subnets, private endpoints, DNS zones, NSG rules |
| Identity | Managed identities, role assignments (`roleDefinitionId`), federated credentials |
| Monitoring | Diagnostic settings, Log Analytics workspace, Application Insights connection |
| Key Vault | Referenced secrets (names only) and access policies |
| Deployment trigger | Called from a workflow step, manually via `az deployment`, or via pipeline release stage |
| Drift risk | Resources referenced in workflows but not found in Bicep files (flag as untracked) |

**Output section**: `## Infrastructure & Deployment Topology` in `docs/project-context.md`.

---

### Step 3 — Solution Structure Analysis

**Goal**: Map the .NET solution — projects, layers, CLI framework, DI patterns, persistence.

1. Read the `.sln` file — list all projects and their paths.
2. For each `.csproj`, classify the layer role:

| Layer | Indicators |
|---|---|
| CLI entry point | References `System.CommandLine`, `Spectre.Console`, `CliFx`; contains `Program.cs` with `RootCommand` or `CommandApp` |
| Application | Contains commands/handlers (`ICommandHandler`, `IRequestHandler`); references MediatR |
| Domain | Pure C# classes; no framework references; entities, value objects, domain events |
| Infrastructure | References EF Core, HTTP clients, Azure SDK, file system, NuGet packages for external services |
| Test | Project name ends in `.Tests`, `.IntegrationTests`, `.E2E`, `.Smoke` |

1. Identify CLI framework (`System.CommandLine` / `Spectre.Console` / `CliFx` / custom) from `<PackageReference>` entries.
1. Identify DI registration pattern: `builder.Services.AddXxx()` patterns in `Program.cs` or extension methods.
1. Identify persistence layer: EF Core (`DbContext`), Dapper, raw ADO.NET, or none.
1. Identify any OpenAPI / HTTP client generation: Kiota, NSwag, Refit, HttpClientFactory patterns.
1. Note any `Directory.Build.props` or `Directory.Packages.props` — these control global settings.

**Output section**: `## Solution Structure` in `docs/project-context.md`.

---

### Step 4 — CLI Surface Analysis

**Goal**: Catalog every command, its handler, domain action, and side-effects.

For each top-level command and subcommand (read from handler classes, command definitions, or README):

| Command | Syntax | Handler class | Domain action | Models touched | Validation rules | Side-effects |
|---|---|---|---|---|---|---|

Side-effects include: REST API calls, file writes, service registrations, event publishing, monitoring hooks, subscription creation.

Note any naming convention inconsistencies (e.g. mixed `verb-noun` and `noun verb` patterns) — flag as UX debt.

**Output section**: `## CLI Surface` in `docs/project-context.md`.

---

### Step 5 — Test Infrastructure Analysis

**Goal**: Understand what is tested today and what is not — to avoid CI failures when adding new code.

| Layer | Test project(s) | Framework | Coverage areas | Gaps identified |
|---|---|---|---|---|
| Unit | | xUnit / NUnit / MSTest | | |
| Integration | | xUnit + WebApplicationFactory / Testcontainers | | |
| E2E / Smoke | | CLI binary invocation / Playwright / Bruno | | |
| Contract | | Pact / OpenAPI assertions | | |

Additionally note:

- Whether CI runs all test layers or only a subset.
- Whether code coverage is measured and what the current threshold is.
- Whether test data is managed via builders/fixtures or magic strings.

**Output section**: `## Test Infrastructure` in `docs/project-context.md`.

---

### Step 6 — Existing Docs Analysis

**Goal**: Inventory existing documentation to avoid duplication and identify gaps.

| File / path | Type | Currency (current / stale / missing) |
|---|---|---|
| `README.md` | Project overview | |
| `docs/` contents | Any existing docs | |
| `CHANGELOG` / `CHANGELOG.md` | Release history | |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR workflow | |
| `docs/architecture/` | ADRs, module maps | |

**Output section**: `## Documentation Inventory` in `docs/project-context.md`.

---

### Step 7 — Produce `docs/project-context.md`

Combine all sections into a single file using this canonical structure:

```markdown
# Project Context — <project-name>

> Generated: <date> | Branch: <branch> | Refresh cadence: every sprint or after major merges.
> Re-run `/cli-platform-analyze` if any section is stale.

## CI/CD Pipeline
<!-- Populated by Step 1 -->

## Infrastructure & Deployment Topology
<!-- Populated by Step 2 -->

## Solution Structure
<!-- Populated by Step 3 -->

## CLI Surface
<!-- Populated by Step 4 -->

## Test Infrastructure
<!-- Populated by Step 5 -->

## Documentation Inventory
<!-- Populated by Step 6 -->

## Deduced Task Patterns

| Task category | Files to touch | Risk areas | Verification |
|---|---|---|---|
| Add new CLI command | Handler, DI registration, test | Breaking existing commands | `dotnet test` |
| Add API provider type | Extension point, factory, DI, test | Registration conflict | `dotnet test` |
| Add subscription hook | Event interface, DI wiring, test | Event ordering | integration test |
| Add monitor integration | Pipeline behavior / decorator, test | Perf regression | load test baseline |
| Update CI pipeline | `.github/workflows/*.yml` | Breaking CI for all PRs | Dry-run on branch |
| Update Bicep infra | `*.bicep` + parameter files | Deployment drift | `bicep build --lint` |
| Update NuGet publish | Release workflow, `*.csproj` version | Broken package consumers | smoke test install |
```

After committing `docs/project-context.md`, present a ≤10-line summary:

```text
CI/CD toolchain   : <dotnet publish → NuGet push | binary → GitHub Releases | ...>
Deploy target     : <Azure App Service | AKS | none detected>
CLI framework     : <System.CommandLine | Spectre.Console | ...>
Solution layers   : <Entry → Application → Domain → Infrastructure>
Persistence       : <EF Core + PostgreSQL | none | ...>
Environments      : <dev / staging / prod | only prod detected | ...>
Test coverage     : <good (unit + integration + E2E) | partial | minimal>
Monitoring        : <Application Insights | custom | none detected>
Top risk area     : <identified from Steps 1–6>
Next action       : /cli-platform-task task="<your assigned task>"
```

## Self-check

- [ ] All 7 steps completed; no section is empty or contains only placeholder text.
- [ ] CLI Surface table has at least one row per top-level command.
- [ ] Test Infrastructure section explicitly identifies coverage gaps (not just what exists).
- [ ] CI/CD Pipeline section identifies all secrets by name and all deployment targets by environment.
- [ ] Infrastructure section identifies all environments and flags any drift (resources in workflows but not in Bicep).
- [ ] `docs/project-context.md` committed to the repo on the current branch.
- [ ] ≤10-line summary presented for team review.

## Refresh cadence

| Trigger | Steps to re-run |
|---|---|
| New or modified `.github/workflows/` file | Step 1 only |
| New or modified Bicep / ARM / Terraform file | Step 2 only |
| New project added to solution or layer refactor | Steps 3 + 4 |
| New test project or coverage threshold change | Step 5 only |
| New docs added | Step 6 only |
| Sprint start (routine) | Diff `docs/project-context.md` vs repo state; update changed sections only |

## 🏆 Elite Section

- **Workflow secret audit**: While scanning workflows, flag any secret referenced in `${{ secrets.* }}` that is not documented in a secrets inventory (e.g. a `docs/secrets-inventory.md`). Open a GitHub issue for each undocumented secret — undocumented secrets are a rotation and rotation-failure risk.
- **Bicep drift detection**: After Step 2, cross-reference resource types found in Bicep files against `az resource list -g <rg> -o table` (if you have read access). Resources in Azure but not in Bicep are unmanaged — flag each as a drift issue.
- **Test gap → issue**: For each coverage gap identified in Step 5, open a GitHub issue tagged `area:testing` before starting the first task. Tracking gaps publicly prevents them from being forgotten across sprint boundaries.
- **CLI surface naming audit**: If Step 4 reveals mixed naming conventions across commands, open a UX debt issue before adding any new commands. A consistent naming convention is much cheaper to establish before the surface grows.
- **Action pin audit**: If Step 1 reveals unpinned third-party actions (using mutable tags like `@v3` instead of full SHA), open a security issue for each unpinned action — this is a supply-chain risk.
