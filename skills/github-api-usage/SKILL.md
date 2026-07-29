---
name: github-api-usage
description: Use the GitHub REST and GraphQL APIs for automation.
---

# GitHub API Usage

**Trigger**: Use when automating GitHub tasks, querying repo data, or building integrations with the GitHub API.

## Authentication

```bash
# With gh CLI (auto-auth)
gh api repos/owner/repo

# With token (scripting)
export GH_TOKEN="github_pat_..."
gh api repos/owner/repo

# With token in header
curl -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/owner/repo
```

## REST API

### Common Endpoints
```bash
# Repo info
gh api repos/:owner/:repo --jq '{name, default_branch, visibility, language, stargazers_count}'

# Latest release
gh api repos/:owner/:repo/releases/latest --jq '{tag_name, html_url, created_at}'

# Branch protection
gh api repos/:owner/:repo/branches/main/protection --jq '.required_pull_request_reviews'

# Open issues
gh api repos/:owner/:repo/issues --jq '.[].title'

# PRs
gh api repos/:owner/:repo/pulls --jq '.[] | {number, title, state, user: .user.login}'

# Workflow runs
gh api repos/:owner/:repo/actions/runs --jq '.workflow_runs[].name'

# Contributors
gh api repos/:owner/:repo/contributors --jq '.[].login'

# Commit status
gh api repos/:owner/:repo/commits/main/status --jq '.state'
```

### Pagination
```bash
# Use --paginate for collections
gh api repos/:owner/:repo/issues --paginate --jq '.[].number'

# Manual pagination
for page in 1 2 3; do
  gh api "repos/:owner/:repo/issues?page=$page&per_page=100"
done
```

### CRUD Operations
```bash
# Create issue
gh api repos/:owner/:repo/issues \
  --method POST \
  --field title="Bug found" \
  --field body="Details about the bug" \
  --field labels='["bug"]'

# Update issue
gh api repos/:owner/:repo/issues/42 \
  --method PATCH \
  --field state=closed

# Create webhook
gh api repos/:owner/:repo/hooks \
  --method POST \
  --input - << 'EOF'
{
  "name": "web",
  "active": true,
  "events": ["push", "pull_request"],
  "config": {"url": "https://example.com/webhook", "content_type": "json"}
}
EOF
```

## GraphQL API

```bash
# Run a GraphQL query
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      name
      stargazerCount
      forkCount
      defaultBranchRef { name }
      issues(first: 5, states: OPEN) {
        nodes { title, createdAt }
      }
    }
  }
'
```

### Useful GraphQL Queries

```bash
# All PRs with review status
gh api graphql -f query='
  {
    repository(owner: "owner", name: "repo") {
      pullRequests(first: 20, states: OPEN) {
        nodes {
          number, title, createdAt
          reviews(first: 5) {
            nodes { state, author { login } }
          }
        }
      }
    }
  }
'
```

## Search API

```bash
# Search code
gh api "search/code?q=apiKey+org:myorg+language:python" --jq '.items[].path'

# Search issues
gh api "search/issues?q=is:open+is:issue+label:bug+repo:owner/repo" \
  --jq '.items[].title'

# Search repos
gh api "search/repositories?q=topic:hermes-agent+stars:>10" \
  --jq '.items[] | {name: .full_name, stars: .stargazers_count}'
```

## Rate Limits

```bash
# Check remaining rate
gh api rate_limit --jq '.rate'

# Unauthenticated: 60/hr
# Authenticated: 5,000/hr
# With GITHUB_TOKEN: 5,000/hr

# Conditional requests (free — don't count toward limit)
curl -H "If-None-Match: \"etag-value\"" https://api.github.com/repos/owner/repo
```

## Pitfalls
- **Rate limiting**: 5,000 requests/hour for authenticated — use conditional requests when polling
- **GraphQL costs**: Complex queries cost more — check `rateLimit.cost` in response
- **Pagination**: Default page size is 30; max is 100 — always use `--paginate` or loop
- **Fields in REST**: Some endpoints don't return all fields by default — use `?fields=` or explicit `Accept` headers

## Verification
```bash
gh api repos/:owner/:repo --jq '.name'    # Quick connectivity test
gh api rate_limit --jq '.rate.remaining'   # Remaining quota
```
