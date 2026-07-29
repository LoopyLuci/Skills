---
name: git-config-essentials
description: Configure git globally — aliases, editors, and line endings.
---

# Git Config Essentials

**Trigger**: Use when setting up git on a new machine, configuring aliases, or optimizing git behavior.

## Configuration Levels

| Level | Scope | File |
|-------|-------|------|
| `--system` | All users on machine | `<git-install>/etc/gitconfig` |
| `--global` | Your user account | `~/.gitconfig` or `~/.config/git/config` |
| `--local` | Current repository | `.git/config` |

## Essential Global Settings

```bash
# Identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Default branch name
git config --global init.defaultBranch main

# Editor
git config --global core.editor "code --wait"        # VS Code
git config --global core.editor "nvim"               # Neovim
git config --global core.editor "nano"               # Nano

# Line endings
git config --global core.autocrlf input              # macOS/Linux
git config --global core.autocrlf true               # Windows
git config --global core.safecrlf warn

# Pull behavior — rebase instead of merge
git config --global pull.rebase true
git config --global rebase.autoStash true

# Color output
git config --global color.ui auto

# Diff and merge
git config --global diff.algorithm histogram
git config --global merge.conflictStyle zdiff3       # Better conflict markers
```

## Time-Saving Aliases

```bash
# Status
git config --global alias.st "status -sb"
git config --global alias.ll "log --oneline --graph --decorate --all"
git config --global alias.tree "log --graph --oneline --all --format='%C(auto)%h %C(bold)%d %C(cyan)%an %Cgreen%ar%Creset %s'"

# Committing
git config --global alias.ci "commit"
git config --global alias.amend "commit --amend --no-edit"
git config --global alias.undo "reset --soft HEAD~1"

# Branching
git config --global alias.br "branch"
git config --global alias.co "checkout"
git config --global alias.cb "checkout -b"
git config --global alias.cleanup "branch --merged | grep -v '\*\|main\|master\|develop' | xargs -r git branch -d"

# Diff
git config --global alias.df "diff"
git config --global alias.dfc "diff --cached"

# Log
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.contributors "shortlog -sn --no-merges"

# Housekeeping
git config --global alias.prune "remote prune origin"
git config --global alias.sweep "!git branch --merged | grep -v 'main\|master\|develop' | xargs git branch -d"
```

## Repository-Specific Settings

```bash
# Per-repo identity (for work vs personal)
git config user.name "Work Name"
git config user.email "work@company.com"

# Large repo tuning
git config core.preloadindex true
git config core.fscache true          # Windows only
git config core.untrackedcache true
```

## Useful Features to Enable

```bash
# Reuse recorded resolution (remembers conflict resolutions)
git config --global rerere.enabled true

# Better merge defaults
git config --global merge.tool vimdiff
git config --global mergetool.prompt false

# Safe force-push
git config --global alias.force-push "push --force-with-lease"

# Auto-correct typos (10ms delay)
git config --global help.autocorrect 10
```

## View Current Config

```bash
git config --list                       # All settings
git config --list --show-origin         # With file location
git config --global --list              # User-level only
git config user.name                    # Single value
```

## Pitfalls
- **CRLF vs LF**: Mismatched line endings cause noise diffs — set `autocrlf` per platform
- **Global vs local identity**: Use work email in `--local`, not `--global`, when you have multiple accounts
- **Alias conflicts**: Don't alias to existing git commands (e.g., `git push` as alias fails)
- **Editor path on Windows**: Use forward slashes or `code --wait` — paths with spaces need quotes

## Verification
```bash
git config --list --show-origin | grep -E "user\.(name|email)|core\.(editor|autocrlf)"
```
