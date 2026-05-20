---
name: rest-api-bootstrap
description: Bootstrap a REST API project from zero -- curated GitHub template repos, dotnet/pip/cookiecutter CLI commands, and quality snippet sources for C# (.NET), Python (FastAPI/Flask), and Bash (curl/jq client patterns).
argument-hint: "[stack: dotnet|python|bash] [style: minimal|clean-arch|full-stack]"
user-invocable: true

disable-model-invocation: false
---

# REST API Bootstrap (Elite)

## When to use

- Starting a new REST API project from scratch in C#, Python, or Bash.

- Choosing a quality GitHub template or scaffolding approach for a given stack.

- Looking for authoritative snippet sources and starter patterns.

- Want a ready-to-run first commit in < 5 minutes.

---

## C# / .NET

### Tier 1 -- Official scaffolding (zero dependencies)

```powershell
# Minimal API (recommended default, .NET 8+)
dotnet new webapi -n MyApi --use-minimal-apis
cd MyApi ; dotnet run

# Web API with controllers (MVC-style)
dotnet new webapi -n MyApi --no-https
```

> Use `dotnet new webapi --help` to see all options.

### Tier 1.5 -- Essential add-ons (layer on top of `dotnet new webapi`)

These four packages should be in virtually every real .NET 8+ REST API. Install them in one shot after scaffolding:

```powershell
dotnet add package FastEndpoints
dotnet add package Serilog.AspNetCore
dotnet add package ErrorOr
dotnet add package Scalar.AspNetCore
```

#### FastEndpoints -- endpoint classes for minimal APIs

Repo: <https://github.com/FastEndpoints/FastEndpoints>

Minimal APIs default to scattered lambda handlers. FastEndpoints replaces them with one strongly-typed class per endpoint, built-in FluentValidation, response mappers, and a test harness -- with zero performance overhead vs raw minimal APIs.

```csharp
// Program.cs
builder.Services.AddFastEndpoints();
app.UseFastEndpoints();

// Endpoints/CreateOrderEndpoint.cs
public class CreateOrderEndpoint : Endpoint<CreateOrderRequest, CreateOrderResponse>
{
    public override void Configure()
    {
        Post("/orders");
        AllowAnonymous();
    }

    public override async Task HandleAsync(CreateOrderRequest req, CancellationToken ct)
    {
        // req is already validated by FluentValidation
        await SendAsync(new CreateOrderResponse { Id = Guid.NewGuid() }, cancellation: ct);
    }
}

// Validators/CreateOrderValidator.cs
public class CreateOrderValidator : Validator<CreateOrderRequest>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.ProductId).NotEmpty();
        RuleFor(x => x.Quantity).GreaterThan(0);
    }
}
```

Prefer **Carter** (`dotnet add package Carter`) if you want a lighter module-grouping approach without FastEndpoints' full conventions:

```csharp
// Modules/OrdersModule.cs
public class OrdersModule : ICarterModule
{
    public void AddRoutes(IEndpointRouteBuilder app)
    {
        app.MapGet("/orders", () => Results.Ok());
        app.MapPost("/orders", (CreateOrderRequest req) => Results.Created("/orders/1", req));
    }
}
```

Repo: <https://github.com/CarterCommunity/Carter>

#### Serilog -- structured logging from day one

```powershell
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console   # human-readable dev output
dotnet add package Serilog.Sinks.Seq        # optional: local Seq dashboard
```

```csharp
// Program.cs -- replace default logging with Serilog in two lines
builder.Host.UseSerilog((ctx, lc) => lc
    .ReadFrom.Configuration(ctx.Configuration)
    .WriteTo.Console(outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}"));
```

```json
// appsettings.Development.json
{
  "Serilog": {
    "MinimumLevel": { "Default": "Debug", "Override": { "Microsoft": "Warning" } }
  }
}
```

Repo: <https://github.com/serilog/serilog-aspnetcore>

#### ErrorOr -- result type instead of exception-driven control flow

Repo: <https://github.com/amantinband/error-or>

