---
name: git-patch-management
description: Create, apply, and share changes as patch files.
---

# Git Patch Management

**Trigger**: Use when sharing changes without a remote, applying patches from others, or working in air-gapped environments.

## Creating Patches

### From Commits
```bash
# Single commit
git format-patch -1 HEAD                # Last commit → 0001-*.patch
git format-patch -3                     # Last 3 commits → 3 .patch files
git format-patch main..feature          # All commits in feature not in main

# Range of commits
git format-patch a1b2c3..d4e5f6         # Commits between SHAs

# With custom output directory
git format-patch main..feature -o patches/
```

### From Working Directory
```bash
# Uncommitted changes (unstaged + staged)
git diff > changes.patch

# Only staged changes
git diff --cached > staged-changes.patch

# Only unstaged changes
git diff > unstaged-changes.patch
```

### Single File
```bash
git format-patch -1 -- src/file.ts      # Patch with only that file
git diff src/file.ts > file-change.patch
```

## Applying Patches

```bash
# Apply from mailbox (format-patch format — preserves commit metadata)
git am < 0001-feat-add-auth.patch
git am --signoff < patch.patch          # Add Signed-off-by

# Apply as a diff (no metadata — just changes)
git apply < changes.patch

# Apply, then stage
git apply --index < changes.patch

# Check if patch applies cleanly
git apply --check < changes.patch
```

## Patch Workflow

### Sending via Email
```bash
# Configure email
git config sendemail.to "maintainer@example.com"
git config sendemail.smtpserver smtp.gmail.com
git config sendemail.smtpuser you@gmail.com

# Send patch series
git send-email --to maintainer@example.com \
  --subject-prefix "PATCH v2" \
  patches/*.patch
```

### Contributing via Patch (no GitHub)
```bash
# Generate your changes
git format-patch main --stdout > my-contribution.patch

# Share via email, paste, or attachment
# Maintainer applies:
git am < my-contribution.patch
```

## Patch with Binary Files

```bash
# Include binary changes
git format-patch --binary main..
git am --binary < patch.patch
```

## Resolving Conflicts

```bash
# If git am fails:
# 1. Fix conflicts manually
# 2. Stage resolved files: git add <file>
# 3. Continue: git am --continue
# OR: git am --skip (skip this patch)
# OR: git am --abort (cancel entire patch series)

# If git apply fails:
git apply --reject < changes.patch
# Creates .rej files with rejected hunks — fix manually
```

## Pitfalls
- **No commit metadata in `git diff`**: Use `git format-patch` / `git am` to preserve author, date, message
- **Binary files**: Not all binary formats survive patch format — use `--binary`
- **Renamed files**: Patches track renames if `git diff` detects them, but can confuse `git am`
- **Signed commits**: `git format-patch` doesn't preserve GPG signatures
- **Large patches**: Prefer a shared remote for large change sets

## Verification
```bash
# Inspect patch content
head -20 0001-feat-add-auth.patch
grep "^Subject:" *.patch               # Patch subjects

# Verify patch applies cleanly
git apply --check < changes.patch && echo "Clean"
```
