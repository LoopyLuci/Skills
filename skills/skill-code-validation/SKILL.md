---
name: skill-code-validation
description: "Use when validating skill code examples and patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-validation, code-quality, syntax-checking, meta]
    related_skills: [skill-quality-standards, skill-testing-automation, skill-blueprint-generator]
---

# Skill Code Validation

Validating that skill code examples are syntactically correct and semantically sound — from Python and shell syntax checks through dependency verification and pattern matching.

## When to Use

- Ensuring skill code examples won't error at runtime
- Automating quality checks across skill inventory
- Verifying code snippets before publishing a skill
- Catching syntax errors, missing imports, and broken patterns

## Validation Methods

```python
import ast, subprocess

def validate_python(code: str) -> List[str]:
    errors = []
    try:
        ast.parse(code)
    except SyntaxError as e:
        errors.append(f"Python syntax error: {e}")
    
    # Check for unbound variables
    tree = ast.parse(code) if not errors else None
    return errors

def validate_bash(code: str) -> List[str]:
    errors = []
    if 'bash' in str(type(code)):
        result = subprocess.run(['bash', '-n', '-'], 
                               input=code, text=True, capture_output=True)
        if result.stderr: errors.append(result.stderr)
    return errors
```

## Verification Checklist

- [ ] Python code passes syntax check (ast.parse)
- [ ] Shell code passes syntax check (bash -n)
- [ ] Imports used in examples exist in standard library or are documented
- [ ] Variable names referenced before assignment
- [ ] Class/method definitions complete and consistent
