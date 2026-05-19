---
name: pg
description: "PostgreSQL quick operations — schema inspection, query optimization, index analysis, lock triage, and connection pool management."
agent: "Backend .NET"

## argument-hint: "concern=<connect|schema|query|locks|vacuum|pool|user> table=<name>"

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Apply the procedure from `.github/skills/postgres/SKILL.md`.

Act as a Backend .NET engineer and help with the PostgreSQL task.

Inputs:

- concern: ${input:concern:connect | schema | query | locks | vacuum | pool | user}

- table: ${input:table:table or query to inspect (optional)}

## Workflow

1. Use the Quick reference section of the skill for immediate commands.

2. For query performance: request the `EXPLAIN (ANALYZE, BUFFERS)` output before recommending indexes.

3. For locks: query `pg_stat_activity` + `pg_locks` to identify the blocker before taking action.

4. For schema changes: stage destructive changes (drop/rename/type change) with a migration plan and rollback.

## Output

- Copy-paste-ready `psql` or SQL commands for the concern.

- Risk classification for any mutating command (`low | medium | high`).

- Verification query to confirm the outcome.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Backend .NET** | always — PostgreSQL operations | *(this prompt)* | Commands provided, risk classified, verification query included |
| 2 | **Reliability** | performance regression or lock contention confirmed | `/postmortem` or `/triage-error` | Root cause identified, fix verified |
| 3 | **Delivery Lead** | schema migration required | `/pr-review` | Migration PR reviewed and merged |
