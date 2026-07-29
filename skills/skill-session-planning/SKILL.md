---
name: skill-session-planning
description: Plan which skills to load before starting complex tasks.
---

# Skill Session Planning

**Trigger**: Use before starting a complex multi-step task that spans multiple domains or needs multiple tools.

## Pre-Task Planning Flow

```markdown
BEFORE you start the task:

1. DECOMPOSE the request into phases
2. MAP each phase to a skill (if one exists)
3. IDENTIFY dependencies between phases
4. PLAN the loading order
5. EXECUTE — load first skill, begin
```

## Planning Template

```markdown
Task: <brief description>

Phase  | Skill              | When to load       | Priority
-------|--------------------|--------------------|----------
1. Init| scaffolding        | Now                | HIGH
2. Code| test-driven-work   | After scaffold done| HIGH
3. Test| python-testing-add | When writing tests | MED
4. CI  | github-actions-wf  | Before commit      | HIGH
5. Doc | technical-writing  | After code         | LOW
```

## Decomposition Example

**Request:** "Create a FastAPI backend with auth, containerize it, set up CI/CD, and deploy to k8s"

```markdown
Phase 1: Scaffold — fastapi-api-development
Phase 2: Auth — oauth-authentication-patterns
Phase 3: Container — dockerfile-optimization
Phase 4: CI/CD — github-actions-workflows
Phase 5: Deploy — kubernetes-deployment, helm-chart-development
Phase 6: Monitor — prometheus-metrics-collection
```

## Dependency-Driven Ordering

```markdown
Skills often depend on each other:
- dockerfile-optimization depends on the app existing (Phase 1-2 done)
- kubernetes-deployment depends on the image existing (Phase 3 done)
- github-actions-workflows can be done in parallel with Phases 3-5

CORRECT ORDER:
1. fastapi-api-development (no deps)
2. oauth-authentication-patterns (no deps)
3. dockerfile-optimization (depends on 1+2)
4. kubernetes-deployment (depends on 3)
5. github-actions-workflows (parallel to 3-5)
6. prometheus-metrics-collection (after 4)

WRONG ORDER:
1. kubernetes-deployment (image doesn't exist yet)
2. dockerfile-optimization (no app yet)
```

## Active Plan Tracking

```markdown
During execution, track progress:

✅ Complete: scaffolding
▶️  In progress: auth implementation
⏳ Pending: containerization
⏳ Pending: CI/CD
⏳ Pending: deployment

Current skill: oauth-authentication-patterns
Next to load: dockerfile-optimization (after auth done)
```

## When Plans Change

```markdown
Adapt the plan when:
- A skill doesn't exist for a phase → use general knowledge or request creation
- A phase turns out simpler than expected → skip the skill
- A phase reveals unexpected complexity → load sub-skills
- User changes requirements mid-task → re-plan remaining phases
```

## Token Budget Planning

```markdown
For a 5-phase task with 5 skills:

Maximum skill cost: 5 × 2K tokens = 10K tokens
If model is 32K: skills use 31% of context — acceptable
If model is 8K:  skills use 125% — IMPOSSIBLE, must reduce

SOLUTION for small models:
- Only load the NEXT skill's content (lazy load)
- Keep descriptions of future skills in mind (from skills_list)
- Never load more than 2 skills at once
```

## Pitfalls
- **Over-planning**: Planning all 10 phases when the user might stop after phase 2 — plan 2-3 ahead max
- **Rigid adherence**: A plan is a guide, not a contract — adapt when reality differs
- **Missing dependency cycles**: Skill A needs B, B needs A — break the cycle with manual context passing
- **Planning paralysis**: Spending 5 minutes planning a 2-minute task — for simple tasks, use gut check

## Verification
```markdown
Before starting, confirm:
- Do I have a clear first step with a loaded skill?
- Is my next skill dependency-satisfied?
- Is this plan going to fit my context budget?
```
