---
name: skill-authoring
description: Author, structure, and maintain high-quality Copilot skills with onboarding, examples, and tools.
user-invocable: true
---
## When to use
- When creating a new skill for the Copilot Dev Framework.
- When refactoring or improving an existing skill to meet elite standards.
- When onboarding contributors to skill authoring best practices.
## Procedure
1. **Plan the skill**
- Define the skill's purpose, scope, and audience.
- Choose a clear, unique skillId (kebab-case).
2. **Create the skill structure**
- Folder: `.github/skills/<skillId>/`
- Files: `SKILL.md`, `onboarding.md`, `examples/README.md`, `tools/` (if needed)
3. **Write SKILL.md**
- Add frontmatter: `name`, `description`, `user-invokable`.
- Sections: When to use, Procedure, Self-check.
4. **Author onboarding.md**
- Quickstart checklist, troubleshooting, resources.
5. **Populate examples/README.md**
- At least 3 actionable, copy-paste-ready examples.
- Cover common, advanced, and edge-case usage.
6. **Add tools/**
- Include scripts or references for validation, linting, or automation (Python, .mjs, etc.).
7. **Integrate with routing and agents/prompts**
- Update `routing/capabilities.yaml`, `routing/matrix.yaml`, and other routing files if the skill is directly invokable.
- Check if the skill should be referenced by agents or prompts; update their files accordingly.
8. **Validate**
- Run all validation scripts (see Self-check).
- Ensure no duplication, clear structure, and discoverability.
## Self-check
- [ ] All required files present: SKILL.md, onboarding.md, examples/README.md, tools/ (if needed)
- [ ] Examples are concrete and runnable
- [ ] Onboarding is clear and actionable
- [ ] Validation scripts pass
- [ ] No duplication with existing skills
- [ ] Routing integration considered and updated if needed
- [ ] Agent/prompt integration considered and updated if needed
