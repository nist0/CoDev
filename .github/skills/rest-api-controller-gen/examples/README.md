# rest-api-controller-gen — Examples

Two annotated examples showing the three input modes in action.

---

## Example 1 — From natural-language description

**Input** (Mode 1 — description):

> "A BlogPosts resource with Id (Guid), Title (string, required, max 300), Body (string, required), AuthorId (Guid), PublishedAt (DateTimeOffset, nullable). CRUD endpoints required."

**Generated artifacts** (summary):

### DTOs

```csharp
public sealed record CreateBlogPostRequest(
    string Title,
    string Body,
    Guid AuthorId,
    DateTimeOffset? PublishedAt
);

public sealed record BlogPostResponse(
    Guid Id,
    string Title,
    string Body,
    Guid AuthorId,
    DateTimeOffset? PublishedAt,
    DateTimeOffset CreatedAt
);
```

### Validator

```csharp
public sealed class CreateBlogPostRequestValidator
    : AbstractValidator<CreateBlogPostRequest>
{
    public CreateBlogPostRequestValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(300);
        RuleFor(x => x.Body).NotEmpty();
        RuleFor(x => x.AuthorId).NotEmpty();
    }
}
```

### MediatR commands

```csharp
public sealed record CreateBlogPostCommand(
    string Title, string Body, Guid AuthorId, DateTimeOffset? PublishedAt)
    : IRequest<BlogPostResponse>;

public sealed record GetBlogPostByIdQuery(Guid Id) : IRequest<BlogPostResponse?>;

public sealed record UpdateBlogPostCommand(
    Guid Id, string Title, string Body, Guid AuthorId, DateTimeOffset? PublishedAt)
    : IRequest<BlogPostResponse?>;

public sealed record DeleteBlogPostCommand(Guid Id) : IRequest<bool>;
```

### Controller (abbreviated)

```csharp
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/blog-posts")]
[Produces("application/json")]
public sealed class BlogPostsController : ControllerBase
{
    private readonly ISender _sender;
    public BlogPostsController(ISender sender) => _sender = sender;

    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(BlogPostResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct = default)
    {
        var result = await _sender.Send(new GetBlogPostByIdQuery(id), ct);
        return result is null ? NotFound() : Ok(result);
    }

    [HttpPost]
    [Authorize]
    [ProducesResponseType(typeof(BlogPostResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] CreateBlogPostRequest request, CancellationToken ct = default)
    {
        var result = await _sender.Send(
            new CreateBlogPostCommand(
                request.Title, request.Body, request.AuthorId, request.PublishedAt), ct);
        return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
    }

    // ... PUT, DELETE follow the same pattern
}
```

**Annotations**:

- `[AllowAnonymous]` on read endpoints, `[Authorize]` on write endpoints.
- `CancellationToken` threaded through every async call.
- `CreatedAtAction` on POST returns `Location` header pointing to `GetById`.

---

## Example 2 — From OpenAPI JSON contract

**Input** (Mode 2 — OpenAPI JSON snippet):

```json
{
  "openapi": "3.0.1",
  "info": { "title": "Inventory API", "version": "v1" },
  "paths": {
    "/api/v1/products": {
      "get": {
        "operationId": "getProducts",
        "responses": { "200": { "description": "List of products" } }
      },
      "post": {
        "operationId": "createProduct",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": { "$ref": "#/components/schemas/CreateProductRequest" }
            }
          }
        },
        "responses": {
          "201": { "description": "Created" },
          "400": { "description": "Validation error" }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "CreateProductRequest": {
        "type": "object",
        "required": ["name", "price"],
        "properties": {
          "name":  { "type": "string", "maxLength": 200 },
          "price": { "type": "number", "format": "double", "minimum": 0.01 },
          "categoryId": { "type": "string", "format": "uuid" }
        }
      }
    }
  }
}
```

**Derivation steps**:

1. Resource: `products` → class name `ProductsController`, route `api/v{version:apiVersion}/products`.
2. Schema `CreateProductRequest` → `sealed record CreateProductRequest(string Name, double Price, Guid? CategoryId)`.
3. `required: ["name", "price"]` → FluentValidation `.NotEmpty()` on `Name`, `.GreaterThan(0.01)` on `Price`.
4. `maxLength: 200` → `.MaximumLength(200)` on `Name`.
5. `"format": "uuid"` → `Guid?` on `CategoryId` (nullable — not in `required`).

**Generated DTOs and validator** (identical structure to Example 1 — see above for full pattern).

**Integration test checklist** produced automatically:

- `POST /api/v1/products` with `{ "name": "Widget", "price": 9.99 }` → `201`
- `POST /api/v1/products` with `{}` → `400 ValidationProblemDetails`
- `POST /api/v1/products` with `{ "name": "", "price": -1 }` → `400` + validation errors for both fields
- `GET /api/v1/products` → `200` with list

---

## Example 3 — From theme only

**Input** (Mode 3 — theme):

> `Orders`

**Default shape assumed**:

- `Id` (Guid)
- `Name` (string, required, max 200)
- `CreatedAt` (DateTimeOffset, auto-set)
- `UpdatedAt` (DateTimeOffset?, auto-set on update)

**Route**: `api/v{version:apiVersion}/orders`

Proceeds with the same 8-step generation flow. All endpoints generated with standard validation and ProblemDetails error contract.

**When to add more fields**: After generating from theme, append domain-specific fields to the DTO and validator before shipping. The scaffolded class is a correct, compilable starting point — not a final artefact.
