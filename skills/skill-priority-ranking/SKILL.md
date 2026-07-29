---
name: skill-priority-ranking
description: Rank which skills to load first in constrained contexts.
---

# Skill Priority Ranking

**Trigger**: Use when you can only load 1-3 skills due to context limits and need to pick the most impactful ones.

## Priority Levels

```markdown
TIER 1 — CRITICAL (load first):
- Skills that contain step-by-step procedures
- Skills with exact commands you can't guess
- Skills for operations that are error-prone or destructive

TIER 2 — IMPORTANT (load if room):
- Skills with configuration templates
- Skills that list pitfalls and edge cases
- Skills for operations you're less familiar with

TIER 3 — NICE TO HAVE (load only if simple):
- Reference/background information
- Alternative approaches
- Verification steps (can often be derived)
```

## The Value-Per-Token Metric

```markdown
VALUE = (steps_count × 2) + (commands_count × 3) + (pitfalls_count × 2)
        - (explanatory_paragraphs × 1)

COST = skill_view() output tokens

EFFICIENCY = VALUE / COST

Load high-efficiency skills first. Skip low-efficiency ones.

Example:
  Skill A: 8 steps, 12 commands, 5 pitfalls, 2 paragraphs
    VALUE = 16 + 36 + 10 - 2 = 60
    COST  = ~1200 tokens
    EFFICIENCY = 0.05

  Skill B: 3 steps, 2 commands, 0 pitfalls, 10 paragraphs
    VALUE = 6 + 6 + 0 - 10 = 2
    COST  = ~800 tokens
    EFFICIENCY = 0.0025

  → Load skill A (20x more value per token)
```

## Context-Constrained Ranking

For a 32K model with ~6K skill budget:

```markdown
Choose 2-3 of the highest priority:

Priority  │ Skill                        │ Why
──────────┼──────────────────────────────┼──────────────────
1st       │ github-actions-workflows     │ Core procedure, has YAML templates
2nd       │ github-actions-secrets       │ Direct dependency (needed in workflow)
3rd       │ github-actions-caching       │ Nice-to-have optimization, skip if tight
4th       │ dockerfile-optimization      │ Different domain, load later when needed
```

## Priority by Task Type

| Task type | Load first | Load second | Skip unless needed |
|-----------|-----------|-------------|-------------------|
| **Build & deploy** | CI/CD workflow | Dockerfile optimization | Monitoring config |
| **Debugging** | Systematic debugging | Error tracking setup | Git bisect |
| **API design** | API design patterns | OpenAPI spec | API testing |
| **Database** | Schema design | Migration patterns | Query optimization |
| **Security** | Security audit | Vulnerability scanning | WAF config |

## Priority Decay Over Time

```markdown
Skills lose priority as you gain experience:

SESSION 1:
  └─ python-package-build        HIGH (never done this)

SESSION 5:
  └─ python-package-build        SKIP (know the procedure)
  └─ github-actions-workflows    HIGH (still learning CI)

SESSION 20:
  └─ most build skills           SKIP (routine)
  └─ kubernetes-deployment       MED (do this monthly)
```

## Pitfalls
- **Unknown unknowns**: A skill you'd rate "nice to have" might contain a critical pitfall — scan the trigger/description before deciding
- **Priority ≠ quality**: A high-priority skill might be poorly written — low value despite high ranking
- **Over-optimization**: Spending 5 minutes ranking skills for a 2-minute task is net negative
- **Static ranking**: A skill's priority shifts as the task evolves — re-evaluate at each phase

## Verification
```markdown
After loading top-priority skills:
- Did I miss a critical piece of info that a skipped skill would have provided?
- Would any token I saved have been better spent on one more skill?
```
