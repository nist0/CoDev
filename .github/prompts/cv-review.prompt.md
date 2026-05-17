---
name: cv-review
description: "Critique and rewrite a CV to modern professional standards: ATS compliance, quantified impact bullets, and optional keyword gap analysis against a job description."
agent: "CV Coach"
argument-hint: "target-role=<role> [target-market=FR|EN|INT] [target-jd=<job description text or URL>]"
---


Argument handling:

- If arguments are provided, treat them as authoritative.
- If arguments are omitted, infer missing values from the current workspace, active file, and session context.
- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.
- Do not fail solely because arguments were omitted.

Apply the full procedure from `.github/skills/cv-coach/SKILL.md`.

## Inputs

| Parameter | Required | Example |
|---|---|---|
| `{{target-role}}` | Yes | "Senior Backend Engineer", "Ingénieur DevOps" |
| `{{target-market}}` | Recommended | `FR` (French norms), `EN` (international), default: detect from CV language |
| `{{target-jd}}` | Optional | Paste of job description text or URL — enables keyword gap analysis (Step 5) |
| CV text | Yes | Paste the CV content in the chat, or attach a file |

If the CV is not provided, begin the guided interview (see agent procedure: "If no CV is provided").

## Expected outputs

1. **Critique table** (10 dimensions, scored 1-5) with findings and recommended fixes.
2. **P0 blockers** -- issues that must be fixed before any application.
3. **Rewritten CV** in Markdown, copy/paste-ready, ATS-safe.
4. **Keyword gap table** (only when `{{target-jd}}` is provided).
5. **Coaching summary card** with overall score, top improvements, and next steps.

## Rules

- Execute all 7 steps from the skill unless explicitly skipped.
- Never fabricate skills, metrics, or experiences.
- Ask for quantification data before writing numbers into bullets.
- Use `{{target-market}}` language for the output CV; default to the language of the input CV.
- Deliver the rewritten CV in a fenced Markdown code block for easy copy/paste.
- Flag ATS-compatibility issues explicitly if the candidate targets recruiter portals.
