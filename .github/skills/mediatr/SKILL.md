---
name: mediatr
description: MediatR CQRS patterns — commands, queries, handlers, pipeline behaviors, and handler testing.
argument-hint: "[feature or bounded context]"
user-invocable: true

## disable-model-invocation: false

# MediatR (CQRS Patterns) (Elite)

## When to use

- Implementing command/query separation with MediatR.

- Adding cross-cutting pipeline behaviors (logging, validation, caching).

- Structuring application layer with handlers.

## Command vs Query Decision

| Scenario | Pattern |
|----------|----------|
| Mutates state | Command (`IRequest<Unit>` or `IRequest<T>`) |
| Returns data only | Query (`IRequest<T>`) |
| Cross-cutting concern | Pipeline behavior (`IPipelineBehavior<TReq, TRes>`) |
| Event propagation | Notification + `INotificationHandler<T>` |

## Workflow

### 1. Define commands/queries

- Clear intent names: `CreateOrderCommand`, `GetOrderByIdQuery`.

- Keep them in the `Application` layer (not `Domain` or `Infrastructure`).

### 2. Implement handlers

- Single responsibility: one handler per command/query.

- Keep handlers thin; delegate domain logic to domain objects.

### 3. Add pipeline behaviors

- Register in DI as `IPipelineBehavior<TReq, TRes>`.

- Execution order: first registered = outermost behavior.

- Common behaviors: `ValidationBehavior`, `LoggingBehavior`, `CachingBehavior`.

### 4. Test handlers in isolation

- Test handlers directly (without `IMediator`); inject fakes/mocks.

- Test pipeline behaviors separately with fake `RequestHandlerDelegate`.

- Integration test the full pipeline for critical flows.

## Self-check

- [ ] Commands and queries have clear intent names.

- [ ] Handlers are thin (domain logic in domain objects, not handlers).

- [ ] Pipeline behavior order is explicit and documented.

- [ ] Handlers tested in isolation with fakes.

- [ ] No business logic inside pipeline behaviors (only cross-cutting concerns).

## Outputs

- Command/query class patterns.

- Handler implementation guidance.

- Pipeline behavior examples.

- Testing approach for handlers.
