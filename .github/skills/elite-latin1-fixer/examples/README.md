Usage examples for the elite-latin1-fixer skill.

1) Inspect a single file (no changes):

```
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --file .github/agents/implement.agent.md --list-only
```

2) Apply changes to a single file with an in-place `.bak` backup and create a JSON log:

```
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --file .github/agents/implement.agent.md --apply --backup --log reports/latin1-fixer-implement.json
```

3) Batch-run across tracked `.github` markdown files (recommended only after pilot review):

```
python .github/skills/elite-latin1-fixer/tools/latin1_fixer.py --glob ".github/**/*.md" --apply --backup --log reports/latin1-fixer-batch.json
```

Notes
- Start with `--list-only` or `--dry-run` to inspect proposed replacements.
- Backups are written next to each file as `<file>.bak`.
- The script produces a JSON log summarizing replacements and size diffs.
