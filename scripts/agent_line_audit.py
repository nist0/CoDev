import pathlib, re
for p in sorted(pathlib.Path('.github/agents').glob('*.agent.md')):
    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()
    elite=[]; step=[]; skillref=[]; skills_section=[]
    for i,l in enumerate(lines,1):
        if re.search(r'Elite .*procedure|Workflow|Procedure', l):
            elite.append(i)
        if re.match(r'^###\s+.*\b(Step|Phase)\b', l, flags=re.I):
            step.append(i)
        if '.github/skills/' in l and 'SKILL.md' in l:
            skillref.append(i)
        if re.match(r'^##\s+Skills used\b', l):
            skills_section.append(i)
    print(f"{p.as_posix()}|elite={elite}|steps={step}|skillref={skillref}|skills_section={skills_section}")