---
name: codev-contributing
description: How to propose changes to CoDev from a consumer repository -- fork, fix, PR, upstream sync, and review protocol.
argument-hint: "[type: bug|enhancement|new-skill|new-agent]"
user-invocable: true

disable-model-invocation: false
---

# Contributing to CoDev Upstream

## When to use

- You found a bug in a CoDev skill, agent, prompt, or script.

- You want to propose a new capability, agent, or skill.

- You need to sync your fork after your PR is merged upstream.

- You want to understand the CoDev governance and review protocol.

---

## 1. Decision: override vs. upstream contribution

Before opening a PR to CoDev, ask:

| Question | Yes -> | No -> |
| --- | --- | --- |
| Is this specific to my host repo? | Use `codev-overrides/` | Consider upstreaming |
| Would other consumers benefit? | Upstream it | Keep it local |
| Is it a breaking change to existing skills? | Open RFC issue first | Proceed with PR |
| Does it require a new routing capability? | Coordinate with maintainer first | Proceed with PR |

---

## 2. Contribution workflow

### Step 1 -- Open an issue on the CoDev repo

Before any code:

```bash
# In your host repo, navigate to the CoDev submodule
gh issue create --repo nist0/CoDev \
  --title "<type>: <short description>" \
  --body-file /tmp/issue-body.md
```

Issue body must include:

- **What** (observed behavior or missing feature)

- **Why** (user impact; which consumers are affected)

- **Acceptance criteria** (checkboxes)

- **Proposed approach** (optional for bugs; required for new capabilities)

> Follow the CoDev mandatory dev workflow: issue first, then branch, then PR.

### Step 2 -- Fork and branch

```bash
# Fork the repo (one-time)
gh repo fork nist0/CoDev --clone=false

# Add your fork as a remote inside the submodule
cd tools/codev
git remote add fork https://github.com/<your-username>/CoDev.git
git fetch fork

# Branch from the latest main
git checkout -b <type>/<slug>   # e.g. fix/skill-lockfile-path, feat/new-db-skill
git push fork <type>/<slug>
```

### Step 3 -- Implement the change

Follow CoDev authoring conventions:

- **Skills**: `SKILL.md` with frontmatter + procedure + examples + self-check + elite section.

- **Agents**: frontmatter `name`, `description`, with `tools` omitted unless explicitly needed; mission + responsibilities + output format + handoff.

- **Prompts**: frontmatter with `agent:` matching an existing agent `name`; `argument-hint` defined.

- **Routing**: update all four YAMLs atomically (`capabilities.yaml`, `aliases.yaml`, `matrix.yaml`, `domains.yaml` if needed).

- **Instructions**: tight `applyTo` glob; additive and non-contradictory.

Run validators before opening a PR:

```bash
python scripts/validate-route-smoke.py
python scripts/validate-customization-registry.py
python scripts/validate-readme-registry.py
python scripts/validate-routing-coverage.py
python scripts/validate-markdown-lint.py
```

All must pass (exit 0).

### Step 4 -- Open a PR to CoDev

```bash
cd tools/codev
gh pr create \
  --repo nist0/CoDev \
  --head <your-username>:<type>/<slug> \
  --base main \
  --title "<type>: <description>" \
  --body-file /tmp/pr-body.md
```

PR body must include:

- Summary of change

- Affected files

- Routing smoke-test phrases and expected outcomes

- Verification commands with expected exit codes

- `Closes #N` reference

> Use `--body-file` with a single-quoted heredoc (PowerShell) or heredoc (bash).
> Never use `--body "..."` for multi-line content -- escaping corrupts backtick spans.

### Step 5 -- Address review feedback

CoDev uses a structured review verdict:

```text
(Agent: Reviewer) approved -- rationale
(Agent: Reviewer) rework required -- <exact gap> | closure evidence: <what to show>
```

For `rework required`:

1. Read the exact gap and closure evidence.

2. Make the minimal change that satisfies the evidence.

3. Push to your branch -- the PR updates automatically.

4. Comment: `@reviewer -- addressed in <commit SHA>`.

### Step 6 -- Upstream sync after merge

Once your PR is merged into CoDev `main`:

```bash
# In your host repo: update the submodule to the merged commit
cd tools/codev
git fetch origin main
git checkout origin/main
cd ../..

# Re-sync the bootstrap
.\tools\codev\codev.ps1 update   # Windows
bash tools/codev/codev.sh update  # Linux/macOS

# Verify
python tools/codev/scripts/validate-route-smoke.py

# Commit
git add tools/codev codev-lock.json .github/copilot-instructions.md
git commit -m "chore: update CoDev submodule (includes <your fix>)"
git push
```

---

## 3. Contribution types and acceptance bars

| Type | Files typically changed | CI gate | Extra review requirement |
| --- | --- | --- | --- |
| Bug fix (skill/agent/prompt) | `SKILL.md` or `*.agent.md` | All validators + lint | Regression test phrase in smoke tests |
| New skill | `SKILL.md` + `examples/README.md` | All validators + lint | Skill documented in `README.md` skills table |
| New agent | `*.agent.md` | All validators + lint | Agent documented in `README.md` agents table |
| New capability (routing) | All 4 routing YAMLs + README | All validators + routing-coverage | At least 3 smoke-test phrases added |
| New prompt | `*.prompt.md` | All validators + lint | Prompt documented in `README.md` prompts table |
| Instruction change | `*.instructions.md` | All validators + lint | No weakening of existing guidance |

---

## 4. Communication norms

- Open an issue **before** any significant change -- do not surprise maintainers with a large PR.

- Use English for all GitHub-published content (issues, PRs, reviews, comments).

- Be specific: include exact commands, expected outputs, and reproduction steps.

- One concern per PR -- do not bundle unrelated changes.

---

## Self-check before opening a PR to CoDev

- [ ] GitHub issue opened and linked (`Closes #N`)

- [ ] All validators pass locally (exit 0)

- [ ] PR body written via `--body-file` (no `--body "..."`)

- [ ] Routing smoke-test phrases updated for any routing change

- [ ] README updated if new agents/skills/prompts added

- [ ] No secrets or credentials in any changed file

---

## Elite practices

- **Pre-mortem before PR**: list the 3 most likely review objections and address them in the PR description before opening.

- **Minimal diff**: prefer surgical changes over rewrites -- smaller diffs are reviewed faster and more thoroughly.

- **Include a "not tested" section**: explicitly state what is out of scope in your PR to signal awareness.

- **Watch the CI run**: don't open a PR and disappear -- monitor the first CI run and fix issues within 30 minutes.

- **Version your agent contracts**: if you change an agent's output format, bump `version:` in the frontmatter and update all callers.
