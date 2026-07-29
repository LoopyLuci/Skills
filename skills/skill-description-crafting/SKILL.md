---
name: skill-description-crafting
description: Write trigger-based 60-char descriptions for skill routing.
---

# Skill Description Crafting

**Trigger**: Use when creating or editing a skill to write its description field — the single most important metadata element for skill discoverability.

## Why 60 Characters?

The skill system prompt index shows every skill's description at Level 0 (skills_list). Descriptions over 60 chars are truncated to 57 + "...", destroying the trigger signal. A good description is the difference between the agent finding your skill or ignoring it.

## The Formula

```
[Action verb] [target] [context].
```

| Element | Example |
|---------|---------|
| Action verb | "Use when", "Build", "Deploy", "Debug" |
| Target | "Docker containers", "React apps" |
| Context | "with health checks", "in production" |

## Templates by Pattern

### "Use when..." (recommended)
```
Use when deploying FastAPI apps with Docker.
Use when debugging memory leaks in Python.
Use when migrating from REST to GraphQL APIs.
```

### "[Action] [noun] for [purpose]"
```
Deploy web apps to Kubernetes with zero downtime.
Migrate databases from MySQL to PostgreSQL.
Optimize Docker images for smaller build sizes.
```

### "[Tool] — [action]"
```
Docker — build, optimize, and deploy containers.
PostgreSQL — query optimization and indexing.
Git — resolve merge conflicts and rebase commits.
```

## Before and After

```
BEFORE (72 chars — TRUNCATED):
"Use this skill when you need to deploy a Docker container
to a Kubernetes cluster with proper health checks"

DISPLAYS AS:
"Use this skill when you need to deploy a Docker container t..."

AFTER (58 chars — FULLY VISIBLE):
"Deploy Docker containers to Kubernetes with health checks."
```

## Common Mistakes

| Mistake | Example | Problem |
|---------|---------|---------|
| No verb | "Docker container deployment" | Unclear when to use |
| Too vague | "Use when needed" | Zero signal |
| Too specific | "Use with Ubuntu 22.04 on AWS EC2" | Never matches |
| Future tense | "Will help you deploy apps" | Weak trigger |
| First person | "I can help you deploy things" | Unclear scope |
| No trigger | "Comprehensive guide to Docker" | No "when" signal |

## Testing Your Description

```markdown
1. Read aloud — starts with verb or "Use when"?
2. Count chars — ≤60 including spaces and period?
3. Unique — sounds different from other skills?
4. Trigger match — if I say "I need X", does this match?
5. Platform — would it work on all platforms?

PASS (57 chars): "Use when deploying Python microservices to k8s."
FAIL (63 chars): "Python microservice deployment on Kubernetes" (no verb)
```

## Verification
```bash
echo -n "Your description here." | wc -c
echo "Deploy apps to production." | grep -qE "^(Use when|[A-Z][a-z]+ )"
```
