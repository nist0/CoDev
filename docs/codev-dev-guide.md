# codev-dev contributor guide

`scripts/codev-dev.py` is the interactive developer CLI for CoDev. It provides
guided contributor flows, routing exploration, repository health checks, and
agent scaffolding with zero risk of accidental side effects unless the user
chooses a later write or publish step outside the CLI preview.

## Commands at a glance

| Command | What it does | Writes files? |
| --- | --- | --- |
| `test-route "<phrase>"` | Show routing result for any phrase | Never |
| `guide route "<request>"` | Preview the best next routing command for a request | Never |
| `guide extension --kind <kind>` | Preview the shortest extension onboarding path | Never |
| `guide issue --title ... --summary ...` | Preview a governance-compliant issue body | Never |
| `guide test-plan --what ... --why ...` | Preview a test-plan block with CI gate | Never |
| `guide pr-checklist --issue N` | Preview a PR checklist body | Never |
| `test-route --list` | List all registered aliases by capability | Never |
| `doctor` | Check required files and run all validators | Never |
| `new agent <name>` | Scaffold a new agent file (dry-run by default) | Only with `--write` |

> `test-route`, `guide`, and `doctor` are **100% read-only**. `new agent`
> dry-runs by default and **never overwrites** an existing file.

## Guided contributor flows

Issue `#40` adds preview-first workflows for the contributor tasks that were
previously spread across issue templates, testing guidance, and PR review
instructions.

```bash
# Route selection
.venv\Scripts\python.exe scripts/codev-dev.py guide route "debug kubernetes pod"

# Extension onboarding path
.venv\Scripts\python.exe scripts/codev-dev.py guide extension --kind agent

# Issue preparation
.venv\Scripts\python.exe scripts/codev-dev.py guide issue --title "Add guided CLI flow" --summary "Help contributors prepare issue bodies"

# Test-plan preparation
.venv\Scripts\python.exe scripts/codev-dev.py guide test-plan --what "guided route flow" --why "Contributors need exact next commands"

# PR checklist preparation
.venv\Scripts\python.exe scripts/codev-dev.py guide pr-checklist --issue 40
```

Each flow prints exact next commands and a dry-run preview block. Nothing is
written to disk, and no GitHub publication happens automatically.

## Contributor profiles via `/quickstart`

Issue `#42` adds four ready-to-use contributor profiles that keep first-run requests on onboarding while biasing the generated card toward a stable contribution style.

| Profile | Use when | Designated agent | Prompt sequence | Validation | Rollback |
| --- | --- | --- | --- | --- | --- |
| `maintenance` | validator drift, repo hygiene, release or governance upkeep | `Delivery Lead` | `/quickstart` -> `/pr-review` -> `/route <maintenance task>` | `.venv\Scripts\python.exe scripts/validate-customization-registry.py`, `.venv\Scripts\python.exe scripts/validate-readme-registry.py`, `.venv\Scripts\python.exe scripts/validate-markdown-lint.py`, plus route smoke when routing changed | fall back to `/route <task>` if implementation work grows |
| `fast-feature` | additive prompt, skill, alias, or capability work | `Architect` | `/quickstart` -> `/route <feature request>` -> `/<best-matching prompt>` | targeted tests plus the validators touched by the change | switch to `safe-refactor` when behaviour preservation becomes the main risk |
| `safe-refactor` | behaviour-preserving cleanup or test-first restructuring | `Architect` | `/quickstart` -> `/test-plan` -> `/route <refactor request>` | regression coverage plus touched validators | narrow to `maintenance` when the change becomes hygiene-only |
| `doc-only` | README, docs, prompt copy, and instruction wording | `Delivery Lead` | `/quickstart` -> `/doc-lint-fix` -> `/route <docs task>` | `.venv\Scripts\python.exe scripts/validate-markdown-lint.py` and `.venv\Scripts\python.exe scripts/validate-readme-registry.py` when inventory docs change | fall back to `/route <task>` if routing or code changes appear |

Use the explicit phrases below to avoid routing ambiguity:

```text
/quickstart maintenance contributor profile for validator cleanup
/quickstart fast-feature contributor profile for a new prompt
/quickstart safe-refactor contributor profile for route cleanup
/quickstart doc-only contributor profile for README cleanup
```

## Guided extension onboarding

Issue `#43` adds a minimal extension path for contributors who want the shortest safe route from idea to validated asset.

```bash
# Agent path
.venv\Scripts\python.exe scripts/codev-dev.py guide extension --kind agent

# Skill path
.venv\Scripts\python.exe scripts/codev-dev.py guide extension --kind skill

# Prompt path
.venv\Scripts\python.exe scripts/codev-dev.py guide extension --kind prompt

# Instruction path
.venv\Scripts\python.exe scripts/codev-dev.py guide extension --kind instruction
```

The preview points to the matching slash prompt, the expected output path, and the exact validator commands to run before PR review.

## Assistive guardrails

Issue `#41` makes validator and CLI failures more actionable without weakening
the underlying checks.

### Before and after: route smoke failure

Before:

```text
Route smoke validation failed: 1 issue(s) across 37 case(s).
 - [case 3] no capability matched for request='add a new agent'
```

After:

```text
Route smoke validation failed: 1 issue(s) across 37 case(s).
 - [case 3] no capability matched for request='add a new agent'
Next actions:
 - Replay the failing phrase with: python scripts/codev-dev.py test-route "add a new agent"
 - Review routing/aliases.yaml and routing/route-smoke-tests.yaml for the missing alias coverage.
 - Re-run: python scripts/validate-route-smoke.py
```

