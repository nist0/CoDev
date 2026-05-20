---
name: c
description: C language -- safety defaults, memory discipline, error handling, sanitizers, and debugging procedure.
argument-hint: "[component or module name]"
user-invocable: true

disable-model-invocation: false
---

# C (Safety, Portability, Debugging) (Elite)

## When to use

- You write or review C code and want safe, portable patterns.

- You debug memory corruption, UB, or performance issues.

## Safety Defaults Table

| Category | Rule |
|----------|------|
| Warnings | `-Wall -Wextra -Wpedantic -Werror` |
| Memory | Every `malloc` paired with `free`; check return value |
| Strings | `snprintf` not `sprintf`; bound all buffer writes |
| Integers | `stdint.h` types (`uint32_t`); check for overflow |
| Pointers | NULL-check before dereference; no OOB arithmetic |
| Error handling | Check all return values; propagate errors explicitly |

## Workflow

### 1. Safety defaults

- Initialize all variables; bounds-check all array accesses.

- Avoid dangerous APIs (`gets`, `strcpy`, `sprintf`).

- Compile with: `gcc -Wall -Wextra -Wpedantic -Werror -fsanitize=address,undefined`.

### 2. Error handling

- Use clear error codes; single exit via `goto cleanup` for resource management.

- Check return values of `malloc`, `fopen`, syscalls, and library functions.

### 3. Memory discipline

- Document ownership at every allocation site.

- Enforce alloc/free symmetry; use `valgrind` for leak detection.

### 4. Tooling

- Compiler warnings + sanitizers (ASan/UBSan) in local builds.

- Static analysis: `clang-tidy`, `cppcheck`, or `splint`.

- Fuzzing for input-handling code: `libFuzzer` or `AFL++`.

### 5. Testing

- Minimal harness for critical functions.

- Regression test for every bug fixed.

## Self-check

- [ ] All warnings enabled and treated as errors (`-Werror`).

- [ ] AddressSanitizer and UBSanitizer run locally.

- [ ] Every allocation has a matching free with documented ownership.

- [ ] All function return values checked.

- [ ] Regression test added for each bug fixed.

## Outputs

- Safe C checklist.

- Debugging plan (warnings/sanitizers).

- Testing harness suggestions.
