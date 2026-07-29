---
name: skill-automatic-invocation
description: Decide when to load a skill proactively vs. waiting.
---

# Skill Automatic Invocation

**Trigger**: Use when deciding whether to proactively load a skill before the user asks, or wait for them to request it.

## When to Auto-Invoke

```markdown
AUTO-INVOKE (load without being asked) when:

1. The user's request STRONGLY matches a skill
   "Deploy my app" → auto-load kubernetes-deployment
   
2. The task has HIGH STAKES and needs guidance
   "Delete the production database" → auto-load database-backup
   
3. You're about to write CODE or CONFIG
   "Add authentication" → auto-load oauth-patterns
   
4. The domain is COMPLEX and unfamiliar
   "Set up a VPN" → auto-load vpn-implementation

WAIT when:
1. Multiple skills could match and you're unsure
2. The task is SIMPLE and well-known
3. The user says "just do it, don't ask"
4. The domain changes mid-conversation
```

## The Decision Tree

```
User request arrives
        │
   ┌────▼───────────────┐
   │ Strong match to    │
   │ exactly one skill? │──YES──► Auto-invoke
   └────┬───────────────┘
        │ NO
   ┌────▼───────────────┐
   │ Multiple matches?  │──YES──► Load one most likely
   └────┬───────────────┘
        │ NO
   ┌────▼───────────────┐
   │ Risky/complex?     │──YES──► Load safety skill
   └────┬───────────────┘
        │ NO → proceed without skill
```

## Examples

### Clear Auto-Invoke
```markdown
USER: "Create a PR from my feature branch"
YOU: "Let me use the PR workflow skill..."
(auto-loads github-pr-workflow)

USER: "Set up monitoring for the web app"
YOU: "Loading prometheus and grafana skills..."
(auto-loads both)
```

### When NOT to Auto-Invoke
```markdown
USER: "Can you help me with my project?"
→ DON'T — too vague, ask what they need

USER: "Fix this bug" (looking at Python code)
→ DON'T — could be 20 different skills, ask first
```

## The Check-First Pattern

```markdown
When unsure, ask:

"I think <skill-name> would be useful here.
Shall I load it?"

This:
- Shows you're thinking ahead
- Lets them correct your assumption
- Avoids wasting tokens on wrong skill
```

## Context-Based Auto-Invoke

```markdown
FIRST INTERACTION:
  "Let me start a new project"
  → Auto-load project-scaffolding (safe bet)

MID-SESSION:
  "Now I need to deploy this"
  → Auto-load deployment skill (natural next step)

DEBUGGING:
  "This error keeps happening"
  → Auto-load debugging skill (continuation)

AFTER CORRECTION:
  "Actually, use Helm not raw YAML"
  → Auto-load helm-chart-development (course correction)
```

## Pitfalls
- **Premature loading**: Loading skills before full context — wait for user to finish describing
- **Token waste**: Auto-loading a skill the user then rejects — verify before committing
- **Ignoring the obvious**: Loading a skill when you clearly know it — demonstrates low confidence
- **User annoyance**: Some users don't want to see skill loading — "just do it"

## Verification
```markdown
After auto-invoking:
- Right skill? (Would user have chosen it?)
- Saved time vs. not loading?
- Did user acknowledge it helped?
```
