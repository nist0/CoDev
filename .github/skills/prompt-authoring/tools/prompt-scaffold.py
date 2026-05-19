# Example: prompt-scaffold.py
"""
Scaffold a new prompt file for prompt-authoring skill.
"""
import sys
name = sys.argv[1] if len(sys.argv) > 1 else 'new-prompt.prompt.md'
with open(name, 'w', encoding='utf-8') as f:
    f.write('''---\ndescription: ""\nname: ""\nargument-hint: ""\nagent: ""\n---\n\n# Prompt\n\n''')
print(f'Created {name}')
