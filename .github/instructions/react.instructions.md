---
name: "React Defaults"
description: "React/TSX guidance: component boundaries, hooks discipline, performance basics."

applyTo: "**/*.tsx"
---

# React Defaults

## Component design

- Keep components small and single-purpose; isolate data fetching from presentation.

- Prefer composition over prop drilling -- use context or component slots for cross-cutting concerns.

- Co-locate component, styles, and tests in the same directory (`Button/Button.tsx`, `Button.test.tsx`).

## Hooks discipline

- Use hooks consistently; document non-obvious `useEffect` dependencies with a comment.

- Never call hooks conditionally or inside loops.

- Prefer `useReducer` over multiple `useState` calls when state transitions are interdependent.

- Extract custom hooks (`useXxx`) for reusable stateful logic; keep them in `hooks/` or alongside the consuming component.

## Performance

- Avoid unnecessary rerenders: memoize **only after measuring** with React DevTools Profiler.

- Prefer stable keys; never use array index as a key for dynamic lists.

- Use `React.lazy` + `Suspense` for route-level code splitting.

## Testing

- Update component tests when behavior changes.

- Use `@testing-library/react`; test user behavior, not implementation details.

- Avoid `act()` wrappers in tests -- prefer `userEvent` which handles this automatically.

## Examples

U+2705 Correct -- container/presentational split:

```tsx
// UserListContainer.tsx -- fetches data
export function UserListContainer() {
  const { data, isLoading } = useUsers();
  return <UserList users={data} isLoading={isLoading} />;
}

// UserList.tsx -- pure presentation
export function UserList({ users, isLoading }: UserListProps) {
  if (isLoading) return <Spinner />;
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

---

## U+1F3C6 Elite Section -- Top 5% React Practices

- **Server components first (Next.js 14+)**: Default to React Server Components for data-fetching pages; opt into `'use client'` only when interactivity requires it. This eliminates hydration cost for static content.

- **Stale-while-revalidate everywhere**: Use `react-query` or SWR with `staleTime` tuned to your data freshness requirements. Never build custom cache logic from scratch.

- **Virtualized lists at scale**: For lists >200 items, use `react-virtual` or `@tanstack/virtual`. Rendering all rows is never acceptable in production.

- **Error boundaries per feature**: Wrap each major feature in an `ErrorBoundary` with a meaningful fallback UI. Never let one broken component crash the whole page.

- **`use` API + Suspense for async**: In React 18+, use the `use()` API to unwrap promises in RSC, letting Suspense handle loading states declaratively instead of manual `isLoading` flags.

- **Accessibility from the start**: Run `axe-core` in CI (`jest-axe` or `vitest-axe`). Every interactive component must pass WCAG 2.1 AA before merging.
