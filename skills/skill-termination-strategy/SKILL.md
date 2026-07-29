---
name: skill-termination-strategy
description: Decide when to stop using a skill and switch approaches.
---

# Skill Termination Strategy

**Trigger**: Use when you've been working with a skill and need to decide whether to continue, switch, or stop.

## The Continuation Decision

```markdown
Every few turns while using a skill, ask:

1. Is the skill's approach WORKING? 
   → Making progress? Commands succeeding?
   
2. Is the skill still RELEVANT?
   → Did the task evolve away from the skill's domain?
   
3. Is the skill's value DIMINISHING?
   → First steps were valuable, remaining ones are generic?

4. Is the skill CONSUMING too much context?
   → Is it still worth the tokens it's using?
```

## Termination Signals

```markdown
CONTINUE USING SKILL when:
- Steps are still directly applicable
- Commands are working without errors
- You're in the middle of the skill's core procedure

SWITCH SKILLS when:
- Current skill's scope is exhausted
- Task has moved to a new domain
- A connected skill is needed for the next phase

STOP USING SKILL when:
- Task is complete
- Skill's instructions have been fully followed
- Skill was a mismatch (wrong tool/version/platform)
- User explicitly changed the request direction
```

## The 3-Attempt Rule

```markdown
If a skill's instruction fails:

Attempt 1: Follow exactly as written
Attempt 2: Adapt to environment (different OS, version, path)
Attempt 3: Try a fundamentally different approach

After 3 failures → ABANDON the skill's approach.
The skill is either outdated, wrong, or doesn't apply.

Don't try 4, 5, 6 times. The tokens are better spent elsewhere.
```

## Graceful Termination

```markdown
When stopping a skill mid-use, always:

1. DOCUMENT what was accomplished
   "Completed steps 1-3 of the deployment skill:
    - Docker image built
    - Pushed to registry
    - Config files created (not yet applied)"

2. EXPLAIN why you're stopping
   "Stopping here because the deployment method differs
    from what the skill describes (we use Helm, not raw YAML)."

3. PROVIDE the next path
   "Next step: Load helm-chart-development for the actual deploy."
```

## Context Cleanup

```markdown
After terminating a skill, it remains in context.
Mitigate its ongoing influence by:

✅ Clearly stating the transition:
   "Done with dockerfile-optimization. Now loading ..."

✅ Referencing the NEW skill instead:
   "As helm-chart-development explains..."
   (not: "As dockerfile-optimization said earlier but...")

✅ Acknowledging the old skill's work is done:
   "The Dockerfile is ready. From here, the deployment
    follows helm-chart-development instead."
```

## Pitfalls
- **Premature termination**: Abandoning a skill at the first error when the fix is simple
- **Stubborn continuation**: Sticking with a mismatched skill because you already loaded it
- **Silent abandonment**: Switching skills without telling the user or documenting what was done
- **Context pollution**: Old skill's terminology bleeding into the new approach — mind your language

## Verification
```markdown
When you switch skills, verify:
- Did I communicate the transition clearly?
- Is the context (files, state, progress) preserved?
- Is the old skill still influencing my decisions?
```
