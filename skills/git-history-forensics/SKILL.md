---
name: git-history-forensics
description: Investigate git history — blame, log, reflog, and bisect.
---

# Git History Forensics

**Trigger**: Use when tracking down when a bug was introduced, who changed what, or recovering lost work.

## Git Blame — Find Who Changed What

```bash
# Basic blame — who last touched each line
git blame src/app.ts

# Show commit hash, author, date, and line content
git blame -s src/app.ts                    # Suppress author (raw output)
git blame -L 50,80 src/app.ts             # Specific line range
git blame -w src/app.ts                   # Ignore whitespace changes
git blame -C src/app.ts                   # Detect lines moved from other files
git blame -M src/app.ts                   # Detect lines moved within file

# Show commit details for a blamed line
git blame -L 75,+1 src/app.ts --porcelain | head -5
```

## Git Log — Navigate History

```bash
# Basic search
git log --oneline -20                                  # Last 20 commits
git log --author="jane" --oneline                      # By author
git log --grep="fix:" --oneline                        # By commit message
git log --since="2024-01-01" --until="2024-06-01"      # By date range
git log -- src/app.ts                                  # File history

# Detailed output
git log --oneline --graph --decorate --all             # Full history tree
git log --stat -1                                      # Files changed in commit
git log -p -3                                          # Full diff of last 3
git log --format="%h %an %ar %s"                       # Custom format

# Find when a function was added/removed
git log -S "functionName" --oneline -- source/         # Pickaxe search
git log -G "pattern" --oneline                         # Regex search (includes moves)
git log --diff-filter=D --oneline -- src/file.ts       # When a file was deleted
```

## Git Reflog — Recover Lost Work

```bash
# Show all HEAD movements (even after resets, rebases, amends)
git reflog
# a1b2c3f HEAD@{0}: commit: fix: handle null email
# d4e5f6a HEAD@{1}: rebase (finish): returning to refs/heads/main
# g7h8i9b HEAD@{2}: rebase (pick): feat: add user profile

# Recover from a bad reset
git reset --hard HEAD@{1}   # Go back to state before the reset

# Recover a dropped commit (after rebase)
git reflog | grep "feature-x"
git cherry-pick <sha>

# Time-based references
git show HEAD@{yesterday}
git show HEAD@{2.hours.ago}
git diff HEAD@{1.hour.ago} HEAD@{now}
```

## Git Bisect — Find the Bug

```bash
# Start bisect
git bisect start
git bisect bad                 # Current commit is broken
git bisect good v1.0.0         # v1.0.0 was working

# Git checks out the midpoint — test it, then mark:
git bisect good                # This commit works
git bisect bad                 # This commit is broken
# Repeat until git shows the first bad commit

# Automate with a script
git bisect start HEAD v1.0.0
git bisect run npm test        # Runs test at each step

# Visualize bisect progress
git bisect log
git bisect visualize

# Exit bisect
git bisect reset
```

## Advanced Investigation

### Find When a Specific String Was Introduced
```bash
git log -S "apiKey" --oneline --pretty="%h %an %ad %s" --date=short
git show <sha> | grep "apiKey"
```

### Find Merge Commit That Introduced a Bug
```bash
# --first-parent follows only the mainline (not branch details)
git log --first-parent --oneline
git bisect --first-parent  # Faster bisect by skipping branch internals
```

### Compare Two Branches
```bash
git log --oneline main..feature     # Commits in feature but not in main
git log --oneline feature..main     # Commits in main but not in feature
git diff main...feature             # Diff of feature vs merge-base with main
```

## Pitfalls
- **Rebase rewrites reflog references**: `HEAD@{N}` changes after rebase — use it immediately
- **blame -C is slow**: On large repos, omit `-C` unless you need cross-file detection
- **Bisect with long-running tests**: Use `git bisect skip` for commits that can't be tested
- **Reflog is local only**: It doesn't survive `git clone` — backup with `git bundle` if needed

## Verification
```bash
git reflog --oneline -5             # Recent history
git log --oneline --all -10         # Active branches
git shortlog -sn --no-merges        # Contributors by commit count
```
