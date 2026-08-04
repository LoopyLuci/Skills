---
name: using-git-worktrees
description: Use when working with multiple git branches simultaneously
tags: [git, worktrees, branching, parallel-development]
related_skills: [git-worktrees-multiple-branches, finishing-a-development-branch]
---

# Using Git Worktrees

## Overview

Git worktrees allow you to check out multiple branches simultaneously in separate directories. This is essential for parallel development, plan execution in isolation, and context switching without stashing.

## Why Worktrees

- **Isolation:** Each worktree is a fully independent working directory
- **Parallel work:** Run tests on one branch while working on another
- **No stash needed:** Switch between contexts without stashing changes
- **Review readiness:** Prepare a branch for review while continuing development
- **Safe experimentation:** Try approaches in isolation without affecting main workspace

## Basic Commands

```bash
# Create a new worktree from current branch
git worktree add ../project-feature feature-branch

# Create a worktree from an existing branch
git worktree add ../project-feature existing-branch

# List all worktrees
git worktree list

# Remove a worktree (after merging or discarding)
git worktree remove ../project-feature

# Prune stale worktree references
git worktree prune
```

## Workflow for Plan Execution

```bash
# 1. Create a worktree for the feature
git worktree add ../project-feature -b feature/awesome-thing

# 2. Work in the worktree
cd ../project-feature
# ... implement changes ...

# 3. Push and create PR from the worktree
git push -u origin feature/awesome-thing

# 4. Clean up after merge
cd /path/to/main/repo
git branch -d feature/awesome-thing
git worktree remove ../project-feature
git worktree prune
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Forgetting to clean up worktrees | Remove after merge and run `git worktree prune` |
| Working in wrong worktree | Check `git worktree list` to confirm location |
| Branch name conflicts | Use descriptive names: `feature/description` |
| Stale references after deletion | Always run `git worktree prune` |

## Verification Checklist

- [ ] Worktree created in isolated directory
- [ ] Working in correct worktree (verify with `pwd` and `git branch`)
- [ ] All changes tested within the worktree
- [ ] Branch pushed and PR created (if applicable)
- [ ] Worktree removed after merge
- [ ] `git worktree prune` run for cleanup
