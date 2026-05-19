---
name: html-css
description: HTML/CSS — semantic structure, accessibility baseline, responsive design, and maintainability.
argument-hint: "[component or page name]"
user-invocable: true

## disable-model-invocation: false

# HTML/CSS (Structure, Accessibility, Maintainability) (Elite)

## When to use

- You need clean, accessible markup and maintainable styling.

- You're working on layout issues, responsiveness, or UI consistency.

## Accessibility Baseline

| Requirement | Implementation |
|-------------|----------------|
| Keyboard navigation | All interactive elements reachable via Tab/Enter/Space |
| Focus states | Visible `:focus-visible` ring on all interactive elements |
| ARIA | Use only when semantic HTML is insufficient |
| Color contrast | WCAG AA: 4.5:1 for text, 3:1 for UI components |
| Alt text | All meaningful images have descriptive `alt` attributes |
| Headings | Logical hierarchy (h1 > h2 > h3), no skipping levels |

## Workflow

### 1. Semantic structure

- Use semantic elements: `<main>`, `<nav>`, `<section>`, `<article>`, `<button>` (not `<div onClick>`).

- Structure content for screen readers: one `<h1>` per page, logical landmark regions.

### 2. Accessibility baseline

- Keyboard navigation, focus states, ARIA only when semantic HTML is insufficient.

- Color contrast and readable typography (WCAG AA).

### 3. Responsive design

- Mobile-first layout; avoid fixed widths; use CSS Grid and Flexbox.

- Use `clamp()`, `min()`, `max()` for fluid typography and spacing.

### 4. Maintainability

- Prefer consistent spacing scale (e.g., 4px/8px base); avoid magic numbers.

- Use CSS custom properties (`--spacing-md: 1rem`) for consistency.

### 5. Verification

- Check in multiple viewports (mobile 375px, tablet 768px, desktop 1440px).

- Run axe-core or Lighthouse for a11y audit.

- Test keyboard-only navigation.

## Self-check

- [ ] Only semantic HTML used; no `<div>` for interactive elements.

- [ ] All interactive elements reachable via keyboard and have focus styles.

- [ ] Color contrast passes WCAG AA (4.5:1 for text).

- [ ] Layout verified at mobile (375px), tablet (768px), desktop (1440px).

- [ ] a11y audit run (axe-core or Lighthouse) with no critical violations.

## 🏆 Elite Section — Top 5% HTML/CSS Practices

- **Design tokens as CSS custom properties**: Structure your styling around a token system (`--color-primary`, `--spacing-4`, `--radius-md`). Tokens are the single source of truth — never hardcode raw values in components.

- **Container queries over media queries**: Use `@container` for component-scoped responsiveness rather than global breakpoints. Components that respond to their container are more composable and reusable.

- **`:focus-visible` over `:focus`**: Use `:focus-visible` to show focus rings only for keyboard navigation, not for mouse clicks. Avoids ugly outlines for mouse users while preserving accessibility for keyboard users.

- **`prefers-reduced-motion` always**: Wrap all CSS animations and transitions in `@media (prefers-reduced-motion: no-preference)`. Never animate unconditionally — users with vestibular disorders depend on this.

- **Lighthouse CI gate**: Run Lighthouse in CI (via `lighthouse-ci`) on every PR that touches layout or styling. Gate on Performance ≥ 80, Accessibility = 100, Best Practices ≥ 90.

- **Utility-first discipline (Tailwind)**: If using Tailwind, restrict `@apply` to shared component classes only. Prefer inline utilities in templates; avoid recreating a custom CSS layer that defeats tree-shaking.

## Outputs

- Semantic and a11y checklist.

- Layout strategy recommendation (flex/grid).

- Verification checklist (responsive + keyboard).
