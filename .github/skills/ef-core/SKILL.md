---
name: ef-core
description: EF Core modeling, migrations, query performance, concurrency, and testing with real Postgres.
argument-hint: "[entity] [concern]"
user-invocable: true

disable-model-invocation: false
---

# EF Core (Modeling, Migrations, Performance) (Elite)

## When to use

- Designing or refactoring EF Core models.

- Handling migrations and schema evolution safely.

- Investigating performance issues (N+1, slow queries, indexes).

- Implementing concurrency control and transactions.

## Workflow

1) Model design

   - Identify aggregates, boundaries, and navigation properties.

   - Prefer explicit configurations (Fluent API) for complex mappings.
2) Migrations discipline

   - Generate migration, review SQL, ensure backward compatibility where possible.

   - Plan data migrations separately if needed (idempotent scripts).
3) Query performance

   - Turn on SQL logging for investigation.

   - Identify N+1 patterns; use Include/Select projections properly.

   - Add indexes aligned with query predicates/sorts.
4) Transactions and concurrency

   - Use explicit transactions when multiple operations must be atomic.

   - Consider optimistic concurrency tokens when needed.
5) Testing

   - Prefer integration tests with real Postgres when behavior matters (e.g., collation, JSONB).
6) Verification

   - Benchmark critical paths; verify query plans and index usage.

## Migration deployment safety

- Review destructive operations explicitly (drop/rename/type-change).

- Prefer staged migrations for large tables (expand -> backfill -> contract).

- Keep rollback strategy documented for every production migration.

## Self-check

- [ ] Navigation properties reviewed for accidental cartesian explosion.

- [ ] Every new index tied to a measured query predicate/sort.

- [ ] `AsNoTracking()` used for read-only paths.

- [ ] Concurrency tokens tested for conflict behavior.

- [ ] Destructive migration operations reviewed explicitly.

- [ ] Integration tests use real Postgres (via testcontainers).

## Outputs

- Model and mapping recommendations.

- Migration plan + safety checklist.

- Performance diagnosis checklist + typical fixes.

- Test strategy for EF Core + Postgres.

## Microsoft references

- [EF Core docs](https://learn.microsoft.com/ef/core/)

- [Migrations](https://learn.microsoft.com/ef/core/managing-schemas/migrations/)

- [Performance](https://learn.microsoft.com/ef/core/performance/)

- [Querying related data](https://learn.microsoft.com/ef/core/querying/related-data/)
