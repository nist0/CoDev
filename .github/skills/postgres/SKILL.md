---
name: postgres
description: PostgreSQL schema design, query optimization, connection management, and PostgreSQL-specific features (JSONB, arrays).
argument-hint: "[table-or-query] [concern]"
user-invocable: true
disable-model-invocation: false
---

# PostgreSQL (with EF Core / Npgsql) (Elite)

## When to use

- Designing schemas and indexes for PostgreSQL.
- Diagnosing slow queries, lock contention, or connection pool exhaustion.
- Using PostgreSQL-specific features (JSONB, arrays, advisory locks).

## Workflow

1) Schema design: types, indexes, constraints, partitioning if needed.
2) Query optimization: EXPLAIN ANALYZE, index coverage, avoid N+1.
3) Connection management: pool sizing, idle timeouts, retry policies.
4) PostgreSQL-specific features: JSONB queries, full-text search basics.
5) Verification: benchmark with realistic data volumes.

## Query optimization checklist

```sql
-- Always run with ANALYZE and BUFFERS for accurate data
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...
```

Look for:

- `Seq Scan` on large tables → add index.
- `Nested Loop` with large sets → consider `Hash Join`.
- High `Buffers: shared hit` ratio is good; high `read` is a cache miss.
- `Filter` rows removed → index the filter column.

## Self-check

- [ ] `EXPLAIN ANALYZE` run before adding indexes.
- [ ] Index justified by a measured query predicate/sort.
- [ ] Destructive schema changes (drop/rename/type change) staged safely.
- [ ] Connection pool sized correctly (`max_connections` — pool × pool_size ≤ limit).
- [ ] JSONB queries use GIN index if querying frequently.

## Quick reference

### Connect

```sh
psql -h <host> -p 5432 -U <user> -d <db>
# Or via connection string:
psql "postgresql://<user>:<pass>@<host>:5432/<db>?sslmode=require"
```

### Explore

```sql
\l                          -- list databases
\c <db>                     -- switch database
\dn                         -- list schemas
\dt <schema>.*              -- list tables in schema
\d <table>                  -- describe table (columns, indexes, constraints)
\di <table>*                -- list indexes on table
\df <pattern>               -- list functions
```

### Inspect running state

```sql
-- Active queries (what is running right now)
SELECT pid, now() - pg_stat_activity.query_start AS duration,
       state, query
FROM pg_stat_activity
WHERE state <> 'idle'
ORDER BY duration DESC;

-- Blocking locks
SELECT bl.pid AS blocked_pid, a.query AS blocked_query,
       kl.pid AS blocking_pid, ka.query AS blocking_query
FROM pg_catalog.pg_locks bl
JOIN pg_catalog.pg_stat_activity a  ON a.pid  = bl.pid
JOIN pg_catalog.pg_locks kl         ON kl.transactionid = bl.transactionid AND kl.pid <> bl.pid
JOIN pg_catalog.pg_stat_activity ka ON ka.pid = kl.pid
WHERE NOT bl.granted;

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;

-- Cache hit ratio (should be > 99%)
SELECT round(100.0 * sum(heap_blks_hit)
     / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2) AS cache_hit_pct
FROM pg_statio_user_tables;
```

### Query analysis

```sql
-- Always use ANALYZE + BUFFERS for real execution data
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...

-- Kill a stuck query
SELECT pg_terminate_backend(<pid>);
```

### Maintenance

```sql
VACUUM ANALYZE <table>;          -- reclaim dead tuples + update stats
REINDEX TABLE <table>;           -- rebuild bloated indexes
ANALYZE <table>;                 -- update planner statistics only
```

### User / role management

```sql
CREATE ROLE <name> WITH LOGIN PASSWORD '<pass>';
GRANT CONNECT ON DATABASE <db> TO <name>;
GRANT USAGE ON SCHEMA <schema> TO <name>;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema> TO <name>;
```

### Connection pool check (PgBouncer / Npgsql)

```sh
# PgBouncer admin console
psql -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"
psql -p 6432 -U pgbouncer pgbouncer -c "SHOW STATS;"
```

## Outputs

- Schema and index recommendations.
- Query optimization checklist.
- Connection pool configuration guidance.
- Testing approach (testcontainers for integration).
