# codev-dev contributor guide

`scripts/codev-dev.py` is the interactive developer CLI for CoDev. It provides
three commands that cover the most common contributor workflows — routing
exploration, repository health, and agent scaffolding — with zero risk of
accidental side effects.

## Commands at a glance

| Command | What it does | Writes files? |
| --- | --- | --- |
| `test-route "<phrase>"` | Show routing result for any phrase | Never |
| `test-route --list` | List all registered aliases by capability | Never |
| `doctor` | Check required files and run all validators | Never |
| `new agent <name>` | Scaffold a new agent file (dry-run by default) | Only with `--write` |

> `test-route` and `doctor` are **100% read-only**. `new agent` dry-runs by
> default and **never overwrites** an existing file.

---

## Persona walkthroughs

### Persona 1 — Junior developer (first contribution to CoDev)

**Goal**: understand what the framework does, find the right agent for a task,
and make a first routing contribution.

**Before `codev-dev`** (15 steps): open README → read capabilities.yaml →
read aliases.yaml → read domains.yaml → read matrix.yaml → open each agent
file → run 4 validators separately → cross-reference results manually.

**After `codev-dev`** (4 commands):

```bash
# 1. Health check — is the repo in a clean state?
python scripts/codev-dev.py doctor
#    ✅ 8 required files present
#    ✅ 4/5 validators pass  (validate-routing-coverage.py has a known
#       Windows Unicode issue — pre-existing, tracked separately)

# 2. Explore what phrases are already handled
python scripts/codev-dev.py test-route --list
#    Displays all aliases grouped by capability

# 3. Test your specific request
python scripts/codev-dev.py test-route "debug kubernetes pod"
#    Capability   debugging   (matched alias: "bug")
#    Domain       devops-cloud   (matched keyword: "kubernetes")
#    Agent        DevOps/Cloud
#    Prompts      /k8s-triage  /helm-triage
#    Skills       kubernetes  aks  helm  logs-alerts

# 4. If you want to add a new agent, preview it first
python scripts/codev-dev.py new agent my-agent
#    Prints a full dry-run preview — nothing is written
#    Add --write only when you are satisfied with the output
```

**Step count**: 15 → 4 commands. Target (≤ 5) met. ✅

---

### Persona 2 — Senior architect (auditing routing coverage)

**Goal**: audit routing coverage, identify capability gaps, and scaffold a new
specialist agent.

```bash
# 1. Full health check including validator output
python scripts/codev-dev.py doctor
#    Shows: required files ✅, validator results (pass/fail + timing)

# 2. Verify a routing hypothesis
python scripts/codev-dev.py test-route "write integration tests for my OrderService"
#    Capability   testing-quality   (matched alias: "write tests")
#    Domain       unknown   ← signals a missing domain keyword for .NET
#    Agent        Architect
#    Prompts      /test-plan  /write-tests  /linters-stack

# 3. Discover alias gaps — phrases that fail to route
python scripts/codev-dev.py test-route "add a new agent"
#    ❌ No capability matched — gap identified
#    Tip: run test-route --list to see all aliases

# 4. Scaffold the missing agent
python scripts/codev-dev.py new agent observability-specialist
#    Prints full .agent.md preview — nothing written

# 5. Write when ready
python scripts/codev-dev.py new agent observability-specialist --write
#    Creates .github/agents/observability-specialist.agent.md
```

**Step count**: 5 commands. Target (≤ 5) met. ✅

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
# 67 passed in ~13 sec
```
