import pathlib, re
patterns=[r'^## Elite .*procedure',r'^## Behavior rules',r'^## Workflow',r'^## Skills used',r'\.github/skills/.+/SKILL\.md',r'^### Step',r'^### Phase',r'^## Self-check$']
for p in sorted(pathlib.Path('.github/agents').glob('*.agent.md')):
    lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
    print(p.as_posix())
    for i,l in enumerate(lines,1):
        for pat in patterns:
            if re.search(pat,l):
                print(f'  {i}: {l}')
                break