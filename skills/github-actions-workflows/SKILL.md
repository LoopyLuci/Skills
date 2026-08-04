---

name: github-actions-workflows
description: Author CI/CD workflows — triggers, jobs, steps, and runners.

---

# GitHub Actions Workflows

**Trigger**: Use when creating a new GitHub Actions workflow, configuring triggers, or structuring CI/CD jobs.

## Workflow Anatomy

```yaml
name: CI
on:                                # Trigger
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:                               # Global env vars
  CARGO_TERM_COLOR: always

jobs:
  test:                            # Job name
    runs-on: ubuntu-latest         # Runner
    strategy:                      # Matrix (optional)
      matrix:
        os: [ubuntu, macos, windows]
    steps:                         # Sequence
      - uses: actions/checkout@v4  # Action
      - run: cargo test            # Shell command
```

## Triggers

| Trigger | Event | When it fires |
|---------|-------|---------------|
| `push` | Push to branch/tag | `branches:`, `tags:`, `paths:` |
| `pull_request` | PR events | `types: [opened, synchronize, reopened]` |
| `workflow_dispatch` | Manual trigger | Button in Actions tab |
| `schedule` | Cron | `cron: '0 0 * * *'` |
| `workflow_run` | Another workflow | `workflows: ["Build"]` |
| `repository_dispatch` | External API | Custom webhook events |
| `issue_comment` | Issue/PR comments | `types: [created, edited]` |

### Path Filters
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '*.rs'
      - '!docs/**'         # Ignore docs changes
```

## Job Configuration

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10           # Default 360
    continue-on-error: false      # Don't fail fast
    
    # Dependencies
    needs: [lint, build]
    
    # Environment
    environment: staging
    
    # Service containers
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      - run: cargo test
```

## Common Actions

```yaml
# Checkout
- uses: actions/checkout@v4
  with:
    fetch-depth: 0           # Full history (for git log, tags)
    submodules: recursive    # Checkout submodules

# Setup language
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'

- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

- uses: actions-rust-lang/setup-rust-toolchain@v1

# Cache
- uses: actions/cache@v4
  with:
    path: ~/.cargo/registry
    key: cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}

# Upload/download artifacts
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/
- uses: actions/download-artifact@v4
```

## Environment Variables

```yaml
# Workflow level
env:
  NODE_ENV: test

# Job level
jobs:
  test:
    env:
      DATABASE_URL: postgres://localhost/test

# Step level
    - run: cargo test
      env:
        RUST_LOG: debug

# Automatic variables
# ${{ github.repository }}  — owner/repo
# ${{ github.ref }}         — refs/heads/main
# ${{ github.sha }}         — commit SHA
# ${{ github.actor }}       — who triggered
# ${{ secrets.MY_SECRET }}  — from repo settings
# ${{ vars.MY_VAR }}        — from repo/organization variables
```

## Conditionals

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Only on main"
      
      - name: Conditional step
        if: ${{ contains(github.event.head_commit.message, '[deploy]') }}
        run: ./deploy.sh

      - name: Cancel on skip
        if: ${{ !contains(github.event.head_commit.message, '[skip ci]') }}
        run: npm test
```

## Workflow Dispatch Inputs

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy target'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
      debug:
        description: 'Enable debug'
        type: boolean
        default: false
jobs:
  deploy:
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
      - if: ${{ inputs.debug }}
        run: echo "Debug mode enabled"
```

## Pitfalls
- **Cost**: Free tier: 2,000 min/month Linux, Windows/Mac costs more
- **Evasive secrets**: Don't echo secrets — GitHub masks them but only after printing
- **Workflow limits**: 72-hour max runtime, 1,000 API requests/hour
- **Matrix explosion**: 4 OS × 3 language versions × 2 configs = 24 runners — use `include`/`exclude`

## Verification
```bash
gh workflow list                    # All workflows
gh run list --limit 5               # Recent runs
gh run view <id> --log --job test   # Job logs
```
