---
name: changelog-generation
description: Auto generate CHANGELOG from conventional commits
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [changelog, generation]
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

## Trigger

Activate this skill when the user mentions:
- changelog, generation workflows or issues
- Building, fixing, or optimizing changelog generation


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
