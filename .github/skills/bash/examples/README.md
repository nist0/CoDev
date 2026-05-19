# Bash Skill — Examples

## 1. Safe Script Skeleton

```bash
#!/usr/bin/env bash
set -euo pipefail
main() {
echo "Hello, world!"
}
main "$@"
```

## 2. Linting with ShellCheck

```text
shellcheck my_script.sh
```

## 3. CI Integration (GitHub Actions)

```yaml
- name: Lint Bash scripts
run: shellcheck scripts/*.sh
```
