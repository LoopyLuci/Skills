---
name: git-merge-conflict-resolution
description: Systematically resolve merge and rebase conflicts.
---

# Git Merge Conflict Resolution

**Trigger**: Use when resolving a merge conflict during `git merge`, `git rebase`, `git pull`, or `git cherry-pick`.

## Understanding Conflict Markers

```
<<<<<<< HEAD
code from your current branch
=======
code from the incoming branch
>>>>>>> feature-branch
```

- `HEAD` = your current branch (what you had)
- `=======` = divider
- `incoming` = the branch you're merging in

## Resolution Workflow

### 1. Identify Conflicting Files

```bash
# After a failed merge/rebase:
git status                            # Shows conflicting files (both modified)
git diff                              # Shows conflict markers
git diff --name-only --diff-filter=U  # Unmerged files only
```

### 2. Choose Your Resolution Strategy

**A) Manual (best for understanding):**
```bash
# Edit files to resolve conflicts, remove markers, keep desired code
git add <file>
git commit                            # For merge
git rebase --continue                 # For rebase
```

**B) Accept one side entirely:**
```bash
# Keep your version (HEAD)
git checkout --ours -- <file>
git add <file>

# Keep their version (incoming)
git checkout --theirs -- <file>
git add <file>
```

**C) Interactive merge tool:**
```bash
git mergetool                         # Opens configured tool (vimdiff, VS Code, etc.)
# Common tools:  meld, kdiff3, vimdiff, code --wait
```

### 3. Complete the Operation

| Operation | Continue command | Abort command |
|-----------|-----------------|---------------|
| Merge | `git commit` | `git merge --abort` |
| Rebase | `git rebase --continue` | `git rebase --abort` |
| Cherry-pick | `git cherry-pick --continue` | `git cherry-pick --abort` |
| Pull | `git commit` | `git merge --abort` |

## Prevention

```bash
# Pull with rebase to avoid merge bubbles
git config --global pull.rebase true

# Before merging, review the diff
git merge --no-commit --no-ff feature  # Stage without committing
git diff --cached                       # Review what will land
git merge --abort                       # Or proceed with git commit

# Use rerere (reuse recorded resolution)
git config --global rerere.enabled true
```

## Complex Scenarios

**Binary file conflicts**: Cannot be merged — choose one side with `--ours`/`--theirs`

**Multiple conflicts in rebase**: Each commit in the rebase can have its own conflicts
```bash
git rebase main
# Fix conflicts, git add, then:
git rebase --continue
# Repeat until all commits are rebased
# Or: git rebase --skip (skip current commit)
# Or: git rebase --abort (undo everything)
```

**Conflict in deleted/modified file**: `git add/rm <file>` then continue

## Pitfalls
- **Accidental markers**: Search for leftover `<<<<<<<`, `=======`, `>>>>>>>` in final diff
- **Whitespace conflicts**: `git merge -Xignore-space-change` for formatting-only diffs
- **Merge --abort loses uncommitted work**: Stash before risky merges
- **Rebase overwrites commit history**: Only rebase local/private branches

## Verification
```bash
git log --oneline --graph --all                # Check history shape
git diff main...HEAD                           # Verify merge introduced correct changes
grep -rn "^<<<<<<< \|^=======$\|^>>>>>>> " .   # No leftover markers
```
