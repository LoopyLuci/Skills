---
name: changelog-generation
description: "Auto generate CHANGELOG from conventional commits"
---

# Changelog Generation

## Conventional Commits
```
feat: add user login
fix: resolve timeout
docs: update API ref
BREAKING CHANGE: new API
```

## Auto-Generate
```bash
pip install git-cliff
git-cliff -o CHANGELOG.md
```

## Manual Entry
```markdown
## [1.2.0] - 2026-07-29
### Added
- New feature X
### Fixed
- Bug in Y
```
