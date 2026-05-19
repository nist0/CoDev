---
name: linters
description: Lint and quality gate setup — polyglot linter matrix, CI integration, pre-commit hooks, and adoption strategy.
argument-hint: "[stack] [languages]"
user-invocable: true

## disable-model-invocation: false

# Linters & Quality Gates (Elite)

## When to use

- Setting up or improving lint/format/quality gates in CI.

- Choosing the right linter for the stack.

## Workflow

1) Identify stack (C#, TS/JS, Python, YAML, Markdown).
2) Select linters and formatters.
3) Integrate in CI (fail fast on lint errors).
4) Add local pre-commit hooks if appropriate.

## Polyglot linter matrix (recommended baseline)

| Language | Linter | Formatter |
|----------|--------|-----------|
| C/C++ | `clang-tidy`, `cppcheck` | `clang-format` |
| C#/.NET | Roslyn analyzers + `.editorconfig` | `dotnet format` |
| Python | `ruff` (lint + optional format) + `mypy` | `ruff format` |
| TypeScript/JS | ESLint + `typescript-eslint` | Prettier |
| Bash | `shellcheck` | `shfmt` |
| YAML | `yamllint` | — |
| Markdown | `markdownlint-cli2` | — |

## Adoption strategy

- **Baseline**: capture current warning set and classify by severity.

- **Gate new issues**: fail PRs on newly introduced high-severity issues.

- **Burn down debt**: address baseline in bounded batches by area.

## Self-check

- [ ] Linter selected and configured for every language in the stack.

- [ ] Linter versions pinned (not `latest`).

- [ ] CI has fast linter stage before slower integration jobs.

- [ ] Local command set documented per stack (in README or CONTRIBUTING).

- [ ] Suppression policy explicit and time-bounded (no permanent `// eslint-disable`).

- [ ] Pre-commit hooks configured (optional but recommended).

## Outputs

- Recommended linter configuration per language.

- CI job snippet.

- Pre-commit hook setup (optional).

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

- [.NET code analysis](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview)

- [Ruff](https://docs.astral.sh/ruff/)

- [ShellCheck](https://www.shellcheck.net/)

- [markdownlint](https://github.com/DavidAnson/markdownlint)