```csharp
// Domain/OrderService.cs
public ErrorOr<Order> CreateOrder(CreateOrderRequest req)
{
    if (req.Quantity <= 0)
        return Error.Validation("quantity", "Quantity must be positive.");

    var order = new Order(Guid.NewGuid(), req.ProductId, req.Quantity);
    return order;
}

// Endpoint handler -- map ErrorOr<T> to IResult in one expression
public override async Task HandleAsync(CreateOrderRequest req, CancellationToken ct)
{
    ErrorOr<Order> result = _orderService.CreateOrder(req);

    await result.MatchAsync(
        order  => SendAsync(new CreateOrderResponse { Id = order.Id }, cancellation: ct),
        errors => SendErrorsAsync(cancellation: ct)
    );
}
```

#### Scalar -- modern OpenAPI UI (replaces Swashbuckle)

Repo: <https://github.com/scalar/scalar>

Microsoft now ships OpenAPI support natively in .NET 9 with Scalar as the recommended UI. For .NET 8, add it explicitly:

```csharp
// Program.cs
builder.Services.AddOpenApi(); // built-in .NET 8 OpenAPI document generation

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();                  // -> /openapi/v1.json
    app.MapScalarApiReference();       // -> /scalar/v1  (interactive UI)
}
```

Docs: <https://scalar.com/blog/scalar-for-dotnet>

#### Full `Program.cs` combining all four

```csharp
using FastEndpoints;
using Scalar.AspNetCore;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((ctx, lc) => lc
    .ReadFrom.Configuration(ctx.Configuration)
    .WriteTo.Console());

builder.Services.AddOpenApi();
builder.Services.AddFastEndpoints();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.UseHttpsRedirection();
app.UseFastEndpoints();

app.Run();
```

> **Decision**: use **FastEndpoints** when endpoints multiply beyond 5-6 (prevents lambda sprawl). Use **Carter** when you prefer a thin module-grouping convention without committing to FastEndpoints' full plugin system.

### Tier 1.5 -- Package scoring table

Scores 1-5. **My recommended combination is marked U+2605**.

#### Individual packages

| Package | DX | Perf | Maintainability | Learning curve | Community | Copilot-friendliness | Total /30 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **FastEndpoints** | 5 | 5 | 5 | 3 | 4 | 5 | **27** |
| **FastEndpoints.Security** | 5 | 5 | 5 | 3 | 4 | 5 | **27** |
| **Carter** | 4 | 5 | 4 | 5 | 3 | 4 | **25** |
| **Serilog.AspNetCore** | 5 | 4 | 5 | 4 | 5 | 5 | **28** |
| **ErrorOr** | 5 | 5 | 5 | 3 | 4 | 5 | **27** |
| **FluentResults** | 4 | 5 | 4 | 4 | 4 | 4 | **25** |
| **Scalar.AspNetCore** | 5 | 5 | 5 | 5 | 4 | 5 | **29** |
| **MediatR** | 3 | 4 | 5 | 3 | 5 | 4 | **24** |
| **Scrutor** | 4 | 5 | 4 | 4 | 3 | 4 | **24** |

> **Scoring criteria:**
>
> - **DX** -- how much boilerplate it eliminates, how quick to be productive.
> - **Perf** -- runtime overhead (5 = zero overhead; 1 = measurable cost at scale).
> - **Maintainability** -- consistency enforced across team, refactor safety.
> - **Learning curve** -- 5 = pick up in < 1 hour; 1 = requires dedicated study.
> - **Community** -- GitHub stars trajectory, NuGet downloads, activity, issues response time.
> - **Copilot-friendliness** -- how well Copilot autocompletes and understands the pattern (popular packages with clear conventions score higher).

#### Curated combinations

| Stack | Packages | Total /30 | When to pick |
| --- | --- | --- | --- |
| U+2605 **Elite minimal** (recommended) | FastEndpoints + FastEndpoints.Security + Serilog + ErrorOr + Scalar | **27.75 avg** | Solo dev or small team; real project with > 5 endpoints; want structure without CQRS overhead |
| **CQRS heavy** | MediatR + Serilog + ErrorOr + Scalar + Scrutor | **26.4 avg** | Large team; DDD; commands/events are first-class concerns |
| **Thin & fast** | Carter + Serilog + FluentResults + Scalar | **26.75 avg** | Microservice / sidecar; minimal surface area; < 10 endpoints |
| **Vanilla + logging** | `dotnet new webapi` + Serilog + Scalar | **28.5 avg** | Tutorial, spike, or prototype; need zero external conventions |
| **Full Clean Arch** | Jason Taylor template (includes MediatR + FV + EF + xUnit) | N/A | Multi-dev project; long-lived product; onboarding structured teams |

