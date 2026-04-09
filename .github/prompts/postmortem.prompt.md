---
name: postmortem
description: "Generate a blameless postmortem draft with timeline, RCA, and action items."
agent: "Reliability"
argument-hint: "incident=<title> date=<YYYY-MM-DD> duration=<HHhMMm> severity=<P1-P4>"
---
Apply the procedure from `.github/skills/rca-kit/SKILL.md`.

Act as a Reliability engineer and create a blameless postmortem in Markdown.

Include:

- Summary
- Impact
- Timeline
- Root cause and contributing factors
- Detection & response
- Corrective actions (owners + due dates)
- Preventative actions

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Reliability** | always — postmortem creation | *(this prompt)* | Blameless postmortem drafted with timeline, RCA, corrective and preventative actions |
| 2 | **Project Orchestrator** | corrective action items produced | `/project-dispatch` | Action items opened as GitHub issues with owners and due dates |
| 3 | **Project Orchestrator** | action items tracked | `/project-governance` | Issues placed on Kanban board, WIP limits set |
| 4 | **Delivery Lead** | postmortem doc ready | `/pr-review` | Postmortem committed to docs/postmortems/, PR merged |
