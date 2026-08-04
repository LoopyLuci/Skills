---

name: git-commit-conventions
description: Write conventional, searchable commit messages with types.

---

# Git Commit Conventions

**Trigger**: Use when writing commit messages, setting up commit standards, or linting commit history.

## Conventional Commits Standard

```
<type>(<scope>): <description>

<body>

<footer>
```

```
feat(auth): add OAuth2 refresh token flow

Implement token rotation with 7-day expiry window.
Store refresh tokens in HTTP-only cookies.

Closes #123
BREAKING CHANGE: drops support for legacy API keys
```

### Types

| Type | When to use | Version bump |
|------|------------|--------------|
| `feat` | New feature | MINOR |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | — |
| `style` | Formatting, whitespace | — |
| `refactor` | Code change that neither fixes nor adds | — |
| `perf` | Performance improvement | — |
| `test` | Adding/fixing tests | — |
| `build` | Build system, dependencies | — |
| `ci` | CI/CD configuration | — |
| `chore` | Maintenance, tooling | — |
| `revert` | Revert a previous commit | — |

## Best Practices

```
# Good — descriptive, completes the sentence "This commit will..."
feat(api): add pagination support to /users endpoint
fix(db): handle null values in user email migration
docs: update README with deployment instructions

# Bad — vague, doesn't explain why
update stuff
fix bug
WIP
```

### Body Guidelines
- Explain **why**, not just **what**
- Reference related issues: `Closes #42`, `See #128`
- Note trade-offs: `This approach was chosen over X because...`
- Wrap at 72 characters

## Configuration

### Commit Message Template
```bash
git config --global commit.template ~/.gitmessage
```

`~/.gitmessage`:
```
# <type>(<scope>): <subject>
# |<---- 50 chars max ---->|

# <body> — explain what and why, not how (72 chars wrap)
#
# Closes #<issue>
```

### Commit Linting (CI)
```yaml
name: Lint Commits
on: [pull_request]
jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - uses: wagoid/commitlint-github-action@v5
```

### Auto-Changelog with semantic-release
```bash
npm install -g @commitlint/cli @commitlint/config-conventional
echo "module.exports = {extends: ['@commitlint/config-conventional']}" > commitlint.config.js
```

## Pitfalls
- **72-char body wrap**: Vim wraps automatically; in VS Code use `editor.rulers: [72]`
- **Scope granularity**: Too narrow (`src/utils/date.ts`) or too broad (`core`) — use module level
- **Footnotes vs body**: Put issue refs and breaking changes in footer, not body
- **Rebase rewrites dates**: Use `--date` flag if author date matters

## Verification
```bash
git log --oneline --format="%C(auto)%h %s" -10
git log --oneline --grep="^feat\|^fix" --since="1 week" # Changelog preview
```
