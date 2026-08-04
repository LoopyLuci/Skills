---
name: writing-skills
description: Use when creating, editing, or testing agent skills
tags: [skills, authoring, testing, documentation]
related_skills: [test-driven-development, skill-discovery, skill-factory-system]
---

# Writing Skills

## Overview

**Writing skills is Test-Driven Development applied to process documentation.** You write test cases (pressure scenarios), watch them fail (baseline behavior), write the skill, watch tests pass, and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| Test case | Pressure scenario with subagent |
| Production code | Skill document (SKILL.md) |
| Test fails (RED) | Agent violates rule without skill |
| Test passes (GREEN) | Agent complies with skill present |
| Refactor | Close loopholes while maintaining compliance |

## When to Create a Skill

- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)

**Don't create for:** One-off solutions, standard practices well-documented elsewhere, project-specific conventions.

## SKILL.md Structure

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## Core Pattern
Before/after code comparison

## Common Pitfalls
What goes wrong + fixes

## Verification Checklist
Actionable items to confirm the skill was followed
```

## Important Notes

**Description = When to Use, NOT What the Skill Does.** The description should only describe triggering conditions. Do NOT summarize the skill's process or workflow in the description.

**Name by what you DO:** Use active voice, verb-first (e.g., `creating-skills` not `skill-creation`).

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Writing skill before testing | Test first, watch it fail, then write the skill |
| Describing workflow in description | Only describe triggering conditions |
| One-off solutions made into skills | Skills must be broadly applicable |
| Skipping real-world testing | Test with real pressure scenarios |
| Vague verification steps | Make checklist items actionable and measurable |

## Verification Checklist

- [ ] Skill addresses a real, recurring problem
- [ ] Description is ≤60 chars, starts with "Use when"
- [ ] Skill tested with pressure scenario before writing
- [ ] Common Pitfalls section included
- [ ] Verification Checklist section included
- [ ] Code examples provided where applicable
- [ ] Related skills cross-referenced
