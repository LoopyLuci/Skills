---
name: skill-awareness-self-assessment
description: Check if a relevant skill exists before starting a task.
---

# Skill Awareness & Self-Assessment

**Trigger**: Use at the start of any task to assess whether a relevant skill exists, before diving into implementation.

## The Awareness Check (5 seconds)

```markdown
Every time you receive a request, run this quick check:

1. Do I recognize this task type?
2. Is there a skill name that matches?
3. Have I done this before in this session?
4. Can I confidently answer without a skill?

If YES to #4 → proceed.
If YES to #2 → load the skill.
If NO to all → request clarification or note as gap.
```

## Skill Existence Check

```markdown
When you think "I know how to do this, I don't need a skill":

PAUSE and ask:
- Do I know the EXACT commands?
- Do I know the CORRECT order of operations?
- Do I know the PITFALLS to watch for?
- Is this a procedure I follow often?

If you hesitated on any → there's probably a skill for this.
Load it. It will save tokens vs. figuring it out from scratch.
```

## The Confidence Assessment

```markdown
Rate your confidence before loading a skill:

TOPIC          CONFIDENCE (1-5)  ACTION
Dockerfiles        5              Optional (you know it)
Kubernetes YAML    2              REQUIRED (load skill)
Helm charts        1              REQUIRED (load skill)
Monitoring setup   1              REQUIRED (load skill)

If any topic scores ≤3, load the corresponding skill.
```

## Recognizing Blind Spots

```markdown
Situations where you think you don't need a skill but actually do:

1. "It's just X" — "It's just a simple Dockerfile" → has pitfalls
2. "I always do it this way" — Your approach might be outdated
3. "The docs are easy to find" — But skill has them pre-curated
4. "I'll figure it out" — Will cost 5x more tokens than loading

When in doubt, load the skill. ~1K tokens to load vs. 
potentially 10K+ tokens of trial and error.
```

## Validation After Loading

```markdown
After loading a skill, validate your choice:

✅ PASS: Steps directly address the task
✅ PASS: Commands match what you expected
✅ PASS: You see how to apply it immediately

❌ FAIL: Skill talks about a different version
❌ FAIL: Approach doesn't apply to your context
❌ FAIL: Skill is for a different tool/platform

If FAIL → stop referencing it, try the next candidate.
```

## Pitfalls
- **False confidence from familiarity**: Familiar topic ≠ knowing the exact procedure
- **Tunnel vision**: Loading ONE skill and ignoring others when task has multiple facets
- **Over-reliance**: Skills are aids — if you genuinely know it, proceed confidently
- **Session drift**: A skill loaded 50 turns ago may still influence you — reassess

## Verification
```markdown
At task end, answer:
- Did I use the right skills?
- Did I miss any I should have loaded?
- Did I load any I didn't need?
```
