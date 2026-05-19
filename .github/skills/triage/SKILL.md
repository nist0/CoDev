---
name: triage
description: Repro-first debugging triage — minimal reproduction, ranked hypotheses, validated fixes, and prevention.
argument-hint: "[error-or-symptom] [environment]"
user-invocable: true

disable-model-invocation: false
---

# Debugging Triage (Elite)

## When to use

- You have an exception, stacktrace, crash, regression, timeout, or wrong output.

- You need a reproducible case and ranked hypotheses before fixing.

- You want a structured triage that separates facts from assumptions.

## Procedure

### 1. Collect context (mandatory before hypothesizing)

| Item | To collect |
|------|------------|
| Environment | OS, runtime version, cloud/local, container vs bare metal |
| Versions | App version, dependency versions, recent upgrades |
| Input | Exact request/payload/data that triggers the issue |
| Timeline | When did it start? What changed around that time? |
| Frequency | Always? Intermittent? Rate? |
| Scope | All users? One tenant? One region? One pod? |
| Recent changes | Last deployment, config change, dependency update |

### 2. Separate facts from assumptions

| Observed facts | Assumptions |
|----------------|-------------|
| <from logs/traces/debugger> | <interpretations or guesses> |

Never propose a fix based on an assumption without a validation step.

### 3. Build minimal reproduction

1. Take the failing case.

2. Strip every component that is not required to trigger the issue.

3. Confirm the minimal case reproduces deterministically.

4. Document minimal repro steps (copy/paste-ready).

If a minimal repro cannot be built: note why and identify the narrowest reproducing scope.

### 4. Extract the first symptom

- Read logs chronologically; find the earliest/most causal error, not the last one.

- Note: timestamp, log level, message, correlation ID, stack trace (top frame).

### 5. Rank hypotheses

Order by `likelihood × (1 / cost to validate)`:

| Rank | Hypothesis | Validation step | Likelihood | Cost |
|------|-----------|-----------------|------------|------|
| 1 | ... | `<command or log query>` | high | low |

- Validate in order; stop when confirmed.

- For each validation, note: expected result (hypothesis true) vs alternative result (hypothesis false).

### 6. Choose fix approach

| Approach | When to use | Risk |
|----------|-------------|------|
| Mitigation | Users impacted now; root cause still unknown | Low |
| Remediation | Root cause confirmed; permanent fix | Medium |
| Hardening | Prevent recurrence after remediation | Low |

Always lead with mitigation if users are impacted; remediation goes through PR review.

### 7. Verify and prevent recurrence

- Confirm fix with the minimal repro (should no longer reproduce).

- Add a regression test that fails before the fix and passes after.

- Add or update an alert/dashboard to detect this failure class earlier.

- Update runbook if this is an operational procedure issue.

## Self-check

- [ ] Context fully collected before hypothesizing.

- [ ] Facts separated from assumptions.

- [ ] Minimal repro documented (copy/paste-ready).

- [ ] First symptom identified (not last).

- [ ] Hypotheses ranked by likelihood × validation cost.

- [ ] Fix validated against minimal repro.

- [ ] Regression test added.

- [ ] Alert/dashboard updated.

## Outputs

- Minimal repro steps (copy/paste-ready).

- Facts vs assumptions table.

- Ranked hypotheses + validation steps.

- Fix options (mitigation vs remediation).

- Verification checklist + regression test intent.

- Prevention actions (alert, dashboard, runbook).
