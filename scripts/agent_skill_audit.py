import pathlib,re
agents = sorted(pathlib.Path('.github/agents').glob('*.agent.md'))
print('file|skill_refs|skills_section|step_phase_headings|flag')
for p in agents:
    t = p.read_text(encoding='utf-8', errors='replace')
    skill_refs = len(re.findall(r'\.github/skills/[^\s`)+]+/SKILL\.md', t))
    skills_section = bool(re.search(r'^##\s+Skills used\b', t, flags=re.M))
    step_phase = len(re.findall(r'^###\s+.*\b(Step|Phase)\b', t, flags=re.M|re.I))
    flag = 'YES' if skill_refs==0 and step_phase>=4 else ''
    print(f"{p.as_posix()}|{skill_refs}|{int(skills_section)}|{step_phase}|{flag}")