# Skill Improving — Examples

## 1. Audit Skill for Required Files

```sh
ls .github/skills/my-skill/
# Should include SKILL.md, onboarding.md, examples/README.md, tools/
```

## 2. Add Examples

```text
echo '# Example usage' >> .github/skills/my-skill/examples/README.md
```

## 3. Run Validation

```sh
python scripts/validate-readme-registry.py
```
