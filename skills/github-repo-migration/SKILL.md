---
name: github-repo-migration
description: Migrate repos — transfer, rename, import, and export data.
---

# GitHub Repo Migration

**Trigger**: Use when transferring a repo between users/orgs, renaming, or importing from another platform.

## Transferring Repos

### Between Users
```bash
# Transfer ownership
gh api repos/:owner/:repo/transfer \
  --method POST \
  -f new_owner=new-owner

# Accept transfer (as new owner)
gh api repos/:new-owner/:repo --jq '.owner.login'
```

### Between Organizations
```bash
# Transfer to org
gh api repos/:current-owner/:repo/transfer \
  --method POST \
  -f new_owner=target-org \
  -f team_ids=[<team-id>]     # Optional: team to add after transfer
```

## Renaming

```bash
# Rename repo
gh repo edit owner/repo --name new-name

# Or via API
gh api repos/:owner/:repo \
  --method PATCH \
  -f name=new-name

# Old URL redirects to new URL automatically
# Update any webhooks, CI configs pointing to old URL
```

## Importing from Other Platforms

### From GitLab
```bash
# Direct mirror + push
git clone --mirror https://gitlab.com/owner/repo.git
cd repo.git
git remote set-url origin https://github.com/new-owner/repo.git
git push --mirror

# Issues and PRs won't transfer — use third-party tools
```

### From Bitbucket
```bash
# Same mirror approach
git clone --mirror https://bitbucket.org/owner/repo.git
cd repo.git
git remote set-url origin https://github.com/new-owner/repo.git
git push --mirror
```

### GitHub Importer (Web UI)
```bash
# Open: https://github.com/new-owner/repo/import
# Supports: GitLab, Bitbucket, Gists, SVN, TFS, Mercurial
# Imports: git history, branches, tags
# Does NOT import: issues, PRs, wikis, releases
```

## Data Export

```bash
# Export repository metadata
gh api repos/:owner/:repo --jq '.' > repo-metadata.json

# Export all issues
gh api repos/:owner/:repo/issues --paginate \
  --jq '.[] | {number, title, state, labels: [.labels[].name], created_at}' \
  > issues-export.json

# Export all PRs
gh api repos/:owner/:repo/pulls --paginate \
  --state all \
  --jq '.[] | {number, title, state, merged_at}' \
  > prs-export.json

# Export releases
gh api repos/:owner/:repo/releases --paginate \
  --jq '.[] | {tag: .tag_name, name, assets: [.assets[].name]}' \
  > releases-export.json

# Export GitHub Pages
gh api repos/:owner/:repo/pages -q '.' > pages-config.json
```

## Archiving

```bash
# Archive (read-only)
gh api repos/:owner/:repo \
  --method PATCH \
  -f archived=true

# Unarchive
gh api repos/:owner/:repo \
  --method PATCH \
  -f archived=false
```

## Bulk Operations

```bash
#!/bin/bash
# Transfer multiple repos
REPOS=("repo-a" "repo-b" "repo-c")
for repo in "${REPOS[@]}"; do
    gh api repos/old-org/$repo/transfer \
      --method POST \
      -f new_owner=new-org
    echo "Transferred $repo"
done
```

## Post-Migration Checklist

- [ ] Update local remotes: `git remote set-url origin <new-url>`
- [ ] Update CI/CD secrets and environments
- [ ] Update webhook URLs
- [ ] Update documentation/README links
- [ ] Update any external integrations (Slack, CI, deployment)
- [ ] Set up branch protection rules on the new location
- [ ] Add collaborators/teams
- [ ] Enable Pages if needed
- [ ] Archive old repo (optional)

## Pitfalls
- **Issues/PRs don't transfer**: Use third-party migration tools (e.g., `gitify`, `github-move`)
- **Webhook URLs**: Old webhook URLs break — must be recreated at the new location
- **Git LFS objects**: `--mirror` doesn't transfer LFS — use `git lfs fetch --all` before migration
- **GitHub Pages**: Pages settings don't transfer — reconfigure after migration
- **Repo redirects**: Old URL redirects to new for git operations, but not for web UI

## Verification
```bash
git ls-remote origin HEAD        # Can push/fetch?
gh repo view owner/repo          # New location visible?
gh api repos/:owner/:repo -q '{name, owner: .owner.login}'
```
