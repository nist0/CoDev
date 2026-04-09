---
name: typescript
description: TypeScript type safety — boundary typing, discriminated unions, type guards, runtime validation, and unsafe pattern elimination.
argument-hint: "[module] [concern]"
user-invocable: true
disable-model-invocation: false
---

# TypeScript (Types, Boundaries, Safety) (Elite)

## When to use

- Designing types at API boundaries.
- Cleaning up unsafe types (`any`, overly broad unions).
- Improving DX and correctness with strong typing.

## Workflow

1) Identify boundaries
   - API clients, external libs, storage, runtime inputs.
2) Define types
   - Prefer explicit DTO interfaces and discriminated unions where relevant.
3) Narrow types early
   - Use type guards; validate runtime inputs.
4) Avoid unsafe patterns
   - No implicit `any`; avoid `as unknown as`.
5) Testing
   - Test boundary transformations and reducers/selectors.

## Type safety checklist

| Pattern | Safe? | Preferred alternative |
|---------|-------|-----------------------|
| `any` | ❌ | `unknown` + type guard |
| `as unknown as T` | ❌ | Proper type assertion with guard |
| Implicit `any` parameter | ❌ | Explicit type annotation |
| `!` non-null assertion | ⚠️ | Optional chaining + nullish coalescing |
| `object` type | ⚠️ | Explicit interface or `Record<K, V>` |
| Discriminated union | ✅ | Preferred for variant modeling |
| `unknown` + `instanceof` guard | ✅ | Preferred for external data |

## Runtime validation

For external data (API responses, env vars, JSON):

```typescript
// Use zod, valibot, or arktype for runtime schema validation
import { z } from 'zod';
const UserSchema = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof UserSchema>;
```

## Self-check

- [ ] `strict: true` in `tsconfig.json`.
- [ ] No `any` in new code; existing `any` tracked and time-bounded.
- [ ] All API boundary types explicit (no inferred from implementation).
- [ ] External data validated at runtime (zod/valibot/etc.).
- [ ] Type guards used to narrow `unknown` inputs.
- [ ] Discriminated unions used for variant modeling.

## 🏆 Elite Section — Top 5% TypeScript Practices

- **Branded types for domain primitives**: Use `type UserId = string & { readonly _brand: 'UserId' }` to prevent mixing IDs of different entity types at compile time.
- **`zod` for runtime validation**: Parse all external data (API responses, env vars, form input) with `zod` schemas and derive TypeScript types from them — single source of truth.
- **`ts-reset` for safer stdlib**: Apply `ts-reset` to fix surprising stdlib typings (e.g. `JSON.parse` returns `unknown`, `Array.filter(Boolean)` narrows correctly).
- **Exhaustiveness checks**: Use `satisfies never` or a `assertNever` helper in `switch` chains over discriminated unions to catch unhandled cases at compile time.
- **`tsc --noEmit` in CI**: Run type-checking separately from bundling so type errors are always caught even when the bundler is permissive.
- **Module boundary linting**: Use `eslint-plugin-boundaries` or `nx/enforce-module-boundaries` to enforce layered imports and prevent circular dependencies from sneaking in.
- **Avoid `as unknown as T`**: This silences the compiler instead of fixing the problem. Prefer a proper type guard or adjust the upstream type. Any use requires an inline comment explaining why.

## Outputs

- Type boundary strategy.
- Type guard and validation suggestions.
- Refactoring plan to remove unsafe typing.
