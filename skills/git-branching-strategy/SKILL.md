---
name: git-branching-strategy
description: Choose and implement a branching strategy for your team.
---

# Git Branching Strategy

**Trigger**: Use when setting up or selecting a git branching model for a project or team.

## Branching Models

### 1. GitHub Flow (simplest — recommended for CI/CD)
```
main ──── feat/a ──────► main
         \── feat/b ──► main
```
- One eternal branch (`main`), short-lived feature branches
- Feature branches merge to `main` via PR
- Deploy from `main` immediately after merge
- Best for: SaaS, continuous deployment, small teams

### 2. Git Flow (structured — releases + hotfixes)
```
main ────► v1.0 ───► v1.1 ───► ...
  \                  ▲
   develop ──► feat ─┘
       \──► release/1.0 ──► main + develop
```
- `main` = production releases only
- `develop` = integration branch
- `feature/` → `develop`, `release/` → `main` + `develop`, `hotfix/` → `main` + `develop`
- Best for: versioned releases, mobile apps, libraries

### 3. Trunk-Based Development (fastest — CI/CD)
```
main ──► short-lived ──► main (commit, not PR)
```
- All developers commit to `main` directly (or very short-lived branches, <1 day)
- Feature flags for incomplete work
- Best for: mature CI/CD, high-trust teams, microservices

### 4. GitLab Flow (environments)
```
main ──► pre/prod ──► production
```
- Environment branches (`staging`, `production`) as deploy targets
- Feature branches → `main` → downstream
- Best for: multiple deployment environments

## Choosing a Model

| Factor | GitHub Flow | Git Flow | Trunk-Based |
|--------|------------|----------|-------------|
| Team size | 1-10 | 5-50 | 1-20 |
| Release cadence | Continuous | Scheduled | Continuous |
| Hotfix urgency | Quick PR | Dedicated branch | Commit + flag |
| Confidence needed | Tests + deploy | Release candidates | Feature flags |

## Setup

```bash
# Protect main branch (replace with your remote)
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --input - <<< '{
    "required_status_checks": {"strict": true, "contexts": ["continuous-integration"]},
    "enforce_admins": true,
    "required_pull_request_reviews": {"required_approving_review_count": 1}
  }'

# Set default branch (if using Git Flow)
git checkout -b develop main
git push origin develop
gh api repos/:owner/:repo --method PATCH \
  --field default_branch=develop
```

## Naming Conventions

```
feature/JIRA-123-short-description   # Feature branches
bugfix/JIRA-456-whats-broken         # Bug fixes
release/v1.2.3                       # Release branches (Git Flow)
hotfix/v1.2.4                        # Critical production fixes
chore/update-deps                    # Maintenance
```

## Pitfalls
- **Mixing models**: Don't combine Git Flow's `develop` with trunk-based commits — pick one
- **Stale long-lived branches**: Set branch lifecycle (auto-delete after merge)
- **Protection rules without CI**: Branch protection is useless without required status checks
- **Release branch drift**: Cherry-pick critical fixes back to `develop`/`main`

## Verification
```bash
git branch -a --merged main    # Check for stale branches
git log --oneline --graph --all --decorate  # Visualize branching health
```
