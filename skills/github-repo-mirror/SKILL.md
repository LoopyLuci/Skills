---
name: github-repo-mirror
description: Mirror repositories between GitHub, GitLab, and other hosts.
---

# GitHub Repo Mirroring

**Trigger**: Use when setting up repository mirrors, migrating repos between platforms, or keeping forks in sync.

## Mirror Types

| Type | Direction | Sync method |
|------|-----------|-------------|
| **Push mirror** | Local → remote | `git push --mirror` |
| **Pull mirror** | Remote → local | `git clone --mirror` |
| **Bi-directional** | Both ways | CI cron + webhooks |

## One-Time Mirror

### Clone with Full History
```bash
# Bare clone (all branches, all tags, no working tree)
git clone --mirror https://github.com/owner/repo.git
cd repo.git

# Push to new remote
git remote set-url origin https://github.com/new-owner/repo.git
git push --mirror
```

### Or Single Command
```bash
# From GitHub → GitHub
gh repo clone owner/repo -- --mirror
cd repo.git
gh repo create new-owner/repo --public --push --source=.

# From GitHub → GitLab
git clone --mirror https://github.com/owner/repo.git
cd repo.git
git remote set-url origin https://gitlab.com/new-owner/repo.git
git push --mirror

# From GitLab → GitHub
git clone --mirror https://gitlab.com/owner/repo.git
cd repo.git
git remote set-url origin https://github.com/new-owner/repo.git
git push --mirror
```

## Automated Mirror (GitHub Actions)

### GitHub → GitLab
```yaml
name: Mirror to GitLab
on:
  push:
    branches: ['*']
    tags: ['*']
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: yesolutions/mirror-action@v0.7
        with:
          REMOTE: "https://gitlab.com/owner/repo.git"
          GIT_USERNAME: ${{ secrets.GITLAB_USER }}
          GIT_PASSWORD: ${{ secrets.GITLAB_TOKEN }}
```

### GitHub → GitHub (Org/User transfer)
```yaml
name: Mirror to Secondary
on:
  schedule:
    - cron: '0 */6 * * *'     # Every 6 hours
  workflow_dispatch:            # Manual trigger
jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          git remote add mirror https://x-access-token:${{ secrets.MIRROR_TOKEN }}@github.com/org/mirror-repo.git
          git push --mirror mirror
```

## GitHub → GHCR Backup (Archival)

```bash
# Archive as a bundle (portable single file)
git bundle create repo-backup-$(date +%Y%m%d).bundle --all
git bundle verify repo-backup-*.bundle
```

## Multi-Platform Mirroring

```bash
# Set up multiple push targets
git remote add github https://github.com/owner/repo.git
git remote add gitlab https://gitlab.com/owner/repo.git
git remote add bitbucket https://bitbucket.org/owner/repo.git

# Push to all
git push --all github
git push --all gitlab
git push --all bitbucket
```

## Using gh CLI for Transfers

```bash
# Transfer repo to another user/org
gh api repos/:owner/:repo/transfer \
  --method POST \
  --field new_owner=new-org

# Rename repo
gh repo edit --name new-name

# Transfer with issues and PRs
# NOTE: gh transfer API doesn't move issues — use third-party tools
```

## Pitfalls
- **Mirror ≠ sync**: Mirror copies git data; issues, PRs, wikis, and releases must be migrated separately
- **Large repos**: `--mirror` clones everything — for repos >1GB use `--filter=blob:none` for partial
- **CI secrets**: Mirror jobs need tokens with `repo` scope in the destination
- **Deleted branches**: `--mirror` push deletes branches not in the source — use `--all` instead for additive sync
- **GitHub Actions artifacts**: Not included in mirror — use `gh run download` separately

## Verification
```bash
# Verify mirror completeness
git ls-remote origin | wc -l             # Source refs
git ls-remote mirror | wc -l             # Mirror refs — should match

# Check branches and tags matching
diff <(git ls-remote origin | awk '{print $2}' | sort) \
     <(git ls-remote mirror | awk '{print $2}' | sort)
```
