---
name: vscode
description: VS Code Copilot Dev Framework usage — bootstrap, reload, discoverability, multi-root workspaces, and troubleshooting.
argument-hint: "[issue or feature: bootstrap|reload|routing|troubleshoot]"
user-invocable: true

disable-model-invocation: false
---

# VS Code (Copilot Dev Framework Usage) (Elite)

## When to use

- You need to ensure Copilot Dev Framework is loaded correctly in VS Code.

- You want best practices for working with prompts, agents, and skills.

## Framework Validation Checklist

| Check | How to verify |
|-------|---------------|
| Bootstrap ran | Check for `.github/` folder with agents/prompts/skills |
| Window reloaded | `Ctrl+Shift+P` > `Developer: Reload Window` |
| Prompts visible | Type `/` in Copilot Chat; look for custom prompts |
| Routing works | `/route <request>` returns a capability + agent |
| Instructions loaded | Files in `.github/instructions/` match `applyTo` globs |

## Workflow

### 1. Bootstrap integration

- Run `copilot_dev/bootstrap/bootstrap.ps1` or `.sh`.

- Confirm `.github/` folder structure is present.

### 2. Reload

- Reload window after bootstrap: `Ctrl+Shift+P` > `Developer: Reload Window`.

### 3. Discoverability

- Use `/route` to select agent/prompt/skill.

- Verify prompts appear in the slash command list.

### 4. Multi-root workspaces

- Ensure `.code-workspace` settings contain `chat.*FilesLocations` pointing to the CoDev repo.

- Add all relevant workspace folders.

### 5. Troubleshooting

- Confirm settings paths; ensure submodule exists and is updated.

- If prompts missing: reload window, verify path in workspace settings.

- If routing fails: check `routing/matrix.yaml` for the capability/domain pair.

## Self-check

- [ ] Bootstrap script ran successfully.

- [ ] Window reloaded after bootstrap.

- [ ] Custom prompts appear in `/` slash command list.

- [ ] `/route` returns expected capability + agent + skills.

- [ ] `.code-workspace` has correct paths for multi-root usage.

## Outputs

- Checklist to validate framework is active.

- Troubleshooting steps for missing prompts/agents.

- Recommended daily usage flow.
