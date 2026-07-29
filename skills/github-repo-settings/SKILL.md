---
name: github-repo-settings
description: Configure branch protection, visibility, and collaborators.
---

# GitHub Repo Settings

**Trigger**: Use when configuring a new repo's settings, setting up branch protection, or managing collaborators.

## CLI vs API vs Web

| Method | Best for |
|--------|----------|
| `gh` CLI | Quick settings, scripting |
| REST API | Automation, CI/CD |
| Web UI | One-time config, visual review |

## Essential Settings (gh CLI)

```bash
# Repo description and topics
gh repo edit --description "My project" --topic "rust,cli,networking"

# Default branch
gh repo edit --default-branch main

# Visibility
gh repo edit --visibility public      # public/private/internal

# Merge strategies
gh repo edit --allow-merge-commit false
gh repo edit --allow-rebase-merge true
gh repo edit --allow-squash-merge true
gh repo edit --delete-branch-on-merge true

# Features
gh repo edit --enable-issues true
gh repo edit --enable-wiki false       # Most projects use README wiki
gh repo edit --enable-projects false
gh repo edit --enable-discussions false
```

## Branch Protection Rules

```bash
# Full protection for main branch
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["continuous-integration", "code-review/lint"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true
  },
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
EOF
```

### Protection Settings Reference

| Setting | Effect |
|---------|--------|
| `required_status_checks.strict` | Require branch up to date before merge |
| `required_pull_request_reviews` | Require N approvals |
| `dismiss_stale_reviews` | Invalidate old approvals on new pushes |
| `require_code_owner_reviews` | Force CODEOWNERS review for affected files |
| `required_linear_history` | No merge commits — only rebase/squash |
| `required_conversation_resolution` | All PR comments must be resolved |
| `enforce_admins` | Apply protection to repo admins too |

## Collaborators & Teams

```bash
# Add collaborator
gh api repos/:owner/:repo/collaborators/username \
  --method PUT \
  --field permission=push    # pull/triage/push/maintain/admin

# Add team
gh api orgs/:org/teams/:team/repos/:owner/:repo \
  --method PUT \
  --field permission=push

# List collaborators
gh api repos/:owner/:repo/collaborators --jq '.[].login'
```

## API Automation

```bash
# Create repo with all settings
gh repo create my-repo --private \
  --description "Auto-created repo" \
  --gitignore Python \
  --license MIT

# Archive (read-only)
gh api repos/:owner/:repo --method PATCH \
  --field archived=true
```

## Pitfalls
- **Branch protection applies to PR merges only**: Direct pushes by admins still bypass protection unless `enforce_admins` is on
- **Rate limits**: `gh api` calls count toward GitHub's rate limit (5,000/hr authenticated)
- **Fine-grained PATs**: Need repo-scoped tokens for branch protection API calls

## Verification
```bash
gh api repos/:owner/:repo -q '.default_branch, .visibility'
gh api repos/:owner/:repo/branches/main/protection -q '.required_pull_request_reviews'
```
