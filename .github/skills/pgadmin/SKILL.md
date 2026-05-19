---
name: pgadmin
description: pgAdmin PostgreSQL UI — schema inspection, query plan analysis, migration validation, and safe DB operations.
argument-hint: "[schema, table, or query to analyze]"
user-invocable: true

## disable-model-invocation: false

# pgAdmin (PostgreSQL Admin UI) (Elite)

## When to use

- You need to inspect schema, indexes, and query plans.

- You want to validate migrations and troubleshoot DB behavior.

## Query Performance Checklist

| Signal | Action |
|--------|--------|
| `Seq Scan` on large table | Check if index is missing or unused |
| High `actual rows` vs `estimated rows` | Run `ANALYZE` to update statistics |
| `Hash Join` on large sets | Consider index or query restructure |
| High `Buffers: shared hit=0` | Cache miss; check working_mem or indexes |
| `Sort` with `external merge` | Increase `work_mem` for the session |

## Workflow

### 1. Connection setup

- host/port/db/user; SSL settings as needed.

- Prefer read-only user for analysis (never production admin for reads).

### 2. Schema inspection

- Tables, columns, constraints, indexes.

- Check for missing indexes on FK columns and frequently-filtered fields.

### 3. Query analysis

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...
```

- Look for: Seq Scan on large tables, high row estimate errors, nested loops on large sets.

### 4. Migration validation

- Verify expected schema changes after migration.

- Check: table/column existence, index creation, constraint correctness.

### 5. Safety

- Avoid direct production mutations via pgAdmin; prefer read-only access.

- Use transactions for any manual data fixes; `ROLLBACK` before `COMMIT`.

## Self-check

- [ ] Read-only connection used for analysis (not admin/superuser).

- [ ] `EXPLAIN (ANALYZE, BUFFERS)` used (not just `EXPLAIN`).

- [ ] Missing indexes identified and remediation planned.

- [ ] Migration validation confirmed (expected schema changes present).

- [ ] No manual production mutation without a transaction and peer review.

## Outputs

- DB inspection checklist.

- Query performance investigation steps.

- Migration validation checklist.
