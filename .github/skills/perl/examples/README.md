# Perl Skill — Examples
## 1. Safe Script Skeleton
```perl
use strict;
use warnings;
print "Hello, world!\n";
```
## 2. Linting with Perl::Critic
```text
perlcritic my_script.pl
```
## 3. CI Integration (GitHub Actions)
```yaml
- name: Lint Perl scripts
run: perlcritic scripts/*.pl
```
