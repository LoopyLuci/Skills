---
name: git-workflow-optimization
description: "Git rebase bisect worktree and interactive squash patterns"
---

# Git Workflow Optimization

## Interactive Rebase
```bash
git rebase -i HEAD~3
git commit --fixup=<sha>
git rebase -i --autosquash HEAD~5
```

## Git Bisect
```bash
git bisect start && git bisect bad HEAD && git bisect good v2.0
```

## Worktrees
```bash
git worktree add ../project-feature feature-branch
git worktree list
```

## Quick Fixes
| Task | Command |
|------|---------|
| Undo last commit keep changes | `git reset --soft HEAD~1` |
| Fix commit message | `git commit --amend` |
| Add to last commit | `git add . && git commit --amend --no-edit` |
