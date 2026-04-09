---
name: repo-understanding
description: Produce a navigable codebase summary — module map, entry points, key data flows, dependency overview, and doc structure.
argument-hint: "[repo-or-feature] [depth]"
user-invocable: true
disable-model-invocation: false
---

# Repo Understanding (Elite)

## When to use

- Explaining how a codebase is structured and how to navigate it.
- Generating architecture summaries or module maps for new contributors.
- Before making cross-cutting changes: understand impact surfaces.
- Producing documentation input (ADR context, onboarding guide).

## Procedure

### 1. Map top-level structure

For each top-level directory/file:

| Path | Purpose | Key contents |
|------|---------|---------------|
| `src/` | ... | ... |
| `.github/` | ... | ... |

Note: language/framework convention vs custom organization.

### 2. Identify entry points

Locate the starting points of execution:

| Type | Location | Description |
|------|----------|-------------|
| Application entry | `main.ts` / `Program.cs` / `__main__.py` | Bootstrap |
| HTTP handlers | `routes/` / `controllers/` | API surface |
| Event handlers | Queue consumers / event listeners | Async entry |
| Scheduled jobs | Cron / timer triggers | Background work |

### 3. Trace key data flows

For each major user-facing flow:

```text
Request → Router → Controller → Service → Repository → Database
                    ↓
                  External API / Queue / Cache
```

- Note where validation happens.
- Note where authentication/authorization is checked.
- Note where side effects occur (emails, webhooks, events).

### 4. Identify key dependencies

| Category | Library/Service | Purpose |
|----------|-----------------|---------|
| HTTP | express / ASP.NET | Web server |
| ORM/DB | EF Core / Prisma | Data access |
| Auth | JWT / OIDC | Identity |
| Messaging | RabbitMQ / Service Bus | Async comms |
| Observability | OpenTelemetry | Traces/metrics |

Note any pinned versions, security advisories, or deprecated packages.

### 5. Identify coupling and risk areas

- **High coupling**: modules that many others depend on.
- **Side-effect heavy**: code that calls external systems without clear boundaries.
- **Test coverage gaps**: directories with no test files.
- **Outdated patterns**: code that contradicts current conventions.

### 6. Produce the summary

```markdown
# Codebase Overview: <repo>

## Module map
| Module | Purpose |

## Entry points
| Type | Path |

## Key data flows
<text diagram>

## Key dependencies
| Category | Library |

## Risk areas
- ...

## Suggested doc structure
- ...
```

## Self-check

- [ ] Every top-level directory described.
- [ ] Entry points for all execution types listed.
- [ ] At least 1 key data flow traced end-to-end.
- [ ] Dependencies table includes observability and auth.
- [ ] Risk areas and test gaps identified.
- [ ] Summary is usable by a new contributor with no prior context.

## Outputs

- Module map (text table or Mermaid).
- Entry points list.
- Key flow descriptions (text diagrams).
- Dependency overview table.
- Risk areas and coupling notes.
- Suggested doc structure.
