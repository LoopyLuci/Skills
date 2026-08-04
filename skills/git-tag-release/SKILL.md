---

name: git-tag-release
description: Manage version tags and coordinate with GitHub releases.

---

# Git Tag & Release Management

**Trigger**: Use when creating version tags, cutting releases, or setting up automated release pipelines.

## Tag Types

```bash
# Lightweight tag (just a pointer)
git tag v1.0.0

# Annotated tag (recommended — stores author, date, message)
git tag -a v1.0.0 -m "Release v1.0.0 — user authentication overhaul"
```

## Semantic Versioning

Given `MAJOR.MINOR.PATCH` (e.g., `v2.5.1`):

| Increment | When | Example |
|-----------|------|---------|
| MAJOR | Breaking API change | `v2.0.0` → `v3.0.0` |
| MINOR | New feature (backward compatible) | `v2.0.0` → `v2.1.0` |
| PATCH | Bug fix (backward compatible) | `v2.0.0` → `v2.0.1` |

Pre-release: `v1.0.0-alpha.1`, `v1.0.0-rc.2`
Build metadata: `v1.0.0+build.20240729`

## Tag Workflow

### Creating Tags

```bash
# Create and push a single tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0

# Create tag at a specific commit
git tag -a v1.0.0 <commit-sha> -m "Initial release"

# Sign tags with GPG (verified on GitHub)
git tag -s v1.0.0 -m "Release v1.0.0"
```

### Listing and Viewing

```bash
git tag                              # List all tags
git tag -l "v2.*"                    # Filter by pattern
git tag --sort=-version:refname      # Sort by version (newest first)
git show v1.0.0                      # Show tag details + commit
git log --oneline --decorate=full    # See where tags point
```

### Deleting and Moving

```bash
# Delete local
git tag -d v1.0.0

# Delete remote
git push origin --delete v1.0.0
git push origin :refs/tags/v1.0.0    # Alternative syntax

# Move a tag (e.g., after a fix)
git tag -f v1.0.0 <new-sha>         # Force move tag
git push origin --force v1.0.0       # Force push (use with caution!)
```

## GitHub Releases

### CLI (gh)

```bash
# Create release from a tag
gh release create v1.2.0 \
  --title "v1.2.0 — New Features" \
  --notes "See changelog for details" \
  --target main

# With release notes from commits
gh release create v1.2.0 \
  --generate-notes

# Upload assets
gh release create v1.2.0 \
  ./dist/app-linux.tar.gz \
  ./dist/app-macos.zip \
  --title "v1.2.0"

# List/View/Delete
gh release list
gh release view v1.2.0
gh release delete v1.2.0
```

### Auto-Release from Tags (GitHub Actions)
```yaml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: go build -o myapp .
      - uses: softprops/action-gh-release@v2
        with:
          files: myapp
          generate_release_notes: true
```

## Changelog Generation

```bash
# Generate changelog from git log
git log --oneline --no-merges v1.0.0..v1.1.0 | \
  sed 's/^/* /' > CHANGELOG.md

# Conventional commits to changelog
git log --oneline --no-merges v1.0.0..v1.1.0 | \
  grep "^.*feat\|^.*fix" | sed 's/^/* /'
```

## Pitfalls
- **Tags without releases**: A git tag exists, but no GitHub release — users can still `git checkout` it
- **Force-pushing tags breaks CI**: Anyone who fetched the old tag has a mismatch
- **Lightweight tags on GitHub**: Show without release notes — prefer annotated
- **Tag name format**: Use `v` prefix (`v1.0.0` not `1.0.0`) — conventional and `gh` expects it
- **Signed tags on clone**: `git clone` fetches them; `git tag -v <tag>` verifies

## Verification
```bash
git tag -n                          # List all tags with annotations
git describe --tags                 # Current tag + commits since
gh release list                     # Verify on GitHub
```
