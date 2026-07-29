---
name: github-templates-community
description: Set up issue/PR templates, CODEOWNERS, and community files.
---

# GitHub Templates & Community Standards

**Trigger**: Use when setting up issue templates, pull request templates, CODEOWNERS, or community health files for a repo.

## Directory Structure

```
.github/
├── ISSUE_TEMPLATE/
│   ├── config.yml               # Template chooser config
│   ├── bug-report.yml           # Bug report form
│   └── feature-request.yml      # Feature request form
├── PULL_REQUEST_TEMPLATE.md     # PR description template
├── CODEOWNERS                   # Auto-review assignment
├── dependabot.yml               # Dependency updates
└── workflows/                   # CI/CD (see github-actions-*)
```

## Issue Templates

### Form Template (YAML — recommended)

`.github/ISSUE_TEMPLATE/bug-report.yml`:
```yaml
name: Bug Report
description: Report a bug to help us improve
title: "[Bug]: "
labels: [bug, triage]
body:
  - type: markdown
    attributes:
      value: Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll to '...'
        4. See error
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Version
      placeholder: "v1.2.3"
  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options: [Windows, macOS, Linux, Other]
```

### Template Chooser

`.github/ISSUE_TEMPLATE/config.yml`:
```yaml
blank_issues_enabled: false
contact_links:
  - name: Security Issue
    url: https://github.com/owner/repo/security/policy
    about: Report security vulnerabilities here
  - name: Discussion
    url: https://github.com/owner/repo/discussions
    about: Ask questions and discuss features
```

## PR Template

`.github/PULL_REQUEST_TEMPLATE.md`:
```markdown
## Description
<!-- Describe your changes in detail -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the project style
- [ ] I have added tests
- [ ] Documentation updated
- [ ] Commits follow conventional commits

Closes #<issue-number>
```

## CODEOWNERS

`.github/CODEOWNERS`:
```text
# Global owners
* @org/core-team

# Specific areas
*.rs @org/rust-team
src/frontend/ @org/frontend-team
/docs/ @org/docs-team

# Security-sensitive files
.github/workflows/ @org/security-team
**/Dockerfile @org/devops

# Build configs
*.config.* @org/devops
```

### Syntax Reference
| Pattern | Assigns | Example |
|---------|---------|---------|
| `*` | Everyone | `* @org/everyone` |
| `*.py` | File extension | `*.py @org/python-team` |
| `/docs/` | Root-level directory | `/docs/ @docs-team` |
| `src/**/tests/` | Nested dirs | `src/**/tests/ @qa-team` |
| `**/secrets/` | Anywhere in repo | `**/secrets/ @security` |

## Community Health Files

Creat repo `.github` (public) — these apply to ALL repos in your org/user:

```
.github/
├── CODE_OF_CONDUCT.md      # Expected behavior
├── CONTRIBUTING.md         # How to contribute
├── SECURITY.md              # Reporting vulnerabilities
├── SUPPORT.md               # Where to get help
└── FUNDING.yml              # Sponsor links
```

### Contributing Guide (quick template)
```markdown
# Contributing

## Getting Started
1. Fork the repo
2. Create a feature branch: `git checkout -b feat/description`
3. Make your changes
4. Run tests: `cargo test`
5. Commit with conventional commits
6. Push and open a PR

## PR Requirements
- All tests pass
- New code has tests
- Commits follow conventional commits
- PR description explains the change
```

## Verification

```bash
# Check community standards
gh repo view --json is_blank_issues_enabled,has_issues,has_projects

# List templates
ls -la .github/ISSUE_TEMPLATE/
gh api repos/:owner/:repo/community/profile -q '.files'  # Community profile

# View CODEOWNERS
# Shows pending reviews on PR
gh pr view <number> --json reviews,reviewsRemaining
```

## Pitfalls
- **CODEOWNERS without branch protection**: CODEOWNERS needs `require_code_owner_reviews` in branch protection to be enforced
- **Blank issues**: Users can bypass forms if `blank_issues_enabled: true`
- **Community profile dotfiles**: Private repos' `.github` doesn't apply to the org — create an org-level `.github` repo
- **Form limits**: GitHub forms don't support dynamic fields or conditional logic
