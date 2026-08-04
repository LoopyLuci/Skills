---
name: dependency-management
description: "Use for dependency management. Audit, update strategies."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, dependencies, packages, vulnerabilities, updates, semver]
    related_skills: [project-setup-scaffolder, code-review-checklist]
---

# Dependency Management

## Overview

Systematic approach to managing project dependencies across languages and ecosystems. Covers vulnerability auditing, license compliance, update strategy (semver analysis, breaking change detection, changelog review), lock file hygiene, dependency pruning, and alternative evaluation. Provides workflows for npm, pip, cargo, go mod, and gem.

## When to Use

- Starting a new project and choosing initial dependencies
- Running a regular dependency audit (weekly/monthly)
- Updating dependencies for a release cycle
- Responding to a critical security advisory
- Reducing dependency count (bloat/pruning)
- Migrating from one library to another
- Upgrading major versions with breaking changes

## Workflow

### Phase 1: Audit for Vulnerabilities

```bash
# Python — pip-audit
pip install pip-audit 2>/dev/null
pip-audit --requirement requirements.txt  # Audit a requirements file
pip-audit --desc  # Include descriptions of vulnerabilities

# Python — Safety CLI
pip install safety 2>/dev/null
safety check --full-report

# Python — pip-licenses (license compliance)
pip install pip-licenses 2>/dev/null
pip-licenses --format=markdown --with-authors  # Generate license table
pip-licenses --allow-only="MIT; Apache-2.0; BSD-3-Clause; BSD-2-Clause; ISC; Python-2.0; Unlicense"

# JavaScript/TypeScript — npm audit
npm audit       # Full report
npm audit --json | jq '.vulnerabilities | to_entries[] | {key, severity, via}'  # Structured

# npm audit fix (careful — only for non-breaking patches)
npm audit fix --dry-run  # Preview before applying
npm audit fix --force    # May include breaking changes

# Rust — cargo audit
cargo install cargo-audit 2>/dev/null
cargo audit                  # Vulnerability report
cargo audit --json | jq '.'  # Structured output

# Go — govulncheck
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...

# Ruby — bundler-audit
gem install bundler-audit
bundler-audit check --update
bundler-audit check --ignore CVE-2023-12345  # Acknowledge known, accepted risk
```

### Phase 2: License Compliance

```bash
# Python — pip-licenses with filtering
pip-licenses --format=json | python3 -c "
import json, sys
licenses = json.load(sys.stdin)
unacceptable = ['GPL-3.0', 'AGPL-3.0', 'BUSL-1.1', 'SSPL-1.0']
for pkg in licenses:
    if pkg['License'] in unacceptable:
        print(f'UNACCEPTABLE: {pkg[\"Name\"]} - {pkg[\"License\"]}')
"

# Node.js — license-checker
npx license-checker --production --onlyAllow "MIT;Apache-2.0;BSD-3-Clause;ISC;Unlicense;CC0-1.0;CC-BY-4.0"

# Node.js — generate LICENSE report
npx license-checker --production --csv --out /tmp/licenses.csv
```

**License compatibility quick reference:**
| Your License | Can include | Cannot include |
|-------------|-------------|----------------|
| MIT | MIT, Apache-2.0, BSD, ISC, Unlicense | GPL, AGPL, SSPL |
| Apache-2.0 | Apache-2.0, MIT, BSD, ISC, Unlicense | GPL v2 (compat issues), SSPL |
| GPL-3.0 | GPL-3.0, MIT, BSD, Apache-2.0 | AGPL, SSPL (if distributing) |
| Commercial | Varies by contract — review carefully | GPL/AGPL (may force source release) |

### Phase 3: Update Strategy (Semver-Aware)

```bash
# ==========================================
# SEMVER RULES
# ==========================================
# MAJOR (1.x → 2.x): Breaking changes — require migration guide
# MINOR (1.1 → 1.2): New features, backward compatible
# PATCH (1.1.0 → 1.1.1): Bug fixes, backward compatible

# ==========================================
# Update strategy by version delta
# ==========================================
# PATCH updates: usually safe, apply automatically in CI
# MINOR updates: review changelog, test, apply
# MAJOR updates: manual migration required, plan separately

# ==========================================
# Check for available updates
# ==========================================
# Python
pip list --outdated --format=columns   # Show all outdated packages
pip list --outdated --format=json | python3 -c "
import json, sys
for pkg in json.load(sys.stdin):
    print(f'{pkg[\"name\"]} {pkg[\"version\"]} -> {pkg[\"latest_version\"]}')
"

# Node.js
npm outdated
npm outdated --json | python3 -c "
import json, sys
deps = json.load(sys.stdin)
for name, info in deps.items():
    print(f'{name} {info[\"current\"]} -> {info[\"wanted\"]} (latest: {info[\"latest\"]})')
"

# Rust
cargo update --dry-run  # Show available updates without applying

# Go
go list -u -m all 2>/dev/null | grep '\['
```

