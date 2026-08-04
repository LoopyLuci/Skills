---
name: batch-skill-creation
description: "Use when bulk creating Hermes skills efficiently."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skill-management, batch-creation, productivity, hermes-agent]
    related_skills: ['skill-authoring-workflows', 'skill-creator']
    tier: class-level
---

## Overview
Template-driven batch creation of Hermes skills using Python scripts that generate SKILL.md files directly. Produces 500-700 skills per run with built-in validation, deduplication, and description formatting.

## When to Use
- "Bulk skill creation for large catalog expansion"
- "When creating 50+ skills efficiently"
- "Template-driven skill generation at scale"
- "Automated skill creation with validation"

## Key Approaches

### 1. Set Up the Environment
```python
import os
SKILLS_DIR = "C:/Users/dubem/AppData/Local/hermes/skills"
existing = set(d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d)))
```

### 2. Define the Skill Factory Function
```python
def create_skill(name, desc, tags, related, overview):
    # Validate description: ≤60 chars, starts "Use when", ends with "."
    assert len(desc) <= 59, f"DESC TOO LONG: {name} ({len(desc)} chars)"
    assert desc.startswith("Use when"), f"Bad desc start: {name}"
    assert desc.endswith("."), f"Bad desc end: {name}"
    
    related_str = ', '.join([f"'{r}'" for r in related.split(',') if r]) if related else "general"
    # ... build body and markdown
```

### 3. Domain-Based Template Pattern
Define domains as tuples `(prefix, label, overview, tags)`, then generate 4-8 variations per domain:

```python
domains = [
    ("supply-chain", "Supply Chain", "Manage supply chains.", "supply-chain, logistics, procurement"),
    ("logistics", "Logistics", "Plan logistics ops.", "logistics, delivery, shipping"),
    # ... 80+ domain templates
]

for prefix, label, overview, tags in domains:
    for suffix, desc_suffix in [
        ("-fundamentals", f"for {label.lower()} fundamentals."),
        ("-implementation", f"for {label.lower()} implementation."),
        ("-optimization", f"for {label.lower()} optimization."),
        ("-management", f"for {label.lower()} management."),
    ]:
        name = prefix + suffix
        desc = "Use when " + desc_suffix
        if len(desc) > 59: desc = desc[:56] + "."
        # Create skill...
```

### 4. Deduplication Check
```python
if name in existing:
    continue  # Skip existing skills
```

### 5. Standard SKILL.md Template
Every generated skill follows the standard format:
- YAML frontmatter: name, description, version, author, license, platforms, metadata (tags, related_skills)
- `## Overview` — brief domain overview
- `## When to Use` — bullet-point trigger conditions
- `## Key Approaches` — numbered implementation steps
- `## Common Pitfalls` — numbered list of common mistakes
- `## Verification Checklist` — markdown task list

### 6. Validation Before Creation
```python
def desc_ok(d):
    return len(d) <= 59 and d.startswith("Use when") and d.endswith(".")
```

### 7. Run and Verify (PROVEN PATTERN: execute_code over subagents)
```python
# Use execute_code for direct execution - NO subagent delegation
# Subagents calling skill_manage per-skill cause HTTP 524 timeouts
from hermes_tools import execute_code
# ... or write batch script and run via terminal
# python batch_script.py
```

### 8. Template-Driven Expansion (4 SKILLS PER DOMAIN)
```python
suffixes = [
    ("-fundamentals", "for {label.lower()} fundamentals."),
    ("-implementation", "for {label.lower()} implementation."),
    ("-best-practices", "for {label.lower()} best practices."),
    ("-troubleshooting", "for {label.lower()} troubleshooting."),
]

for prefix, label, overview, tags in domains:
    for suffix, desc_suffix in suffixes:
        name = prefix + suffix
        desc = "Use when applying " + desc_suffix.format(label=label)
        if len(desc) > 59: desc = desc[:56] + "."
        make_skill(name, desc, tags, overview)
```

## Common Pitfalls
1. **Description exceeds 60 chars** — Always truncate to `desc[:56] + "."` and validate with `len(desc) <= 59`
2. **Missing 'Use when' prefix** — Descriptions must start with "Use when" exactly
3. **Missing period at end** — All descriptions must end with "."
4. **Duplicate skill names** — Always check `existing` set before creating
5. **Script too large for write_file** — Use `execute_code` to write large Python scripts to disk, or split into smaller batch scripts
6. **Subagent timeout for bulk creation** — Subagents that call `skill_manage` per-skill (one API call per skill) cause **HTTP 524 timeouts** at 120s proxy read timeout or 1200s hard ceiling. For 50-100+ skills, delegation always fails. **Always use direct terminal `python batch_script.py` execution instead.**
7. **Variable scope errors in retry scripts** — When patching batch scripts, ensure counter variables (`created`, `failed`) are initialized before any loops that reference them
8. **F-string escaping in Python** — When embedding the SKILL.md template, be careful with curly braces in YAML/metadata sections
9. **Not cleaning up scripts** — Always remove temporary batch scripts after the session

## Reference Files
- `references/template_batch_creator.py` — Reusable starter script; edit the DOMAINS list and run
- `scripts/verify_skills.py` — Post-creation verification: checks YAML, sections, description length Produces 4 variations per domain with automatic validation.

## Verification Checklist
- [x] Script validates descriptions before creation
- [x] `desc_ok()` function checks length, prefix, and period
- [ ] `existing` set prevents duplicate creation
- [ ] Each skill has `## Overview`, `## When to Use`, `## Key Approaches`
- [ ] Each skill has `## Common Pitfalls` and `## Verification Checklist`
- [ ] Total SKILL.md count matches expected number
- [ ] Temporary batch scripts cleaned up after use
- [ ] All generated descriptions are ≤60 characters