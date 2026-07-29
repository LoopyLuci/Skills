---
name: git-stash-workflow
description: Temporarily save work-in-progress changes with git stash.
---

# Git Stash Workflow

**Trigger**: Use when needing to switch branches, pull updates, or start a different task without committing half-finished work.

## Basic Operations

```bash
# Stash current changes (tracked files only)
git stash

# Stash including untracked files
git stash --include-untracked      # -u
git stash --all                     # Everything (including ignored)

# Stash with a descriptive message
git stash push -m "WIP: refactoring auth middleware"

# List all stashes
git stash list
# stash@{0}: On feature/auth: WIP: refactoring auth middleware
# stash@{1}: On main: temp: debug logging

# Apply latest stash (keep in stash list)
git stash apply                     # Latest
git stash apply stash@{2}          # Specific stash

# Apply and remove from stash list
git stash pop                       # Latest
git stash pop stash@{1}            # Specific

# Drop a stash
git stash drop stash@{2}

# Clear all stashes
git stash clear
```

## Advanced Workflows

### 1. Stash Only Specific Files
```bash
git stash push -m "only frontend changes" -- src/frontend/
git stash push -m "config tweaks" -- '*.config.*'
```

### 2. Create a Branch from a Stash
```bash
git stash branch new-branch-name stash@{1}
# Creates branch at the original commit, pops the stash
```

### 3. Stash While Keeping Staged Files
```bash
git stash push --staged -m "keeping staged"  # Stashes only staged changes
git stash push --keep-index -m "unstaged only" # Stashes only unstaged changes
```

### 4. View Stash Contents
```bash
git stash show stash@{1}                     # Summary
git stash show -p stash@{1}                  # Full diff
git stash show -p stash@{1} -- src/file.ts   # Single file
```

### 5. Partial Stash (Interactive)
```bash
git stash push -p                             # Interactively select hunks to stash
# Similar to git add -p — answer y/n per hunk
```

## Recovery

```bash
# Find a dropped stash
git fsck --lost-found | grep commit       # Find dangling commits
git show <sha>                            # Inspect
git stash store <sha>                     # Re-add to stash list

# Apply stash to a different branch
git checkout target-branch
git stash pop                             # Works as long as there's no conflict
```

## Pitfalls
- **Dropped stashes are garbage-collected** after 30 days — recover with `git fsck`
- **Stash conflicts**: Handle like merge conflicts — edit, `git add`, then `git stash drop`
- **Stash doesn't track untracked by default**: Always use `-u` if you have new files
- **Large stashes are slow**: Consider creating a WIP commit instead for large changes
- **Stashes are local**: They don't push/pull — use a branch for sharing WIP

## Best Practices

```bash
# Always name your stashes
git stash push -m "descriptive-message"

# Before a risky operation
git stash push -m "backup-before-rebase-$(date +%Y%m%d)"

# Consider WIP commits instead (easier to find, survives pushes)
git commit -m "wip: current state"
# Later:
git reset HEAD~1              # Undo the commit, keep changes
```

## Verification
```bash
git stash list                             # See all stashes
git diff stash@{0}                         # Review contents before applying
git stash show -p stash@{0} | wc -l        # How many lines changed
```
