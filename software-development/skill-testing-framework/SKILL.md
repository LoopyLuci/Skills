---
name: skill-testing-framework
description: "Use when creating testable skill content and patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta, skill-testing, framework, automation, validation, CI]
    related_skills: [skill-test-generation, skill-code-validation, skill-quality-standards, skill-testing-automation]
---

# Skill Testing Framework

Creating testable skill content — from automated code validation through checklist verification, snippet testing, and CI/CD for skills.

## When to Use

- Ensuring skill code examples actually work
- Automating skill validation in CI
- Creating test suites for skills
- Verifying cross-references are valid
- Testing skill content for completeness

## Framework Design

```python
import ast, json, os, re

class SkillTestSuite:
    """Create and run tests for skills."""
    
    @staticmethod
    def validate_python_blocks(skill_md: str) -> List[Dict]:
        """Extract and syntax-check Python code blocks."""
        results = []
        blocks = re.findall(r'```python\n(.*?)\n```', skill_md, re.DOTALL)
        
        for i, block in enumerate(blocks):
            try:
                ast.parse(block)
                results.append({'block': i, 'status': 'pass'})
            except SyntaxError as e:
                results.append({
                    'block': i, 'status': 'fail',
                    'error': str(e), 'line': e.lineno,
                })
        return results
    
    @staticmethod
    def verify_references(skill_md: str, all_skills: set) -> List[str]:
        """Verify all See Also references point to real skills."""
        refs = re.findall(r'^- ([a-z0-9-]+)', 
                         skill_md.split('## See Also')[-1] if '## See Also' in skill_md else '',
                         re.MULTILINE)
        return [r for r in refs if r not in all_skills]
    
    @staticmethod
    def check_frontmatter(skill_md: str) -> Dict:
        """Validate frontmatter completeness."""
        issues = []
        if not skill_md.startswith('---'):
            issues.append('Missing opening frontmatter ---')
            return {'valid': False, 'issues': issues}
        
        required = ['name', 'description', 'version', 'author']
        fm = skill_md.split('---')[1] if '---' in skill_md else ''
        
        for field in required:
            if f'{field}:' not in fm:
                issues.append(f'Missing required field: {field}')
        
        if 'related_skills:' not in fm:
            issues.append('Missing related_skills (improves discoverability)')
        
        return {'valid': len(issues) == 0, 'issues': issues}
```

## CI Pipeline

```yaml
CI_PIPELINE = """
name: Skill Tests
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate Python examples
        run: python -c "import ast; ast.parse(open('skill.md').read())"
      - name: Check frontmatter
        run: python -c "
      - name: Verify references
        run: python verify_references.py
      - name: Spell check
        uses: codespell-project/actions-codespell@v2
"""
```

## Common Pitfalls

1. **Testing only syntax** — valid syntax doesn't mean valid logic; test logic too
2. **No CI integration** — manual validation doesn't happen; automate it
3. **Brittle tests** — tests that break on minor formatting changes
4. **No reference checking** — broken cross-references degrade navigation
5. **Ignoring non-Python code** — validate bash, YAML, SQL, and configs too

## Verification Checklist

- [ ] Python code blocks pass syntax validation
- [ ] Shell commands pass bash -n validation
- [ ] YAML frontmatter is valid (yaml.load)
- [ ] All See Also references point to existing skills
- [ ] Frontmatter has all required fields
- [ ] CI pipeline runs skill tests on every PR
- [ ] Test failures block skill publishing
- [ ] Spell check runs on skill content
