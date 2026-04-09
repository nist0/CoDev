---
name: prompt-engineering
description: Prompt engineering for the Copilot Dev Framework - intent, constraints, context, deterministic output, verification, and framework change protocol.
argument-hint: "[task type: triage|generate|review|plan|refactor|explain]"
user-invocable: true
disable-model-invocation: false
---

# Prompt Engineering (Copilot Dev Framework) (Elite)

## When to use

- You need consistent prompts that produce deterministic, reviewable outputs.
- You want prompts that work well with routing (capability + domain).
- You want to reduce ambiguity and hallucinations.

## Good Prompt Quality Criteria

| Dimension | Question to ask |
|-----------|----------------|
| Intent | Is the task type explicit? (triage, generate, review, plan) |
| Constraints | Are tech stack, style rules, and output format specified? |
| Context | Are concrete files/symbols/errors referenced? |
| Determinism | Does it ask for checklists/steps/command blocks? |
| Verification | Does it include "how to validate" section? |
| Security | No secrets, no broad permissions, no destructive defaults? |

## Workflow

### 1. Define intent

- "What is the task?" (triage, generate, review, plan, refactor, explain).
- Pick the right interaction mode for the task size/complexity.

### 2. Provide constraints

- Tech stack, style rules, safety constraints, output format.

### 3. Provide context

- Minimal necessary inputs: file paths, errors, requirements, expected behavior.
- Reference concrete files/symbols when possible.

### 4. Ask for deterministic output

- Checklists, steps, command blocks, file content blocks.

### 5. Add verification

- "How to validate" section (tests/commands/CI).

### 6. Iterate with deltas

- Encourage "apply patch" style edits rather than rewriting everything.

### 7. Review and secure

- Check edge cases, error handling, and security-sensitive behavior.

## Capability/agent/skill/prompt/instruction change protocol

When adding a capability or AI capability in this framework:

1) Scope first
   - Define user outcomes, non-goals, and acceptance criteria.
2) Prefer stable roles
   - Reuse existing agents when possible; add new agents only for truly new roles.
3) Modular artifacts
   - Add leaf `SKILL.md` modules and narrowly scoped prompts.
4) Deterministic routing
   - Update `routing/capabilities.yaml`, `routing/aliases.yaml`, and `routing/matrix.yaml`.
5) Keep instructions concise
   - Put global rules in core instructions; use scoped `applyTo` files for specifics.
6) Verify and document
   - Run validators; update docs and examples for discoverability.

## Self-check

- [ ] Intent is explicit (task type stated clearly).
- [ ] Constraints include tech stack and output format.
- [ ] Context references concrete files/symbols/errors (not vague descriptions).
- [ ] Output asks for deterministic format (checklist/steps/commands).
- [ ] Verification guidance included.
- [ ] No secrets or broad destructive permissions in prompt.

## Outputs

- A prompt pattern library (intent -> template).
- A "good prompt" checklist.
- Suggested prompt file structure for `/` commands.
- A reusable checklist for adding capabilities/agents/skills/prompts/instructions.