### Phase 4: Breaking Change Detection

```bash
# ==========================================
# Python — Review changelogs & test compatibility
# ==========================================
# Before upgrading a major version:
# 1. Check the package's changelog
curl -s https://pypi.org/pypi/<package>/json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('Latest version:', data['info']['version'])
print('Home page:', data['info']['home_page'])
"

# Check Python version compatibility
# pip install pip-tools
pip-compile --upgrade-package <package> --output-file=/dev/null 2>&1 | head -20

# ==========================================
# Node.js — Breaking changes analyzer
# ==========================================
npm install semver-diff 2>/dev/null
npx npm-check --update --skip-unused  # Interactive dependency updater

# npm-check with major version awareness
npx npm-check --update-all --skip-unused 2>&1 | grep -E "MAJOR|MINOR|PATCH"

# ==========================================
# Rust — Cargo breaking changes detector
# ==========================================
cargo install cargo-outdated
cargo outdated --root-deps-only  # Show only direct dependencies
cargo outdated --exit-code 1     # Exit with code 1 if updates available

# ==========================================
# Generic — Diff the changelog
# ==========================================
# Check if the package has a CHANGELOG, HISTORY, or Release Notes
# Most major packages publish a changelog file or GitHub Releases
# Always read the CHANGELOG through before major upgrades
```

### Phase 5: Lock File Hygiene & Pruning

```bash
# Python — pip
# Clean unused dependencies
pip install pip-tools
pip-compile --upgrade --resolver=backtracking --strip-extras  # Recompile requirements

# Check for dependencies not in requirements.txt but installed
pip freeze | cut -d= -f1 > /tmp/installed.txt
grep -v '^#' requirements.txt | cut -d= -f1 > /tmp/required.txt
comm -23 /tmp/installed.txt /tmp/required.txt  # Extra deps to investigate

# Node.js — npm
npm prune              # Remove extraneous packages
npm dedupe             # Deduplicate packages
rm -rf node_modules && npm install  # Clean install (last resort)

# Check for unused dependencies
npx depcheck           # Find unused dependencies
npx depcheck --ignores="@types/*,eslint-*"  # With ignores

# npm list to analyze dependency tree depth
npm ls --depth=0       # Direct dependencies
npm ls --depth=5       # Full tree (be careful — very long)
npm ls <package>       # Why is this package installed?

# Rust — cargo
cargo install cargo-udeps 2>/dev/null
cargo +nightly udeps  # Find unused dependencies (requires nightly)

cargo install cargo-deny
cargo deny check bans     # Check for duplicate versions
cargo deny check sources  # Check allowed sources (crates.io only?)

# Go
go mod tidy              # Remove unused dependencies
go mod verify            # Verify checksums
```

### Phase 6: Alternative Evaluation Framework

When evaluating whether to add or replace a dependency, use this rubric:

```markdown
| Criterion | Weight | Score (1-5) | Notes |
|-----------|--------|-------------|-------|
| **Maintenance** | 3x | /5 | Last release, commit frequency, issue response time |
| **License** | 3x | /5 | Compatible with project license |
| **API Design** | 2x | /5 | Clean, documented, typed |
| **Performance** | 2x | /5 | Benchmarks vs alternatives |
| **Bundle Size** | 1x | /5 | Footprint relative to value added |
| **Community** | 1x | /5 | Stars, contributors, ecosystem |
| **Security** | 3x | /5 | Past vulnerabilities, response to security issues |
| **Total** | | /105 | Sum of (weight × score) |

Threshold: ≥ 60/105 → Accept, 40-59 → Consider, < 40 → Reject
```

```bash
# Evaluate a package's health
# Python — check PyPI metadata
curl -s https://pypi.org/pypi/<package>/json | python3 -c "
import json, sys
d = json.load(sys.stdin)
i = d['info']
print(f'Package: {i[\"name\"]}')
print(f'Version: {i[\"version\"]}')
print(f'License: {i[\"license\"]}')
print(f'Author: {i[\"author\"]}')
print(f'Python: {i[\"requires_python\"]}')
print(f'Dependencies: {len(i.get(\"requires_dist\", []))}')
print(f'Homepage: {i.get(\"home_page\", \"N/A\")}')
"

# Node.js — check npm metadata
npm view <package> --json 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Version: {d[\"version\"]}')
print(f'License: {d.get(\"license\", \"N/A\")}')
print(f'Dependencies: {len(d.get(\"dependencies\", {}))}')
print(f'Weekly downloads: {d.get(\"downloads\", \"N/A\")}')
print(f'Maintainers: {len(d.get(\"maintainers\", []))}')
"

# GitHub health check
# Stars, issues, PRs, last commit
curl -s https://api.github.com/repos/owner/repo 2>/dev/null | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Stars: {d.get(\"stargazers_count\", \"N/A\")}')
print(f'Forks: {d.get(\"forks_count\", \"N/A\")}')
print(f'Open Issues: {d.get(\"open_issues_count\", \"N/A\")}')
print(f'Last Push: {d.get(\"pushed_at\", \"N/A\")}')
print(f'License: {d.get(\"license\", {}).get(\"spdx_id\", \"N/A\") if d.get(\"license\") else \"N/A\"}')
"
```

