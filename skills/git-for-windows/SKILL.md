---
name: git-for-windows
description: "Use when configuring Git on Windows."
category: software-development
tags: [git, windows, configuration, line-endings, authentication]
---
# Git for Windows

Configuring Git for optimal use on Windows.

## Installation

```powershell
# Via winget
winget install --id Git.Git -e

# Key install options:
# - Use Git from command line and 3rd-party tools
# - Use bundled OpenSSH
# - Checkout Windows-style, commit Unix-style line endings
# - Enable symbolic links (needs admin/Windows Developer Mode)
```

## Essential Configuration

```powershell
# Identity
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Line endings
git config --global core.autocrlf true       # Windows default (CRLF checkout, LF commit)
git config --global core.autocrlf input      # For cross-platform (LF checkout + commit)

# Long paths (Windows 10+)
git config --global core.longpaths true

# Case sensitivity (avoid issues)
git config --global core.ignorecase false

# Credential helper
git config --global credential.helper wincred     # Windows Credential Manager
git config --global credential.helper manager     # Git Credential Manager (newer)

# Default branch name
git config --global init.defaultBranch main
```

## SSH Authentication

```powershell
# Generate key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Add key to GitHub/GitLab/etc.
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# SSH config
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

## Git Credential Manager

```powershell
# GCM handles OAuth tokens for GitHub, Azure DevOps, etc.
# It's included with Git for Windows

# If not installed:
winget install --id GitCredentialManager.GitCredentialManager -e

# Configure
git config --global credential.helper manager-core
```

## Windows-Specific Tips

```powershell
# Enable symlinks (must re-clone repos)
git clone -c core.symlinks=true https://github.com/user/repo.git

# File mode (ignore permission differences on FAT/NTFS)
git config --global core.fileMode false

# Parallel operations (faster fetch/clone)
git config --global fetch.parallel 8
git config --global submodule.fetchJobs 8

# Use VS Code as default editor
git config --global core.editor "code --wait"
```

## WSL2 Interop

```powershell
# Avoid committing CRLF from Windows into WSL2 repos
# In WSL2:
git config core.autocrlf input

# Use the same git config across Windows and WSL2
# Set up symlink or copy:
cp /mnt/c/Users/limpi/.gitconfig ~/.gitconfig
```

## Pitfalls

- Line ending mismatches cause `git diff` noise -- set core.autocrlf consistently
- Long paths (>260 chars) need registry or git config fix
- Credential manager caches tokens -- use `git credential reject` to clear
- FileMode differences cause false modified flags -- set core.fileMode false
- Symlinks need Developer Mode enabled on Windows 10+
