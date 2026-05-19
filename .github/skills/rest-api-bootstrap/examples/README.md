# REST API Bootstrap Skill — Examples

## 1. Scaffold a .NET Web API

```sh
dotnet new webapi -n MyApi
```

## 2. Scaffold a FastAPI Project (Python)

```text
pip install fastapi uvicorn
mkdir myapi && cd myapi
fastapi --help
```

## 3. Cookiecutter Template

```sh
cookiecutter gh:tiangolo/full-stack-fastapi-postgresql
```

## Example 1 — Bootstrap a .NET minimal API

**Input**

```text
/rest-api-bootstrap dotnet minimal
```

**Output**

```powershell
dotnet new webapi -n OrdersApi --use-minimal-apis
cd OrdersApi
dotnet run
# → http://localhost:5000/swagger
```

## Template used: `dotnet new webapi` (official, zero external dependencies)

## Example 1b — Apply Tier 1.5 enhancements to a fresh minimal API

```text
dotnet new webapi -n OrdersApi --use-minimal-apis
cd OrdersApi
## Add the four essential packages
dotnet add package FastEndpoints
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package ErrorOr
dotnet add package Scalar.AspNetCore
dotnet run
## → http://localhost:5000/scalar/v1  (Scalar UI, replaces Swagger)
```

## Use-case: real project (> 5 endpoints) where you want structured logging, result types, organized endpoint classes, and a modern API explorer from day one

## Example 2 — Bootstrap a FastAPI full-stack project

**Input**

```text
/rest-api-bootstrap python full-stack
```

**Output**

```text
pip install cookiecutter
cookiecutter <https://github.com/fastapi/full-stack-fastapi-template>
## → prompts for project name, domain, etc.
docker compose up -d
## → http://localhost/docs (Swagger UI)
```

## Template used: `fastapi/full-stack-fastapi-template` (React + FastAPI + PostgreSQL + Docker Compose)

## Example 3 — Bootstrap Clean Architecture .NET API

**Input**

```text
/rest-api-bootstrap dotnet clean-arch
```

**Output**

```text
dotnet new install Clean.Architecture.Solution.Template
dotnet new ca-sln -n Ecom
cd Ecom
dotnet build
dotnet test
## All tests pass on fresh clone
dotnet run --project src/Web
## → http://localhost:5000/swagger
```

## Template used: `jasontaylordev/CleanArchitecture` — CQRS, MediatR, FluentValidation, EF Core, xUnit

## Example 4 — Bash REST client for an API key-secured endpoint

**Input**

```text
/rest-api-bootstrap bash client
```

**Output**

```text
#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${API_BASE_URL:?}"
TOKEN="${API_TOKEN:?}"
curl --silent --fail \
--header "Authorization: Bearer ${TOKEN}" \
--header "Accept: application/json" \
"${BASE_URL}/orders" | jq '.[] | {id, status}'
```

## Shell tools recommended: `curl`, `jq`, optionally `xh` or `hurl` for assertion-based testing

## Example 5 — Bootstrap helper script (multi-stack)

```bash
bash bootstrap-api.sh dotnet MyApi
# → dotnet minimal API scaffold, runs immediately
bash bootstrap-api.sh fastapi myapp
# → FastAPI venv + uvicorn ready to run
```

See the `bootstrap-api.sh` snippet in `SKILL.md` → Bash section for the full script.
