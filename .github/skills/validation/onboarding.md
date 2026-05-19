# Onboarding: Validation Skill

Welcome to the validation skill! This guide helps you run, extend, and integrate validation scripts for CI and contributor workflows.

## Quickstart Checklist

1. Read [SKILL.md](SKILL.md) for validation procedures and integration patterns.

2. Use tools in the tools/ directory for running all validators or individual checks.

3. See [examples/README.md](examples/README.md) for usage patterns and CLI invocations.

4. Integrate validation scripts into CI for automated checks.

## Integration Patterns

- Use with doc-qa for documentation validation.

- Combine with repo-inventory for file enumeration and targeted validation.

- Reference validation scripts in PR templates and contributor guides.

## Troubleshooting

- **Validator fails unexpectedly?**

- Check script output for error details.

- Ensure all dependencies are installed in your environment.

- **CI not running validators?**

- Confirm scripts are referenced in the workflow YAML.

## Resources

- [SKILL.md](SKILL.md): Full validation procedure and best practices.

- [examples/README.md](examples/README.md): CLI usage and integration patterns.

- [repo-inventory/SKILL.md](../repo-inventory/SKILL.md): File listing and filtering for validation.
_Last reviewed: 2026-05-19_