#### U+2605 My recommendation -- Elite minimal stack

```powershell
dotnet new webapi -n MyApi --use-minimal-apis
cd MyApi
dotnet add package FastEndpoints
dotnet add package FastEndpoints.Swagger        # integrates Scalar + OpenAPI into FE pipeline
dotnet add package FastEndpoints.Security       # JWT bearer + cookie auth, roles, permissions
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package ErrorOr
```

Minimal JWT wiring (`FastEndpoints.Security`):

```csharp
// Program.cs
builder.Services.AddAuthenticationJwtBearer(s => s.SigningKey = builder.Configuration["Jwt:Key"]!);
builder.Services.AddAuthorization();

// In app pipeline (after UseFastEndpoints)
app.UseAuthentication();
app.UseAuthorization();

// Endpoint -- require authenticated user
public override void Configure()
{
    Post("/orders");
    // AllowAnonymous(); <- remove this line
}
```

> **Security note (from specialist review):** authentication is not a bolt-on. Wire `FastEndpoints.Security` in the same sprint as the scaffold -- never leave endpoints open by default.

**Why this wins:**

1. **FastEndpoints** eliminates the #1 pain point of minimal APIs (lambda sprawl) while matching raw ASP.NET Core throughput in benchmarks (TechEmpower Round 22).

2. **`FastEndpoints.Swagger`** sub-package wires Scalar + OpenAPI doc generation automatically -- no separate `AddOpenApi()` plumbing needed.

3. **`FastEndpoints.Security`** adds JWT bearer + cookie auth + fine-grained permissions in < 5 lines -- no manual `AddAuthentication().AddJwtBearer()` ceremony.

4. **Serilog** is the de-facto standard (.NET ecosystem, 500M+ NuGet downloads); every sink you'll ever need exists.

5. **ErrorOr** keeps domain errors as typed values -- `ErrorOr<T>` maps to `SendErrorsAsync()` in FastEndpoints and to `Results.Problem()` in vanilla APIs without any infrastructure code.

6. The whole stack takes < 10 minutes to wire and generates code that Copilot autocompletes accurately and consistently.

**When to drop this and go Clean Architecture instead:** your domain has > 3 bounded contexts, you have > 3 developers, or you need event sourcing / domain events -- at that point, the CQRS heavy stack wins on long-term maintainability.

### Tier 2 -- .NET Aspire (cloud-native / distributed)

```powershell
dotnet workload install aspire
dotnet new aspire-starter -n MyApp
```

- Repo: <https://github.com/dotnet/aspire>

- Samples: <https://github.com/dotnet/aspire-samples>

- Best for: multi-service setups requiring service discovery, health dashboards, and OpenTelemetry out of the box.

### Tier 3 -- Community Clean Architecture templates

| Template | GitHub | Install | Best for |
| --- | --- | --- | --- |
| **Jason Taylor -- Clean Architecture** | <https://github.com/jasontaylordev/CleanArchitecture> | `dotnet new install Clean.Architecture.Solution.Template` | Full-stack (Angular/React + API): CQRS, MediatR, FluentValidation, EF Core, Identity, xUnit |
| **Ardalis -- Clean Architecture** | <https://github.com/ardalis/CleanArchitecture> | `dotnet new install Ardalis.CleanArchitecture.Template` | API-only: DDD-friendly, minimal external dependencies |
| **eShopOnWeb** (Microsoft reference) | <https://github.com/dotnet-architecture/eShopOnWeb> | Clone | Comprehensive reference: Razor Pages + API, Domain-Driven Design, tested by Microsoft |

```powershell
# Jason Taylor (most popular community template)
dotnet new install Clean.Architecture.Solution.Template
dotnet new ca-sln -n MyApi
```

### Quality snippet sources (C#)

| Source | URL | Notes |
| --- | --- | --- |
| Microsoft -- ASP.NET Core docs examples | <https://github.com/dotnet/AspNetCore.Docs> | Official, versioned per .NET release |
| Minimal API samples | <https://github.com/martincostello/aspnetcore-openapi> | OpenAPI 3.1 with .NET 9 minimal APIs |
| awesome-dotnet (curated list) | <https://github.com/quozd/awesome-dotnet> | Community-maintained link registry |

