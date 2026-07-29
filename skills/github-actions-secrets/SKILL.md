---
name: github-actions-secrets
description: Manage secrets, environments, and variables for workflows.
---

# GitHub Actions Secrets & Environments

**Trigger**: Use when storing secrets for workflows, setting up deployment environments, or managing configuration variables.

## Secret Types

| Type | Scope | Encrypted | Best for |
|------|-------|-----------|----------|
| Repository secrets | Single repo | Yes | Per-repo keys, tokens |
| Environment secrets | Specific env | Yes | Per-env secrets (staging vs prod) |
| Organization secrets | All org repos | Yes | Shared tokens across repos |
| Variables | Repo/org/Env | No (plain text) | Non-sensitive config |

## Repository Secrets

### CLI
```bash
# Set a secret
gh secret set DOCKER_PASSWORD --body "my-docker-password"

# Set from file
gh secret set SSH_KEY < ~/.ssh/id_ed25519

# List secrets
gh secret list

# Delete
gh secret remove DOCKER_PASSWORD

# For org repos
gh secret set ORG_SECRET --org my-org --visibility all
gh secret set ORG_SECRET --org my-org --visibility selected --repos repo1,repo2
```

### Scripting
```bash
#!/bin/bash
# Bulk set from .env file
while IFS='=' read -r key value; do
  [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
  gh secret set "$key" --body "$value"
done < config.env
```

## Environment Secrets

### Create Environment
```bash
# Create environment
gh api repos/:owner/:repo/environments/production \
  --method PUT

# Set environment secret
gh secret set --env production DEPLOY_KEY --body "prod-key-123"

# List environment secrets
gh secret list --env production

# Configure protection rules
gh api repos/:owner/:repo/environments/production \
  --method PUT \
  --input - << 'EOF'
{
  "deployment_branch_policy": {
    "protected_branches": true,
    "custom_branch_policies": false
  },
  "reviewers": [{"type": "User", "id": 12345}]
}
EOF
```

### Use in Workflow
```yaml
name: Deploy
on:
  workflow_dispatch:
    inputs:
      env:
        type: choice
        options: [staging, production]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.env }}
    steps:
      - run: echo "Deploying to ${{ inputs.env }}"
      - name: Use environment secret
        run: deploy.sh ${{ secrets.DEPLOY_KEY }}
```

## Organization Variables

```bash
# Organization secret (shared across repos)
gh secret set ORG_TOKEN --org my-org --visibility all

# Organization variable (plain text)
gh variable set NPM_REGISTRY --org my-org --visibility all --body "https://npm.pkg.github.com"

# Can restrict to selected repos
gh variable set SHARED_CONFIG --org my-org --visibility selected --repos repoA,repoB
```

## Best Practices

```yaml
# Use granular secrets — don't use one token for everything
# Wrong:
- run: ./deploy.sh
  env:
    TOKEN: ${{ secrets.MEGA_TOKEN }}

# Right:
- run: ./deploy.sh
  env:
    GH_TOKEN: ${{ secrets.GH_DEPLOY_TOKEN }}
    AWS_ACCESS_KEY: ${{ secrets.AWS_DEPLOY_KEY }}

# Mask custom values in logs
- run: echo "::add-mask::${{ secrets.API_KEY }}"

# Use OIDC instead of static secrets when possible (see github-actions-oidc)
```

## Using Secrets in Actions

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # As environment variable
      - run: docker login -u ${{ secrets.DOCKER_USER }} -p ${{ secrets.DOCKER_PASS }}

      # As input to action
      - uses: some/action@v1
        with:
          api-key: ${{ secrets.API_KEY }}

      # In a file (for tools that read config files)
      - run: |
          echo "${{ secrets.GPG_KEY }}" > gpg.key
          gpg --import gpg.key
          rm gpg.key
```

## Pitfalls
- **Secret masking**: GitHub masks secrets in log output, but only after they print — don't echo them
- **Fork PRs**: Secrets aren't passed to workflows triggered by fork PRs (security measure)
- **Organization secret limits**: 1,000 org secrets, 100 per repo
- **Variable overrides**: Environment variables override repo variables, which override org variables
- **Secret rotation**: Use `gh secret set` to update; old values are immediately invalid

## Verification
```bash
gh secret list                      # Repository secrets
gh secret list --env production     # Environment secrets
gh variable list                    # Repository variables
gh api repos/:owner/:repo/environments --jq '.[].name'  # All environments
```
