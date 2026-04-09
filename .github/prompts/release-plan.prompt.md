---
name: release-plan
description: "Release plan: versioning, changelog, build artifacts, rollout/rollback, verification, comms."
agent: "Delivery Lead"
argument-hint: "scope=<features or tickets> target-env=<prod|staging> version=<vX.Y.Z>"
---
Act as a Delivery Lead and create a release plan.

Include:

- Release scope and prerequisites
- Versioning plan (SemVer rules + tag strategy)
- Changelog strategy (what to include/exclude)
- Build + artifact outputs
- Rollout steps + rollback steps
- Verification checklist (pre-release and post-release)
- Communication plan (who/when/what)
- Risks and mitigations
- Go/no-go criteria for release approval
- Abort criteria and rollback trigger thresholds

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Delivery Lead** | always — release planning | *(this prompt)* | Release plan produced: scope, versioning, changelog, rollout, rollback, go/no-go criteria |
| 2 | **DevOps/Cloud** | deployment steps involve Kubernetes or Helm | `/helm-triage` or `/k8s-triage` (pre-check) | Deployment readiness confirmed, rollback tested |
| 3 | **Automation/Scripting** | release pipeline automation needed | `/automation-script` | CI/CD pipeline steps scripted and verified |
| 4 | **Reviewer** | release plan sign-off | `/pr-review` | Verdict approved, all go/no-go criteria met |
| 5 | **Delivery Lead** | ready to ship | *(execute release)* | Tag created, artifacts published, comms sent |
