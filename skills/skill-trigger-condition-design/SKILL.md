---
name: skill-trigger-condition-design
description: Write clear trigger conditions that fire at the right time.
---

# Skill Trigger Condition Design

**Trigger**: Use when creating a skill to define when it should be loaded — the trigger condition that routes users to this skill.

## Anatomy of a Trigger

```markdown
Good trigger: "Use when deploying a Node.js app to production."
              → Clear, specific, actionable

Bad trigger:  "For deployments"
              → Vague, no hint of when to invoke

Great trigger: "Use when setting up CI/CD for the first time, or 
                when migrating from Jenkins to GitHub Actions."
              → Multiple entry points, common scenarios
```

## Trigger Formats

### Single Condition
```
Use when deploying a Python web app with Docker.
```

### Multiple Conditions
```
Use when migrating from REST to GraphQL, designing a new API, 
or adding rate limiting to existing endpoints.
```

### Platform-Specific
```
Use when debugging macOS build failures or Xcode project settings.
(Add `platforms: [macos]` to frontmatter)
```

## The Trigger Matching Test

```markdown
Trigger: "Use when deploying web apps with Docker to production."

✅ "I need to deploy my Flask app" → YES
✅ "Set up production hosting" → YES
❌ "Run my app locally" → NO
❌ "Build a Docker image for CI" → PARTIAL

PASS: 2 clear hits, 2 clear misses = good scope
FAIL: All 4 are "maybe" = scope too broad
```

## Best Practices

```markdown
1. START with "Use when" or a verb
   ✓ "Use when deploying..."
   ✓ "Debug memory leaks..."
   ✗ "This skill is for..." (too wordy)

2. BE SPECIFIC about context
   ✓ "Use when deploying Node.js apps with PM2"
   ✗ "Use when deploying apps" (which? where?)

3. INCLUDE the technology
   ✓ "Use when configuring nginx as a reverse proxy"
   ✗ "Use when configuring a reverse proxy" (which one?)

4. COVER the most common case first
   ✓ "Use when migrating to TypeScript, or adding types to JS"
   ✗ "Use for type systems" (too vague)
```

## Trigger + Description Alignment

```yaml
---
description: Deploy Node.js apps with PM2 to production servers.
#    ↑ matches trigger below ↑
---
## When to Use
**Trigger**: Use when deploying Node.js applications to production
using PM2 process manager, or setting up high-availability with
clustering and auto-restart.
```

## Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| No trigger | "Docker deployment" | "Use when deploying with Docker" |
| Too broad | "Use when coding" | "Use when writing Python CLI tools" |
| Too narrow | "Use only with Ubuntu 22.04" | "Use when deploying to Ubuntu" |
| Future tense | "Will help you deploy" | "Use when deploying" (present) |

## Pitfalls
- **Circular triggers**: "Use when you need this skill" — useless
- **Description mismatch**: Trigger says "deploy" but skill covers "debug" — confusing
- **Cross-agent search**: Triggers as search keywords help Codex/Claude find the skill

## Verification
```markdown
Read trigger aloud:
1. Starts with verb or "Use when"?
2. Mentions specific tool/technology?
3. Clear when someone would load this?
4. Would a search for "how do I X" find this?
```
