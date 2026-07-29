---
name: skill-fallback-strategy
description: Recover when no skill matches or the loaded one fails.
---

# Skill Fallback Strategy

**Trigger**: Use when no skill seems to match the current task, the loaded skill's instructions don't work, or you need an alternative approach.

## Fallback Decision Tree

```
Loaded skill not working?
        │
   ┌────▼─────────┐
   │ Steps unclear?│──YES──► Load reference files for detail
   └────┬─────────┘
        │ NO
   ┌────▼─────────┐
   │ Commands     │──YES──► General knowledge, same goal
   │ outdated?    │
   └────┬─────────┘
        │ NO
   ┌────▼──────────┐
   │ Wrong track?  │──YES──► Try a different approach
   └────┬──────────┘
        │ NO
   ┌────▼──────────┐
   │ Wrong skill?  │──YES──► Score and load next best
   └────┬──────────┘
        │ Still stuck
   ┌────▼──────────────┐
   │ General knowledge │──► Rely on base capabilities
   └───────────────────┘
```

## Fallback Levels

| Level | What to do | Token cost |
|-------|-----------|------------|
| L1 | Re-read skill reference files | ~1K |
| L2 | General knowledge with skill's approach | 0 |
| L3 | Load sibling skill in same category | ~1-2K |
| L4 | Load general skill (e.g., systematic-debugging) | ~1K |
| L5 | Base knowledge, note gap for creation | 0 |

## Real-World Examples

### Commands Outdated
```
Loaded: docker-compose-patterns
Issue:  `docker-compose` is deprecated — `docker compose` needed
Action: L2 — Adjust commands on the fly
Result: Skill structure still useful, adjusted syntax
```

### Wrong Version
```
Loaded: django-rest-framework-apis
Issue:  Skill covers DRF v3, project uses DRF v4
Action: L3 — Load fastapi-api-development instead
Result: Better match for actual stack
```

### No Skill Exists
```
Task:  "Set up RabbitMQ cluster with mirroring"
Search: No skill found for "rabbitmq" or "message-broker"
Action: L5 — General knowledge, mark as gap
```

## When to Give Up

```markdown
Evaluate after 3 attempts:
1. Failed? → Re-read instructions carefully
2. Failed again? → Check if applying correctly
3. Failed third time? → Skill is wrong/outdated — switch

Abandon a mismatched skill early rather than forcing it.
Token cost is already sunk — don't compound the loss.
```

## Pitfalls
- **Skill quality variance**: A skill might exist but be poorly written
- **False confidence**: Loading a skill can make you overconfident — verify commands
- **Update lag**: Skills for rapidly changing tools can be outdated
- **Sunk cost**: "I already loaded this, I should use it" — drop it if it doesn't fit

## Verification
```markdown
After fallback:
- Did the alternative work?
- Should the skill be patched?
- Is a new skill needed for this gap?
```
