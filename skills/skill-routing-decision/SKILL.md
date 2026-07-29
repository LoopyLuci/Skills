---
name: skill-routing-decision
description: Choose the right skill for any task at any moment.
---

# Skill Routing Decision

**Trigger**: Use when you have a task and need to determine which skill(s) to load and whether to load them now.

## Decision Framework

```
User request arrives
        │
   ┌────▼────┐
   │ Does a  │
   │ skill   │──YES──► Load skill via /skill-name or skill_view
   │ match?  │
   └────┬────┘
        │ NO
   ┌────▼────────┐
   │ Multiple    │──YES──► Stack: load the most specific first
   │ skills      │
   │ match?      │
   └────┬────────┘
        │ NO
   ┌────▼────────────┐
   │ Partial match?  │──YES──► Load closest + note gaps
   │ (covers 50%+)   │
   └────┬────────────┘
        │ NO
   ┌────▼──────────┐
   │ General skill │──YES──► Load generic skill (e.g., systematic-debugging)
   │ applicable?   │
   └────┬──────────┘
        │ NO
   └──► No skill needed — proceed with general knowledge
```

## Step 1: Parse the Task

```markdown
# When you receive a request, ask yourself:
1. What domain is this? (networking, ML, git, deployment, creative?)
2. What action is being taken? (create, debug, deploy, analyze, migrate?)
3. What constraints exist? (language, framework, platform, timeline?)
4. Is this a multi-step process that needs multiple skills?
```

## Step 2: Search Skills

```bash
# Quick scan — check categories that match the domain
skills_list()  # See all skill names + descriptions (3K tokens)

# If the task mentions specific tools/technologies:
skill_view("git-merge-conflict-resolution")
skill_view("docker-compose-patterns")

# If the task is complex (5+ steps), load the planning skills first:
skill_view("skill-session-planning")
```

## Step 3: Match Quality Scoring

| Match Level | Description | Action |
|-------------|-------------|--------|
| **Exact** | Skill name matches task verbatim | Load immediately |
| **Strong** | Description trigger words match ≥2 | Load immediately |
| **Partial** | Category matches, specific sub-skill unclear | Load closest + note gaps |
| **Weak** | Same domain but different focus | Load only if task is large |
| **None** | No relevant skill exists | Flag as skill gap |

## Step 4: Load Decision

```markdown
# CONSUME TOKENS WISELY
# Loading a skill costs ~200-2000 tokens per skill_view().
# Budget: you have ~8K-64K context depending on model.

# Priority order for loading:
1. HIGH — Skills that provide step-by-step procedures
2. MED — Skills with configuration snippets or commands  
3. LOW — Reference documentation or background info
4. SKIP — Things you already know confidently
```

## Multi-Skill Stacking

```markdown
# When a task needs multiple skills, load them in THIS order:
1. The MOST SPECIFIC skill first (highest relevance score)
2. The BROADEST skill last (general context)
3. Maximum 5 skills per /stack invocation
4. If you hit 5, evaluate: are ALL still needed?

# Example: "Deploy the app with monitoring"
# Stack: /kubernetes-deployment /prometheus-metrics-collection /grafana-dashboard-design
```

## Pitfalls
- **Overloading**: Loading >5 skills floods context — use progressive loading instead
- **False matches**: A skill named "python" might be about Python packaging, not Python language features
- **Missing the obvious**: Sometimes the best "skill" is your own general knowledge — not every task needs a skill
- **Recency bias**: Loading skills mentioned earlier in conversation even if no longer relevant — re-evaluate each turn

## Verification
```bash
# After loading, ask:
# - Does this skill's description match my task?
# - Does it have the commands/procedures I need?
# - Do I need additional skills to complete this?
```
