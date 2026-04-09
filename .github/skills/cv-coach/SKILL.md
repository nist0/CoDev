---
name: cv-coach
description: >
  Analyze, review, and rewrite a CV/resume to modern professional standards.
  Covers ATS compliance, impact-first bullet points, quantified achievements,
  keyword gap analysis against a target job description, and output in
  Markdown or structured plain text.
argument-hint: "[cv-file-or-text] [target-role] [target-jd-url-or-text]"
user-invocable: true
disable-model-invocation: false
---

# CV Coach (Elite)

## When to use

- Reviewing an existing CV and producing an actionable critique.
- Rewriting a CV to modern standards (ATS, impact-first, quantified).
- Tailoring a CV to a specific job offer (keyword gap analysis).
- Producing a fresh CV from a candidate self-description.
- Coaching a candidate through CV best practices.

## Pre-requisites

Collect from the user before starting:

| Input | Required | Notes |
|---|---|---|
| Current CV (text, Markdown, .docx, paste) | Yes | If absent, offer to build from scratch via guided interview |
| Target role / job title | Yes | e.g. "Senior Software Engineer", "Lead DevOps" |
| Target industry / company type | Recommended | e.g. startup, enterprise, public sector |
| Seniority level | Recommended | Junior / Mid / Senior / Lead / Exec |
| Target job description (JD) | Optional | Required for keyword gap analysis (Step 5) |
| Geographic market | Optional | FR / EN / international — affects format norms |

If any required input is missing, ask in a single message (never split questions over multiple turns).

---

## Procedure

### Step 1 — Parse and structure the raw CV

Extract and organise all content into the following canonical sections:

| Section | Contains |
|---|---|
| Identity | Name, email, phone, LinkedIn, GitHub/portfolio, location |
| Summary / Headline | 2-4 sentence professional pitch or objective |
| Work Experience | Role, company, location, dates, bullet-point achievements |
| Skills | Technical skills, tools, frameworks, languages |
| Education | Degree, institution, dates, notable projects/grades |
| Certifications | Name, issuer, date/expiry |
| Languages | Language + level (CEFR/IELTS/TOEFL where relevant) |
| Optional | Publications, open-source, volunteering, talks, awards |

For each work experience entry, map bullets to:
- **Action verb** (start of bullet)
- **Task / context** (what was done)
- **Result / impact** (quantified if possible)

Flag sections that are:
- Missing (mandatory: Identity, Work Experience, Skills, Education)
- Thin (fewer than 2 bullet points per experience)
- Unquantified (no numbers, %, timeframes, or scales)
- Outdated (experiences > 10 years unless strategic)
- Redundant or padded

---

### Step 2 — Diagnose quality against modern standards

Score each dimension on a 1-5 scale and produce a critique table:

| Dimension | Score (1-5) | Finding | Recommended fix |
|---|---|---|---|
| ATS compatibility | | | |
| Impact quantification | | | |
| Action verb diversity | | | |
| Keyword density (role-match) | | | |
| Summary / headline quality | | | |
| Visual / structural clarity | | | |
| Length appropriateness | | | |
| Relevance (to target role) | | | |
| Language quality | | | |
| Modern formatting | | | |

**Scoring guide:**
- 5 = Excellent, no change needed
- 4 = Good, minor polish
- 3 = Adequate, improvement recommended
- 2 = Weak, significant rewrite needed
- 1 = Missing or severely deficient

**Modern standards reference (2025):**
- Length: 1 page for <5 yrs exp; 2 pages for 5-15 yrs; max 3 pages for senior/exec.
- ATS: no tables, headers/footers, images, or text boxes for ATS-destined versions.
- Action verbs: strong, varied, active voice — avoid "responsible for", "helped with".
- Quantification: aim for >=60% of experience bullets to contain a number or measurable outcome.
- Summary: 3-4 lines, first-person omitted, role-specific, top-loaded with keywords.
- Skills section: grouped by category (languages, frameworks, tools, soft skills) — not a raw dump.
- Dates: month + year for recent roles; year-only acceptable for roles > 5 yrs old.
- Links: LinkedIn and GitHub must be active and professional (custom slug preferred).
- No photos, no marital status, no date of birth (FR exception: optional but dated practice).

---

### Step 3 — Identify critical blockers

Flag these as P0 (must fix before any application):

- [ ] Contact information incomplete or broken (bad email, dead LinkedIn link)
- [ ] Unexplained employment gaps > 6 months
- [ ] Timeline inconsistencies (overlapping dates, missing years)
- [ ] No quantified achievements anywhere
- [ ] Generic / copy-paste summary with no differentiation
- [ ] Skills section lists outdated technologies as primary skills
- [ ] Spelling or serious grammar errors
- [ ] File name format: use `Firstname-Lastname-CV-Role-Year.pdf` (never "Mon CV.docx")

---

### Step 4 — Rewrite (impact-first, quantified)

For each work experience entry, rewrite bullets using the formula:

```
[Strong action verb] + [what you did / scope] + [measurable outcome / impact]
```

**Action verb bank (by category):**

