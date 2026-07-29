---
name: skill-relevance-scoring
description: Score and rank skills by relevance to the current task.
---

# Skill Relevance Scoring

**Trigger**: Use when multiple skills could match a task and you need to pick the best one(s) without loading them all.

## Scoring Dimensions

Score each candidate skill from 0-10 on these axes:

| Dimension | What it measures | Weight |
|-----------|-----------------|--------|
| **Semantic match** | How closely the skill name/description matches the task | 3x |
| **Trigger alignment** | Whether the skill's trigger condition matches | 3x |
| **Domain overlap** | Category of skill matches task domain | 2x |
| **Technology match** | Tags, framework, or library matches | 2x |
| **Task type match** | Debugging, deploying, creating, analyzing | 1x |
| **Complexity fit** | Skill complexity aligns with task complexity | 1x |

## Scoring Algorithm

```markdown
Total Score = (semantic × 3) + (trigger × 3) + (domain × 2) 
            + (tech × 2) + (task_type × 1) + (complexity × 1)

MAX = 120

RANKING:
  90-120: EXACT MATCH — load immediately
  60-89:  STRONG MATCH — load if no exact match exists  
  30-59:  WEAK MATCH — load only for complex tasks
  0-29:   NO MATCH — don't load
```

## Real-World Example

**Task:** "Set up a CI pipeline that runs tests on PRs for my Python project"

Scanning skills_list():

| Skill | Semantic | Trigger | Domain | Tech | Type | Total |
|-------|----------|---------|--------|------|------|-------|
| **github-actions-workflows** | 10 | 9 | 10 | 8 | 10 | **108** ✅ |
| **ci-cd-pipeline-setup** | 9 | 8 | 9 | 7 | 9 | **98** ✅ |
| **github-actions-secrets** | 5 | 3 | 7 | 4 | 4 | **55** ❓ |
| **python-testing-advanced** | 4 | 2 | 3 | 7 | 3 | **42** ❌ |
| **docker-compose-patterns** | 1 | 1 | 2 | 2 | 2 | **16** ❌ |

**Decision:** Load `github-actions-workflows` (108) + `ci-cd-pipeline-setup` (98). Skip the rest.

## Description Scanning Heuristics

When reading skill descriptions (from skills_list), look for:
1. **Action verbs** in the description: "Use when deploying..." → task is deployment
2. **Technology names**: "docker", "kubernetes", "fastapi", "react"
3. **Process nouns**: "migration", "debugging", "optimization", "testing"
4. **Exclusions**: "without X" / "not for Y" — inverse matches

## Quick Ranking (Low-Token Version)

```markdown
When you have very limited context, use this abbreviated flow:

1. Read ALL skill descriptions once (skills_list = ~3K tokens)
2. Pick the TOP 3 that seem relevant
3. Load their full content with skill_view()
4. If the first one fits perfectly — stop there
5. If not — load the next one

Never load more than 5 skills for a single task.
```

## Pitfalls
- **Over-scoring popular skills**: "python" skills score highly on any Python task even when inappropriate
- **Missing cross-domain skills**: A networking task might benefit from a security skill — scoring can miss this
- **Score anchoring**: The first high-scoring skill you see should not prevent considering combinations
- **Description quality**: A poorly described skill may be more useful than its score suggests — consider loading if category matches

## Verification
```markdown
After loading your top-scoring skill, answer:
- Does the first step actually address my task?
- If not, which other skill from my ranked list should I try next?
```
