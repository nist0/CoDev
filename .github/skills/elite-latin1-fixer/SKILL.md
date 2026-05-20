---
name: "elite-latin1-fixer"
description: "Skill to detect and safely replace non-Latin-1 characters and common mojibake sequences in .github Markdown files. Designed for deterministic, reversible edits with backups and reviewability."
---
---

# Elite Latin-1 Fixer

Purpose
- Detect files under `.github/` that contain characters outside ISO-8859-1 (Latin-1) or common mojibake sequences (e.g. `é`, `--`, `§`, `âU+2030¥`).
- Provide deterministic replacement to Latin-1-safe characters or ASCII sequences (e.g. `é`, `--`, `>=`).
- Create `.bak` backups for each modified file, produce a JSON log and diffs for review, and support rollback.

Usage (examples)

Run on a single file (dry-run):

```powershell
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --file .github/agents/implement.agent.md --list-only
```

Run and apply changes with backup and JSON log:

```powershell
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --file .github/agents/implement.agent.md --apply --backup --log reports/latin1-fixer-implement.json
```

Run across all tracked `.github` markdown files (batch):

```powershell
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --glob ".github/**/*.md" --apply --backup --log reports/latin1-fixer-batch.json
```

Acceptance criteria
- All output files contain only characters encodable in ISO-8859-1 (Latin-1).
- For each changed file: a `.bak` exists, JSON log records pre/post sizes and replacements, and a unified diff is produced under `reports/`.
- Review step by `reviewer` agent confirms no semantic loss before backups are removed.

Guidance
- Always run on a single file first for human review before batch applying.
- Use `--dry-run` / `--list-only` to inspect offending characters and proposed replacements.
