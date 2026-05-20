---
name: diagram-tooling
description: Produce, modify, validate, and convert architecture diagrams with PlantUML, Mermaid, and open-source tooling.
argument-hint: "[format] [source] [target]"
user-invocable: true

disable-model-invocation: false
---

# diagram-tooling Skill (Elite)

## When to use

- You need architecture or flow diagrams as code.

- You need conversions across PlantUML, Mermaid, SVG, or PNG.

- You need reproducible diagram updates in PR workflows.

> **Mermaid-first on GitHub**: if the diagram will live in a GitHub Markdown file (README, ADR, wiki), prefer Mermaid -- it renders natively without any plugin. For comprehensive Mermaid guidance (all diagram types, best practices, CI validation), see the dedicated [`mermaid` skill](.github/skills/mermaid/SKILL.md) and use `/mermaid-create`, `/mermaid-review`, or `/mermaid-embed` prompts.

## Source Format Reference

| Format | Strengths | Use when |
|--------|-----------|----------|
| PlantUML (`.puml`) | Rich diagram types (sequence, class, component, deployment) | Complex architecture diagrams, C4 in PlantUML |
| Mermaid (`.mmd`) | GitHub-native rendering, low-friction syntax | Any diagram embedded in GitHub Markdown |
| D2 (`.d2`) | Clean syntax, modern look | Architecture diagrams where D2 tooling is available |
| SVG | Vector, scalable, diffable | Exports for docs/ADRs |
| PNG | Universal compatibility | When SVG not supported |

### Mermaid quick-reference (common types)

| Mermaid type | Keyword | Use when |
|---|---|---|
| Flowchart | `flowchart LR` | Process flows, pipelines |
| Sequence | `sequenceDiagram` | API/actor interactions |
| Class | `classDiagram` | Domain models |
| ER | `erDiagram` | Database schema |
| State | `stateDiagram-v2` | Lifecycle / FSM |
| Git graph | `gitGraph` | Branch/merge history |
| C4 Context | `C4Context` | Architecture context views |

> For the full Mermaid type reference, theming, accessibility, and CI validation, see the [`mermaid` skill](.github/skills/mermaid/SKILL.md).

## Procedure

### 1. Pick canonical source format

- Prefer text-based diagram sources committed in repo (`.puml`, `.mmd`).

- Keep generated binaries (`.png`, `.svg`) derived and reproducible.

### 2. Author or modify diagrams

- Use clear node IDs and stable grouping.

- Keep naming aligned with repository vocabulary.

### 3. Validate renderability

- Render diagrams locally/CI and fail on syntax errors.

- Keep deterministic outputs for review diffs.

### 4. Convert/export

- Support exports for docs and ADRs (SVG preferred; PNG when required).

- Preserve source files as the editable truth.

### 5. Review quality

- Check readability, layout clarity, and stale references.

- Ensure links or references in docs point to source + rendered output.

## Self-check

- [ ] Source files (`.puml`/`.mmd`) versioned in repo.

- [ ] Render steps are deterministic and run in CI.

- [ ] Doc links reference the canonical source.

- [ ] Diagram naming is consistent with repo vocabulary.

- [ ] SVG/PNG exports are reproducible from source.

## Deliverables

- Diagram source updates (`.puml`/`.mmd`).

- Export strategy (`.svg`/`.png`) with reproducible steps.

- Diagram QA checklist.
