---
name: git-hooks-workflow
description: Automate checks with client-side git hooks.
---

# Git Hooks Workflow

**Trigger**: Use when setting up pre-commit checks, commit message validation, or any git lifecycle automation.

## Hook Types

| Hook | Trigger | Use case |
|------|---------|----------|
| `pre-commit` | Before commit message | Lint, format, check secrets |
| `prepare-commit-msg` | Before editor opens | Add template, prefix branch name |
| `commit-msg` | After message written | Validate format, check length |
| `post-commit` | After commit created | Notify, update logs |
| `pre-push` | Before push | Run tests, check build |
| `pre-rebase` | Before rebase | Prevent rebase on protected branches |
| `post-checkout` | After checkout | Restore dependencies |
| `post-merge` | After merge | Install new dependencies |
| `post-rewrite` | After rebase/amend | Update metadata |

## Setup

```bash
# Hooks live in .git/hooks/ — need to be executable
touch .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Essential Hook Examples

### 1. pre-commit — Prevent Secrets
```bash
#!/bin/sh
# .git/hooks/pre-commit — prevents committing secrets
if git diff --cached | grep -E "(API_KEY|SECRET|PASSWORD|-----BEGIN)" >/dev/null; then
    echo "ERROR: Potential secret detected in staged changes!"
    exit 1
fi
```

### 2. pre-commit — Format Code
```bash
#!/bin/sh
# Run formatter on staged files
STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep '\.py$')
if [ -n "$STAGED" ]; then
    ruff check --fix $STAGED
    git add $STAGED
fi
```

### 3. commit-msg — Validate Conventional Commits
```bash
#!/bin/sh
# .git/hooks/commit-msg
COMMIT_MSG=$(cat "$1")
if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?:.{1,}"; then
    echo "ERROR: Commit message must follow Conventional Commits format"
    echo "  feat(scope): description"
    exit 1
fi
```

### 4. pre-push — Run Tests
```bash
#!/bin/sh
# .git/hooks/pre-push — run tests before pushing
echo "Running tests before push..."
if ! cargo test --quiet 2>/dev/null && ! pytest -q 2>/dev/null; then
    echo "ERROR: Tests failed — push aborted"
    exit 1
fi
```

## Using Pre-commit Framework

```bash
# Install pre-commit (Python)
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.2.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
EOF

# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run trailing-whitespace
```

## Sharing Hooks with the Team

```bash
# Store hooks in the repo
mkdir -p .githooks
mv .git/hooks/pre-commit .githooks/

# Configure git to use custom hooks path
git config core.hooksPath .githooks

# Or commit a setup script
```

## Pitfalls
- **Skipping hooks**: `git commit --no-verify` / `-n` bypasses pre-commit and commit-msg hooks
- **Performance**: Heavy hooks (linters on large files) slow down every commit
- **Hook path config**: `core.hooksPath` is a git config, not committed — team members must opt in
- **Non-zero exit**: Any hook that exits non-zero aborts the operation
- **pre-commit Python dependency**: Team needs Python + pre-commit installed, or use hooks written in shell

## Verification
```bash
git config core.hooksPath   # Check hook path
ls .githooks/               # List active hooks
pre-commit run --all-files  # Test all hooks on everything
```
