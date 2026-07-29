---
name: skill-loading-strategy
description: Progressively load skills to minimize context token waste.
---

# Skill Loading Strategy

**Trigger**: Use when deciding whether to load a skill's full content or just its description, and how many skills to load at once.

## The Token Budget Problem

```
skills_list()        → ~3,000 tokens  (all 1,000+ skill descriptions)
skill_view(name)     → ~200-2,000 tokens per skill (full content)
5× skill_view()      → ~1,000-10,000 tokens

With a 128K model: skills could consume 10-20% of context.
With lower models: skills could consume 50%+ — use sparingly.
```

## Progressive Loading Strategy

```
Level 0: skills_list()           
  See all names + descriptions. Pick candidates.
  Cost: ~3K tokens (one-time, early in session)

Level 1: skill_view(name)        
  Load one skill's full content.
  Cost: ~0.2-2K tokens per load

Level 2: skill_view(name, path)  
  Load a specific reference file from a skill.
  Cost: ~0.5-2K tokens (only when needed)

Level 3: /skill-name arguments   
  Stack with slash command in next turn.
  Cost: 0 tokens now — loaded on next turn
```

## When to Stop Loading

```markdown
# STOP loading and START executing when:
1. The loaded skill covers the FIRST STEP of the task
2. You have enough context to produce a reasonable answer
3. The next skill to load would be "nice to have" not "need to have"

# CONTINUE loading when:
1. The task requires MULTIPLE specialized domains
2. The loaded skill explicitly references another skill (→ Connected Skills section)
3. You've tried the skill and it's not working — need a different approach
```

## Loading Order (Highest Impact First)

```markdown
Load skills in this priority order:

1. PROCESS skills — step-by-step guides (highest value per token)
2. COMMAND skills — exact commands and configurations  
3. REFERENCE skills — background info, explanations (lowest value)
4. VERIFICATION skills — only after completing the task

Example: For "deploy a Kubernetes app":
  HIGH: kubernetes-deployment (has the yaml + commands) 
  MED:  dockerfile-optimization (if building custom images)
  LOW:  kubernetes-pod-design (reference — only if needed)
```

## Lazy Loading Pattern

```markdown
# Instead of pre-loading 5 skills, try this:

1. Load the MOST LIKELY skill (your best guess)
2. Follow its instructions
3. If/when you hit a sub-task that needs another skill — load it then
4. Proceed with the new instructions
5. Repeat until task is done

This spreads skill loading across multiple turns instead of 
front-loading 10K tokens of unused content.
```

## Context Window Budget by Model Size

| Model context | Max skills to load | Notes |
|-------------|-------------------|-------|
| 8K | 1-2 | Load only the single best skill |
| 16K | 2-3 | One main + one backup |
| 32K | 3-4 | Main + supporting + reference |
| 64K | 4-5 | Full stack — all relevant |
| 128K+ | 5-7 | Can afford depth, but don't waste it |

## Pitfalls
- **Premature loading**: Loading Level 2 (reference files) before Level 1 (main content) wastes context
- **Duplicate loading**: Loading the same skill twice in a session — check if it's already in context
- **Orphaned references**: Loading a reference file from a skill whose main content you haven't loaded
- **Sunk cost**: Loading 3 skills then realizing none match — drop them despite the token investment

## Verification
```markdown
Before each skill_view() call, ask:
- Does this task DEFINITELY need this skill?
- Can I make progress with just the description?
- Would waiting until I need it save tokens?
```
