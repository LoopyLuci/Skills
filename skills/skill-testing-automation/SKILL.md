---
name: skill-testing-automation
description: "Use when validating skills for correctness and freshness."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, testing, validation, automation, quality]
    related_skills: [skill-inventory-management, skill-development-workflow, meta-skill-patterns]
---

# Skill Testing Automation

Automated validation of skills for structural correctness, command freshness, cross-reference integrity, and runtime behavior.

## When to Use

- After creating or patching a skill — verify it's structurally sound
- Before a quarterly audit — batch-validate all skills
- When a skill seems broken (command not found, wrong paths, stale APIs)
- When migrating skills between Hermes versions
- Setting up CI for skill quality

## Validation Checks

### 1. Structural Linting

Verifies every skill's frontmatter and basic structure.

```python
import os, re, yaml

SKILLS_ROOT = os.path.expandvars('$LOCALAPPDATA/hermes/skills')

def lint_skill(skill_path):
    """Lint a single SKILL.md file. Returns list of issues."""
    issues = []
    content = open(skill_path).read()
    rel = os.path.relpath(skill_path, SKILLS_ROOT)
    
    if not content.startswith('---'):
        issues.append(f"{rel}: Does not start with '---'")
        return issues
    
    try:
        m = re.search(r'\n---\s*\n', content[3:])
        if not m:
            issues.append(f"{rel}: No closing '---'")
            return issues
        fm = yaml.safe_load(content[3:m.start()+3])
    except Exception as e:
        issues.append(f"{rel}: YAML parse error: {e}")
        return issues
    
    if not fm.get('name'):
        issues.append(f"{rel}: Missing 'name'")
    if not fm.get('description'):
        issues.append(f"{rel}: Missing 'description'")
    elif len(fm['description']) > 1024:
        issues.append(f"{rel}: Description too long ({len(fm['description'])} > 1024)")
    elif not fm['description'].startswith('Use when'):
        issues.append(f"{rel}: Should start with 'Use when'")
    
    body = content[m.start()+3:]
    if not body.strip():
        issues.append(f"{rel}: Empty body")
    if '## Pitfalls' not in body and '## Common Pitfalls' not in body:
        issues.append(f"{rel}: Missing '## Pitfalls' section")
    
    return issues

# Run on all skills
all_issues = []
for cat in os.listdir(SKILLS_ROOT):
    cat_path = os.path.join(SKILLS_ROOT, cat)
    if not os.path.isdir(cat_path) or cat.startswith('.'):
        continue
    for skill in os.listdir(cat_path):
        sk_path = os.path.join(cat_path, skill, 'SKILL.md')
        if os.path.exists(sk_path):
            all_issues.extend(lint_skill(sk_path))

if all_issues:
    print("ISSUES FOUND:")
    for i in all_issues:
        print(f"  - {i}")
else:
    print("ALL SKILLS PASS STRUCTURAL LINT")
```

### 2. Cross-Reference Integrity

Verifies that every `related_skills` entry actually exists:

```python
def get_all_skill_names():
    names = set()
    for cat in os.listdir(SKILLS_ROOT):
        cat_path = os.path.join(SKILLS_ROOT, cat)
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
        for skill in os.listdir(cat_path):
            names.add(skill)
    return names

def check_references():
    all_names = get_all_skill_names()
    issues = []
    for cat in os.listdir(SKILLS_ROOT):
        cat_path = os.path.join(SKILLS_ROOT, cat)
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
        for skill_name in os.listdir(cat_path):
            sk_path = os.path.join(cat_path, skill_name, 'SKILL.md')
            if not os.path.exists(sk_path):
                continue
            content = open(sk_path).read()
            m = re.search(r'\n---\s*\n', content[3:])
            if not m: continue
            try:
                fm = yaml.safe_load(content[3:m.start()+3])
            except: continue
            refs = (fm.get('metadata', {}) or {}).get('hermes', {}) or {}
            refs = refs.get('related_skills', [])
            if not refs:
                body = content[m.start()+3:]
                refs = re.findall(r'^- (\S+)$', body, re.MULTILINE)
            for ref in refs:
                ref = ref.strip()
                if ref and ref not in all_names:
                    issues.append(f"{skill_name} -> '{ref}' not found")
    return issues

issues = check_references()
if issues:
    print("BROKEN REFERENCES:")
    for i in issues:
        print(f"  - {i}")
else:
    print("ALL REFERENCES RESOLVE")
```

