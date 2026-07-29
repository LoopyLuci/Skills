---
name: github-actions-matrix
description: Run test/config combos in parallel with matrix strategy.
---

# GitHub Actions Matrix Builds

**Trigger**: Use when running tests across multiple OS, language versions, or configurations in parallel.

## Basic Matrix

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20, 22]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

This creates 3 × 3 = 9 parallel runners.

## Controlling the Matrix

### Include
```yaml
include:
  - os: macos
    node: 22         # Extra combo not in main grid
  - os: ubuntu
    node: 18
    coverage: true   # Extra variable
```

### Exclude
```yaml
exclude:
  - os: windows
    node: 22
  - os: macos
    node: 18
```

### Fail Fast & Concurrency
```yaml
strategy:
  fail-fast: false      # Continue other jobs even if one fails
  max-parallel: 4       # Max concurrent runners
  matrix: ...
```

## Real-World Examples

### Rust — Multiple Checks
```yaml
strategy:
  matrix:
    job:
      - {cmd: "cargo test", os: ubuntu-latest}
      - {cmd: "cargo clippy", os: ubuntu-latest}
      - {cmd: "cargo fmt --check", os: ubuntu-latest}
      - {cmd: "cargo test", os: macos-latest}
      - {cmd: "cargo test", os: windows-latest}
```

### Python — Versions + OS
```yaml
matrix:
  os: [ubuntu-latest, macos-latest]
  python: ['3.10', '3.11', '3.12']
  include:
    - os: windows-latest
      python: '3.12'
```

## Dynamic Matrix

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.m.outputs.matrix }}
    steps:
      - id: m
        run: |
          echo 'matrix={"os":["ubuntu","macos"],"node":["18","20"]}' >> $GITHUB_OUTPUT
  build:
    needs: setup
    strategy:
      matrix: ${{ fromJson(needs.setup.outputs.matrix) }}
```

## Pitfalls
- **Matrix explosion**: 4 OS × 5 versions × 3 configs = 60 runners — use `exclude` and `max-parallel`
- **Cost**: Each job is a separate runner minute
- **Cache per combo**: Each matrix combo gets its own cache key

## Verification
```bash
gh run view <run-id> --json jobs --jq '.jobs[].name'
```
