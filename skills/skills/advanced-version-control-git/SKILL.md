---
name: advanced-version-control-git
description: "Use when using advanced git workflows and recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, version-control, advanced, branching, rebase, bisect, reflog]
    related_skills: [git-for-windows, github-pr-workflow, github-code-review, systematic-debugging]
---

# Advanced Git — Workflows, Recovery, and Automation

Advanced git workflows, history manipulation, debugging with bisect, recovery from disasters, and automation patterns.

## When to Use

- Recovering from mistaken commits, rebases, or deletions
- Using git bisect to find the commit that introduced a bug
- Implementing advanced branching strategies (GitFlow, trunk-based)
- Automating git operations in scripts and CI
- Understanding git internals to debug weird repository states

## Git Object Model (Mental Model)

```
Commits → Trees → Blobs (content-addressed, immutable)
References → branches, tags, HEAD (pointers to commits)
Reflog → local history of where HEAD has been (safety net)
```

## Recovery Patterns

### Undo Almost Anything

```bash
# Undo a commit but keep changes staged
git reset --soft HEAD~1

# Undo a commit and unstage changes (keep working dir)
git reset --mixed HEAD~1  # (default)

# Undo a commit AND discard all changes
git reset --hard HEAD~1   # DANGER: destroys uncommitted work

# Undo a commit that was already pushed (create inverse commit)
git revert HEAD  # Safe for shared branches

# Recover a commit that was "lost" via reset
git reflog  # Find the commit hash
git cherry-pick <hash>  # Recover it
```

### Recover Deleted Branch

```bash
# Find the commit hash from reflog
git reflog | grep "branch: deleted"
# Checkout the last commit from that branch
git checkout -b recovered-branch <hash>
```

### Fix the Last Commit Message

```bash
git commit --amend -m "New message"
# For pushed commits: git push --force-with-lease
```

## Git Bisect (Find the Bug)

```bash
# Automated binary search through history
git bisect start
git bisect bad        # Current commit is broken
git bisect good v1.0  # Tag v1.0 was working

# Git checks out middle commit. Test it.
# If broken: git bisect bad
# If working: git bisect good
# Repeat until the first bad commit is found

# Automated bisect (supply a test script)
git bisect run pytest tests/test_bug.py
# Git runs the script on each commit automatically

git bisect reset  # Return to original state
```

## Interactive Rebase

```bash
# Squash, reorder, edit, or drop commits
git rebase -i HEAD~5

# Commands inside the editor:
# pick = use commit
# reword = use commit but edit message
# edit = use commit but stop to amend
# squash = combine with previous commit
# fixup = like squash but discard message
# drop = remove commit
# exec = run shell command

# Auto-squash fixup commits
git commit --fixup=<sha>     # Mark as fixup
git rebase -i --autosquash   # Auto-arrange
```

## Branching Strategies

### Trunk-Based Development

```bash
# Main principles:
# - Short-lived feature branches (hours to days)
# - Feature flags for incomplete work
# - Continuous integration to main
git checkout -b feature/xyz
# ...work...
git commit -m "feat: add xyz"
git push origin feature/xyz
# PR → merge to main quickly
```

### GitFlow

```bash
# Branches: main, develop, feature/*, release/*, hotfix/*
git flow init
git flow feature start my-feature
git flow feature finish my-feature  # Merges to develop
git flow release start 1.2.0
git flow release finish 1.2.0  # Merges to main + develop
```

## Git Automation

```python
import subprocess
import json

class GitAutomation:
    """Automate git operations from scripts."""
    
    @staticmethod
    def run(cmd):
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            raise RuntimeError(f"Git error: {result.stderr}")
        return result.stdout.strip()
    
    @classmethod
    def get_current_branch(cls):
        return cls.run("git rev-parse --abbrev-ref HEAD")
    
    @classmethod
    def get_changed_files(cls, base_branch='main'):
        """Get files changed in current branch vs base."""
        output = cls.run(f"git diff --name-only {base_branch}...HEAD")
        return output.split('\n') if output else []
    
    @classmethod
    def create_release_tag(cls, version):
        """Create and push an annotated tag."""
        cls.run(f"git tag -a v{version} -m 'Release v{version}'")
        cls.run("git push --tags")
    
    @classmethod
    def get_commit_history(cls, count=10):
        """Get recent commit history as JSON."""
        output = cls.run(
            f'git log --format=\'{{"hash":"%H","author":"%an","message":"%s"}}\' -{count}'
        )
        return [json.loads(line) for line in output.split('\n') if line]
```

## Common Pitfalls

1. **`--force` vs `--force-with-lease`** — force push can overwrite others' work; always use `--force-with-lease`
2. **Rebasing shared branches** — rebasing a branch others have based work on causes duplicates
3. **Large files in git** — git LFS or it gets slow; never commit binaries >10MB
4. **Merge commits in rebase workflow** — mixing merge and rebase creates confusing history
5. **Detached HEAD panic** — HEAD detached is fine; create a branch to save work
6. **Lost reflog** — reflog expires (default 90 days); important recoveries should be tagged

## Verification Checklist

- [ ] Branching strategy documented and followed by the team
- [ ] `git reflog` understood as the primary recovery tool
- [ ] `git bisect` can systematically find bug-introducing commits
- [ ] Interactive rebase used for cleanup before merging
- [ ] Force pushes use `--force-with-lease` (never bare `--force`)
- [ ] CI runs on every push (no long-lived unmerged branches)

## See Also

- git-for-windows — git setup on Windows
- github-pr-workflow — PR lifecycle
- github-code-review — reviewing diffs
- systematic-debugging — using bisect for debugging
