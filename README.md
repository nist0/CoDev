# CoDev — GitHub Copilot Customization Framework

CoDev is a **GitHub Copilot customization framework** that turns Copilot into a team of specialized AI engineers. It provides a structured collection of **agents**, **prompts**, **skills**, and **instructions** organized around a canonical routing system. Instead of starting from scratch with each request, you use `/route` (or any alias) to automatically select the right agent, prompt, and skills for any engineering task.

---

## Quick Start — Use CoDev in your project

> **This is the primary way to use CoDev.** Add it as a Git submodule and all agents, skills,
> prompts, instructions, and routing are immediately available in VS Code Copilot — no copy-paste.

### 1. Add the submodule

```bash
# Bash / Linux / macOS / Git Bash
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
```

```powershell
# PowerShell (Windows)
git submodule add https://github.com/nist0/CoDev.git tools/codev
git submodule update --init --recursive
```

### 2. Bootstrap

```bash
./tools/codev/codev.sh init
```

If you run Bash from WSL against a repo under `/mnt/<drive>/...`, CoDev will
fall back to lockfile mode so it does not create Linux-target symlinks that
Windows tools cannot resolve correctly. Use `codev.ps1` if you specifically want
Windows-native symlink mode.

```powershell
.\tools\codev\codev.ps1 init
```

### 3. Verify

Open VS Code in the repository — `.github/agents/` should list all CoDev agents.
Run a smoke test:

```bash
python tools/codev/scripts/validate-route-smoke.py
```

### Modes

| Mode | When | Mechanism |
| --- | --- | --- |
| **Symlink** (default) | Linux / macOS / Windows Developer Mode | OS symlinks `.github/{agents,skills,…}` → submodule |
| **Lockfile** (fallback) | Windows without Developer Mode | File copy + SHA256 `codev-lock.json` |

The CLI auto-detects which mode to use.

### Commands

| Command | Purpose |
| --- | --- |
| `codev init` | Bootstrap the submodule into the host repo |
| `codev update` | Re-sync after `git submodule update` |
| `codev teardown --force` | Remove all managed artefacts (keeps `codev-overrides/`) |

> **`--force` is required on Windows / non-interactive shells.** Without it the CLI waits
> for a keystroke that PowerShell cannot forward — it will appear frozen until killed.

### Override strategies

- **`extend`** (default): your `codev-overrides/copilot-instructions.override.md` is appended
  after the submodule base in the generated `copilot-instructions.md`.
- **`override`**: the submodule base is fully replaced by your override file.

### Full documentation

- [docs/submodule-guide.md](docs/submodule-guide.md) — getting-started guide (init, extend, override, upgrade, teardown)
- [docs/submodule-cli-contract.md](docs/submodule-cli-contract.md) — CLI contract reference
- [docs/mcp-integration-guide.md](docs/mcp-integration-guide.md) — MCP design, setup, analysis, and debug guide for VS Code and GitHub Copilot
- [schemas/codev.schema.json](schemas/codev.schema.json) — `codev.json` JSON Schema

---

## Table of Contents

