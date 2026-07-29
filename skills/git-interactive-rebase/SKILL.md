---
name: git-interactive-rebase
description: Squash, reorder, and clean up commits interactively.
---

# Git Interactive Rebase

**Trigger**: Use when cleaning up commit history before merging, squashing fixup commits, or reordering changes.

## Core Command

```bash
git rebase -i HEAD~N    # Rebase last N commits
git rebase -i <commit>  # Rebase all commits after <commit> (exclusive)
```

## Interactive Rebase Actions

| Action | Short | Effect |
|--------|-------|--------|
| `pick` | `p` | Use commit as-is |
| `reword` | `r` | Edit commit message only |
| `edit` | `e` | Stop to amend content and/or message |
| `squash` | `s` | Combine with previous commit, merge messages |
| `fixup` | `f` | Combine with previous commit, discard its message |
| `drop` | `d` | Remove commit entirely |
| `break` | `b` | Stop here (useful before `exec`) |
| `exec` | `x` | Run shell command |

## Common Workflows

### 1. Squash WIP Commits Before PR
```bash
# Before: a1b2c3 WIP, d4e5f6 fix typo, g7h8i9 Oops
# Want: one clean commit
git rebase -i HEAD~3
# Change to:
#   pick g7h8i9
#   squash d4e5f6
#   squash a1b2c3
# After: one squashed commit
```

### 2. Edit a Specific Old Commit
```bash
git rebase -i HEAD~10
# Change 'pick' to 'edit' on the target commit
# Git stops at that commit — make your changes:
git add -A
git commit --amend --no-edit
git rebase --continue
```

### 3. Reorder Commits Logically
```bash
git rebase -i HEAD~5
# Reorder lines in the editor — oldest at top, newest at bottom
# Move lines up/down to reorder commits
```

### 4. Split a Commit Into Multiple
```bash
git rebase -i HEAD~N
# Mark the commit to split as 'edit'
# When stopped:
git reset HEAD^                          # Unstage everything
git add file1.py && git commit -m "feat: part one"
git add file2.py && git commit -m "feat: part two"
git rebase --continue
```

### 5. Fixup (Squash Without Editing Message)
```bash
git commit --fixup=<target-sha>          # Creates "fixup! original message" commit
git rebase -i --autosquash HEAD~N        # Auto-arranges fixup commits
```

## Safety

```bash
# Always create a backup branch first
git branch backup/rebase-YYYY-MM-DD

# Or use the reflog to recover
git rebase --abort                       # Cancel the rebase entirely
git reflog                               # Find pre-rebase state
git reset --hard HEAD@{N}               # Restore to before rebase
```

## Pitfalls
- **Never rebase pushed commits** others depend on — force-push only your own branches
- **Squashing loses individual commit metadata** — good for cleanup, bad for attribution
- **Long rebases generate many conflicts** — prefer `git merge --squash` for large squashes
- **Autosquash needs exact matching** — `--fixup` creates `fixup!` prefix, `--squash` creates `squash!`

## Verification
```bash
git log --oneline -5                     # Check resulting history
git diff main...HEAD                     # Verify net diff is unchanged after squash
```
