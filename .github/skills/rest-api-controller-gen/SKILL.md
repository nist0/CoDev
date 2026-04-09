---
name: rest-api-controller-gen
description: Generate a production-ready ASP.NET Core REST API controller (CRUD) from a description, OpenAPI JSON contract, or resource theme — with MediatR handlers, FluentValidation, ProblemDetails, OpenAPI annotations, versioning, and an integration-test checklist.
argument-hint: "[input-mode: description|openapi|theme] [resource-name-or-spec]"
user-invocable: true
disable-model-invocation: false
---

# REST API Controller Generation (Elite)

## When to use

- You need a complete, production-ready ASP.NET Core CRUD controller for a new resource.
- You have one of three inputs: a natural-language description, an OpenAPI JSON contract, or a plain resource name / theme.
- The output must be immediately compilable and follow the team's architecture (MediatR, ProblemDetails, FluentValidation).

## Input modes

### Mode 1 — Natural-language description

Provide a sentence describing the resource and its fields.

Example: *"A Products resource with Id (Guid), Name (string, required, max 200), Price (decimal, > 0), CategoryId (Guid)."*

Steps:

1. Parse resource name, field names, types, and validation constraints from the description.
2. Derive REST routes (`GET /api/v{version}/products`, `GET /api/v{version}/products/{id}`, `POST`, `PUT`, `DELETE`).
3. Proceed to [Controller generation steps](#controller-generation-steps).

### Mode 2 — OpenAPI JSON contract

Provide a path to an OpenAPI JSON file or paste an inline snippet.

Steps:

1. Identify the primary resource from `paths` and `components/schemas`.
2. Extract operations (GET, POST, PUT, DELETE) and their request/response schemas.
3. Map schema properties to C# types (see table below).
4. Extract validation rules from `minLength`, `maxLength`, `minimum`, `maximum`, `pattern`, `required` fields.
5. Proceed to [Controller generation steps](#controller-generation-steps).

OpenAPI → C# type mapping:

| OpenAPI type | Format | C# type |
| --- | --- | --- |
| `string` | `uuid` | `Guid` |
| `string` | `date-time` | `DateTimeOffset` |
| `string` | *(none)* | `string` |
| `integer` | `int32` | `int` |
| `integer` | `int64` | `long` |
| `number` | `float` | `float` |
| `number` | `double` | `double` |
| `boolean` | *(any)* | `bool` |
| `array` | *(any)* | `List<T>` |

### Mode 3 — Theme / resource name only

Provide just the resource name (e.g. `Orders`, `Invoices`, `BlogPosts`).

Steps:

1. Assume a standard resource shape: `Id` (Guid), `Name` (string, required), `CreatedAt` (DateTimeOffset), `UpdatedAt` (DateTimeOffset, nullable).
2. Derive REST routes as in Mode 1.
3. Proceed to [Controller generation steps](#controller-generation-steps).

## Controller generation steps

### Step 1 — DTOs

Generate request and response DTOs for each operation:

```csharp
// Request DTO (POST / PUT body)
public sealed record CreateProductRequest(
    string Name,
    decimal Price,
    Guid CategoryId
);

// Response DTO (GET / POST / PUT response body)
public sealed record ProductResponse(
    Guid Id,
    string Name,
    decimal Price,
    Guid CategoryId,
    DateTimeOffset CreatedAt
);
```

Rules:

- Use `sealed record` for DTOs — immutable, structural equality by default.
- Do not expose domain entities directly; always map through a DTO.
- Use `DateTimeOffset` (not `DateTime`) for timestamps.
- Nullable fields: use `Type?` syntax.

### Step 2 — FluentValidation validators

Generate one `AbstractValidator<TRequest>` per request DTO:

```csharp
public sealed class CreateProductRequestValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(200);

        RuleFor(x => x.Price)
            .GreaterThan(0);

        RuleFor(x => x.CategoryId)
            .NotEmpty();
    }
}
```

Register validators globally via `services.AddValidatorsFromAssemblyContaining<Program>()`.

### Step 3 — MediatR commands and queries

Generate one command/query per operation:

```csharp
// Query
public sealed record GetProductByIdQuery(Guid Id) : IRequest<ProductResponse?>;

// Command
public sealed record CreateProductCommand(
    string Name,
    decimal Price,
    Guid CategoryId
) : IRequest<ProductResponse>;

public sealed record UpdateProductCommand(
    Guid Id,
    string Name,
    decimal Price,
    Guid CategoryId
) : IRequest<ProductResponse?>;

public sealed record DeleteProductCommand(Guid Id) : IRequest<bool>;
```

Handlers:

```csharp
public sealed class GetProductByIdHandler : IRequestHandler<GetProductByIdQuery, ProductResponse?>
{
    private readonly IProductRepository _repository;

    public GetProductByIdHandler(IProductRepository repository)
        => _repository = repository;

    public async Task<ProductResponse?> Handle(
        GetProductByIdQuery request,
        CancellationToken cancellationToken)
    {
        var entity = await _repository.GetByIdAsync(request.Id, cancellationToken);
        return entity is null ? null : MapToResponse(entity);
    }

    private static ProductResponse MapToResponse(Product entity) =>
        new(entity.Id, entity.Name, entity.Price, entity.CategoryId, entity.CreatedAt);
}
```

### Step 4 — Controller class

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/products")]
[Produces("application/json")]
public sealed class ProductsController : ControllerBase
{
    private readonly ISender _sender;

    public ProductsController(ISender sender) => _sender = sender;

    /// <summary>Get all products (paginated).</summary>
    /// <response code="200">List of products.</response>
    [HttpGet]
    [ProducesResponseType(typeof(IReadOnlyList<ProductResponse>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var results = await _sender.Send(
            new GetProductsQuery(page, pageSize), cancellationToken);
        return Ok(results);
    }

    /// <summary>Get a product by ID.</summary>
    /// <response code="200">Product found.</response>
    /// <response code="404">Product not found.</response>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(ProductResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(
        Guid id, CancellationToken cancellationToken = default)
    {
        var result = await _sender.Send(new GetProductByIdQuery(id), cancellationToken);
        return result is null ? NotFound() : Ok(result);
    }

    /// <summary>Create a new product.</summary>
    /// <response code="201">Product created.</response>
    /// <response code="400">Validation failure.</response>
    [HttpPost]
    [ProducesResponseType(typeof(ProductResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] CreateProductRequest request,
        CancellationToken cancellationToken = default)
    {
        var command = new CreateProductCommand(
            request.Name, request.Price, request.CategoryId);
        var result = await _sender.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
    }

    /// <summary>Update an existing product.</summary>
    /// <response code="200">Product updated.</response>
    /// <response code="400">Validation failure.</response>
    /// <response code="404">Product not found.</response>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(typeof(ProductResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        Guid id,
        [FromBody] CreateProductRequest request,
        CancellationToken cancellationToken = default)
    {
        var command = new UpdateProductCommand(
            id, request.Name, request.Price, request.CategoryId);
        var result = await _sender.Send(command, cancellationToken);
        return result is null ? NotFound() : Ok(result);
    }

    /// <summary>Delete a product.</summary>
    /// <response code="204">Product deleted.</response>
    /// <response code="404">Product not found.</response>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(
        Guid id, CancellationToken cancellationToken = default)
    {
        var deleted = await _sender.Send(new DeleteProductCommand(id), cancellationToken);
        return deleted ? NoContent() : NotFound();
    }
}
```

### Step 5 — Authorization hooks

Add per-endpoint authorization attributes based on the resource sensitivity. Default pattern:

```csharp
[Authorize]                  // require any authenticated user
[Authorize(Policy = "Admin")] // scope to a named policy
[AllowAnonymous]             // explicitly public
```

Rules:

- Read endpoints (`GET`) are typically `[AllowAnonymous]` or low-privilege.
- Write endpoints (`POST`, `PUT`, `DELETE`) require authenticated + scoped policy.
- Always add `[ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status401Unauthorized)]` and `403` where applicable.

### Step 6 — Versioning

Register API versioning in `Program.cs` or `Startup.cs`:

```csharp
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
});
builder.Services.AddVersionedApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});
```

Route template: `[Route("api/v{version:apiVersion}/products")]`

### Step 7 — OpenAPI documentation

Ensure `Swashbuckle.AspNetCore` is configured to include XML comments:

```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.IncludeXmlComments(
        Path.Combine(AppContext.BaseDirectory,
        $"{Assembly.GetExecutingAssembly().GetName().Name}.xml"));
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });
    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                    { Type = ReferenceType.SecurityScheme, Id = "Bearer" }
            },
            Array.Empty<string>()
        }
    });
});
```

Enable XML documentation in the `.csproj`:

```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <NoWarn>$(NoWarn);1591</NoWarn>
</PropertyGroup>
```

### Step 8 — ProblemDetails global handler

Ensure the global exception middleware converts unhandled exceptions to `ProblemDetails`:

```csharp
app.UseExceptionHandler(exceptionHandlerApp =>
{
    exceptionHandlerApp.Run(async context =>
    {
        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        context.Response.ContentType = "application/problem+json";
        var problem = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An unexpected error occurred.",
            Detail = context.Features.Get<IExceptionHandlerPathFeature>()?.Error.Message
        };
        await context.Response.WriteAsJsonAsync(problem);
    });
});
```

## Integration-test checklist

After generating the controller, produce an integration test scaffolding using `WebApplicationFactory<Program>`:

```csharp
public sealed class ProductsControllerTests
    : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ProductsControllerTests(WebApplicationFactory<Program> factory)
        => _client = factory.CreateClient();

    [Fact]
    public async Task GetAll_ReturnsOk() { /* ... */ }

    [Fact]
    public async Task GetById_WithUnknownId_ReturnsNotFound() { /* ... */ }

    [Fact]
    public async Task Create_WithValidPayload_Returns201() { /* ... */ }

    [Fact]
    public async Task Create_WithInvalidPayload_Returns400() { /* ... */ }

    [Fact]
    public async Task Update_WithUnknownId_ReturnsNotFound() { /* ... */ }

    [Fact]
    public async Task Delete_WithUnknownId_ReturnsNotFound() { /* ... */ }
}
```

**Required test cases**:

- `GET /products` → `200 OK`, response is a list
- `GET /products/{id}` (known) → `200 OK`, correct body
- `GET /products/{id}` (unknown) → `404 Not Found` + `ProblemDetails`
- `POST /products` (valid) → `201 Created`, `Location` header set
- `POST /products` (invalid) → `400 Bad Request` + `ValidationProblemDetails`
- `PUT /products/{id}` (known, valid) → `200 OK`
- `PUT /products/{id}` (unknown) → `404 Not Found`
- `DELETE /products/{id}` (known) → `204 No Content`
- `DELETE /products/{id}` (unknown) → `404 Not Found`
- (if auth) Unauthenticated request to write endpoint → `401 Unauthorized`

## Self-check

- [ ] DTOs use `sealed record`; no naked entity exposure.
- [ ] `AbstractValidator<TRequest>` created for every write DTO.
- [ ] `ProblemDetails` / `ValidationProblemDetails` on all error paths.
- [ ] All controller actions have `[ProducesResponseType]` for each documented status code.
- [ ] XML doc comments on every action — renders in Swagger UI.
- [ ] `CancellationToken` threaded through all async calls.
- [ ] Versioning route template applied (`api/v{version:apiVersion}/...`).
- [ ] Authorization attribute applied (even if `[AllowAnonymous]` — explicit is safe).
- [ ] Integration test cases cover all 4 CRUD operations and error paths.

## Advanced patterns

- **Idempotency keys**: for `POST` operations on financial or external-trigger resources, add `Idempotency-Key` header handling via a pipeline behavior.
- **Optimistic concurrency**: add `ETag` / `If-Match` header support for `PUT` when contention risk is high.
- **Pagination**: prefer cursor-based pagination over offset for large datasets; add `X-Total-Count` response header.
- **HATEOAS**: for API-first designs, add `_links` to responses using a `LinkGenerator`-backed utility.
- **Minimal API alternative**: if endpoint count is small (< 5), consider `MapGet` / `MapPost` with `IResult` returns instead of a controller class.
