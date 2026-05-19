---
name: ".NET Defaults"
description: "C#/.NET code standards: safety, readability, diagnostics, testing expectations."

## applyTo: "**/*.cs"

# .NET Defaults

- Prefer clear, testable code (small methods, explicit dependencies).

- Use file-scoped namespaces when possible.

- Prefer explicit types in public APIs; `var` only when obvious.

- Use cancellation tokens for async entrypoints where relevant.

- Prefer structured logging (include correlation IDs if available).

- Validate inputs; return meaningful status codes and errors.

- For API changes, update OpenAPI/Swagger docs and add/adjust tests.

- Add unit tests for new behavior; add integration tests when endpoint behavior changes.

## Advanced .NET quality guardrails

- Prefer immutable request/response contracts where practical (`record` DTOs for API boundaries).

- Keep application layers explicit (API -> application -> infrastructure) and avoid leaking EF entities across boundaries.

- Use `ProblemDetails` as the default API error contract.

- Use `IOptions<T>`/`IOptionsMonitor<T>` for configuration; validate options at startup for required settings.

- Treat nullable reference types as enabled and resolve warnings intentionally.

## Performance and reliability defaults

- Avoid sync-over-async and blocking calls on request paths.

- Favor projection queries (`Select`) for read endpoints instead of loading entire aggregates.

- Add cancellation token flow from controller entrypoints into downstream I/O calls.

- Benchmark or measure before micro-optimizing; document the metric used and the before/after delta.

## Security defaults

- Never trust client input: validate model + business invariants.

- Prefer least-privilege database permissions and secret-less local examples.

- Keep authentication/authorization checks close to endpoint boundaries; deny-by-default for sensitive operations.

## Example patterns

- Controller pattern:

  - inject application service/mediator only (not DbContext directly)

  - pass `CancellationToken` to async calls

  - return `ProblemDetails` for known failures

- Data-access pattern:

  - read: `AsNoTracking()` + projection

  - write: explicit transaction for multi-step invariants

  - migration: review generated SQL before applying

## Microsoft references

- ASP.NET Core fundamentals:

  - <https://learn.microsoft.com/aspnet/core/fundamentals/>

- Error handling and ProblemDetails:

  - <https://learn.microsoft.com/aspnet/core/fundamentals/error-handling>

- Dependency injection:

  - <https://learn.microsoft.com/dotnet/core/extensions/dependency-injection>

- Configuration and options pattern:

  - <https://learn.microsoft.com/dotnet/core/extensions/options>

- Logging in .NET:

  - <https://learn.microsoft.com/dotnet/core/extensions/logging>

- EF Core docs:

  - <https://learn.microsoft.com/ef/core/>

- .NET code analysis and style rules:

  - <https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview>

---

## 🏆 Elite Section — Top 5% .NET Practices

- **Source generators over reflection**: Prefer compile-time code generation (e.g. `System.Text.Json` source gen, Dapper source gen) over runtime reflection for performance-critical paths.

- **Vertical slice architecture**: Organize features as self-contained slices (`Features/Orders/CreateOrder/{Command,Handler,Validator,Endpoint}.cs`) instead of horizontal layers. Reduces coupling and merge conflicts.

- **Outbox pattern for reliability**: Never publish events inside a database transaction. Use the transactional outbox pattern to guarantee at-least-once delivery without distributed transactions.

- **BenchmarkDotNet before merging hot paths**: Any change to a code path that handles >1k req/s must ship with a `BenchmarkDotNet` comparison showing no regression.

- **Structured diagnostics from day 0**: Instrument new services with `ActivitySource` for distributed tracing and `Meter` for custom metrics from the first commit — retrofitting is painful.

- **Resiliency via Polly pipelines**: Define named `ResiliencePipeline` policies (retry + circuit breaker + timeout) at startup; never inline retry logic ad hoc inside service methods.
