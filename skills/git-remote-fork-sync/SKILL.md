---
name: git-remote-fork-sync
description: Sync forks, manage remotes, and keep branches up to date.
---

# Git Remote & Fork Sync

**Trigger**: Use when setting up remotes, synchronizing a fork with its upstream, or managing multiple remote repositories.

## Understanding Remotes

```bash
# List remotes
git remote -v
# origin  https://github.com/you/repo.git (fetch)
# origin  https://github.com/you/repo.git (push)
```

## Fork Sync Workflow

### 1. Add Upstream Remote
```bash
# Clone your fork first
git clone https://github.com/YOU/repo.git
cd repo

# Add the original repo as upstream
git remote add upstream https://github.com/ORIGINAL/repo.git
git remote -v
# origin    https://github.com/YOU/repo.git (fetch/push)
# upstream  https://github.com/ORIGINAL/repo.git (fetch)
```

### 2. Sync Fork with Upstream
```bash
# Fetch all upstream branches
git fetch upstream

# Sync your main branch
git checkout main
git rebase upstream/main            # Clean history (recommended)
# OR
git merge upstream/main             # Merge (creates merge commit)

# Push updates to your fork
git push origin main

# Sync a feature branch
git checkout feature-branch
git rebase upstream/main
git push --force-with-lease origin feature-branch
```

### 3. Automate with gh CLI
```bash
# GitHub CLI can update forks
gh repo sync owner/repo --branch main
```

## Remote Management

### Adding and Removing Remotes
```bash
# Add a remote
git remote add coworker https://github.com/coworker/repo.git

# Rename
git remote rename origin upstream

# Remove
git remote remove coworker

# Change URL
git remote set-url origin https://github.com/new-owner/repo.git
git remote set-url --push origin git@github.com:new-owner/repo.git
```

### Fetching from Specific Remotes
```bash
git fetch upstream               # Fetch all upstream branches
git fetch upstream main          # Fetch upstream/main only
git fetch --all                  # All remotes
git fetch --prune                # Remove deleted remote branches
```

## Multiple Orgs / Accounts

```bash
# Work repo with different identity
git clone https://github.com/company/project.git
cd project
git config user.name "Work Name"
git config user.email "work@company.com"

# Or use SSH config for different keys (see git-credential-management)
```

## Common Remote Patterns

| Pattern | Command |
|---------|---------|
| Add upstream | `git remote add upstream <url>` |
| Change origin URL | `git remote set-url origin <new-url>` |
| Add coworker's fork | `git remote add <name> <fork-url>` |
| Prune stale branches | `git fetch --prune` |
| List remote branches | `git branch -r` |
| Track branch from remote | `git switch -c <local> <remote>/<branch>` |

## Pitfalls
- **Rebase vs merge**: Rebasing a fork makes clean history but requires force-push — coordinate with collaborators
- **Multiple upstreams**: Add each as a named remote — git has no concept of "primary upstream"
- **SSH vs HTTPS URLs**: If you cloned with HTTPS, push with token; if SSH, push with key — don't mix
- **Fork freshness**: Always sync before creating a PR — CI checks against latest upstream

## Verification
```bash
git remote -v                                      # All remotes
git log --oneline main..upstream/main              # Commits behind upstream
git branch -r                                      # All remote branches
git fetch --dry-run                                # Preview fetch without downloading
```
