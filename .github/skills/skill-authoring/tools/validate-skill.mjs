// validate-skill.mjs
import fs from 'fs';
import path from 'path';

const skillDir = process.argv[2];
if (!skillDir) {
  console.error('Usage: node validate-skill.mjs <skill-dir>');
  process.exit(1);
}
const required = ['SKILL.md', 'onboarding.md', path.join('examples', 'README.md')];
const missing = required.filter(f => !fs.existsSync(path.join(skillDir, f)));
if (missing.length) {
  console.error('Missing files:', missing.join(', '));
  process.exit(2);
}
console.log('Skill structure valid.');
