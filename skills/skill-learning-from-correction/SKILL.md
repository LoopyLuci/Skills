---
name: skill-learning-from-correction
description: Turn user corrections into skill improvements or new skills.
---

# Skill Learning from Correction

**Trigger**: Use when a user corrects your approach, shows a better way, or points out a mistake — convert that into skill knowledge.

## The Correction → Skill Pipeline

```
User correction or feedback
        │
   ┌────▼──────────────┐
   │ Was I using a     │
   │ skill when this   │──YES──► Patch the skill with correction
   │ happened?         │
   └────┬──────────────┘
        │ NO
   ┌────▼──────────────┐
   │ Is this a         │
   │ repeatable        │──YES──► Create a new skill
   │ procedure?        │
   └────┬──────────────┘
        │ NO
   ┌────▼──────────────┐
   │ Is this a         │
   │ personal          │──YES──► Save to memory, not skill
   │ preference?       │
   └────┬──────────────┘
        │ NO
   └──► Acknowledge, no action needed
```

## Correction Types

| Type | Example | Action |
|------|---------|--------|
| **Command error** | "Use `docker compose` not `docker-compose`" | Patch skill's commands |
| **Wrong approach** | "We use Helm, not raw k8s YAML" | Patch skill's procedure |
| **Missing step** | "You need to set up RBAC first" | Add step to skill |
| **Wrong tool** | "We use PostgreSQL not MySQL" | Add context to skill |
| **Order error** | "Tests before lint, not after" | Reorder skill steps |
| **Pitfall discovered** | "That flag is deprecated in v2" | Add pitfall to skill |
| **New workflow** | "We always add this config after deploy" | Create new skill |

## Correction Capture Template

```markdown
CORRECTION CAPTURE
──────────────────
What I did wrong:   <description>
Correct approach:   <what user said>
Applies to skill:  <skill-name if applicable>
Category:          command/approach/step/tool/order/pitfall
Action taken:      patched/created/noted/saved to memory
---
```

## Example: Patching a Skill from Correction

```markdown
CONTEXT:
- User asked me to deploy a Node.js app
- I used docker-compose-patterns skill
- User: "We use `docker compose` v2, not docker-compose"

ACTION:
skill_manage(
  action="patch",
  name="docker-compose-patterns",
  old_string="docker-compose up -d",
  new_string="docker compose up -d"
)

Also check for all other `docker-compose` references in the skill
and update them — the old CLI is deprecated across the board.
```

## Example: Creating a Skill from Correction

```markdown
CONTEXT:
- User corrected me on their team's deploy process 3 times
- Process: feature branch → staging → QA → prod
- Has 6 clear steps with approval gates

ACTION:
Propose: "I notice I've been corrected on the deployment process
a few times. Should I create a 'team-deploy-process' skill so I
get it right every time?"
```

## When to Save to Memory vs. Skill

```markdown
SAVE TO MEMORY (not skill):
- User preference ("I prefer tabs not spaces")
- Personal details ("I use Chrome not Firefox")
- One-off context ("This project uses port 8080")

SAVE AS SKILL:
- Repeatable procedures (5+ steps, reusable)
- Technical workflows (deploy, migrate, configure)
- Domain knowledge (API endpoints, tool-specific commands)

Memory = small durable facts
Skill = longer procedures loaded on demand
```

## Pitfalls
- **Over-correction**: Not every correction needs a skill update — one-off context goes in memory
- **Premature patching**: Patching a skill mid-task when the issue might be specific to this context
- **Confirmation required**: Don't silently patch skills — confirm with user or use write_approval gate
- **Skill scope expansion**: Patching "fix a bug in Python" with deployment info makes the skill unfocused

## Verification
```markdown
After a correction-led update:
- Does the skill now reflect the correct approach?
- Did I check all instances of the old pattern (not just the first)?
- Should I inform the user that the skill was updated?
```
