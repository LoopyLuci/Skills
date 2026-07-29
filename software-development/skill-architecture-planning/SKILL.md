---
name: skill-architecture-planning
description: "Use when planning multi-skill architectures for complex tasks."
category: software-development
tags: [skills, architecture, planning, meta, workflow]
---
# Skill Architecture Planning

Designing and planning multi-skill architectures for complex, multi-step tasks.

## When to Plan a Skill Architecture

- Task spans 3+ distinct domains (Docker + PS + WSL2)
- Task has branching logic (if X do Y, else do Z)
- Task requires sequential phases with dependencies
- Workflow will repeat with variations
- Different parts need different expertise levels

## Architecture Patterns

### Linear Pipeline
```
Skill A → Skill B → Skill C → Skill D
```
Use when: Steps are sequential, each depends on previous.

### Branching Tree
```
         ┌→ Skill B → Skill D
Skill A ─┤
         └→ Skill C → Skill E
```
Use when: Different conditions lead to different sub-flows.

### Hub-and-Spoke
```
         ┌→ Skill B
Skill A ─┼→ Skill C → Skill D
         └→ Skill E
```
Use when: One orchestrator delegates to multiple specialized skills.

### Layered
```
Skill A (orchestrator)
├── Skill B (planning)
├── Skill C (execution)
└── Skill D (verification)
```
Use when: Different abstraction levels need separation.

## Cross-Reference Convention

At the bottom of each skill, reference related skills:

```markdown
## See Also
- skill-architecture-planning  — planning multi-skill architectures
- skill-development-workflow   — building and testing skills
- skill-discovery             — discovering existing skills
```

## Pitfalls

- Over-engineering: don't split a 3-step task into 3 skills
- Missing links: always cross-reference related skills
- Stale chains: when updating one skill, check all chain consumers
- Circular deps: Skill A → B → A creates infinite loops
- Skill bloat: a skill covering too many domains should be split