### 3. Command Freshness

Check for known-stale commands:

```python
STALE_PATTERNS = [
    (r'docker-compose\b', 'Use `docker compose` (v2)'),
    (r'`pip install`', 'Prefer `python -m pip install`'),
    (r'node-sass\b', 'node-sass is deprecated; use sass'),
    (r'bower\b', 'bower is deprecated; use npm/yarn'),
]

def check_stale():
    issues = []
    for cat in os.listdir(SKILLS_ROOT):
        cat_path = os.path.join(SKILLS_ROOT, cat)
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
        for skill_name in os.listdir(cat_path):
            sk_path = os.path.join(cat_path, skill_name, 'SKILL.md')
            if not os.path.exists(sk_path): continue
            content = open(sk_path).read()
            for pattern, msg in STALE_PATTERNS:
                if re.search(pattern, content):
                    issues.append(f"{skill_name}: {msg}")
    return issues
```

### 4. Description Truncation Check

First 57 chars of each description must be self-contained (appear in system prompt index):

```python
def check_descriptions():
    issues = []
    for cat in os.listdir(SKILLS_ROOT):
        cat_path = os.path.join(SKILLS_ROOT, cat)
        if not os.path.isdir(cat_path) or cat.startswith('.'):
            continue
        for skill_name in os.listdir(cat_path):
            sk_path = os.path.join(cat_path, skill_name, 'SKILL.md')
            if not os.path.exists(sk_path): continue
            content = open(sk_path).read()
            m = re.search(r'\n---\s*\n', content[3:])
            if not m: continue
            try:
                fm = yaml.safe_load(content[3:m.start()+3])
            except: continue
            desc = fm.get('description', '')
            window = desc[:57]
            if window.endswith('...'):
                issues.append(f"{skill_name}: 57-char window ends with '...'")
            if not window.startswith('Use when'):
                issues.append(f"{skill_name}: doesn't start with 'Use when'")
            if window.strip() and not window.rstrip().endswith('.'):
                issues.append(f"{skill_name}: window should end with period")
    return issues
```

## CI Integration

Add as a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit: validate changed SKILL.md files
CHANGED=$(git diff --cached --name-only --diff-filter=ACM | grep 'SKILL.md$')
[ -z "$CHANGED" ] && exit 0
echo "$CHANGED" | while read -r file; do
    python3 -c "
import yaml, re, sys
content = open('$file').read()
assert content.startswith('---'), f'$file: missing ---'
m = re.search(r'\n---\s*\n', content[3:])
assert m, f'$file: no closing ---'
fm = yaml.safe_load(content[3:m.start()+3])
assert 'name' in fm and 'description' in fm
print(f'  OK: {fm[\"name\"]}')" || exit 1
done
```

## Common Pitfalls

1. **False positives on stale command checks** — use judgement; some patterns are legitimate
2. **Cross-reference checks across profiles** — skills in another Hermes profile aren't visible
3. **Over-validating** — structural perfection doesn't guarantee usefulness; combine with usage stats
4. **Skipping the description window check** — the 57-char truncation is subtle; always verify
5. **Validation scripts drift** — update stale-pattern list quarterly as tools evolve

## Verification Checklist

- [ ] All skills pass structural lint
- [ ] All related_skills cross-references resolve
- [ ] No known-stale commands detected
- [ ] All descriptions self-contained within first 57 chars
- [ ] Broken skills patched or queued for deletion
- [ ] CI hook installed for skill repo

## See Also

- skill-inventory-management — auditing and pruning skills
- skill-development-workflow — building and testing skills
- meta-skill-patterns — design patterns for meta-skills
