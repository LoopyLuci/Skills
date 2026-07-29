---
name: git-ignore-patterns
description: Write effective .gitignore files to keep repos clean.
---

# Git Ignore Patterns

**Trigger**: Use when creating a .gitignore file, excluding generated files, or keeping secrets out of version control.

## Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `file.txt` | Specific file anywhere | `config.local.json` |
| `/file.txt` | File only in repo root | `/secret.key` |
| `dir/` | Directory anywhere | `node_modules/` |
| `/dir/` | Directory only in root | `/build/` |
| `*.log` | All files with extension | `debug.log`, `error.log` |
| `**/temp` | Nested directories | `src/a/temp`, `src/a/b/temp` |
| `!important.log` | Negation (re-include) | Track `important.log` while ignoring others |
| `name?.txt` | Single char wildcard | `name1.txt`, `nameA.txt` |
| `name[0-9].txt` | Char range | `name5.txt` |

## By Language / Framework

### Node.js
```gitignore
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnp.*
.yarn/
.env
.env.*.local
dist/
coverage/
*.tsbuildinfo
```

### Python
```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.env
venv/
.venv/
env/
*.egg-info/
dist/
build/
*.egg
.coverage
htmlcov/
.tox/
.mypy_cache/
.ruff_cache/
.pytest_cache/
```

### Rust
```gitignore
/target/
**/*.rs.bk
Cargo.lock      # Uncomment if library (not binary)
.env
```

### Go
```gitignore
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
/target
/vendor/        # Unless using vendoring
```

### Java / JVM
```gitignore
*.class
*.jar
*.war
*.nar
target/
build/
.gradle/
!gradle/wrapper/gradle-wrapper.jar
.idea/
*.iml
*.ipr
*.iws
.settings/
.project
.classpath
```

## Universal Patterns

```gitignore
# OS files
.DS_Store
Thumbs.db
Desktop.ini
*.swp
*.swo
*~
*.orig

# IDE
.idea/
.vscode/
*.sublime-*
*.sublime-workspace
.project
.classpath
.settings/

# Secrets (NEVER commit these)
.env
.env.*
*.pem
*.key
*.p12
*.pfx
secrets.*
config/credentials.*

# Dependencies
vendor/
node_modules/
packages/

# Build output
dist/
build/
out/
*.tsbuildinfo

# Logs
*.log
logs/

# Temp files
*.tmp
*.temp
.cache/
```

## Template Generator

```bash
# Using GitHub's API (lists templates by platform)
curl -s https://www.toptal.com/developers/gitignore/api/python,node,rust

# Or use gh:
gh api repos/github/gitignore/contents/Python.gitignore --jq '.content' | base64 -d
```

## Global .gitignore (personal exclusions)

```bash
# Create a global gitignore for your editor & OS
git config --global core.excludesFile ~/.gitignore_global
echo ".DS_Store" >> ~/.gitignore_global
echo "*.swp" >> ~/.gitignore_global
```

## Verification

```bash
# Check what would be ignored
git check-ignore -v path/to/file

# Show all ignored files
git status --ignored

# List gitignore rules affecting a file
git check-ignore -v node_modules/package.json

# Test if .gitignore rules work correctly
touch test-ignore-file.tmp
git check-ignore test-ignore-file.tmp  # Should output the filename
rm test-ignore-file.tmp
```

## Pitfalls
- **Already tracked files**: `.gitignore` does NOT affect tracked files — use `git rm --cached` to untrack
- **Negation order**: Later patterns override earlier ones — `!` must come after the rule it negates
- **Nested .gitignores**: Child directories' `.gitignore` overrides parent's
- **Pattern anchoring**: Leading `/` anchors to repo root, no leading `/` matches anywhere
- **`.gitignore` vs `.git/info/exclude`**: Both work; `exclude` is local-only (not shared)

## Verification
```bash
# Run through all rules
git check-ignore -v somefile.ext

# List every ignore rule affecting current directory
git check-ignore $(find . -maxdepth 3 -type f | head -50) 2>/dev/null
```
