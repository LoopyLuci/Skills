---
name: github-insights-traffic
description: Analyze repo traffic, contributions, and community metrics.
---

# GitHub Insights & Traffic

**Trigger**: Use when analyzing repository traffic, tracking clone/download stats, or reviewing contributor analytics.

## Traffic Analytics

### View Traffic via API
```bash
# Clones (last 14 days)
gh api repos/:owner/:repo/traffic/clones --jq '.clones[] | {timestamp, count, uniques}'

# Views (last 14 days)
gh api repos/:owner/:repo/traffic/views --jq '.views[] | {timestamp, count, uniques}'

# Referrers (where traffic comes from)
gh api repos/:owner/:repo/traffic/popular/referrers --jq '.[].referrer'

# Popular content
gh api repos/:owner/:repo/traffic/popular/paths --jq '.[].path'
```

### Summary
```bash
gh api repos/:owner/:repo/traffic/clones --jq '{
  total: .count,
  unique: .uniques,
  daily_average: (.count / (.clones | length))
}'
```

## Contributor Analytics

```bash
# Top contributors
gh api repos/:owner/:repo/contributors --jq \
  '.[] | {login, contributions, type}'

# Weekly activity
gh api repos/:owner/:repo/stats/code_frequency --jq \
  '.[] | {week: .[0], additions: .[1], deletions: .[2]}'

# Commit activity (per week)
gh api repos/:owner/:repo/stats/commit_activity --jq \
  '.[] | {week: .week, days: .days}'

# Punch card (hour of week)
gh api repos/:owner/:repo/stats/punch_card

# Participation (weekly commits, last year)
gh api repos/:owner/:repo/stats/participation --jq '.all'
```

## Community Profile

```bash
# Community standards
gh api repos/:owner/:repo/community/profile --jq '{
  health_percentage: .health_percentage,
  files: .files | keys
}'

# Check for standard files
gh api repos/:owner/:repo/community/profile -q \
  '.files | to_entries[] | select(.value.present == false) | .key + " — MISSING"'
```

## Dependency Insights

```bash
# Dependency graph (published)
gh api repos/:owner/:repo/dependency-graph/snapshots \
  --jq '.manifests | keys'

# Vulnerability alerts (need security access)
gh api repos/:owner/:repo/dependabot/alerts --jq \
  '.[] | {summary: .security_advisory.summary, severity: .security_advisory.severity}'
```

## Forks & Stars

```bash
# Stars over time (via starred events)
gh api repos/:owner/:repo/stargazers --jq '.[].starred_at'

# Fork count (direct from repo)
gh api repos/:owner/:repo --jq '{forks: .forks_count, stars: .stargazers_count}'

# Watchers
gh api repos/:owner/:repo/subscribers --jq '.[].login'
```

## Release Downloads

```bash
# Download counts per release
gh api repos/:owner/:repo/releases --jq \
  '.[] | {tag: .tag_name, downloads: .assets[].download_count}'
```

## Aggregation Script

```bash
#!/bin/bash
# repo-health.sh — Quick health check for a repo
REPO="${1:-:owner/:repo}"
echo "=== $REPO Health ==="
gh api repos/$REPO --jq '{
  name, stars: .stargazers_count, forks: .forks_count,
  open_issues: .open_issues_count, license: .license.spdx_id,
  last_push: .pushed_at
}'
echo "--- Clones (14d) ---"
gh api repos/$REPO/traffic/clones --jq '{total: .count, unique: .uniques}'
echo "--- Top Contributors ---"
gh api repos/$REPO/contributors --jq '.[:5] | .[] | "\(.login): \(.contributions) commits"'
```

## Pitfalls
- **14-day window**: Traffic data only covers the last 14 days — export regularly for long-term tracking
- **Incremental counts**: Clone/view counts are not de-duplicated across time periods
- **Community profile caching**: The health percentage is cached — refresh may take a few minutes
- **Contributors API excludes bots**: Set `?exclude_bots=false` to include bot accounts
- **Git Archive access**: Archived repos return 410 for traffic endpoints

## Verification
```bash
gh api repos/:owner/:repo/traffic/clones --jq '.count'
gh api repos/:owner/:repo/contributors --jq 'length'
gh api repos/:owner/:repo/community/profile -q '.health_percentage'
```