### Decision matrix

| Scenario | Recommended approach |
| --- | --- |
| Quick prototype / microservice | `dotnet new webapi --use-minimal-apis` |
| Long-lived API with CQRS | Jason Taylor Clean Architecture |
| Domain-model-heavy, DDD | Ardalis Clean Architecture |
| Multi-service dashboard + traces | .NET Aspire |
| Corporate reference / study | eShopOnWeb |

---

## Python

### Tier 1 -- FastAPI (recommended default)

```bash
pip install fastapi uvicorn[standard]

# main.py -- production-ready skeleton in 25 lines
cat > main.py << 'EOF'
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown

app = FastAPI(title="My API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
EOF

uvicorn main:app --reload
```

### Tier 2 -- FastAPI full-stack template (batteries included)

| Template | GitHub | Notes |
| --- | --- | --- |
| **FastAPI Full Stack** (official) | <https://github.com/fastapi/full-stack-fastapi-template> | React + FastAPI + PostgreSQL + SQLModel + Alembic + Docker Compose; maintained by Tiangolo |
| **FastAPI Best Practices** | <https://github.com/zhanymkanov/fastapi-best-practices> | Community opinionated guide + patterns repo |
| **fastapi-starter** | <https://github.com/arthurhenrique/cookiecutter-fastapi> | Cookiecutter template with Docker, Pytest, pre-commit |

```bash
# FastAPI official full-stack template (requires cookiecutter)
pip install cookiecutter
cookiecutter https://github.com/fastapi/full-stack-fastapi-template
```

### Tier 3 -- Flask (lightweight)

```bash
pip install flask flask-smorest marshmallow

# Minimal Flask REST app
python -c "
from flask import Flask, jsonify
app = Flask(__name__)

@app.get('/health')
def health():
    return jsonify(status='ok')

app.run(debug=True)
"
```

| Template | GitHub | Notes |
| --- | --- | --- |
| **cookiecutter-flask-restful** | <https://github.com/karec/cookiecutter-flask-restful> | JWT, SQLAlchemy, Marshmallow, Celery, Docker |
| **Flask Smorest** skeleton | <https://flask-smorest.readthedocs.io/en/latest/> | OpenAPI 3 spec driven, recommended for schema-first Flask |

### Quality snippet sources (Python)

| Source | URL | Notes |
| --- | --- | --- |
| FastAPI docs examples | <https://github.com/fastapi/fastapi/tree/master/docs_src> | Canonical, tested against each release |
| Real Python -- FastAPI tutorial | <https://realpython.com/fastapi-python-web-apis/> | Step-by-step practical guide |
| awesome-fastapi | <https://github.com/mjhea0/awesome-fastapi> | Curated plugin and template list |

### Decision matrix -- Python

| Scenario | Recommended approach |
| --- | --- |
| New project, async, performance matters | FastAPI + `dotenv` + `uvicorn` |
| Full-stack one-command start | `full-stack-fastapi-template` cookiecutter |
| Existing Flask codebase | Flask + flask-smorest |
| Microservice / event-driven | FastAPI + Pydantic v2 |

---

## Bash -- REST client patterns

> Bash does not serve REST APIs. This section covers **bash scripts that consume REST APIs** via `curl` + `jq`, and bash bootstrap scripts that scaffold other projects.

### Core snippets

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${API_BASE_URL:?env var required}"
TOKEN="${API_TOKEN:?env var required}"

# GET with JSON response
get_resource() {
  local path="$1"
  curl --silent --fail \
    --header "Authorization: Bearer ${TOKEN}" \
    --header "Accept: application/json" \
    "${BASE_URL}${path}" | jq .
}

# POST with JSON body
create_resource() {
  local path="$1" payload="$2"
  curl --silent --fail \
    --request POST \
    --header "Authorization: Bearer ${TOKEN}" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" \
    --data "${payload}" \
    "${BASE_URL}${path}" | jq .
}

