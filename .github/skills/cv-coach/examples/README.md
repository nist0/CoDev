# cv-coach Skill — Examples

## Example 1: Quick critique of a provided CV

**User input:**

```text
/cv-review target-role="Senior Backend Engineer" target-market=EN

[paste of CV text]
```

**Expected output:**

- Critique table with scores on 10 dimensions
- List of P0 blockers
- 3-5 concrete rewrites of weak bullets (before/after)
- Coaching summary card

---

## Example 2: Full rewrite with JD tailoring

**User input:**

```text
/cv-review target-role="Lead Site Reliability Engineer" target-jd="[paste of JD]"
```

**Expected output:**

- Full rewritten CV in Markdown
- Keyword gap table (JD keywords vs CV coverage)
- Tailored summary paragraph
- Coaching summary with keyword coverage percentage

---

## Example 3: Build from scratch via guided interview

**User input:**

```text
/cv-review target-role="DevOps Engineer"
(no CV provided)
```

**Agent response (turn 1):**

```text
I'll help you build a CV from scratch. Please answer these questions:

1. Full name, email, LinkedIn URL, GitHub handle?
2. Current or most recent role and company?
3. List your last 3 roles (title, company, dates, 3-5 key things you did)?
4. Key skills (languages, tools, cloud platforms)?
5. Education (degree, institution, year)?
6. Any certifications or notable projects?
```

**After answers:** produces full rewritten CV + coaching summary.

---

## Example 4: French market CV review

**User input:**

```text
/cv-review target-role="Ingénieur Logiciel Senior" target-market=FR
```

**Key differences in output:**

- Language: French
- Format: 2 pages acceptable; French professional norms applied
- Photo and date of birth flagged as optional (declining practice)
- Accroche (summary) in French
- "Compétences" section labelled in French
