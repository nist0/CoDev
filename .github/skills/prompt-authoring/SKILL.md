---
name: prompt-authoring
description: Create stable, reusable prompt files (.prompt.md) with consistent structure, inputs, outputs, and acceptance criteria.
argument-hint: "[goal] [inputs] [constraints]"
user-invocable: true

disable-model-invocation: false
---

# prompt-authoring Skill (Elite)

## When to use

- Creating a new reusable prompt file in `.github/prompts/`.

- Updating an existing prompt to add structure, inputs, or a self-check.

- Migrating an ad hoc chat pattern into a repeatable slash command.

## Minimal extension workflow

Use this path when you want the shortest safe route from idea to a validated prompt file:

1. Run `/prompt-from-theme theme=<goal> intent=<what the prompt should do>`.

2. Save the generated file as `.github/prompts/<name>.prompt.md`.

3. If the prompt is referenced by routing, update `routing/matrix.yaml` plus any needed capability, alias, or domain entries in the same change.

4. Validate locally before opening a PR:

    - `python scripts/validate-customization-registry.py`

    - `python scripts/validate-readme-registry.py`

    - `python scripts/validate-markdown-lint.py`

    - `python scripts/validate-route-smoke.py` when routing changed

Minimal example:

```text
/prompt-from-theme theme="Contributor UX" intent="generate a minimal extension onboarding checklist"
```

This path stays additive: it uses the existing prompt-authoring system and validators rather than adding a new scaffold flow.

## Procedure

### Domain research (mandatory for new domains/themes)

Before writing any content, gather authoritative references for the domain or theme this prompt serves:

1. **Identify the domain**: name it explicitly (e.g. "release management", "REST API design", "AVR firmware").

2. **Gather ≥2 primary sources**: official documentation, language specs, RFC/standards, canonical style guides. Prioritise primary over aggregated/secondary sources.

3. **Read related CoDev assets**: scan existing skills, agents, and instructions that touch the same domain to avoid contradiction and duplication.

4. **Synthesise best practices**: extract the non-contradictory union. Where sources conflict, document the choice — *"Source A recommends X; Source B recommends Y — using X because `<rationale>`."*

5. **Cite sources**: add a `## Sources` section at the end of the skill this prompt drives, or inline-link references in the prompt body when domain-specific rules are stated.

> Skip only for thin orchestration prompts that delegate entirely to a skill and contain no domain-specific rules.

### 0. Naming and placement

- File MUST be placed in `.github/prompts/`.

- Filename conventions:

  - Use **kebab-case**: `my-feature.prompt.md`.

  - The file stem becomes the slash command: `my-feature.prompt.md` → `/my-feature`.

  - The `name:` frontmatter field can override the display name, but the file stem still determines the slash trigger.

- One prompt per file; one clear capability per prompt.

- If the prompt is purely for sub-agent consumption (not user-facing), set `user-invocable: false` in frontmatter.

### 1. Check for existing prompts first

1. List `.github/prompts/` directory.

2. Check if a prompt covering the same goal already exists.

3. If so: extend it; do not create a duplicate.

4. Review `routing/matrix.yaml` to see if a prompt is already referenced for the same capability.

### 2. Define goal and success criteria

- **Goal**: one-sentence summary of what the prompt achieves.

- **Success criteria** (falsifiable): what does a correct output look like? What would a reviewer accept?

### 3. Define the prompt frontmatter

