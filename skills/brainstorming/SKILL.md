---
name: brainstorming
description: Use when exploring ideas and design before writing code
tags: [design, planning, requirements, spec]
related_skills: [writing-plans, subagent-driven-development, executing-plans]
---

# Brainstorming Ideas Into Designs

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

## Core Principle

**Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.** This applies to EVERY project regardless of perceived simplicity.

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Process Checklist

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to their complexity, get user approval after each section
5. **Write design doc** — save to spec location and commit
6. **Spec self-review** — check for placeholders, contradictions, ambiguity, scope
7. **User reviews written spec** — ask user to review the spec file before proceeding
8. **Transition to implementation** — invoke writing-plans skill to create implementation plan

## Code Example: Design Doc Template

```markdown
# [Feature Name] Design

## Purpose
[One sentence]

## Approach
[Recommended approach with rationale]

## Architecture
[Components, data flow, interfaces]

## Implementation Plan
[Phased approach with dependencies]

## Open Questions
[Items to resolve during implementation]
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Skipping design for "simple" projects | Present a short design anyway — simple projects hide the most assumptions |
| Asking too many questions at once | Ask one question per message, break topics into multiple questions |
| Designing for hypothetical future needs | Apply YAGNI: only what's needed now |
| Proposing without understanding context | Always explore current codebase state and recent changes first |
| Moving to implementation without spec review | Always self-review the spec doc for gaps before user reviews it |

## Verification Checklist

- [ ] Explored current project context (files, docs, recent commits)
- [ ] Asked clarifications one at a time
- [ ] Proposals consider 2-3 approaches with trade-offs
- [ ] Design approved by user before any implementation
- [ ] Design doc written and committed
- [ ] Spec self-review completed (placeholders, contradictions, scope)
- [ ] User reviewed and approved the written spec
- [ ] Transitioned to writing-plans skill (not direct implementation)
