---
name: skill-test-generation
description: "Use when generating test cases for skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-testing, test-generation, validation, meta, quality]
    related_skills: [skill-code-validation, skill-quality-standards, skill-testing-automation]
---

# Skill Test Generation

Generating and managing test cases for Hermes skills — from automated test generation based on skill content through validation of code examples and verification checklists.

## When to Use

- Creating test suites for skill code examples
- Validating that skill patterns actually work
- Ensuring verification checklist items are testable
- Automating regression testing across skill inventory

## Test Generator

```python
from typing import Dict, List

class SkillTestGenerator:
    """Generate test cases from skill content."""
    
    def extract_code_tests(self, skill_md: str) -> List[Dict]:
        """Extract code blocks and generate test expectations."""
        import re
        blocks = re.findall(r'```python\n(.*?)\n```', skill_md, re.DOTALL)
        tests = []
        for i, block in enumerate(blocks):
            tests.append({
                'id': f'test_code_block_{i}',
                'code': block,
                'expected': 'SyntaxError' if 'SyntaxError' in block else 'runs_successfully',
            })
        return tests
    
    def extract_checklist_tests(self, skill_md: str) -> List[str]:
        """Convert checklist items into testable assertions."""
        import re
        items = re.findall(r'- \[ \] (.*)', skill_md)
        return [{'checklist_item': item, 'testable': len(item) > 10} for item in items]
```

## Verification Checklist

- [ ] Code blocks extracted and syntax-validated
- [ ] Checklist items converted to test assertions
- [ ] Test generator handles multiple code languages
- [ ] Edge cases: empty code blocks, malformed markdown
- [ ] Tests are idempotent (can run repeatedly)
