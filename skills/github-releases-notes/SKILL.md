---
name: github-releases-notes
description: Create releases, automate release notes, and manage assets.
---

# GitHub Releases & Release Notes

**Trigger**: Use when creating a GitHub release, generating release notes, or automating the release pipeline.

## Creating Releases

### Manual (gh CLI)
```bash
# Simple release from latest tag
gh release create v1.2.0

# With custom title and notes
gh release create v1.2.0 \
  --title "v1.2.0 — Authentication Overhaul" \
  --notes "See changelog for details"

# Auto-generate from commits since last tag
gh release create v1.2.0 \
  --generate-notes

# With assets
gh release create v1.2.0 \
  ./dist/app-linux.tar.gz \
  ./dist/app-macos.dmg \
  ./dist/app-windows.exe \
  --title "v1.2.0"

# Create from a specific branch
gh release create v1.2.0 --target main
```

### Release Types
```bash
gh release create v1.2.0                           # Latest release
gh release create v1.2.0 --prerelease               # Pre-release
gh release create v1.2.0 --draft                    # Draft (not visible)
gh release create v1.2.0 --discussion-category announcements  # Enable discussions
```

## Viewing & Managing

```bash
gh release list
gh release list --limit 50
gh release view v1.2.0
gh release view v1.2.0 --json body,tagName,createdAt
gh release download v1.2.0
gh release download v1.2.0 --pattern "*.tar.gz"
gh release edit v1.2.0 --title "Updated Title" --notes "Updated notes"
gh release delete v1.2.0
```

## Automated Release Workflow

### GitHub Actions — Release on Tag Push
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
      - name: Build
        run: |
          mkdir -p dist
          echo "release-$(git describe --tags)" > dist/version.txt
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/*
          generate_release_notes: true
          make_latest: true
```

### Release Notes Generation (manual)
```bash
# Generate notes from git log
git log --oneline --no-merges $(git tag --sort=-version:refname | head -1)..HEAD | \
  sed 's/^/  * /' > release-notes.md

# Categorized by type
echo "## Features" >> release-notes.md
git log --oneline --no-merges v1.0.0..v1.1.0 | grep "^.*feat" | sed 's/^/  * /' >> release-notes.md
echo "## Fixes" >> release-notes.md
git log --oneline --no-merges v1.0.0..v1.1.0 | grep "^.*fix" | sed 's/^/  * /' >> release-notes.md
```

## Multi-Platform Release

```yaml
name: Multi-Platform Release
on:
  push:
    tags: ['v*']
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - run: cargo build --release
      - uses: actions/upload-artifact@v4
        with:
          name: binary-${{ runner.os }}
          path: target/release/myapp*
  release:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/download-artifact@v4
      - uses: softprops/action-gh-release@v2
        with:
          files: binary-*/*
          generate_release_notes: true
```

## Pitfalls
- **Tag without release**: `git push --tags` creates the tag but no GitHub release page
- **Asset size limit**: GitHub limits release assets to 2 GB total, 500 MB per file
- **Draft releases**: Not visible via API until published — CI won't find them

## Verification
```bash
gh release list --limit 5
gh release view $(gh release list --json tagName --jq '.[0].tagName')
git tag -n | head -10
```
