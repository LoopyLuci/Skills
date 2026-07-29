---
name: github-teams-orgs
description: Manage GitHub teams, orgs, roles, and permissions.
---

# GitHub Teams & Organizations

**Trigger**: Use when setting up teams, managing organization permissions, or configuring repository access.

## Organization vs User Accounts

| Feature | Personal user | Organization |
|---------|---------------|--------------|
| Max repositories | Unlimited | Unlimited |
| Teams | — | Yes |
| SAML SSO | No | Yes |
| Audit log | — | Yes |
| Required reviewers | — | Yes |
| Free tier features | All public | All public + private for free orgs |

## Team Management

### Create Teams
```bash
# Create a team
gh api orgs/:org/teams \
  --method POST \
  -f name=engineering \
  -f description="Engineering team" \
  -f privacy=closed                # visible only to members

# Create child team
gh api orgs/:org/teams \
  --method POST \
  -f name=frontend \
  -f parent_team_id=<engineering-id>
```

### Add Members
```bash
# Add member to team
gh api orgs/:org/teams/engineering/memberships/username \
  --method PUT \
  -f role=member                   # member or maintainer

# Add repo to team
gh api orgs/:org/teams/engineering/repos/org/repo \
  --method PUT \
  -f permission=push               # pull/triage/push/maintain/admin
```

### List Teams & Members
```bash
gh api orgs/:org/teams --jq '.[].name'
gh api orgs/:org/teams/engineering/members --jq '.[].login'
```

## Repository Permissions

| Permission | Actions | Issues | Pull | Push | Admin |
|------------|---------|--------|------|------|-------|
| Read | ✅ | ✅ | ✅ | — | — |
| Triage | ✅ | ✅ | ✅ | — | — |
| Write | ✅ | ✅ | ✅ | ✅ | — |
| Maintain | ✅ | ✅ | ✅ | ✅ | — |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

### Set Permission
```bash
gh api repos/:owner/:repo/collaborators/username \
  --method PUT \
  -f permission=push

# Remove collaborator
gh api repos/:owner/:repo/collaborators/username \
  --method DELETE
```

## Organization Settings

```bash
# Get org info
gh api orgs/:org --jq '{name, login, plan, public_repos, total_private_repos}'

# Update org settings
gh api orgs/:org --method PATCH \
  -f default_repository_permission=read \
  -f members_can_create_repositories=false \
  -f blog=https://example.com

# List org members
gh api orgs/:org/members --jq '.[].login'

# Audit log (need admin)
gh api orgs/:org/audit-log --jq '.[] | {action, actor, created_at}'
```

## SAML SSO

```bash
# Check SAML status
gh api orgs/:org --jq '.saml_sso'

# Download SAML metadata (if configured)
gh api orgs/:org/saml/sso-config/download
```

## Best Practices

1. **Use teams, not individual collaborators**: Teams scale better with automation
2. **Least privilege**: Start with `read` and escalate only when needed
3. **Child teams**: Use `engineering/frontend` instead of flat `frontend` for nested permissions
4. **Auto-assign repos**: Team `push` access auto-applies to new repos with default permission
5. **Require SAML**: For orgs with >10 members, enforce SAML SSO

## Pitfalls
- **Org limits**: Free orgs: unlimited repos but 1 GB of Actions storage, 2,000 min/month
- **Outside collaborators**: Count toward license seats but aren't org members — use sparingly
- **Team sync**: LDAP/Azure AD sync is Enterprise-only — not available on free/Team plans
- **Org webhooks**: Not inherited by repos — each repo needs its own or an org-level webhook that filters

## Verification
```bash
gh api orgs/:org/teams --jq '.[].name'
gh api orgs/:org/members --jq 'length'
gh api orgs/:org --jq '{plan, default_repo_permission}'
```
