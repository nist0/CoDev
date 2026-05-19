# Summary

- What changed:

- Why:

## Cross-agent review checklist

- [ ] Router: capability/domain mapping is correct

- [ ] Delivery Lead: prompts/skills are reusable and non-duplicated

- [ ] Reviewer: security/reliability/testing constraints respected

- [ ] Routing updates included when adding theme/capability:

  - [ ] routing/capabilities.yaml

  - [ ] routing/aliases.yaml

  - [ ] routing/matrix.yaml

  - [ ] routing/domains.yaml (if needed)

- [ ] Documentation maintained:

  - [ ] .github/copilot-instructions.md updated (if behavior changed)

  - [ ] README.md inventories updated (if coverage changed)

## Validation

- [ ] `python scripts/validate-route-smoke.py` passes locally

- [ ] `python scripts/validate-customization-registry.py` passes locally

- [ ] `python scripts/validate-readme-registry.py` passes locally

- [ ] CI `route-smoke` job is green

## Verdict

- [ ] approved

- [ ] rework required (list gaps)
