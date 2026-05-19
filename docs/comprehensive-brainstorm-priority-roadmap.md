# Comprehensive Brainstorm Priority Roadmap

## 1) Benchmark context and source files

This document consolidates benchmark context, brainstorming analysis, execution-ready
priorities, and specialist review outcomes for CoDev.

### Benchmark context

- Baseline benchmark run date: 2026-05-13.

- Top benchmark set: 10 projects scored with weighted criteria.

- Primary benchmark document: `docs/competitive-benchmark-and-enhancement-roadmap.md`.

- Benchmark script mode used for determinism: `baseline`.

### Benchmark source files

- `scripts/benchmark-similar-projects.py`.

- `docs/competitive-benchmark-and-enhancement-roadmap.md`.

- `temp/benchmark-similar-projects.md`.

- `temp/benchmark-similar-projects.json`.

- `reports/autofix-20260305T134831Z.md`.

- `reports/autofix-20260305T134828Z.json`.

- `routing/capabilities.yaml`.

- `routing/domains.yaml`.

- `routing/aliases.yaml`.

- `routing/matrix.yaml`.

## 2) Brainstorming framing

### Objective

Increase CoDev delivery confidence, customisation quality, and contributor velocity
while preserving deterministic routing and governance discipline.

### Constraints

- Keep deterministic routing behaviour as the primary invariant.

- Avoid introducing non-reproducible CI or benchmark checks.

- Minimise additional maintenance burden for contributors.

- Maintain compatibility with current repository structure conventions.

- Preserve markdownlint-friendly documentation standards.

### Assumptions

- Contributors rely on docs and scripts more than IDE-only guidance.

- Benchmark evidence should remain reproducible in offline baseline mode.

- Routing quality can regress silently without explicit coverage checks.

- Governance complexity is acceptable only if guidance is actionable.

- Incremental rollout is preferred over broad one-shot changes.

### Success metric

Within 2 sprints:

- Routing validation pass rate remains 100 percent in CI.

- New benchmark refresh workflow succeeds in 3 consecutive runs.

- Median time to first successful contribution decreases by 25 percent.

- At least 80 percent of top-priority enhancements are implemented.

## 3) Option portfolio (10 options)

| Option | Type | Summary | Effort | Expected impact | Risk |
| --- | --- | --- | --- | --- | --- |
| O1 | Safe | Add benchmark CI smoke and artifact publication | S | High | Low |
| O2 | Safe | Add benchmark JSON schema and strict validation tests | S | High | Low |
| O3 | Safe | Add docs command index and validator map pages | M | Medium | Low |
| O4 | Adjacent | Add monthly benchmark refresh workflow with trend snapshots | M | High | Medium |
| O5 | Adjacent | Add score breakdown table per project and tie-break tests | M | High | Medium |
| O6 | Adjacent | Add plugin-based scoring criteria extension mechanism | M | Medium | Medium |
| O7 | Adjacent | Add route coverage guardrail for capability and domain drift | M | High | Medium |
| O8 | Bold | Build issue automation for benchmark refresh and dispatch map | L | High | Medium |
| O9 | Bold | Build guided contributor workflow command in `codev-dev.py` | L | High | Medium |
| O10 | Bold | Introduce continuous quality dashboard from reports and routing | L | High | High |

## 4) Top 3 shortlist with scoring and full analysis

### Scoring model

Weighted score out of 100:

- Impact on reliability: 30.

- Delivery speed gain: 25.

- Adoption friction: 20.

- Maintenance cost: 15.

- Implementation risk: 10.

Higher score is better.

### Shortlist ranking

| Rank | Option | Score | Why shortlisted |
| --- | --- | --- | --- |
| 1 | O1 | 88 | Fastest path to durable reliability signal |
| 2 | O4 | 83 | Adds trend visibility and planning cadence |
| 3 | O7 | 80 | Protects routing quality from silent drift |

### Option O1 analysis

#### O1 inversion

If O1 fails, likely causes are flaky CI execution, unclear artifacts, or duplicated
checks that slow merges. Countermeasure: keep a single smoke path with explicit
artifact naming and bounded runtime.

#### O1 reference class

Comparable repos that introduced deterministic smoke checks typically reduced
regression discovery time and lowered debugging cost for script changes.

#### O1 second-order effects

- Positive: clearer release confidence and easier contributor self-validation.

- Negative: increased CI minutes and noise if failure messages are weak.

#### O1 pre-mortem

Failure scenario in 30 days:

- Smoke workflow exists but is ignored because output is unclear.

- Artifact is produced but not linked from docs.

Preventive action:

- Add explicit README link and failure triage section.

- Ensure artifacts include concise summary markdown.

### Option O4 analysis

#### O4 inversion

