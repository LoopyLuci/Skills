---

name: meta-skill-patterns
description: "Use when designing meta-skills for creation and management."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, meta, patterns, architecture, design]
    related_skills: [skill-development-workflow, skill-architecture-planning, skill-inventory-management, skill-testing-automation]

---

# Meta-Skill Patterns

Design patterns for creating meta-skills — skills whose domain is the skill system itself. Meta-skills manage, orchestrate, generate, or analyze other skills.

## When to Use

- Designing a skill that creates/modifies/deletes other skills
- Building a skill that orchestrates multiple skills as a pipeline
- Creating a skill that audits or analyzes the skill inventory
- Designing self-improving skill systems
- Building skill templates or code generators for skill creation

## Meta-Skill Archetypes

### 1. Orchestrator Meta-Skill

Orchestrates a multi-skill workflow without duplicating steps from referenced skills.

```
┌─────────────────────────────┐
│  orchestrator-meta-skill    │
│  (loads + sequences skills) │
├─────────────────────────────┤
│  Phase 1: Skill A           │
│  Phase 2: Skill B           │
│  Phase 3: Skill C + D       │
│  Phase 4: Verification      │
└─────────────────────────────┘
```

**Pattern**: The meta-skill's body references other skills by name and sequences them. Each phase says "Load and follow skill-X for this step" rather than duplicating content.

```markdown
## Procedure

### Phase 1: Inventory
Load and follow **skill-inventory-management** phase 1–2.

### Phase 2: Lint
Load and follow **skill-testing-automation** structural lint section.

### Phase 3: Consolidation
Apply **skill-inventory-management** merge patterns to identified duplicates.
```

### 2. Generator Meta-Skill

Generates new skills from templates or specifications.

```
┌─────────────────────────────────────┐
│  skill-generator-meta-skill         │
│  (produces SKILL.md from templates) │
├─────────────────────────────────────┤
│  1. Accept skill spec               │
│  2. Load template from references/  │
│  3. Fill template with spec         │
│  4. Validate output                 │
│  5. skill_manage(action='create')   │
└─────────────────────────────────────┘
```

**Pattern**: Uses `skill_manage` programmatically. Frequently paired with a templates/ directory.

```python
# Template-driven skill generator
NAME = "my-new-skill"
CATEGORY = "software-development"
DESCRIPTION = "Use when <trigger>. <one-line behavior>."
TAGS = ["tag1", "tag2"]

CONTENT = f'''---
name: {NAME}
description: "{DESCRIPTION}"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [{', '.join(f'\"{t}\"' for t in TAGS)}]
---

# {NAME.replace('-', ' ').title()}

## Overview

## When to Use

## Procedure

## Common Pitfalls

## See Also
'''

print(CONTENT)
```

### 3. Auditor Meta-Skill

Analyzes the skill inventory for quality, completeness, freshness. See **skill-testing-automation** and **skill-inventory-management** for the audit logic.

### 4. Curriculum Meta-Skill

Defines a learning path across skills — useful for onboarding or leveling up.

```markdown
## Level 1: Foundation
1. skill-development-workflow — basic skill creation
2. skill-discovery — finding and loading skills
3. skill-architecture-planning — planning skill structure

## Level 2: Authoring
4. hermes-agent-skill-authoring — SKILL.md format
5. meta-skill-patterns — meta-skill design
6. skill-testing-automation — validation

## Level 3: Advanced
7. skill-inventory-management — auditing
8. skill-architecture-planning — pipeline design
9. spike — experimental skill design
```

## Composition Patterns

### Sequential
```yaml
Phase 1: Run skill-a to generate inventory
Phase 2: Pass inventory to skill-b for analysis
Phase 3: Apply skill-c recommendations
```

### Conditional
```yaml
if skill_count > 80:
    load skill-inventory-management (audit mode)
else:
    load skill-testing-automation (quick check only)
```

### Parallel
```yaml
parallel:
  - skill-audit-1: inventory check
  - skill-audit-2: reference integrity
merge: combine reports from all three
```

## Self-Improvement Loop

```python
# After using a skill, record what worked
after_task:
  if user_says "that was helpful":
    increment_usage(skill_name)
  if user_says "that was wrong":
    log_improvement(skill_name)
```

## Meta-Skill as Cron Job

```bash
cronjob(action='create',
    name='monthly-skill-audit',
    schedule='0 9 1 * *',
    skills=['skill-inventory-management', 'skill-testing-automation'],
    prompt='Run a full audit of the skill inventory. Report findings and recommendations.')
```

## Common Pitfalls

1. **Infinite recursion** — meta-skills calling themselves or creating circular dependencies
2. **Over-abstraction** — a meta-skill for a one-step task adds more overhead than value
3. **Stale references** — meta-skills hardcoding other skill names that later get deleted
4. **Lost in meta** — spending more time managing skills than using them; keep it pragmatic
5. **Generator fragility** — template generators break when skill format changes
6. **Auditor fatigue** — running full audits too frequently produces noise; schedule quarterly

## Verification Checklist

- [ ] Meta-skill has a clear archetype (orchestrator/generator/auditor/curriculum)
- [ ] References to other skills use current names
- [ ] No circular skill dependencies
- [ ] Template files (if any) versioned alongside the meta-skill
- [ ] No duplication of content from referenced skills
- [ ] Verification step confirms the meta-skill's purpose was served

## See Also

- skill-inventory-management — auditing and pruning skills
- skill-testing-automation — automated skill validation
- skill-architecture-planning — multi-skill architecture design
- skill-development-workflow — basic skill creation workflow
