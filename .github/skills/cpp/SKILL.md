---
name: cpp
description: Modern C++ -- RAII, ownership, smart pointers, error handling policy, performance measurement-first, and tooling.
argument-hint: "[component or module]"
user-invocable: true

disable-model-invocation: false
---

# C++ (Modern Practices, Safety, Performance) (Elite)

## When to use

- You write or review C++ code and want modern safe patterns.

- You need RAII, ownership clarity, and performance tuning.

## Ownership and Lifetime Table

| Scenario | Recommended pattern |
|----------|--------------------|
| Sole ownership | `std::unique_ptr<T>` |
| Shared ownership | `std::shared_ptr<T>` (use sparingly) |
| Non-owning reference | Raw pointer or `std::span<T>` |
| Stack allocation | Prefer value types; avoid premature heap |
| Resource cleanup | RAII wrappers; no naked `new`/`delete` |

## Workflow

### 1. Ownership and lifetime

- Prefer RAII; use smart pointers for heap resources.

- Avoid raw owning pointers; document non-owning pointer semantics.

### 2. APIs and const correctness

- Mark `const` all methods and parameters that don't mutate.

- Avoid returning raw owning pointers from functions.

### 3. Error handling

- Decide exceptions vs error codes per module; be consistent.

- Document the policy in the module header.

- Use `std::expected` (C++23) or `std::optional` for fallible operations where exceptions are undesirable.

### 4. Performance

- Measure first with profiler (`perf`, `gprof`, `VTune`) before optimizing.

- Avoid copies: prefer move semantics, `std::string_view`, `std::span`.

### 5. Tooling

- Warnings: `-Wall -Wextra -Wpedantic -Werror`.

- Sanitizers: `-fsanitize=address,undefined` in debug builds.

- Static analysis: `clang-tidy`, `cppcheck`.

- Formatting: `clang-format` with shared `.clang-format`.

## Self-check

- [ ] No raw owning pointers; RAII used for all resources.

- [ ] Const correctness applied throughout.

- [ ] Error handling policy is consistent within the module.

- [ ] Performance changes measured before and after (profiler data).

- [ ] Sanitizers run locally; `clang-tidy` passes.

## Outputs

- Modern C++ checklist.

- Ownership/lifetime guidance.

- Performance triage checklist.