### Phase 7: Automated Dependency Update Pipeline

```yaml
# .github/workflows/deps.yml
name: Dependency Management
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6am
  workflow_dispatch:       # Manual trigger

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pip-audit safety pip-licenses
      - run: pip-audit --desc | tee vulnerability_report.txt
      - run: safety check --full-report | tee -a vulnerability_report.txt
      - run: pip-licenses --format=json | python3 check_licenses.py
      - uses: actions/upload-artifact@v4
        with:
          name: dependency-audit
          path: vulnerability_report.txt

  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Automated patch updates
        run: |
          pip install pip-tools
          pip-compile --upgrade --upgrade-package=">=" --resolver=backtracking
      - name: Create PR
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'chore(deps): weekly dependency update'
          title: 'chore: weekly dependency update'
          branch: 'chore/deps-weekly'
          body: |
            Automated dependency update.
            - Patch updates applied automatically
            - Minor/major updates require manual review
```

### Phase 8: Dependency Pruning Process

```bash
# 1. Identify unused dependencies
npx depcheck          # JS/TS
cargo +nightly udeps  # Rust
go mod why <pkg>      # Why is this Go package needed?
python -c "
# Python: check each import from requirements against actual usage
import ast, os, sys
from collections import defaultdict

required = set(line.strip() for line in open('requirements.txt')
              if line.strip() and not line.startswith('#'))
required = set(r.split('==')[0].split('>=')[0].split('<')[0].split('[')[0] for r in required)

imports_found = set()
for root, dirs, files in os.walk('src'):
    for f in files:
        if not f.endswith('.py'):
            continue
        with open(os.path.join(root, f)) as fh:
            try:
                tree = ast.parse(fh.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports_found.add(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports_found.add(node.module.split('.')[0])
            except SyntaxError:
                pass

imports_found.discard('__future__')
print('INSTALLED NOT IMPORTED:', required - imports_found)
print('IMPORTED NOT INSTALLED:', imports_found - required)
"

# 2. Check if removing a dep is safe
git grep -l '<module_name>' -- src/ tests/  # Where is it used?
pip show <package>  # What depends on this?
pipdeptree -p <package>  # Dependency tree showing reverse deps

# 3. If it's genuinely unused:
# - Remove from requirements.txt / pyproject.toml
# - Run full test suite
# - Verify no import errors
# - Commit the removal separately
```

## Common Pitfalls

- **Blind `--upgrade-all`**: Never run `pip install --upgrade` or `npm update` without a lock file and review. Always review changelogs.
- **Not pinning ranges**: Too loose (`*` or no bound) installs incompatible versions. Too tight (`==1.0.0`) prevents security patches. Use `>=X,<Y`.
- **Ignoring transitive dependencies**: A vulnerability in a transitive dep is still a vulnerability. Use tools that audit the full tree.
- **No automated audit schedule**: Dependencies should be audited at least weekly. A manual-only approach misses critical CVEs.
- **Removing deps without testing**: A package might be needed by an obscure code path. Always run full test suite after removal.
- **Mixing dep updates with feature work**: Dependency upgrades should be their own PR with a clear scope. Never bury a dep update in a feature branch.
- **Forgetting dev dependencies**: Only scanning production deps misses build-time and dev-time vulnerabilities. Scan everything.
- **Lock file not committed**: Lock files (requirements.txt, package-lock.json, Cargo.lock) ensure reproducible builds. Always commit them.
- **Not checking Python version compatibility**: A new library version may drop support for your Python version. Check `requires_python` on PyPI.

## Verification Checklist

- [ ] Vulnerability audit run (pip-audit / npm audit / cargo audit / govulncheck)
- [ ] All vulnerabilities addressed (upgraded, mitigated, or acknowledged with ticket)
- [ ] License compliance checked — no incompatible licenses in transitive deps
- [ ] Lock file committed and up-to-date
- [ ] Dependency update strategy documented (policy: patch auto, minor review, major manual)
- [ ] Weekly automated dependency audit scheduled in CI
- [ ] Unused dependencies identified and removed (or ticket created)
- [ ] All dependency versions pinned with safe ranges (`>=X,<Y`)
- [ ] Full test suite passes after any dependency change
- [ ] Breaking changes evaluated via changelog review before major upgrades
- [ ] No duplicate or conflicting dependency versions in the lock file
- [ ] Python version compatibility verified for each dependency
- [ ] Dependency tree reviewed for unnecessary bloat