**Official attribute reference** — [VS Code prompt-files docs](https://code.visualstudio.com/docs/copilot/customization/prompt-files) (verified 2026-03-04):

| Attribute | Required | Allowed values / notes |
| --- | --- | --- |
| `description` | No | Short description shown in `/` menu |
| `name` | No | Display name (defaults to file name) |
| `argument-hint` | No | Hint shown in chat input |
| `agent` | No | `ask`, `agent`, `plan`, or a custom agent name |
| `model` | No | Model name string or array |
| `tools` | No | List of tool/tool-set names — **omit entirely to inherit agent tools** |

**`agent` attribute decision rule:**

| Scenario | Value to use |
| --- | --- |
| Analysis, Q&A, explanation, no tool use needed | `ask` |
| Multi-step execution that needs tools (file reads, terminal, gh CLI) | `agent` |
| Specialist workflow with a dedicated agent (e.g. PromptSmith, Reviewer) | custom agent name from `.github/agents/` |
| No `agent:` set | Inherits the currently active chat mode |

Rule of thumb: if the prompt body says "run", "create", "edit a file", or "execute" → use `agent`. If it says "explain", "analyze", "review" without changing state → use `ask`.

**Prohibited / deprecated attributes** — do not use:

| Attribute | Status | Replacement |
| --- | --- | --- |
| `mode` | Deprecated | Use `agent: ask` / `agent: agent` instead |
| `skills` | Not valid | Reference skills in the body: `Apply the procedure from .github/skills/<name>/SKILL.md.` |
| `tools: []` | Anti-pattern | Omit `tools:` entirely to inherit agent tools (empty list zeroes out all tools) |

```yaml
---
description: "<one sentence: what this prompt does and when to use it>"
name: "<slug-used-after-slash>"
argument-hint: "<free-text or ${input:name:placeholder} hint>"
agent: ask                   # optional; values: ask | agent | plan | <custom-agent-id>
# model: ...                 # optional; omit to use the selected model
# tools: [specific, tools]   # only set when deliberately overriding agent tools
---
```

### 4. Define inputs

- Use `${input:name:description}` for required user inputs.

- List optional context the user can provide.

- Keep inputs minimal: prompt must be usable without extra effort.

### 5. Write the prompt body

Structure:

```text
# <Title>

<1-2 sentence setup / context for the LLM>

## Task
<clear, actionable instruction using ${input:...}>

## Constraints
- Constraint 1
- Constraint 2

## Output format
<exactly what the LLM should produce: sections, format, level of detail>
```

- Prefer procedural prompts ("do this, then this") over open-ended instructions.

- Reference skill files when the agent needs deeper knowledge: `See: .github/skills/<theme>/SKILL.md`.

### 6. Add a self-check section

Include at the end of the prompt (the LLM will use it to validate its own output):

```markdown
## Self-check
- [ ] ...
- [ ] ...
```

### 7. Add an agent delegation chain (mandatory for non-trivial prompts)

Every prompt that triggers multi-step work MUST include a delegation chain table so the executing agent knows exactly how to hand off. Place it at the end of the prompt body, after the self-check:

```markdown
## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **<specialist>** | always — <task> | *(this prompt)* | <artifact produced> |
| 2 | **Reviewer** | output ready | `/pr-review` | No blockers, `validate-customization-registry.py` passes |
| 3 | **Delivery Lead** | PR ready | — | PR merged, branch deleted |
```

Omit the table only for simple Q&A-style prompts that produce no artifacts and require no follow-on actions.

### 8. Smoke-test the prompt before committing

1. Save the file.

2. In VS Code chat, type `/<your-prompt-name>` and confirm it appears in the autocomplete picker.

3. Invoke it with representative inputs; verify the output matches the `## Output format` section.

4. If the prompt takes `${input:...}` parameters, test with both typical and edge-case values.

5. Fix any output drift before proceeding.

### 9. Register in routing (if new capability or domain)

- If the prompt covers a new capability: add to `routing/capabilities.yaml`.

- If new domain: add to `routing/domains.yaml`.

- Add alias triggers to `routing/aliases.yaml`.

- Map to agent in `routing/matrix.yaml`.

- Run smoke test: `python scripts/validate-route-smoke.py`.

### 10. Register in customization registry

- Run all three validators after adding the file:

  ```powershell
  python scripts/validate-customization-registry.py
  python scripts/validate-readme-registry.py
  python scripts/validate-markdown-lint.py
  ```

- Add entry to `README.md` prompts table (required; `validate-readme-registry.py` will fail otherwise).

- All three must exit 0 before opening a PR.

## Self-check (authoring)

- [ ] Existing prompts checked before creating a new one (Step 1).

- [ ] File is in `.github/prompts/`, kebab-case stem, one capability per file (Step 0).

- [ ] Frontmatter complete: `description` present; `agent:` chosen per decision rule (Step 3).

- [ ] `mode:` is **not** used (deprecated — use `agent: ask` or `agent: agent` instead).

- [ ] `tools: []` is **not** used (anti-pattern — omit to inherit agent tools).

- [ ] Inputs use `${input:...}` syntax; ≤ 3 required inputs (Step 4).

- [ ] Output format section clearly defines what the LLM should produce (Step 5).

- [ ] Prompt body prefers procedural instructions over open-ended ones (Step 5).

- [ ] Prompt references the relevant skill file(s) when deeper knowledge is needed (Step 5).

- [ ] Self-check section added to the prompt body (Step 6).

- [ ] Agent delegation chain table included for non-trivial prompts (Step 7).

- [ ] Prompt smoke-tested in VS Code chat with representative inputs (Step 8).

- [ ] Routing updated if new capability/domain (Step 9).

- [ ] All three registry validators pass: `validate-customization-registry.py`, `validate-readme-registry.py`, `validate-markdown-lint.py` (Step 10).

- [ ] README.md prompts table updated.

## Outputs

- New or updated `.github/prompts/*.prompt.md` file.

- Routing update (if applicable).

- Registry validation result (all three validators green).

---

## 🏆 Elite Section — Top 5% Prompt-Authoring Practices

- **Description as the first line of defense**: the `description:` field is what users see in the `/` picker. It should encode *when* to invoke the prompt, not just what it does. Good: `"Use after a bug report to produce a repro-first triage plan."` Bad: `"Triage bugs."`

- **Input economy (≤ 3 rule)**: every required `${input:...}` adds friction. If you need more than 3, the prompt is doing too much — split it. Optional context (files, issue numbers) should be mentioned in prose, not as mandatory inputs.

- **Determinism cues**: open-ended prompts produce inconsistent outputs. Anchor the LLM with exact output structures: section headings, table column names, severity labels (`blocker` / `major` / `minor`), and explicit exit conditions.

- **Prompt length discipline**: a prompt longer than ~60 lines is a red flag. Long prompts usually mean the prompt is duplicating skill content. Extract the procedure into a skill file and reference it: `Apply the procedure from .github/skills/<theme>/SKILL.md.`

- **Idempotent re-invocation**: a well-authored prompt can be run twice on the same input and produce the same structure. If re-running would produce contradictory output, the output format is under-specified.

- **Version the intent, not the implementation**: when a prompt body needs to change significantly, update it in place and log the rationale in a comment block or the linked issue — do not create a v2 file.