If O4 fails, monthly workflow may produce stale or noisy data due to unstable
sources. Countermeasure: baseline fallback and tagged snapshots with metadata.

#### O4 reference class

Projects with periodic benchmark refresh and trend tracking usually improve roadmap
discipline and justify priority changes with evidence instead of intuition.

#### O4 second-order effects

- Positive: supports planning discussions with measurable trends.

- Negative: can bias teams toward score chasing over user value.

#### O4 pre-mortem

Failure scenario in 60 days:

- Workflow runs but trend snapshots are not consumed.

- Score changes are misinterpreted without criteria breakdown.

Preventive action:

- Add trend interpretation notes in docs.

- Store criterion-level breakdown beside top-line score.

### Option O7 analysis

#### O7 inversion

If O7 fails, routing guardrails can block valid changes and frustrate contributors.
Countermeasure: clear exceptions policy and deterministic coverage thresholds.

#### O7 reference class

Routing-centric frameworks with explicit drift detection tend to preserve quality,
but must tune thresholds to avoid over-enforcement.

#### O7 second-order effects

- Positive: fewer route regressions and clearer ownership boundaries.

- Negative: initial setup complexity and possible false alarms.

#### O7 pre-mortem

Failure scenario in 45 days:

- Coverage rule triggers frequent false negatives.

- Contributors bypass checks through ad hoc process exceptions.

Preventive action:

- Add fixture-based tests for edge cases.

- Add documented exception process with expiry.

## 5) Hypotheses, evidence thresholds, kill criteria, rollback, spike plan

### O1 hypothesis package

- Hypothesis: benchmark CI smoke reduces undetected benchmark regressions by at
  least 60 percent.

- Evidence threshold: zero missed benchmark script regressions across 3
  consecutive PR cycles where script or docs change.

- Kill criteria: if smoke job adds more than 15 percent median CI duration for 2
  consecutive weeks without measurable defect reduction.

- Rollback posture: disable workflow trigger, keep script and docs changes,
  revert CI workflow file only.

- Spike plan: 1 day.

  - Implement minimal workflow.

  - Validate artifact upload and deterministic runtime.

  - Measure CI duration delta.

### O4 hypothesis package

- Hypothesis: monthly trend snapshots improve roadmap reprioritisation quality,
  measured by fewer priority reversals in sprint planning.

- Evidence threshold: at least 2 roadmap reprioritisation decisions cite trend
  data over 2 planning cycles.

- Kill criteria: if monthly job produces unstable outputs in 2 consecutive runs
  with no reproducible baseline fallback.

- Rollback posture: stop scheduler, retain manual benchmark path and trend docs.

- Spike plan: 2 days.

  - Add scheduled workflow with baseline fallback.

  - Persist timestamped snapshots.

  - Add trend summary table generation.

### O7 hypothesis package

- Hypothesis: route coverage guardrails reduce post-merge routing regressions by
  at least 50 percent.

- Evidence threshold: no unplanned route fallback regressions in 1 month.

- Kill criteria: if false positive rate exceeds 20 percent of routing changes in
  one sprint.

- Rollback posture: relax threshold and convert hard fail to warning while
  retaining diagnostics artifact.

- Spike plan: 2 days.

  - Implement guardrail in validation script.

  - Add fixture tests for known edge cases.

  - Run against historical routing scenarios.

## 6) Final recommendation

Proceed in this sequence:

1. Implement O1 first as immediate reliability anchor.

2. Implement O7 second to protect routing invariants.

3. Implement O4 third to support data-driven planning.

Rationale:

- This sequence balances low-risk wins with structural quality improvements.

- It preserves deterministic behaviour while introducing measurable governance.

- It creates evidence for broader investments such as O8 to O10.

## 7) Ranked enhancement backlog (32 enhancements)

Priority scale:

- P0 = critical now.

- P1 = high value next.

- P2 = medium value planned.

- P3 = opportunistic.

