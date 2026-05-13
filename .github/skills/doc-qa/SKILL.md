---
name: doc-qa
description: Lint and validate Markdown docs — broken links, heading hierarchy, code block fences, and actionable fix list.
argument-hint: "[docs-path] [fix-mode]"
user-invocable: true
disable-model-invocation: false
---

# Doc QA (Elite)

## When to use

- Linting and validating Markdown documentation.
- Checking for broken links, inconsistent headings, or missing code block fences.
- Running doc quality gates in CI.

## Procedure

### 1. Run markdownlint

```bash
python scripts/validate-markdown-lint.py
```

Scope rule:

- When validating CoDev docs, inspect tracked and non-ignored repository files only.
- Never analyze `external/`.
- Never analyze any path excluded by `.gitignore` or Git's standard excludes.
- Do not replace the repository validator with broad workspace globs such as `**/*.md`.

Common rules to enforce:

| Rule | ID | What it checks |
|------|----|----------------|
| Heading levels | MD001 | No skipped heading levels |
| Trailing spaces | MD009 | No trailing whitespace |
| Blank lines around headings | MD022 | Blank line before/after heading |
| Code block fences | MD040 | Language identifier on all fenced blocks |
| No bare URLs | MD034 | URLs wrapped in `<>` or as links |
| Line length | MD013 | ≤ 120 chars (configure or disable for tables) |

### 2. Check for broken links

```bash
# Internal and external links for tracked, non-ignored docs only
# Prefer a file list derived from Git rather than recursive workspace globs.
```

`.mlc.json` template:

```json
{
  "ignorePatterns": [
    { "pattern": "^https://localhost" }
  ],
  "retryCount": 2,
  "timeout": "20s"
}
```

### 3. Verify heading hierarchy

Check every file:

1. Document starts with exactly one `#` (H1).
2. Headings go `#` → `##` → `###` without skipping levels.
3. No duplicate H1 in a single file.

### 4. Ensure code blocks have language identifiers

Every fenced code block must declare a language:

```markdown
```bash
echo "correct"
```text

```

Search for unlabeled blocks:

```bash
grep -rn '^```$' docs/
```

### 5. Produce fix list

For each issue found:

| File | Line | Rule | Severity | Fix |
|------|------|------|----------|-----|
| docs/foo.md | 42 | MD040 | Warning | Add `bash` to fenced block |

Priority:

1. Broken links (HIGH — affects readers).
2. Missing code block language (MEDIUM — syntax highlighting broken).
3. Skipped headings (MEDIUM — navigation broken).
4. Style lint failures (LOW — cosmetic).

### 6. CI integration

```yaml
- name: Lint docs
  run: python scripts/validate-markdown-lint.py

- name: Check links
  run: <tracked-nonignored-doc-link-check command>
```

Fail the PR if any HIGH issue is found. Warn on MEDIUM/LOW.

## Self-check

- [ ] `markdownlint-cli2` run and errors addressed.
- [ ] Broken links checked (internal and external).
- [ ] Heading hierarchy verified in all files.
- [ ] All fenced code blocks have language identifiers.
- [ ] Fix list produced with file, line, rule, and severity.
- [ ] CI job added for ongoing lint enforcement.
- [ ] Validation scope respected: tracked and non-ignored files only, never `external/` or gitignored paths.

## Outputs

- Lint error list with fix suggestions (file + line + rule).
- Broken link report.
- Doc quality checklist.
- CI lint job YAML snippet.
