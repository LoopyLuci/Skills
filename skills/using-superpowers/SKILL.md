---
name: using-superpowers
description: Use when orchestrating Obra superpowers skills for agentic workflows
tags: [superpowers, obra, agent-orchestration, skills]
related_skills: [dispatching-parallel-agents, subagent-driven-development, writing-plans]
---

# Using Superpowers

## Overview

Superpowers is a framework of agentic development skills that work together. This skill explains how to orchestrate them effectively.

## Skill Orchestration Flow

The superpowers follow a specific workflow:

```
Brainstorming → Writing Plans → Subagent-Driven Development / Executing Plans → Finishing Branch
```

### 1. Brainstorming
When starting creative work, use the brainstorming skill to explore requirements, propose approaches, and get design approval before any implementation.

### 2. Writing Plans
After design approval, use writing-plans to break the design into bite-sized tasks with interfaces and test expectations.

### 3. Execution
Two options:
- **Subagent-Driven Development (recommended):** Dispatch a fresh subagent per task with review gates
- **Executing Plans:** Execute tasks inline in the current session

### 4. Finishing Branch
After all tasks complete, use finishing-a-development-branch to verify tests and present merge options.

## When to Use Each Skill

| Situation | Skill |
|-----------|-------|
| New feature or design work | brainstorming |
| After design approval | writing-plans |
| Implementing with context savings | subagent-driven-development |
| Inline implementation | executing-plans |
| Completing and merging | finishing-a-development-branch |
| Parallel independent work | dispatching-parallel-agents |
| After receiving reviewer feedback | receiving-code-review |
| Final quality check | verification-before-completion |

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Skipping design phase | Always brainstorm before implementing |
| Using wrong execution mode | Prefer subagent-driven-development for complex tasks |
| Missing verification step | Always run verification-before-completion before finishing |
| Not committing work in progress | Commit frequently with conventional commit messages |
| Ignoring the skill chain | Follow the flow: brainstorm → plan → execute → finish |

## Verification Checklist

- [ ] Design approved before starting implementation
- [ ] Plan written before execution
- [ ] Appropriate execution mode chosen
- [ ] Tests pass before branch completion
- [ ] Merge options presented to user
