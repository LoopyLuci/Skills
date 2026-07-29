---
name: skill-context-budget
description: Manage context window usage across multiple loaded skills.
---

# Skill Context Budget

**Trigger**: Use when deciding how many skills to load, considering limited context window and competing demands for tokens.

## The Context Budget Equation

```
Total context = model max (e.g., 128K tokens)

Reserved (fixed):
  System prompt       ~5K tokens
  Conversation history ~varies by turn count
  Tool outputs        ~varies by task
  Current user input  ~0.5-2K

Available for skills:
  = Total - Reserved - Future(+history growth per turn)

RULE OF THUMB:
  Skills should use ≤ 30% of total context budget.
  After 30%, response quality degrades noticeably.
```

## Budget by Model

| Model context | Skill budget | Max skills |
|-------------|-------------|------------|
| 8K (small) | ~800 tokens | 0-1 skills |
| 16K (medium) | ~2,500 tokens | 1-2 skills |
| 32K | ~6,000 tokens | 3-4 skills |
| 64K | ~15,000 tokens | 4-6 skills |
| 128K+ | ~30,000 tokens | 5-8 skills |

## Real-Time Budget Tracking

```markdown
Before each skill_view() call, track running budget:

Current state:
  Skills loaded:    2 (4.2K tokens)
  Conversation:     12 turns (~8K tokens)  
  System:           ~5K tokens
  Tool outputs:     ~2K tokens
  ──────────────────────────
  Total used:       ~19.2K / 128K (15%)
  Remaining budget: ~30K tokens for skills + future turns

Decision: Can safely load 1 more skill.
```

## High-Density Skills (Best Token Value)

```markdown
Some skills pack more value per token than others:

HIGH DENSITY (load first):
  - Step-by-step procedures with exact commands
  - Configuration templates with all options
  - Decision trees and tables

LOW DENSITY (load last, or skip):
  - Background explanations and theory
  - Extensive reference documentation
  - Multiple examples of the same pattern
```

## The 2-Skill Default

```markdown
Unless you have a specific reason to load more:

LOAD NO MORE THAN 2 SKILLS by default.
This covers 90% of tasks and leaves room for:
- Conversation growth (10+ more turns)
- Tool outputs (file contents, command output)
- Future skill loading if needed

Exceptions:
- Complex deployment with 3+ phases → 3-4 skills
- Research/synthesis tasks → 3-5 skills
- Simple/well-known tasks → 0-1 skills
```

## Releasing Skills (Context Management)

```markdown
Once a skill's purpose is served, you can effectively "release" it:

1. ✅ STOP referencing the skill's instructions
2. ✅ Let the conversation move to new topics
3. ✅ The old skill's tokens remain in context but stop directing behavior

Skills release naturally through:
- Turn progression (old content scrolls out of active attention)
- Topic shifts (new skill's instructions override old ones)
- Task completion (no need to mention the skill anymore)
```

## Pitfalls
- **Holding onto outdated skills**: A skill loaded 20 turns ago for a different task is still consuming budget — stop referencing it
- **Skill loading during tool calls**: Loading skills inside `execute_code` can double-count — load at the agent level
- **Overestimating 128K**: Even with 128K context, skill loading at 50% leaves only 64K for conversation — fills fast
- **The "just one more" trap**: "I'll load just one more skill" repeated 5 times → 30K tokens in skills

## Verification
```markdown
Before each load, ask:
- What will I REMOVE from context to make room for this skill?
- Is this skill worth more than 2 additional conversation turns?
- Am I loading this because I need it, or because it exists?
```
