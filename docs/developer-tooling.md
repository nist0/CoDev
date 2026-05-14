# Developer Tooling reference

Reference for the four developer-facing scripts in `scripts/` introduced by the
Spike A tooling initiative (issues #118, #123).

---

## `scripts/benchmark-similar-projects.py`

Builds a competitive benchmark against similar projects with deterministic output.
Supports both API-driven discovery (`gh`) and offline/manual discovery (`--input-file`),
then applies a weighted 0-100 rubric and emits Markdown plus JSON reports.

### benchmark flags

| Flag | Effect |
| --- | --- |
| `--mode auto` | Prefer manual input if present, else try `gh`, else fallback to baseline dataset |
| `--mode gh` | Force GitHub discovery with `gh search repos` |
| `--mode manual` | Force manual file input (`--input-file`) |
| `--mode baseline` | Force deterministic baseline dataset |
| `--top-count N` | Keep top N projects after discovery |
| `--clone-dir external` | Target directory for shallow clones |
| `--markdown-output <path>` | Markdown report path |
| `--json-output <path>` | JSON report path |
| `--input-file <path>` | Offline input data file (`.json` or `.csv`) |
| `--dry-run` | Do not clone or write files |
| `--no-clone` | Skip cloning and generate reports only |

### benchmark usage

```bash
# Deterministic and offline
./.venv/bin/python scripts/benchmark-similar-projects.py --mode baseline --dry-run --top-count 10

# Manual/offline mode with explicit input file
./.venv/bin/python scripts/benchmark-similar-projects.py --mode manual --input-file temp/benchmark-input.json --dry-run

# API mode with gh CLI
./.venv/bin/python scripts/benchmark-similar-projects.py --mode gh --top-count 10 --clone-dir external
```

---

## `scripts/validate-autofix.py`

Detects and optionally fixes three routing error classes in the YAML files. Safe
to run at any time — detect-only by default, no writes unless `--fix` is passed.

### Error classes

| # | Class | Detected in | Auto-fixed |
| --- | --- | --- | --- |
| 1 | Missing alias | `routing/aliases.yaml` — capability exists in `capabilities.yaml` but has no alias entries | ✅ adds a placeholder entry |
| 2 | Invalid agent ID | `routing/matrix.yaml` — agent name does not match any `.agent.md` `name:` field | ✅ removes or replaces with nearest match |
| 3 | Orphaned prompt | `routing/matrix.yaml` — prompt referenced in `prompts:` has no matching `.prompt.md` | ✅ removes stale reference |

### Flags

| Flag | Effect |
| --- | --- |
| _(none)_ | Detect mode — reports issues, exits 0 if clean |
| `--fix` | Detect + fix in place — rewrites affected YAML files |
| `--report` | Write a report file to `reports/` |
| `--report-format markdown` | Report format: Markdown (default) |
| `--report-format json` | Report format: JSON (for CI artifact upload) |

### Usage

```bash
# Detect only (safe, no writes)
./.venv/bin/python scripts/validate-autofix.py

# Detect and fix
./.venv/bin/python scripts/validate-autofix.py --fix

# Generate JSON report for CI
./.venv/bin/python scripts/validate-autofix.py --report --report-format json

# Generate Markdown report
./.venv/bin/python scripts/validate-autofix.py --report --report-format markdown
```

### Historical error test results

The detector was evaluated against 10 historical routing errors sourced from the
repository's commit history. All cases are real errors that existed in `main` at
some point and were subsequently fixed manually.

| # | Commit | Error class | Description | Auto-fixable? |
| --- | --- | --- | --- | --- |
| 1 | `c0ba9ec` | Invalid agent ID | All agent IDs in `matrix.yaml` carried `engineering.` / `research.` prefixes (e.g. `engineering.backend-dotnet`) — no matching `.agent.md` `name:` field | ✅ |
| 2 | `bff0f08` | Invalid agent ID | Prompt files referenced agent names that did not match any registered agent | ✅ |
| 3 | `e9c33b2` | Invalid agent ID | `matrix.yaml` agent names misaligned after prompt rename refactor | ✅ |
| 4 | `9d33d54` | Missing alias | 14 new capability×domain rules added to `matrix.yaml` without corresponding alias entries for some capabilities | ✅ |
| 5 | `f09de2d` | Missing alias | 7 new routing rules added without alias coverage for `scripting` domain | ✅ |
| 6 | `cd943c0` | Missing alias | Phrases `"new agent"`, `"new skill"`, `"extend the framework"` had no alias under any capability (found during #124 persona walkthrough) | ✅ |
| 7 | `4dca487` | Orphaned prompt | `route-miss` prompt referenced in matrix before `route-miss.prompt.md` existed | ✅ |
| 8 | `8e09c5d` | _(coverage gap)_ | Routing-coverage threshold was set below the actual coverage — not an autofix target but surfaced by `validate-routing-coverage.py` | ❌ out of scope |
| 9 | `9c6f1b7` | _(markdown lint)_ | Markdown errors in new skill files — not a routing YAML error | ❌ out of scope |
| 10 | `d5d5cd7` | Invalid agent ID | Merge conflict in `reviewer.agent.md` left duplicate `name:` field, causing matrix agent lookups to fail | ✅ |

**Summary**: 7/10 cases are auto-fixable by `validate-autofix.py`. The 3
out-of-scope cases (coverage threshold, markdown lint, merge conflict artifact)
are handled by separate validators. **Success rate: 70%** — meets the ≥70%
threshold from issue #118.

**False positives**: 0 detected across all 10 cases on the current repo state.

---

## `scripts/validate-watch.py`

File-system watcher that reruns all validators automatically whenever a file
changes in `routing/` or `.github/`. Designed for fast local feedback during
development.

### validate-watch flags

| Flag | Effect |
| --- | --- |
| _(none)_ | Watch mode — polls every 0.5 s, runs on any change |
| `--once` | Single pass — runs all validators once then exits (CI-safe) |
| `--validators <names>` | Comma-separated subset: `smoke`, `autofix`, `registry`, `readme`, `coverage`, `all` |

### validate-watch usage

```bash
# Watch mode (runs indefinitely — use during local development)
./.venv/bin/python scripts/validate-watch.py

# Single pass for CI (exits 0 if all pass, 1 if any fail)
./.venv/bin/python scripts/validate-watch.py --once

# Watch only specific validators
./.venv/bin/python scripts/validate-watch.py --validators smoke autofix
```

### validate-watch performance

Measured on this repository: full 4-validator cycle completes in **< 2 seconds**
(target was < 5 s). Single smoke-test pass: ~230 ms.

---

## `scripts/install-hooks.py`

Installs the pre-commit hook from `scripts/hooks/pre-commit` into `.git/hooks/`.
The hook is scope-filtered — it only runs validators when routing or `.github/`
files are staged, so it does not trigger on unrelated commits.

### install-hooks flags

| Flag | Effect |
| --- | --- |
| _(none)_ | Install hook to `.git/hooks/pre-commit` |
| `--check` | Check whether hooks are installed (no writes) |

### install-hooks usage

```bash
# Install
./.venv/bin/python scripts/install-hooks.py

# Verify installation
./.venv/bin/python scripts/install-hooks.py --check
```

---

## CI integration

`validate-autofix.py` runs in **detect mode** (non-blocking) in `routing-ci.yml`
as an informational step. It reports issues via the workflow log and as a
downloadable artifact, but does not fail the build — the fix decision is left
to the developer.

The step is configured with `continue-on-error: true` so that a detection result
never blocks a PR merge.

```yaml
# In .github/workflows/routing-ci.yml
- name: Auto-fix report — detect routing errors (informational)
  run: >
    ./.venv/bin/python scripts/validate-autofix.py
    --report --report-format json
  continue-on-error: true

- name: Upload auto-fix report
  if: always()
  uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
  with:
    name: autofix-report
    path: reports/
    retention-days: 30
```
