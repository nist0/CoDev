---
name: skill-improving
description: Audit, enhance, and refactor Copilot skills to meet elite quality standards.

## user-invocable: true

## When to use

- When reviewing or improving an existing skill.

- When migrating scripts or examples into a skill.

- When onboarding contributors to skill improvement best practices.

## Procedure

1. **Audit the skill**

- Check for onboarding.md, examples/README.md, tools/.

- Review SKILL.md for clarity, completeness, and structure.

2. **Enhance documentation**

- Add or update onboarding.md with quickstart and troubleshooting.

- Ensure examples/README.md has at least 3 actionable examples.

3. **Add or update tools/**

- Include scripts for validation, linting, or automation as needed.

4. **Integrate with routing and agents/prompts**

- Update `routing/capabilities.yaml`, `routing/matrix.yaml`, and other routing files if the skill is directly invokable.

- Check if the skill should be referenced by agents or prompts; update their files accordingly.

5. **Validate**

- Run all validation scripts (see Self-check).

- Ensure no duplication, clear structure, and discoverability.

## Self-check

- [ ] All required files present and up to date

- [ ] Examples are concrete and runnable

- [ ] Onboarding is clear and actionable

- [ ] Validation scripts pass

- [ ] No duplication with existing skills

- [ ] Routing integration considered and updated if needed

- [ ] Agent/prompt integration considered and updated if needed
