---
name: executing-plans
description: Use when executing written implementation plans step by step
tags: [plans, execution, implementation, development]
related_skills: [writing-plans, subagent-driven-development, finishing-a-development-branch]
---

# Executing Plans

## Overview

Load a plan, review critically, execute all tasks, report when complete.

## Step 1: Load and Review Plan

1. Ensure an isolated workspace (use using-git-worktrees or verify existing one)
2. Read the plan file
3. Review critically — identify any questions or concerns
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create todos for the plan items and proceed

## Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly
3. Run verifications as specified
4. Mark as completed

## Step 3: Complete Development

After all tasks complete and verified:
- Use finishing-a-development-branch skill to verify tests and present options

## When to Stop and Ask for Help

**STOP immediately when:** Hit a blocker, plan has critical gaps, instruction unclear, verification fails repeatedly. Ask for clarification rather than guessing.

## Code Example: Task Progress Tracking

```
- [x] Step 1: Create database schema
- [x] Step 2: Implement API endpoints
- [ ] Step 3: Add input validation
- [ ] Step 4: Write integration tests
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Skipping plan review | Always review critically before executing |
| Following vague steps blindly | Stop and ask for clarification |
| Guessing instead of asking | Ask for help when stuck — never guess |
| Modifying plan without approval | Raise concerns, let partner update the plan |
| Skipping verification steps | Run all specified verifications before marking done |

## Verification Checklist

- [ ] Plan reviewed critically before starting
- [ ] Todos created for all plan items
- [ ] Each task completed with verification
- [ ] No steps skipped or guessed at
- [ ] Blocker handling: asked for help when needed
- [ ] finishing-a-development-branch invoked at completion
- [ ] Tests pass, changes committed