| Rank | Priority | Enhancement | Rationale |
| --- | --- | --- | --- |
| 1 | P0 | Add benchmark CI smoke job with artifact upload | Fastest reliability gain and regression visibility |
| 2 | P0 | Add strict JSON schema validation for benchmark output | Prevents silent contract drift |
| 3 | P0 | Add tie-break determinism tests for benchmark ranking | Ensures reproducible ordering |
| 4 | P0 | Add route coverage drift guardrail in CI | Protects core routing behaviour |
| 5 | P0 | Add failure triage notes for benchmark workflow | Reduces fix time during CI failures |
| 6 | P0 | Add docs link from README to benchmark roadmap | Improves discoverability for contributors |
| 7 | P0 | Add benchmark command index in developer tooling docs | Lowers onboarding friction |
| 8 | P1 | Add monthly scheduled benchmark refresh workflow | Establishes evidence cadence |
| 9 | P1 | Store timestamped benchmark snapshots in reports | Enables trend analysis |
| 10 | P1 | Add criterion-level score table per project | Improves prioritisation clarity |
| 11 | P1 | Add manual mode input schema checks | Prevents malformed candidate data |
| 12 | P1 | Add parser tests for malformed CSV and whitespace | Hardens offline mode |
| 13 | P1 | Add benchmark dry-run policy check for write-capable scripts | Enforces safe defaults |
| 14 | P1 | Add route-smoke fixture expansion for ambiguous prompts | Improves classification resilience |
| 15 | P1 | Add validator mapping page with failure examples | Speeds contributor troubleshooting |
| 16 | P1 | Add benchmark comparator section to dev guide | Supports strategic decisions |
| 17 | P1 | Add issue template for benchmark refresh cycles | Improves governance consistency |
| 18 | P1 | Add gh authentication troubleshooting section | Reduces environment setup blockers |
| 19 | P1 | Add reproducibility checklist for baseline refresh | Protects repeatability |
| 20 | P1 | Add `codev-dev.py` wrapper command for benchmark run | Improves UX and command consistency |
| 21 | P2 | Add plugin-based scoring criteria extension | Supports custom adoption contexts |
| 22 | P2 | Add optional repository language filter flag | Improves candidate quality |
| 23 | P2 | Add minimum stars threshold option | Reduces low-signal noise |
| 24 | P2 | Add clone size threshold skip option | Controls resource usage |
| 25 | P2 | Add report mode to suppress clone action section | Supports docs-only workflows |
| 26 | P2 | Add synthetic fixture generator for benchmark tests | Improves test breadth |
| 27 | P2 | Add CI policy check for positive top-count value | Prevents runtime misconfiguration |
| 28 | P2 | Add docs cross-links to submodule and tooling guides | Improves navigation coherence |
| 29 | P2 | Add benchmark trend summary command output | Improves release communication |
| 30 | P2 | Add routing change impact report in CI artifacts | Improves review signal quality |
| 31 | P3 | Add contributor wizard for route-only changes | Nice UX improvement with moderate effort |
| 32 | P3 | Add quarterly governance checklist for benchmark updates | Maintains long-term discipline |

## 8) Issue-ready dispatch map

| Task ID | Scope | Depends on | Acceptance criteria | Verification command |
| --- | --- | --- | --- | --- |
| T1 | Benchmark CI smoke workflow | None | Workflow runs in baseline mode and uploads artifact summary | `python scripts/benchmark-similar-projects.py --mode baseline --top-count 10 --clone-dir external --markdown-output reports/benchmark-similar-projects.md --json-output reports/benchmark-similar-projects.json` |
| T2 | JSON schema and output validation tests | T1 | Invalid output fails; valid output passes in CI | `python scripts/validate-routing-coverage.py` |
| T3 | Tie-break and parser edge-case tests | T2 | Deterministic rank ordering test passes | `python -m pytest tests/test_benchmark_similar_projects.py -v` |
| T4 | Route drift guardrail | None | Route coverage gate fails on intentional drift fixture | `python scripts/validate-route-smoke.py` |
| T5 | Monthly refresh workflow and snapshots | T1, T2 | Scheduled run publishes timestamped files in reports | `python scripts/benchmark-similar-projects.py --mode baseline --dry-run --top-count 10 --clone-dir external --markdown-output reports/benchmark-similar-projects.md --json-output reports/benchmark-similar-projects.json` |
| T6 | Docs command index and validator map | T1, T4 | Docs include all validated commands and links | `python scripts/validate-markdown-lint.py` |
| T7 | Benchmark issue template and governance checklist | T5, T6 | New issue template is usable and checklist complete | `python scripts/validate-customization-registry.py` |
| T8 | `codev-dev.py` wrapper benchmark command | T1, T3 | Wrapper executes baseline benchmark successfully | `python scripts/codev-dev.py --help` |

## 9) Specialist review lines

(Agent: Innovator) approved - Option portfolio is balanced across safe, adjacent, and bold bets.

(Agent: Project-Orchestrator) approved - Dispatch map has explicit dependencies and verification commands.

(Agent: Reviewer) rework required - Add criterion-level score trend section for each monthly snapshot output.

(Agent: Reliability) approved - Hypotheses and kill criteria are falsifiable and operationally measurable.

(Agent: Testing-Quality) approved - Priority ordering correctly front-loads deterministic test coverage.

## 10) Execution order summary

1. Ship T1 to T3 in sequence.

2. Ship T4 in parallel with T2 and T3 where possible.

3. Ship T5 after T1 and T2 stabilise.

4. Ship T6 to T8 as consolidation and adoption accelerators.

This roadmap is intended to be revisited monthly after benchmark refresh.
