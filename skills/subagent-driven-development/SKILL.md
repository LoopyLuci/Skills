---
name: subagent-driven-development
description: Use when implementing plans by dispatching subagents per task
tags: [subagents, delegation, plan-execution, development]
related_skills: [dispatching-parallel-agents, writing-plans, executing-plans]
---

# Subagent-Driven Development

## Overview

Dispatch a fresh subagent per task from an implementation plan with review between tasks. This provides 50-100x context savings per task compared to inline execution.

## Core Principle

Each subagent starts fresh — no context from prior tasks, no accumulated conversation history. They focus solely on their assigned task and produce self-contained changes.

## Pattern

### 1. Load the Plan
Read the plan file. Identify tasks and their interfaces.

### 2. Prepare Task Context
For each task, prepare the exact context the subagent needs:
- The task's specific steps
- Interfaces it consumes and produces
- Files to create/modify
- Test expectations

### 3. Dispatch Subagent
Craft a focused prompt with complete context for one task.

### 4. Review Output
Two-stage review:
- **Stage 1:** Spec compliance — does output match the plan?
- **Stage 2:** Code quality — is the code clean, tested, and well-structured?

### 5. Iterate
Pass review feedback back to the subagent or fix inline and move to next task.

## Code Example: Task Dispatch

```
Subagent (general-purpose):
Implement Task 3 from the plan at docs/superpowers/plans/2024-01-feature.md:

Task 3: Add input validation

Files:
- Modify: src/validation.ts (add schema validation)
- Create: tests/validation.test.ts

Interfaces:
- Consumes: parseInput() from Task 2
- Produces: validateSchema(input, schema) -> {valid: boolean, errors: string[]}

Steps:
1. Write failing test for validateSchema
2. Run to verify failure
3. Implement validateSchema
4. Run to verify pass
5. Commit
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Too much context in one dispatch | Give only what the task needs — no full conversation history |
| No interface contract | Always specify consumes/produces interfaces clearly |
| Skipping review gate | Always review subagent output before moving to next task |
| Dispatches with vague scope | Each dispatch = one task from the plan |
| Not providing test expectations | Include expected test behavior in the prompt |

## Verification Checklist

- [ ] Plan loaded and tasks identified
- [ ] Each task dispatched with complete, focused context
- [ ] Consumes/produces interfaces specified
- [ ] Two-stage review performed per task
- [ ] All tests passing after integration
- [ ] No regressions introduced
