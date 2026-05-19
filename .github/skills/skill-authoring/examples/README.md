# Skill Authoring — Examples
## 1. Minimal Skill Structure
```text
.github/skills/my-skill/
SKILL.md
onboarding.md
examples/README.md
tools/
```
## 2. SKILL.md Frontmatter
```text
---
name: my-skill
description: My skill description
user-invokable: true
---
```
## 3. Validation Command
```sh
python scripts/validate-customization-registry.py
```
