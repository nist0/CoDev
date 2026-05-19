---
name: instruction-authoring
description: Create scoped instruction files (*.instructions.md) with clear applyTo patterns and non-duplicated rules.
argument-hint: "[scope] [rules]"
user-invocable: true

disable-model-invocation: false
---

# instruction-authoring Skill (Elite)

## When to use

- Adding or updating `.github/instructions/*.instructions.md`.

- Creating per-language, per-domain, or repo-wide standards.

- Enforcing security, quality, or style constraints on all AI-generated output.

## Procedure

### Domain research (mandatory for new domains/themes)

Before writing any rules, gather authoritative references for the domain or technology this instruction targets:

1. **Identify the domain**: name it explicitly (e.g. "C# async patterns", "Helm chart standards", "React component design").

2. **Gather ≥2 primary sources**: official documentation, language specs, RFC/standards, canonical style guides. Prioritise primary over aggregated/secondary sources.

3. **Read related CoDev assets**: scan existing instructions, skills, and agents that touch the same domain to avoid contradiction and duplication.

4. **Synthesise best practices**: extract the non-contradictory union. Where sources conflict, document the choice — *"Source A recommends X; Source B recommends Y — using X because `<rationale>`."*

5. **Cite sources**: inline-link primary references at the top of the instruction file or in the relevant rule where domain-specific constraints are stated.

> Skip only if the instruction captures purely internal framework conventions with no external domain standards.

### 1. Check for existing coverage first

Before creating a new instruction file:

1. Read all files in `.github/instructions/`.

2. Read `00-core.instructions.md` — repo-wide rules always apply.

3. Check for an existing file with the same `applyTo` scope.

4. If coverage already exists: extend the existing file; do not create a duplicate.

### 2. Define a tight `applyTo` glob

| Scope | `applyTo` example |
|-------|-------------------|
| All files | `**` |
| All markdown | `**/*.md` |
| CI workflows | `.github/workflows/**/*.yml` |
| C# files only | `**/*.cs` |
| Specific folder | `src/api/**/*.ts` |

Rule: prefer the **narrowest** glob that covers the intended files without overlap.

### 3. Write the frontmatter

**Official attribute reference** — [VS Code custom-instructions docs](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) (verified 2026-03-04):

| Attribute | Required | Allowed values / notes |
| --- | --- | --- |
| `name` | No | Display name shown in UI (defaults to file name) |
| `description` | No | Short description shown on hover |
| `applyTo` | No | Glob pattern for auto-apply; omit if manual-only |

No other attributes are valid for `.instructions.md` files.

```yaml
---
name: "<short-id>"
description: "<one sentence: what this instruction enforces>"
applyTo: "<glob>"
---
```

### 4. Write actionable rules (not principles)

Good rule: `"Use FluentValidation for all request DTOs; never validate in controllers."`

Bad rule: `"Validate user input properly."`

For each rule:

- State what TO do (preferred) OR what NOT to do (when a prohibition is clearest).

- Be specific enough that a code reviewer can check it without ambiguity.

### 5. Structure the instruction file

```markdown
---
<frontmatter>
---

# <Title> (<scope>)

## <Section: e.g. "Code style">

- Rule 1
- Rule 2

## <Section: e.g. "Security">

- Rule 1
```

- Use `##` sections for grouping (style, security, testing, performance, …).

- Keep each rule to 1–2 lines; link to docs if more context is needed.

- Do not embed code examples longer than 5 lines; link to a skill or example file instead.

### 6. Avoid duplication with other instruction layers

- Never repeat rules already in `00-core.instructions.md`.

- If a rule belongs in a shared layer, add it there and reference it.

- After writing, cross-check against every existing instruction file.

### 7. Register the instruction (if required)

- If the project uses `validate-customization-registry.py`, add the new file to the registry.

- Run `python scripts/validate-customization-registry.py` to confirm.

### 8. Test the instruction (smoke check)

For each major rule in the file:

- Write 1 example that satisfies the rule.

- Write 1 example that violates the rule.

- Verify that Copilot with the instruction active follows the rule in a test prompt.

## Self-check

- [ ] Existing instruction files checked before creating a new one.

- [ ] `applyTo` is the narrowest correct glob.

- [ ] Frontmatter complete (`name`, `description`, `applyTo`).

- [ ] All rules are actionable (checkable by a reviewer).

- [ ] No duplication with `00-core.instructions.md` or other layers.

- [ ] Registry updated (if applicable).

- [ ] Smoke check performed for each major rule.

## Outputs

- New or updated `*.instructions.md` file.

- Cross-check table (new rules vs existing layers).

- Smoke check results.