# PUT
update_resource() {
  local path="$1" payload="$2"
  curl --silent --fail \
    --request PUT \
    --header "Authorization: Bearer ${TOKEN}" \
    --header "Content-Type: application/json" \
    --data "${payload}" \
    "${BASE_URL}${path}" | jq .
}

# DELETE
delete_resource() {
  local path="$1"
  curl --silent --fail \
    --request DELETE \
    --header "Authorization: Bearer ${TOKEN}" \
    "${BASE_URL}${path}"
  echo "Deleted: ${path}"
}

# PATCH
patch_resource() {
  local path="$1" payload="$2"
  curl --silent --fail \
    --request PATCH \
    --header "Authorization: Bearer ${TOKEN}" \
    --header "Content-Type: application/json" \
    --data "${payload}" \
    "${BASE_URL}${path}" | jq .
}
```

### Pagination pattern (offset / cursor)

```bash
# Fetch all pages (offset-based)
fetch_all_pages() {
  local path="$1"
  local page=1 per_page=100 has_more=true
  while $has_more; do
    response=$(curl --silent --fail \
      --header "Authorization: Bearer ${TOKEN}" \
      "${BASE_URL}${path}?page=${page}&per_page=${per_page}")
    echo "${response}" | jq '.items[]'
    count=$(echo "${response}" | jq '.items | length')
    [[ "$count" -lt "$per_page" ]] && has_more=false || ((page++))
  done
}
```

### Error handling wrapper

```bash
# Treat non-2xx as fatal; print error body
safe_curl() {
  local http_code body
  body=$(curl --silent --write-out "\n%{http_code}" "$@")
  http_code=$(echo "${body}" | tail -n1)
  body=$(echo "${body}" | sed '$d')
  if [[ "${http_code}" -lt 200 || "${http_code}" -ge 300 ]]; then
    echo "HTTP error ${http_code}: ${body}" >&2
    exit 1
  fi
  echo "${body}"
}
```

### Quality snippet sources (Bash)

| Source | URL | Notes |
| --- | --- | --- |
| **hurl** (HTTP testing DSL) | <https://github.com/Orange-OpenSource/hurl> | Declarative HTTP tests in plain text; alternative to curl chaining |
| **xh** (httpie in Rust) | <https://github.com/ducaale/xh> | Fast `curl` replacement with friendly output |
| **navi** cheats | <https://github.com/denisidoro/navi> | TUI cheat-sheet tool; curate curl snippets |
| **awesome-shell** API clients section | <https://github.com/alebcay/awesome-shell> | Curated shell tools inventory |

### Bash scaffold helper (generate project structure)

```bash
#!/usr/bin/env bash
# Usage: bootstrap-api.sh dotnet MyApi | bootstrap-api.sh python myapi | bootstrap-api.sh fastapi myapp
set -euo pipefail

stack="${1:?first arg: dotnet|python|fastapi}"
name="${2:?second arg: project name}"

case "${stack}" in
  dotnet)
    dotnet new webapi -n "${name}" --use-minimal-apis
    cd "${name}"
    dotnet add package Swashbuckle.AspNetCore
    echo "U+2705  ${name} (dotnet minimal API) ready -- run: dotnet run"
    ;;
  python|fastapi)
    python -m venv "${name}/.venv"
    # shellcheck disable=SC1090
    source "${name}/.venv/bin/activate"
    pip install --quiet fastapi uvicorn[standard] pydantic-settings
    echo "from fastapi import FastAPI; app = FastAPI()" > "${name}/main.py"
    echo "U+2705  ${name} (FastAPI) ready -- run: uvicorn main:app --reload"
    ;;
  *)
    echo "Unknown stack: ${stack}" >&2; exit 1 ;;
esac
```

---

## Self-check

- [ ] Chosen template has an active maintainer (commits within 6 months).

- [ ] Template is pinned to a compatible language/framework version.

- [ ] Secrets and credentials are injected via env vars, not hardcoded.

- [ ] OpenAPI/Swagger is available out of the box or added immediately.

- [ ] A health endpoint (`/health` or `/healthz`) is included.

- [ ] Tests pass on a fresh clone (`dotnet test` / `pytest` / `bats`).

## Outputs

- **Chosen template URL + clone/install command** for the selected stack.

- **First-run commands** to confirm the API is live.

- **Decision rationale** (one sentence: why this template over alternatives).
