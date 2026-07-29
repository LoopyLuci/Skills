---
name: git-shallow-sparse
description: Clone partially — shallow, sparse, and blobless checkouts.
---

# Git Shallow & Sparse Clones

**Trigger**: Use when cloning large repos, working in CI with limited history, or only needing part of a monorepo.

## Clone Types for Large Repos

| Technique | What it does | Speed gain | Use case |
|-----------|-------------|------------|----------|
| Shallow clone | `--depth 1` — last commit only | 10-50x | CI, build-only |
| Sparse checkout | Subset of files | 2-5x | Monorepo single project |
| Blobless clone | `--filter=blob:none` — no file contents | 5-10x | Full history, no blobs |
| Tree-less clone | `--filter=tree:0` — minimal metadata | 50-100x | Very large monorepos |

## Shallow Clone

```bash
# Last commit only
git clone --depth 1 https://github.com/owner/repo.git

# Last N commits
git clone --depth 50 https://github.com/owner/repo.git

# Shallow since a date
git clone --shallow-since="2024-01-01" https://github.com/owner/repo.git

# Shallow with tags
git clone --depth 1 --no-single-branch https://github.com/owner/repo.git

# Un-shallow (fetch the rest)
git fetch --unshallow
```

## Sparse Checkout

```bash
# Clone without checking out files
git clone --no-checkout https://github.com/owner/repo.git
cd repo

# Enable sparse checkout
git sparse-checkout init --cone     # Cone mode (fast)
git sparse-checkout set src/api tests/
git checkout main

# Add more directories
git sparse-checkout add docs/

# List sparse patterns
git sparse-checkout list

# Disable sparse checkout
git sparse-checkout disable
```

### Sparse Checkout with Shallow
```bash
# Combined — fastest possible clone for CI
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/owner/repo.git
cd repo
git sparse-checkout set src/my-package/
```

## Blobless & Treeless Clones

```bash
# Blobless — full commit/tree history, no file contents
git clone --filter=blob:none https://github.com/owner/repo.git
# Files are downloaded on-demand during checkout

# Treeless — minimal (no trees either)
git clone --filter=tree:0 https://github.com/owner/repo.git
# Needs --depth or partial clone protocol

# Partial clone with fetch
git clone --filter=blob:none https://github.com/owner/repo.git
git checkout main                        # Downloads files for HEAD
git diff HEAD~1 HEAD -- src/file.ts      # Downloads blob for that commit
```

## CI Optimizations

```yaml
# Fastest CI checkout
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 1           # Shallow — no history
      sparse-checkout: |       # Only needed dirs
        src/
        tests/
        Cargo.toml
      sparse-checkout-cone-mode: true
```

## Working with Partial Clones

```bash
# Git-aware operations still work
git log --oneline -5           # History is local (blobless mode)
git diff HEAD~1                # Downloads missing blobs automatically

# Force download all blobs
git fetch --refetch

# Check what's missing
git rev-list --objects --all --count 2>/dev/null
git cat-file --batch-check --batch-all-objects | wc -l
```

## Pitfalls
- **Shallow push**: `git push` from shallow clone fails if remote doesn't have the base — use `--depth` with matching remote
- **Sparse + tags**: `git fetch --tags` in cone mode fetches tags but not files outside cone
- **Blobless clone requires protocol v2**: `git config --global protocol.version 2`
- **CI with shallow**: Some actions (like CodeQL) need full history — override with `fetch-depth: 0`
- **Partial clone + LFS**: LFS files still download as needed — no extra benefit

## Verification
```bash
git rev-list --count HEAD              # Commits in local history
git ls-files | wc -l                   # Checked-out files
git rev-parse --is-shallow-repository  # true/false
git sparse-checkout list               # Active sparse patterns
```
