---
name: skill-catalog-navigation
description: Browse and search 1,000+ skills to find what you need.
---

# Skill Catalog Navigation

**Trigger**: Use when you need to find a skill in a large catalog and don't want to scan all 1,000+ descriptions.

## Search Methods Ranked by Speed

| Method | Speed | Tokens | Best for |
|--------|-------|--------|----------|
| skills_list() full scan | Fast | ~3K | Full first-time scan |
| Category scan | Fast | ~300 | Known domain |
| `/skill` partial match | Instant | 0 | Known name |
| hermes skills search | Fast | variable | External search |
| Keyword matching | Manual | varies | Specific tool name |

## Step 1: Narrow by Category

```markdown
From skills_list(), note the category of each skill:

  docker/              → Docker containers, compose
  networking/          → Firewalls, VPN, DNS, pentesting
  mlops/               → ML training, evaluation, inference
  github-repository/   → GitHub repo settings, templates
  github-actions/      → CI/CD workflows, secrets, caching
  git-fundamentals/    → Branching, merges, rebase, stash
  skill-meta/          → Skills ABOUT skills (this category)
  
If you need "deploy to k8s" → check docker/ or software-development/
If you need "CI pipeline" → check github-actions/
If you need "choose a skill" → check skill-meta/
```

## Step 2: Scan Descriptions in Category

```markdown
Category: github-actions/     (~6 skills)
  github-actions-workflows    "Author CI/CD workflows..."
  github-actions-secrets      "Manage secrets..."
  github-actions-caching      "Cache dependencies..."
  github-actions-matrix       "Run test combos..."
  github-actions-reusable     "Share workflows..."
  github-actions-oidc         "Authenticate via OIDC..."

→ The one I need: github-actions-workflows
```

## Step 3: Partial Name Matching

```markdown
# Known part of the name → use it
/k8s → no match (no skill starts with "k8s")
/kubernetes → kubernetes-deployment, kubernetes-pod-design
/git- → multiple results

# Skill names: lowercase, hyphens, no spaces.
```

## Step 4: The Fast-Select Method

```markdown
When you need a skill quickly:

1. CALL skills_list() once (3K tokens)
2. MENTALLY FILTER descriptions for trigger keywords
3. As soon as one matches → load it with skill_view()

This should take ~2 seconds.
```

## When You Can't Find It

```markdown
If skills_list() doesn't reveal a match:

1. Try SYNONYMS
   - "deploy" → "release", "ship", "publish"
   - "debug" → "troubleshoot", "diagnose"
   - "config" → "setup", "configuration"

2. Try BROADER categories
   - "connect to Postgres" → all database skills
   - "OAuth login" → all auth skills

3. Search by TECHNOLOGY not task
   - "deploy with Helm" → check "helm" skills
   - "build with esbuild" → check bundler skills

4. Accept no match → general knowledge or flag as gap
```

## Pitfalls
- **Description-only blindness**: "git-workflow-optimization" might help with CI — don't judge by name alone
- **Category misplacement**: Some skills are in surprising categories — check broadly
- **Scanning fatigue**: 100+ descriptions blend together — take mental breaks

## Verification
```markdown
After finding a skill:
- Does it match my task?
- How long did the search take?
- Could I have found it faster?
```
