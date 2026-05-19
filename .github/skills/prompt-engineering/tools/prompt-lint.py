# Example: prompt-lint.py
"""
Lint and validate prompt YAML frontmatter and structure for prompt-engineering skill.
"""
import sys, yaml
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    doc = yaml.safe_load(f)
    if 'description' not in doc:
        print('Missing description')
        sys.exit(1)
    print('Prompt is valid')
