---
name: "TypeScript Defaults"
description: "TS/JS guidance: types first, predictable state, lint-friendly patterns."
applyTo: "**/*.ts"
---

# TypeScript Defaults

## Type discipline

- Prefer explicit types at boundaries (API responses, function signatures, external libs).
- Avoid implicit `any`; use `unknown` when the type is genuinely unknown, then narrow explicitly.
- Enable `strict: true` in `tsconfig.json` — never disable it project-wide.
- Use `satisfies` operator to validate object shapes without widening the inferred type.

## State & side effects

- Keep side effects isolated; prefer pure functions where possible.
- Avoid global mutable state; use dependency injection or context.
- Model domain concepts with `type` aliases or `interface`; use `enum` only for stable, closed sets.

## Async patterns

- Prefer `async`/`await` over raw promise chains for readability.
- Always handle rejected promises: either `await` with `try/catch` or attach `.catch()`.
- Use `AbortController` / `AbortSignal` for cancellable async operations.

## Naming & module conventions

- Use `camelCase` for variables/functions, `PascalCase` for types/classes, `SCREAMING_SNAKE_CASE` for constants.
- Prefer named exports over default exports for discoverability and refactoring.
- Avoid barrel files (`index.ts` re-exports everything) in large packages — they hurt tree-shaking.

## Examples

✅ Correct — explicit types, safe async:

```typescript
async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch user ${id}: ${res.status}`);
  return res.json() as Promise<User>;
}
```

❌ Wrong — implicit any, swallowed error:

```typescript
async function fetchUser(id) {
  const res = await fetch(`/api/users/${id}`);
  return res.json(); // no error handling, implicit any
}
```

---

## 🏆 Elite Section — Top 5% TypeScript Practices

- **Branded types for domain primitives**: Use `type UserId = string & { readonly _brand: 'UserId' }` to prevent mixing primitive IDs at compile time.
- **`zod` for runtime validation**: Parse external data (API responses, env vars, form input) with `zod` schemas. Derive TypeScript types from schemas — single source of truth.
- **`ts-reset` for safer stdlib**: Apply `ts-reset` to fix surprising stdlib typings (e.g. `JSON.parse` returns `unknown`, `Array.filter(Boolean)` narrows correctly).
- **Exhaustiveness checks**: Use `satisfies never` or a helper function in `switch` / `if-else` chains over discriminated unions to catch unhandled cases at compile time.
- **`tsc --noEmit` in CI**: Run type-checking separately from bundling so type errors are always caught even when the bundler is permissive.
- **Module boundary linting with ESLint**: Use `eslint-plugin-boundaries` or `nx/enforce-module-boundaries` to enforce layered imports and prevent circular dependencies.
