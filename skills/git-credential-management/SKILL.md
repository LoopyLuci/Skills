---
name: git-credential-management
description: Manage git credentials — tokens, SSH keys, and helpers.
---

# Git Credential Management

**Trigger**: Use when setting up GitHub auth, rotating tokens, configuring SSH keys, or troubleshooting authentication failures.

## Authentication Methods

| Method | Best for | Persistence |
|--------|----------|-------------|
| **HTTPS + PAT** | CLI, CI/CD, automation | Credential helper caches token |
| **SSH key** | Long-term dev setup | Key on disk, no reauth |
| **GitHub CLI (`gh`)** | Interactive use | OAuth token in system keychain |
| **OAuth device flow** | Limited input environments | Short-lived session |

## HTTPS + Personal Access Tokens

### Create a PAT (GitHub)
```bash
# Fine-grained (recommended)
gh auth token --scopes "repo,workflow,write:packages"
# Or create at: https://github.com/settings/tokens
```

### Configure Credential Helper

```bash
# macOS — Keychain (persists across reboots)
git config --global credential.helper osxkeychain

# Windows — Git Credential Manager (GCM)
git config --global credential.helper manager-core

# Linux — libsecret (GNOME Keyring)
git config --global credential.helper /usr/lib/git-core/git-credential-libsecret

# Linux — cache (in-memory, configurable timeout)
git config --global credential.helper "cache --timeout=86400"  # 24 hours

# Linux — store (plaintext, persistent — use with caution)
git config --global credential.helper store
```

### Use Token in Clone URL
```bash
git clone https://<token>@github.com/owner/repo.git
# Or with gh:
gh repo clone owner/repo
```

## SSH Keys

### Generate and Add
```bash
# Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "your@email.com" -f ~/.ssh/id_ed25519_github

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github

# Add to GitHub
cat ~/.ssh/id_ed25519_github.pub
# → https://github.com/settings/keys → New SSH Key
```

### SSH Config for Multiple Accounts
```bash
# ~/.ssh/config
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github

Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work

# Clone with work identity
git clone git@github-work:org/project.git
```

### Test Connection
```bash
ssh -T git@github.com
# Hi username! You've successfully authenticated...
```

## GitHub CLI Auth

```bash
# Login (browser-based OAuth)
gh auth login

# Login with token (non-interactive)
gh auth login --with-token < ~/github-token.txt

# Check auth status
gh auth status

# Get current token
gh auth token
```

## Multi-Account Setup

```bash
# Per-repo identity
git config user.name "Work User"
git config user.email "work@company.com"

# Per-repo credential override
# ~/.gitconfig
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```

## Token Rotation

```bash
# Rotate stored credentials
echo "url=https://github.com" | git credential reject   # Remove old
echo "url=https://<token>@github.com" | git credential approve  # Store new

# Or clear entirely
git credential reject < /dev/null
```

## Pitfalls
- **PAT expiry**: Set reminder for token expiration — GitHub PATs can have expiry dates
- **SSH key passphrase**: Use `ssh-add --apple-use-keychain` (macOS) or `ssh-add ~/.ssh/key` to avoid re-entering
- **GCM on Windows**: If stuck in auth loop, clear from Windows Credential Manager
- **GitHub fine-grained PATs**: Must be scoped to specific repos — won't work for org-wide actions without `repo` scope

## Verification
```bash
gh auth status                    # Check GitHub CLI auth
ssh -T git@github.com             # Check SSH auth
git ls-remote origin HEAD         # Check read access to repo
```
