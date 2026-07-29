---
name: skill-combination-techniques
description: Stack and chain multiple skills for complex tasks.
---

# Skill Combination Techniques

**Trigger**: Use when a task requires expertise from multiple domains and needs multiple skills working together.

## When to Combine Skills

```markdown
COMBINE skills when:
- Task spans multiple domains (e.g., deploy + monitor + alert)
- Task has multiple phases (build → test → deploy)
- The skill references "Connected Skills" in its body

DON'T COMBINE when:
- One skill fully covers the task
- Skills overlap significantly (redundant)
- Combining would exceed context budget
```

## Combination Patterns

### 1. Sequential Chain (most common)
```
Phase 1: /github-actions-workflows    → Create CI pipeline
Phase 2: /dockerfile-optimization     → Optimize Docker build
Phase 3: /kubernetes-deployment       → Deploy to k8s
```
Each phase completes before the next loads. Spread across turns.

### 2. Parallel Stack (loaded together)
```
/docker-compose-patterns /github-actions-workflows /secrets-management
```
All needed simultaneously. Max 5 per stack.

### 3. Nested (skill within a skill)
```
Primary: /webapp-penetration-testing
  ├── Sub: /sql-injection-exploitation
  └── Sub: /api-testing-contracts
```
Load primary first. Only load sub-skills when you reach that section.

### 4. Fallback Chain
```
Primary:  /docker-compose-migration    → Latest approach
Fallback: /docker-compose-patterns    → Alternative if primary fails
```

## The Stack Command

```markdown
# Up to 5 leading /skill tokens, rest is instruction
/github-pr-workflow /test-driven-development fix issue #123

# Bundles are better for permanent combos
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development
```

## Skill Handoff Protocol

When transitioning between skills in a chain:

1. **ANNOUNCE**: "Now using <next-skill> for <next-phase>"
2. **SUMMARIZE** what previous skill accomplished
3. **LOAD** next skill only when needed
4. **PASS context** between skills

```
Example:
"Using github-actions-workflows, I've set up the CI pipeline.
Now loading dockerfile-optimization for the Docker build step..."
```

## Connected Skills

When a skill lists "Connected Skills", load them only when you reach that subsection:

```
## Connected Skills
`dockerfile-optimization`, `helm-chart-development`, `prometheus-metrics`

Strategy:
1. Load kubernetes-deployment first
2. At "Build container" → load dockerfile-optimization
3. At "Deploy with Helm" → load helm-chart-development
4. At "Set up monitoring" → load prometheus-metrics
```

## Pitfalls
- **Premature loading**: Loading all phase skills upfront wastes context
- **Handoff failure**: Starting new skill without communicating what old skill did
- **Over-stacking**: >5 skills in one message — Hermes caps at 5
- **Bundle vs stack**: Same combo 3+ times → create a bundle instead

## Verification
```markdown
After multi-skill task:
- Did each skill add unique value?
- Was there overlap?
- Would a bundle be better next time?
```
