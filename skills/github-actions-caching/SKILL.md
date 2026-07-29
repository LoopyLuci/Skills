---
name: github-actions-caching
description: Cache dependencies and build outputs to speed up workflows.
---

# GitHub Actions Caching

**Trigger**: Use when optimizing workflow speed by caching dependencies, build artifacts, or downloaded data.

## How Caching Works

GitHub Actions cache is a key-value store scoped to a branch + repository. Each cache entry has:
- **Key**: Deterministic (e.g., hash of lockfile)
- **Restore keys**: Fallback patterns if exact key miss
- **Paths**: What to save/restore
- **Scope**: `ref` (branch) — cache is branch-specific

## Basic Cache Setup

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
    restore-keys: |
      npm-${{ runner.os }}-
```

## By Language

### Node.js / npm
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'                     # Built-in — handles ~/.npm + node_modules
```

### Python / pip
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'                     # Built-in — handles ~/.cache/pip

# Manual (requirements.txt)
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      pip-${{ runner.os }}-
```

### Rust / Cargo
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry
      ~/.cargo/git
      target
    key: cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}-${{ github.sha }}
    restore-keys: |
      cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}
      cargo-${{ runner.os }}-
```

### Go
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
    key: go-${{ runner.os }}-${{ hashFiles('**/go.sum') }}
    restore-keys: |
      go-${{ runner.os }}-
```

## Advanced Patterns

### Matrix Caching
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20]
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node }}
      cache: 'npm'
  # Each os+node combo gets its own cache
```

### Cache per Workflow Run
```yaml
# Include commit SHA to avoid reading stale cache
key: cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}-${{ github.sha }}
restore-keys: |
  cargo-${{ runner.os }}-${{ hashFiles('**/Cargo.lock') }}
  cargo-${{ runner.os }}-
```

### Cache Across Branches
```yaml
# restore-keys without the exact hash match fall back to any branch
restore-keys: |
  npm-${{ runner.os }}-
```

## Cache Limits

| Plan | Max size | Max entries | Retention |
|------|----------|-------------|-----------|
| Free | 10 GB | 1,000 | 7 days |
| Pro | 10 GB | 1,000 | 7 days |
| Team | 10 GB | 1,000 | 7 days |
| Enterprise | 50 GB | 1,000 | 7 days |

## Cache Actions

```yaml
# Dependency cache (recommended for most cases)
- uses: actions/cache@v4

# Package manager built-in caches (preferred)
- uses: actions/setup-node@v4
  with:
    cache: 'npm'

# Save always, even on failure
- uses: actions/cache@v4
  if: ${{ !cancelled() }}        # Save even if tests fail
  with:
    path: .next/cache
    key: next-${{ runner.os }}-${{ hashFiles('next.config.js') }}
```

## Debugging Cache

```bash
# Check cache hit/miss in workflow logs
# Look for: Cache restored from key: npm-ubuntu-abc123
# Cache Size: ~15 MB (12345678 bytes)

# Clear cache for a specific key
# There's no API to delete — let it expire or change the key
```

## Pitfalls
- **Cache poisoning**: Don't cache build outputs that could contain stale binaries — prefer dep-only caches
- **Cache size limits**: 10 GB fills quickly with node_modules across many branches
- **Branch isolation**: Cache from `feature/foo` can't be restored on `feature/bar` unless restore-keys match
- **No cache on schedule**: `schedule` events don't have a branch cache context — use `workflow_dispatch` to warm
- **Cache version stale**: Change the cache key version (e.g., `v2-`) when you need to invalidate all

## Verification
```bash
# Check cache usage in workflow logs
gh run view <id> --log | grep -i "cache"

# Monitor cache size
gh api repos/:owner/:repo/actions/caches --jq '.actions_caches[].size_in_bytes'
```
