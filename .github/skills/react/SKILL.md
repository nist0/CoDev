---
name: react
description: React architecture -- component boundaries, state strategy, data fetching, performance, a11y, and testing.
argument-hint: "[component-or-page] [concern]"
user-invocable: true

disable-model-invocation: false
---

# React (Architecture, State, Performance) (Elite)

## When to use

- Building or refactoring React components/pages.

- Choosing state management patterns.

- Fixing performance or re-render issues.

## Workflow

1) Component boundaries

   - Split container vs presentational components where useful.
2) State strategy

   - Local state for local concerns; lift state only when needed.

   - Use derived state carefully; prefer memoization only after measuring.
3) Data fetching

   - Centralize fetch logic; handle loading/error states consistently.

   - Prefer React Query / SWR for server state over hand-rolled `useEffect`.
4) Performance basics

   - Identify unnecessary rerenders; memoize selectively.

   - Measure with React DevTools Profiler before optimizing.
5) Testing

   - Unit tests for pure logic; component tests for UI behaviors.

   - Use React Testing Library (user-event, not implementation details).
6) Verification

   - Manual flows + automated tests; check accessibility (keyboard, ARIA).

## Self-check

- [ ] Component boundary follows Page/Container/Presentational pattern.

- [ ] No `useEffect` for data fetching; React Query or SWR used.

- [ ] Memoization (`useMemo`, `useCallback`) applied only after measuring.

- [ ] Keyboard navigation and focus management verified.

- [ ] WCAG AA color contrast checked.

- [ ] Component tests use React Testing Library (user-event-first).

## U+1F3C6 Elite Section -- Top 5% React Practices

- **Server components first (Next.js 14+)**: Default to React Server Components for data-fetching pages; opt into `'use client'` only when interactivity requires it. This eliminates hydration cost for static content.

- **`startTransition` for non-urgent updates**: Wrap non-critical state updates in `startTransition` to keep the UI responsive during heavy renders -- avoids blocking user input.

- **Stale-while-revalidate everywhere**: Use React Query / SWR with `staleTime` tuned to your data freshness requirements. Never build custom cache logic from scratch.

- **Virtualized lists at scale**: For lists >200 items, use `@tanstack/virtual`. Rendering all rows is never acceptable in production.

- **Error boundaries per feature**: Wrap each major feature in an `ErrorBoundary` with a meaningful fallback. Never let one broken component crash the whole page.

- **`use()` API + Suspense for async**: In React 18+, unwrap promises with `use()` in RSC, letting Suspense handle loading states declaratively instead of manual `isLoading` flags.

- **Accessibility in CI**: Run `jest-axe` or `vitest-axe` on every component test suite. Every interactive component must pass WCAG 2.1 AA before merging -- never defer a11y.

## Outputs

- Recommended component/state architecture.

- Performance triage checklist.

- Test plan suggestions.