| Led / Directed | Built / Implemented | Improved / Optimised | Analysed / Designed |
|---|---|---|---|
| Led, Orchestrated, Spearheaded, Drove, Championed | Built, Implemented, Developed, Deployed, Automated | Reduced, Improved, Increased, Accelerated, Optimised | Designed, Architected, Modelled, Analysed, Evaluated |
| Mentored, Coached, Managed | Migrated, Integrated, Shipped, Delivered | Eliminated, Simplified, Standardised | Researched, Benchmarked, Audited |

**Examples — before / after:**

| Before (weak) | After (strong) |
|---|---|
| Responsible for the backend API | Architected and delivered a REST API serving 2M+ requests/day, reducing p99 latency from 800ms to 120ms |
| Helped the team with DevOps tasks | Automated CI/CD pipelines with GitHub Actions, cutting deployment time from 45 min to 8 min |
| Worked on React frontend | Led migration of legacy AngularJS frontend to React 18, improving Lighthouse score from 62 to 94 |
| Managed a team of developers | Managed a 5-engineer team across 3 time zones, delivering 4 major features on schedule in Q3 2024 |

**Quantification prompts to ask the user when data is missing:**
- "How many users / requests / transactions did this system handle?"
- "By how much did the change improve performance / cost / time?"
- "What was the team or budget size you managed?"
- "What was the release cadence or sprint velocity before/after?"

---

### Step 5 — Keyword gap analysis (when JD provided)

1. Extract all hard skills, technologies, and role-specific terms from the target JD.
2. Cross-reference against skills and experience sections of the CV.
3. Produce a gap table:

| Keyword from JD | Present in CV? | Recommended action |
|---|---|---|
| Kubernetes | Yes (Step 2, 2023) | Already covered |
| Terraform | No | Add to skills; mention in relevant experience if applicable |
| Lead / Staff Engineer behaviours | Partial | Strengthen leadership bullets in last 2 roles |
| GDPR compliance | No | Add if genuinely applies; do not fabricate |

4. Suggest natural language bridges: phrases that cover the gap without fabrication.
5. Recommend a "tailored summary" specific to this JD.

**Rule**: never add skills or experiences the candidate does not have. Only surface what already exists but was not prominently stated.

---

### Step 6 — Produce the rewritten CV

Output the rewritten CV in Markdown with this structure:

```markdown
# [Full Name]
[City, Country] | [email@example.com] | [+XX XX XX XX XX] | [linkedin.com/in/slug] | [github.com/handle]

---

## Summary
[3-4 sentence professional pitch, role-specific, quantified where possible]

---

## Experience

### [Role Title] | [Company] | [City] | [Month Year] - [Month Year or Present]
- [Rewritten bullet 1]
- [Rewritten bullet 2]
- [Rewritten bullet 3]

[Repeat for each role, most recent first]

---

## Skills

| Category | Technologies / Tools |
|---|---|
| Languages | Python, TypeScript, C#, SQL |
| Frameworks | ASP.NET Core, React, FastAPI |
| DevOps & Cloud | Azure, GitHub Actions, Kubernetes, Terraform |
| Tools | Git, Docker, Postgres, Redis |

---

## Education

### [Degree Name] | [Institution] | [City] | [Year] - [Year]
[Optional: notable project, grade, or distinction]

---

## Certifications
- [Certification Name] — [Issuer] — [Year]

---

## Languages
- French: Native
- English: Professional working proficiency (C1)

---

## Notable Projects (optional)
### [Project Name] | [github.com/link or URL]
[1-2 sentence description with tech stack and impact]
```

---

### Step 7 — Produce the coaching summary

Deliver a concise handoff card:

```text
## CV coaching summary — [Candidate Name]
Target role: [Role]
Overall score: [X/50] — [Excellent / Good / Needs work / Critical issues]

P0 blockers (fix before applying):
- [List any P0 issues]

Top 3 improvements made:
1. [e.g. Quantified 8/10 experience bullets]
2. [e.g. Rewrote summary to target [Role] keywords]
3. [e.g. Restructured skills into categories]

Keyword coverage (if JD provided): [N/M keywords matched] ([%])

Recommended next steps:
1. [e.g. Add 2025 GitHub activity to portfolio]
2. [e.g. Request LinkedIn recommendation from recent manager]
3. [e.g. Tailor skills section for each application]

File naming: [Firstname-Lastname-CV-[Role]-[Year].pdf]
```

---

## Non-negotiables

- **Never fabricate** experience, metrics, skills, or certifications.
- **Never remove** real experience without explaining why and confirming with the user.
- Ask for quantification data before writing "estimated" numbers.
- For FR market: include LinkedIn URL; date of birth and photo are optional but note they are dated practice.
- For EN/international market: omit photo, DOB, marital status; LinkedIn is mandatory.
- Always offer both ATS-safe (no tables/columns) and design-optimised versions.
- Respect the candidate's authentic voice — do not over-formalise a creative profile.
- Content must be in the language of the target market (FR / EN) unless the candidate requests otherwise.

---

## Self-check

- [ ] All 7 steps executed (or explicitly skipped with reason).
- [ ] Critique table produced with scores and findings.
- [ ] P0 blockers identified and addressed.
- [ ] >=60% of experience bullets quantified in the rewritten CV.
- [ ] Action verbs are strong, active, and varied.
- [ ] Keyword gap analysis done if a JD was provided.
- [ ] Coaching summary card produced.
- [ ] No fabricated information.
- [ ] Output is copy/paste-ready Markdown.
