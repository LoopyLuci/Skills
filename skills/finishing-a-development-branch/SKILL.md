---
name: finishing-a-development-branch
description: Use when completing dev work: verify tests and present merge options
tags: [git, branch, merge, testing, pull-request]
related_skills: [executing-plans, receiving-code-review, verification-before-completion]
---

# Finishing a Development Branch

## Overview

After all tasks in a plan are complete, verify everything works and present merge options to the user.

## Required Steps

### Step 1: Run All Tests

Run the full test suite. If tests fail, fix them. Do not skip this step.

### Step 2: Check for Issues

- Run linters and type checkers
- Review for any TODO/FIXME comments added during development
- Ensure all new code has appropriate tests

### Step 3: Present Options

Present a clear choice to the user with specific recommendations:

```
Option 1: Merge worktree branch into main
- All tests passing
- Ready for code review
- Run: git merge ...

Option 2: Create PR for review
- Branch is pushed to remote
- Open PR with description of changes
- Request specific reviewers

Option 3: Request code review
- Invite review of specific components
- Address feedback before merging
```

### Step 4: Execute User's Choice

Once user selects an option, execute it.

## Code Example: Post-Completion Summary

```
✓ All 47 tests passing
✓ ESLint clean (0 warnings)
✓ TypeScript strict check passed
✓ No TODO/FIXME comments remain
✓ Documentation updated

Options:
1. Merge to main (fast-forward)
2. Open PR for team review
3. Request my code review
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Skipping test run | Always run full suite before declaring done |
| Ignoring lint/type errors | Fix all warnings — they signal real issues |
| Merging without user approval | Always present options and wait for choice |
| Leaving TODO comments | Remove or address all TODOs before completion |

## Verification Checklist

- [ ] Full test suite passes
- [ ] Linting/type-checking clean
- [ ] No TODO/FIXME left behind
- [ ] All new code has tests
- [ ] Options presented to user
- [ ] User's choice executed
