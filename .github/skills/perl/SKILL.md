---
name: perl
description: Perl scripting — safety pragmas, error handling, clear structure, and documentation.
argument-hint: "[script name or automation goal]"
user-invocable: true

## disable-model-invocation: false

# Perl Scripting (Elite)

## When to use

- Writing Perl scripts for text processing, automation, or legacy tooling.

## Safe Skeleton

```perl
#!/usr/bin/env perl
use strict;
use warnings;
use Carp qw(croak);

main();

sub main {
    # ...
}
```

## Workflow

### 1. Always use strict and warnings

- `use strict; use warnings;` — mandatory, no exceptions.

- Add `use Carp qw(croak confess)` for better error reporting.

### 2. Clear variable names and subroutines

- Avoid `$_` as the loop variable in complex code; name it explicitly.

- Break logic into named subroutines with a single purpose.

### 3. Error handling

- Use `die` with actionable messages: `die "Cannot open $file: $!\n"`.

- Use `eval { ... } or die $@` for exception handling.

- Check return values of `open`, `close`, `system`, etc.

### 4. Document usage

- Add POD (`=head1 SYNOPSIS`) or at minimum a comment block with usage.

## Self-check

- [ ] `use strict; use warnings;` at the top.

- [ ] All variables declared with `my`.

- [ ] Return values of `open`, `close`, `system` checked.

- [ ] `die` messages include `$!` (errno) where relevant.

- [ ] Script has usage comment or POD documentation.

## Outputs

- Script skeleton.

- Common idioms reference.

- Usage examples.
