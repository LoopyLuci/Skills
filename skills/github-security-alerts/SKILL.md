---

name: github-security-alerts
description: Manage Dependabot, secret scanning, and code scanning.

---

# GitHub Security & Alerts

**Trigger**: Use when setting up dependency scanning, managing security alerts, or configuring vulnerability detection.

## GitHub Security Features

| Feature | What it does | Availability |
|---------|-------------|--------------|
| Dependabot alerts | Known vulnerabilities | Public + private |
| Dependabot updates | Auto-PRs for vulnerable deps | Public + private |
| Secret scanning | Credentials in code | Public + private |
| Code scanning (CodeQL) | Code vulnerabilities | Public repos (free) |

## Dependabot Setup

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "automerge"
    groups:
      minor-and-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "cargo"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Secret Scanning

```bash
# Enable
gh api repos/:owner/:repo \
  --method PATCH \
  --field security_and_analysis='{"secret_scanning":{"status":"enabled"}}'

# Push protection
gh api repos/:owner/:repo \
  --method PATCH \
  --field security_and_analysis='{"secret_scanning_push_protection":{"status":"enabled"}}'
```

## Code Scanning (CodeQL)

```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'
jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    strategy:
      matrix:
        language: ['javascript', 'python']
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
      - uses: github/codeql-action/analyze@v3
```

## Alert Management

```bash
# List alerts
gh api repos/:owner/:repo/dependabot/alerts --jq '.[].security_advisory.summary'
gh api repos/:owner/:repo/secret-scanning/alerts --jq '.[].secret_type'
gh api repos/:owner/:repo/code-scanning/alerts --jq '.[].rule.description'

# Dismiss an alert
gh api repos/:owner/:repo/dependabot/alerts/1 \
  --method PATCH \
  --field state=dismissed \
  --field dismissed_reason="tolerable_risk"
```

## Pitfalls
- **False positives**: Suppress obvious false positives rather than leaving open alerts
- **Dependabot limits**: 5 concurrent PRs per ecosystem by default — increase with `open-pull-requests-limit`
- **Secret push protection**: Can be bypassed by admins — combine with branch protection
- **CodeQL analysis time**: Large repos can take 30+ min — use `queries` filter to narrow

## Verification
```bash
gh api repos/:owner/:repo/dependabot/alerts --jq 'length'
gh api repos/:owner/:repo/code-scanning/alerts --jq 'length'
```
