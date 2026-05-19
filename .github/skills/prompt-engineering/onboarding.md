# Onboarding: Prompt Engineering

Welcome to the prompt-engineering skill! This guide will help you design, structure, and maintain high-quality Copilot prompts.

## Quickstart Checklist

1. Read [SKILL.md](SKILL.md) for core patterns and procedures.

2. Review [examples/README.md](examples/README.md) for practical prompt engineering patterns.

3. Identify your prompt's goal, required inputs, and expected outputs.

4. Choose the right agent and reference any required skills.

5. Draft your prompt using the recommended structure and output format.

6. Test your prompt with realistic inputs and review the output.

7. Update routing and smoke tests if you add or change a prompt.

## Troubleshooting

- **Prompt not invoking tools/skills?**

- Check that skills are referenced in the body, not frontmatter.

- Ensure the agent supports the required tools.

- **Argument not working?**

- Use `${input:argumentName}` and set `argument-hint` in frontmatter.

- **Output not deterministic?**

- Use explicit markdown sections and code blocks.

## Resources

- [SKILL.md](SKILL.md): Full procedure and best practices.

- [examples/README.md](examples/README.md): Copy/paste-ready prompt patterns.

- [prompt-authoring/SKILL.md](../prompt-authoring/SKILL.md): Writing prompt files.

- [agent-authoring/SKILL.md](../agent-authoring/SKILL.md): Agent design.
_Last reviewed: 2026-05-19_
