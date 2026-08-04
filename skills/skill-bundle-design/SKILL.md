---

name: skill-bundle-design
description: Design skill bundles for recurring multi-skill workflows.

---

# Skill Bundle Design

**Trigger**: Use when you find yourself using the same 2-5 skills together repeatedly and want a single-command shortcut.

## When to Create a Bundle

```markdown
CREATE a bundle when:
- Same 3+ skills used together 3+ times
- The combination defines a distinct "task type"
- A single slash command would save 5+ seconds of typing
- You want to share a workflow template with your team

DON'T CREATE a bundle when:
- Skills are never used together
- The bundle would have only 1 skill (just use the skill)
- The combination is accidental (won't repeat)
```

## Bundle Anatomy

```yaml
# ~/.hermes/skill-bundles/backend-dev.yaml
name: backend-dev
description: Backend feature work — review, test, PR.
skills:
  - github-code-review
  - test-driven-development
  - github-pr-workflow
instruction: |
  Always start by writing failing tests, then implement.
  Open the PR through the standard workflow with co-author tags.
```

### Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | No (defaults to filename) | Slash command slug |
| `description` | No | Shown in `/bundles` list |
| `skills` | Yes | Ordered list of skill names |
| `instruction` | No | Extra guidance prepended to skills |

## Design Principles

### 1. Task-Oriented, Not Topic-Oriented
```
GOOD: "Build a new API endpoint" bundle
  → github-code-review, test-driven-development, fastapi-api-development

BAD: "Python" bundle
  → python-advanced-patterns, python-testing-advanced, python-async-patterns
  (Too broad — these are rarely all needed at once)
```

### 2. Progressive Depth
```
LAYERED BUNDLES:

/dev-backend    → code-review + tdd + fastapi (slim — everyday use)
/dev-backend+   → above + database-design + caching (full — complex features)
```
Start with core, create variants for depth.

### 3. Dependency Order
Skills should be listed in execution order, not importance order:
```yaml
# WRONG — testing before code exists
skills: [python-testing, python-coding, python-deploy]

# RIGHT — chronological order
skills: [python-coding, python-testing, python-deploy]
```

## Bundle Patterns

### Full Stack Feature
```yaml
name: fullstack-feature
description: Ship a full-stack feature — frontend to deploy.
skills:
  - frontend-bootstrap
  - fastapi-api-development
  - test-driven-development
  - dockerfile-optimization
  - github-pr-workflow
```

### Incident Response
```yaml
name: incident-response
description: Debug, fix, and deploy a hotfix in production.
skills:
  - systematic-debugging
  - git-bisect-debugging
  - github-pr-workflow
  - git-tag-release
instruction: |
  This is a production incident. Work fast but carefully.
  Document everything in the PR. Add monitoring after fix.
```

### DevOps Pipeline
```yaml
name: devops-pipeline
description: Set up CI/CD pipeline with monitoring.
skills:
  - github-actions-workflows
  - dockerfile-optimization
  - kubernetes-deployment
  - prometheus-metrics-collection
  - grafana-dashboard-design
```

## Managing Bundles

```bash
# Create
hermes bundles create backend-dev \
  --skill github-code-review \
  --skill test-driven-development \
  --skill github-pr-workflow \
  -d "Backend feature work"

# List
hermes bundles list

# Show details
hermes bundles show backend-dev

# Edit (recreate with --force)
hermes bundles create backend-dev --skill new-skill --force

# Delete
hermes bundles delete backend-dev
```

## Pitfalls
- **Bundle divergence**: Skills in a bundle evolve independently — a skill might become irrelevant to the bundle over time
- **Over-bundling**: 20 bundles when 5 would do — each bundle should cover a distinct task type
- **Missing skills**: Bundle references a skill that doesn't exist — it's silently skipped
- **Bundle vs automatic stacking**: `/skill1 /skill2 /skill3` does the same thing — bundles just save typing
- **Team sharing**: Bundle YAML can be checked into a dotfiles repo — `~/.hermes/skill-bundles/` is the path

## Verification
```bash
hermes bundles list                    # All bundles
hermes bundles show my-bundle          # Verify contents
# In chat:
/bundles                               # List all bundles
/my-bundle test the auth endpoint      # Test it
```