- [Quick Start — Use CoDev in your project](#quick-start--use-codev-in-your-project)
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Usage Examples](#usage-examples)
- [Routing System](#routing-system)
- [Agents](#agents)
- [Instructions](#instructions)
- [Prompts](#prompts)
- [Skills](#skills)
- [Submodule Reference](#submodule-reference)
- [Capability Extension Protocol](#capability-extension-protocol)

---

## Overview

| Layer | Purpose | Location |
|-------|---------|----------|
| **Agents** | Specialized AI roles with defined responsibilities and output formats | `.github/agents/` |
| **Instructions** | Always-on coding standards applied per file-type or repo-wide | `.github/instructions/` |
| **Prompts** | Reusable slash-command templates for recurring tasks | `.github/prompts/` |
| **Skills** | Deep reference modules loaded on demand for specific procedures | `.github/skills/<theme>/SKILL.md` |
| **Routing** | YAML-driven matrix mapping capability + domain → agent + prompts + skills | `routing/` |

**Core principles:**

- Start every session with `/route` to select the right tool for the job.
- Prefer copy/paste-ready outputs: commands, file content, checklists.
- Never introduce secrets. Never log sensitive data.
- Make small, reviewable changes with verification steps included.

---

## Repository Structure

This tree is schematic, not exhaustive. Inventory-heavy sections below are generated from the
actual repository contents.

```text
CoDev/
├── README.md
├── .github/
│   ├── copilot-instructions.md        # Repo-wide Copilot working agreement
│   ├── agents/                        # Custom agent definitions (.agent.md)
│   ├── instructions/                  # Coding standards (.instructions.md)
│   ├── prompts/                       # Slash-command templates (.prompt.md)
│   └── skills/                        # Procedure modules (<theme>/SKILL.md)
└── routing/
    ├── capabilities.yaml              # Capability catalog
    ├── domains.yaml                   # Domain catalog + keywords
    ├── aliases.yaml                   # Natural-language aliases per capability
    └── matrix.yaml                    # Routing rules: capability + domain → recommendation
```

---

## Getting Started

### Primary entry point

Use the **`/route`** prompt (aliases: `route`, `router`, `which agent`, `where to start`) to classify your request and get a deterministic recommendation:

```text
/route I need to debug a CrashLoopBackOff on my AKS pod
```

Copilot will respond with:

- **Capability** identified (e.g., `debugging`)
- **Domain** identified (e.g., `devops-cloud`)
- **Recommended agent** to switch to
- **Recommended prompts** to run
- **Recommended skills** to load
- **Rationale** and next actions

### Quick-start examples

| Task | Alias to type |
|------|---------------|
| Route any request | `/route <your request>` |
| Debug a bug | `bug`, `exception`, `stack trace` |
| Write tests | `write tests`, `test plan` |
| Open PR / review | `pr review`, `commit message` |
| Create a release | `release`, `changelog`, `semver` |
| Brainstorm ideas | `brainstorm`, `alternatives` |
| Write a script | `bash script`, `python script` |
| Tech watch digest | `what's new`, `trends` |
| Set up or debug MCP | `mcp`, `set up mcp`, `debug mcp` |
| Onboard to a .NET CLI platform project | `/cli-platform-init repo=.` |

### Validation commands (local + CI parity)

Use these checks before opening a PR for customization changes:

```bash
python scripts/validate-route-smoke.py
python scripts/validate-customization-registry.py
python scripts/validate-readme-registry.py
python scripts/validate-routing-coverage.py
python scripts/validate-markdown-lint.py
```

Note: Markdown lint validation uses `markdownlint-cli2` via `npx` (Node.js required).

### Local pre-commit hooks (recommended)

Install pre-commit hooks to catch routing errors before every push — no waiting for CI:

```bash
pip install pre-commit
pre-commit install
```

The hooks run all routing validators automatically on each commit:

- `route-smoke-tests` — alias resolution and smoke test suite
- `customization-registry` — agents, prompts, skills, and instructions cross-links
- `routing-coverage` — strict mode, no uncovered capability×domain pairs allowed
- `readme-registry` — skill documentation completeness

CI gates — all run on every `pull_request` and `push` to `main`:

Generated workflow inventory:

<!-- codev:generated:workflows:start -->
| Workflow | File | Triggers |
| --- | --- | --- |
| CoDev Submodule Integrity | .github/workflows/codev-integrity.yml | workflow_call |
| markdown-lint | .github/workflows/markdown-lint.yml | pull_request, push |
| readme-registry | .github/workflows/readme-registry.yml | pull_request, push |
| route-coverage | .github/workflows/route-coverage.yml | pull_request, push |
| route-smoke | .github/workflows/route-smoke.yml | pull_request, push |
| Routing CI | .github/workflows/routing-ci.yml | pull_request, push |
| unit-tests | .github/workflows/unit-tests.yml | pull_request, push |
<!-- codev:generated:workflows:end -->

### Developer Tooling

Additional scripts for day-to-day development — auto-fix, watch mode, and an interactive CLI.

#### `scripts/validate-autofix.py` — detect and auto-fix routing errors

Detects and optionally fixes 3 common routing error classes:

| Error class | Detected | Auto-fixed |
| --- | --- | --- |
| Missing alias in `aliases.yaml` | ✅ | ✅ |
| Incorrect agent ID in `matrix.yaml` | ✅ | ✅ |
| Orphaned prompt reference in `matrix.yaml` | ✅ | ✅ |

```bash
# Detect only (safe, no writes)
python scripts/validate-autofix.py

# Detect and fix in place
python scripts/validate-autofix.py --fix

# Generate a Markdown report (written to reports/)
python scripts/validate-autofix.py --report --report-format markdown

# Generate a JSON report for CI artifact upload
python scripts/validate-autofix.py --report --report-format json
```

#### `scripts/validate-watch.py` — continuous validation on file change

Polls `routing/` and `.github/` directories and reruns validators automatically on any change. Validation cycle is under 2 seconds.

```bash
# Watch mode (runs indefinitely)
python scripts/validate-watch.py

# Single run (CI-friendly, exits after one pass)
python scripts/validate-watch.py --once

# Watch only specific validators
python scripts/validate-watch.py --validators smoke autofix
```

#### `scripts/install-hooks.py` — install pre-commit hooks

Installs the scope-filtered pre-commit hook from `scripts/hooks/pre-commit` into `.git/hooks/`. The hook runs validators only when routing or `.github/` files are staged.

```bash
# Install the pre-commit hook
python scripts/install-hooks.py

# Check if hooks are installed (no writes)
python scripts/install-hooks.py --check
```

#### `scripts/codev-dev.py` — interactive developer CLI

Three commands to explore routing, scaffold agents, and run health checks — all safe to run at any time.

| Command | Description | Writes files? |
| --- | --- | --- |
| `test-route "<phrase>"` | Show routing result for any phrase with rationale | Never |
| `doctor` | Check required files and run all validators | Never |
| `new agent <name>` | Scaffold a new agent file (dry-run by default) | Only with `--write` |

```bash
# Route any phrase interactively
python scripts/codev-dev.py test-route "debug kubernetes pod"

# List all known routing aliases grouped by capability
python scripts/codev-dev.py test-route --list

# Run repository health check
python scripts/codev-dev.py doctor

# Scaffold a new agent (dry-run — prints output, writes nothing)
python scripts/codev-dev.py new agent my-agent

# Scaffold and write to .github/agents/ (requires --write)
python scripts/codev-dev.py new agent my-agent --write
```

> **Safety contract**: `test-route` and `doctor` are 100% read-only. `new agent` dry-runs by default and never overwrites an existing file.

See [docs/codev-dev-guide.md](docs/codev-dev-guide.md) for persona walkthroughs, step-count measurements, and doctor verification results.

> **Full reference**: [docs/developer-tooling.md](docs/developer-tooling.md) covers all four scripts (`validate-autofix.py`, `validate-watch.py`, `install-hooks.py`, `codev-dev.py`) with historical error test results and CI integration details.

---

## Usage Examples

All examples start with `/route` to let the framework pick the right agent, prompts, and skills automatically. Each block shows: the command you type → what the router returns → the follow-up action.

---

### 1 — Set up an MCP server for VS Code and GitHub Copilot

```text
/route set up an MCP server for VS Code and GitHub Copilot
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `mcp` |
| Domain | none |
| Agent | `mcp-specialist` |
| Prompts | `/mcp-setup`, `/mcp-analyze`, `/mcp-debug` |
| Skills | `mcp-integration`, `vscode` |

**Follow-up**

```text
/mcp-setup goal="Expose our internal docs search" host=both server=remote transport=http
```

Expect: a topology decision, a least-privilege primitive choice, a copy/paste-ready configuration pattern, and a verification checklist.

---

### 2 — Debug a crashing Kubernetes pod

```text
/route my AKS pod keeps restarting with OOMKilled
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `debugging` |
| Domain | `devops-cloud` |
| Agent | `DevOps/Cloud` |
| Prompts | `/k8s-triage`, `/helm-triage` |
| Skills | `kubernetes`, `aks`, `helm`, `logs-alerts` |

**Follow-up** — switch to the `DevOps/Cloud` agent, then run:

```text
/k8s-triage
```

The agent will walk you through: reproduce → observe → hypothesize → fix → prevent regression.

---

### 3 — Write tests for a .NET service

```text
/route write integration tests for my OrderService in ASP.NET Core
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `testing-quality` |
| Domain | `backend-dotnet` |
| Agent | `Backend .NET` |
| Prompts | `/test-plan`, `/write-tests`, `/linters-stack` |
| Skills | `test-strategy`, `dotnet-testing`, `linters`, `github-actions` |

**Follow-up** — first produce a test plan, then generate the tests:

```text
/test-plan
/write-tests
```

Expect: test plan (what/why/how/not-tested), then xUnit tests with Testcontainers for the DB layer.

---

### 4 — Review a pull request

```text
/route review my open pull request before merge
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `github-delivery` |
| Domain | `github-delivery` |
| Agent | `delivery-lead` |
| Prompts | `/pr-review` |
| Skills | `pr-review`, `commits`, `git` |

**Follow-up**

```text
/pr-review
```

The agent produces a structured review with sections: correctness · security · tests · docs · verdict (`approved` or `rework required`).

---

### 5 — Brainstorm architectural alternatives

```text
/route brainstorm alternatives to our current monolithic event processor
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `brainstorming` |
| Domain | `backend-dotnet` |
| Agent | `innovator` |
| Prompts | `/brainstorm` |
| Skills | `elite-brainstorming`, `innovation-sprint`, `adr` |

**Follow-up**

```text
/brainstorm objective="Replace monolithic event processor" constraints="must keep existing SLA" success="p99 < 100 ms at 2× load"
```

Expect: 8–12 ideas → scored shortlist (safe / adjacent / bold) → time-boxed spike plan → specialist review verdicts.

---

### 6 — Generate a tech-watch digest

```text
/route what's new in the .NET ecosystem this week
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `tech-watch` |
| Domain | `backend-dotnet` |
| Agent | `tech-scout` |
| Prompts | `/tech-watch-digest` |
| Skills | `weekly-digest` |

**Follow-up**

```text
/tech-watch-digest
```

Expect: structured digest entries with **What changed → Why it matters → Experiments to try → Action / Effort / Deadline**.

---

### 7 — Create a release plan

```text
/route create a release plan for our next minor version
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `release` |
| Domain | `cicd` |
| Agent | `delivery-lead` |
| Prompts | `/release-plan` |
| Skills | `release`, `supply-chain` |

**Follow-up**

```text
/release-plan
```

Expect: SemVer bump decision, changelog draft, tag + GitHub Release steps, rollout and rollback procedure.

---

### 8 — Extend the framework with a new agent

```text
/route I want to add a new agent for database performance tuning
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `routing` |
| Domain | `backend-dotnet` |
| Agent | `router` → hand-off to `promptsmith` |
| Prompts | `/new-agent`, `/new-skill` |
| Skills | `agent-authoring`, `canonical-routing`, `prompt-engineering` |

**Follow-up**

```text
/new-agent agentId=db-perf mission="Database performance tuning: query plans, index analysis, slow-query triage"
/new-skill skillId=db-perf-analysis theme="Database Performance" scope="When diagnosing slow queries or index inefficiencies"
```

Then update the four routing YAMLs (`capabilities.yaml`, `domains.yaml`, `aliases.yaml`, `matrix.yaml`) and validate:

```bash
python scripts/validate-route-smoke.py
python scripts/validate-customization-registry.py
```

---

### 9 — Generate a production-ready ASP.NET Core CRUD controller

```text
/route generate a REST CRUD controller for an Orders resource in ASP.NET Core
```

**Router output**

| Field | Value |
|-------|-------|
| Capability | `scaffolding` |
| Domain | `backend-dotnet` |
| Agent | `backend-dotnet` |
| Prompts | `/generate-controller` |
| Skills | `rest-api-controller-gen`, `aspnet-core`, `mediatr`, `openapi` |

**Follow-up**

```text
/generate-controller resource=Order description="Manages customer orders with status tracking"
```

Generates: controller class with CRUD endpoints, MediatR commands/queries, FluentValidation validators, ProblemDetails error responses, OpenAPI annotations, versioning wiring, and an integration-test checklist — ready to compile.

---

### Quick-reference cheat sheet

| What you want to do | What to type |
|--------------------|--------------|
| Route any request | `/route <your request>` |
| Debug a crash or error | `/route <error/symptom>` → `/triage-error` |
| Triage a K8s issue | `/route k8s <symptom>` → `/k8s-triage` |
| Write or review tests | `/route write tests for <component>` → `/test-plan` then `/write-tests` |
| Review a PR | `/route review my PR` → `/pr-review` |
| Plan a release | `/route release plan` → `/release-plan` |
| Brainstorm ideas | `/route brainstorm <topic>` → `/brainstorm` |
| Get a tech digest | `/route what's new in <technology>` → `/tech-watch-digest` |
| Generate a CRUD controller | `/generate-controller resource=<Name> description="<desc>"` |
| Add a new agent/skill | `/route new agent for <domain>` → `/new-agent` then `/new-skill` |
| Onboard to a repo | `/quickstart` |
| Diagnose a bad route | `/route-miss` |

---

## Routing System

The routing system is defined in four YAML files under `routing/`:

These inventories are generated from the routing source files so the README stays aligned with the
actual matrix.

### `routing/capabilities.yaml`

Defines **what** Copilot can do. Each capability has an `id` and a `default_agent`.

<!-- codev:generated:capabilities:start -->
| Capability ID | Description | Default Agent |
| --- | --- | --- |
| `routing` | Route a request using the canonical capability + domain matrix. | Router |
| `debugging` | Bug triage, reproduction, instrumentation, root cause analysis. | Reliability |
| `postmortem` | Incident analysis, timeline, RCA, action items (blameless). | Reliability |
| `code-analysis` | Explain code, identify flows/invariants, generate doc-ready explanations. | Architect |
| `docs` | Generate repository and reference documentation. | Delivery Lead |
| `docs-system` | Doc architecture model, markdown standards, linting, doc governance. | Delivery Lead |
| `testing-quality` | Test planning, writing tests, quality gates, linters. | Architect |
| `github-delivery` | Commits, PR reviews, issues/projects planning, delivery practices. | Delivery Lead |
| `release` | Release planning and execution: SemVer, tags, changelog, artifacts, rollout/rollback. | Delivery Lead |
| `automation` | Automation scripts, CLI orchestration, and repo tooling workflows. | Automation/Scripting |
| `project-orchestration` | Lead whole-project delivery: clarify, plan, dispatch specialists, track issues/Kanban, and review outcomes. | Project Orchestrator |
| `brainstorming` | Generate innovative ideas, alternatives, spikes. | Innovator |
| `tech-watch` | Tech/science watch, weekly digest, inspiration. | Tech Scout |
| `onboarding` | Interactive framework orientation: gather role + domain + goal, then emit a personalised first-command card. | Router |
| `route-miss` | Feedback loop: capture a routing miss, diagnose root cause, propose an additive fix, and emit a ready-to-open GitHub issue. | Router |
| `project-takeover` | Analyse exhaustive d'un ou plusieurs dépôts GitHub on-prem lors d'une prise en charge d'équipe. Produit une documentation complète en français dans .takeover/ (jamais commité). | Project Takeover |
| `security` | Identify threats, audit secrets, triage vulnerabilities, and enforce secure-by-default practices. | Security |
| `cli-platform-onboarding` | Three-phase onboarding for a .NET CLI platform project: bootstrap CoDev as submodule, run full static analysis (GH workflows, Bicep, solution), then execute tasks using deduced project context. | CLI Platform Onboarder |
| `mcp` | Design, install, analyze, and debug Model Context Protocol integrations for VS Code and GitHub Copilot. | mcp-specialist |
| `scaffolding` | Generate production-ready code artefacts (controllers, handlers, tests) from a description, OpenAPI contract, or resource theme; or bootstrap a new REST API project from scratch using curated templates. | Backend .NET |
| `mermaid` | Produce, review, and embed Mermaid diagrams in Markdown files — GitHub-native rendering, best practices, and CI validation. | mermaid-diagrammer |
| `codev-management` | CoDev submodule lifecycle: init, update, override authoring, teardown, and upstream contribution. | CoDev Consumer |
| `cv-coaching` | Analyse, critique, and rewrite CVs/resumes to modern professional standards: ATS compliance, impact-first bullets, quantified achievements, and keyword gap analysis against a target job offer. | CV Coach |
| `bot-engineering` | Design, scaffold, and debug bots for Teams, Telegram, WhatsApp, Discord and other platforms in C# or Python. | Bot Engineer |
<!-- codev:generated:capabilities:end -->

### `routing/domains.yaml`

Defines **where** capabilities apply. Keywords trigger automatic domain detection.

<!-- codev:generated:domains:start -->
| Domain ID | Example Keywords |
| --- | --- |
| `backend-dotnet` | `dotnet`, `.net`, `asp.net`, `aspnet`, `c#`, `ef core`, `entity framework`, `mediatr` |
| `devops-cloud` | `aks`, `kubernetes`, `k8s`, `helm`, `chart`, `charts`, `values.yaml`, `kubectl` |
| `observability` | `elastic`, `elasticsearch`, `kibana`, `kql`, `lucene`, `apm`, `trace`, `tracing` |
| `native` | `language c`, `c++`, `cpp`, `asm`, `assembly`, `x86`, `avr`, `pic` |
| `frontend` | `react`, `typescript`, `javascript`, `html`, `css`, `npm`, `yarn`, `vite` |
| `scripting` | `python`, `perl`, `script`, `scripting` |
| `shell-automation` | `bash`, `powershell`, `pwsh`, `batch`, `cmd`, `shell`, `automation` |
| `cicd` | `github actions`, `actions`, `workflow`, `pipeline`, `continuous integration`, `continuous delivery`, `release`, `tag` |
| `github-delivery` | `pull request`, `review`, `commits`, `conventional commits`, `issues`, `projects`, `milestones`, `labels` |
| `project-orchestration` | `orchestrate`, `orchestration`, `project lead`, `delegate whole project`, `dispatch`, `work breakdown`, `task assignment`, `kanban` |
| `docs-system` | `markdown`, `docs`, `documentation`, `docs lint`, `markdown lint`, `plantuml`, `mermaid`, `diagram` |
| `bot-platforms` | `teams`, `telegram`, `whatsapp`, `discord`, `slack`, `bot`, `chatbot`, `webhook` |
<!-- codev:generated:domains:end -->

### `routing/aliases.yaml`

Maps natural-language phrases to capability IDs so you can use plain English instead of IDs.

### `routing/matrix.yaml`

The core routing table: `capability + domain → agent + prompts + skills`. Domain-specific rules fire first; capability-only rules are fallbacks.

---

## Agents

Agents are specialized AI roles defined in `.github/agents/`. Each has a clear mission, responsibilities, output format, and handoff behavior.

Generated agent inventory:

<!-- codev:generated:agents:start -->
| Agent | File | Description |
| --- | --- | --- |
| Architect | architect.agent.md | Cross-cutting architecture: boundaries, patterns, tradeoffs, ADR proposals, and documentation-ready explanations. |
| Automation/Scripting | automation-scripting.agent.md | Bash/PowerShell/Python/Perl automation, CLI tooling, and repo tooling scripts. |
| Backend .NET | backend-dotnet.agent.md | ASP.NET Core, EF Core, PostgreSQL, MediatR, OpenAPI; production-grade REST APIs and CLIs. |
| Bot Engineer | bot-engineer.agent.md | Multi-platform bot engineering: Microsoft Teams (M365 Agents SDK / Teams AI Library), Telegram (python-telegram-bot), WhatsApp (Cloud API), and cross-platform bot architecture patterns in C# and Python. |
| CLI Platform Onboarder | cli-platform-onboarder.agent.md | Bootstrap CoDev into a .NET CLI platform repo, run full static analysis (GH workflows, Bicep/infra, solution), and drive task execution using deduced project context. |
| CoDev Consumer | codev-consumer.agent.md | Guides repository maintainers through the full CoDev submodule lifecycle: init, update, override authoring, teardown, and contributing changes upstream. |
| CV Coach | cv-coach.agent.md | Analyse, critique, and rewrite CVs/resumes to modern professional standards. Covers ATS compliance, impact-first bullets, quantified achievements, and keyword gap analysis against a target job description. |
| Delivery Lead | delivery-lead.agent.md | GitHub delivery: PR hygiene, reviews, issues/projects planning, docs governance, release readiness. |
| DevOps/Cloud | devops-cloud.agent.md | AKS/Kubernetes, Helm, GitHub Actions CI/CD, Azure tooling, delivery and runtime operations. |
| Frontend | frontend.agent.md | React + TypeScript frontend engineering, tooling, UI patterns, and test strategy. |
| GitHub Ops | github-ops.agent.md | Executes GitHub CLI operations: create/close issues, open/merge PRs, add comments, and link work items. Use when a GitHub action needs to be performed, not just planned. |
| implement | implement.agent.md | Implements a plan as small diffs, respecting repo conventions. Writes code/files. |
| Innovator | innovator.agent.md | Structured brainstorming: alternatives, spikes, innovation shortlists with scored portfolio and execution handoff. |
| mcp-specialist | mcp-specialist.agent.md | Specialist agent for designing, installing, analyzing, and debugging MCP integrations for VS Code and GitHub Copilot. |
| mermaid-diagrammer | mermaid-diagrammer.agent.md | Specialist agent for producing, reviewing, and improving Mermaid diagrams in documentation. Generates correct, GitHub-native Mermaid from descriptions; reviews existing diagrams for syntax, best practices, and rendering compatibility. |
| Native/Systems | native-systems.agent.md | C/C++ and assembly (x86/AVR/PIC): memory, performance, tooling, and low-level debugging. |
| plan | plan.agent.md | Converts a goal into a precise implementation plan + file checklist. No coding. |
| Project Orchestrator | project-orchestrator.agent.md | Leads end-to-end project delivery: clarify, plan, dispatch, track, and review across specialist agents. |
| Project Takeover | project-takeover.agent.md | Analyse exhaustive d'un ou plusieurs dépôts GitHub on-prem lors d'une prise en charge d'équipe. Produit 6 documents en français dans le répertoire local `.takeover/` (gitignored). Couvre : inventaire des dépôts, état du Kanban, graphe des sous-modules, topologie API & BD, décomposition fonctionnelle, et plan d'étude point par point. |
| promptsmith | promptsmith.agent.md | Creates stable prompts, skills, agents, and instruction files for this repo. Always plans first. |
| Reliability | reliability.agent.md | Reliability engineering: debugging triage, postmortems, performance regressions, observability-first fixes. |
| reviewer | reviewer.agent.md | Reviews changes for correctness, security, consistency, and instruction/skill compliance with codebase-first evidence. |
| Router | router.agent.md | Canonical routing: capability + domain → recommended agent, prompts, and skills. |
| Security | security-agent.agent.md | Guides threat modeling, vulnerability triage, and secrets hygiene within Copilot Chat sessions. Design-time and code-time agent — not a live infrastructure scanner. |
| Tech Scout | tech-scout.agent.md | Tech/scientific watch: actionable digests (what changed / why it matters / what to try). |
<!-- codev:generated:agents:end -->

---

## Instructions

Instructions are always-on coding standards applied automatically based on file patterns. Defined in `.github/instructions/`.

Generated instruction inventory:

<!-- codev:generated:instructions:start -->
| File | applyTo | Description |
| --- | --- | --- |
| 00-core.instructions.md | `**` | Core working agreement: deterministic steps, copy/paste-ready outputs, non-contradictory layering. |
| bash.instructions.md | `**/*.sh` | Bash guidance: safe shell scripting. |
| bot.instructions.md | `**/*bot*.{cs,py},**/*bot*handler*.{cs,py},**/*webhook*.{cs,py}` | Always-on rules for bot code files across all platforms (Teams, Telegram, WhatsApp, Discord). Non-negotiable security baseline, SDK selection, and reliability standards. |
| brainstorming-governance.instructions.md | `**` | Mandatory brainstorm-first gate for all non-trivial tasks: require elite ideation quality, scored option portfolio, execution handoff, and named specialist reviews. |
| cli-platform.instructions.md | `**` | Mandatory working standards for the .NET CLI platform project: three-phase workflow enforcement, context discipline, extension conventions, and infra/CI authoring rules. |
| codev-consumer.instructions.md | `codev-overrides/**` | Rules for authoring assets in codev-overrides/: naming, non-duplication, safety, and validation. |
| customization-governance.instructions.md | `.github/**/*.{md,yml,yaml}` | Mandatory governance for agents/prompts/skills/instructions and routing consistency. |
| docs-system.instructions.md | `**/*.md` | Documentation Architecture Model (DAM), consistent markdown structure, lint-friendly docs. |
| dotnet.instructions.md | `**/*.cs` | C#/.NET code standards: safety, readability, diagnostics, testing expectations. |
| github-actions-yaml.instructions.md | `.github/workflows/**/*.yaml` | Same as .yml; provided separately for .yaml extension. |
| github-actions.instructions.md | `.github/workflows/**/*.yml` | Workflow best practices: minimal permissions, reproducibility, clear steps. |
| helm-chart.instructions.md | `**/Chart.yaml` | Helm chart conventions: renderability, values discipline, safe upgrades, and lint-friendly structure. |
| mcp.instructions.md | `**/mcp*.json` | Authoring rules for MCP configuration files: least privilege, trust boundaries, transport choice, and verification. |
| mermaid.instructions.md | `**/*.md` | Always-on authoring rules for Mermaid diagrams in Markdown files: fencing, diagram type selection, GitHub rendering constraints, accessibility, and versioning. |
| powershell.instructions.md | `**/*.ps1` | PowerShell guidance: idempotence, error handling, safe automation. |
| project-orchestration.instructions.md | `**` | Whole-project delegation defaults: clarify, plan, dispatch, track, and review. |
| python.instructions.md | `**/*.py` | Python guidance: readability, safety, robust CLI/script behavior. |
| react.instructions.md | `**/*.tsx` | React/TSX guidance: component boundaries, hooks discipline, performance basics. |
| reliability.instructions.md | `**` | Repro-first debugging, measurement-first performance, blameless postmortems, observability standards. |
| security.instructions.md | `**/*` | Secure-by-default coding: secrets hygiene, least-privilege, threat modeling, supply chain. |
| tech-watch.instructions.md | `**` | Actionable digests: what changed, why it matters, what to try. |
| testing-quality.instructions.md | `**` | Test plans, regression tests for bug fixes, and lint/quality gate practices. |
| typescript.instructions.md | `**/*.ts` | TS/JS guidance: types first, predictable state, lint-friendly patterns. |
| values-yaml.instructions.md | `**/values*.{yml,yaml}` | Values file clarity: documentation, naming consistency, safe defaults. |
<!-- codev:generated:instructions:end -->

---

## Prompts

Reusable slash-command templates defined in `.github/prompts/`. Invoke them with `/prompt-name` in Copilot chat.

Generated prompt inventory:

<!-- codev:generated:prompts:start -->
| Prompt | File | Agent | Description |
| --- | --- | --- | --- |
| `/apm-analysis` | apm-analysis.prompt.md |  | ﻿--- |
| `/automation-script` | automation-script.prompt.md |  | ﻿--- |
| `/az-ops` | az-ops.prompt.md | DevOps/Cloud | Azure CLI operations — subscription context, resource discovery, AKS, Key Vault, ACR, RBAC, and monitoring queries. |
| `/bot-scaffold` | bot-scaffold.prompt.md | Bot Engineer | Scaffold a production-ready bot project for Teams, Telegram, WhatsApp or other platforms in C# or Python. Gathers requirements and emits exact setup steps, project structure, and security baseline. |
| `/bot-triage` | bot-triage.prompt.md | Bot Engineer | Systematically debug and triage bot issues across Teams, Telegram, WhatsApp and other platforms. Follows repro-first methodology: symptom collection, platform identification, SDK version, ranked hypotheses, and verified fix. |
| `/brainstorm` | brainstorm.prompt.md |  | ﻿--- |
| `/cli-platform-analyze` | cli-platform-analyze.prompt.md |  | ﻿--- |
| `/cli-platform-init` | cli-platform-init.prompt.md |  | ﻿--- |
| `/cli-platform-task` | cli-platform-task.prompt.md |  | ﻿--- |
| `/codev-contribute` | codev-contribute.prompt.md |  | ﻿--- |
| `/codev-init` | codev-init.prompt.md |  | ﻿--- |
| `/codev-update` | codev-update.prompt.md |  | ﻿--- |
| `/cv-review` | cv-review.prompt.md | CV Coach | Critique and rewrite a CV to modern professional standards: ATS compliance, quantified impact bullets, and optional keyword gap analysis against a job description. |
| `/deep-plan` | deep-plan.prompt.md | plan | Elite planning entry point: runs a mandatory brainstorm (≥ 3 scored options), produces a ranked implementation plan, and emits a GitHub issue draft with full sub-task checklist — for any domain. |
| `/diagram-ops` | diagram-ops.prompt.md |  | ﻿--- |
| `/doc-lint-fix` | doc-lint-fix.prompt.md |  | ﻿--- |
| `/dotnet-excellence` | dotnet-excellence.prompt.md |  | ﻿--- |
| `/explain-code` | explain-code.prompt.md |  | ﻿--- |
| `/generate-controller` | generate-controller.prompt.md | Backend .NET | Generate a production-ready ASP.NET Core CRUD controller from a description, OpenAPI JSON contract, or resource theme. |
| `/generate-docs-tree` | generate-docs-tree.prompt.md |  | ﻿--- |
| `/generate-onboarding` | generate-onboarding.prompt.md |  | ﻿--- |
| `/helm-triage` | helm-triage.prompt.md |  | ﻿--- |
| `/k8s-triage` | k8s-triage.prompt.md |  | ﻿--- |
| `/linters-stack` | linters-stack.prompt.md |  | ﻿--- |
| `/logs-analysis` | logs-analysis.prompt.md |  | ﻿--- |
| `/markdown-ops` | markdown-ops.prompt.md |  | ﻿--- |
| `/mcp-analyze` | mcp-analyze.prompt.md | mcp-specialist | Analyze an existing MCP design or configuration for topology correctness, least privilege, and VS Code or GitHub Copilot fit. |
| `/mcp-debug` | mcp-debug.prompt.md | mcp-specialist | Debug MCP startup, discovery, auth, or invocation failures in VS Code or GitHub Copilot with a repro-first troubleshooting flow. |
| `/mcp-setup` | mcp-setup.prompt.md | mcp-specialist | Design and install an MCP integration for VS Code or GitHub Copilot with a guided intake, strict topology decisions, and least-privilege verification steps. |
| `/mermaid-create` | mermaid-create.prompt.md | mermaid-diagrammer | Generate a Mermaid diagram from a natural-language description. Outputs a GitHub-ready fenced code block with prose context. |
| `/mermaid-embed` | mermaid-embed.prompt.md | mermaid-diagrammer | Embed a Mermaid diagram into an existing Markdown file (GitHub README, ADR, wiki, PR description). Handles correct fencing, placement, prose context, and accessibility. |
| `/mermaid-review` | mermaid-review.prompt.md | mermaid-diagrammer | Review an existing Mermaid diagram snippet for syntax errors, deprecated patterns, GitHub rendering compatibility, and best-practice violations. Returns structured verdict + improved version. |
| `/new-agent` | new-agent.prompt.md |  | ﻿--- |
| `/new-instructions` | new-instructions.prompt.md |  | ﻿--- |
| `/new-skill` | new-skill.prompt.md |  | ﻿--- |
| `/new-theme-pack` | new-theme-pack.prompt.md |  | ﻿--- |
| `/obs` | obs.prompt.md | Reliability | Observability incident triage — first response for latency spikes, error rate surges, log anomalies, and missing traces across Elastic APM, Kibana, and log pipelines. |
| `/pg` | pg.prompt.md | Backend .NET | PostgreSQL quick operations — schema inspection, query optimization, index analysis, lock triage, and connection pool management. |
| `/postmortem` | postmortem.prompt.md |  | ﻿--- |
| `/pr-review` | pr-review.prompt.md |  | ﻿--- |
| `/project-dispatch` | project-dispatch.prompt.md |  | ﻿--- |
| `/project-governance` | project-governance.prompt.md |  | ﻿--- |
| `/project-kickoff` | project-kickoff.prompt.md |  | ﻿--- |
| `/project-takeover` | project-takeover.prompt.md | Project Takeover | Analyse exhaustive d'un ou plusieurs dépôts GitHub on-prem lors d'une prise en charge d'équipe. Produit une documentation complète en français dans .takeover/ (non commité). |
| `/prompt-from-theme` | prompt-from-theme.prompt.md |  | ﻿--- |
| `/quickstart` | quickstart.prompt.md |  | ﻿--- |
| `/release-plan` | release-plan.prompt.md |  | ﻿--- |
| `/route-miss` | route-miss.prompt.md |  | ﻿--- |
| `/route` | route.prompt.md |  | ﻿--- |
| `/secrets-audit` | secrets-audit.prompt.md |  | ﻿--- |
| `/tech-watch-digest` | tech-watch-digest.prompt.md |  | ﻿--- |
| `/test-plan` | test-plan.prompt.md |  | ﻿--- |
| `/threat-model` | threat-model.prompt.md |  | ﻿--- |
| `/triage-error` | triage-error.prompt.md |  | ﻿--- |
| `/vuln-triage` | vuln-triage.prompt.md |  | ﻿--- |
| `/write-tests` | write-tests.prompt.md |  | ﻿--- |
<!-- codev:generated:prompts:end -->

---

## Skills

Skills are deep, on-demand reference modules loaded when a routing rule recommends them. Each lives in `.github/skills/<theme>/SKILL.md` and covers the full engineering stack.

Generated skill inventory:

<!-- codev:generated:skills:start -->
| Skill | Description |
| --- | --- |
| `adr` | Architecture Decision Records — structured context, options, decision, consequences, and follow-up tasks. |
| `agent-authoring` | Create stable custom agents (.agent.md) with clear mission, boundaries, and repeatable workflow. |
| `aks` | AKS cluster operations — health checks, node pool management, networking triage, and safe upgrade procedure. |
| `apm` | APM trace analysis — latency hotspots, span breakdown, error correlation, and instrumentation improvements. |
| `asm-x86` | x86 Assembly (Intel) — calling conventions, stack frames, registers, and low-level debugging procedure. |
| `aspnet-core` | ASP.NET Core REST API conventions — routing, versioning, validation, error handling, auth, observability, and production readiness. |
| `avr` | AVR firmware — MCU identification, ISR safety, peripheral configuration, memory constraints, and debugging. |
| `az` | Azure CLI operational playbook — identity safety, context confirmation, AKS ops, and safe command patterns. |
| `azure` | Azure operational basics — identity safety, resource navigation, secrets management, networking, and change verification. |
| `bash` | Bash shell automation — safety defaults, idempotency, input validation, error handling, and ShellCheck integration. |
| `batch` | Windows batch/CMD scripting — safe patterns, error handling, and migration guidance. Prefer PowerShell for complex logic. |
| `bot-architecture` | Cross-platform bot architecture patterns -- Activity/Turn model, middleware pipeline, state management, secrets hygiene, webhook vs polling, and AI integration. Applies to C# and Python across Teams, Telegram, WhatsApp, and other platforms. |
| `bruno` | Bruno API testing — collection structure, environment strategy, request standardization, response validation, CI integration. |
| `c` | C language — safety defaults, memory discipline, error handling, sanitizers, and debugging procedure. |
| `canonical-routing` | Deterministic routing using capability + domain matrix — classification, fallback, and handoff. |
| `cli-platform-analysis` | Full static analysis of a .NET CLI platform project — GH workflow files, Bicep/ARM/Terraform infra, solution structure, CLI surface, test projects, and existing docs — producing docs/project-context.md as the living context document for all subsequent task prompts. |
| `cli-platform-bootstrap` | Add CoDev as a git submodule to a .NET CLI platform repo, run codev init with the extend strategy, author the codev-overrides/ stub, verify, and commit — ready for full project analysis. |
| `codev-contributing` | How to propose changes to CoDev from a consumer repository — fork, fix, PR, upstream sync, and review protocol. |
| `codev-submodule` | Full reference for managing CoDev as a Git submodule — init, update, override authoring, teardown, and troubleshooting. |
| `commits` | Conventional Commits — type/scope/subject rules, commit size, merge strategy, and message quality checklist. |
| `contracts` | Full-stack API contracts — ownership, versioning, schema generation, validation, and consumer-driven contract tests. |
| `cpp` | Modern C++ — RAII, ownership, smart pointers, error handling policy, performance measurement-first, and tooling. |
| `cv-coach` | Analyze, review, and rewrite a CV/resume to modern professional standards. Covers ATS compliance, impact-first bullet points, quantified achievements, keyword gap analysis against a target job description, and output in Markdown or structured plain text. |
| `delivery` | End-to-end delivery discipline — Definition of Done, PR hygiene, CI quality gates, release readiness, and post-release verification. |
| `diagram-tooling` | Produce, modify, validate, and convert architecture diagrams with PlantUML, Mermaid, and open-source tooling. |
| `doc-architecture-model` | Propose or enforce a Documentation Architecture Model (DAM) — purpose-driven doc tree, audience clarity, ownership, and lint compliance. |
| `doc-qa` | Lint and validate Markdown docs — broken links, heading hierarchy, code block fences, and actionable fix list. |
| `dotnet-cli` | .NET CLI build/test/publish workflow — reproducible CI commands, diagnostics, and artifact strategy. |
| `dotnet-testing` | .NET unit and integration testing — xUnit, WebApplicationFactory, testcontainers, FluentAssertions, and CI gating. |
| `e2e` | End-to-End testing — critical flow selection, stable environments, flakiness prevention, and CI gating strategy. |
| `ef-core` |  |
| `elastic` | Elasticsearch/Kibana/ELK - KQL queries, dashboards, alerting rules, and log analysis workflow. |
| `elite-brainstorming` | High-rigor brainstorming playbook that converts ideas into testable bets, delegated execution, and named specialist reviews. |
| `fullstack-test-strategy` | Full-stack test pyramid — risk mapping, unit/integration/contract/E2E allocation, data strategy, CI gating, and flakiness control. |
| `git` | Elite Git workflow — branching discipline, conventional commits, safe rebasing, history hygiene, and conflict resolution. |
| `github-actions` | Elite GitHub Actions CI/CD — security hardening, reusable workflows, quality gates, and structured debug methodology. |
| `github-work-management` | Elite delivery governance — issue lifecycle, Kanban discipline, traceability, WIP enforcement, and review gates. |
| `helm` | Helm chart operations — lint, template rendering, diff, safe upgrade, rollback, and verification. |
| `helm-cli` | Helm CLI operational cheatsheet - inspect, render, upgrade, rollback, and diff workflows. |
| `html-css` | HTML/CSS — semantic structure, accessibility baseline, responsive design, and maintainability. |
| `innovation-sprint` | Short structured ideation sprint — constrained diverge, cluster, score, falsifiable shortlist, and spike plans. |
| `instruction-authoring` | Create scoped instruction files (*.instructions.md) with clear applyTo patterns and non-duplicated rules. |
| `issues` | GitHub Issues triage — classification, labels, acceptance criteria, and planning integration. |
| `js-testing` | JavaScript/TypeScript testing — tooling selection, unit/component/E2E patterns, CI integration, and flakiness prevention. |
| `k9s` | k9s Kubernetes triage UI — fast incident triage, pod/log/event inspection, and rollout verification. |
| `kubectl` | kubectl operational cheatsheet — context/namespace management, workload triage, logs, events, and rollouts. |
| `kubernetes` | Kubernetes workload triage — workload spec review, resource limits, probes, RBAC, logs, and rollback. |
| `lens` | Lens Kubernetes UI - cluster context confirmation, workload inspection, config review, and fix validation. |
| `linters` | Lint and quality gate setup — polyglot linter matrix, CI integration, pre-commit hooks, and adoption strategy. |
| `logs-alerts` | Log analysis and alerting — symptom identification, time-scoped filtering, correlation, and alert rule design. |
| `markdown-docops` | Markdown doc operations for production, modification, linting, restructuring, conversion, import, and export. |
| `mcp-integration` | MCP integration for VS Code and GitHub Copilot - design, install, secure use, and troubleshoot client/server workflows. |
| `mediatr` | MediatR CQRS patterns — commands, queries, handlers, pipeline behaviors, and handler testing. |
| `mermaid` | Mermaid diagrams in Markdown — all diagram types, authoring best practices, GitHub-native rendering, accessibility, and CI validation. |
| `npm` | npm Node tooling — install strategy, standard scripts, lockfile discipline, CI gating, and troubleshooting. |
| `onboarding-factory` | Generate a developer onboarding guide — setup, architecture, conventions, and contribution workflow. |
| `openapi` | OpenAPI/Swagger — operation IDs, response schemas, auth documentation, error responses, and spec validation. |
| `perf-regression` | Performance regression triage — measure-first, baseline comparison, ranked hypotheses, mitigation, and alerting. |
| `perl` | Perl scripting — safety pragmas, error handling, clear structure, and documentation. |
| `pgadmin` | pgAdmin PostgreSQL UI — schema inspection, query plan analysis, migration validation, and safe DB operations. |
| `pic` | PIC firmware — MCU identification, ISR safety, peripheral configuration, memory constraints, and debugging. |
| `planning` | Elite GitHub delivery planning — milestones, roadmaps, prioritization, and cadence governance. |
| `postgres` | PostgreSQL schema design, query optimization, connection management, and PostgreSQL-specific features (JSONB, arrays). |
| `postman` | Postman API collections — domain organization, environment strategy, test assertions, and CI integration. |
| `powershell` | PowerShell automation — error handling, param validation, idempotency, WhatIf support, and PSScriptAnalyzer. |
| `pr-review` | Elite PR review — multi-pass analysis, severity classification, instruction compliance, merge gate decision. |
| `project-orchestration` | End-to-end orchestration workflow for idea clarification, deep planning, specialist dispatch, and delivery governance. |
| `project-takeover` | Analyse en profondeur un ou plusieurs dépôts GitHub on-premise lors d'une prise en charge d'équipe. Produit une documentation exhaustive en français dans un répertoire local `.takeover/` (non commité). Couvre : structure des dépôts, état du Kanban de référence, graphe des sous-modules, dépendances API & BD, décomposition fonctionnelle complète, et plan d'étude point par point. |
| `prompt-authoring` | Create stable, reusable prompt files (.prompt.md) with consistent structure, inputs, outputs, and acceptance criteria. |
| `prompt-engineering` | Prompt engineering for the Copilot Dev Framework - intent, constraints, context, deterministic output, verification, and framework change protocol. |
| `python` | Python scripting — argparse, error handling, idempotency, type hints, and clean exit codes. |
| `rca-kit` | Blameless postmortem and root cause analysis — 5-Whys, timeline, action items, and prevention tracking. |
| `react` | React architecture — component boundaries, state strategy, data fetching, performance, a11y, and testing. |
| `release` | End-to-end release pipeline — SemVer tagging, artifact signing, changelog, smoke test, and rollback. |
| `repo-understanding` | Produce a navigable codebase summary — module map, entry points, key data flows, dependency overview, and doc structure. |
| `rest-api-bootstrap` | Bootstrap a REST API project from zero — curated GitHub template repos, dotnet/pip/cookiecutter CLI commands, and quality snippet sources for C# (.NET), Python (FastAPI/Flask), and Bash (curl/jq client patterns). |
| `rest-api-controller-gen` | Generate a production-ready ASP.NET Core REST API controller (CRUD) from a description, OpenAPI JSON contract, or resource theme — with MediatR handlers, FluentValidation, ProblemDetails, OpenAPI annotations, versioning, and an integration-test checklist. |
| `rfc` | Request for Comments — structured design proposal for cross-team changes with goals, options, risks, and rollout plan. |
| `roadmap` | Actionable roadmap — outcome-driven milestones, dependency and risk register, success metrics, and review cadence. |
| `supply-chain` | Software supply chain hardening — dependency pinning, SBOM, artifact signing, provenance, and policy enforcement. |
| `teams-bot` |  |
| `telegram-bot` | Build production-grade Telegram bots in Python using python-telegram-bot v22+ (Bot API 9.5+). Covers async application setup, handler registration, ConversationHandler dialogs, webhook vs polling, persistence, and security. |
| `test-strategy` | Test pyramid design — risk mapping, test type selection, data strategy, CI gate definition, and flakiness prevention. |
| `threat-modeling` | Step-by-step STRIDE threat modeling playbook: enumerate assets, map trust boundaries, identify and score threats, define mitigations, document residual risk. |
| `triage` | Repro-first debugging triage — minimal reproduction, ranked hypotheses, validated fixes, and prevention. |
| `typescript` | TypeScript type safety — boundary typing, discriminated unions, type guards, runtime validation, and unsafe pattern elimination. |
| `vscode` | VS Code Copilot Dev Framework usage — bootstrap, reload, discoverability, multi-root workspaces, and troubleshooting. |
| `weekly-digest` | Produce a structured weekly tech watch digest — curated by topic, sourced from primaries, with actionable experiments. |
| `whatsapp-bot` | Build WhatsApp bots using the WhatsApp Business Cloud API (Meta). Covers webhook verification, HMAC-SHA256 signature validation, message types (text, template, interactive), Python and C# outbound patterns, and deployment checklist. |
<!-- codev:generated:skills:end -->

---

## Submodule Reference

> **New here?** See [Quick Start — Use CoDev in your project](#quick-start--use-codev-in-your-project) at the top for the 3-step setup.

### Detailed documentation

| Document | Description |
| --- | --- |
| [docs/submodule-guide.md](docs/submodule-guide.md) | Full guide: init, extend, override, upgrade, teardown (5 workflows) |
| [docs/submodule-cli-contract.md](docs/submodule-cli-contract.md) | CLI contract reference: all flags, exit codes, file conventions |
| [docs/mcp-integration-guide.md](docs/mcp-integration-guide.md) | MCP design and operating guide for setup, review, and debugging in VS Code and GitHub Copilot |
| [schemas/codev.schema.json](schemas/codev.schema.json) | `codev.json` JSON Schema with field constraints |

### Bootstrap modes in detail

| Mode | When | Mechanism | Notes |
| --- | --- | --- | --- |
| **Symlink** | Linux / macOS / Windows Developer Mode | Directory symlinks from `.github/{agents,skills,prompts,instructions}/` to submodule | Zero file duplication; updates are instant |
| **Lockfile** | Windows without Developer Mode, or WSL on `/mnt/<drive>/...` | Full file copy to `.github/`; SHA256 manifest in `codev-lock.json` | Run `codev update` after each `git submodule update` |

### Override patterns

| Strategy | File to create | Effect |
| --- | --- | --- |
| `extend` (default) | `codev-overrides/copilot-instructions.override.md` | Appended after submodule base in generated `copilot-instructions.md` |
| `override` | `codev-overrides/copilot-instructions.override.md` | Fully replaces submodule base |

Place additional host-specific agents, skills, prompts, or instructions under `codev-overrides/` — the pre-commit hook will prevent accidental edits to submodule-managed files.

### CLI command reference

| Command | Flags | Purpose |
| --- | --- | --- |
| `codev init` | `--strategy extend\|override` | Bootstrap submodule into host repo |
| `codev update` | — | Re-sync after `git submodule update` |
| `codev teardown` | `--force` | Remove all managed artefacts; `--force` required on Windows |

---

## Capability Extension Protocol

When adding a new capability, agent, skill, prompt, or instruction to this framework:

1. **Domain research (reference-gathering gate)** — before authoring, read ≥2 primary sources relevant to the new domain (official docs, existing skills, instruction files). Synthesise a non-contradictory union and cite sources in the PR body.
2. **Define scope and acceptance criteria** — what does it do, when does it trigger, what does it output?
3. **Reuse existing roles** — check if an existing agent can cover the new capability before creating a new one.
4. **Add or update skills/prompts** — create modular leaf units rather than bloating agent/instruction files.
5. **Update routing** — add entries to all relevant routing files:
   - `routing/capabilities.yaml` — new capability ID and default agent
   - `routing/domains.yaml` — new domain keywords if needed
   - `routing/aliases.yaml` — natural-language aliases for the new capability
   - `routing/matrix.yaml` — routing rules mapping capability + domain → recommendations
6. **Add/update documentation** — update this README, relevant `docs/` files, and skill documentation so all framework references stay current.
7. **Add issue to Kanban board** — use `gh project item-add 2 --owner nist0 --url <issue-url>` immediately after creating the issue, and keep the board status in sync (Todo → In Progress → Done).
8. **Validate** — test the `/route` prompt with representative phrases to confirm correct routing.

### Useful prompts for extension

```text
/new-agent agentId=my-agent mission="What this agent does"
/new-skill skillId=my-skill theme="Theme Name" scope="When to use"
/new-instructions
/new-theme-pack
```
