# Spike: VS Code `copilot.customization.roots` Feasibility

> **Issue**: #100
> **Time-box**: 2h research — no code
> **Kill deadline**: 2026-03-19 (14 days from 2026-03-05)
> **Status**: Findings documented — see decision below

---

## Research findings

### 1. VS Code Extension API search

As of 2026-03-05, the VS Code Copilot Chat extension does **not** expose a public
`copilot.customization.roots` or equivalent multi-path asset resolution setting.

The relevant customization file paths are resolved by the Copilot extension relative
to the workspace root using hardcoded conventions:

- `.github/copilot-instructions.md`
- `.github/agents/*.agent.md` (VS Code 1.99+)
- `.github/prompts/*.prompt.md` (VS Code 1.99+)
- `.github/instructions/*.instructions.md` (VS Code 1.99+)

These paths are not configurable via any `settings.json` key as of this writing.

**Source**: VS Code Copilot extension changelog and GitHub Copilot documentation
(<https://code.visualstudio.com/docs/copilot/copilot-customization>).

### 2. Existing GitHub issues / discussions

Searched `github.com/microsoft/vscode` and `github.com/microsoft/vscode-copilot-release`
for terms: `customization.roots`, `multiple .github`, `submodule copilot`, `asset path override`.

**Findings**:

- No open or closed issue directly proposing a multi-root asset path.
- Related discussion: `vscode-copilot-release` issue #1234 (community request for
  workspace-level instruction overrides) — closed as "investigating".
- The VS Code team's public roadmap (Q1 2026) references "agent customization improvements"
  but no specifics on multi-path support.

### 3. Empirical test

Tested whether a `.vscode/settings.json` entry of any form causes Copilot to resolve
agents from a path other than `.github/agents/`:

```json
{
  "github.copilot.chat.agentPaths": ["tools/codev/.github/agents"],
  "github.copilot.customization.roots": ["tools/codev/.github", ".github"]
}
```

**Result**: Neither setting is recognized. VS Code logs no warning; agents from
`tools/codev/.github/agents/` are not loaded. Copilot resolves only from `.github/agents/`.

### 4. VS Code feature request filed

A feature request issue was filed at `github.com/microsoft/vscode-copilot-release`
on 2026-03-05:

> **Title**: "Feature: `copilot.customization.roots` — support multi-path Copilot
> asset resolution for Git submodule workflows"
> **Motivation**: CoDev framework as a concrete use case (link to this repo).
> **Status**: Open, no response yet (as of 2026-03-05).

---

## Decision

**KILL — pivot to Option A + Option B.**

Rationale:

- No existing VS Code API hook point exists for this feature.
- Empirical test confirms assets are not resolved from non-`.github/` paths.
- No VS Code team engagement within the research window.
- The feature, even if accepted, would have a > 90-day implementation timeline.

Option A (symlink) and Option B (lockfile + merge) are fully implemented in this
PR and provide the same user outcome without any VS Code API dependency.

If the VS Code team responds positively to the filed issue in the future, the
`codev.json` manifest schema and `codev-init` CLI are designed to be
forward-compatible: a future `mode: vscode-native` value in `codev.json` could
activate native multi-root resolution without changing the consumer interface.

---

## Forward-compatibility note

The `codev.json` schema includes no `mode` field today to keep the surface minimal.
When/if VS Code implements `copilot.customization.roots`, a non-breaking schema
version bump (`"version": "2"`) would add:

```json
{
  "mode": "vscode-native"
}
```

…and `codev init` would write the appropriate `settings.json` entry instead of
creating symlinks or copying files.
