---
name: "Docs System & Markdown Standards"
description: "Documentation Architecture Model (DAM), consistent markdown structure, lint-friendly docs."

## applyTo: "**/*.md"

# Docs System

- Follow the Documentation Architecture Model (DAM).

- Keep docs modular: small pages with explicit purpose/audience.

- Use consistent heading levels (no skipped levels).

- Use relative links within the repo.

- Use fenced code blocks with language identifiers when possible.

- Enforce markdownlint and link checking in CI.

## Linter-driven rule codification (mandatory)

- When markdownlint reports an error or warning, update this instruction set (or the most specific markdown-focused instruction file) with:

  - the rule identifier (for example `MD022`)

  - the normative requirement to follow

  - one tested, copy/paste-ready example that passes the repository markdownlint configuration

- Treat recurring lint findings as documentation-standard gaps: do not only fix a single file, also codify the rule with a reusable example.

### Tested examples to follow

- `MD022` (headings should be surrounded by blank lines):

  ```md
  Paragraph before heading.

## Section title

  Paragraph after heading.
  ```

- `MD032` (lists should be surrounded by blank lines):

  ```md
  Intro paragraph.

  - Item one

  - Item two

  Closing paragraph.
  ```

- `MD009` (no trailing spaces): use a linter-fix command (`markdownlint --fix`) before committing.

- `MD013` (line length): keep prose lines ≤120 characters; use soft-wrap in editors, not hard wraps at 80.

- `MD026` (no trailing punctuation in headings): headings must not end with `:`, `.`, `!`, or `?`.

  ```md
  <!-- Wrong -->

### Register webhook via curl:

  <!-- Correct -->

### Register webhook via curl

  ```

- `MD031` (fenced code blocks should be surrounded by blank lines): always leave one blank line before and after every fenced block.

  ````md
  Paragraph before the block.

  ```bash
  echo "surrounded by blank lines"
  ```

  Paragraph after the block.
  ````

- `MD040` (fenced code blocks must have a language tag):

  ````md
  ```bash
  echo "always specify a language"
  ```
  ````

## Markdown quality gate (mandatory)

**Applies to**: every task that creates or modifies any `.md` file, regardless of scope or agent.

This gate is **non-negotiable** — it must run before the task is marked done and before a PR is opened or updated.

### Pre-commit automation (install once)

The repository pre-commit hook runs `validate-markdown-lint.py` automatically whenever `.md` files are staged. Install it once after cloning:

```bash
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
# or
python scripts/install-hooks.py
```

The hook blocks the commit and prints the fix command if any markdown error is found.

### Step 1 — Local lint (blocking)

Run the repository validator immediately after writing or editing any markdown:

```bash
python scripts/validate-markdown-lint.py
```

- Exit code must be `0`. Any non-zero exit is a **blocking finding** — fix all violations before proceeding.

- CoDev markdown validation must inspect tracked and non-ignored repository files only.

- Never lint `external/` or any path excluded by `.gitignore` or Git's standard excludes.

- Do not replace this with broad workspace globs such as `npx markdownlint-cli2 "**/*.md"`.

### Step 2 — Remote CI confirmation (blocking before done)

After pushing, confirm the `markdown-lint` CI check is green on the PR before closing the task:

```bash
gh pr checks <PR-number>
```

- The `markdown-lint` job must show ✓. A failing or pending lint check means the task is **not complete**.

- If the CI check fails on content you did not touch (pre-existing violation), open a separate fix PR first and rebase your branch on it — do not suppress or skip the check.

### Enforcement

- Violations found at local lint that are committed anyway are treated as a **process violation**, equivalent to merging with a failing CI gate.

- Any PR review that discovers a markdown lint failure that passed local lint must flag it as a **blocking finding** (`rework required`).

## Doc structure conventions

- Every doc page must have exactly one `# H1` title.

- Keep TOC entries stable; avoid renaming headings without updating all inbound links.

- Prefer tables over long bullet lists for structured comparisons.

- Add a `## See also` or `## References` section when linking to external resources.

---

## 🏆 Elite Section — Top 5% Documentation Practices

- **Docs-as-code pipeline**: Treat docs with the same review rigor as code. PRs that change behavior must update the corresponding doc in the same commit — no "update docs later" tickets.

- **Audience-driven writing**: Every page starts with an explicit audience statement (e.g. `Audience: platform engineer onboarding`). Content that serves no stated audience gets removed.

- **Living ADRs**: Capture architecture decisions in lightweight ADR files (`docs/adr/NNNN-title.md`). Each ADR includes status (Proposed/Accepted/Deprecated), context, decision, and consequences.

- **Link rot prevention**: Run a link-checker (e.g. `lychee`, `markdown-link-check`) in CI on every PR touching `.md` files. Track broken link count as a project health metric.

- **Diagram versioning**: Store diagrams as code (Mermaid, PlantUML, or D2) alongside the docs they describe. Never commit only a rendered PNG without the source.

- **Changelog discipline**: Maintain a `CHANGELOG.md` following Keep a Changelog format. Every user-visible change gets an entry before the PR merges.