### Before and after: customization registry failure

Before:

```text
Customization registry validation failed:
 - routing rule #7 references unknown agent: Missing Agent
```

After:

```text
Customization registry validation failed:
 - routing rule #7 references unknown agent: Missing Agent
Next actions:
 - Review routing/matrix.yaml, routing/capabilities.yaml, routing/aliases.yaml, and routing/domains.yaml for the referenced ID mismatch.
 - Re-run: python scripts/validate-customization-registry.py
 - Optional overview: python scripts/codev-dev.py doctor --validators registry
```

### Write-capable preview guardrail

`new agent --write` still prints the full generated file preview before the
write happens, and now labels that execution mode explicitly so the last step is
obvious before any file is created.

---

## Persona walkthroughs

### Persona 1 — Junior developer (first contribution to CoDev)

**Goal**: understand what the framework does, find the right agent for a task,
and make a first routing contribution.

**Before `codev-dev`** (15 steps): open README → read capabilities.yaml →
read aliases.yaml → read domains.yaml → read matrix.yaml → open each agent
file → run 4 validators separately → cross-reference results manually.

**After `codev-dev`** (5 commands):

```bash
# 1. Health check — is the repo in a clean state?
./.venv/bin/python scripts/codev-dev.py doctor
#    ✅ 8 required files present
#    ✅ 5/5 validators pass

# 2. Explore what phrases are already handled
./.venv/bin/python scripts/codev-dev.py test-route --list
#    Displays all aliases grouped by capability

# 3. Test your specific request
./.venv/bin/python scripts/codev-dev.py test-route "debug kubernetes pod"
#    Capability   debugging   (matched alias: "bug")
#    Domain       devops-cloud   (matched keyword: "kubernetes")
#    Agent        DevOps/Cloud
#    Prompts      /k8s-triage  /helm-triage
#    Skills       kubernetes  aks  helm  logs-alerts

# 4. If you need to open a delivery issue, preview the body first
.venv\Scripts\python.exe scripts/codev-dev.py guide issue --title "Improve onboarding copy" --summary "Prepare an issue body before opening GitHub"
#    Prints a complete issue body preview and the exact gh issue create command

# 5. If you want to add a new agent, preview it first
./.venv/bin/python scripts/codev-dev.py new agent my-agent
#    Prints a full dry-run preview — nothing is written
#    Add --write only when you are satisfied with the output
```

**Step count**: 15 -> 5 commands. Target (<= 5) met.

---

### Persona 2 — Senior architect (auditing routing coverage)

**Goal**: audit routing coverage, identify capability gaps, and scaffold a new
specialist agent.

```bash
# 1. Full health check including validator output
./.venv/bin/python scripts/codev-dev.py doctor
#    Shows: required files ✅, validator results (pass/fail + timing)

# 2. Verify a routing hypothesis
./.venv/bin/python scripts/codev-dev.py test-route "write integration tests for my OrderService"
#    Capability   testing-quality   (matched alias: "write tests")
#    Domain       unknown   ← signals a missing domain keyword for .NET
#    Agent        Architect
#    Prompts      /test-plan  /write-tests  /linters-stack

# 3. Discover alias gaps — phrases that fail to route
./.venv/bin/python scripts/codev-dev.py test-route "add a new agent"
#    ❌ No capability matched — gap identified
#    Tip: run test-route --list to see all aliases

# 4. Prepare a focused test plan before editing
.venv\Scripts\python.exe scripts/codev-dev.py guide test-plan --what "routing alias expansion" --why "Need targeted regression coverage before modifying aliases"
#    Prints a reusable test-plan block with CI command

# 5. Scaffold the missing agent
./.venv/bin/python scripts/codev-dev.py new agent observability-specialist
#    Prints full .agent.md preview — nothing written

# 6. Write when ready
./.venv/bin/python scripts/codev-dev.py new agent observability-specialist --write
#    Creates .github/agents/observability-specialist.agent.md
```

**Step count**: 6 commands. This path adds one explicit test-planning step before writing.

---

## Findings from doctor verification (last 5 merged PRs)

`doctor` was run against `main` after merging PRs #120, #121, #122, and the
two earlier squash commits (`dacfc77`, `385b054`):

| Validator | Result | Notes |
| --- | --- | --- |
| `validate-route-smoke.py` | ✅ Pass | All 37 smoke-test cases pass |
| `validate-autofix.py` | ✅ Pass | No routing errors detected |
| `validate-customization-registry.py` | ✅ Pass | All cross-links valid |
| `validate-readme-registry.py` | ✅ Pass | All skills documented |
| `validate-routing-coverage.py` | ✅ Pass | Coverage within threshold |

`doctor` correctly surfaces the pre-existing coverage validator issue without
masking the 4 passing validators. None of the last 5 merged PRs introduced
regressions.

---

## Alias gap discovered and fixed during walkthrough

During the senior-architect walkthrough, the phrase `"add a new agent"` returned
no match. The routing capability for framework extension is `routing`, but no
aliases covered the `new agent / new skill / new prompt / extend the framework`
intent.

**Fix applied** — added to `routing/aliases.yaml` under `routing`:

```yaml
- "new agent"
- "create agent"
- "scaffold agent"
- "new skill"
- "create skill"
- "new prompt"
- "create prompt"
- "extend the framework"
- "add a new agent"
- "add a new skill"
```

Smoke tests and registry validator pass after the fix (37/37 smoke cases). ✅

---

## Running the tests

```bash
.venv\Scripts\python.exe -m pytest tests/test_codev_dev.py -v
# 78 passed in ~36 sec
```
