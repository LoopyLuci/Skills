---
name: skill-quality-standards
description: "Use when defining quality standards for skills."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill-quality, standards, best-practices, review, checklist, meta]
    related_skills: [skill-testing-automation, skill-inventory-management, meta-skill-patterns, skill-blueprint-generator]
---

# Skill Quality Standards

Defining and enforcing quality standards for Hermes skills — from frontmatter validation and description rules through code verification, documentation completeness, and review checklists.

## When to Use

- Creating new skills that meet quality standards
- Reviewing existing skills for quality compliance
- Establishing team-wide skill authoring conventions
- Automated quality gates for skill contributions

## Quality Dimensions

```python
QUALITY_DIMENSIONS = {
    'frontmatter': 'Valid YAML, required fields, proper tags',
    'description': '≤60 chars, "Use when" prefix, ends with period',
    'content': 'Executable code, clear sections, practical examples',
    'verification': 'Checklist items are testable, not aspirational',
    'references': 'Related skills exist and are accurately referenced',
}
```

## Best Practices

```python
SKILL_BEST_PRACTICES = {
    'naming': 'Lowercase, hyphens (kebab-case), max 64 chars',
    'description': 'Start with "Use when", fit 60 chars, end with period',
    'frontmatter': 'Include tags (3-8), version, author, full metadata',
    'organization': 'Clear sections: When to Use → Core → Pitfalls → Checklist',
    'code': 'Executable patterns (not just description), runnable examples',
    'pitfalls': '5-6 specific, actionable failure modes with explanations',
    'checklist': '5-10 testable items (not "think about X", rather "X is configured")',
    'see_also': '3-5 related skills that complement this one',
}
```

## Verification Checklist

- [ ] Description starts with "Use when" and fits 60 chars
- [ ] Frontmatter has all required fields (name, description, version, author, tags)
- [ ] Skill has Common Pitfalls section with ≥4 actionable items
- [ ] Skill has Verification Checklist with testable items
- [ ] Code examples syntactically correct
- [ ] See Also references existing skills
- [ ] Tags are relevant (3-8 tags)
- [ ] Skill name is lowercase kebab-case
