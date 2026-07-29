---
name: git-lfs-setup
description: Manage large files in git repositories with Git LFS.
---

# Git Large File Storage (LFS)

**Trigger**: Use when storing binary files, large assets, datasets, or any file over 50 MB in a git repo.

## When to Use LFS

| File type | Example | Use LFS? |
|-----------|---------|----------|
| Binaries | `.exe`, `.dll`, `.so` | ✅ |
| Media | `.mp4`, `.mov`, `.wav` | ✅ |
| Images | `.psd`, `.tiff`, `.png > 1MB` | ✅ |
| Datasets | `.parquet`, `.h5`, `.csv > 10MB` | ✅ |
| Archives | `.zip`, `.tar.gz`, `.7z` | ✅ |
| Models | `.pth`, `.h5`, `.gguf`, `.onnx` | ✅ |
| Small images | `.png < 100KB`, `.jpg` | ❌ (text repo is fine) |
| Source code | `.py`, `.rs`, `.ts`, `.js` | ❌ (never LFS) |

## Setup

```bash
# Install LFS
git lfs install                    # One-time global setup

# Track file patterns
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "**/*.bin"

# Commit .gitattributes (required — tracks the LFS config)
git add .gitattributes
git commit -m "chore: configure LFS for binary files"

# Use git normally — LFS handles transparently
git add assets/design.psd
git commit -m "feat: add mockup"
git push
```

## Common Patterns

```bash
# Track by extension
git lfs track "*.psd" "*.mp4" "*.zip"

# Track by directory
git lfs track "models/**"
git lfs track "datasets/*.parquet"

# Track specific file
git lfs track "large_checkpoint.pt"

# List tracked patterns
git lfs track

# Check if a file is tracked by LFS
git lfs ls-files --all
```

## Migration

### Convert Existing Files to LFS
```bash
# Migrate existing tracked files to LFS
git lfs migrate import --include="*.psd,*.mp4" --everything

# Migrate only recent history (faster)
git lfs migrate import --include="*.psd" --include-ref=main --include-ref=develop

# Fix .gitattributes after migration
git lfs migrate info                                # Show what's LFS
```

### Undo LFS (move back to regular git)
```bash
# Remove LFS tracking
git lfs untrack "*.psd"
git rm .gitattributes
git lfs migrate export --include="*.psd" --everything
```

## LFS Operations

```bash
# Pull LFS files (after clone)
git lfs pull

# Fetch LFS files without checkout
git lfs fetch --all

# Check LFS disk usage
git lfs ls-files --all --size

# Prune old LFS objects locally
git lfs prune

# Lock a file (prevent concurrent edits)
git lfs lock assets/design.psd
git lfs locks                              # List locks
git lfs unlock assets/design.psd
```

## CI/CD Considerations

```yaml
# GitHub Actions — LFS needs manual checkout
steps:
  - uses: actions/checkout@v4
    with:
      lfs: true                           # Pull LFS files

  # Or install LFS first
  - run: |
      git lfs install
      git lfs pull
```

## Pitfalls
- **Bandwidth limits**: GitHub LFS has 1 GB/month free; 50 GB/month for Pro — overages cost $$
- **Clone speed**: LFS repos clone slower — each LFS file is an HTTP download
- **LFS + CI minutes**: CI runners download LFS files every run — can waste minutes
- **No diffs**: Git can't diff LFS files — `git diff` shows pointer files, not content
- **LFS pointer files**: If LFS isn't installed, you'll see `.gitattributes` pointer files instead of real content
- **Migration rewrites history**: `git lfs migrate import` changes SHAs — coordinate with team

## Verification
```bash
git lfs track                            # Tracked patterns
git lfs ls-files --all | head -5         # LFS files in repo
git lfs env                              # LFS configuration
du -sh .git/lfs/                         # LFS storage used locally
```
