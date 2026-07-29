---
name: git-maintenance-optimization
description: Optimize git repos — gc, repack, and regular maintenance.
---

# Git Maintenance & Optimization

**Trigger**: Use when optimizing git performance, reducing disk usage, or running scheduled maintenance.

## Key Commands

| Command | What it does | When to run |
|---------|-------------|-------------|
| `git gc` | Garbage collect — removes unreachable objects | Monthly, or after large operations |
| `git repack` | Reorganize object packs for performance | After many small commits |
| `git prune` | Remove unreachable objects | After `git gc` if space is critical |
| `git maintenance` | Scheduled background maintenance (v2.30+) | Automatic — set and forget |
| `git fsck` | Check repository integrity | After crashes, or quarterly |

## Git GC

```bash
# Standard garbage collection
git gc

# Aggressive (slower, better compression)
git gc --aggressive

# Prune old objects (default: 2 weeks)
git gc --prune=now                 # Immediate cleanup
git gc --prune=1.week.ago          # Keep objects < 1 week

# Auto mode (runs when needed)
git gc --auto

# Check what gc would do
git gc --dry-run
```

## Manual Repacking

```bash
# Repack all objects into one pack (best compression)
git repack -a -d --depth=250 --window=250

# Repack with bitmap (faster clones/fetches)
git repack -a -d --write-bitmap-index

# Delta islands (monorepos — separate object sharing)
git repack -a -d --delta-islands

# Show pack info
git count-objects -vH
```

## Git Maintenance (v2.30+)

```bash
# Start automatic background maintenance
git maintenance start

# View current tasks
git maintenance run

# Run specific task
git maintenance run --task=gc
git maintenance run --task=prefetch
git maintenance run --task=loose-objects
git maintenance run --task=incremental-repack
git maintenance run --task=pack-refs

# Stop maintenance
git maintenance stop

# Register repo for maintenance
git maintenance register
```

### Maintenance Config
```bash
# Maintenance strategy
git config maintenance.strategy incremental
# Options: none, incremental, full

# Task schedule
git config maintenance.gc.auto 1
git config maintenance.commit-graph.auto 1
```

## Integrity Checks

```bash
# Full filesystem check
git fsck

# Check only for corruption (not dangling objects)
git fsck --strict

# Check connectivity
git fsck --connectivity-only

# Check all objects
git fsck --full

# Check specific object
git fsck <object-sha>

# Auto-fix (only safe fixes)
git fsck --auto
```

## Performance Tuning

```bash
# Optimize commit graph (faster git log)
git commit-graph write --reachable

# Enable commit-graph for all clones
git config --global fetch.writeCommitGraph true

# Increase pack window for better compression
git config pack.window 250
git config pack.depth 250

# Multi-pack index (faster object lookup with many packs)
git multi-pack-index write

# Enable feature.manyFiles (monorepo optimization)
git config feature.manyFiles true
```

## Scheduled Maintenance Script

```bash
#!/bin/bash
# ~/.local/bin/git-maintenance.sh — run weekly via cron
for repo in ~/projects/*/; do
    cd "$repo"
    echo "=== $(basename "$repo") ==="
    git gc --auto --quiet
    git commit-graph write --reachable --changed-paths
done
```

## Disk Usage Analysis

```bash
# Show object store size
git count-objects -vH

# Large objects
git rev-list --all --objects | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print $3, $4}' | sort -rn | head -10

# Top largest files (with names)
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sed -n 's/^blob //p' | sort -rn -k1 | head -20
```

## Pitfalls
- **gc --aggressive**: Very slow on large repos (hours) — only run when needed
- **prune=now**: Can lose objects currently referenced by reflog entries — expire reflog first
- **Shared repos**: Running `git gc` on a `--shared` clone can corrupt other clones
- **Maintenance v2.30+**: Older git versions don't have `git maintenance` — use cron scripts instead
- **Network drives**: `git gc` on network filesystems can be unreliable — run locally

## Verification
```bash
git count-objects -vH                 # Disk usage
git fsck --connectivity-only          # Health check
git maintenance run --dry-run         # Maintenance preview
git commit-graph verify               # Commit graph integrity
```
